import { lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '@/common/components/layout/layout';
import NotFound from '@/common/components/error/notFound/notFound';
import Home from '@/main/home/home';
import { getAuthenticationUrl } from '@/assets/endpoints/app/authEndpoints';
import Snackbars from '@/common/components/snackbars/snackbars';
import { getArchiveUrl, getContactUrl, getEnterWallUrl, getHomeUrl, getSubmitJokeUrl } from '@/assets/endpoints/app/appEndpoints';
import { getSettingsUrl } from '@/assets/endpoints/app/settingEndpoints';
import { getNewsletterUrl } from '@/assets/endpoints/app/newsletterEndpoints';
import { getImprintUrl, getPrivacyPolicyUrl } from '@/assets/endpoints/app/legalEndpoints';
import FeatureSelectorWrapper from '@/common/components/featureSelectorWrapper';
import authenticationRoutes from '@/main/authentication/authentication';
import newsletterRoutes from '@/main/newsletter/newsletter';
import settingsRoutes from '@/main/settings/settings';
import SeoHead from '@/seo/seoHead';

const Archive = lazy(() => import('@/main/archive/archive'));
const SubmitJoke = lazy(() => import('@/main/submitJoke/submitJoke'));
const ContactForm = lazy(() => import('@/main/contact/contactForm'));
const PrivacyPolicy = lazy(() => import('@/main/legals/privacyPolicy'));
const Impressum = lazy(() => import('@/main/legals/impressum'));
const EnterWall = lazy(() => import('@/main/enterWall/enterWall'));

const Routing = createBrowserRouter([
  {
    element: <SeoHead />,
    children: [
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
                    path: getArchiveUrl(),
                    element: <Archive />,
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
    ],
  },
]);

export default Routing;
