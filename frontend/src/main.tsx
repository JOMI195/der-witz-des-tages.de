import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import { Provider } from 'react-redux';
import { store } from './store/index.ts';
import http from "./services/httpService";
import '@fontsource/inter';
import StoreGate from './common/components/storeGate.tsx';
import { useEffect } from 'react';
import localStorageBuildVersionUpdate from './common/components/localStorageBuildVersionUpdateService.ts';

const AppWrapper = () => {

  useEffect(() => {
    const handleRefresh = () => {
      localStorageBuildVersionUpdate();
    };

    window.addEventListener('load', handleRefresh);

    return () => {
      window.removeEventListener('load', handleRefresh);
    };
  }, []);

  return (
    <Provider store={store}>
      <StoreGate>
        <App />
      </StoreGate>
    </Provider>
  );
};

const container = document.getElementById("root");
const root = createRoot(container!);

root.render(<AppWrapper />);

http.apiSetup(store);
