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

# Step 9 - uncertainty_spread
def uncertainty_spread(base_spread, uncertainty):
    """Return a spread width >= base_spread that grows with uncertainty."""
    # TODO: choose a spread width that is at least base_spread and increases with uncertainty.
    return base_spread + uncertainty

# Step 10 - inventory_skewed_quotes
def inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength):
    """
    Computes bid and ask quotes shifted to manage inventory risk.
    
    - Positive inventory (long) shifts quotes DOWN to encourage selling/discourage buying.
    - Negative inventory (short) shifts quotes UP to encourage buying/discourage selling.
    - Zero inventory or zero skew_strength results in perfectly symmetric quotes.
    """
    # Calculate the shift direction and magnitude
    # A positive inventory results in a negative shift (downward pressure)
    shift = -inventory * skew_strength
    
    # Calculate the skewed midpoint
    skewed_mid = fair_value + shift
    
    # Position the spread symmetrically around the skewed midpoint
    half_spread = spread_width / 2.0
    bid = skewed_mid - half_spread
    ask = skewed_mid + half_spread
    
    return {
        'bid': float(bid),
        'ask': float(ask)
    }

# Step 11 - update_fair_value_from_trade
def update_fair_value_from_trade(fair_value, side, bid, ask, adjustment):
    # TODO: Update the fair-value estimate after observing a counterparty trade on the given side.
    half_spread = (ask-bid)/2
    if side == "buy":
        return fair_value + adjustment*half_spread 
    elif side == "sell":
        return fair_value - adjustment*half_spread

# Step 12 - update_remaining_card_value
def update_remaining_card_value(remaining_counts, revealed_value):
    """
    Updates the face-down deck counts after a card reveal and recalculates
    the expected value of drawing from the remaining cards.
    """
    # Create a shallow copy to avoid mutating the original dictionary
    updated_counts = remaining_counts.copy()
    
    # Decrement the count of the revealed card if it exists in the deck
    if revealed_value in updated_counts:
        updated_counts[revealed_value] -= 1
        # Prune the key if the count drops to zero
        if updated_counts[revealed_value] <= 0:
            del updated_counts[revealed_value]
            
    # Calculate total remaining cards and total value sum
    total_cards = sum(updated_counts.values())
    
    if total_cards == 0:
        expected_val = 0.0
    else:
        # Recompute the mean value of a uniformly drawn card
        total_value = sum(card * count for card, count in updated_counts.items())
        expected_val = float(total_value / total_cards)
        
    return {
        'remaining_counts': updated_counts,
        'expected_value': expected_val
    }

# Step 13 - run_market_making_episode
def run_market_making_episode(true_value, counterparty_sides, initial_fair_value, config):
    # Initialize running state
    cash = 0.0
    inventory = 0
    fair_value = initial_fair_value
    history = []
    
    # Extract config values with defaults of 0
    base_spread = config.get('base_spread', 0.0)
    uncertainty = config.get('uncertainty', 0.0)
    skew_strength = config.get('skew_strength', 0.0)
    belief_adjustment = config.get('belief_adjustment', 0.0)
    
    # Loop over each counterparty action
    for side in counterparty_sides:
        # 1. Choose a spread width
        spread = uncertainty_spread(base_spread, uncertainty)
        
        # 2. Generate skewed bid/ask quotes
        quotes = inventory_skewed_quotes(fair_value, spread, inventory, skew_strength)
        bid = quotes['bid']
        ask = quotes['ask']
        
        # 3. Execute the counterparty trade
        current_state = {"cash": cash, "inventory": inventory}
        new_state = execute_trade(current_state, side, bid, ask)
        
        # Update our running cash and inventory tracking variables
        cash = new_state["cash"]
        inventory = new_state["inventory"]
        
        # 4. Update fair-value belief in the direction of the trade
        fair_value = update_fair_value_from_trade(fair_value, side, bid, ask, belief_adjustment)
        
        # Record the snapshot for this round
        history.append({
            'bid': bid,
            'ask': ask,
            'side': side,
            'cash': cash,
            'inventory': inventory,
            'fair_value': fair_value
        })
        
    # 5. At the end of the episode, mark to market
    pnl = mark_to_market_pnl(cash, inventory, true_value)
    
    # Return the final state and episode history
    return {
        'pnl': pnl,
        'cash': cash,
        'inventory': inventory,
        'fair_value': fair_value,
        'history': history
    }

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

