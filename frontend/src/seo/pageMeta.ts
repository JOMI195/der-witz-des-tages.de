export const SITE_NAME = "Der Witz des Tages";
export const SITE_ORIGIN = "https://www.der-witz-des-tages.de";
export const OG_IMAGE = "/android-chrome-512x512.png";

export interface PageMeta {
  path: string;
  title: string;
  description?: string;
  prerender?: boolean;
  noindex?: boolean;
  matchPrefix?: boolean;
}

export const pages: PageMeta[] = [
  {
    path: "/",
    title: "Der Witz des Tages – täglich ein neuer Flachwitz",
    description:
      "Jeden Morgen ein neuer Flachwitz mit passendem Bild – auf der Website und als kostenloser Newsletter. Heute schon gelacht?",
    prerender: true,
  },
  {
    path: "/galerie/",
    title: "Witze Galerie – alle Witze des Tages",
    description:
      "Alle bisherigen Witze des Tages mit ihren Bildern: durchstöbere die Galerie und finde deinen Lieblingswitz.",
    prerender: true,
  },
  {
    path: "/witz-einreichen/",
    title: "Witz einreichen – werde Teil vom Witz des Tages",
    description:
      "Du hast einen guten Flachwitz? Reiche ihn ein und werde vielleicht schon morgen mit deinem Witz des Tages gefeatured.",
    prerender: true,
  },
  {
    path: "/kontakt/",
    title: "Kontakt – Der Witz des Tages",
    description:
      "Fragen, Anregungen oder einen Bug gefunden? Schreib uns über das Kontaktformular – wir melden uns zurück.",
    prerender: true,
  },
  {
    path: "/datenschutzerklaerung/",
    title: "Datenschutzerklärung – Der Witz des Tages",
    description:
      "Wie Der Witz des Tages personenbezogene Daten verarbeitet: Newsletter, Nutzerkonto, Reichweitenmessung und deine Rechte nach DSGVO.",
    prerender: true,
  },
  {
    path: "/impressum/",
    title: "Impressum – Der Witz des Tages",
    description:
      "Anbieterkennzeichnung nach § 5 TMG: Herausgeber, Kontaktdaten und Urheberrechtshinweise zu der-witz-des-tages.de.",
    prerender: true,
  },
  { path: "/auth/", title: "Anmelden – Der Witz des Tages", noindex: true, matchPrefix: true },
  { path: "/settings/", title: "Einstellungen – Der Witz des Tages", noindex: true, matchPrefix: true },
  {
    path: "/joke-newsletter/",
    title: "Newsletter – Der Witz des Tages",
    noindex: true,
    matchPrefix: true,
  },
  { path: "/comingSoon/", title: "Bald verfügbar – Der Witz des Tages", noindex: true },
];

export const prerenderedPages = pages.filter((page) => page.prerender);

export const canonicalUrl = (path: string) => SITE_ORIGIN + path;

const normalizePath = (pathname: string) => {
  const withLeading = pathname.startsWith("/") ? pathname : `/${pathname}`;
  return withLeading.endsWith("/") ? withLeading : `${withLeading}/`;
};

export const findPageMeta = (pathname: string): PageMeta => {
  const path = normalizePath(pathname);

  const exact = pages.find((page) => page.path === path);
  if (exact) return exact;

  const prefixed = pages
    .filter((page) => page.matchPrefix && path.startsWith(page.path))
    .sort((a, b) => b.path.length - a.path.length)[0];
  if (prefixed) return prefixed;

  return {
    path,
    title: "Seite nicht gefunden – Der Witz des Tages",
    prerender: false,
    noindex: true,
  };
};
