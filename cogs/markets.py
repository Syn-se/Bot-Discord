import asyncio
import datetime
import aiohttp
import discord
from discord.ext import commands
from utils.checks import only_market_channel

# --- Configuration ---

# Choisis le cluster adapté: "west", "us", "asia"
API_HOST = "https://west.albion-online-data.com"

# Villes royales + Brecilien
ROYAL_CITIES = [
    "Caerleon",
    "Bridgewatch",
    "Martlock",
    "Lymhurst",
    "Fort Sterling",
    "Thetford",
    "Brecilien",
]

# Nom exact du Black Market côté API
BLACK_MARKET = "Black Market"

# Timeout HTTP (secondes)
HTTP_TIMEOUT = 15


def _normalize_item_id(maybe_base_or_full: str, tier: int | None) -> str:
    """
    Si l'utilisateur passe 'T5_BOW' -> on garde.
    Si l'utilisateur passe 'BOW' + tier=5 -> on construit 'T5_BOW'.
    """
    s = (maybe_base_or_full or "").strip().upper()
    if s.startswith("T") and "_" in s:
        return s  # déjà un ITEM_ID complet
    if not tier:
        # Pas de tier fourni et pas d'item complet -> on lève une ValueError
        raise ValueError("ITEM incomplet. Fournis soit un ITEM_ID complet (ex: T5_BOW), soit BASE_ID + TIER.")
    return f"T{int(tier)}_{s}"


def _fmt_silver(v: int | float | None) -> str:
    if not v or v <= 0:
        return "—"
    return f"{int(v):,} silver".replace(",", " ")


def _fmt_when(iso_str: str | None) -> str:
    if not iso_str:
        return "n/a"
    try:
        dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        delta = datetime.datetime.now(datetime.timezone.utc) - dt.astimezone(datetime.timezone.utc)
        mins = int(delta.total_seconds() // 60)
        if mins < 1:
            return "à l’instant"
        if mins < 60:
            return f"il y a {mins} min"
        hrs = mins // 60
        if hrs < 48:
            return f"il y a {hrs} h"
        days = hrs // 24
        return f"il y a {days} j"
    except Exception:
        return iso_str


class Markets(commands.Cog):
    """Commandes pour comparer Black Market vs HDV royaux/Brecilien."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="bestprice",
        help=(
            "Compare le meilleur prix entre le Black Market et les HDV (royales + Brecilien) pour un item.\n"
            "Syntaxe : !bestprice <ITEM_ID|BASE_ID> <TIER> <QUALITE>\n"
            "  • ITEM_ID complet (ex: T5_BOW) : !bestprice T5_BOW 5 1\n"
            "  • BASE_ID + TIER (ex: BOW 5 1) : !bestprice BOW 5 1\n"
            "Qualité : 1=Normal, 2=Bon, 3=Exceptionnel, 4=Remarquable, 5=Chef-d’œuvre"
        ),
        aliases=["bp", "best"]
    )
    @only_market_channel()
    async def bestprice(self, ctx: commands.Context, item_or_base: str, tier: int, qualite: int):
        """
        Règle:
        - Black Market: on regarde le meilleur prix d'achat (buy_price_max) -> c'est ce que le BM te paiera.
        - Villes: on regarde le meilleur prix de vente mini (sell_price_min) -> ce que tu peux espérer vendre rapidement.
        On renvoie le meilleur prix et l'emplacement gagnant.
        """
        # Validation simple
        if qualite < 1 or qualite > 5:
            await ctx.send("❌ Qualité invalide. Utilise un entier entre 1 et 5.")
            return

        try:
            item_id = _normalize_item_id(item_or_base, tier)
        except ValueError as e:
            await ctx.send(f"❌ {e}")
            return

        # Construire l'URL (on interroge toutes les villes + BM en un appel)
        locations = ",".join([BLACK_MARKET] + ROYAL_CITIES)
        url = f"{API_HOST}/api/v2/stats/prices/{item_id}.json?locations={locations}&qualities={qualite}"

        # Appel HTTP
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=HTTP_TIMEOUT) as resp:
                    if resp.status != 200:
                        await ctx.send(f"❌ API indisponible (HTTP {resp.status}).")
                        return
                    data = await resp.json()
        except asyncio.TimeoutError:
            await ctx.send("⏱️ Timeout en interrogeant l’API.")
            return
        except Exception as e:
            await ctx.send(f"❌ Erreur d’appel API: {e}")
            return

        if not data:
            await ctx.send("❌ Aucun prix trouvé pour cet item/qualité.")
            return

        # Agréger par ville
        bm_best = {"price": 0, "when": None}
        cities = {city: {"price": 0, "when": None} for city in ROYAL_CITIES}

        for row in data:
            city = row.get("city")
            if not city:
                continue

            if city == BLACK_MARKET:
                # on garde le meilleur buy_price_max
                price = row.get("buy_price_max") or 0
                when = row.get("buy_price_max_date")
                if price > bm_best["price"]:
                    bm_best = {"price": price, "when": when}
            else:
                # pour les villes: meilleur sell_price_min
                if city in cities:
                    price = row.get("sell_price_min") or 0
                    when = row.get("sell_price_min_date")
                    # on choisit le meilleur prix de vente mini
                    if price > (cities[city]["price"] or 0):
                        cities[city] = {"price": price, "when": when}

        # Trouver le meilleur global
        best_location = BLACK_MARKET
        best_price = bm_best["price"]
        best_when = bm_best["when"]

        for city, info in cities.items():
            if (info["price"] or 0) > (best_price or 0):
                best_location = city
                best_price = info["price"]
                best_when = info["when"]

        # Construire la réponse
        title = f"📊 Meilleur prix — {item_id} (Q{qualite})"
        embed = discord.Embed(title=title, color=discord.Color.blurple())
        embed.add_field(
            name="🏆 Meilleur emplacement",
            value=f"**{best_location}** — **{_fmt_silver(best_price)}**\n*{_fmt_when(best_when)}*",
            inline=False
        )

        # Black Market
        embed.add_field(
            name="🖤 Black Market (achat NPC)",
            value=f"{_fmt_silver(bm_best['price'])}\n*{_fmt_when(bm_best['when'])}*",
            inline=True
        )

        # Villes royales + Brecilien
        city_lines = []
        for city in ROYAL_CITIES:
            info = cities[city]
            city_lines.append(f"**{city}** — {_fmt_silver(info['price'])}  \n*{_fmt_when(info['when'])}*")
        embed.add_field(name="🏛️ Marchés (vente mini)", value="\n".join(city_lines), inline=True)

        embed.set_footer(text="Source: Albion Online Data Project • BM = buy_price_max, Villes = sell_price_min")

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Markets(bot))
