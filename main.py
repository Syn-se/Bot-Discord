import os
import logging
import discord
from http_stub import start_http_stub
from discord.ext import commands

# === Intents & Help par défaut (sans descriptions d’arguments) ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

default_help = commands.DefaultHelpCommand()
default_help.show_parameter_descriptions = False
default_help.verify_checks = False  # le help n'exécute pas les checks

bot = commands.Bot(command_prefix="!", intents=intents, help_command=default_help)

# === Logs propres ===
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("albion-bot")

# === Chargement des extensions (cogs) ===
@bot.event
async def setup_hook():
    for ext in ("cogs.transport", "cogs.markets"):
        try:
            await bot.load_extension(ext)
            log.info(f"✅ Loaded {ext}")
        except Exception as e:
            log.exception(f"❌ Failed to load {ext}: {e}")

@bot.event
async def on_ready():
    log.info(f"{bot.user} s'est connecté à Discord ! (id: {bot.user.id})")
    log.info(f"Guilds: {len(bot.guilds)}")

# === Filtrage global des commandes par salon/catégorie ===
from utils.checks import (
    in_transport_channel,
    in_market_channel,
    COMMAND_PREFIX,
    TRANSPORT_CHANNEL_NAME,
    TRANSPORT_CATEGORY_NAME,
    MARKET_CHANNEL_NAME,
    MARKET_CATEGORY_NAME,
)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    # Laisse toujours passer !help (sinon il peut être bloqué par le filtre)
    if message.content.startswith("!help"):
        await bot.process_commands(message)
        return

    if message.content.startswith(COMMAND_PREFIX):
        if not (in_transport_channel(message.channel) or in_market_channel(message.channel)):
            await message.channel.send(
                "🔒 Commandes autorisées uniquement dans "
                f"**{TRANSPORT_CATEGORY_NAME} > #{TRANSPORT_CHANNEL_NAME}** "
                "ou "
                f"**{MARKET_CATEGORY_NAME} > #{MARKET_CHANNEL_NAME}**."
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

    # Render gratuit : ouvre un port HTTP fictif pour éviter le timeout
    start_http_stub()

    bot.run(token)

if __name__ == "__main__":
    main()import os
import logging
import discord
from http_stub import start_http_stub
from discord.ext import commands

# === Intents & Help par défaut (sans descriptions d’arguments) ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

default_help = commands.DefaultHelpCommand()
default_help.show_parameter_descriptions = False
default_help.verify_checks = False  # le help n'exécute pas les checks

bot = commands.Bot(command_prefix="!", intents=intents, help_command=default_help)

# === Logs propres ===
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("albion-bot")

# === Chargement des extensions (cogs) ===
@bot.event
async def setup_hook():
    for ext in ("cogs.transport", "cogs.markets"):
        try:
            await bot.load_extension(ext)
            log.info(f"✅ Loaded {ext}")
        except Exception as e:
            log.exception(f"❌ Failed to load {ext}: {e}")

@bot.event
async def on_ready():
    log.info(f"{bot.user} s'est connecté à Discord ! (id: {bot.user.id})")
    log.info(f"Guilds: {len(bot.guilds)}")

# === Filtrage global des commandes par salon/catégorie ===
from utils.checks import (
    in_transport_channel,
    in_market_channel,
    COMMAND_PREFIX,
    TRANSPORT_CHANNEL_NAME,
    TRANSPORT_CATEGORY_NAME,
    MARKET_CHANNEL_NAME,
    MARKET_CATEGORY_NAME,
)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    # Laisse toujours passer !help (sinon il peut être bloqué par le filtre)
    if message.content.startswith("!help"):
        await bot.process_commands(message)
        return

    if message.content.startswith(COMMAND_PREFIX):
        if not (in_transport_channel(message.channel) or in_market_channel(message.channel)):
            await message.channel.send(
                "🔒 Commandes autorisées uniquement dans "
                f"**{TRANSPORT_CATEGORY_NAME} > #{TRANSPORT_CHANNEL_NAME}** "
                "ou "
                f"**{MARKET_CATEGORY_NAME} > #{MARKET_CHANNEL_NAME}**."
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

    # Render gratuit : ouvre un port HTTP fictif pour éviter le timeout
    start_http_stub()

    bot.run(token)

if __name__ == "__main__":
    main()
