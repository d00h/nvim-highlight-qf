import os
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from pstats import Stats
from typing import Iterable


@dataclass
class ProfilerItemLocation:

    filename: str
    line: int
    funcname: str


@dataclass
class ProfilerItemMetrics:

    total_calls: int
    prim_calls: int
    total_time: float
    cum_time: float


@dataclass
class ProfilerItem:

    location: ProfilerItemLocation
    metrics: ProfilerItemMetrics

    @classmethod
    def expand(cls, stats: dict) -> Iterable['ProfilerItem']:
        for key, value in stats.items():
            (fname, line, fn) = key
            (cc, nc, tt, ct) = value[:4]
            yield cls(
                location=ProfilerItemLocation(
                    filename=fname,
                    line=line,
                    funcname=fn,
                ),
                metrics=ProfilerItemMetrics(
                    total_calls=nc,
                    prim_calls=cc,
                    total_time=tt,
                    cum_time=ct,
                )
            )
            # childs = value[4] if len(value) == 5 else {}
            # yield from cls.expand(childs)

    @classmethod
    def parse_file(cls, filename) -> Iterable['ProfilerItem']:
        stats = Stats()
        stats.load_stats(filename)
        yield from cls.expand(stats.stats)


METRICS = {
    'total_time': lambda item: f'total_time={item.metrics.total_time:.10f}',
    'total_calls': lambda item: f'total_calls={item.metrics.total_calls}',
    'prim_calls': lambda item: f'prim_calls={item.metrics.prim_calls}',
    'cum_time': lambda item: f'cum_time={item.metrics.cum_time:.10f}',
}


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description='Print python profiler data as vimgrep format')
    parser.add_argument('metric', choices=METRICS)
    parser.add_argument('filename')
    return parser


def print_error(*args):
    print('error: ', *args, file=sys.stderr)


def main():
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()
    try:
        calc_metric = METRICS[args.metric]
        for item in ProfilerItem.parse_file(args.filename):
            item_metric = calc_metric(item)
            print(f'{item.location.filename}:{item.location.line}:{item_metric}')
    except FileNotFoundError:
        print_error('not_found', os.path.abspath(args.filename))


if __name__ == '__main__':
    main()
