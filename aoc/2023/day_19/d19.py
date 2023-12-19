from aoc.cli import file_input
from dataclasses import dataclass
from operator import lt, gt


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int


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



if __name__ == "__main__":
    main()
