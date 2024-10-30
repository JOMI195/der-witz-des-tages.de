import { Box, Container, useMediaQuery, useTheme } from "@mui/material";
import { Outlet, ScrollRestoration } from "react-router-dom";
import TopAppbar from "./topLayout/topAppBar";
import Footer from "./bottomLayout/footer";
import { useAppSelector } from "@/store";
import { getNavigation } from "@/store/ui/settings/settings.slice";
import { getSelectedFeature } from "@/store/ui/navigation/navigation.slice";
import SignUpOptionsDialog from "./dialogs/signUpOptions/signUpOptions";

const MainLayout: React.FC = () => {
    const theme = useTheme();
    const isBottomNavigationOpen = useAppSelector(getNavigation).bottomNavigation.open;
    const isSettingsFeatureSelected = useAppSelector(getSelectedFeature).title === "settings" ? true : false;
    const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <TopAppbar />
            <ScrollRestoration />
            <SignUpOptionsDialog />
            <Container
                maxWidth="xl"
                sx={{
                    flex: '1 1 auto',
                    display: 'flex',
                    alignItems: "center",
                    flexDirection: 'column',
                    pt: isSmallScreen ? 0 : 5,
                    pb: 10,
                }}
            >
                <Outlet />
            </Container>
            {/* <CookieBanner /> */}
            {isBottomNavigationOpen && isSettingsFeatureSelected ? null : <Footer />}
        </Box>
    );
};

export default MainLayout;
