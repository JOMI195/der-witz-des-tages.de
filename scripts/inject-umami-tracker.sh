#!/bin/bash

# Injects the umami tracking snippet into the index.html served by the running
# nginx container. Resolves the website id through the umami REST API and
# creates the website if it does not exist yet.
#
# The nginx container filesystem is ephemeral: any `up --build`,
# `up --force-recreate` or recreate-from-image wipes the injection, which is why
# app-command.sh re-runs this after every `up`.
#
# Input Variables (read from the env file):
#   UMAMI_URL              - public base URL of the umami vhost
#   UMAMI_TRACKER_SCRIPT_NAME - tracker script name (umami rewrites it to /script.js)
#   UMAMI_USER             - umami admin username
#   UMAMI_PASSWORD         - umami admin password
#   UMAMI_WEBSITE_NAME     - display name of the tracked website
#   UMAMI_WEBSITE_DOMAIN   - hostname of the tracked website

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <docker-compose-file> <env-file>"
  exit 1
fi

DOCKER_COMPOSE_FILE="$1"
ENV_FILE="$2"

if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
  echo "Error: Docker Compose file '$DOCKER_COMPOSE_FILE' not found!"
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: Environment file '$ENV_FILE' not found!"
  exit 1
fi

# Sourcing keeps quoted values and ${VAR} interpolation intact.
set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

for var in UMAMI_URL UMAMI_TRACKER_SCRIPT_NAME UMAMI_USER UMAMI_PASSWORD \
           UMAMI_WEBSITE_NAME UMAMI_WEBSITE_DOMAIN; do
  if [ -z "${!var}" ]; then
    echo "Error: '$var' is not set in '$ENV_FILE'!"
    exit 1
  fi
done

# Only consumed at build time, but compose warns when it is unset.
export VITE_APP_BUILD_VERSION="${VITE_APP_BUILD_VERSION:-}"

COMPOSE="docker compose -f $DOCKER_COMPOSE_FILE --env-file $ENV_FILE"

# container_name is not set in every compose file, so resolve by service name.
UMAMI_CID=$($COMPOSE ps -q umami)
NGINX_CID=$($COMPOSE ps -q nginx)

if [ -z "$UMAMI_CID" ]; then
  echo "Error: umami container is not running!"
  exit 1
fi

if [ -z "$NGINX_CID" ]; then
  echo "Error: nginx container is not running!"
  exit 1
fi

echo "### Waiting for umami ..."
READY=0
for _ in $(seq 1 60); do
  if docker exec "$UMAMI_CID" curl -fsS http://127.0.0.1:3000/api/heartbeat > /dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 2
done

if [ "$READY" != "1" ]; then
  echo "Error: umami did not become ready in time!"
  exit 1
fi

echo "### Resolving website id for '$UMAMI_WEBSITE_DOMAIN' ..."
# Runs inside the container so no port needs publishing and the host needs no
# JSON tooling. Node 18 has a global fetch.
WEBSITE_ID=$(docker exec \
  -e UMAMI_USER="$UMAMI_USER" \
  -e UMAMI_PASSWORD="$UMAMI_PASSWORD" \
  -e UMAMI_WEBSITE_NAME="$UMAMI_WEBSITE_NAME" \
  -e UMAMI_WEBSITE_DOMAIN="$UMAMI_WEBSITE_DOMAIN" \
  "$UMAMI_CID" node -e '
// 127.0.0.1, not localhost: undici resolves localhost to ::1 and umami listens on IPv4.
const api = "http://127.0.0.1:3000/api";

async function call(path, options = {}) {
  const res = await fetch(api + path, options);
  if (!res.ok) {
    throw new Error(`${options.method || "GET"} ${path} -> ${res.status} ${await res.text()}`);
  }
  return res.json();
}

(async () => {
  const { token } = await call("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: process.env.UMAMI_USER,
      password: process.env.UMAMI_PASSWORD,
    }),
  });

  const auth = { Authorization: `Bearer ${token}` };
  const domain = process.env.UMAMI_WEBSITE_DOMAIN;

  const websites = await call("/websites", { headers: auth });
  const list = Array.isArray(websites) ? websites : websites.data;
  const existing = list.find(w => w.domain === domain);

  if (existing) {
    process.stdout.write(existing.id);
    return;
  }

  const created = await call("/websites", {
    method: "POST",
    headers: { ...auth, "Content-Type": "application/json" },
    body: JSON.stringify({ name: process.env.UMAMI_WEBSITE_NAME, domain }),
  });
  process.stdout.write(created.id);
})().catch(e => {
  console.error(e.message);
  process.exit(1);
});
')

if [ -z "$WEBSITE_ID" ]; then
  echo "Error: could not resolve the umami website id!"
  exit 1
fi

echo "### Injecting tracker for website $WEBSITE_ID ..."
SNIPPET="  <!-- umami:start -->
  <script defer src=\"${UMAMI_URL}/${UMAMI_TRACKER_SCRIPT_NAME}\" data-website-id=\"${WEBSITE_ID}\"></script>
  <!-- umami:end -->"

printf '%s\n' "$SNIPPET" | docker exec -i "$NGINX_CID" sh -c 'cat > /tmp/umami-snippet.html'

# Delete before insert so reruns stay idempotent and a changed id is picked up.
# Kept busybox-safe: no GNU-only sed commands.
docker exec "$NGINX_CID" sh -c '
  set -e
  f=/usr/share/nginx/html/index.html
  sed -i "/<!-- umami:start -->/,/<!-- umami:end -->/d" "$f"
  awk "/<\/head>/ { while ((getline l < \"/tmp/umami-snippet.html\") > 0) print l } { print }" \
      "$f" > "$f.new"
  mv "$f.new" "$f"
  chmod 644 "$f"
  rm -f /tmp/umami-snippet.html
  # Stale precompressed copy would disagree with the patched index.html.
  rm -f "$f.br"
'

if [ $? -ne 0 ]; then
  echo "Error: failed to patch index.html in the nginx container!"
  exit 1
fi

echo "### Injected:"
docker exec "$NGINX_CID" grep -A1 "umami:start" /usr/share/nginx/html/index.html
