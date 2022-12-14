import inspect
from textwrap import dedent
from typing import Any, Callable, List

import pandas as pd


### Public functions


def show_solution(exercise_name: str) -> Any:
    """This displays the source code of a solution."""
    func = _get_function(exercise_name)
    source_code = inspect.getsource(func)
    print(source_code)


def run_solution(exercise_name: str, **kwargs) -> Any:
    """This runs the solution, using locals from the calling namespace."""
    func = _get_function(exercise_name)
    frame = inspect.currentframe()
    caller_locals = frame.f_back.f_locals

    arg_names = inspect.getfullargspec(func)[0]

    full_kwargs = {}
    full_kwargs.update({name: caller_locals[name] for name in arg_names})
    full_kwargs.update(kwargs)
    return func(**full_kwargs)


def describe(text: str) -> Callable[[Callable], Callable]:
    def decorator(f: Callable) -> Callable:
        f.__doc__ = text
        return f

    return decorator


def list_solutions() -> List[str]:
    return [name[9:] for name in globals() if name.startswith("solution_")]


### Basics

def solution_hello_world():
    print("Hello world!")


def solution_last_10_titles(titles: pd.Series) -> pd.Series:
    """Select the last 10 movie titles from the list."""
    return titles[-10:]


def solution_list_like(titles: pd.Series) -> None:
    """Choose a few more operations you would typically do with
    a list and try to apply them on titles. What will happen?"""
    sorted(titles)  # OK
    reversed(titles)  # OK
    # TODO: Add a few?

def solution_actors_and_ages() -> pd.DataFrame:
    return pd.DataFrame([
        {"first_name": "Meryl", "surname": "Streep", "age": 73},
        {"first_name": "Emma", "surname": "Watson", "age": 32},
        {"first_name": "Ian", "surname": "MacKellen", "age": 83},
    ])


### Data manipulation

def solution_genre_histogram(movie_titles_with_genre_count: pd.DataFrame) -> pd.DataFrame:
    return px.histogram(movie_titles_with_genre_count, "genre_count")


def solution_10_oldest(movie_titles: pd.DataFrame) -> pd.DataFrame:
    """Find the 10 oldest movies that are longer than 2 hours."""
    return movie_titles[movie_titles["runtimeMinutes"] > 120].nsmallest(10, "startYear")


def solution_longest_title(movie_titles: pd.DataFrame) -> pd.Series:
    """Show the row with the movie having the longest (primary) title."""
    return movie_titles.loc[movie_titles["primaryTitle"].str.len().idxmax()]


def solution_pink(movie_titles: pd.DataFrame) -> pd.DataFrame:
    is_pink = movie_titles["primaryTitle"].str.contains("Pink Panther")
    return movie_titles[is_pink]


def solution_hour_length(movie_titles: pd.DataFrame) -> pd.DataFrame:
    return movie_titles.assign(runtimeHours=movie_titles["runtimeMinutes"] / 60)


def solution_qe2_reign(movie_titles, reign_start=1952, reign_end=2022):
    reign_movies = movie_titles[(movie_titles["year"] >= reign_start) & (movie_titles["year"] <= reign_end)]
    return len(reign_movies) / len(movie_titles)


def solution_binge_watch(movie_titles):
    from datetime import datetime

    last_year_movies = movie_titles[movie_titles["year"] == 2021]
    last_year_minutes = last_year_movies["runtimeMinutes"].sum()    
    return datetime.now() + pd.Timedelta(minutes=last_year_minutes)


def solution_drop_imdb_id(movies_rated):
    movies_rated = movies_rated.drop(columns=["imdb_id"])
    return movies_rated


def solution_plot_budget_corr(movies_rated_cpi):
    return px.scatter(movies_rated_cpi, x="revenue", y="vote_average", log_x=True)


def solution_cpi_2022(cpi):
    month_cols = cpi.columns[1:13]
    cpi = cpi.assign(
        Annual=cpi["Annual"].where(cpi["Annual"].notna(), cpi[month_cols].mean(axis="columns"))
    )
    return cpi


def solution_cpi_validate_merge(movies_rated, cpi):
    movies_rated_cpi_all = movies_rated.merge(
        cpi[["year", "Annual"]].rename(columns={"Annual": "CPI"}),
        on="year",
        validate="many_to_one",
    )
    return movies_rated_cpi_all


def solution_hover_data(movies_rated_cpi):
    return px.scatter_matrix(
        movies_rated_cpi, 
        dimensions=["averageRating", "budget", "popularity", "revenue", "vote_average"],
        hover_name="primaryTitle",
        hover_data=movies_rated_cpi.columns,
        opacity=0.3,
    )


def solution_inflation_adjust(movies_rated_cpi):
    cpi_2022 = cpi.loc[cpi["year"] == 2022, "Annual"].item()

    revenue_2022 = movies_rated_cpi["revenue"] / movies_rated_cpi["CPI"] * cpi_2022
    budget_2022 = movies_rated_cpi["budget"] / movies_rated_cpi["CPI"] * cpi_2022

    movies_rated_cpi_2022 = movies_rated_cpi.assign(
        revenue_2022=revenue_2022,
        budget_2022=budget_2022,
    )

    return movies_rated_cpi_2022


def solution_sort_decades(movies_rated_cpi):
    return px.box(
        movies_rated_cpi.assign(decade=decades).sort_values("year", ascending=True),
        x="decade",
        y="averageRating",
    )


def solution_star_rating(movies_rated_cpi):
    star_rating = pd.qcut(
        movies_rated_cpi["averageRating"],
        q=5,
        labels=range(1, 6),
    )
    return star_rating


def solution_pivot_table(decades_and_genres):
    pivot_table = decades_and_genres.pivot_table(values="numVotes", index="year", columns="genre", aggfunc="sum")
    return pivot_table


def solution_genre_normalize(decades_vs_genres_crosstab):
    return decades_vs_genres_crosstab / decades_vs_genres_crosstab.mean(axis="rows")


def _get_function(exercise_name: str) -> Callable:
    try:
        return globals()[f"solution_{exercise_name}"]
    except KeyError:
        print(f"There is no solution defined for {exercise_name}.")
