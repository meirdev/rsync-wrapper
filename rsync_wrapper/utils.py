from rich.progress import BarColumn, Progress, TaskID, TextColumn

from . import error_codes, types


def rich_progress(
    output_iter: types.OutputIterator,
    # TODO: progress: Progress | None = None,
    # TODO: task_id: TaskID | None = None,
) -> int:
    progress = Progress(
        TextColumn("{task.fields[offset]}"),
        BarColumn(),
        TextColumn("{task.fields[rate]}{task.fields[units]} {task.fields[remain]}"),
    )

    task_id = progress.add_task("", rate="-", units="-", remain="-", offset="-")

    with progress:
        for out in output_iter:
            if isinstance(out, types.ProgressBar):
                progress.update(
                    task_id,
                    completed=out.percentage,
                    rate=out.rate,
                    units=out.units,
                    remain=out.remain,
                    offset=out.offset,
                )
            elif isinstance(out, types.StdOut):
                if stdout := out.strip():
                    progress.console.print("[cyan]▏", stdout)
            elif isinstance(out, types.StdErr):
                if stderr := out.strip():
                    progress.console.print("[red]▏", stderr)
            elif isinstance(out, types.ExitCode):
                if out != error_codes.RErr.OK.code:
                    if err := error_codes.get_error_code(out):
                        progress.console.print("[red]▏", err.message)
                    return out

        return 0
