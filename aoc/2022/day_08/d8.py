from aoc.cli import file_input


def up(i, j) -> int:
    return i,j-1

def down(i, j) -> int:
    return i,j+1

def left(i, j) -> int:
    return i-1,j

def right(i, j) -> int:
    return i+1, j


def get_score_and_visibility(i: int, j: int, trees: list[list[str]]) -> tuple[bool, int]:
    score = 1
    found_visibility = False

    for direction in [up, down, right, left]:
        i_idx, j_idx = i, j

        direction_score = 0

        while (0 < i_idx < len(trees)-1) and (0 < j_idx < len(trees[i_idx])-1):
            next_i, next_j = direction(i_idx, j_idx)
            direction_score += 1

            if trees[i][j] <= trees[next_i][next_j]:
                break

            i_idx, j_idx = next_i, next_j

        score *= direction_score
        if (
            i_idx in {0, len(trees)-1}
            or j_idx in {0, len(trees[i_idx])-1}
        ):
            found_visibility = True
    return found_visibility, score


def get_top_score_and_visibility_count(trees: list[list[str]]) -> tuple[int, int]:
    top_score = 0
    visible_count = len(trees)*2 + (len(trees[0])-2)*2

    for i in range(1, len(trees)-1):
        for j in range(1, len(trees[i])-1):
            visible, score = get_score_and_visibility(i, j, trees)
            if visible:
                visible_count += 1
            top_score = max(score, top_score)

    return visible_count, top_score


def main() -> None:
    trees = []
    with file_input() as file:
        while line := file.readline().strip():
            trees.append(list(map(int, list(line))))

    visible, top_score = get_top_score_and_visibility_count(trees)
    print(f"{visible=}")
    print(f"{top_score=}")


if __name__ == "__main__":
    main()
