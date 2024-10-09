import random
from django.db.models import Sum
from jokes.models import Joke, JokeOfTheDay


def get_joke_of_the_day() -> Joke:
    # Get the IDs of jokes that have already been used
    used_jokes = JokeOfTheDay.objects.values_list("joke_id", flat=True)

    # Filter out used jokes
    available_jokes = Joke.objects.exclude(id__in=used_jokes)

    # If no unused jokes, use all jokes
    if not available_jokes.exists():
        available_jokes = Joke.objects.all()

    # If no jokes at all, raise an exception
    if not available_jokes.exists():
        raise ValueError("No jokes available.")

    # Calculate the total sum of the weights
    total_weight = available_jokes.aggregate(
        total_weight=Sum("joke_of_the_day_selection_weight")
    )["total_weight"]

    if total_weight is None:
        raise ValueError("No jokes with valid weights available.")

    # Generate a random number between 0 and total_weight
    random_value = random.uniform(0, total_weight)

    # Find the joke corresponding to the random value by traversing the weights
    cumulative_weight = 0
    for joke in available_jokes:
        cumulative_weight += joke.joke_of_the_day_selection_weight
        if cumulative_weight >= random_value:
            return joke

    # Fallback in case something goes wrong
    raise ValueError("Joke selection failed.")


def create_joke_of_the_day_entry(joke: Joke):
    JokeOfTheDay.objects.create(joke=joke)
