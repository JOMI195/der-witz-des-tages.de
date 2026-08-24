/* eslint-disable react-refresh/only-export-components -- route config module, the lazy() consts are routes, not exported components */
import { lazy } from "react";
import NotFound from "@/common/components/error/notFound/notFound";
import { getNewsletterActivationUrl, getNewsletterUnsubscribeUrl } from "@/assets/endpoints/app/newsletterEndpoints";

const Layout = lazy(() => import("../authentication/layout"));
const Activation = lazy(() => import("./activate"));
const Unsubscribtion = lazy(() => import("./unsubscribe"));

const newsletterRoutes = [
    {
        path: "*",
        element: <NotFound />,
    },
    {
        element: <Layout />,
        children: [
            {
                path: getNewsletterActivationUrl(),
                element: <Activation />,
            },
            {
                path: getNewsletterUnsubscribeUrl(),
                element: <Unsubscribtion />,
            },
        ],
    },
];

export default newsletterRoutes;
