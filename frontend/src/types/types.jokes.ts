export interface IJoke {
    id: number;
    text: string;
    created_at: string;
    created_by: {
        username: string;
    }
    joke_of_the_day_selection_weight: number;
    joke_picture: IJokePicture | null;
}

export interface IJokePicture {
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