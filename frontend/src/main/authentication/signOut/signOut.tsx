import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import {
  signOutUser,
} from "@/store/entities/authentication/authentication.actions";
import { getHomeUrl } from "@/assets/endpoints/app/appEndpoints";

export default function SignOut() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSignOut = () => {
    dispatch(signOutUser());
    navigate(getHomeUrl(), { replace: true });
  };

  const handleCancel = () => {
    navigate(getHomeUrl(), { replace: true });
  };

  return (
    <Box>
      <Typography component="h1" variant="h5" textAlign={"center"}>
        {"Abmelden"}
      </Typography>
      <Box
        component="form"
        id="sign-out-form"
        noValidate
        sx={{ mt: 3 }}
      >
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="body1" textAlign={"center"}>
              {"Bist du dir wirklich sicher, dass du dich abmelden willst?"}
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Button
              type="button"
              form="sign-out-form"
              fullWidth
              variant="contained"
              color="primary"
              onClick={handleSignOut}
            >
              {"Abmelden"}
            </Button>
          </Grid>
          <Grid item xs={12}>
            <Button
              type="button"
              fullWidth
              variant="outlined"
              color="secondary"
              onClick={handleCancel}
            >
              {"Abbrechen"}
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}
