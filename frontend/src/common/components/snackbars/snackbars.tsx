import AuthenticationAlertSnackbar from "../snackbars/alertSnackbar";
import AuthenticationLoadingSnackbar from "../snackbars/loadingSnackbar";
import JokeNewsletterAlertSnackbar from "../snackbars/alertSnackbar";
import JokeNewsletterLoadingSnackbar from "../snackbars/loadingSnackbar";
import JokesAlertSnackbar from "../snackbars/alertSnackbar";
import JokesLoadingSnackbar from "../snackbars/loadingSnackbar";
import ContactAlertSnackbar from "../snackbars/alertSnackbar";
import ContactLoadingSnackbar from "../snackbars/loadingSnackbar";
import { closeAuthAlertSnackbar, closeAuthLoadingSnackbar, getAuthSnackbar } from "@/store/ui/authentication/authentication.slice";
import { Box } from "@mui/material";
import { Outlet } from "react-router-dom";
import { closeJokeNewsletterAlertSnackbar, closeJokeNewsletterLoadingSnackbar, getJokeNewsletterSnackbar } from "@/store/ui/jokeNewsletter/jokeNewsletter.slice";
import { closeJokesAlertSnackbar, closeJokesLoadingSnackbar, getJokesSnackbar } from "@/store/ui/jokes/jokes.slice";
import { closeContactAlertSnackbar, closeContactLoadingSnackbar, getContactSnackbar } from "@/store/ui/contact/contact.slice";

export const Snackbars = () => {
    return (
        <Box>
            <Outlet />
            <AuthenticationAlertSnackbar
                getSnackbar={getAuthSnackbar}
                closeSnackbar={closeAuthAlertSnackbar}
            />
            <AuthenticationLoadingSnackbar
                getSnackbar={getAuthSnackbar}
                closeSnackbar={closeAuthLoadingSnackbar}
            />
            <JokeNewsletterAlertSnackbar
                getSnackbar={getJokeNewsletterSnackbar}
                closeSnackbar={closeJokeNewsletterAlertSnackbar}
            />
            <JokeNewsletterLoadingSnackbar
                getSnackbar={getJokeNewsletterSnackbar}
                closeSnackbar={closeJokeNewsletterLoadingSnackbar}
            />
            <JokesAlertSnackbar
                getSnackbar={getJokesSnackbar}
                closeSnackbar={closeJokesAlertSnackbar}
            />
            <JokesLoadingSnackbar
                getSnackbar={getJokesSnackbar}
                closeSnackbar={closeJokesLoadingSnackbar}
            />
            <ContactAlertSnackbar
                getSnackbar={getContactSnackbar}
                closeSnackbar={closeContactAlertSnackbar}
            />
            <ContactLoadingSnackbar
                getSnackbar={getContactSnackbar}
                closeSnackbar={closeContactLoadingSnackbar}
            />
        </Box>
    );
}

export default Snackbars;