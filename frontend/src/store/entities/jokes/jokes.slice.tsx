import { RootState } from "@/store";
import { IJoke, IJokesWithPicturesPaginated } from "@/types";
import { createSlice } from "@reduxjs/toolkit";

type SliceState = {
  api: {
    loading: boolean;
    lastFetch: number | null;
  };
  joke_of_the_day: IJoke;
  jokes_with_pictures_paginated: IJokesWithPicturesPaginated;
};

const initialState: SliceState = {
  api: {
    loading: false,
    lastFetch: null,
  },
  joke_of_the_day: {
    id: 0,
    text: "",
    created_at: "",
    created_by: {
      username: "",
    },
    joke_picture: null,
    joke_of_the_day_selection_weight: 1
  },
  jokes_with_pictures_paginated: {
    count: 0,
    next: null,
    previous: null,
    page: 1,
    results: []
  }
};

const jokesSlice = createSlice({
  name: "jokes",
  initialState,
  reducers: {
    jokeOfTheDayRequested: (jokes) => {
      jokes.api.loading = true;
    },
    jokeOfTheDayReceived: (jokes, action) => {
      jokes.joke_of_the_day = action.payload;
      jokes.api.lastFetch = Date.now();
      jokes.api.loading = false;
    },
    jokeOfTheDayRequestFailed: (jokes) => {
      jokes.api.loading = false;
    },
    jokesWithPicturesPaginatedRequested: (jokes) => {
      jokes.api.loading = true;
    },
    jokesWithPicturesPaginatedReceived: (jokes, action) => {
      jokes.jokes_with_pictures_paginated = {
        ...action.payload,
        page: jokes.jokes_with_pictures_paginated.page,
      };
      jokes.api.lastFetch = Date.now();
      jokes.api.loading = false;
    },
    jokesWithPicturesPaginatedRequestFailed: (jokes) => {
      jokes.api.loading = false;
    },
    jokesWithPicturesPaginatedPageSet: (jokes, action) => {
      jokes.jokes_with_pictures_paginated.page = action.payload;
    },
    jokeSubmitPending: (jokes) => {
      jokes.api.loading = true;
    },
    jokeSubmitFulfilled: (jokes) => {
      jokes.api.lastFetch = Date.now();
      jokes.api.loading = false;
    },
    jokeSubmitFailed: (jokes) => {
      jokes.api.loading = false;
    },
  },
});

export const {
  jokeOfTheDayRequested,
  jokeOfTheDayReceived,
  jokeOfTheDayRequestFailed,
  jokesWithPicturesPaginatedRequested,
  jokesWithPicturesPaginatedReceived,
  jokesWithPicturesPaginatedRequestFailed,
  jokesWithPicturesPaginatedPageSet,
  jokeSubmitPending,
  jokeSubmitFailed,
  jokeSubmitFulfilled
} = jokesSlice.actions;
export default jokesSlice.reducer;

export const getApi = (state: RootState) => state.entities.jokes.api;
export const getJokeOfTheDay = (state: RootState) => state.entities.jokes.joke_of_the_day;
export const getJokesWithPicturesPaginated = (state: RootState) => state.entities.jokes.jokes_with_pictures_paginated;
