import inspect
from IPython.display import Code


def show_solution(exercise_name: str) -> Code:
    try:
        func = globals()[f"solution_{exercise_name}"]
    except KeyError:
        print(f"There is no solution defined for {exercise_name}.")
    else:
        source_code = inspect.getsource(func)
        return Code(source_code, language="python")
        


def solution_longest_title(movies):
    longest_title_movie = "a"


if __name__ == "__main__":
    show_solution("longest_title")