import { getAuthenticationUrl, getSignOutUrl } from "../endpoints/app/authEndpoints";
import { getUserSettingsUrl, getSettingsUrl } from "../endpoints/app/settingEndpoints";
import PersonIcon from '@mui/icons-material/Person';
import LogoutIcon from '@mui/icons-material/Logout';
import HomeIcon from '@mui/icons-material/Home';
import PublishIcon from '@mui/icons-material/Publish';
import { IAccountMenuItem, IAppBarMenuItem } from "@/types";
import { getSubmitJokeUrl } from "../endpoints/app/appEndpoints";

export const appBarMenuItems: IAppBarMenuItem[] = [
    {
        name: "Newsletter",
        url: "/",
        icon: HomeIcon
    },
    // {
    //     name: "Archiv",
    //     url: getArchiveUrl(),
    //     icon: PhotoAlbumIcon
    // },
    {
        name: "Witz einreichen",
        url: getSubmitJokeUrl(),
        icon: PublishIcon
    },
];

export const accountMenuItems: IAccountMenuItem[] = [
    {
        name: "Konto",
        url: getSettingsUrl() + getUserSettingsUrl(),
        icon: PersonIcon
    },
    {
        name: "Abmelden",
        url: getAuthenticationUrl() + getSignOutUrl(),
        icon: LogoutIcon
    },
];