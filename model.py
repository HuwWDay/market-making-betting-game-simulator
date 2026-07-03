"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
def expected_value(values, probabilities):
    # TODO: return the expected value of the discrete distribution (values, probabilities).
    return np.sum(np.array(values)*np.array(probabilities))

# Step 2 - one_reroll_die_value
def one_reroll_die_value(sides):
    # TODO: return {'value': expected winnings under optimal reroll policy, 'reroll_faces': sorted faces to reroll}
    values = [i for i in range(1, sides+1)]
    probs = [1/sides for i in range(sides)]
    mu = expected_value(values, probs)
    maxval = [max(mu, val) for val in values]
    opt = expected_value(maxval, probs)
    reroll = [val for val in values if val < mu]
    return {"value": opt, "reroll_faces":reroll}

# Step 3 - pay_per_reroll_die_game
def pay_per_reroll_die_game(sides, reroll_cost):
    V = []
    for t in range(1, sides + 1):
        # Calculate expected value for threshold t
        ev = (t + sides) / 2 - reroll_cost * (t - 1) / (sides - t + 1)
        V.append(ev)
    
    max_value = max(V)
    # .index() returns the 0-based index, add 1 to get the actual threshold value
    optimal_threshold = V.index(max_value) + 1 
    
    return {'threshold': optimal_threshold, 'value': max_value}

# Step 4 - red_black_card_game_value (not yet solved)
# TODO: implement

# Step 5 - make_quotes (not yet solved)
# TODO: implement

# Step 6 - execute_trade (not yet solved)
# TODO: implement

# Step 7 - mark_to_market_pnl (not yet solved)
# TODO: implement

# Step 8 - adverse_selection_loss (not yet solved)
# TODO: implement

# Step 9 - uncertainty_spread (not yet solved)
# TODO: implement

# Step 10 - inventory_skewed_quotes (not yet solved)
# TODO: implement

# Step 11 - update_fair_value_from_trade (not yet solved)
# TODO: implement

# Step 12 - update_remaining_card_value (not yet solved)
# TODO: implement

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

