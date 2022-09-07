import inspect
from typing import Any, Callable

import pandas as pd
from IPython.display import Code


### Public functions

def show_solution(exercise_name: str) -> Code:
    """This displays the source code of a solution."""
    func = _get_function(exercise_name)
    source_code = inspect.getsource(func)
    return Code(source_code, language="python")


def run_solution(exercise_name: str, **kwargs) -> Any:
    """This runs the solution, using locals from the calling namespace."""
    func = _get_function(exercise_name)
    frame = inspect.currentframe()
    caller_locals = (frame.f_back.f_locals)

    arg_names = inspect.getfullargspec(func)[0]
    
    full_kwargs = {}
    full_kwargs.update({name: caller_locals[name] for name in arg_names})
    full_kwargs.update(kwargs)
    return func(**full_kwargs)


### Data manipulation

def solution_10_oldest(movie_titles: pd.DataFrame) -> pd.DataFrame:
    """Find the 10 oldest movies that are longer than 2 hours."""
    return movie_titles[movie_titles["runtimeMinutes"] > 120].nsmallest(10, "startYear")


def solution_longest_title(movie_titles: pd.DataFrame) -> pd.Series:
    """Show the row with the movie having the longest (primary) title."""
    return movie_titles.loc[movie_titles["primaryTitle"].str.len().idxmax()]


def solution_pink(movie_titles: pd.DataFrame) -> pd.DataFrame:
    is_pink = movie_titles["primaryTitle"].str.contains("Pink Panther")
    return movie_titles[is_pink]


def solution_hour_length(movie_titles: pd.DataFrame) -> pd.Series:
    return movies_titles.assign(
        runtimeHours=movie_titles["runtimeMinutes"] / 60
    )


def _get_function(exercise_name: str) -> Callable:
    try:
        return globals()[f"solution_{exercise_name}"]
    except KeyError:
        print(f"There is no solution defined for {exercise_name}.")
