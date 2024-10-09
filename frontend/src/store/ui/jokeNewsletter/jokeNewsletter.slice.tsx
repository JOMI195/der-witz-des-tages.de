import { activateJokeNewsletterSubscriptionFailed, activateJokeNewsletterSubscriptionFulfilled, activateJokeNewsletterSubscriptionRequested, subscribeToNewsletterFailed, subscribeToNewsletterFulfilled, subscribeToNewsletterRequested, unsubscribeFromNewsletterFailed, unsubscribeFromNewsletterFulfilled, unsubscribeFromNewsletterRequested } from "@/store/entities/jokeNewsletter/jokeNewsletter.slice";
import { AlertColor } from "@mui/material";
import { createSlice } from "@reduxjs/toolkit";

type SliceState = {
  snackbar: {
    alert: { open: boolean; message: string; severity: AlertColor };
    loading: { open: boolean; message: string; };
  };
};

const initialState: SliceState = {
  snackbar: {
    alert: { open: false, message: "", severity: "success" },
    loading: { open: false, message: "", },
  },
};

const jokeNewsletterSlice = createSlice({
  name: "jokeNewsletter",
  initialState,
  extraReducers: (builder) => {
    builder
      .addCase(subscribeToNewsletterRequested, (jokeNewsletter) => {
        jokeNewsletter.snackbar.loading = {
          open: true,
          message: "Anmeldung zum Newsletter läuft",
        };
      })
      .addCase(subscribeToNewsletterFulfilled, (jokeNewsletter) => {
        jokeNewsletter.snackbar.alert = {
          open: true,
          message: "Anmeldung zum Newsletter erfolgreich. Übeprüfe deine Mails um den Erhalt zu bestätigen.",
          severity: "success",
        };
        jokeNewsletter.snackbar.loading = {
          open: false,
          message: "",
        };
      })
      .addCase(subscribeToNewsletterFailed, (jokeNewsletter) => {
        jokeNewsletter.snackbar.alert = {
          open: true,
          message: "Anmeldung zum Newsletter fehlgeschlagen",
          severity: "error",
        };
        jokeNewsletter.snackbar.loading = {
          open: false,
          message: "",
        };
      })
      .addCase(unsubscribeFromNewsletterRequested, (jokeNewsletter) => {
        jokeNewsletter.snackbar.loading = {
          open: true,
          message: "Abmeldung vom Newsletter läuft",
        };
      })
      .addCase(unsubscribeFromNewsletterFulfilled, (jokeNewsletter) => {
        jokeNewsletter.snackbar.alert = {
          open: true,
          message: "Abmeldung vom Newsletter erfolgreich",
          severity: "success",
        };
        jokeNewsletter.snackbar.loading = {
          open: false,
          message: "",
        };
      })
      .addCase(unsubscribeFromNewsletterFailed, (jokeNewsletter) => {
        jokeNewsletter.snackbar.alert = {
          open: true,
          message: "Abmeldung vom Newsletter fehlgeschlagen",
          severity: "error",
        };
        jokeNewsletter.snackbar.loading = {
          open: false,
          message: "",
        };
      })
      .addCase(activateJokeNewsletterSubscriptionRequested, (jokeNewsletter) => {
        jokeNewsletter.snackbar.loading = {
          open: true,
          message: "Aktivierung des Newsletter Abonnements läuft",
        };
      })
      .addCase(activateJokeNewsletterSubscriptionFulfilled, (jokeNewsletter) => {
        jokeNewsletter.snackbar.alert = {
          open: true,
          message: "Aktivierung des Newsletter Abonnements erfolgreich",
          severity: "success",
        };
        jokeNewsletter.snackbar.loading = {
          open: false,
          message: "",
        };
      })
      .addCase(activateJokeNewsletterSubscriptionFailed, (jokeNewsletter) => {
        jokeNewsletter.snackbar.alert = {
          open: true,
          message: "Aktivierung des Newsletter Abonnements fehlgeschlagen",
          severity: "error",
        };
        jokeNewsletter.snackbar.loading = {
          open: false,
          message: "",
        };
      })
  },
  reducers: {
    alertSnackbarOpened: (jokeNewsletter, action) => {
      jokeNewsletter.snackbar.alert = {
        open: true,
        message: action.payload.message,
        severity: action.payload.severity,
      };
    },
    alertSnackbarClosed: (jokeNewsletter) => {
      jokeNewsletter.snackbar.alert = {
        ...jokeNewsletter.snackbar.alert,
        open: false,
      };
    },
    loadingSnackbarOpened: (jokeNewsletter, action) => {
      jokeNewsletter.snackbar.loading = {
        open: true,
        message: action.payload.message,
      };
    },
    loadingSnackbarClosed: (jokeNewsletter) => {
      jokeNewsletter.snackbar.loading = {
        ...jokeNewsletter.snackbar.loading,
        open: false,
      };
    },
  },
});

export const openJokeNewsletterAlertSnackbar = (payload: {
  message: string;
  severity: string;
}) => ({
  type: alertSnackbarOpened.type,
  payload,
});

export const closeJokeNewsletterAlertSnackbar = () => ({
  type: alertSnackbarClosed.type,
});

export const openJokeNewsletterLoadingSnackbar = (payload: {
  message: string;
}) => ({
  type: loadingSnackbarOpened.type,
  payload,
});

export const closeJokeNewsletterLoadingSnackbar = () => ({
  type: loadingSnackbarClosed.type,
});

export const {
  alertSnackbarOpened,
  alertSnackbarClosed,
  loadingSnackbarOpened,
  loadingSnackbarClosed
} = jokeNewsletterSlice.actions;
export default jokeNewsletterSlice.reducer;

export const getJokeNewsletterSnackbar = (state: any) => state.ui.jokeNewsletter.snackbar;
