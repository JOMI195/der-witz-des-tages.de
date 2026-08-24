/* eslint-disable react-refresh/only-export-components -- route config module, the lazy() consts are routes, not exported components */
import { lazy } from "react";
import {
  getActivationUrl,
  getResetPasswordConfirmationUrl,
  getResetPasswordUrl,
  getSignInUrl,
  getSignOutUrl,
  getSignUpConfirmationUrl,
  getSignUpUrl,
  getUsersUrl,
} from "@/assets/endpoints/app/authEndpoints";
import NotFound from "@/common/components/error/notFound/notFound";

const Layout = lazy(() => import("./layout"));
const SignIn = lazy(() => import("./signIn/signIn"));
const SignOut = lazy(() => import("./signOut/signOut"));
const SignUp = lazy(() => import("./signUp/signUp"));
const Activation = lazy(() => import("./users/activation"));
const PasswordReset = lazy(() => import("./users/passwordReset"));
const PasswordResetConfirmation = lazy(() => import("./users/passwordResetConfirmation"));
const SignUpConfirmation = lazy(() => import("./signUp/signUpConfirmation"));

const authenticationRoutes = [
  {
    path: "*",
    element: <NotFound />,
  },
  {
    element: <Layout />,
    children: [
      {
        path: getSignInUrl(),
        element: <SignIn />,
      },
      {
        path: getSignOutUrl(),
        element: <SignOut />,
      },
      {
        path: getSignUpUrl(),
        element: <SignUp />,
      },
      {
        path: getUsersUrl(),
        children: [
          {
            path: getSignUpConfirmationUrl(),
            element: <SignUpConfirmation />,
          },
          {
            path: getActivationUrl(),
            element: <Activation />,
          },
          {
            path: getResetPasswordUrl(),
            element: <PasswordReset />,
          },
          {
            path: getResetPasswordConfirmationUrl(),
            element: <PasswordResetConfirmation />,
          },
        ],
      },
    ],
  },
];

export default authenticationRoutes;
