import { Box, Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import { getArchiveUrl, getHomeUrl, getSubmitJokeUrl } from "@/assets/endpoints/app/appEndpoints";

const NotFound = () => {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                textAlign: 'center',
                minHeight: '60vh',
                py: 6,
            }}
        >
            <Typography variant="h1" fontWeight="bold" sx={{ fontSize: { xs: 'h3.fontSize', md: 'h2.fontSize' } }}>
                404 – Diese Seite gibt es nicht
            </Typography>
            <Typography variant="body1" sx={{ mt: 2, mb: 4 }}>
                Der Witz ist wohl an der falschen Adresse gelandet. Hier geht es zurück zum Lachen:
            </Typography>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <Button component={Link} to={getHomeUrl()} variant="contained">
                    Witz des Tages
                </Button>
                <Button component={Link} to={"/" + getArchiveUrl()} variant="outlined">
                    Witze Galerie
                </Button>
                <Button component={Link} to={"/" + getSubmitJokeUrl()} variant="outlined">
                    Witz einreichen
                </Button>
            </Stack>
        </Box>
    );
};

export default NotFound;
