export interface IJoke {
    id: number;
    text: string;
    created_at: string;
    created_by: {
        username: string;
    }
    joke_picture: IJokePicture | null;
    shareable_image: IShareableImage | null;
    joke_of_the_day_created_at: string | null;
}

export interface IJokePictureVariants {
    w400_webp: string | null;
    w800_webp: string | null;
    w800_jpg: string | null;
}

export interface IJokePicture {
    image: string;
    created_at: string;
    variants?: IJokePictureVariants | null;
}

export interface IShareableImage {
    image: string;
    created_at: string;
}

export interface IJokesWithPicturesPaginated {
    count: number;
    next: string | null;
    previous: string | null;
    page: number;
    results: IJoke[];
};