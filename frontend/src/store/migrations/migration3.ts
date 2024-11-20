import { RootState } from '..';

const migration3 = (state: RootState): RootState => {
  return {
    ...state,
    entities: {
      ...state.entities,
      jokes: {
        ...state.entities.jokes,
        joke_of_the_day: {
          id: 0,
          text: "",
          created_at: "",
          created_by: {
            username: "",
          },
          joke_picture: null,
          shareable_image: null,
          joke_of_the_day_created_at: null,
        },
      },
    },
  };
};

export default migration3;
