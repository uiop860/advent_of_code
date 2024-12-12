import os
from dataclasses import dataclass
from enum import Enum


class Tiles(Enum):
    WALL = "#"
    WALKED = "X"
    EMPTY = "."


@dataclass
class Point:
    x: int
    y: int


class Movement(Enum):
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)


guard_map: list[list[int]] = []
guard_map_size: Point
guard_pos: Point = None
guard_direction: Movement = Movement.UP
guard_first_loop_turn_pos: Point

with open(os.getcwd() + "/2024/day6/data.txt") as file:
    for idy, line in enumerate(file):
        for idx, letter in enumerate(line):
            if letter == "^":
                guard_pos = Point(idx, idy)
        guard_map.append([i.replace("^", ".") for i in line.strip()])
    del line
    del idx
    del idy
    del letter
    del file
    guard_map_size = Point(len(guard_map[0]) - 1, len(guard_map) - 1)


def get_next_pos(cur_pos: Point, direction: Movement):
    return Point(cur_pos.x + direction.value.x, cur_pos.y + direction.value.y)


turns = 0
possible_loops = 0
while True:
    next_pos = get_next_pos(guard_pos, guard_direction)
    # Stop traversing the map
    if next_pos.x > guard_map_size.x or next_pos.y > guard_map_size.y:
        break

    # Get the next tile
    next_tile = guard_map[next_pos.y][next_pos.x]

    if turns == 3:
        if (
            guard_direction in [Movement.RIGHT, Movement.LEFT]
            and guard_pos.x == guard_first_loop_turn_pos.x
        ) or (
            guard_direction in [Movement.UP, Movement.DOWN]
            and guard_pos.y == guard_first_loop_turn_pos.y
        ):
            possible_loops += 1
            turns = 0
        else:
            pass

    # Walk to next tile
    if next_tile in [Tiles.EMPTY.value, Tiles.WALKED.value]:
        guard_pos = next_pos
        guard_map[next_pos.y][next_pos.x] = Tiles.WALKED.value
    # Change direction right 90 degrees
    elif next_tile == Tiles.WALL.value:
        if turns == 0:
            guard_first_loop_turn_pos = guard_pos
        turns += 1
        if guard_direction == Movement.UP:
            guard_direction = Movement.RIGHT
        elif guard_direction == Movement.RIGHT:
            guard_direction = Movement.DOWN
        elif guard_direction == Movement.DOWN:
            guard_direction = Movement.LEFT
        elif guard_direction == Movement.LEFT:
            guard_direction = Movement.UP

    os.system("cls||clear")
    for y in guard_map:
        print("".join([str(i) for i in y]) + "\n")


print(possible_loops)
