import NotFound from "@/common/components/error/notFound/notFound";
import Layout from "../authentication/layout"; // Assuming the layout is shared with authentication
import { getNewsletterActivationUrl, getNewsletterUnsubscribeUrl } from "@/assets/endpoints/app/newsletterEndpoints";
import Activation from "./activate";
import Unsubscribtion from "./unsubscribe";

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
