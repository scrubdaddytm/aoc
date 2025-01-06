from enum import Enum

from aoc.y_2019.intcode.instruction import Product, Sum


class Opcode(int, Enum):
    SUM = 1
    PRODUCT = 2
    TERMINATE = 99


OPCODE_TO_INSTRUCTION = {
    Opcode.SUM: Sum(),
    Opcode.PRODUCT: Product(),
}
