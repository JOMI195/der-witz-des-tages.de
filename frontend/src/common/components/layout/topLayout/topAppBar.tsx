import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import { Link, useNavigate } from 'react-router-dom';
import { accountMenuItems, appBarMenuItems } from '@/assets/appBarMenu/appBarMenu';
import { useColorThemeContext } from '@/context/colorTheme/colorThemeContext';
import { Grid, ListItemIcon, useMediaQuery, useTheme } from '@mui/material';
import { useAppSelector } from '@/store';
import { getUser } from '@/store/entities/authentication/authentication.slice';
import { getAuthenticationUrl, getSignInUrl } from '@/assets/endpoints/app/authEndpoints';
import SettingsIcon from '@mui/icons-material/Settings';
import { getAppSettingsUrl, getSettingsUrl } from '@/assets/endpoints/app/settingEndpoints';

function TopAppBar() {
    const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
    const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);
    const { colorMode, toggleColorMode, iconComponent: IconComponent } = useColorThemeContext();
    const theme = useTheme();
    const navigate = useNavigate();

    const isSmallScreen = useMediaQuery(theme.breakpoints.down('md'));

    const user = useAppSelector(getUser);

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    const handleSettingsClick = () => {
        navigate(getSettingsUrl() + getAppSettingsUrl(), { replace: true });
    }

    return (
        <AppBar
            elevation={0}
            position="sticky"
            sx={{
                height: theme => theme.layout.appbar.height,
                background: theme => theme.palette.background.default,
            }}
        >
            <Toolbar sx={{ height: "100%" }}>
                <Grid container alignItems="center" justifyContent="space-between" sx={{ height: "100%" }}>
                    {/* logo - md */}
                    {/* <Grid display={{ xs: "none", md: "flex" }} item md={3} alignItems="center" justifyContent="flex-start">
                        <Logo
                            darkLogoSrc="/witz-des-tages-logo-dark-full.svg"
                            lightLogoSrc="/witz-des-tages-logo-light-full.svg"
                            width={200}
                            marginRight={16}
                            clickable={true}
                            linkUrl={getHomeUrl()}
                        />
                    </Grid> */}

                    {/* links - xs */}
                    <Grid display={{ xs: "flex", md: "none" }} item xs={8} alignItems="center" justifyContent="flex-start">
                        <IconButton
                            size="small"
                            aria-label="account of current user"
                            aria-controls="menu-appbar"
                            aria-haspopup="true"
                            onClick={handleOpenNavMenu}
                        >
                            <MenuIcon />
                        </IconButton>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorElNav}
                            anchorOrigin={{
                                vertical: 'bottom',
                                horizontal: 'left',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'left',
                            }}
                            open={Boolean(anchorElNav)}
                            onClose={handleCloseNavMenu}
                            sx={{
                                display: { xs: 'block', md: 'none' },
                            }}
                        >
                            {appBarMenuItems.map((item) => (
                                <MenuItem component={Link} to={item.url} key={item.name} onClick={handleCloseNavMenu}>
                                    <ListItemIcon>
                                        <item.icon fontSize="small" />
                                    </ListItemIcon>
                                    <Typography textAlign="center">{item.name}</Typography>
                                </MenuItem>
                            ))}
                        </Menu>
                    </Grid>

                    {/* right icons - always */}
                    <Grid display={"flex"} item xs={4} md={12} alignItems="center" justifyContent={isSmallScreen ? "flex-end" : "center"}>
                        {!isSmallScreen && appBarMenuItems.map((item) => (
                            <Button
                                key={item.name}
                                variant='outlined'
                                component={Link}
                                to={item.url}
                                onClick={handleCloseNavMenu}
                                sx={{
                                    my: 2,
                                    textDecoration: 'none',
                                    minHeight: 40,
                                    borderRadius: theme => theme.shape.borderRadius,
                                    mx: 1
                                }}
                            >
                                {item.name}
                            </Button>
                        ))}
                        <Box
                            sx={{
                                flex: isSmallScreen ? 0 : 1
                            }}
                        />
                        <Tooltip title={colorMode === "dark" ? "Wechsel in den hellen Modus" : "Wechsel in den dunklen Modus"}>
                            <IconButton size={isSmallScreen ? "medium" : "medium"} onClick={toggleColorMode} sx={{ p: 1 }}>
                                <IconComponent fontSize={isSmallScreen ? "medium" : "medium"} />
                            </IconButton>
                        </Tooltip>
                        <IconButton size={isSmallScreen ? "medium" : "medium"} onClick={handleSettingsClick} sx={{ p: 1 }}>
                            <SettingsIcon fontSize={isSmallScreen ? "medium" : "medium"} />
                        </IconButton>
                        {user.loggedIn ? (
                            <Box>
                                <IconButton onClick={handleOpenUserMenu} sx={{ p: 0, ml: 1 }}>
                                    <Avatar
                                        sx={{
                                            width: 30,
                                            height: 30,
                                            m: 1
                                        }}
                                        alt="Account"
                                    >
                                        {`${user.me.username.slice(0, 1).toUpperCase()}`}
                                    </Avatar>
                                </IconButton>
                                <Menu
                                    sx={{ mt: '45px' }}
                                    id="menu-appbar"
                                    anchorEl={anchorElUser}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    keepMounted
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    open={Boolean(anchorElUser)}
                                    onClose={handleCloseUserMenu}
                                >
                                    {accountMenuItems.map((item) => (
                                        <MenuItem component={Link} to={item.url} key={item.name} onClick={handleCloseUserMenu}>
                                            <ListItemIcon>
                                                <item.icon fontSize="small" />
                                            </ListItemIcon>
                                            <Typography textAlign="center">{item.name}</Typography>
                                        </MenuItem>
                                    ))}
                                </Menu>
                            </Box>
                        ) : (
                            <Box>
                                <Button
                                    component={Link}
                                    to={getAuthenticationUrl() + getSignInUrl()}
                                    variant='contained'
                                    size={isSmallScreen ? "small" : "medium"}
                                    sx={{ ml: 1 }}
                                >
                                    Anmelden
                                </Button>
                            </Box>
                        )}
                    </Grid>
                </Grid>
            </Toolbar>
        </AppBar>
    );
}
export default TopAppBar;
