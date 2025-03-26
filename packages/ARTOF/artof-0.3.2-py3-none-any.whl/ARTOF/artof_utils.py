import os

def get_next_step(iter: int, step: int, lens_steps: int):
        """
        Get the next step of a run

        Args:
            iter: Current iteration.
            step: Current step.
            lens_steps: Total number of steps.

        Returns:
            Next iteration and step
        """


        if step == lens_steps-1:
            return iter+1, 0
        return iter, step+1

def is_last_file(iter: int, step: int, lens_steps: int, stop_iter: int):
    """
    Check if the current file is the last file of a run

    Args:
        iter: Current iteration.
        step: Current step.
        lens_steps: Total number of steps.
        stop_iter: Maximum number of iterations.

    Returns:
        Boolean value if the current file is the last file
    """

    return iter == stop_iter-1 and step == lens_steps-1

def next_file_exists(path: str, iter: int, step: int, lens_steps: int, stop_iter: int):
    """
    Check if the next file of a run exists

    Args:
        path: Path where data files are located.
        iter: Current iteration.
        step: Current step.
        lens_steps: Total number of steps.

    Returns:
        Boolean value if the next file exists
    """

    next_step = get_next_step(iter, step, lens_steps)
    return os.path.exists(f'{path}/{next_step[0]}_{next_step[1]}') or is_last_file(iter, step, lens_steps, stop_iter)