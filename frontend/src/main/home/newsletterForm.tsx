import { useEffect, useState } from 'react';
import { useFormik, getIn } from 'formik';
import * as yup from 'yup';
import { TextField, Button, Grid, Box, useMediaQuery, useTheme, Alert } from '@mui/material';
import { useAppDispatch } from '@/store';
import { subscribeToJokeNewsletter } from '@/store/entities/jokeNewsletter/jokeNewsletter.actions';
import { keyframes } from '@emotion/react';
import { INewsletterRecieverSubscribeResponse, isINewsletterRecieverSubscribeResponse } from '@/types';

const subscribeButtonShakeAnimation = keyframes`
  0% { transform: translateX(0) rotate(0deg); }
  25% { transform: translateX(-5px) rotate(-3deg); }
  50% { transform: translateX(5px) rotate(3deg); }
  75% { transform: translateX(-5px) rotate(-3deg); }
  100% { transform: translateX(0) rotate(0deg); }
`;

const NewsletterForm = () => {
    const [subscribeButtonShouldShake, setSubscribeButtonShouldShake] = useState(false);
    const dispatch = useAppDispatch();
    const [initialValues] = useState({
        email: "",
    });

    const [subscribeMessage, setSubscribeMessage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));

    const validationSchema = yup.object({
        email: yup.string()
            .email('Email muss gültig sein')
            .required('Dieses Feld wird benötigt'),
    });

    const newsletterForm = useFormik({
        initialValues: initialValues,
        validationSchema: validationSchema,
        enableReinitialize: true,
        onSubmit: async (values: any) => {
            setErrorMessage("");
            setSubscribeMessage("");

            const response: any = await dispatch(subscribeToJokeNewsletter(values.email));
            const newNewsletterRecieverSubscribeResponse = response as INewsletterRecieverSubscribeResponse;
            if (isINewsletterRecieverSubscribeResponse(newNewsletterRecieverSubscribeResponse)) {
                setSubscribeMessage("Anmeldung zum Newsletter erfolgreich. Übeprüfe deine Mails um den täglichen Erhalt des Newsletters zu bestätigen.");
            } else {
                setErrorMessage("Bitte überprüfe deine E-Mail-Adresse auf Tippfehler und der korrekten Domain. Versuche es anschließend erneut. Bei wiederholten Problemen kontaktiere bitte unseren Support.");
            }
            newsletterForm.resetForm();
        },
    });

    useEffect(() => {
        const interval = setInterval(() => {
            setSubscribeButtonShouldShake(true);
            setTimeout(() => setSubscribeButtonShouldShake(false), 500);
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    return (
        <Box
            component='form'
            id='newsletter-form'
            noValidate
            onSubmit={newsletterForm.handleSubmit}
        >
            {subscribeMessage && (
                <Alert severity="success" sx={{ mt: 2, mb: 2 }}>
                    {subscribeMessage}
                </Alert>
            )}
            {errorMessage && (
                <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
                    {errorMessage}
                </Alert>
            )}
            <Grid
                container
                spacing={2}
                direction={isMobile ? 'column' : 'row'}
                alignItems={isMobile ? 'center' : 'flex-start'}
                justifyContent={isMobile ? 'center' : "space-between"}
            >
                <Grid
                    item
                    xs={12}
                    md={7}
                    sx={{ width: isMobile ? '100%' : 'auto' }}
                >
                    <TextField
                        id='email'
                        name='email'
                        label='Email'
                        value={newsletterForm.values.email}
                        onBlur={newsletterForm.handleBlur}
                        error={
                            newsletterForm.touched.email && Boolean(newsletterForm.errors.email)
                        }
                        helperText={
                            getIn(newsletterForm.touched, "email") &&
                            getIn(newsletterForm.errors, "email")
                        }
                        onChange={newsletterForm.handleChange}
                        fullWidth
                        autoComplete='email'
                        variant='outlined'
                        sx={{

                            '& .MuiInputBase-root': {
                                height: '56px',
                            },
                            '& .MuiFormHelperText-root': {
                                position: 'absolute',
                                bottom: '-20px',
                            },
                        }}
                    />
                </Grid>
                <Grid item xs={12} md={5} sx={{ width: isMobile ? '100%' : 'auto' }}>
                    <Button
                        type='submit'
                        fullWidth
                        form='newsletter-form'
                        variant='contained'
                        sx={{
                            height: '56px',
                            fontWeight: "bold",
                            fontSize: 'h6.fontSize',
                            animation: subscribeButtonShouldShake
                                ? `${subscribeButtonShakeAnimation} 0.5s ease`
                                : 'none',
                        }}
                    >
                        {'Jetzt Anmelden'}
                    </Button>
                </Grid>
            </Grid>
        </Box>
    );
};

export default NewsletterForm;