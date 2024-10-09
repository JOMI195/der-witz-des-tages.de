import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAppDispatch } from "@/store";
import { unsubscribeFromJokeNewsletter } from "@/store/entities/jokeNewsletter/jokeNewsletter.actions";
import { getHomeUrl } from "@/assets/endpoints/app/appEndpoints";

const Unsubscribtion = () => {
    const { unsubscribe_token } = useParams();
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        navigate(getHomeUrl(), { replace: true });
        dispatch(unsubscribeFromJokeNewsletter(unsubscribe_token as string));
    }, []);

    return null;
};

export default Unsubscribtion;