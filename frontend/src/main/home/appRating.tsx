import React from 'react';
import { Box, Typography, Avatar, Stack, Rating, useTheme } from '@mui/material';

const AppRating: React.FC = () => {
    const theme = useTheme();
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: "column",
                justifyContent: "center",
                alignItems: 'center',
                gap: 1
            }}
        >
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: 'center',
                }}
            >
                <Stack direction="row" spacing={-1}>
                    {[...Array(3)].map((_, index) => (
                        <Avatar
                            key={index}
                            sx={{
                                width: 25,
                                height: 25,
                                bgcolor: theme.palette.grey[400],
                                fontSize: '12px'
                            }}
                        />
                    ))}
                </Stack>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                    <Rating
                        name="size-large"
                        value={5}
                        size="large"
                        readOnly
                        sx={{
                            color: theme.palette.accent.main,
                            '& .MuiRating-iconEmpty': {
                                color: theme.palette.grey[400],
                            },
                        }}
                    />
                </Box>
            </Box>

            <Typography
                variant="body2" color="text.secondary" textAlign={"center"}
            >
                Bringen schon<Box fontSize={'h5.fontSize'} component="span" fontWeight='bold'> 30+ </Box>Nutzer täglich zum lachen 🎉
            </Typography>
        </Box>
    );
};

export default AppRating;