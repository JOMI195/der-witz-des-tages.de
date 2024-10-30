import React from 'react';
import {
    Dialog,
    DialogContent,
    Paper,
    Typography,
    Grid,
    Box,
    useTheme
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import EmailIcon from '@mui/icons-material/Email';
import PersonIcon from '@mui/icons-material/Person';
import { getAuthenticationUrl, getSignInUrl } from '@/assets/endpoints/app/authEndpoints';
import { getHomeUrl } from '@/assets/endpoints/app/appEndpoints';
import { closeLoginOptionsDialog, getDialogs } from '@/store/ui/navigation/navigation.slice';
import { useAppDispatch, useAppSelector } from '@/store';

interface SignUpOption {
    icon: React.ReactNode;
    title: string;
    path: string;
    disabled?: boolean;
    active?: boolean;
}

const options: SignUpOption[] = [
    {
        icon: <EmailIcon sx={{ fontSize: 40 }} />,
        title: 'Newsletter',
        path: getHomeUrl(),
        disabled: false
    },
    {
        icon: <PersonIcon sx={{ fontSize: 40 }} />,
        title: 'Account',
        path: getAuthenticationUrl() + getSignInUrl(),
        disabled: false
    },
];

const SignUpOptionsDialog: React.FC = () => {
    const navigate = useNavigate();
    const dispatch = useAppDispatch();
    const theme = useTheme();
    const open = useAppSelector(getDialogs).loginOptions.open;

    const closeDialog = () => {
        dispatch(closeLoginOptionsDialog());
    }

    const handleOptionClick = (path: string, disabled?: boolean): void => {
        if (!disabled) {
            navigate(path);
            setTimeout(() => {
                const element = document.getElementById('newsletterSignUp');
                if (element) {
                    const elementPosition = element.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.scrollY - theme.layout.appbar.height;
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }, 0);
            closeDialog();
        }
    };

    return (
        <Dialog
            open={open}
            onClose={closeDialog}
            maxWidth="xs"
            PaperProps={{
                sx: {
                    bgcolor: 'background.default',
                    p: 1,
                }
            }}
        >
            <DialogContent>
                <Grid container spacing={2}>
                    {options.map((option) => (
                        <Grid item xs={6} key={option.title}>
                            <Paper
                                elevation={3}
                                onClick={() => handleOptionClick(option.path, option.disabled)}
                                sx={{
                                    display: 'flex',
                                    flexDirection: "column",
                                    justifyContent: 'center',
                                    alignItems: 'center',
                                    textAlign: "center",
                                    p: 2,
                                    backgroundColor: "primary.main"
                                }}
                            >
                                <Box
                                    sx={{
                                        mb: 1,
                                        display: 'flex',
                                        justifyContent: 'center',
                                        alignItems: 'center',
                                        color: theme.palette.common.white,
                                    }}
                                >
                                    {option.icon}
                                </Box>
                                <Typography
                                    variant="body1"
                                    component="div"
                                    color={theme.palette.common.white}
                                >
                                    {option.title}
                                </Typography>
                            </Paper>
                        </Grid>
                    ))}
                </Grid>
                <Typography
                    variant="body1"
                    sx={{ mt: 4, textAlign: 'center' }}
                >
                    Bitte wähle eine der obenstehenden Optionen aus. Ein Account wird nur benötigt wenn du einen Witz einreichen willst.
                </Typography>
            </DialogContent>
        </Dialog>
    );
};

export default SignUpOptionsDialog;