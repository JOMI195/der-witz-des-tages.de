import { RootState } from "@/store";
import { createSlice } from "@reduxjs/toolkit";

type SliceState = {
  api: {
    loading: boolean;
    lastFetch: number | null;
  };
};

const initialState: SliceState = {
  api: {
    loading: false,
    lastFetch: null,
  },
};

const jokeNewsletterSlice = createSlice({
  name: "jokeNewsletter",
  initialState,
  reducers: {
    subscribeToNewsletterRequested: (jokes) => {
      jokes.api.loading = true;
    },
    subscribeToNewsletterFulfilled: (jokes, _action) => {
      jokes.api.lastFetch = Date.now();
      jokes.api.loading = false;
    },
    subscribeToNewsletterFailed: (jokes) => {
      jokes.api.loading = false;
    },
    unsubscribeFromNewsletterRequested: (jokes) => {
      jokes.api.loading = true;
    },
    unsubscribeFromNewsletterFulfilled: (jokes, _action) => {
      jokes.api.lastFetch = Date.now();
      jokes.api.loading = false;
    },
    unsubscribeFromNewsletterFailed: (jokes) => {
      jokes.api.loading = false;
    },
    activateJokeNewsletterSubscriptionRequested: (jokes) => {
      jokes.api.loading = true;
    },
    activateJokeNewsletterSubscriptionFulfilled: (jokes, _action) => {
      jokes.api.lastFetch = Date.now();
      jokes.api.loading = false;
    },
    activateJokeNewsletterSubscriptionFailed: (jokes) => {
      jokes.api.loading = false;
    },
  },
});

export const {
  subscribeToNewsletterRequested,
  subscribeToNewsletterFulfilled,
  subscribeToNewsletterFailed,
  unsubscribeFromNewsletterRequested,
  unsubscribeFromNewsletterFulfilled,
  unsubscribeFromNewsletterFailed,
  activateJokeNewsletterSubscriptionRequested,
  activateJokeNewsletterSubscriptionFulfilled,
  activateJokeNewsletterSubscriptionFailed
} = jokeNewsletterSlice.actions;
export default jokeNewsletterSlice.reducer;

export const getApi = (state: RootState) => state.entities.jokeNewsletter.api;
