import random

# Card representations
gem_emote = u"\U0001f48e"
idol_emote = u"\U0001f3c6"
# Fire, zombie, spider web, rock, snake
hazard_emotes = u"\U0001f525" + u"\U0001f9df" + u"\U0001f578" + u"\U0001faa8" + u"\U0001f40d"

# Deck setup: 15 gem cards, 5 idols, 3x5 hazards
deck = [str(i) + gem_emote for i in range(1, 16)]
deck.extend(3*list(hazard_emotes))

# Maps ordinal of idol obtained to its point value
idol_values = [5, 5, 5, 10, 10]


def shuffle(remaining_idols: int):
    shuffled_deck = deck.copy()  # "shuffled_deck = deck" just assigns a new alias "shuffled_deck" to the deck object
    shuffled_deck.extend(remaining_idols*[idol_emote])
    random.shuffle(shuffled_deck)
    return shuffled_deck


def check_hazards(current_deck: list):
    duplicates = [i for i in current_deck if current_deck.count(i) > 1]
    for j in duplicates:
        if j in hazard_emotes:
            return True
    return False


def check_idols(current_deck: list,
                remaining_idols: int):
    idol_count = current_deck.count(idol_emote)
    beginning_index = 5 - remaining_idols
    total_value = 0
    for i in range(beginning_index, beginning_index + idol_count):
        total_value += idol_values[beginning_index]

    if idol_count == 0:
        return False, idol_count, total_value
    else:
        return True, idol_count, total_value


def update_before_decisions(latest_card: str,
                            remaining_players: list,
                            current_shared: int,
                            current_unclaimed: int):
    try:
        num_gems = int("".join([i for i in latest_card if i in "0123456789"]))  # Extract the integer from gem cards
        num_players = len(remaining_players)
        new_unclaimed = current_unclaimed + num_gems % num_players  # Add leftovers from current card, sum may overflow
        new_shared = (current_shared
                      + num_gems // num_players        # Add from current card
                      + new_unclaimed // num_players)  # Get overflow from new_unclaimed (will be 0 if no overflow)
        new_unclaimed = new_unclaimed % num_players    # Adjust for overflow, now counted on the previous line
        return new_shared, new_unclaimed

    except ValueError:  # Non-gem cards
        return current_shared, current_unclaimed


def update_after_decisions(shared_gems: int,
                           unclaimed_gems: int,
                           returning_players: list):

    return (shared_gems + unclaimed_gems // len(returning_players),     # Payout to returning players
            unclaimed_gems - unclaimed_gems // len(returning_players))  # Remaining unclaimed gems

