import { getRandomMuiColor } from '@/common/utils/color/color';
import { useAppDispatch, useAppSelector } from '@/store';
import { fetchJokesWithPicturesPaginated, setJokesWithPicturesPaginatedPage } from '@/store/entities/jokes/jokes.actions';
import { getApi, getJokesWithPicturesPaginated } from '@/store/entities/jokes/jokes.slice';
import InstagramIcon from '@mui/icons-material/Instagram';
import { IJoke, IJokesWithPicturesPaginated } from '@/types';
import {
    Box,
    Card,
    CardContent,
    Skeleton,
    Typography,
    Grid,
    Container,
    Pagination,
    useTheme,
    TextField,
    MenuItem,
    useMediaQuery,
    Button,
} from '@mui/material';
import { useEffect, useState } from 'react';
import JokeCard from './card';

const Archive = () => {
    const theme = useTheme();
    const dispatch = useAppDispatch();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const paginatedJokes: IJokesWithPicturesPaginated = useAppSelector(getJokesWithPicturesPaginated);
    const jokesApiLoading = useAppSelector(getApi).loading;

    const [pageSize, setPageSize] = useState(10);
    const [filterText, setFilterText] = useState('');

    useEffect(() => {
        dispatch(fetchJokesWithPicturesPaginated(paginatedJokes.page, pageSize));
    }, [dispatch, paginatedJokes.page, pageSize]);

    const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
        dispatch(setJokesWithPicturesPaginatedPage(value));
    };

    const handleFilterTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFilterText(event.target.value);
    };

    const handlePageSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newPageSize = parseInt(event.target.value);
        setPageSize(newPageSize);
    };

    const filteredJokes = paginatedJokes.results.filter((joke) => {
        const textMatch = joke.text.toLowerCase().includes(filterText.toLowerCase());
        return textMatch;
    });

    const totalPages = Math.ceil(paginatedJokes.count / pageSize);

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            <Typography variant={"h1"} fontWeight={"bold"} sx={{ mb: isMobile ? 3 : 5, }}>Witze Galerie 🗄️</Typography>
            <Box
                sx={{ mb: isMobile ? 3 : 5, }}
            >
                <Typography variant="h5" sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}>
                    Die ganze Galerie ist auch auf
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

            <Box sx={{ mb: 4, display: "flex" }}>
                {!isMobile ? <Box sx={{ flexGrow: 1 }} /> : null}
                <TextField
                    label="Durchsuche Seite"
                    value={filterText}
                    onChange={handleFilterTextChange}
                    sx={{
                        mr: 2,
                        flexGrow: isMobile ? 1 : 0,
                    }}
                />
                <TextField
                    select
                    label="Anzahl Witze"
                    value={pageSize}
                    onChange={handlePageSizeChange}
                    sx={{
                        minWidth: "120px"
                    }}
                >
                    <MenuItem value={10}>10</MenuItem>
                    <MenuItem value={20}>20</MenuItem>
                    <MenuItem value={50}>50</MenuItem>
                </TextField>
            </Box>

            <Grid container spacing={5}>
                {jokesApiLoading ? (
                    Array.from({ length: pageSize <= 3 ? pageSize : 3 }).map((_, index) => (
                        <Grid item key={index} xs={12} sm={6} md={4}>
                            <Card
                                sx={{
                                    height: '100%',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    transition: 'transform 0.2s'
                                }}
                            >
                                <Skeleton variant="rectangular" height={300} />
                                <CardContent
                                    sx={{
                                        flexGrow: 1,
                                        backgroundColor: getRandomMuiColor(theme)
                                    }}
                                >
                                    <Box
                                        sx={{
                                            height: '100px',
                                            display: 'flex',
                                            flexDirection: 'column',
                                            justifyContent: 'space-between'
                                        }}
                                    >
                                        <Skeleton variant="text" />
                                        <Skeleton variant="text" width="50%" />
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))
                ) : (
                    filteredJokes.length !== 0 ? (
                        filteredJokes.map((joke: IJoke) => (
                            <Grid item key={joke.id} xs={12} sm={6} md={4}>
                                <JokeCard joke={joke} />
                            </Grid>
                        ))
                    ) : (
                        paginatedJokes.results.length !== 0 ? (
                            <Box
                                sx={{
                                    display: "flex",
                                    flexDirection: "column",
                                    justifyContent: "center",
                                    alignItems: "center",
                                    my: isMobile ? 3 : 5,
                                    textAlign: "center"
                                }}
                            >
                                <Typography variant={"h4"} fontWeight={"bold"} sx={{ mb: 1 }}>
                                    Leider stimmen keine Witze auf dieser Seite mit deiner Suche überein 😔
                                </Typography>
                                <Button variant='contained' onClick={() => setFilterText("")}>
                                    Filter zurücksetzen
                                </Button>
                            </Box>

                        ) : (
                            <Typography variant={"h4"} fontWeight={"bold"}>
                                Keine Witze vorhanden 😔
                            </Typography>
                        )
                    )
                )}
            </Grid>

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <Pagination
                    showFirstButton={paginatedJokes.page > 1}
                    showLastButton={paginatedJokes.page < totalPages}
                    count={totalPages}
                    page={paginatedJokes.page}
                    onChange={handlePageChange}
                    color="primary"
                    disabled={paginatedJokes.page === 1 && !paginatedJokes.next}
                />
            </Box>
        </Container>
    );
};

export default Archive;