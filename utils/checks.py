import os
import discord
from discord.ext import commands

# ========= Config par NOMS (fallback) =========
TRANSPORT_CATEGORY_NAME = os.getenv("TRANSPORT_CATEGORY_NAME", "Transport")
TRANSPORT_CHANNEL_NAME  = os.getenv("TRANSPORT_CHANNEL_NAME",  "test-bot-transport")

MARKET_CATEGORY_NAME    = os.getenv("MARKET_CATEGORY_NAME",  "Economie")
MARKET_CHANNEL_NAME     = os.getenv("MARKET_CHANNEL_NAME",   "bot-commerce")

# ========= Config par IDs (PRIORITAIRES si présents) =========
# (Active le mode développeur Discord, clic droit > Copier l’identifiant)
TRANSPORT_CATEGORY_ID = os.getenv("TRANSPORT_CATEGORY_ID")  # ex: "123456789012345678"
TRANSPORT_CHANNEL_ID  = os.getenv("TRANSPORT_CHANNEL_ID")   # ex: "234567890123456789"
MARKET_CATEGORY_ID    = os.getenv("MARKET_CATEGORY_ID")     # ex: "345678901234567890"
MARKET_CHANNEL_ID     = os.getenv("MARKET_CHANNEL_ID")      # ex: "456789012345678901"

COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# ---------- Helpers ----------
def _match_ids(channel: discord.abc.GuildChannel, chan_id: str | None, cat_id: str | None) -> bool:
    """Vrai si les IDs (salon + catégorie) correspondent exactement."""
    if not (chan_id and cat_id):
        return False
    try:
        return (
            isinstance(channel, discord.TextChannel)
            and str(getattr(channel, "id", "")) == str(chan_id)
            and str(getattr(channel.category, "id", "")) == str(cat_id)
        )
    except Exception:
        return False

def _match_names(channel: discord.abc.GuildChannel, chan_name: str, cat_name: str) -> bool:
    """Vrai si les noms (insensibles à la casse/espaces) correspondent."""
    try:
        category = getattr(channel, "category", None)
        category_name = category.name if category else None
        return (
            isinstance(channel, discord.TextChannel)
            and channel.name.strip().lower() == chan_name.strip().lower()
            and category_name is not None
            and category_name.strip().lower() == cat_name.strip().lower()
        )
    except Exception:
        return False

# ---------- Transport ----------
def in_transport_channel(channel: discord.abc.GuildChannel) -> bool:
    # Priorité aux IDs si fournis
    if _match_ids(channel, TRANSPORT_CHANNEL_ID, TRANSPORT_CATEGORY_ID):
        return True
    # Sinon fallback aux noms
    return _match_names(channel, TRANSPORT_CHANNEL_NAME, TRANSPORT_CATEGORY_NAME)

def only_transport_channel():
    """Check silencieux: n’autorise que dans la zone Transport; ne parle pas tout seul."""
    async def predicate(ctx: commands.Context):
        return in_transport_channel(ctx.channel)  # <-- plus de ctx.send ici
    return commands.check(predicate)

# ---------- Marché / Économie ----------
def in_market_channel(channel: discord.abc.GuildChannel) -> bool:
    if _match_ids(channel, MARKET_CHANNEL_ID, MARKET_CATEGORY_ID):
        return True
    return _match_names(channel, MARKET_CHANNEL_NAME, MARKET_CATEGORY_NAME)

def only_market_channel():
    """Check silencieux: n’autorise que dans la zone Économie; ne parle pas tout seul."""
    async def predicate(ctx: commands.Context):
        return in_market_channel(ctx.channel)  # <-- plus de ctx.send ici
    return commands.check(predicate)
