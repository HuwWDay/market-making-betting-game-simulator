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

# Step 4 - red_black_card_game_value
from functools import lru_cache

def red_black_card_game_value(num_red, num_black):
    @lru_cache(maxsize=None)
    def V(r, b):
        # Base cases
        if r == 0:
            return 0.0
        if b == 0:
            return float(r)
        
        # Total remaining cards
        total = r + b
        
        # Expected value if we choose to draw another card:
        # P(Red) * (1 + V(r-1, b)) + P(Black) * (-1 + V(r, b-1))
        ev_draw = (r / total) * (1 + V(r - 1, b)) + (b / total) * (-1 + V(r, b - 1))
        
        # The player can always stop now and take 0 (or continue if ev_draw > 0)
        return max(0.0, ev_draw)

    # Calculate the expected payout for the initial state
    # We evaluate the drawing value first to see if we should stop immediately
    if num_red == 0:
        ev_draw = 0.0
    elif num_black == 0:
        ev_draw = float(num_red)
    else:
        total = num_red + num_black
        ev_draw = (num_red / total) * (1 + V(num_red - 1, num_black)) + (num_black / total) * (-1 + V(num_red, num_black - 1))
    
    # Per the problem description: If ev_draw <= 0, we choose to stop immediately.
    stop_now = ev_draw <= 0
    initial_value = max(0.0, ev_draw)
    
    return {'value': initial_value, 'stop_now': stop_now}

# Step 5 - make_quotes
def make_quotes(fair_value, spread_width):
    # TODO: return a dict with 'bid' and 'ask' symmetric around fair_value with total width spread_width
    half = spread_width/2 
    return {"bid": fair_value-half, "ask":fair_value+half}

# Step 6 - execute_trade
def execute_trade(state, side, bid, ask, size=1):
    # TODO: apply a counterparty trade against your bid/ask and return updated state
    cash, inv = state["cash"], state["inventory"]
    if side == "buy":
        cash += size*ask
        inv -= size
    elif side == "sell":
        cash -= size*bid 
        inv += size 
    new_state = state.copy()
    new_state["cash"], new_state["inventory"] = cash, inv 
    return new_state

# Step 7 - mark_to_market_pnl
def mark_to_market_pnl(cash, inventory, settlement_value):
    # TODO: return total P&L given cash, remaining inventory, and settlement value.
    return cash + inventory*settlement_value

# Step 8 - adverse_selection_loss
import numpy as np

def adverse_selection_loss(fair_value, bid, ask, informed_values, informed_probabilities):
    """
    Quantifies the expected loss to an informed counterparty based on the provided quotes 
    and the probability distribution of the asset's true value.
    """
    informed_values = np.asarray(informed_values, dtype=float)
    informed_probabilities = np.asarray(informed_probabilities, dtype=float)
    
    # Loss when true value is above the ask price (counterparty buys from you)
    ask_loss = np.maximum(0, informed_values - ask)
    
    # Loss when true value is below the bid price (counterparty sells to you)
    bid_loss = np.maximum(0, bid - informed_values)
    
    # Total loss per state
    total_loss_per_state = ask_loss + bid_loss
    
    # Expected loss is the probability-weighted sum of losses across all states
    expected_loss = np.sum(total_loss_per_state * informed_probabilities)
    
    return float(expected_loss)

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

