import abc
import time

from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.minimax import find_best_move
from tic_tac_toe.logic.models import GameState, Symbol, Move


class Player(metaclass=abc.ABCMeta):
    def __init__(self, symbol: Symbol) -> None:
        self.symbol = symbol

    def make_move(self, game_state: GameState) -> GameState:
        if self.symbol is game_state.current_symbol:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("No more moves")
        else:
            raise InvalidMove("Other player's turn")

    @abc.abstractmethod
    def get_move(self, game_state: GameState):
        """Return the current player's move in the given game state."""


class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def get_move(self, game_state: GameState):
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState):
        """Return the computer's move in the given game state."""


class Minimax(ComputerPlayer):
    def get_computer_move(self, game_state: GameState):
        return find_best_move(game_state)
