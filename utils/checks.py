import os
import discord
from discord.ext import commands

# Noms par défaut (tu peux les remplacer par des IDs via variables d'env)
ALLOWED_CATEGORY_NAME = os.getenv("ALLOWED_CATEGORY_NAME", "Transport")
ALLOWED_CHANNEL_NAME  = os.getenv("ALLOWED_CHANNEL_NAME",  "test-bot-transport")
COMMAND_PREFIX        = os.getenv("COMMAND_PREFIX", "!")

def in_allowed_channel(channel: discord.abc.GuildChannel) -> bool:
    try:
        category_name = channel.category.name if getattr(channel, "category", None) else None
        return (
            isinstance(channel, discord.TextChannel)
            and channel.name.lower() == ALLOWED_CHANNEL_NAME.lower()
            and category_name is not None
            and category_name.lower() == ALLOWED_CATEGORY_NAME.lower()
        )
    except Exception:
        return False

def only_transport_channel():
    async def predicate(ctx: commands.Context):
        if in_allowed_channel(ctx.channel):
            return True
        await ctx.send(
            f"🔒 Cette commande n'est autorisée que dans **#{ALLOWED_CHANNEL_NAME}** "
            f"de la catégorie **{ALLOWED_CATEGORY_NAME}**."
        )
        return False
    return commands.check(predicate)
