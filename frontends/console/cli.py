import re

from tic_tac_toe.game.engine import TicTacToe
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.models import GameState, Move, Symbol
from tic_tac_toe.game.players import Player, Minimax

from .renderers import ConsoleRenderer


class Console(Player):
    def get_move(self, game_state: GameState):
        while not game_state.game_over:
            try:
                prompt = "{}'s move: ".format(self.symbol)
                console_input = input(prompt).strip()
                index = board_to_index(console_input)
            except ValueError:
                print("Cell number format: <Letter><Number>")
            else:
                try:
                    return game_state.make_move_to(index)
                except InvalidMove:
                    print("Cell taken.")
        return None


def board_to_index(board: str) -> int:
    if re.match(r"[abcABC][123]", board):
        col, row = board
    else:
        raise ValueError("Invalid grid coordinates")
    return 3 * (int(row) - 1) + (ord(col.upper()) - ord("A"))


def main() -> None:
    first = Console(Symbol("X"))
    second = Minimax(Symbol("O"))
    TicTacToe(first, second, ConsoleRenderer()).play()
