from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import Callable, Generator, Iterable, Iterator, TypeVar

from jinja2 import Template

T1 = TypeVar("T1")
T2 = TypeVar("T2")


def item_formatter(template: str) -> Template:
    return Template(
        template,
        variable_start_string="{",
        variable_end_string="}",
        autoescape=False,
        keep_trailing_newline=True,
        finalize=lambda x: x or "",
    )


@contextmanager
def concurrentcontext(
    function: Callable[[T1], T2],
    generator: Iterable[T1],
    *,
    workers: int | None = None,
) -> Generator[Iterator[T2], None, None]:
    """With context, run a function on a batch of arguments concurrently."""

    with ThreadPoolExecutor(max_workers=workers) as executor:
        yield executor.map(function, generator)


def concurrent(
    function: Callable[[T1], T2],
    generator: Iterable[T1],
    *,
    workers: int | None = None,
) -> list[T2]:
    """Run a functions on a batch of arguments in concurrently."""

    with concurrentcontext(function, generator, workers=workers) as results:
        return list(results)
