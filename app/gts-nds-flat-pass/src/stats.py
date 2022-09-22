from array import array
from namegen import namegen


def statread(pkm):
    p = array('B')
    p.fromstring(pkm)

    pid = p[0x00] + (p[0x01] << 8) + (p[0x02] << 16) + (p[0x03] << 24)
    nickname = namegen(pkm[0x48:0x5e])
    lv = p[0x8c]
    nat = nature.get(pid % 25)
    spec = species.get((p[0x09] << 8) + p[0x08])
    abil = ability.get(p[0x15])
    if p[0x40] & 4:
        gender = '(Genderless)'
    elif p[0x40] & 2:
        gender = '(Female)'
    else:
        gender = '(Male)'
    otname = namegen(pkm[0x68:0x78])
    otid = (p[0x0d] << 8) + p[0x0c]
    secid = (p[0x0f] << 8) + p[0x0e]
    held = items.get((p[0x0b] << 8) + p[0x0a])
    ivs = ivcheck(p[0x38:0x3c])
    evs = evcheck(p[0x18:0x1e])
    atk = attackcheck(p[0x28:0x30])
    hidden = hiddenpower(ivs)
    happy = p[0x14]
    shiny = shinycheck(pid, otid, secid)
    if shiny:
        shiny = ' Shiny!'
    else:
        shiny = ''

    s = '%s:%s\n    ' % (nickname, shiny)
    s += 'Lv %d %s %s with %s %s\n\n    ' % (lv, nat, spec, abil, gender)
    s += 'OT: %s,  ID: %05d,  Secret ID: %05d\n    ' % (otname, otid, secid)
    s += 'Holding: %s,  Happiness: %d\n    ' % (held, happy)
    s += 'Hidden Power: %s-type, %d Base Power\n\n    ' % hidden
    s += 'Attacks: %-12s %-12s\n             %-12s %-12s\n\n    ' % atk
    s += 'IVs: HP %3d, Atk %3d, Def %3d, SpA %3d, SpD %3d, Spe %3d\n    ' % ivs
    s += 'EVs: HP %3d, Atk %3d, Def %3d, SpA %3d, SpD %3d, Spe %3d, \
Total %d\n\n' % evs
    s += '=' * 80 + '\n\n'

    with open('statlog.txt', 'a') as f:
        f.write(s)


def ivcheck(b):
    ivs = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
    hp = (ivs & 0x0000001f)
    atk = (ivs & 0x000003e0) >> 5
    df = (ivs & 0x00007c00) >> 10
    spe = (ivs & 0x000f8000) >> 15
    spa = (ivs & 0x01f00000) >> 20
    spd = (ivs & 0x3e000000) >> 25
    return (hp, atk, df, spa, spd, spe)


def evcheck(b):
    hp = b[0]
    atk = b[1]
    df = b[2]
    spe = b[3]
    spa = b[4]
    spd = b[5]
    total = hp + atk + df + spe + spa + spd
    return (hp, atk, df, spa, spd, spe, total)


def attackcheck(b):
    a1 = attacks.get(b[0] + (b[1] << 8))
    a2 = attacks.get(b[2] + (b[3] << 8))
    a3 = attacks.get(b[4] + (b[5] << 8))
    a4 = attacks.get(b[6] + (b[7] << 8))
    return (a1, a2, a3, a4)


def shinycheck(pid, otid, secid):
    pida = pid >> 16
    pidb = pid & 0xffff
    ids = otid ^ secid
    pids = pida ^ pidb
    return (ids ^ pids) < 8


def hiddenpower(ivs):
    t = 0
    p = 0
    for i in range(6):
        t += (ivs[i] % 2) * (2 ** i)
        m = ivs[i] % 4
        if m == 2 or m == 3:
            p += 2 ** i

    t = int((t * 15) / 63)
    p = int((p * 40) / 63) + 30
    return (hptype.get(t), p)


species = {
    1: 'Bulbasaur',
    2: 'Ivysaur',
    3: 'Venusaur',
    4: 'Charmander',
    5: 'Charmeleon',
    6: 'Charizard',
    7: 'Squirtle',
    8: 'Wartortle',
    9: 'Blastoise',
    10: 'Caterpie',
    11: 'Metapod',
    12: 'Butterfree',
    13: 'Weedle',
    14: 'Kakuna',
    15: 'Beedrill',
    16: 'Pidgey',
    17: 'Pidgeotto',
    18: 'Pidgeot',
    19: 'Rattata',
    20: 'Raticate',
    21: 'Spearow',
    22: 'Fearow',
    23: 'Ekans',
    24: 'Arbok',
    25: 'Pikachu',
    26: 'Raichu',
    27: 'Sandshrew',
    28: 'Sandslash',
    29: 'Nidoran (F)',
    30: 'Nidorina',
    31: 'Nidoqueen',
    32: 'Nidoran (M)',
    33: 'Nidorino',
    34: 'Nidoking',
    35: 'Clefairy',
    36: 'Clefable',
    37: 'Vulpix',
    38: 'Ninetales',
    39: 'Jigglypuff',
    40: 'Wigglytuff',
    41: 'Zubat',
    42: 'Golbat',
    43: 'Oddish',
    44: 'Gloom',
    45: 'Vileplume',
    46: 'Paras',
    47: 'Parasect',
    48: 'Venonat',
    49: 'Venomoth',
    50: 'Diglett',
    51: 'Dugtrio',
    52: 'Meowth',
    53: 'Persian',
    54: 'Psyduck',
    55: 'Golduck',
    56: 'Mankey',
    57: 'Primeape',
    58: 'Growlithe',
    59: 'Arcanine',
    60: 'Poliwag',
    61: 'Poliwhirl',
    62: 'Poliwrath',
    63: 'Abra',
    64: 'Kadabra',
    65: 'Alakazam',
    66: 'Machop',
    67: 'Machoke',
    68: 'Machamp',
    69: 'Bellsprout',
    70: 'Weepinbell',
    71: 'Victreebel',
    72: 'Tentacool',
    73: 'Tentacruel',
    74: 'Geodude',
    75: 'Graveler',
    76: 'Golem',
    77: 'Ponyta',
    78: 'Rapidash',
    79: 'Slowpoke',
    80: 'Slowbro',
    81: 'Magnemite',
    82: 'Magneton',
    83: 'Farfetch\'d',
    84: 'Doduo',
    85: 'Dodrio',
    86: 'Seel',
    87: 'Dewgong',
    88: 'Grimer',
    89: 'Muk',
    90: 'Shellder',
    91: 'Cloyster',
    92: 'Gastly',
    93: 'Haunter',
    94: 'Gengar',
    95: 'Onix',
    96: 'Drowzee',
    97: 'Hypno',
    98: 'Krabby',
    99: 'Kingler',
    100: 'Voltorb',
    101: 'Electrode',
    102: 'Exeggcute',
    103: 'Exeggutor',
    104: 'Cubone',
    105: 'Marowak',
    106: 'Hitmonlee',
    107: 'Hitmonchan',
    108: 'Lickitung',
    109: 'Koffing',
    110: 'Weezing',
    111: 'Rhyhorn',
    112: 'Rhydon',
    113: 'Chansey',
    114: 'Tangela',
    115: 'Kangaskhan',
    116: 'Horsea',
    117: 'Seadra',
    118: 'Goldeen',
    119: 'Seaking',
    120: 'Staryu',
    121: 'Starmie',
    122: 'Mr. Mime',
    123: 'Scyther',
    124: 'Jynx',
    125: 'Electabuzz',
    126: 'Magmar',
    127: 'Pinsir',
    128: 'Tauros',
    129: 'Magikarp',
    130: 'Gyarados',
    131: 'Lapras',
    132: 'Ditto',
    133: 'Eevee',
    134: 'Vaporeon',
    135: 'Jolteon',
    136: 'Flareon',
    137: 'Porygon',
    138: 'Omanyte',
    139: 'Omastar',
    140: 'Kabuto',
    141: 'Kabutops',
    142: 'Aerodactyl',
    143: 'Snorlax',
    144: 'Articuno',
    145: 'Zapdos',
    146: 'Moltres',
    147: 'Dratini',
    148: 'Dragonair',
    149: 'Dragonite',
    150: 'Mewtwo',
    151: 'Mew',
    152: 'Chikorita',
    153: 'Bayleef',
    154: 'Meganium',
    155: 'Cyndaquil',
    156: 'Quilava',
    157: 'Typhlosion',
    158: 'Totodile',
    159: 'Croconaw',
    160: 'Feraligatr',
    161: 'Sentret',
    162: 'Furret',
    163: 'Hoothoot',
    164: 'Noctowl',
    165: 'Ledyba',
    166: 'Ledian',
    167: 'Spinarak',
    168: 'Ariados',
    169: 'Crobat',
    170: 'Chinchou',
    171: 'Lanturn',
    172: 'Pichu',
    173: 'Cleffa',
    174: 'Igglybuff',
    175: 'Togepi',
    176: 'Togetic',
    177: 'Natu',
    178: 'Xatu',
    179: 'Mareep',
    180: 'Flaaffy',
    181: 'Ampharos',
    182: 'Bellossom',
    183: 'Marill',
    184: 'Azumarill',
    185: 'Sudowoodo',
    186: 'Politoed',
    187: 'Hoppip',
    188: 'Skiploom',
    189: 'Jumpluff',
    190: 'Aipom',
    191: 'Sunkern',
    192: 'Sunflora',
    193: 'Yanma',
    194: 'Wooper',
    195: 'Quagsire',
    196: 'Espeon',
    197: 'Umbreon',
    198: 'Murkrow',
    199: 'Slowking',
    200: 'Misdreavus',
    201: 'Unown',
    202: 'Wobbuffet',
    203: 'Girafarig',
    204: 'Pineco',
    205: 'Forretress',
    206: 'Dunsparce',
    207: 'Gligar',
    208: 'Steelix',
    209: 'Snubbull',
    210: 'Granbull',
    211: 'Qwilfish',
    212: 'Scizor',
    213: 'Shuckle',
    214: 'Heracross',
    215: 'Sneasel',
    216: 'Teddiursa',
    217: 'Ursaring',
    218: 'Slugma',
    219: 'Magcargo',
    220: 'Swinub',
    221: 'Piloswine',
    222: 'Corsola',
    223: 'Remoraid',
    224: 'Octillery',
    225: 'Delibird',
    226: 'Mantine',
    227: 'Skarmory',
    228: 'Houndour',
    229: 'Houndoom',
    230: 'Kingdra',
    231: 'Phanpy',
    232: 'Donphan',
    233: 'Porygon2',
    234: 'Stantler',
    235: 'Smeargle',
    236: 'Tyrogue',
    237: 'Hitmontop',
    238: 'Smoochum',
    239: 'Elekid',
    240: 'Magby',
    241: 'Miltank',
    242: 'Blissey',
    243: 'Raikou',
    244: 'Entei',
    245: 'Suicune',
    246: 'Larvitar',
    247: 'Pupitar',
    248: 'Tyranitar',
    249: 'Lugia',
    250: 'Ho-Oh',
    251: 'Celebi',
    252: 'Treecko',
    253: 'Grovyle',
    254: 'Sceptile',
    255: 'Torchic',
    256: 'Combusken',
    257: 'Blaziken',
    258: 'Mudkip',
    259: 'Marshtomp',
    260: 'Swampert',
    261: 'Poochyena',
    262: 'Mightyena',
    263: 'Zigzagoon',
    264: 'Linoone',
    265: 'Wurmple',
    266: 'Silcoon',
    267: 'Beautifly',
    268: 'Cascoon',
    269: 'Dustox',
    270: 'Lotad',
    271: 'Lombre',
    272: 'Ludicolo',
    273: 'Seedot',
    274: 'Nuzleaf',
    275: 'Shiftry',
    276: 'Taillow',
    277: 'Swellow',
    278: 'Wingull',
    279: 'Pelipper',
    280: 'Ralts',
    281: 'Kirlia',
    282: 'Gardevoir',
    283: 'Surskit',
    284: 'Masquerain',
    285: 'Shroomish',
    286: 'Breloom',
    287: 'Slakoth',
    288: 'Vigoroth',
    289: 'Slaking',
    290: 'Nincada',
    291: 'Ninjask',
    292: 'Shedinja',
    293: 'Whismur',
    294: 'Loudred',
    295: 'Exploud',
    296: 'Makuhita',
    297: 'Hariyama',
    298: 'Azurill',
    299: 'Nosepass',
    300: 'Skitty',
    301: 'Delcatty',
    302: 'Sableye',
    303: 'Mawile',
    304: 'Aron',
    305: 'Lairon',
    306: 'Aggron',
    307: 'Meditite',
    308: 'Medicham',
    309: 'Electrike',
    310: 'Manectric',
    311: 'Plusle',
    312: 'Minun',
    313: 'Volbeat',
    314: 'Illumise',
    315: 'Roselia',
    316: 'Gulpin',
    317: 'Swalot',
    318: 'Carvanha',
    319: 'Sharpedo',
    320: 'Wailmer',
    321: 'Wailord',
    322: 'Numel',
    323: 'Camerupt',
    324: 'Torkoal',
    325: 'Spoink',
    326: 'Grumpig',
    327: 'Spinda',
    328: 'Trapinch',
    329: 'Vibrava',
    330: 'Flygon',
    331: 'Cacnea',
    332: 'Cacturne',
    333: 'Swablu',
    334: 'Altaria',
    335: 'Zangoose',
    336: 'Seviper',
    337: 'Lunatone',
    338: 'Solrock',
    339: 'Barboach',
    340: 'Whiscash',
    341: 'Corphish',
    342: 'Crawdaunt',
    343: 'Baltoy',
    344: 'Claydol',
    345: 'Lileep',
    346: 'Cradily',
    347: 'Anorith',
    348: 'Armaldo',
    349: 'Feebas',
    350: 'Milotic',
    351: 'Castform',
    352: 'Kecleon',
    353: 'Shuppet',
    354: 'Banette',
    355: 'Duskull',
    356: 'Dusclops',
    357: 'Tropius',
    358: 'Chimecho',
    359: 'Absol',
    360: 'Wynaut',
    361: 'Snorunt',
    362: 'Glalie',
    363: 'Spheal',
    364: 'Sealeo',
    365: 'Walrein',
    366: 'Clamperl',
    367: 'Huntail',
    368: 'Gorebyss',
    369: 'Relicanth',
    370: 'Luvdisc',
    371: 'Bagon',
    372: 'Shelgon',
    373: 'Salamence',
    374: 'Beldum',
    375: 'Metang',
    376: 'Metagross',
    377: 'Regirock',
    378: 'Regice',
    379: 'Registeel',
    380: 'Latias',
    381: 'Latios',
    382: 'Kyogre',
    383: 'Groudon',
    384: 'Rayquaza',
    385: 'Jirachi',
    386: 'Deoxys',
    387: 'Turtwig',
    388: 'Grotle',
    389: 'Torterra',
    390: 'Chimchar',
    391: 'Monferno',
    392: 'Infernape',
    393: 'Piplup',
    394: 'Prinplup',
    395: 'Empoleon',
    396: 'Starly',
    397: 'Staravia',
    398: 'Staraptor',
    399: 'Bidoof',
    400: 'Bibarel',
    401: 'Kricketot',
    402: 'Kricketune',
    403: 'Shinx',
    404: 'Luxio',
    405: 'Luxray',
    406: 'Budew',
    407: 'Roserade',
    408: 'Cranidos',
    409: 'Rampardos',
    410: 'Shieldon',
    411: 'Bastiodon',
    412: 'Burmy',
    413: 'Wormadam',
    414: 'Mothim',
    415: 'Combee',
    416: 'Vespiquen',
    417: 'Pachirisu',
    418: 'Buizel',
    419: 'Floatzel',
    420: 'Cherubi',
    421: 'Cherrim',
    422: 'Shellos',
    423: 'Gastrodon',
    424: 'Ambipom',
    425: 'Drifloon',
    426: 'Drifblim',
    427: 'Buneary',
    428: 'Lopunny',
    429: 'Mismagius',
    430: 'Honchkrow',
    431: 'Glameow',
    432: 'Purugly',
    433: 'Chingling',
    434: 'Stunky',
    435: 'Skuntank',
    436: 'Bronzor',
    437: 'Bronzong',
    438: 'Bonsly',
    439: 'Mime Jr.',
    440: 'Happiny',
    441: 'Chatot',
    442: 'Spiritomb',
    443: 'Gible',
    444: 'Gabite',
    445: 'Garchomp',
    446: 'Munchlax',
    447: 'Riolu',
    448: 'Lucario',
    449: 'Hippopotas',
    450: 'Hippowdon',
    451: 'Skorupi',
    452: 'Drapion',
    453: 'Croagunk',
    454: 'Toxicroak',
    455: 'Carnivine',
    456: 'Finneon',
    457: 'Lumineon',
    458: 'Mantyke',
    459: 'Snover',
    460: 'Abomasnow',
    461: 'Weavile',
    462: 'Magnezone',
    463: 'Lickilicky',
    464: 'Rhyperior',
    465: 'Tangrowth',
    466: 'Electivire',
    467: 'Magmortar',
    468: 'Togekiss',
    469: 'Yanmega',
    470: 'Leafeon',
    471: 'Glaceon',
    472: 'Gliscor',
    473: 'Mamoswine',
    474: 'Porygon-Z',
    475: 'Gallade',
    476: 'Probopass',
    477: 'Dusknoir',
    478: 'Froslass',
    479: 'Rotom',
    480: 'Uxie',
    481: 'Mesprit',
    482: 'Azelf',
    483: 'Dialga',
    484: 'Palkia',
    485: 'Heatran',
    486: 'Regigigas',
    487: 'Giratina',
    488: 'Cresselia',
    489: 'Phione',
    490: 'Manaphy',
    491: 'Darkrai',
    492: 'Shaymin',
    493: 'Arceus'
}

nature = {
    0: 'Hardy',
    1: 'Lonely',
    2: 'Brave',
    3: 'Adamant',
    4: 'Naughty',
    5: 'Bold',
    6: 'Docile',
    7: 'Relaxed',
    8: 'Impish',
    9: 'Lax',
    10: 'Timid',
    11: 'Hasty',
    12: 'Serious',
    13: 'Jolly',
    14: 'Naive',
    15: 'Modest',
    16: 'Mild',
    17: 'Quiet',
    18: 'Bashful',
    19: 'Rash',
    20: 'Calm',
    21: 'Gentle',
    22: 'Sassy',
    23: 'Careful',
    24: 'Quirky'
}

ability = {
    1: 'Stench',
    2: 'Drizzle',
    3: 'Speed Boost',
    4: 'Battle Armor',
    5: 'Sturdy',
    6: 'Damp',
    7: 'Limber',
    8: 'Sand Veil',
    9: 'Static',
    10: 'Volt Absorb',
    11: 'Water Absorb',
    12: 'Oblivious',
    13: 'Cloud Nine',
    14: 'Compoundeyes',
    15: 'Insomnia',
    16: 'Color Change',
    17: 'Immunity',
    18: 'Flash Fire',
    19: 'Shield Dust',
    20: 'Own Tempo',
    21: 'Suction Cups',
    22: 'Intimidate',
    23: 'Shadow Tag',
    24: 'Rough Skin',
    25: 'Wonder Guard',
    26: 'Levitate',
    27: 'Effect Spore',
    28: 'Synchronize',
    29: 'Clear Body',
    30: 'Natural Cure',
    31: 'Lightningrod',
    32: 'Serene Grace',
    33: 'Swift Swim',
    34: 'Chlorophyll',
    35: 'Illuminate',
    36: 'Trace',
    37: 'Huge Power',
    38: 'Poison Point',
    39: 'Inner Focus',
    40: 'Magma Armor',
    41: 'Water Veil',
    42: 'Magnet Pull',
    43: 'Soundproof',
    44: 'Rain Dish',
    45: 'Sand Stream',
    46: 'Pressure',
    47: 'Thick Fat',
    48: 'Early Bird',
    49: 'Flame Body',
    50: 'Run Away',
    51: 'Keen Eye',
    52: 'Hyper Cutter',
    53: 'Pickup',
    54: 'Truant',
    55: 'Hustle',
    56: 'Cute Charm',
    57: 'Plus',
    58: 'Minus',
    59: 'Forecast',
    60: 'Sticky Hold',
    61: 'Shed Skin',
    62: 'Guts',
    63: 'Marvel Scale',
    64: 'Liquid Ooze',
    65: 'Overgrow',
    66: 'Blaze',
    67: 'Torrent',
    68: 'Swarm',
    69: 'Rock Head',
    70: 'Drought',
    71: 'Arena Trap',
    72: 'Vital Spirit',
    73: 'White Smoke',
    74: 'Pure Power',
    75: 'Shell Armor',
    76: 'Air Lock',
    77: 'Tangled Feet',
    78: 'Motor Drive',
    79: 'Rivalry',
    80: 'Steadfast',
    81: 'Snow Cloak',
    82: 'Gluttony',
    83: 'Anger Point',
    84: 'Unburden',
    85: 'Heatproof',
    86: 'Simple',
    87: 'Dry Skin',
    88: 'Download',
    89: 'Iron Fist',
    90: 'Poison Heal',
    91: 'Adaptability',
    92: 'Skill Link',
    93: 'Hydration',
    94: 'Solar Power',
    95: 'Quick Feet',
    96: 'Normalize',
    97: 'Sniper',
    98: 'Magic Guard',
    99: 'No Guard',
    100: 'Stall',
    101: 'Technician',
    102: 'Leaf Guard',
    103: 'Klutz',
    104: 'Mold Breaker',
    105: 'Super Luck',
    106: 'Aftermath',
    107: 'Anticipation',
    108: 'Forewarn',
    109: 'Unaware',
    110: 'Tinted Lens',
    111: 'Filter',
    112: 'Slow Start',
    113: 'Scrappy',
    114: 'Storm Drain',
    115: 'Ice Body',
    116: 'Solid Rock',
    117: 'Snow Warning',
    118: 'Honey Gather',
    119: 'Frisk',
    120: 'Reckless',
    121: 'Multitype',
    122: 'Flower Gift',
    123: 'Bad Dreams'
}

attacks = {
    1: 'Pound',
    2: 'Karate Chop',
    3: 'Double Slap',
    4: 'Comet Punch',
    5: 'Mega Punch',
    6: 'Pay Day',
    7: 'Fire Punch',
    8: 'Ice Punch',
    9: 'Thunder Punch',
    10: 'Scratch',
    11: 'Vice Grip',
    12: 'Guillotine',
    13: 'Razor Wind',
    14: 'Swords Dance',
    15: 'Cut',
    16: 'Gust',
    17: 'Wing Attack',
    18: 'Whirlwind',
    19: 'Fly',
    20: 'Bind',
    21: 'Slam',
    22: 'Vine Whip',
    23: 'Stomp',
    24: 'Double Kick',
    25: 'Mega Kick',
    26: 'Jump Kick',
    27: 'Rolling Kick',
    28: 'Sand-Attack',
    29: 'Headbutt',
    30: 'Horn Attack',
    31: 'Fury Attack',
    32: 'Horn Drill',
    33: 'Tackle',
    34: 'Body Slam',
    35: 'Wrap',
    36: 'Take Down',
    37: 'Thrash',
    38: 'Double-Edge',
    39: 'Tail Whip',
    40: 'Poison Sting',
    41: 'Twineedle',
    42: 'Pin Missile',
    43: 'Leer',
    44: 'Bite',
    45: 'Growl',
    46: 'Roar',
    47: 'Sing',
    48: 'Supersonic',
    49: 'Sonic Boom',
    50: 'Disable',
    51: 'Acid',
    52: 'Ember',
    53: 'Flamethrower',
    54: 'Mist',
    55: 'Water Gun',
    56: 'Hydro Pump',
    57: 'Surf',
    58: 'Ice Beam',
    59: 'Blizzard',
    60: 'Psybeam',
    61: 'Bubble Beam',
    62: 'Aurora Beam',
    63: 'Hyper Beam',
    64: 'Peck',
    65: 'Drill Peck',
    66: 'Submission',
    67: 'Low Kick',
    68: 'Counter',
    69: 'Seismic Toss',
    70: 'Strength',
    71: 'Absorb',
    72: 'Mega Drain',
    73: 'Leech Seed',
    74: 'Growth',
    75: 'Razor Leaf',
    76: 'Solar Beam',
    77: 'Poison Powder',
    78: 'Stun Spore',
    79: 'Sleep Powder',
    80: 'Petal Dance',
    81: 'String Shot',
    82: 'Dragon Rage',
    83: 'Fire Spin',
    84: 'Thunder Shock',
    85: 'Thunderbolt',
    86: 'Thunder Wave',
    87: 'Thunder',
    88: 'Rock Throw',
    89: 'Earthquake',
    90: 'Fissure',
    91: 'Dig',
    92: 'Toxic',
    93: 'Confusion',
    94: 'Psychic',
    95: 'Hypnosis',
    96: 'Meditate',
    97: 'Agility',
    98: 'Quick Attack',
    99: 'Rage',
    100: 'Teleport',
    101: 'Night Shade',
    102: 'Mimic',
    103: 'Screech',
    104: 'Double Team',
    105: 'Recover',
    106: 'Harden',
    107: 'Minimize',
    108: 'SmokeScreen',
    109: 'Confuse Ray',
    110: 'Withdraw',
    111: 'Defense Curl',
    112: 'Barrier',
    113: 'Light Screen',
    114: 'Haze',
    115: 'Reflect',
    116: 'Focus Energy',
    117: 'Bide',
    118: 'Metronome',
    119: 'Mirror Move',
    120: 'Self Destruct',
    121: 'Egg Bomb',
    122: 'Lick',
    123: 'Smog',
    124: 'Sludge',
    125: 'Bone Club',
    126: 'Fire Blast',
    127: 'Waterfall',
    128: 'Clamp',
    129: 'Swift',
    130: 'Skull Bash',
    131: 'Spike Cannon',
    132: 'Constrict',
    133: 'Amnesia',
    134: 'Kinesis',
    135: 'Soft Boiled',
    136: 'High Jump Kick',
    137: 'Glare',
    138: 'Dream Eater',
    139: 'Poison Gas',
    140: 'Barrage',
    141: 'Leech Life',
    142: 'Lovely Kiss',
    143: 'Sky Attack',
    144: 'Transform',
    145: 'Bubble',
    146: 'Dizzy Punch',
    147: 'Spore',
    148: 'Flash',
    149: 'Psywave',
    150: 'Splash',
    151: 'Acid Armor',
    152: 'Crabhammer',
    153: 'Explosion',
    154: 'Fury Swipes',
    155: 'Bonemerang',
    156: 'Rest',
    157: 'Rock Slide',
    158: 'Hyper Fang',
    159: 'Sharpen',
    160: 'Conversion',
    161: 'Tri Attack',
    162: 'Super Fang',
    163: 'Slash',
    164: 'Substitute',
    165: 'Struggle',
    166: 'Sketch',
    167: 'Triple Kick',
    168: 'Thief',
    169: 'Spider Web',
    170: 'Mind Reader',
    171: 'Nightmare',
    172: 'Flame Wheel',
    173: 'Snore',
    174: 'Curse',
    175: 'Flail',
    176: 'Conversion 2',
    177: 'Aeroblast',
    178: 'Cotton Spore',
    179: 'Reversal',
    180: 'Spite',
    181: 'Powder Snow',
    182: 'Protect',
    183: 'Mach Punch',
    184: 'Scary Face',
    185: 'Feint Attack',
    186: 'Sweet Kiss',
    187: 'Belly Drum',
    188: 'Sludge Bomb',
    189: 'Mud-Slap',
    190: 'Octazooka',
    191: 'Spikes',
    192: 'Zap Cannon',
    193: 'Foresight',
    194: 'Destiny Bond',
    195: 'Perish Song',
    196: 'Icy Wind',
    197: 'Detect',
    198: 'Bone Rush',
    199: 'Lock-On',
    200: 'Outrage',
    201: 'Sandstorm',
    202: 'Giga Drain',
    203: 'Endure',
    204: 'Charm',
    205: 'Rollout',
    206: 'False Swipe',
    207: 'Swagger',
    208: 'Milk Drink',
    209: 'Spark',
    210: 'Fury Cutter',
    211: 'Steel Wing',
    212: 'Mean Look',
    213: 'Attract',
    214: 'Sleep Talk',
    215: 'Heal Bell',
    216: 'Return',
    217: 'Present',
    218: 'Frustration',
    219: 'Safeguard',
    220: 'Pain Split',
    221: 'Sacred Fire',
    222: 'Magnitude',
    223: 'Dynamic Punch',
    224: 'Megahorn',
    225: 'Dragon Breath',
    226: 'Baton Pass',
    227: 'Encore',
    228: 'Pursuit',
    229: 'Rapid Spin',
    230: 'Sweet Scent',
    231: 'Iron Tail',
    232: 'Metal Claw',
    233: 'Vital Throw',
    234: 'Morning Sun',
    235: 'Synthesis',
    236: 'Moonlight',
    237: 'Hidden Power',
    238: 'Cross Chop',
    239: 'Twister',
    240: 'Rain Dance',
    241: 'Sunny Day',
    242: 'Crunch',
    243: 'Mirror Coat',
    244: 'Psych Up',
    245: 'Extreme Speed',
    246: 'Ancient Power',
    247: 'Shadow Ball',
    248: 'Future Sight',
    249: 'Rock Smash',
    250: 'Whirlpool',
    251: 'Beat Up',
    252: 'Fake Out',
    253: 'Uproar',
    254: 'Stockpile',
    255: 'Spit Up',
    256: 'Swallow',
    257: 'Heat Wave',
    258: 'Hail',
    259: 'Torment',
    260: 'Flatter',
    261: 'Will-O-Wisp',
    262: 'Memento',
    263: 'Facade',
    264: 'Focus Punch',
    265: 'Smelling Salts',
    266: 'Follow Me',
    267: 'Nature Power',
    268: 'Charge',
    269: 'Taunt',
    270: 'Helping Hand',
    271: 'Trick',
    272: 'Role Play',
    273: 'Wish',
    274: 'Assist',
    275: 'Ingrain',
    276: 'Superpower',
    277: 'Magic Coat',
    278: 'Recycle',
    279: 'Revenge',
    280: 'Brick Break',
    281: 'Yawn',
    282: 'Knock Off',
    283: 'Endeavor',
    284: 'Eruption',
    285: 'Skill Swap',
    286: 'Imprison',
    287: 'Refresh',
    288: 'Grudge',
    289: 'Snatch',
    290: 'Secret Power',
    291: 'Dive',
    292: 'Arm Thrust',
    293: 'Camouflage',
    294: 'Tail Glow',
    295: 'Luster Purge',
    296: 'Mist Ball',
    297: 'Feather Dance',
    298: 'Teeter Dance',
    299: 'Blaze Kick',
    300: 'Mud Sport',
    301: 'Ice Ball',
    302: 'Needle Arm',
    303: 'Slack Off',
    304: 'Hyper Voice',
    305: 'Poison Fang',
    306: 'Crush Claw',
    307: 'Blast Burn',
    308: 'Hydro Cannon',
    309: 'Meteor Mash',
    310: 'Astonish',
    311: 'Weather Ball',
    312: 'Aromatherapy',
    313: 'Fake Tears',
    314: 'Air Cutter',
    315: 'Overheat',
    316: 'Odor Sleuth',
    317: 'Rock Tomb',
    318: 'Silver Wind',
    319: 'Metal Sound',
    320: 'Grass Whistle',
    321: 'Tickle',
    322: 'Cosmic Power',
    323: 'Water Spout',
    324: 'Signal Beam',
    325: 'Shadow Punch',
    326: 'Extrasensory',
    327: 'Sky Uppercut',
    328: 'Sand Tomb',
    329: 'Sheer Cold',
    330: 'Muddy Water',
    331: 'Bullet Seed',
    332: 'Aerial Ace',
    333: 'Icicle Spear',
    334: 'Iron Defense',
    335: 'Block',
    336: 'Howl',
    337: 'Dragon Claw',
    338: 'Frenzy Plant',
    339: 'Bulk Up',
    340: 'Bounce',
    341: 'Mud Shot',
    342: 'Poison Tail',
    343: 'Covet',
    344: 'Volt Tackle',
    345: 'Magical Leaf',
    346: 'Water Sport',
    347: 'Calm Mind',
    348: 'Leaf Blade',
    349: 'Dragon Dance',
    350: 'Rock Blast',
    351: 'Shock Wave',
    352: 'Water Pulse',
    353: 'Doom Desire',
    354: 'Psycho Boost',
    355: 'Roost',
    356: 'Gravity',
    357: 'Miracle Eye',
    358: 'Wake-Up Slap',
    359: 'Hammer Arm',
    360: 'Gyro Ball',
    361: 'Healing Wish',
    362: 'Brine',
    363: 'Natural Gift',
    364: 'Feint',
    365: 'Pluck',
    366: 'Tailwind',
    367: 'Acupressure',
    368: 'Metal Burst',
    369: 'U-turn',
    370: 'Close Combat',
    371: 'Payback',
    372: 'Assurance',
    373: 'Embargo',
    374: 'Fling',
    375: 'Psycho Shift',
    376: 'Trump Card',
    377: 'Heal Block',
    378: 'Wring Out',
    379: 'Power Trick',
    380: 'Gastro Acid',
    381: 'Lucky Chant',
    382: 'Me First',
    383: 'Copycat',
    384: 'Power Swap',
    385: 'Guard Swap',
    386: 'Punishment',
    387: 'Last Resort',
    388: 'Worry Seed',
    389: 'Sucker Punch',
    390: 'Toxic Spikes',
    391: 'Heart Swap',
    392: 'Aqua Ring',
    393: 'Magnet Rise',
    394: 'Flare Blitz',
    395: 'Force Palm',
    396: 'Aura Sphere',
    397: 'Rock Polish',
    398: 'Poison Jab',
    399: 'Dark Pulse',
    400: 'Night Slash',
    401: 'Aqua Tail',
    402: 'Seed Bomb',
    403: 'Air Slash',
    404: 'X-Scissor',
    405: 'Bug Buzz',
    406: 'Dragon Pulse',
    407: 'Dragon Rush',
    408: 'Power Gem',
    409: 'Drain Punch',
    410: 'Vacuum Wave',
    411: 'Focus Blast',
    412: 'Energy Ball',
    413: 'Brave Bird',
    414: 'Earth Power',
    415: 'Switcheroo',
    416: 'Giga Impact',
    417: 'Nasty Plot',
    418: 'Bullet Punch',
    419: 'Avalanche',
    420: 'Ice Shard',
    421: 'Shadow Claw',
    422: 'Thunder Fang',
    423: 'Ice Fang',
    424: 'Fire Fang',
    425: 'Shadow Sneak',
    426: 'Mud Bomb',
    427: 'Psycho Cut',
    428: 'Zen Headbutt',
    429: 'Mirror Shot',
    430: 'Flash Cannon',
    431: 'Rock Climb',
    432: 'Defog',
    433: 'Trick Room',
    434: 'Draco Meteor',
    435: 'Discharge',
    436: 'Lava Plume',
    437: 'Leaf Storm',
    438: 'Power Whip',
    439: 'Rock Wrecker',
    440: 'Cross Poison',
    441: 'Gunk Shot',
    442: 'Iron Head',
    443: 'Magnet Bomb',
    444: 'Stone Edge',
    445: 'Captivate',
    446: 'Stealth Rock',
    447: 'Grass Knot',
    448: 'Chatter',
    449: 'Judgment',
    450: 'Bug Bite',
    451: 'Charge Beam',
    452: 'Wood Hammer',
    453: 'Aqua Jet',
    454: 'Attack Order',
    455: 'Defend Order',
    456: 'Heal Order',
    457: 'Head Smash',
    458: 'Double Hit',
    459: 'Roar of Time',
    460: 'Spacial Rend',
    461: 'Lunar Dance',
    462: 'Crush Grip',
    463: 'Magma Storm',
    464: 'Dark Void',
    465: 'Seed Flare',
    466: 'Ominous Wind',
    467: 'Shadow Force'
}

items = {
    0x0000: 'Nothing',
    0x0001: 'Master Ball',
    0x0002: 'Ultra Ball',
    0x0003: 'Great Ball',
    0x0004: 'Poke Ball',
    0x0005: 'Safari Ball',
    0x0006: 'Net Ball',
    0x0007: 'Dive Ball',
    0x0008: 'Nest Ball',
    0x0009: 'Repeat Ball',
    0x000A: 'Timer Ball',
    0x000B: 'Luxury Ball',
    0x000C: 'Premier Ball',
    0x000D: 'Dusk Ball',
    0x000E: 'Heal Ball',
    0x000F: 'Quick Ball',
    0x0010: 'Cherish Ball',
    0x0011: 'Potion',
    0x0012: 'Antidote',
    0x0013: 'Burn Heal',
    0x0014: 'Ice Heal',
    0x0015: 'Awakening',
    0x0016: 'Parlyz Heal',
    0x0017: 'Full Restore',
    0x0018: 'Max Potion',
    0x0019: 'Hyper Potion',
    0x001A: 'Super Potion',
    0x001B: 'Full Heal',
    0x001C: 'Revive',
    0x001D: 'Max Revive',
    0x001E: 'Fresh Water',
    0x001F: 'Soda Pop',
    0x0020: 'Lemonade',
    0x0021: 'Moomoo Milk',
    0x0022: 'EnergyPowder',
    0x0023: 'Energy Root',
    0x0024: 'Heal Powder',
    0x0025: 'Revival Herb',
    0x0026: 'Ether',
    0x0027: 'Max Ether',
    0x0028: 'Elixir',
    0x0029: 'Max Elixir',
    0x002A: 'Lava Cookie',
    0x002B: 'Berry Juice',
    0x002C: 'Sacred Ash',
    0x002D: 'HP Up',
    0x002E: 'Protein',
    0x002F: 'Iron',
    0x0030: 'Carbos',
    0x0031: 'Calcium',
    0x0032: 'Rare Candy',
    0x0033: 'PP Up',
    0x0034: 'Zinc',
    0x0035: 'PP Max',
    0x0036: 'Old Gateau',
    0x0037: 'Guard Spec.',
    0x0038: 'Dire Hit',
    0x0039: 'X Attack',
    0x003A: 'X Defend',
    0x003B: 'X Speed',
    0x003C: 'X Accuracy',
    0x003D: 'X Special',
    0x003E: 'X Sp. Def',
    0x003F: 'Poke Doll',
    0x0040: 'Fluffy Tail',
    0x0041: 'Blue Flute',
    0x0042: 'Yellow Flute',
    0x0043: 'Red Flute',
    0x0044: 'Black Flute',
    0x0045: 'White Flute',
    0x0046: 'Shoal Salt',
    0x0047: 'Shoal Shell',
    0x0048: 'Red Shard',
    0x0049: 'Blue Shard',
    0x004A: 'Yellow Shard',
    0x004B: 'Green Shard',
    0x004C: 'Super Repel',
    0x004D: 'Max Repel',
    0x004E: 'Escape Rope',
    0x004F: 'Repel',
    0x0050: 'Sun Stone',
    0x0051: 'Moon Stone',
    0x0052: 'Fire Stone',
    0x0053: 'Thunderstone',
    0x0054: 'Water Stone',
    0x0055: 'Leaf Stone',
    0x0056: 'TinyMushroom',
    0x0057: 'Big Mushroom',
    0x0058: 'Pearl',
    0x0059: 'Big Pearl',
    0x005A: 'Stardust',
    0x005B: 'Star Piece',
    0x005C: 'Nugget',
    0x005D: 'Heart Scale',
    0x005E: 'Honey',
    0x005F: 'Growth Mulch',
    0x0060: 'Damp Mulch',
    0x0061: 'Stable Mulch',
    0x0062: 'Gooey Mulch',
    0x0063: 'Root Fossil',
    0x0064: 'Claw Fossil',
    0x0065: 'Helix Fossil',
    0x0066: 'Dome Fossil',
    0x0067: 'Old Amber',
    0x0068: 'Armor Fossil',
    0x0069: 'Skull Fossil',
    0x006A: 'Rare Bone',
    0x006B: 'Shiny Stone',
    0x006C: 'Dusk Stone',
    0x006D: 'Dawn Stone',
    0x006E: 'Oval Stone',
    0x006F: 'Odd Keystone',
    0x0070: 'Griseous Orb',
    0x0071: '???',
    0x0072: '???',
    0x0073: '???',
    0x0074: '???',
    0x0075: '???',
    0x0076: '???',
    0x0077: '???',
    0x0078: '???',
    0x0079: '???',
    0x007A: '???',
    0x007B: '???',
    0x007C: '???',
    0x007D: '???',
    0x007E: '???',
    0x007F: '???',
    0x0080: '???',
    0x0081: '???',
    0x0082: '???',
    0x0083: '???',
    0x0084: '???',
    0x0085: '???',
    0x0086: '???',
    0x0087: 'Adamant Orb',
    0x0088: 'Lustrous Orb',
    0x0089: 'Grass Mail',
    0x008A: 'Flame Mail',
    0x008B: 'Bubble Mail',
    0x008C: 'Bloom Mail',
    0x008D: 'Tunnel Mail',
    0x008E: 'Steel Mail',
    0x008F: 'Heart Mail',
    0x0090: 'Snow Mail',
    0x0091: 'Space Mail',
    0x0092: 'Air Mail',
    0x0093: 'Mosaic Mail',
    0x0094: 'Brick Mail',
    0x0095: 'Cheri Berry',
    0x0096: 'Chesto Berry',
    0x0097: 'Pecha Berry',
    0x0098: 'Rawst Berry',
    0x0099: 'Aspear Berry',
    0x009A: 'Leppa Berry',
    0x009B: 'Oran Berry',
    0x009C: 'Persim Berry',
    0x009D: 'Lum Berry',
    0x009E: 'Sitrus Berry',
    0x009F: 'Figy Berry',
    0x00A0: 'Wiki Berry',
    0x00A1: 'Mago Berry',
    0x00A2: 'Aguav Berry',
    0x00A3: 'Iapapa Berry',
    0x00A4: 'Razz Berry',
    0x00A5: 'Bluk Berry',
    0x00A6: 'Nanab Berry',
    0x00A7: 'Wepear Berry',
    0x00A8: 'Pinap Berry',
    0x00A9: 'Pomeg Berry',
    0x00AA: 'Kelpsy Berry',
    0x00AB: 'Qualot Berry',
    0x00AC: 'Hondew Berry',
    0x00AD: 'Grepa Berry',
    0x00AE: 'Tamato Berry',
    0x00AF: 'Cornn Berry',
    0x00B0: 'Magost Berry',
    0x00B1: 'Rabuta Berry',
    0x00B2: 'Nomel Berry',
    0x00B3: 'Spelon Berry',
    0x00B4: 'Pamtre Berry',
    0x00B5: 'Watmel Berry',
    0x00B6: 'Durin Berry',
    0x00B7: 'Belue Berry',
    0x00B8: 'Occa Berry',
    0x00B9: 'Passho Berry',
    0x00BA: 'Wacan Berry',
    0x00BB: 'Rindo Berry',
    0x00BC: 'Yache Berry',
    0x00BD: 'Chople Berry',
    0x00BE: 'Kebia Berry',
    0x00BF: 'Shuca Berry',
    0x00C0: 'Coba Berry',
    0x00C1: 'Payapa Berry',
    0x00C2: 'Tanga Berry',
    0x00C3: 'Charti Berry',
    0x00C4: 'Kasib Berry',
    0x00C5: 'Haban Berry',
    0x00C6: 'Colbur Berry',
    0x00C7: 'Babiri Berry',
    0x00C8: 'Chilan Berry',
    0x00C9: 'Liechi Berry',
    0x00CA: 'Ganlon Berry',
    0x00CB: 'Salac Berry',
    0x00CC: 'Petaya Berry',
    0x00CD: 'Apicot Berry',
    0x00CE: 'Lansat Berry',
    0x00CF: 'Starf Berry',
    0x00D0: 'Enigma Berry',
    0x00D1: 'Micle Berry',
    0x00D2: 'Custap Berry',
    0x00D3: 'Jaboca Berry',
    0x00D4: 'Rowap Berry',
    0x00D5: 'BrightPowder',
    0x00D6: 'White Herb',
    0x00D7: 'Macho Brace',
    0x00D8: 'Exp. Share',
    0x00D9: 'Quick Claw',
    0x00DA: 'Soothe Bell',
    0x00DB: 'Mental Herb',
    0x00DC: 'Choice Band',
    0x00DD: 'King\'s Rock',
    0x00DE: 'SilverPowder',
    0x00DF: 'Amulet Coin',
    0x00E0: 'Cleanse Tag',
    0x00E1: 'Soul Dew',
    0x00E2: 'DeepSeaTooth',
    0x00E3: 'DeepSeaScale',
    0x00E4: 'Smoke Ball',
    0x00E5: 'Everstone',
    0x00E6: 'Focus Band',
    0x00E7: 'Lucky Egg',
    0x00E8: 'Scope Lens',
    0x00E9: 'Metal Coat',
    0x00EA: 'Leftovers',
    0x00EB: 'Dragon Scale',
    0x00EC: 'Light Ball',
    0x00ED: 'Soft Sand',
    0x00EE: 'Hard Stone',
    0x00EF: 'Miracle Seed',
    0x00F0: 'BlackGlasses',
    0x00F1: 'Black Belt',
    0x00F2: 'Magnet',
    0x00F3: 'Mystic Water',
    0x00F4: 'Sharp Beak',
    0x00F5: 'Poison Barb',
    0x00F6: 'NeverMeltIce',
    0x00F7: 'Spell Tag',
    0x00F8: 'TwistedSpoon',
    0x00F9: 'Charcoal',
    0x00FA: 'Dragon Fang',
    0x00FB: 'Silk Scarf',
    0x00FC: 'Up-Grade',
    0x00FD: 'Shell Bell',
    0x00FE: 'Sea Incense',
    0x00FF: 'Lax Incense',
    0x0100: 'Lucky Punch',
    0x0101: 'Metal Powder',
    0x0102: 'Thick Club',
    0x0103: 'Stick',
    0x0104: 'Red Scarf',
    0x0105: 'Blue Scarf',
    0x0106: 'Pink Scarf',
    0x0107: 'Green Scarf',
    0x0108: 'Yellow Scarf',
    0x0109: 'Wide Lens',
    0x010A: 'Muscle Band',
    0x010B: 'Wise Glasses',
    0x010C: 'Expert Belt',
    0x010D: 'Light Clay',
    0x010E: 'Life Orb',
    0x010F: 'Power Herb',
    0x0110: 'Toxic Orb',
    0x0111: 'Flame Orb',
    0x0112: 'Quick Powder',
    0x0113: 'Focus Sash',
    0x0114: 'Zoom Lens',
    0x0115: 'Metronome',
    0x0116: 'Iron Ball',
    0x0117: 'Lagging Tail',
    0x0118: 'Destiny Knot',
    0x0119: 'Black Sludge',
    0x011A: 'Icy Rock',
    0x011B: 'Smooth Rock',
    0x011C: 'Heat Rock',
    0x011D: 'Damp Rock',
    0x011E: 'Grip Claw',
    0x011F: 'Choice Scarf',
    0x0120: 'Sticky Barb',
    0x0121: 'Power Bracer',
    0x0122: 'Power Belt',
    0x0123: 'Power Lens',
    0x0124: 'Power Band',
    0x0125: 'Power Anklet',
    0x0126: 'Power Weight',
    0x0127: 'Shed Shell',
    0x0128: 'Big Root',
    0x0129: 'Choice Specs',
    0x012A: 'Flame Plate',
    0x012B: 'Splash Plate',
    0x012C: 'Zap Plate',
    0x012D: 'Meadow Plate',
    0x012E: 'Icicle Plate',
    0x012F: 'Fist Plate',
    0x0130: 'Toxic Plate',
    0x0131: 'Earth Plate',
    0x0132: 'Sky Plate',
    0x0133: 'Mind Plate',
    0x0134: 'Insect Plate',
    0x0135: 'Stone Plate',
    0x0136: 'Spooky Plate',
    0x0137: 'Draco Plate',
    0x0138: 'Dread Plate',
    0x0139: 'Iron Plate',
    0x013A: 'Odd Incense',
    0x013B: 'Rock Incense',
    0x013C: 'Full Incense',
    0x013D: 'Wave Incense',
    0x013E: 'Rose Incense',
    0x013F: 'Luck Incense',
    0x0140: 'Pure Incense',
    0x0141: 'Protector',
    0x0142: 'Electirizer',
    0x0143: 'Magmarizer',
    0x0144: 'Dubious Disc',
    0x0145: 'Reaper Cloth',
    0x0146: 'Razor Claw',
    0x0147: 'Razor Fang',
    0x0148: 'TM01',
    0x0149: 'TM02',
    0x014A: 'TM03',
    0x014B: 'TM04',
    0x014C: 'TM05',
    0x014D: 'TM06',
    0x014E: 'TM07',
    0x014F: 'TM08',
    0x0150: 'TM09',
    0x0151: 'TM10',
    0x0152: 'TM11',
    0x0153: 'TM12',
    0x0154: 'TM13',
    0x0155: 'TM14',
    0x0156: 'TM15',
    0x0157: 'TM16',
    0x0158: 'TM17',
    0x0159: 'TM18',
    0x015A: 'TM19',
    0x015B: 'TM20',
    0x015C: 'TM21',
    0x015D: 'TM22',
    0x015E: 'TM23',
    0x015F: 'TM24',
    0x0160: 'TM25',
    0x0161: 'TM26',
    0x0162: 'TM27',
    0x0163: 'TM28',
    0x0164: 'TM29',
    0x0165: 'TM30',
    0x0166: 'TM31',
    0x0167: 'TM32',
    0x0168: 'TM33',
    0x0169: 'TM34',
    0x016A: 'TM35',
    0x016B: 'TM36',
    0x016C: 'TM37',
    0x016D: 'TM38',
    0x016E: 'TM39',
    0x016F: 'TM40',
    0x0170: 'TM41',
    0x0171: 'TM42',
    0x0172: 'TM43',
    0x0173: 'TM44',
    0x0174: 'TM45',
    0x0175: 'TM46',
    0x0176: 'TM47',
    0x0177: 'TM48',
    0x0178: 'TM49',
    0x0179: 'TM50',
    0x017A: 'TM51',
    0x017B: 'TM52',
    0x017C: 'TM53',
    0x017D: 'TM54',
    0x017E: 'TM55',
    0x017F: 'TM56',
    0x0180: 'TM57',
    0x0181: 'TM58',
    0x0182: 'TM59',
    0x0183: 'TM60',
    0x0184: 'TM61',
    0x0185: 'TM62',
    0x0186: 'TM63',
    0x0187: 'TM64',
    0x0188: 'TM65',
    0x0189: 'TM66',
    0x018A: 'TM67',
    0x018B: 'TM68',
    0x018C: 'TM69',
    0x018D: 'TM70',
    0x018E: 'TM71',
    0x018F: 'TM72',
    0x0190: 'TM73',
    0x0191: 'TM74',
    0x0192: 'TM75',
    0x0193: 'TM76',
    0x0194: 'TM77',
    0x0195: 'TM78',
    0x0196: 'TM79',
    0x0197: 'TM80',
    0x0198: 'TM81',
    0x0199: 'TM82',
    0x019A: 'TM83',
    0x019B: 'TM84',
    0x019C: 'TM85',
    0x019D: 'TM86',
    0x019E: 'TM87',
    0x019F: 'TM88',
    0x01A0: 'TM89',
    0x01A1: 'TM90',
    0x01A2: 'TM91',
    0x01A3: 'TM92',
    0x01A4: 'HM01',
    0x01A5: 'HM02',
    0x01A6: 'HM03',
    0x01A7: 'HM04',
    0x01A8: 'HM05',
    0x01A9: 'HM06',
    0x01AA: 'HM07',
    0x01AB: 'HM08',
    0x01AC: 'Explorer Kit',
    0x01AD: 'Loot Sack',
    0x01AE: 'Rule Book',
    0x01AF: 'Poke Radar',
    0x01B0: 'Point Card',
    0x01B1: 'Journal',
    0x01B2: 'Seal Case',
    0x01B3: 'Fashion Case',
    0x01B4: 'Seal Bag',
    0x01B5: 'Pal Pad',
    0x01B6: 'Works Key',
    0x01B7: 'Old Charm',
    0x01B8: 'Galactic Key',
    0x01B9: 'Red Chain',
    0x01BA: 'Town Map',
    0x01BB: 'Vs. Seeker',
    0x01BC: 'Coin Case',
    0x01BD: 'Old Rod',
    0x01BE: 'Good Rod',
    0x01BF: 'Super Rod',
    0x01C0: 'Sprayduck',
    0x01C1: 'Poffin Case',
    0x01C2: 'Bicycle',
    0x01C3: 'Suite Key',
    0x01C4: 'Oak\'s Letter',
    0x01C5: 'Lunar Wing',
    0x01C6: 'Member Card',
    0x01C7: 'Azure Flute',
    0x01C8: 'S.S. Ticket',
    0x01C9: 'Contest Pass',
    0x01CA: 'Magma Stone',
    0x01CB: 'Parcel',
    0x01CC: 'Coupon 1',
    0x01CD: 'Coupon 2',
    0x01CE: 'Coupon 3',
    0x01CF: 'Storage Key',
    0x01D0: 'SecretPotion',
    0x01D1: 'Vs. Recorder',
    0x01D2: 'Gracidea',
    0x01D3: 'Secret Key',
    0x01D4: 'Apricorn Box',
    0x01D5: 'Unown Report',
    0x01D6: 'Berry Pots',
    0x01D7: 'Dowsing MCHN',
    0x01D8: 'Blue Card',
    0x01D9: 'Slowpoketail',
    0x01DA: 'Clear Bell',
    0x01DB: 'Card Key',
    0x01DC: 'Basement Key',
    0x01DD: 'Squirtbottle',
    0x01DE: 'Red Scale',
    0x01DF: 'Lost Item',
    0x01E0: 'Pass',
    0x01E1: 'Machine Part',
    0x01E2: 'Silver Wing',
    0x01E3: 'Rainbow Wing',
    0x01E4: 'Mystery Egg',
    0x01E5: 'Red Apricorn',
    0x01E6: 'Ylw Apricorn',
    0x01E7: 'Blu Apricorn',
    0x01E8: 'Grn Apricorn',
    0x01E9: 'Pnk Apricorn',
    0x01EA: 'Wht Apricorn',
    0x01EB: 'Blk Apricorn',
    0x01EC: 'Fast Ball',
    0x01ED: 'Level Ball',
    0x01EE: 'Lure Ball',
    0x01EF: 'Heavy Ball',
    0x01F0: 'Love Ball',
    0x01F1: 'Friend Ball',
    0x01F2: 'Moon Ball',
    0x01F3: 'Sport Ball',
    0x01F4: 'Park Ball',
    0x01F5: 'Photo Album',
    0x01F6: 'GB Sounds',
    0x01F7: 'Tidal Bell',
    0x01F8: 'RageCandyBar',
    0x01F9: 'Data Card 01',
    0x01FA: 'Data Card 02',
    0x01FB: 'Data Card 03',
    0x01FC: 'Data Card 04',
    0x01FD: 'Data Card 05',
    0x01FE: 'Data Card 06',
    0x01FF: 'Data Card 07',
    0x0200: 'Data Card 08',
    0x0201: 'Data Card 09',
    0x0202: 'Data Card 10',
    0x0203: 'Data Card 11',
    0x0204: 'Data Card 12',
    0x0205: 'Data Card 13',
    0x0206: 'Data Card 14',
    0x0207: 'Data Card 15',
    0x0208: 'Data Card 16',
    0x0209: 'Data Card 17',
    0x020A: 'Data Card 18',
    0x020B: 'Data Card 19',
    0x020C: 'Data Card 20',
    0x020D: 'Data Card 21',
    0x020E: 'Data Card 22',
    0x020F: 'Data Card 23',
    0x0210: 'Data Card 24',
    0x0211: 'Data Card 25',
    0x0212: 'Data Card 26',
    0x0213: 'Data Card 27',
    0x0214: 'Jade Orb',
    0x0215: 'Lock Capsule',
    0x0216: 'Red Orb',
    0x0217: 'Blue Orb',
    0x0218: 'Enigma Stone'
}

hptype = {
    0: 'Fighting',
    1: 'Flying',
    2: 'Poison',
    3: 'Ground',
    4: 'Rock',
    5: 'Bug',
    6: 'Ghost',
    7: 'Steel',
    8: 'Fire',
    9: 'Water',
    10: 'Grass',
    11: 'Electric',
    12: 'Psychic',
    13: 'Ice',
    14: 'Dragon',
    15: 'Dark'
}
