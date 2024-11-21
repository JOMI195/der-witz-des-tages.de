import { formatDateOnly } from "@/common/utils/date/date";
import { IJoke } from "@/types";
import { Avatar, Box, CardMedia, Typography } from "@mui/material";


const MEDIA_BASE_URL = import.meta.env.VITE_API_MEDIA_BASE_URL;

const getRandomRotations = (): [number, number] => {
    /**
     * Generate random rotation values for the image and card.
     * 
     * @returns [imageRotation, cardRotation]
     */
    const getRandomValue = (min: number, max: number): number =>
        Math.random() * (max - min) + min;

    const imageRotation = getRandomValue(-1, 1);
    const cardRotation = getRandomValue(-1, 1);

    if (Math.random() < 0.5) {
        return [cardRotation, imageRotation];
    }

    return [imageRotation, cardRotation];
}

function getRandomColor(colorList?: string[]): string {
    /**
     * Select a random color from the provided list or default colors.
     * 
     * @param colorList - Optional array of color strings
     * @returns A randomly selected color string
     */
    const defaultColors = ["#D5C8F4", "#F1E3C7", "#F2D7EC"];
    const colors = colorList ?? defaultColors;
    return colors[Math.floor(Math.random() * colors.length)];
}


interface IJokeCardProps {
    joke: IJoke
}

const JokeCard: React.FC<IJokeCardProps> = ({ joke }) => {
    const cardColor = getRandomColor();
    const cardRotations = getRandomRotations();

    // const navigateToArchiveItem = (jokeId: number) => {
    //     navigate(`${jokeId}`, { replace: true });
    // }

    return (
        <Box
            sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            {joke.joke_picture?.image && (
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                    }}
                >
                    <CardMedia
                        component="img"
                        image={MEDIA_BASE_URL + joke.joke_picture.image}
                        alt="joke image"
                        sx={{
                            width: '85%',
                            aspectRatio: '1 / 1',
                            objectFit: 'cover',
                            borderRadius: 2,
                            transform: `rotate(${cardRotations[0]}deg)`,
                            boxShadow: 2
                        }}
                    />
                </Box>
            )}
            <Box
                sx={{
                    backgroundColor: cardColor,
                    transform: `rotate(${cardRotations[1]}deg)`,
                    p: 2,
                    borderRadius: 1,
                    boxShadow: 2,
                    marginTop: '-30px',
                    zIndex: 1,
                    minHeight: 120,
                    display: "flex",
                    flexDirection: "column"
                }}
            >
                <Typography color={"black"} variant="body1" sx={{ flexGrow: 1 }}>{joke.text}</Typography>
                {joke.created_by.username !== "" && (
                    <Box
                        sx={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            mt: 2,
                            textWrap: "stable"
                        }}
                    >
                        <Typography color={"black"} variant="caption">
                            {"Eingereicht von"}
                        </Typography>
                        <Avatar
                            sx={{
                                width: 5,
                                height: 5,
                                p: 1.5,
                                mx: 1,
                                color: "white"
                            }}
                            alt="Account"
                        >
                            {`${joke.created_by.username === "admin" ? "jomi".slice(0, 1).toUpperCase() : joke.created_by.username.slice(0, 1).toUpperCase()}`}
                        </Avatar>
                        <Typography color={"black"} variant="body2">
                            {
                                `${joke.created_by.username === "admin" ? "jomi" : joke.created_by.username}`
                            }
                        </Typography>
                    </Box>
                )}
                {joke.joke_of_the_day_created_at && (
                    <Typography color={"black"} variant="caption" sx={{ textAlign: 'center', mt: 1 }}>
                        {formatDateOnly(joke.joke_of_the_day_created_at)}
                    </Typography>
                )}
            </Box>
        </Box>
    );
};

export default JokeCard;