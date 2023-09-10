from __future__ import annotations

from typing import TYPE_CHECKING

import re

from tic_tac_toe.logic.exceptions import InvalidState


def validate_players(first: "Player", second: "Player") -> None:
    if first.symbol is second.symbol:
        raise ValueError("Players must use different symbols")


def validate_board(board: "Board") -> None:
    if not re.match(r"^[\sXO]{9}$", board.cells):
        raise ValueError("Must contain 9 cells of: X, O, or space")


def validate_game_state(game_state: "GameState") -> None:

    validate_number_of_symbols(game_state.board)
    validate_winner(game_state.board, game_state.winner)


def validate_number_of_symbols(board: "Board") -> None:
    if abs(board.x_count - board.o_count) > 1:
        raise InvalidState("Too many symbols!")


def validate_winner(board: "Board", winner) -> None:

    if winner == "X":
        if board.x_count <= board.o_count:
            raise InvalidState("Invalid state Xs")
    elif winner == "O":
        if board.o_count != board.x_count:
            raise InvalidState("Invalid state Os")



