import { jokeSubmitFailed, jokeSubmitFulfilled, jokeSubmitPending } from "@/store/entities/jokes/jokes.slice";
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

const jokesSlice = createSlice({
  name: "jokes",
  initialState,
  extraReducers: (builder) => {
    builder
      .addCase(jokeSubmitPending, (jokes) => {
        jokes.snackbar.loading = {
          open: true,
          message: "Einreichung von Witz läuft",
        };
      })
      .addCase(jokeSubmitFulfilled, (jokes) => {
        jokes.snackbar.alert = {
          open: true,
          message: "Einreichung von Witz erfolgreich",
          severity: "success",
        };
        jokes.snackbar.loading = {
          open: false,
          message: "",
        };
      })
      .addCase(jokeSubmitFailed, (jokes) => {
        jokes.snackbar.alert = {
          open: true,
          message: "Einreichung von Witz fehlgeschlagen",
          severity: "error",
        };
        jokes.snackbar.loading = {
          open: false,
          message: "",
        };
      })
  },
  reducers: {
    alertSnackbarOpened: (jokes, action) => {
      jokes.snackbar.alert = {
        open: true,
        message: action.payload.message,
        severity: action.payload.severity,
      };
    },
    alertSnackbarClosed: (jokes) => {
      jokes.snackbar.alert = {
        ...jokes.snackbar.alert,
        open: false,
      };
    },
    loadingSnackbarOpened: (jokes, action) => {
      jokes.snackbar.loading = {
        open: true,
        message: action.payload.message,
      };
    },
    loadingSnackbarClosed: (jokes) => {
      jokes.snackbar.loading = {
        ...jokes.snackbar.loading,
        open: false,
      };
    },
  },
});

export const openJokesAlertSnackbar = (payload: {
  message: string;
  severity: string;
}) => ({
  type: alertSnackbarOpened.type,
  payload,
});

export const closeJokesAlertSnackbar = () => ({
  type: alertSnackbarClosed.type,
});

export const openJokesLoadingSnackbar = (payload: {
  message: string;
}) => ({
  type: loadingSnackbarOpened.type,
  payload,
});

export const closeJokesLoadingSnackbar = () => ({
  type: loadingSnackbarClosed.type,
});

export const {
  alertSnackbarOpened,
  alertSnackbarClosed,
  loadingSnackbarOpened,
  loadingSnackbarClosed
} = jokesSlice.actions;
export default jokesSlice.reducer;

export const getJokesSnackbar = (state: any) => state.ui.jokes.snackbar;
