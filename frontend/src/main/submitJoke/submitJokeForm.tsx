import { useEffect, useState } from 'react';
import { useFormik, getIn } from 'formik';
import * as yup from 'yup';
import { TextField, Button, Grid, Box, useMediaQuery, useTheme, Card, CardContent, Typography } from '@mui/material';
import { useAppDispatch, useAppSelector } from '@/store';
import { keyframes } from '@emotion/react';
import { submitJoke } from '@/store/entities/jokes/jokes.actions';
import { getUser } from '@/store/entities/authentication/authentication.slice';
import { Link } from 'react-router-dom';
import { getAuthenticationUrl, getSignInUrl } from '@/assets/endpoints/app/authEndpoints';

const submitButtonShakeAnimation = keyframes`
  0% { transform: translateX(0) rotate(0deg); }
  25% { transform: translateX(-5px) rotate(-3deg); }
  50% { transform: translateX(5px) rotate(3deg); }
  75% { transform: translateX(-5px) rotate(-3deg); }
  100% { transform: translateX(0) rotate(0deg); }
`;

const SubmitJokeForm = () => {
    const [submitButtonShouldShake, setSubmitButtonShouldShake] = useState(false);
    const dispatch = useAppDispatch();
    const [initialValues] = useState({
        joke: "",
    });

    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    const loggedIn = useAppSelector(getUser).loggedIn;

    const validationSchema = yup.object({
        joke: yup.string()
            .required('Dieses Feld wird benötigt'),
    });

    const submitJokeForm = useFormik({
        initialValues: initialValues,
        validationSchema: validationSchema,
        enableReinitialize: true,
        onSubmit: async (values: any) => {
            dispatch(submitJoke(values.joke));
            submitJokeForm.resetForm();
        },
    });

    useEffect(() => {
        const interval = setInterval(() => {
            setSubmitButtonShouldShake(true);
            setTimeout(() => setSubmitButtonShouldShake(false), 500);
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    return (
        <Box position="relative">
            <Box
                component='form'
                id='submit-joke-form'
                noValidate
                onSubmit={submitJokeForm.handleSubmit}
                sx={{
                    filter: loggedIn ? 'none' : 'blur(5px)',
                    pointerEvents: loggedIn ? 'auto' : 'none',
                    userSelect: loggedIn ? 'auto' : 'none',
                }}
            >
                <Grid
                    container
                    spacing={2}
                    alignItems={'center'}
                    justifyContent={isMobile ? 'center' : "flex-end"}
                >
                    <Grid
                        item
                        xs={12}
                    >
                        <TextField
                            id='joke'
                            name='joke'
                            label="Hier rein mit dem Witz ✏️"
                            value={submitJokeForm.values.joke}
                            onBlur={submitJokeForm.handleBlur}
                            error={
                                submitJokeForm.touched.joke && Boolean(submitJokeForm.errors.joke)
                            }
                            helperText={
                                getIn(submitJokeForm.touched, "joke") &&
                                getIn(submitJokeForm.errors, "joke")
                            }
                            onChange={submitJokeForm.handleChange}
                            fullWidth
                            autoComplete='joke'
                            variant='outlined'
                            multiline
                            rows={4}
                        />
                        <Typography variant="subtitle2">⚠️ Mit der Einsendung von Inhalten überträgst du alle Rechte daran an uns. Wir dürfen die Inhalte nach Belieben verwenden, bearbeiten und veröffentlichen.</Typography>
                    </Grid>
                    <Grid
                        item
                        container
                        xs={12}
                        spacing={2}
                        display={"flex"}
                        justifyContent={"space-between"}
                    >
                        <Grid
                            item
                            xs={12}
                            md={6}
                            sx={{ order: { xs: 1, md: 2 }, }}
                        >
                            <Button
                                type='submit'
                                fullWidth
                                form='submit-joke-form'
                                variant='contained'
                                sx={{
                                    height: "100%",
                                    fontWeight: "bold",
                                    fontSize: 'h6.fontSize',
                                    animation: submitButtonShouldShake
                                        ? `${submitButtonShakeAnimation} 0.5s ease`
                                        : 'none',
                                }}
                            >
                                {'Jetzt Einreichen'}
                            </Button>
                        </Grid>
                        <Grid
                            item
                            xs={12}
                            md={6}
                            sx={{ order: { xs: 2, md: 1 }, }}
                        >
                            <Button
                                type="button"
                                fullWidth
                                variant="outlined"
                                color="secondary"
                                onClick={() => submitJokeForm.resetForm()}
                            >
                                {"Zurücksetzen"}
                            </Button>
                        </Grid>
                    </Grid>
                </Grid>
            </Box>
            {!loggedIn && (
                <Card
                    sx={{
                        position: 'absolute',
                        top: '54%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        zIndex: 1,
                        width: '80%',
                        maxWidth: 500,
                    }}
                >
                    <CardContent>
                        <Typography variant="h5" component="div" gutterBottom>
                            Anmeldung erforderlich 🔑
                        </Typography>
                        <Typography variant="body1" color="text.secondary">
                            Um einen Witz einzureichen wird ein Nutzerkonto vorrausgesezt. Bitte melde dich an oder registrere dich.
                        </Typography>
                        <Button
                            variant="contained"
                            color="primary"
                            component={Link}
                            to={getAuthenticationUrl() + getSignInUrl()}
                            sx={{ mt: 2 }}
                        >
                            Jetzt Anmelden
                        </Button>
                    </CardContent>
                </Card>
            )}
        </Box>
    );
};

export default SubmitJokeForm;