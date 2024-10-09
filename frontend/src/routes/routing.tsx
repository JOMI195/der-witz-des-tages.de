import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '@/common/components/layout/layout';
import NotFound from '@/common/components/error/notFound/notFound';
import Home from '@/main/home/home';
import { getAuthenticationUrl } from '@/assets/endpoints/app/authEndpoints';
import Snackbars from '@/common/components/snackbars/snackbars';
import { getContactUrl, getEnterWallUrl, getHomeUrl, getSubmitJokeUrl } from '@/assets/endpoints/app/appEndpoints';
import { getSettingsUrl } from '@/assets/endpoints/app/settingEndpoints';
import { getNewsletterUrl } from '@/assets/endpoints/app/newsletterEndpoints';
import SubmitJoke from '@/main/submitJoke/submitJoke';
import ContactForm from '@/main/contact/contactForm';
import { getImprintUrl, getPrivacyPolicyUrl } from '@/assets/endpoints/app/legalEndpoints';
import PrivacyPolicy from '@/main/legals/privacyPolicy';
import Impressum from '@/main/legals/impressum';
import EnterWall from '@/main/enterWall/enterWall';
import FeatureSelectorWrapper from '@/common/components/featureSelectorWrapper';
import authenticationRoutes from '@/main/authentication/authentication';
import newsletterRoutes from '@/main/newsletter/newsletter';
import settingsRoutes from '@/main/settings/settings';

const Routing = createBrowserRouter([
  {
    element: <Snackbars />,
    children: [
      {
        path: getAuthenticationUrl(),
        element: <FeatureSelectorWrapper feature="authentication" />,
        children: authenticationRoutes,
      },
      {
        path: getNewsletterUrl(),
        element: <FeatureSelectorWrapper feature="newsletter" />,
        children: newsletterRoutes,
      },
      {
        path: getEnterWallUrl(),
        element: <EnterWall />,
      },
      {
        element: <MainLayout />,
        children: [
          {
            path: "*",
            element: <NotFound />,
          },
          {
            element: <FeatureSelectorWrapper feature="app" />,
            children: [
              {
                path: getHomeUrl(),
                element: <Home />,
              },
              {
                path: getContactUrl(),
                element: <ContactForm />,
              },
              {
                path: getSubmitJokeUrl(),
                element: <SubmitJoke />,
              },
              {
                path: getPrivacyPolicyUrl(),
                element: <PrivacyPolicy />,
              },
              {
                path: getImprintUrl(),
                element: <Impressum />,
              },
            ],
          },
          {
            path: getSettingsUrl() + "*",
            element: <FeatureSelectorWrapper feature="settings" />,
            children: settingsRoutes,
          },
        ],
      },
    ],
  },
]);

export default Routing;
