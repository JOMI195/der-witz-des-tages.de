/* eslint-disable react-refresh/only-export-components -- route config module, the lazy() consts are routes, not exported components */
import { lazy } from "react";
import { getHomeUrl } from "@/assets/endpoints/app/appEndpoints";
import ProtectedRoute from "@/common/components/protectedRoute";
import NotFound from "@/common/components/error/notFound/notFound";
import { getAppSettingsUrl, getUserSettingsUrl } from "@/assets/endpoints/app/settingEndpoints";

const Layout = lazy(() => import("./layout"));
const User = lazy(() => import("./user/user"));
const App = lazy(() => import("./app/app"));

const settingsRoutes = [
  {
    path: "*",
    element: <NotFound />,
  },
  {
    element: <Layout />,
    children: [
      {
        path: getAppSettingsUrl(),
        element: <App />,
      },
      {
        element: <ProtectedRoute redirectPath={getHomeUrl()} />,
        children: [
          {
            path: getUserSettingsUrl(),
            element: <User />,
          },
        ],
      },
    ],
  },
];

export default settingsRoutes;
