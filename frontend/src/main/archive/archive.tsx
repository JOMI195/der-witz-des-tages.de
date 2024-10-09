import { useAppDispatch, useAppSelector } from '@/store';
import { fetchJokesWithPicturesPaginated } from '@/store/entities/jokes/jokes.actions';
import { getJokesWithPicturesPaginated, jokesWithPicturesPaginatedPageSet } from '@/store/entities/jokes/jokes.slice';
import { IJoke, IJokesWithPicturesPaginated } from '@/types';
import { Box } from '@mui/material';
import { useEffect } from 'react';

const MEDIA_BASE_URL = import.meta.env.VITE_API_MEDIA_BASE_URL;

const Archive = () => {
    const dispatch = useAppDispatch();

    const paginatedJokes: IJokesWithPicturesPaginated = useAppSelector(getJokesWithPicturesPaginated);

    useEffect(() => {
        dispatch(fetchJokesWithPicturesPaginated(paginatedJokes.page));
    }, []);

    const handleNextPage = () => {
        if (paginatedJokes.next) {
            dispatch(jokesWithPicturesPaginatedPageSet(paginatedJokes.page + 1));
        }
    };

    const handlePreviousPage = () => {
        if (paginatedJokes.previous) {
            dispatch(jokesWithPicturesPaginatedPageSet(paginatedJokes.page - 1));
        }
    };

    return (
        <Box>
            <ul>
                {paginatedJokes.results.map((joke: IJoke) => (
                    <li key={joke.id}>
                        {joke.text} - <img width={"200px"} height={"200px"} src={MEDIA_BASE_URL + joke.joke_picture?.image} alt="joke" />
                    </li>
                ))}
            </ul>
            <div>
                <button disabled={!paginatedJokes.previous} onClick={handlePreviousPage}>
                    Previous
                </button>
                <button disabled={!paginatedJokes.next} onClick={handleNextPage}>
                    Next
                </button>
            </div>
        </Box>
    );
};

export default Archive;
