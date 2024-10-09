import { combineReducers } from "redux";

import authReducer from "./authentication/authentication.slice";
import navigationReducer from "./navigation/navigation.slice";
import settingsReducer from "./settings/settings.slice";
import jokeNewsletterReducer from "./jokeNewsletter/jokeNewsletter.slice";
import jokesReducer from "./jokes/jokes.slice";
import contactReducer from "./contact/contact.slice";

export default combineReducers({
  navigation: navigationReducer,
  settings: settingsReducer,
  auth: authReducer,
  jokeNewsletter: jokeNewsletterReducer,
  jokes: jokesReducer,
  contact: contactReducer,
});
