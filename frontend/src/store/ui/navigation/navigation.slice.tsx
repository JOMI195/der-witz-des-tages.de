import { createSlice } from "@reduxjs/toolkit";

type SliceState = {
  selectedFeature: { title: string };
  dialogs: { loginOptions: { open: boolean } };
};

const initialState: SliceState = {
  selectedFeature: { title: "welcome" },
  dialogs: { loginOptions: { open: false } }
};

const navigationSlice = createSlice({
  name: "navigation",
  initialState,
  reducers: {
    featureSelected: (navigation, action) => {
      navigation.selectedFeature.title = action.payload;
    },
    loginOptionsDialogOpened: (navigation) => {
      navigation.dialogs.loginOptions.open = true;
    },
    loginOptionsDialogClosed: (navigation) => {
      navigation.dialogs.loginOptions.open = false;
    },
  },
});

export const setSelectedFeature = (payload: string) => ({
  type: featureSelected.type,
  payload,
});

export const openLoginOptionsDialog = () => ({
  type: loginOptionsDialogOpened.type,
});

export const closeLoginOptionsDialog = () => ({
  type: loginOptionsDialogClosed.type,
});

export const {
  featureSelected,
  loginOptionsDialogOpened,
  loginOptionsDialogClosed
} = navigationSlice.actions;

export default navigationSlice.reducer;

export const getSelectedFeature = (state: any) =>
  state.ui.navigation.selectedFeature;

export const getDialogs = (state: any) =>
  state.ui.navigation.dialogs;