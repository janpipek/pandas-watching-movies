import inspect


def show_solution(exercise_name: str) -> None:
    try:
        func = globals()[f"solution_{exercise_name}"]
    except KeyError:
        print(f"There is no solution defined for {exercise_name}.")
    else:
        source_code = inspect.getsource(func)
        print(source_code)


def solution_longest_title(movies):
    longest_title_movie = "a"


if __name__ == "__main__":
    show_solution("longest_title")