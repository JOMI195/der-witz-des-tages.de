import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAppDispatch } from "@/store";
import { activateJokeNewsletterSubscription } from "@/store/entities/jokeNewsletter/jokeNewsletter.actions";
import { getHomeUrl } from "@/assets/endpoints/app/appEndpoints";

const Activation = () => {
    const { activation_token } = useParams();
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        navigate(getHomeUrl(), { replace: true });
        dispatch(activateJokeNewsletterSubscription(activation_token as string));
    }, []);

    return null;
};

export default Activation;