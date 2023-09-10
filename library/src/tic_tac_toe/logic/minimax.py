from functools import partial

from tic_tac_toe.logic.models import GameState, Symbol, Move


def find_best_move(game_state: GameState):
    maximizer: Symbol = game_state.current_symbol
    bound_minimax = partial(minimax, maximizer=maximizer)
    return max(game_state.possible_moves, key=bound_minimax)


def minimax(move: Move, maximizer: Symbol, choose_highest_score: bool = False) -> int:

    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)

    results = []
    for next_move in move.after_state.possible_moves:
        score = minimax(next_move, maximizer, not choose_highest_score)
        results.append(score)

    if choose_highest_score:
        best_score = max(results)
    else:
        best_score = min(results)

    return best_score

