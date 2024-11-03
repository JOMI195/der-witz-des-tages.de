import { RootState } from '..';

const migration2 = (state: RootState): RootState => {
  return {
    ...state,
    ui: {
      ...state.ui,
      navigation: {
        ...state.ui.navigation,
        dialogs: { loginOptions: { open: false } },
      }
    },
  };
};

export default migration2;
