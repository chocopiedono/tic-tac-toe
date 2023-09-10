import enum
import random
import re
from dataclasses import dataclass
from functools import cached_property

from tic_tac_toe.logic.exceptions import InvalidMove, NoGameScore
from tic_tac_toe.logic.validators import validate_game_state, validate_board

PATT_REG = ("???......", "...???...", "......???", "?..?..?..", ".?..?..?.", "..?..?..?", "?...?...?", "..?.?.?..")


class Symbol(str, enum.Enum):
    CROSS = "X"
    NAUGHT = "O"

    @property
    def other(self) -> "Symbol":
        return Symbol.CROSS if self is Symbol.NAUGHT else Symbol.NAUGHT


@dataclass(frozen=True)
class Board:
    cells: str = " " * 9

    def __post_init__(self) -> None:
        validate_board(self)

    @cached_property
    def x_count(self) -> int:
        return self.cells.count("X")

    @cached_property
    def o_count(self) -> int:
        return self.cells.count("O")

    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(" ")


@dataclass(frozen=True)
class Move:
    symbol: Symbol
    cell_index: int
    before_state: "GameState"
    after_state: "GameState"


@dataclass(frozen=True)
class GameState:
    board: Board
    starting_symbol: Symbol = Symbol("X")

    def __post_init__(self) -> None:
        validate_game_state(self)

    @cached_property
    def current_symbol(self) -> Symbol:
        if self.board.x_count == self.board.o_count:
            return self.starting_symbol
        else:
            return self.starting_symbol.other

    @cached_property
    def game_not_started(self) -> bool:
        return self.board.empty_count == 9

    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie

    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.board.empty_count == 0

    @cached_property
    def winner(self):
        for pattern in PATT_REG:
            for symbol in Symbol:
                if re.match(pattern.replace("?", symbol), self.board.cells):
                    return symbol
        return None

    @cached_property
    def winning_cells(self) -> list[int]:
        for pattern in PATT_REG:
            for symbol in Symbol:
                if re.match(pattern.replace("?", symbol), self.board.cells):
                    return [
                        match.start() for match in re.finditer(r"\?", pattern)
                    ]
        return []

    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for match in re.finditer(r"\s", self.board.cells):
                moves.append(self.make_move_to(match.start()))
        return moves

    def evaluate_score(self, symbol: Symbol) -> int:
        if self.game_over:
            if self.tie:
                return 0
            if self.winner is symbol:
                return 1
            else:
                return -1
        raise NoGameScore("Game is not over yet")

    def make_move_to(self, index: int) -> Move:
        if self.board.cells[index] != " ":
            raise InvalidMove("Cell is not empty")

        first_part_board = self.board.cells[:index]
        last_part_board = self.board.cells[index + 1:]
        new_board = Board(first_part_board + self.current_symbol + last_part_board)
        game_state = GameState(new_board, self.starting_symbol)
        move = Move(self.current_symbol, index, self, game_state)
        return move


