from aoc.cli import file_input


def up(i, j) -> int:
    return i,j-1

def down(i, j) -> int:
    return i,j+1

def left(i, j) -> int:
    return i-1,j

def right(i, j) -> int:
    return i+1, j


def get_score(i: int, j: int, trees: list[list[str]]) -> bool:
    score = 1
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

    return score


def get_best_score(trees: list[list[str]]) -> int:
    best_score = 0
    for i in range(1, len(trees)-1):
        for j in range(1, len(trees[i])-1):
            best_score = max(best_score, get_score(i, j, trees))

    return best_score


def check_visibility(i: int, j: int, trees: list[list[str]]) -> bool:
    for direction in [up, down, right, left]:
        i_idx, j_idx = i, j
        visible = True
        while (0 < i_idx < len(trees)-1) and (0 < j_idx < len(trees[i_idx])-1):
            next_i, next_j = direction(i_idx, j_idx)
            if trees[i][j] <= trees[next_i][next_j]:
                visible = False
                break
            i_idx, j_idx = next_i, next_j

        if visible:
            return True
    return False


def count_visible(trees: list[list[str]]) -> int:
    visible = len(trees)*2 + (len(trees[0])-2)*2
    for i in range(1, len(trees)-1):
        for j in range(1, len(trees[i])-1):
            if check_visibility(i, j, trees):
                visible += 1
    return visible


def main() -> None:
    trees = []
    with file_input() as file:
        while line := file.readline().strip():
            trees.append(list(map(int, list(line))))

    visible = count_visible(trees)
    print(f"{visible=}")

    best_score = get_best_score(trees)
    print(f"{best_score=}")



if __name__ == "__main__":
    main()