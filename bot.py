import os
import time
import game
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Emotes for UI
ticket_emote = u"\U0001f3ab"
checkmark_emote = u"\U00002705"

# Variables relevant to game logic
game_active = False
players = []            # List of all players
remaining_players = []  # List of players that have not returned to camp. Some module-level functions use this variable
decision_dict = {}      # Maps player name to explore/return decision
score_dict = {}         # Maps player name to total score


@bot.event
async def on_ready():
    print(bot.user.name, "has connected")


@bot.event
async def my_signal():
    pass


@bot.command(name="start")
async def start(ctx):
    global game_active
    if game_active:
        return
    game_active = True
    start_msg = await ctx.send(f"{ticket_emote} to join, {checkmark_emote} to confirm lobby.\n"
                               f"Current players: {players}")
    await start_msg.add_reaction(ticket_emote)
    await start_msg.add_reaction(checkmark_emote)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add")
            reaction = str(reaction)  # Convert from Reaction class

            if reaction == ticket_emote:
                if user.name not in players and user.name != "IncanBot":
                    players.append(user.name)
                await start_msg.edit(content=f"{ticket_emote} to join, {checkmark_emote} to confirm lobby.\n"
                                             f"Current players: {players}")

            elif reaction == checkmark_emote:
                await start_msg.delete()
                await ctx.send(f"**Lobby:** {players}")
                for player in players:
                    score_dict[player] = 0  # Initialize player scores to 0
                await set_up_interface(ctx)
                break

        except TimeoutError:
            ctx.send("Lobby setup took too long. Setup aborted.")


async def update_decisions(interaction):
    await interaction.response.edit_message(content=f"**Responses: **{decision_dict.keys()}")
    if set(decision_dict.keys()) == set(remaining_players):  # Have all players made a decision?
        bot.dispatch("my_signal")  # Signal to update game


async def explore_button_press(interaction):
    if interaction.user.name not in remaining_players:
        await interaction.response.defer()
        return
    decision_dict[interaction.user.name] = "Explore"
    await update_decisions(interaction)


async def return_button_press(interaction):
    if interaction.user.name not in remaining_players:
        await interaction.response.defer()
        return
    decision_dict[interaction.user.name] = "Return"
    await update_decisions(interaction)


async def set_up_interface(ctx):  # Set up interface
    view = discord.ui.View()

    explore_button = discord.ui.Button(label="Explore further",
                                       style=discord.ButtonStyle.blurple,
                                       custom_id="explore_button")
    explore_button.callback = explore_button_press
    return_button = discord.ui.Button(label="Return home",
                                      style=discord.ButtonStyle.green,
                                      custom_id="return_button")
    return_button.callback = return_button_press
    view.add_item(explore_button)
    view.add_item(return_button)

    players_state = await ctx.send("Initializing...")
    game_state = await ctx.send("Initializing...")
    gem_state = await ctx.send("Initializing...")
    expedition_index = 0  # How many expeditions have occurred
    idols_remaining = 5  # Number of idols left in the deck

    async def end_game():
        await ctx.send("Game over")
        quit()
        # Rematch option
        # Delete all messages, show score breakdown for each expedition?

    async def expedition():
        nonlocal expedition_index
        expedition_index += 1
        if expedition_index > 5:
            await end_game()
            return

        nonlocal idols_remaining
        deck = game.shuffle(idols_remaining)
        expedition_steps = 1
        shared, unclaimed = 0, 0
        global remaining_players
        remaining_players.extend(players)  # Set all players back to explore

        while len(remaining_players) > 0:
            latest_card = deck[expedition_steps - 1]
            if latest_card == u"\U0001f3c6":  # Idol drawn
                idols_remaining -= 1
            await players_state.edit(content=f"**Responses:** {decision_dict.keys()}", view=view)
            await game_state.edit(content=f"**Expedition {expedition_index} of 5:** {deck[:expedition_steps]}")

            if game.check_hazards(deck[:expedition_steps]):
                await gem_state.edit(content="Two hazards of the same type have been encountered.")
                remaining_players.clear()
                time.sleep(1)
                break

            else:
                shared, unclaimed = game.update_before_decisions(latest_card, remaining_players, shared, unclaimed)
                await gem_state.edit(content=f"Remaining explorers now have {shared} gems. "
                                             f"{unclaimed} gems go unclaimed.")

            # Above: card drawn, players make decisions
            await bot.wait_for("my_signal")
            # Below: decisions made, game updated

            returning_players = [key for key, value in decision_dict.items() if value == "Return"]
            if len(returning_players) > 0:
                payout, unclaimed = game.update_after_decisions(shared, unclaimed, returning_players)
                idols_present, num_idols, total_value = game.check_idols(deck[:expedition_steps], idols_remaining)
                if len(returning_players) == 1 and idols_present:
                    await gem_state.edit(content=f"{returning_players} escapes alone with {payout} gems and "
                                                 f"{num_idols} idols worth {total_value} points.")
                    score_dict[returning_players[0]] += total_value
                else:
                    await gem_state.edit(content=f"{returning_players} returns with {payout} gems each. "
                                                 f"{unclaimed} gems go unclaimed.")
                for i in returning_players:
                    score_dict[i] += payout
                    remaining_players.remove(i)

                time.sleep(2)  # Let players see the player returning results before continuing

            decision_dict.clear()
            expedition_steps += 1

        await gem_state.edit(content=f"Expedition {expedition_index} has ended. Current scores: {score_dict}")
        time.sleep(2)
        await expedition()

    await expedition()  # Initial function call to begin the game


bot.run(TOKEN)
