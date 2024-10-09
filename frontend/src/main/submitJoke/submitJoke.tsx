import ContentCard from "@/common/components/contentCard";
import { alpha, Box, Grid, Typography, useMediaQuery, useTheme } from "@mui/material";
import SubmitJokeForm from "./submitJokeForm";

const SubmitJoke = () => {
    const theme = useTheme();
    const isSmallerThanLg = useMediaQuery(theme.breakpoints.down('lg'));
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const motivationSection = () => {
        return (
            <Grid item xs={12} lg={5} display={"flex"} justifyContent={{ lg: "center", md: "flex-start", xs: "center" }}>
                <ContentCard
                    backgroundColor={alpha(theme.palette.accent.main, 0.3)}
                >
                    <Typography fontWeight={"bold"} variant="h4" sx={{ pb: 1 }}>Warum mitmachen?</Typography>
                    <Typography variant="h6">Mit deinem Witz kannst du andere zum Lachen bringen und ihren Tag positiv beeinflussen. Und das ganz ohne Aufwand 😱. Also, worauf wartest du noch? Lass uns gemeinsam die Welt ein bisschen fröhlicher machen - wir sind gespannt auf deine Einreichung!</Typography>
                </ContentCard>
            </Grid>
        );
    }

    const catchingSection = () => {
        return (
            <Grid item xs={12} lg={7} display={"flex"} justifyContent={{ lg: "space-around", md: "flex-end", xs: "center" }}>
                <ContentCard
                    transform="rotate(2deg)"
                    backgroundColor={alpha(theme.palette.primary.main, 0.3)}
                >
                    <Typography fontWeight={"bold"} variant="h4" sx={{ pb: 3 }}>Hast du einen Witz 😁💎 auf Lager, und brennst darauf diesen mit der Welt zu teilen? 🌍</Typography>
                    <Typography variant="h5">Dann bist du hier genau richtig! Wir sind immer auf der Suche nach neuen, originellen und humorvollen Witzen für den Witz des Tages und würden uns freuen, wenn du deinen Lieblingswitz mit uns teilst.</Typography>
                </ContentCard>
            </Grid>
        );
    }

    return (
        <Grid
            container
            spacing={isMobile ? 3 : 10}
            display={"flex"}
            alignItems="center"
            justifyContent={isMobile ? "center" : "space-between"}
        >
            <Grid item xs={12} lg={7} textAlign={"center"}>
                <Typography variant={"h1"} fontWeight={"bold"}>Werde ein Teil des Witz des Tages 🤙🏼</Typography>
            </Grid>

            {isSmallerThanLg ? catchingSection() : motivationSection()}

            <Grid
                item xs={12}
                container
                display={"flex"}
                justifyContent={"space-between"}
                spacing={isMobile ? 3 : 10}
            >
                {isSmallerThanLg ? motivationSection() : catchingSection()}
                <Grid
                    item
                    xs={12} lg={5}
                    display={"flex"}
                    alignItems={"center"}
                    justifyContent={{ md: "flex-end", xs: "center" }}
                >
                    <ContentCard
                        transform="rotate(-2deg)"
                        backgroundColor={alpha(theme.palette.secondary.main, 0.3)}
                    >
                        <Typography fontWeight={"bold"} variant="h4" sx={{ pb: 1 }}>Bitte beachte:</Typography>
                        <Box
                            textAlign={"left"}
                        >
                            <Typography variant="h6">✅ Wir freuen uns über humorvolle, kreative und positive Witze.</Typography>
                            <Typography variant="h6">❌ Witze, die diskriminierend, beleidigend oder unangemessen sind, haben bei uns keinen Platz.</Typography>
                            <Typography variant="h6">❌ Politische Witze oder solche, die bestimmte Personengruppen herabwürdigen, werden nicht akzeptiert.</Typography>
                        </Box>
                    </ContentCard>
                </Grid>
            </Grid>

            <Grid item xs={12} lg={10} display={"flex"} justifyContent={{ lg: "flex-end", xs: "center" }}>
                <ContentCard
                    maxWidth="800px"
                    transform="rotate(0deg)"
                    sx={{ width: "700px" }}
                    backgroundColor={alpha(theme.palette.accent.main, 0.3)}
                >
                    <SubmitJokeForm />
                </ContentCard>
            </Grid>
        </Grid>
    );
}

export default SubmitJoke;