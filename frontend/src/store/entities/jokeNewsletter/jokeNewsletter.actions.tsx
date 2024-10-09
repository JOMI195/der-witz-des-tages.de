import * as jokesSlice from "./jokeNewsletter.slice";
import { apiRequest } from "@/common/utils/constants/api.constants";
import * as jokeNewsletterEndpoints from "@/assets/endpoints/api/jokeNewsletterEndpoints";

export const subscribeToJokeNewsletter = (email: string) =>
  apiRequest({
    url: jokeNewsletterEndpoints.getJokeNewsletterRecieverUrl(),
    method: "post",
    onStart: jokesSlice.subscribeToNewsletterRequested.type,
    onSuccess: jokesSlice.subscribeToNewsletterFulfilled.type,
    onError: jokesSlice.subscribeToNewsletterFailed.type,
    data: { email: email }
  });

export const unsubscribeFromJokeNewsletter = (unsubscribe_token: string) =>
  apiRequest({
    url: jokeNewsletterEndpoints.getJokeNewsletterUnsubscribeUrl(),
    method: "post",
    onStart: jokesSlice.unsubscribeFromNewsletterRequested.type,
    onSuccess: jokesSlice.unsubscribeFromNewsletterFulfilled.type,
    onError: jokesSlice.unsubscribeFromNewsletterFailed.type,
    data: { unsubscribe_token: unsubscribe_token }
  });

export const activateJokeNewsletterSubscription = (activation_token: string) =>
  apiRequest({
    url: jokeNewsletterEndpoints.getJokeNewsletterActivationUrl(),
    method: "post",
    onStart: jokesSlice.activateJokeNewsletterSubscriptionRequested.type,
    onSuccess: jokesSlice.activateJokeNewsletterSubscriptionFulfilled.type,
    onError: jokesSlice.activateJokeNewsletterSubscriptionFailed.type,
    data: { activation_token: activation_token }
  });