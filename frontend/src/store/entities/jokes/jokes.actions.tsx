import * as jokesSlice from "./jokes.slice";
import { apiRequest } from "@/common/utils/constants/api.constants";
import * as jokesEndpoints from "@/assets/endpoints/api/jokesEndpoints";

export const fetchJokeOfTheDay = () =>
  apiRequest({
    url: jokesEndpoints.getJokeOfTheDayUrl(),
    onStart: jokesSlice.jokeOfTheDayRequested.type,
    onSuccess: jokesSlice.jokeOfTheDayReceived.type,
    onError: jokesSlice.jokeOfTheDayRequestFailed.type,
  });

export const fetchJokesWithPicturesPaginated = (
  page: number = 1,
  page_size: number = 50
) =>
  apiRequest({
    url: jokesEndpoints.getJokesWithPicturesPaginatedUrl(page, page_size),
    onStart: jokesSlice.jokesWithPicturesPaginatedRequested.type,
    onSuccess: jokesSlice.jokesWithPicturesPaginatedReceived.type,
    onError: jokesSlice.jokesWithPicturesPaginatedRequestFailed.type,
  });

export const submitJoke = (joke: string) =>
  apiRequest({
    url: jokesEndpoints.getSubmitJokeUrl(),
    method: "post",
    onStart: jokesSlice.jokeSubmitPending.type,
    onSuccess: jokesSlice.jokeSubmitFulfilled.type,
    onError: jokesSlice.jokeSubmitFailed.type,
    data: { text: joke }
  });
