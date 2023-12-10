import heapq
from typing import Any


class PriorityQueue:
    entry_finder: dict[Any, tuple[int, Any]]
    pq: list[tuple[int, Any]]

    def __init__(self, *, pq_removed_item: Any):
        self.entry_finder = {}
        self.pq = []
        self.pq_removed_item = pq_removed_item

    def add(self, item: Any, prio: int) -> None:
        if item in self.entry_finder:
            self.remove(item)
        entry = [prio, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, item: Any) -> None:
        entry = self.entry_finder.pop(item)
        entry[-1] = self.pq_removed_item

    def _pop(self) -> Any:
        prio, item = heapq.heappop(self.pq)
        return item

    def pop(self) -> Any:
        while self.pq:
            item = self._pop()
            if item is not self.pq_removed_item:
                del self.entry_finder[item]
                return item
        raise KeyError("pop from empty pq")

    def is_empty(self) -> bool:
        while self.pq and self.pq[0][-1] == self.pq_removed_item:
            self._pop()
        return not bool(self.pq)

    def __bool__(self) -> bool:
        return not self.is_empty()

    def items(self) -> list[Any]:
        stuff = []
        for item, entry in self.entry_finder.items():
            if entry[-1] != self.pq_removed_item:
                stuff.append(item)
        return stuff
