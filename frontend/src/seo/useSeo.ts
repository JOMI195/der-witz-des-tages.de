import { useEffect } from "react";
import { useLocation, useSearchParams } from "react-router-dom";
import { useAppSelector } from "@/store";
import { getJokesWithPicturesPaginated } from "@/store/entities/jokes/jokes.slice";
import { getArchiveUrl } from "@/assets/endpoints/app/appEndpoints";
import { OG_IMAGE, SITE_NAME, SITE_ORIGIN, canonicalUrl, findPageMeta } from "./pageMeta";

const upsertMeta = (attribute: "name" | "property", key: string, content?: string) => {
  const existing = document.head.querySelector<HTMLMetaElement>(`meta[${attribute}="${key}"]`);

  if (!content) {
    existing?.remove();
    return;
  }

  if (existing) {
    existing.content = content;
    return;
  }

  const meta = document.createElement("meta");
  meta.setAttribute(attribute, key);
  meta.content = content;
  document.head.appendChild(meta);
};

const upsertLink = (rel: string, href?: string) => {
  const existing = document.head.querySelector<HTMLLinkElement>(`link[rel="${rel}"]`);

  if (!href) {
    existing?.remove();
    return;
  }

  if (existing) {
    existing.href = href;
    return;
  }

  const link = document.createElement("link");
  link.rel = rel;
  link.href = href;
  document.head.appendChild(link);
};

const GALLERY_PATH = `/${getArchiveUrl()}`;

const useSeo = () => {
  const { pathname } = useLocation();
  const [searchParams] = useSearchParams();
  const paginatedJokes = useAppSelector(getJokesWithPicturesPaginated);

  const pageParam = Number(searchParams.get("page")) || 1;
  const hasNextPage = Boolean(paginatedJokes.next);

  useEffect(() => {
    const page = findPageMeta(pathname);
    const isGallery = page.path === GALLERY_PATH;
    const galleryPageUrl = (pageNumber: number) =>
      pageNumber > 1 ? `${canonicalUrl(page.path)}?page=${pageNumber}` : canonicalUrl(page.path);

    const url = isGallery ? galleryPageUrl(pageParam) : canonicalUrl(page.path);
    const image = SITE_ORIGIN + OG_IMAGE;
    const title =
      isGallery && pageParam > 1 ? `${page.title} – Seite ${pageParam}` : page.title;

    document.title = title;
    upsertLink("canonical", url);
    upsertLink("prev", isGallery && pageParam > 1 ? galleryPageUrl(pageParam - 1) : undefined);
    upsertLink("next", isGallery && hasNextPage ? galleryPageUrl(pageParam + 1) : undefined);

    upsertMeta("name", "description", page.description);
    upsertMeta("name", "robots", page.noindex ? "noindex, nofollow" : "index, follow");

    upsertMeta("property", "og:type", "website");
    upsertMeta("property", "og:site_name", SITE_NAME);
    upsertMeta("property", "og:locale", "de_DE");
    upsertMeta("property", "og:url", url);
    upsertMeta("property", "og:title", title);
    upsertMeta("property", "og:description", page.description);
    upsertMeta("property", "og:image", image);

    upsertMeta("name", "twitter:card", "summary_large_image");
    upsertMeta("name", "twitter:title", title);
    upsertMeta("name", "twitter:description", page.description);
    upsertMeta("name", "twitter:image", image);
  }, [pathname, pageParam, hasNextPage]);
};

export default useSeo;
