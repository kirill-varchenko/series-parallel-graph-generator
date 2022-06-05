import collections
import itertools
import re
from enum import Enum
from typing import Generator, Optional, Union


def partitions(n: int) -> Generator[list[int], None, None]:
    """
    Integer partitions generator:
    3 -> [[1, 1, 1], [1, 2], [3]]
    """

    if n == 0:
        yield []
        return

    for p in partitions(n - 1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]


class CircuitType(str, Enum):
    NORMAL = "r"
    SERIES = "s"
    PARALLEL = "p"


class Circuit:
    conjugation_pairs = {
        CircuitType.NORMAL: CircuitType.NORMAL,
        CircuitType.SERIES: CircuitType.PARALLEL,
        CircuitType.PARALLEL: CircuitType.SERIES,
    }

    def __init__(
        self,
        type: CircuitType = CircuitType.NORMAL,
        items: Optional[list["Circuit"]] = None,
    ) -> None:
        if type != CircuitType.NORMAL and items is None:
            raise ValueError

        self.type = type
        self.items = items or []

    def canonical(self) -> Union[str, tuple]:
        if self.type == CircuitType.NORMAL:
            return self.type.value
        return (self.type.value, *[item.canonical() for item in self.items])

    def conjugate(self) -> "Circuit":
        if self.type == CircuitType.NORMAL:
            return Circuit()
        return Circuit(
            type=self.conjugation_pairs[self.type],
            items=[item.conjugate() for item in self.items],
        )

    def __str__(self) -> str:
        return re.sub(r"[',]", "", str(self.canonical()))

    def __hash__(self) -> int:
        return hash(self.canonical())


class CircuitGenerator:
    def __init__(self, pre_order: Optional[int] = None) -> None:
        self.generated_order = 0
        self.series_circuits: dict[int, list[Circuit]] = collections.defaultdict(list)
        self.parallel_circuits: dict[int, list[Circuit]] = collections.defaultdict(list)

        if pre_order:
            self._pre_generate(pre_order)

    def _pre_generate(self, order: int) -> None:
        if order <= self.generated_order:
            return

        for n in range(self.generated_order + 1, order + 1):
            if n == 1:
                c = Circuit()
                self.series_circuits[1].append(c)
                self.parallel_circuits[1].append(c)
                continue
            for partition in partitions(n):
                if partition == [n]:
                    continue
                counts = collections.Counter(partition)
                iters = [
                    itertools.combinations_with_replacement(
                        self.parallel_circuits[i], c
                    )
                    for i, c in counts.items()
                ]
                for p_combination in itertools.product(*iters):
                    flattened = itertools.chain.from_iterable(p_combination)
                    s = Circuit(type=CircuitType.SERIES, items=list(flattened))
                    self.series_circuits[n].append(s)
                    self.parallel_circuits[n].append(s.conjugate())

        self.generated_order = order

    def iter_circuits(self, order: int) -> Generator[Circuit, None, None]:
        if order > self.generated_order:
            self._pre_generate(order)
        if order == 1:
            yield from self.series_circuits[1]
            return
        yield from self.series_circuits[order] + self.parallel_circuits[order]


if __name__ == "__main__":
    N = 4
    circuit_generator = CircuitGenerator(pre_order=N)
    for n in range(1, N + 1):
        print(f"{n=}")
        total = 0
        for circuit in circuit_generator.iter_circuits(order=n):
            print(" " * 4, circuit)
            total += 1
        print(f"{total=}\n")
