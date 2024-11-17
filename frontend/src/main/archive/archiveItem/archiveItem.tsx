import { useAppSelector } from "@/store";
import { getJokesWithPicturesPaginated } from "@/store/entities/jokes/jokes.slice";
import { IJokesWithPicturesPaginated } from "@/types";
import { Typography } from "@mui/material";
import { useParams } from "react-router-dom";


const ArchiveItem = () => {
    const { archive_item_id } = useParams();
    const paginatedJokes: IJokesWithPicturesPaginated = useAppSelector(getJokesWithPicturesPaginated);
    const joke = paginatedJokes.results.find(joke => joke.id === Number(archive_item_id))

    if (joke === undefined) {
        return (
            <Typography
                variant={"h3"}
                fontWeight={"bold"}
                textAlign={"center"}
                sx={{ mt: 20 }}
            >
                Leider konnten wir diesen Witz nicht in unserem Archiv finden 😔
            </Typography>
        );
    }

    return (
        <>
            {joke.text}
        </>
    );
}

export default ArchiveItem;