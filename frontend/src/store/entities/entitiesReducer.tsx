import { combineReducers } from "redux";
import jokesReducer from "./jokes/jokes.slice";
import jokeNewsletterReducer from "./jokeNewsletter/jokeNewsletter.slice";
import contactReducer from "./contact/contact.slice";

export default combineReducers({
    jokes: jokesReducer,
    jokeNewsletter: jokeNewsletterReducer,
    contact: contactReducer
});
