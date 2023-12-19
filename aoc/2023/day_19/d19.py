from dataclasses import dataclass, replace
from collections import defaultdict
from operator import lt, gt
from aoc.cli import file_input
from aoc.geometry import split_at_point


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int


@dataclass(frozen=True, order=True)
class PartRange:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]


@dataclass(frozen=True)
class Comparison:
    category: str
    cmp: callable
    value: int
    result: str

    def __repr__(self) -> str:
        return f"{self.category}{'<' if self.cmp is lt else '>'}{self.value}:{self.result}"


@dataclass(frozen=True)
class Workflow:
    name: str
    comparisons: list[Comparison]
    result: str

    def __repr__(self) -> str:
        return f"{self.name}{{{','.join(map(str, self.comparisons))},{self.result}}}"


def p1(parts: list[Part], workflows: dict[str, Workflow]) -> None:
    accepted = []
    for part in parts:
        wf_name = "in"
        while wf_name not in {"A", "R"}:
            wf = workflows[wf_name]
            passed = False
            for cmp in wf.comparisons:
                val = getattr(part, cmp.category)
                if cmp.cmp(val, cmp.value):
                    wf_name = cmp.result
                    passed = True
                    break
            if not passed:
                wf_name = wf.result
        if wf_name == "A":
            accepted.append(part)

    result = 0
    for p in accepted:
        result += p.x + p.m + p.a + p.s
    print(f"Part 1: {result}")


def p2(workflows: dict[str, Workflow]) -> None:
    to_check = {"in": [PartRange((1, 4000), (1, 4000), (1, 4000), (1, 4000))]}
    accepted = []
    rejected = []
    while to_check:
        next_checks = defaultdict(list)
        for wf_name, ranges in to_check.items():
            print(f"{wf_name} -> {len(ranges)}")
            if not ranges:
                continue
            elif wf_name == "R":
                rejected.extend(ranges)
                continue
            elif wf_name == "A":
                accepted.extend(ranges)
                continue

            wf = workflows[wf_name]
            for part_range in ranges:
                for cmp in wf.comparisons:
                    cat_part_range = getattr(part_range, cmp.category)
                    new_part = None
                    print(f"SPLITTING: {part_range}")
                    if cmp.cmp is lt:
                        new_range = split_at_point(cat_part_range, cmp.value)
                        new_part = replace(part_range, **{cmp.category: new_range[0]})
                        part_range = replace(part_range, **{cmp.category: new_range[1]})
                    else:
                        new_range = split_at_point(cat_part_range, cmp.value+1)
                        new_part = replace(part_range, **{cmp.category: new_range[1]})
                        part_range = replace(part_range, **{cmp.category: new_range[0]})
                    print(f" - {new_part}")
                    print(f" - {part_range}")
                    next_checks[cmp.result].append(new_part)
                next_checks[wf.result].append(part_range)

        to_check = next_checks

    print()
    result = 0
    for part in sorted(accepted):
        print(part)
        combos = 1
        combos *= (part.x[1] - part.x[0] + 1)
        combos *= (part.m[1] - part.m[0] + 1)
        combos *= (part.a[1] - part.a[0] + 1)
        combos *= (part.s[1] - part.s[0] + 1)
        result += combos
    rejected_count = 0
    for part in sorted(rejected):
        print(part)
        combos = 1
        combos *= (part.x[1] - part.x[0] + 1)
        combos *= (part.m[1] - part.m[0] + 1)
        combos *= (part.a[1] - part.a[0] + 1)
        combos *= (part.s[1] - part.s[0] + 1)
        rejected_count += combos

    max_possible = 4000 * 4000 * 4000 * 4000
    print(f"Part 2: {result} + {rejected_count} == {max_possible} -> {result + rejected_count == max_possible}")


def main() -> None:
    workflows = {}
    parts = []
    parsing_workflows = True
    with file_input() as file:
        while line := file.readline():
            line = line.strip()
            if not line:
                parsing_workflows = False
                continue
            if parsing_workflows:
                line = line.split("{")
                name = line[0]
                raw_cmps = line[1].split(",")
                cmps = []
                result = None
                for cmp in raw_cmps:
                    if "<" in cmp:
                        cmp = cmp.split("<")
                        val, result = cmp[1].split(":")
                        cmps.append(Comparison(cmp[0], lt, int(val), result))
                    elif ">" in cmp:
                        cmp = cmp.split(">")
                        val, result = cmp[1].split(":")
                        cmps.append(Comparison(cmp[0], gt, int(val), result))
                    else:
                        result = cmp[:-1]
                workflows[name] = Workflow(name, cmps, result)
            else:
                line = line[1:-1].split(",")
                cats = []
                for c in line:
                    cats.append(int(c.split("=")[1]))
                parts.append(Part(cats[0], cats[1], cats[2], cats[3]))

    p1(parts, workflows)
    p2(workflows)


if __name__ == "__main__":
    main()
