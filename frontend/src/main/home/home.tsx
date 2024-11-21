import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchJokeOfTheDay } from '@/store/entities/jokes/jokes.actions';
import { Box, Grid, Typography, useTheme, useMediaQuery, Card, CardMedia, alpha, Skeleton, Avatar, Button, keyframes } from '@mui/material';
import TextGradient from '@/common/components/textGradient';
import NewsletterForm from './newsletterForm';
import { getJokeOfTheDay } from '@/store/entities/jokes/jokes.slice';
import { landingPageCatchPhrases } from './catchPhrases';
import AppRating from './appRating';
import { IJoke } from '@/types';
import ContentCard from '@/common/components/contentCard';
import { Link } from 'react-router-dom';
import { getSubmitJokeUrl } from '@/assets/endpoints/app/appEndpoints';
import Logo from '@/common/components/logo';
import { formatDateOnly } from '@/common/utils/date/date';
import InstagramIcon from '@mui/icons-material/Instagram';

const MEDIA_BASE_URL = import.meta.env.VITE_API_MEDIA_BASE_URL;

const getRandomCatchPhrase = () => {
    const randomIndex = Math.floor(Math.random() * landingPageCatchPhrases.length);
    return landingPageCatchPhrases[randomIndex];
};

const jokeOfTheDayPictureAnimation = keyframes`
  0%, 100% {
    opacity: 1;
    transform: rotate(5deg) scale(1);
  }
  50% {
    transform: rotate(5deg) scale(1.1);
  }
`;

const Home = () => {
    const dispatch = useAppDispatch();
    const [catchPhrase, setCatchPhrase] = useState('');
    const [jokeOfTheDayPictureShouldAnimate, _setJokeOfTheDayPictureShouldAnimate] = useState(false);
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    const jokeOfTheDay: IJoke = useAppSelector(getJokeOfTheDay);

    useEffect(() => {
        dispatch(fetchJokeOfTheDay());
        setCatchPhrase(getRandomCatchPhrase());
    }, []);

    // useEffect(() => {
    //     const interval = setInterval(() => {
    //         setJokeOfTheDayPictureShouldAnimate(true);
    //         setTimeout(() => setJokeOfTheDayPictureShouldAnimate(false), 1000);
    //     }, 10000);

    //     return () => clearInterval(interval);
    // }, []);

    // useEffect(() => {
    //     const interval = setInterval(() => {
    //         setCatchPhrase(getRandomCatchPhrase());
    //     }, 20000);

    //     return () => clearInterval(interval);
    // }, []);

    return (
        <Box
            sx={{

                textAlign: "center",
            }}
        >
            <Logo
                darkLogoSrc="/witz-des-tages-logo-dark-full.svg"
                lightLogoSrc="/witz-des-tages-logo-light-full.svg"
                maxWidth={500}
                marginRight={16}
                clickable={false}
            />
            <Grid
                container
                spacing={3}
                alignItems="center"
                display={"flex"}
                justifyContent={isMobile ? "center" : "space-between"}
                sx={{ pb: 3 }}
            >
                <Grid
                    item
                    xs={12}
                    sx={{
                        textAlign: 'center',
                        mb: isMobile ? 3 : 5,
                        order: { xs: 2, md: 1 }
                    }}
                >
                    {jokeOfTheDay.text !== "" ? (
                        <TextGradient
                            options={{
                                variant: isMobile ? 'h2' : 'h1',
                                direction: 'to bottom right',
                                startColor: theme.palette.accent.main,
                                endColor: theme.palette.primary.main,
                            }}
                            sx={{
                                fontWeight: 'bold',
                            }}
                        >
                            {jokeOfTheDay?.text || catchPhrase}
                        </TextGradient>
                    ) : (
                        <Box sx={{ pb: 1, }}>
                            <Typography variant="h2">{<Skeleton />}</Typography>
                            <Typography variant="h2">{<Skeleton />}</Typography>
                        </Box>
                    )}
                    <Box
                        sx={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: isMobile ? "column" : "row"
                        }}
                    >
                        <Typography variant="h6">
                            {`Witz des Tages ${formatDateOnly(new Date())}`}
                        </Typography>
                        {jokeOfTheDay.created_by.username !== "" && (
                            <Box
                                sx={{
                                    display: "flex",
                                    justifyContent: "center",
                                    alignItems: "center",
                                }}
                            >
                                {!isMobile ? (
                                    <Typography sx={{ pl: 1 }} variant="h6">
                                        {"- Eingereicht von"}
                                    </Typography>
                                ) : (
                                    <Typography variant={"body2"}>
                                        {"Eingereicht von"}
                                    </Typography>
                                )}
                                <Avatar
                                    sx={{
                                        width: 30,
                                        height: 30,
                                        p: 1.5,
                                        mx: 1,
                                    }}
                                    alt="Account"
                                >
                                    {`${jokeOfTheDay.created_by.username === "admin" ? "jomi".slice(0, 1).toUpperCase() : jokeOfTheDay.created_by.username.slice(0, 1).toUpperCase()}`}
                                </Avatar>
                                <Typography variant="h6">
                                    {
                                        `${jokeOfTheDay.created_by.username === "admin" ? "jomi" : jokeOfTheDay.created_by.username}`
                                    }
                                </Typography>
                            </Box>
                        )}
                    </Box>
                    <Box
                        sx={{ my: 1, display: 'flex', justifyContent: 'center', }}
                    >
                        <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}>
                            Auch auf
                            <Button
                                variant="outlined"
                                startIcon={<InstagramIcon />}
                                sx={{ mx: 1 }}
                                component="a"
                                href="https://www.instagram.com/der_witz_des_tages.de/"
                                target="_blank"
                            >
                                Instagram
                            </Button>
                            verfügbar
                        </Typography>
                    </Box>
                </Grid>
                <Grid item xs={12} md={7}
                    sx={{
                        textAlign: isMobile ? 'center' : 'left',
                        order: { xs: 3, md: 1 },
                    }}
                >
                    <Card
                        id="newsletterSignUp"
                        elevation={10}
                        sx={{
                            p: isMobile ? 2 : 5,
                            backgroundColor: alpha(theme.palette.accent.main, 0.5),
                            transform: "rotate(-1deg)",
                        }}
                    >
                        <Box sx={{ mb: 3, fontSize: 'h5.fontSize' }}>
                            Dir gefällt 😍 der heutige Witz des Tages und willst dringend mehr davon?
                        </Box>
                        <Box sx={{ mb: 3, fontSize: 'h5.fontSize' }}>
                            Dann melde dich mit deiner Emailadresse bei unserem
                            <Box fontSize={'h4.fontSize'} component="span" fontWeight='bold'> Newsletter </Box>
                            an und erhalte täglich morgens eine Nachricht mit dem Witz des Tages direkt in dein Postfach 📬
                        </Box>
                        <NewsletterForm />
                    </Card>
                </Grid>
                <Grid item xs={12} md={4}
                    sx={{
                        display: "flex",
                        justifyContent: "center",
                        m: 3,
                        order: { xs: 1, md: 2 }
                    }}>
                    <Card
                        elevation={10}
                        sx={{
                            //margin: 'auto',
                            borderRadius: 3,
                            transform: "rotate(5deg)",
                            aspectRatio: "1 / 1",
                            maxWidth: isMobile ? "300px" : "600px",
                            animation: jokeOfTheDayPictureShouldAnimate
                                ? `${jokeOfTheDayPictureAnimation} 1s ease`
                                : 'none',
                        }}
                    >
                        {jokeOfTheDay.joke_picture !== null ? (
                            <CardMedia
                                component="img"
                                image={MEDIA_BASE_URL + jokeOfTheDay.joke_picture.image}
                                alt="Joke of the day"
                                sx={{
                                    objectFit: 'cover',
                                    flexGrow: 1,
                                }}
                            />
                        ) : (
                            <Skeleton
                                variant="rectangular"
                                sx={{
                                    width: isMobile ? "300px" : "600px",
                                    height: isMobile ? "300px" : "600px"
                                }}
                            />
                        )}
                    </Card>
                </Grid>
                <Grid container item xs={12}
                    sx={{ order: { xs: 3, md: 3 } }}
                    display={"flex"}
                    justifyContent={"center"}
                    alignItems={"center"}
                    spacing={3}
                >
                    <Grid item md={8} sm={12}
                        display={"flex"}
                        justifyContent={"center"}
                    >
                        <Card
                            elevation={10}
                            sx={{
                                p: isMobile ? 2 : 2,
                                backgroundColor: alpha(theme.palette.primary.main, 0.3),
                                transform: "rotate(1deg)",
                                maxWidth: "700px",
                                minWidth: { sm: "500px", xs: "auto" },
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "center",
                                alignItems: "center"
                            }}
                        >
                            <Box sx={{ pb: 3, fontWeight: 'medium', fontSize: 'h4.fontSize', textAlign: "center" }}>
                                {`${catchPhrase}`}
                            </Box>
                            <AppRating />
                        </Card>
                    </Grid>
                    <Grid item md={4} sm={12}
                        display={"flex"}
                        justifyContent={"center"}
                        sx={{ order: { xs: 3, md: 3 } }}>
                        <ContentCard
                            transform="rotate(-2deg)"
                            backgroundColor={alpha(theme.palette.secondary.main, 0.3)}
                        >
                            <Typography variant="h6" sx={{ pb: 1 }}> Du hast selbst einen Witz 💎 auf Lager, und brennst darauf diesen mit der Welt 🌍 zu teilen? Dann spende diesen doch einfach!</Typography>
                            <Button
                                component={Link}
                                to={getSubmitJokeUrl()}
                                variant='contained'
                                sx={{ fontWeight: "bold" }}
                            >
                                Zur Einreichung 📝
                            </Button>
                        </ContentCard>
                    </Grid>
                </Grid>

            </Grid>
        </Box>
    );
};

export default Home;