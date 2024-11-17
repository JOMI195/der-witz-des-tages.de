import { getAuthenticationUrl, getSignOutUrl } from "../endpoints/app/authEndpoints";
import { getUserSettingsUrl, getSettingsUrl } from "../endpoints/app/settingEndpoints";
import PersonIcon from '@mui/icons-material/Person';
import LogoutIcon from '@mui/icons-material/Logout';
import HomeIcon from '@mui/icons-material/Home';
import PublishIcon from '@mui/icons-material/Publish';
import PhotoAlbumIcon from '@mui/icons-material/PhotoAlbum';
import EmailIcon from '@mui/icons-material/Email';
import { IAccountMenuItem, IAppBarMenuItem } from "@/types";
import { getArchiveUrl, getHomeUrl, getSubmitJokeUrl } from "../endpoints/app/appEndpoints";

export const appBarMenuItems: IAppBarMenuItem[] = [
    {
        name: "Witz des Tages",
        url: getHomeUrl(),
        icon: HomeIcon
    },
    {
        name: "Newsletter",
        url: getHomeUrl(),
        icon: EmailIcon
    },
    {
        name: "Witz einreichen",
        url: getSubmitJokeUrl(),
        icon: PublishIcon
    },
    {
        name: "Galerie",
        url: getArchiveUrl(),
        icon: PhotoAlbumIcon
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