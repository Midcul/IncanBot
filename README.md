# IncanBot
A Python-based Discord bot to facilitate play of Incan Gold (a board game designed by Bruno Faidutti & Alan R. Moon)

# Using the bot
Change the discord token parameter to be your own, invite the bot to your server, and use !start. Currently, the bot turns itself off after the game is complete.

# How to play Incan Gold
__Deck of cards:__  
15 cards with a range of 1-15 gems(💎)  
15 hazard cards (3 copies each of 5 different types 🔥🕸️🧟🗿🐍)  
5 artifact cards (🏆)  

The game contains a series of five expeditions. At the beginning of each expedition, the deck is shuffled.

__The top card is revealed. Here are the possible outcomes:__  
💎: Gems are split among the explorers equally, with any remainder being left unclaimed.  
🏆: The artifact is left unclaimed until a sole explorer returns to camp. It is removed from the deck for future expeditions.  
🔥🕸️🧟🗿🐍: If it is the first occurrence of a specific hazard, nothing happens. If it is the second occurrence of a specific hazard, remaining explorers must abandon their wealth to flee.  

__After revealing the top card, explorers can choose either:__  
EXPLORE FURTHER: Remain in the expedition, sharing wealth from future gem cards.  
RETURN HOME: Leave the expedition, safely scoring their share of gems and the unclaimed gems that were not distributed to explorers prior. When multiple explorers return home, unclaimed gems are divided equally. If only one explorer returns home, they keep any revealed artifacts for themself.  

As long as at least one explorer chooses to go further, continuing drawing from the top of the deck one card at a time.  

An expedtion ends when all explorers have returned home, or two hazards of the same type are drawn.  

# Scoring
💎 = 1 point  
🏆 = 5 points each for the first three drawn, and 10 points each for the next two

Happy exploring!
