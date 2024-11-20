import { RootState } from '..';

const migration4 = (state: RootState): RootState => {
  return {
    ...state,
    entities: {
      ...state.entities,
      jokes: {
        ...state.entities.jokes,
        joke_of_the_day: {
          ...state.entities.jokes.joke_of_the_day,
          joke_of_the_day_created_at: null,
        },
      },
    },
  };
};

export default migration4;
