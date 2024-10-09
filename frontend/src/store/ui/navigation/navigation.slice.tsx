import { createSlice } from "@reduxjs/toolkit";

type SliceState = {
  selectedFeature: { title: string };
};

const initialState: SliceState = {
  selectedFeature: { title: "welcome" },
};

const navigationSlice = createSlice({
  name: "navigation",
  initialState,
  reducers: {
    featureSelected: (navigation, action) => {
      navigation.selectedFeature.title = action.payload;
    },
  },
});

export const setSelectedFeature = (payload: string) => ({
  type: featureSelected.type,
  payload,
});

export const {
  featureSelected,
} = navigationSlice.actions;

export default navigationSlice.reducer;

export const getSelectedFeature = (state: any) =>
  state.ui.navigation.selectedFeature;
