import { IJokePicture } from "@/types";

const MEDIA_BASE_URL = import.meta.env.VITE_API_MEDIA_BASE_URL;

const absolute = (path: string | null | undefined) =>
    path ? MEDIA_BASE_URL + path : undefined;

/**
 * Builds the <img> source attributes for a joke picture.
 *
 * Falls back to the original upload whenever a generated variant is missing,
 * so pictures created before the variant pipeline keep working.
 */
export const jokeImageSources = (picture: IJokePicture) => {
    const original = absolute(picture.image) as string;
    const w400 = absolute(picture.variants?.w400_webp);
    const w800 = absolute(picture.variants?.w800_webp) ?? absolute(picture.variants?.w800_jpg);

    const srcSet = [w400 ? `${w400} 400w` : null, w800 ? `${w800} 800w` : null]
        .filter(Boolean)
        .join(", ");

    return {
        src: absolute(picture.variants?.w800_jpg) ?? original,
        srcSet: srcSet || undefined,
    };
};
