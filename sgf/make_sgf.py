from enum import StrEnum


class Color(StrEnum):
    BLACK = "B"
    WHITE = "W"


def write_stones(file, stones):
    for x, y in stones:
        file.write(f'[{chr(x + ord("a"))}{chr(y + ord("a"))}]')


def make_sgf(file, black, white, to_play):
    file.write("(;FF[4]\n")
    file.write("GM[1]\n")
    file.write("AB")
    write_stones(file, black)
    file.write("\nAW")
    write_stones(file, white)
    file.write(f"\nPL[{to_play}]\n)\n")
