import discord
from discord.ext import commands
from utils.checks import only_transport_channel
from utils.formatting import format_silver

class Transport(commands.Cog):
    """Commandes liées au transport Albion (CAERLEON, etc.)."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="transport_caer",
        aliases=["transport_CAER"],
        help=("Calcule le coût d'un transport CAERLEON selon la catégorie, le poids (KG) et l'estimation marchande (EVM).\n"
              "Syntaxe : !transport_caer <CATEGORIE> <KG> <EVM>\n"
              "Catégories : STANDARD | CLIENT | VIP\n"
              "Exemples :\n"
              "  !transport_caer STANDARD 12000 5000000\n"
              "  !transport_caer vip 8500 3200000")
    )
    @only_transport_channel()
    async def transport_caer(self, ctx: commands.Context, categorie: str, kg: float, evm: float):
        """
        Règle : on affiche uniquement le maximum entre ESTIMATION_MARCHANDE et PRIX_KG.
        """
        # ⚠️ Paramètres : adapte-les à tes règles
        # NOTE : dans un précédent message tu avais 0.1 / 0.8 / 0.6 et 325k / 350k / 275k.
        # Ici je remets ces valeurs "classiques". Modifie si besoin.
        params = {
            "STANDARD": {"evm_pct": 0.1, "kg_rate": 325_000},
            "CLIENT":   {"evm_pct": 0.8, "kg_rate": 350_000},
            "VIP":      {"evm_pct": 0.6, "kg_rate": 275_000},
        }

        cat = categorie.strip().upper()
        if cat not in params:
            await ctx.send("❌ Catégorie invalide. Utilisez : `STANDARD`, `CLIENT` ou `VIP`.")
            return
        if kg <= 0 or evm <= 0:
            await ctx.send("❌ KG et EVM doivent être des valeurs strictement positives.")
            return

        evm_pct = params[cat]["evm_pct"]
        kg_rate = params[cat]["kg_rate"]

        estimation_marchande = evm_pct * evm
        prix_kg = kg_rate * (kg / 1000.0)
        cout_final = max(estimation_marchande, prix_kg)

        embed = discord.Embed(
            title="💰 Calcul de transport - CAERLEON",
            description=f"Catégorie **{cat}**",
            color=discord.Color.gold()
        )
        embed.add_field(name="Poids", value=f"{kg:,.2f} KG".replace(",", " "), inline=True)
        embed.add_field(name="EVM (estimation marchande)", value=format_silver(evm), inline=True)
        embed.add_field(name="—", value="—", inline=True)

        embed.add_field(name="Estimation marchande appliquée", value=format_silver(estimation_marchande), inline=True)
        embed.add_field(name="Prix au KG", value=format_silver(prix_kg), inline=True)
        embed.add_field(name="Règle", value="On retient **le maximum** entre les deux.", inline=True)
        embed.add_field(name="💸 Coût final", value=f"**{format_silver(cout_final)}**", inline=False)

        await ctx.send(embed=embed)

    @transport_caer.error
    async def transport_caer_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument)):
            await ctx.send("❌ Mauvaise syntaxe. Exemple : `!transport_caer STANDARD 12000 5000000`")
        else:
            raise error

async def setup(bot: commands.Bot):
    await bot.add_cog(Transport(bot))
