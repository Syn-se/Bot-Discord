import os
import asyncio
import logging
import discord
from discord.ext import commands

# === Intents & Help par défaut (sans descriptions d’arguments) ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

default_help = commands.DefaultHelpCommand()
default_help.show_parameter_descriptions = False

bot = commands.Bot(command_prefix="!", intents=intents, help_command=default_help)

# === Logs propres ===
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("albion-bot")

# === Chargement des extensions (cogs) ===
@bot.event
async def setup_hook():
    # Charge les cogs au démarrage
    await bot.load_extension("cogs.transport")

@bot.event
async def on_ready():
    log.info(f"{bot.user} s'est connecté à Discord ! (id: {bot.user.id})")
    log.info(f"Guilds: {len(bot.guilds)}")

# === Filtrage global des commandes par salon/catégorie ===
# (Si tu as aussi un décorateur par commande, tu peux garder les deux.)
from utils.checks import in_allowed_channel, COMMAND_PREFIX

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if message.content.startswith(COMMAND_PREFIX) and not in_allowed_channel(message.channel):
        await message.channel.send(
            "🔒 Les commandes de transport sont réservées au salon autorisé de la catégorie Transport."
        )
        return
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Commande inconnue. Utilisez `!help` pour voir les commandes disponibles.")
    elif isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument)):
        await ctx.send("❌ Arguments invalides. Exemple : `!transport_caer STANDARD 12000 5000000`")
    else:
        log.exception("Erreur de commande", exc_info=error)
        await ctx.send("❌ Une erreur s'est produite.")

def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN manquant dans les variables d'environnement.")
        raise SystemExit(1)

    bot.run(token)

if __name__ == "__main__":
    main()
