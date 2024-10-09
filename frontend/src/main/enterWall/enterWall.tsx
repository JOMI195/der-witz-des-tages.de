import ContentCard from "@/common/components/contentCard";
import Logo from "@/common/components/logo";
import { alpha, Box, Container, Grid, Link, Typography, useTheme } from "@mui/material";

const EnterWall = () => {
    const theme = useTheme();
    return (
        <Container component="main" maxWidth="md">
            <Box
                sx={{
                    my: 10,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    width: "100%",
                    textAlign: " center"
                }}
            >
                <Box sx={{ mb: 7, width: "100%" }}>
                    <Logo
                        darkLogoSrc="/witz-des-tages-logo-dark-full.svg"
                        lightLogoSrc="/witz-des-tages-logo-light-full.svg"
                        marginRight={0}
                        clickable={false}
                    />
                </Box>
                <Grid container>
                    <Grid item xs={12} display={"flex"} justifyContent={"center"}>
                        <ContentCard
                            transform={"rotate(3deg)"}
                            backgroundColor={alpha(theme.palette.primary.main, 0.2)}
                        >
                            <Typography gutterBottom variant="h4">Hey Leute! 🚀 Unsere Seite für den ultimativen Witz des Tages ist bald am Start! 🎉 Bleibt dran, denn wir bringen euch die besten Lacher direkt auf den Bildschirm! 📲 Bis dahin, bleibt cool und lacht euch schon mal warm!🔥</Typography>
                            <Typography variant="h6">Bei Fragen vorab: <Link href="mailto:info@der-witz-des-tages.de">info@der-witz-des-tages.de</Link></Typography>
                        </ContentCard>
                    </Grid>
                </Grid>

            </Box>
        </Container>
    );
}

export default EnterWall;