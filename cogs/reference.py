import discord
from discord.ext import commands
from utils.checks import only_market_channel

# ===========================================================
# Données de référence (tokens = base pour ITEM_ID ex: T5_<TOKEN>@2)
# ===========================================================

# Familles d'armes (EN -> FR)
WEAPON_FAMILIES = {
    "bows":              "Arcs",
    "swords":            "Épées",
    "axes":              "Haches",
    "maces":             "Masses",
    "spears":            "Lances",
    "crossbows":         "Arbalètes",
    "daggers":           "Dagues",
    "hammers":           "Marteaux",
    "quarterstaff":      "Long bâton",
    "fire_staffs":       "Pyromancien",
    "frost_staffs":      "Mage de givre",
    "cursed_staffs":     "Sorcier",
    "holy_staffs":       "Prêtre",
    "arcane_staffs":     "Arcaniste",
    "nature_staffs":     "Bâton naturel",
}

# Mains droites (off-hands)
OFFHAND_FAMILIES = {
    "offhands": "Mains droites (combattant torche, combattant tome, combattant bouclier)",
}

# --- Détails par famille : (TOKEN EN, "Nom FR") ---

BOWS = [
    ("BOW",           "Arc"),
    ("WARBOW",        "Arc de guerre"),
    ("LONGBOW",       "Arc long"),
    ("WHISPERINGBOW", "Arc murmurant"),
    ("WAILINGBOW",    "Arc gémissant"),
    ("BOWOFBADON",    "Arc de Badon"),
    ("MISTPIERCER",   "Perce-brume"),
    ("SKYSTRIDER",    "Arc marche-ciel"),
]

SWORDS = [
    ("BROADSWORD",    "Épée large"),
    ("CLAYMORE",      "Claymore"),
    ("DUALSWORD",     "Doubles épées"),
    ("CLARENTBLADE",  "Lame de Clarent"),
    ("CARVING",       "Épée tranchante"),
    ("KINGMAKER",     "Adoube-Roi"),
    ("GALATINEPAIR",  "Paires de galatines"),
    ("INFINITYBLADE", "Lame infinie"),
]

AXES = [
    ("AXE",             "Hache de guerre"),
    ("GREATAXE",        "Grande hache"),
    ("HALBERD",         "Hallebarde"),
    ("CARRIONCALLER",   "Mande-charogne"),
    ("INFERNALSCYTHE",  "Faux infernale"),
    ("REALMBREAKER",    "Brise-royaume"),
    ("CRYSTALREAPER",   "Faucheuse de cristal"),
    ("BEARPAWS",        "Patte d'ours"),
]

MACES = [
    ("MACE",              "Masse"),
    ("MORNINGSTAR",       "Morgenstern"),
    ("INCUBUSMACE",       "Masse d'incube"),
    ("CAMLANMACE",        "Masse de Camlann"),
    ("OATHKEEPERS",       "Gardes-serment"),
    ("DREADSTORMMONARCH", "Gardiens du serment"),
    ("HEAVYMACE",         "Masse lourde"),
    ("BEDROCKMACE",       "Masse du soubacement"),
]

SPEARS = [
    ("SPEAR",          "Lance"),
    ("PIKE",           "Pique"),
    ("GLAIVE",         "Glaive"),
    ("SPIRITHUNTER",   "Chassesprit"),
    ("TRINITYSPEAR",   "Lance de la Trinité"),
    ("DAYBREAKER",     "Diurnebris"),
    ("RIFTGLAIVE",     "Glaive déchirant"),
    ("HERONSPEAR",     "Lance de héron"),
]

CROSSBOWS = [
    ("CROSSBOW",         "Arbalète"),
    ("LIGHTCROSSBOW",    "Arbalète légère"),
    ("HEAVYCROSSBOW",    "Arbalète lourde"),
    ("WEEPINGREPEATER",  "Arbalète à répétition des larmes"),
    ("BOLTCASTERS",      "Lanceurs de foudre"),
    ("SIEGEBOW",         "Arc de siège"),
    ("ENERGYSHAPER",     "Matrice d'énergie"),
    ("ARCLIGHTBLASTERS", "Désintégrateurs de Lumière"),
]

DAGGERS = [
    ("DAGGER",        "Dague"),
    ("DAGGERPAIR",    "Paire de dagues"),
    ("CLAWS",         "Griffes"),
    ("DEATHGIVERS",   "Sacrificateurs"),
    ("BLOODLETTER",   "Saigneur"),
    ("DEMONFANG",     "Croc-de-démon"),
    ("BRIDLEDFURY",   "Brides-furie"),
    ("TWINSLAYERS",   "Jumelles tueuses"),
]

HAMMERS = [
    ("HAMMER",          "Marteau"),
    ("POLEHAMMER",      "Bec de corbin"),
    ("GREATHAMMER",     "Grand marteau"),
    ("TOMBHAMMER",      "Martel-tombe"),
    ("GROVEKEEPER",     "Gardien du bosquet"),
    ("HANDOFJUSTICE",   "Main de justice"),
    ("FORGEHAMMERS",    "Marteaux forgés"),
    ("TRUEBOLTHAMMER",  "Marteau de foudre"),
]

QUARTERSTAVES = [
    ("QUARTERSTAFF",          "Long bâton"),
    ("IRONCLADSTAFF",         "Bâton sans faille"),
    ("DOUBLEBLADEDSTAFF",     "Bâton à double tranchant"),
    ("BLACKMONKSTAFF",        "Bâton de moine noir"),
    ("SOULSCYTHE",            "Fauchâme"),
    ("STAFFOFBALANCE",        "Bâton d’équilibre"),
    ("GRAILSEEKER",           "Cherchegraal"),
    ("PHANTOMTWINBLADE",      "Lame double fantôme"),
]

FIRE_STAFFS = [
    ("FIRESTAFF",         "Bâton de feu"),
    ("GREATFIRESTAFF",    "Grand bâton de feu"),
    ("WILDFIRESTAFF",     "Bâton braisier"),
    ("BRIMSTONESTAFF",    "Bâton sulfureux"),
    ("BLAZINGSTAFF",      "Bâton ardent"),
    ("FLAMEWALKER STAFF", "Bâton de Marcheflammes"),
    ("INFERNALSTAFF",     "Bâton infernal"),
    ("DAWNSONG",        "Chant de l’aube"),
]

FROST_STAFFS = [
    ("FROSTSTAFF",        "Bâton de givre"),
    ("GREATFROSTSTAFF",   "Grand bâton de givre"),
    ("HOARFROSTSTAFF",    "Bâton de gelée blanche"),
    ("GLACIALSTAFF",      "Bâton glacial"),
    ("ICICLESTAFF",       "Bâton de stalactite"),
    ("PERMAFROSTPRISM",   "Prisme de pergélisol"),
    ("CHILLHOWL",         "Hurlegivre"),
    ("ARCTICSTAFF",       "Bâton arctique"),
]

CURSED_STAFFS = [
    ("CURSEDSTAFF",       "Bâton damné"),
    ("GREATCURSEDSTAFF",  "Grand bâton damné"),
    ("LIFECURSESTAFF",    "Bâton de malédiction de vie"),
    ("DEMONICSTAFF",      "Bâton démoniaque"),
    ("DAMNATIONSTAFF",    "Bâton de la damnation"),
    ("SHADOWCALLER",      "Mande-ténèbres"),
    ("CURSEDSKULL",       "Crâne damné"),
    ("ROTCALLER",         "Bâton de putréfaction"),
]

HOLY_STAFFS = [
    ("HOLYSTAFF",        "Bâton béni"),
    ("GREATHOLYSTAFF",   "Grand bâton béni"),
    ("DIVINESTAFF",      "Bâton divin"),
    ("FALLENSTAFF",      "Bâton déchu"),
    ("LIFETOUCHSTAFF",   "Bâton du toucher de vie"),
    ("RDEMPTIONSTAFF",   "Bâton de rédemption"),
    ("HALLOWFALL",       "Sanctificateur"),
    ("EXALTEDSTAFF",     "Bâton exalté"),
]

ARCANE_STAFFS = [
    ("ARCANESTAFF",       "Bâton esotérique"),
    ("GREATARCANESTAFF",  "Grand bâton esotérique"),
    ("ENIGMATICSTAFF",    "Bâton énigmatique"),
    ("OCCULTSTAFF",       "Bâton occulte"),
    ("WITCHWORKSTAFF",    "Bâton de sorcellerie"),
    ("MALEVOLENTLOCUS",   "Locus malveillant"),
    ("EVENSONG",          "Cercle vesperien"),
    ("ASTRALSTAFF",       "Bâton astral"),
]

NATURE_STAFFS = [
    ("NATURESTAFF",       "Bâton naturel"),
    ("GREATNATURESTAFF",  "Grand bâton naturel"),
    ("DRUIDICSTAFF",      "Bâton druidique"),
    ("BLIGHTSTAFF",       "Bâton de fléau"),
    ("WILDSTAFF",         "Bâton sauvage"),
    ("RAMPANTSTAFF",      "Bâton souchefer"),
    ("RAMPANTSTAFF",      "Bâton effréné"),
    ("FORGEBARKSTAFF",    "Bâton de forgécorce"),
]

SHAPESHIFTER_STAFF = [
    ("PROWLINGSTAFF",       "Bâton rôdeur"),
    ("ROOTBOUNDSTAFF",      "Bâton enraciné"),
    ("PRIMALSTAFF",         "Bâton primitif"),
    ("DLOODMOONSTAFF",      "Bâton de lune de sang"),
    ("HELLSPAWNSTAFF",      "Bâton de créature infernale"),
    ("EARTHRUNESTAFF",      "Bâton de terre-rune"),
    ("LIGHTCALLER",         "Mande-lumière"),
    ("STILLGAZESTAFF",      "Bâton de regard figé"),
]

WAR_GLOVES = [
    ("BRAWLERGLOVES",       "Gantelets de bagarreur"),
    ("BATTLEBRACERS",       "Gantelets de bataille"),
    ("SPIKEDGAUNTLETS",     "Gantelets à pointe"),
    ("URSINEMAULERS",       "Poignes ursines"),
    ("HELLFIRE",            "Mains infernales"),
    ("RAVENSTRIKECESTUS",   "Cestes-des-freux"),
    ("FISTSOFAVALON",       "Poings d'Avalon"),
    ("FORCEPULES BRACERS",  "Brassards d'Impulsion de force"),
]

# Mains droites (off-hands)
OFFHANDS_TORCH = [
    ("TORCH",           "Torche"),
    ("MISTCALLER",      "Mandebrume"),
    ("LEERINGCANE",     "Canne grimaçante"),
    ("CRYPTCANDLE",     "Bougie de la crypte"),
    ("SACREDSCEPTER",   "Sceptre sacré"),
    ("BLUEFLAMETORCH",  "Toche Flammebleue céleste"),
]

OFFHANDS_MAGE = [
    ("TOMEOFSPELLS",        "Tome de sorts"),
    ("EYEOFSECRETS",        "Œil des secrets"),
    ("MUISAK",              "Miniaturisé"),
    ("TAPROOT",             "Racine pivot"),
    ("CELESTIALCENSER",     "Encens céleste"),
    ("TIMELOCKEDGRIMOIRE",  "Grimoire Chronostatique"),

]

OFFHANDS_SHIELD = [
    ("SHIELD",          "Bouclier"),
    ("SARCOPHAGUS",     "Sarcophage"),
    ("CAITIFFSHIELD",   "Bouclier de scélérat"),
    ("FACEBREAKER",     "Brise-face"),
    ("ASTRALAEGIS",     "Egide astrale"),
    ("UNBREAKABLEWARD", "Barrière incassable"),
]

# Ressources (gros niveaux)
RESOURCES_OVERVIEW = [
    ("WOOD",   "Bois"),
    ("ORE",    "Minerai"),
    ("FIBER",  "Fibre"),
    ("HIDE",   "Cuir brut"),
    ("STONE",  "Pierre"),
]

# Détails simples par ressource (base token -> FR)
WOOD = [("WOOD", "Bois"), ("PLANKS",          "Planches")]
ORE  = [("ORE",  "Minerai"), ("METALBAR",     "Lingots")]
FIBER= [("FIBER", "Fibre"), ("CLOTH",         "Tissu")]
HIDE = [("HIDE",  "Peaux"), ("LEATHER",       "Cuir")]
STONE= [("STONE", "Pierre"), ("STONEBLOCK",   "Bloc de pierre")]

QUALITY_MAP = [
    (1, "Normal"),
    (2, "Bon"),
    (3, "Exceptionnel"),
    (4, "Remarquable"),
    (5, "Chef-d’œuvre (Formidable)"),
]

# ===========================================================
# Helpers
# ===========================================================

def _embed_pairs(title: str, pairs: list[tuple[str, str, str]], color=discord.Color.blurple()) -> discord.Embed:
    e = discord.Embed(title=title, color=color)
    for token, en, fr in pairs:
        e.add_field(name=token, value=f"**{en}** — {fr}", inline=False)
    return e

# ===========================================================
# Cog
# ===========================================================

class Reference(commands.Cog):
    """Aides/mappings FR-EN pour les armes, off-hands, ressources et qualités."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ----- listes globales -----

    @commands.command(name="list_armes", help="Liste des familles d’armes (EN → FR).")
    @only_market_channel()
    async def list_armes(self, ctx: commands.Context):
        e = discord.Embed(title="🗡️ Familles d’armes", color=discord.Color.green())
        for en, fr in WEAPON_FAMILIES.items():
            e.add_field(name=en, value=fr, inline=True)
        e.set_footer(text="Ex: !list_bow  |  Utilise les tokens pour !bestprice")
        await ctx.send(embed=e)

    @commands.command(name="list_offhands", help="Liste des mains droites (off-hands).")
    @only_market_channel()
    async def list_offhands(self, ctx: commands.Context):
        await ctx.send(embed=_embed_pairs("🛡️ Off-hands — tokens", OFFHANDS, color=discord.Color.gold()))

    @commands.command(name="list_resources", help="Liste des ressources principales.")
    @only_market_channel()
    async def list_resources(self, ctx: commands.Context):
        await ctx.send(embed=_embed_pairs("⛏️ Ressources — catégories", RESOURCES_OVERVIEW, color=discord.Color.dark_gold()))

    @commands.command(name="list_quality", help="Liste des qualités (1 → 5).")
    @only_market_channel()
    async def list_quality(self, ctx: commands.Context):
        e = discord.Embed(title="⭐ Qualités (Albion)", color=discord.Color.purple())
        for q, label in QUALITY_MAP:
            e.add_field(name=str(q), value=label, inline=True)
        e.set_footer(text="Qualité 5 = Chef-d’œuvre (aussi appelé Formidable)")
        await ctx.send(embed=e)

    # ----- armes : commandes détaillées -----

    @commands.command(name="list_bow", help="Arcs : token → EN / FR.")
    @only_market_channel()
    async def list_bow(self, ctx):       await ctx.send(embed=_embed_pairs("🏹 Arcs — tokens", BOWS))

    @commands.command(name="list_sword", help="Épées : token → EN / FR.")
    @only_market_channel()
    async def list_sword(self, ctx):     await ctx.send(embed=_embed_pairs("⚔️ Épées — tokens", SWORDS))

    @commands.command(name="list_axe", help="Haches : token → EN / FR.")
    @only_market_channel()
    async def list_axe(self, ctx):       await ctx.send(embed=_embed_pairs("🪓 Haches — tokens", AXES))

    @commands.command(name="list_mace", help="Masses : token → EN / FR.")
    @only_market_channel()
    async def list_mace(self, ctx):      await ctx.send(embed=_embed_pairs("🔨 Masses — tokens", MACES))

    @commands.command(name="list_spear", help="Lances : token → EN / FR.")
    @only_market_channel()
    async def list_spear(self, ctx):     await ctx.send(embed=_embed_pairs("🪬 Lances — tokens", SPEARS))

    @commands.command(name="list_crossbow", help="Arbalètes : token → EN / FR.")
    @only_market_channel()
    async def list_crossbow(self, ctx):  await ctx.send(embed=_embed_pairs("🏹 Arbalètes — tokens", CROSSBOWS))

    @commands.command(name="list_dagger", help="Dagues : token → EN / FR.")
    @only_market_channel()
    async def list_dagger(self, ctx):    await ctx.send(embed=_embed_pairs("🗡️ Dagues — tokens", DAGGERS))

    @commands.command(name="list_hammer", help="Marteaux : token → EN / FR.")
    @only_market_channel()
    async def list_hammer(self, ctx):    await ctx.send(embed=_embed_pairs("⛏️ Marteaux — tokens", HAMMERS))

    @commands.command(name="list_quarterstaff", help="Bâtons de combat : token → EN / FR.")
    @only_market_channel()
    async def list_quarterstaff(self, ctx): await ctx.send(embed=_embed_pairs("🥢 Bâtons de combat — tokens", QUARTERSTAVES))

    @commands.command(name="list_fire", help="Bâtons de feu : token → EN / FR.")
    @only_market_channel()
    async def list_fire(self, ctx):      await ctx.send(embed=_embed_pairs("🔥 Bâtons de feu — tokens", FIRE_STAFFS))

    @commands.command(name="list_frost", help="Bâtons de glace : token → EN / FR.")
    @only_market_channel()
    async def list_frost(self, ctx):     await ctx.send(embed=_embed_pairs("❄️ Bâtons de glace — tokens", FROST_STAFFS))

    @commands.command(name="list_cursed", help="Bâtons maudits : token → EN / FR.")
    @only_market_channel()
    async def list_cursed(self, ctx):    await ctx.send(embed=_embed_pairs("💀 Bâtons maudits — tokens", CURSED_STAFFS))

    @commands.command(name="list_holy", help="Bâtons sacrés : token → EN / FR.")
    @only_market_channel()
    async def list_holy(self, ctx):      await ctx.send(embed=_embed_pairs("✨ Bâtons sacrés — tokens", HOLY_STAFFS))

    @commands.command(name="list_arcane", help="Bâtons des arcanes : token → EN / FR.")
    @only_market_channel()
    async def list_arcane(self, ctx):    await ctx.send(embed=_embed_pairs("🌀 Bâtons des arcanes — tokens", ARCANE_STAFFS))

    @commands.command(name="list_nature", help="Bâtons de nature : token → EN / FR.")
    @only_market_channel()
    async def list_nature(self, ctx):    await ctx.send(embed=_embed_pairs("🌿 Bâtons de nature — tokens", NATURE_STAFFS))

    # ----- ressources détaillées -----

    @commands.command(name="list_wood", help="Ressources bois : token → EN / FR.")
    @only_market_channel()
    async def list_wood(self, ctx):      await ctx.send(embed=_embed_pairs("🌲 Bois — tokens", WOOD, color=discord.Color.dark_green()))

    @commands.command(name="list_ore", help="Ressources minerai : token → EN / FR.")
    @only_market_channel()
    async def list_ore(self, ctx):       await ctx.send(embed=_embed_pairs("⛏️ Minerai — tokens", ORE, color=discord.Color.dark_gray()))

    @commands.command(name="list_fiber", help="Ressources fibre : token → EN / FR.")
    @only_market_channel()
    async def list_fiber(self, ctx):     await ctx.send(embed=_embed_pairs("🪵 Fibre — tokens", FIBER, color=discord.Color.teal()))

    @commands.command(name="list_hide", help="Ressources peaux/cuir : token → EN / FR.")
    @only_market_channel()
    async def list_hide(self, ctx):      await ctx.send(embed=_embed_pairs("🐾 Peaux & cuir — tokens", HIDE, color=discord.Color.dark_orange()))

    @commands.command(name="list_stone", help="Ressources pierre : token → EN / FR.")
    @only_market_channel()
    async def list_stone(self, ctx):     await ctx.send(embed=_embed_pairs("🪨 Pierre — tokens", STONE, color=discord.Color.light_gray()))

async def setup(bot: commands.Bot):
    await bot.add_cog(Reference(bot))
