import namegen
import stats
from array import array
from datetime import date
from boxtoparty import makeparty

# TODO: remove file

def makends(gba):
    # Deconstructing GBA .3gpkm file
    pid = gba[0:4]
    otid = gba[4:8]
    nickname = convertname(gba[8:18])
    nickname = extendname(nickname, False)

    lang = gba[18]

    otname = convertname(gba[20:27])

    species = ord(gba[32]) + (ord(gba[33]) << 8)
    species = pokemonindex.get(species)

    gend = genderbyte(species, pid)
    forme = form(species, gend, pid)
    nicknamed = namegen.namegen(nickname) != stats.species.get(species).upper()
    ability = abilities.get(species)

    species = chr(species & 0xff) + chr((species >> 8) & 0xff)

    item = gba[34:36]

    exp = gba[36:40]

    ppup = ord(gba[40])
    ppupa = chr(ppup & 3)
    ppupb = chr((ppup >> 2) & 3)
    ppupc = chr((ppup >> 4) & 3)
    ppupd = chr((ppup >> 6) & 3)

    happy = gba[41]

    atk1 = gba[44:46]
    atk2 = gba[46:48]
    atk3 = gba[48:50]
    atk4 = gba[50:52]
    pp1 = gba[52]
    pp2 = gba[53]
    pp3 = gba[54]
    pp4 = gba[55]

    hpev = gba[56]
    atkev = gba[57]
    defev = gba[58]
    speev = gba[59]
    spaev = gba[60]
    spdev = gba[61]

    pkrs = gba[68]
    lvmet = ord(gba[70]) & 0x7f
    fmlot = ord(gba[71]) & 0x80
    ivs = gba[72:76]
    ribbons = gba[76:80]

    # Generating NDS .pkm file
    pkm = species + item + otid + exp + happy
    pkm += ability[ord(pid[0]) % 2]
    pkm += '\x00'      # Markings
    pkm += lang + hpev + atkev + defev + speev + spaev + spdev
    pkm += '\x00' * 10  # Contest values, Sinnoh ribbons
    pkm += atk1 + atk2 + atk3 + atk4 + pp1 + pp2 + pp3 + pp4
    pkm += ppupa + ppupb + ppupc + ppupd
    pkm += ivbytes(ivs, nicknamed)
    pkm += ribbons     # Hoenn ribbons
    pkm += chr(forme)
    pkm += '\x00' * 5 + '\x37\x00'  # Shiny leaves, padding, egg from, met at
    pkm += nickname
    pkm += '\x00\x03'  # Padding, hometown (Hoenn, Emerald)
    pkm += '\x00' * 8  # Sinnoh Ribbons, Padding
    pkm += extendname(otname, True, pkm[0x40:0x50])
    pkm += '\x00' * 3  # Date egg received
    pkm += datemet()
    pkm += '\x00' * 2  # Egg location
    pkm += '\x37\x00'  # Location met (Migrated from Emerald)
    pkm += pkrs
    pkm += '\x04'     # Poke ball
    pkm += chr(lvmet | fmlot)
    pkm += '\x00'     # Encounter type
    pkm += '\x04'     # Poke ball
    pkm += '\x00'     # Padding

    chksm = getsum(pkm)
    pkm = pid + '\x00\x00' + chksm + pkm
    return makeparty(pkm)


def convertname(n):
    bytes = array('B')
    bytes.fromstring(n)
    converted = ''

    for val in bytes:
        if val == 0xff:
            break
        c = name.get(val)
        if c:
            c = [k for k, v in namegen.namelist.iteritems() if v == c][0]
            converted += chr(c) + '\x01'

    converted += '\xff\xff'
    return converted


def extendname(n, ot, trash='\x00\x00\x00\x00\x00\x00\x00\x00\x42\x00\x00\x00\x00\x00\x00\x00\xc8\x19\x0c\x02\xe0\xff'):
    if ot:
        if len(n) < 16:
            n += trash[len(n):]
    else:
        if len(n) < 22:
            n += trash[len(n):]

    return n


def ivbytes(ivs, name):
    mod = ord(ivs[3])
    if name:
        mod = mod | 0x80

    return ivs[0:3] + chr(mod)


def genderbyte(species, pid):
    gid = ord(pid[0])
    genratio = gender.get(species)
    if genratio == 'Genderless':
        return 4
    elif genratio == '0 %':
        return 2
    elif genratio == '12.5 %':
        if gid < 223:
            return 2
        else:
            return 0
    elif genratio == '25 %':
        if gid < 191:
            return 2
        else:
            return 0
    elif genratio == '50 %':
        if gid < 127:
            return 2
        else:
            return 0
    elif genratio == '75 %':
        if gid < 63:
            return 2
        else:
            return 0
    elif genratio == '87.5 %':
        if gid < 31:
            return 2
        else:
            return 0
    elif genratio == '100 %':
        return 0


def form(id, gend, pid):
    if id == 201:
        letter1 = ord(pid[3]) & 3
        letter2 = ord(pid[2]) & 3
        letter3 = ord(pid[1]) & 3
        letter4 = ord(pid[0]) & 3
        letter = (letter1 << 6) + (letter2 << 4) + (letter3 << 2) + letter4
        return (unown.get(letter % 28) << 3) | gend
    elif id == 386:
        return (0x18 << 3) | gend
    else:
        return gend


def datemet():
    val = date.today()
    return chr(val.year - 2000) + chr(val.month) + chr(val.day)


def getsum(pkm):
    ar = array('H')
    ar.fromstring(pkm)
    sum = 0
    for val in ar:
        sum += val

    return chr(sum & 0xff) + chr((sum >> 8) & 0xff)


name = {
    0xa1: '0',
    0xa2: '1',
    0xa3: '2',
    0xa4: '3',
    0xa5: '4',
    0xa6: '5',
    0xa7: '6',
    0xa8: '7',
    0xa9: '8',
    0xaa: '9',
    0xbb: 'A',
    0xbc: 'B',
    0xbd: 'C',
    0xbe: 'D',
    0xbf: 'E',
    0xc0: 'F',
    0xc1: 'G',
    0xc2: 'H',
    0xc3: 'I',
    0xc4: 'J',
    0xc5: 'K',
    0xc6: 'L',
    0xc7: 'M',
    0xc8: 'N',
    0xc9: 'O',
    0xca: 'P',
    0xcb: 'Q',
    0xcc: 'R',
    0xcd: 'S',
    0xce: 'T',
    0xcf: 'U',
    0xd0: 'V',
    0xd1: 'W',
    0xd2: 'X',
    0xd3: 'Y',
    0xd4: 'Z',
    0xd5: 'a',
    0xd6: 'b',
    0xd7: 'c',
    0xd8: 'd',
    0xd9: 'e',
    0xda: 'f',
    0xdb: 'g',
    0xdc: 'h',
    0xdd: 'i',
    0xde: 'j',
    0xdf: 'k',
    0xe0: 'l',
    0xe1: 'm',
    0xe2: 'n',
    0xe3: 'o',
    0xe4: 'p',
    0xe5: 'q',
    0xe6: 'r',
    0xe7: 's',
    0xe8: 't',
    0xe9: 'u',
    0xea: 'v',
    0xeb: 'w',
    0xec: 'x',
    0xed: 'y',
    0xee: 'z'
}
abilities = {
    1: ('\x41', '\x41'),
    2: ('\x41', '\x41'),
    3: ('\x41', '\x41'),
    4: ('\x42', '\x42'),
    5: ('\x42', '\x42'),
    6: ('\x42', '\x42'),
    7: ('\x43', '\x43'),
    8: ('\x43', '\x43'),
    9: ('\x43', '\x43'),
    10: ('\x13', '\x13'),
    11: ('\x3d', '\x3d'),
    12: ('\x0e', '\x0e'),
    13: ('\x13', '\x13'),
    14: ('\x3d', '\x3d'),
    15: ('\x44', '\x44'),
    16: ('\x33', '\x33'),
    17: ('\x33', '\x33'),
    18: ('\x33', '\x33'),
    19: ('\x32', '\x3e'),
    20: ('\x32', '\x3e'),
    21: ('\x33', '\x33'),
    22: ('\x33', '\x33'),
    23: ('\x3d', '\x16'),
    24: ('\x3d', '\x16'),
    25: ('\x09', '\x09'),
    26: ('\x09', '\x09'),
    27: ('\x08', '\x08'),
    28: ('\x08', '\x08'),
    29: ('\x26', '\x26'),
    30: ('\x26', '\x26'),
    31: ('\x26', '\x26'),
    32: ('\x26', '\x26'),
    33: ('\x26', '\x26'),
    34: ('\x26', '\x26'),
    35: ('\x38', '\x38'),
    36: ('\x38', '\x38'),
    37: ('\x12', '\x12'),
    38: ('\x12', '\x12'),
    39: ('\x38', '\x38'),
    40: ('\x38', '\x38'),
    41: ('\x27', '\x27'),
    42: ('\x27', '\x27'),
    43: ('\x22', '\x22'),
    44: ('\x22', '\x22'),
    45: ('\x22', '\x22'),
    46: ('\x1b', '\x1b'),
    47: ('\x1b', '\x1b'),
    48: ('\x0e', '\x0e'),
    49: ('\x13', '\x13'),
    50: ('\x08', '\x47'),
    51: ('\x08', '\x47'),
    52: ('\x35', '\x35'),
    53: ('\x07', '\x07'),
    54: ('\x06', '\x0d'),
    55: ('\x06', '\x0d'),
    56: ('\x48', '\x48'),
    57: ('\x48', '\x48'),
    58: ('\x16', '\x12'),
    59: ('\x16', '\x12'),
    60: ('\x06', '\x0b'),
    61: ('\x06', '\x0b'),
    62: ('\x06', '\x0b'),
    63: ('\x1c', '\x27'),
    64: ('\x1c', '\x27'),
    65: ('\x1c', '\x27'),
    66: ('\x3e', '\x3e'),
    67: ('\x3e', '\x3e'),
    68: ('\x3e', '\x3e'),
    69: ('\x22', '\x22'),
    70: ('\x22', '\x22'),
    71: ('\x22', '\x22'),
    72: ('\x1d', '\x40'),
    73: ('\x1d', '\x40'),
    74: ('\x45', '\x05'),
    75: ('\x45', '\x05'),
    76: ('\x45', '\x05'),
    77: ('\x32', '\x12'),
    78: ('\x32', '\x12'),
    79: ('\x0c', '\x14'),
    80: ('\x0c', '\x14'),
    81: ('\x2a', '\x05'),
    82: ('\x2a', '\x05'),
    83: ('\x33', '\x27'),
    84: ('\x32', '\x30'),
    85: ('\x32', '\x30'),
    86: ('\x2f', '\x2f'),
    87: ('\x2f', '\x2f'),
    88: ('\x01', '\x3c'),
    89: ('\x01', '\x3c'),
    90: ('\x4b', '\x4b'),
    91: ('\x4b', '\x4b'),
    92: ('\x1a', '\x1a'),
    93: ('\x1a', '\x1a'),
    94: ('\x1a', '\x1a'),
    95: ('\x45', '\x05'),
    96: ('\x0f', '\x0f'),
    97: ('\x0f', '\x0f'),
    98: ('\x34', '\x4b'),
    99: ('\x34', '\x4b'),
    100: ('\x2b', '\x09'),
    101: ('\x2b', '\x09'),
    102: ('\x22', '\x22'),
    103: ('\x22', '\x22'),
    104: ('\x45', '\x1f'),
    105: ('\x45', '\x1f'),
    106: ('\x07', '\x07'),
    107: ('\x33', '\x33'),
    108: ('\x0c', '\x14'),
    109: ('\x1a', '\x1a'),
    110: ('\x1a', '\x1a'),
    111: ('\x45', '\x1f'),
    112: ('\x45', '\x1f'),
    113: ('\x1e', '\x20'),
    114: ('\x22', '\x22'),
    115: ('\x30', '\x30'),
    116: ('\x21', '\x21'),
    117: ('\x26', '\x26'),
    118: ('\x21', '\x29'),
    119: ('\x21', '\x29'),
    120: ('\x23', '\x1e'),
    121: ('\x23', '\x1e'),
    122: ('\x2b', '\x2b'),
    123: ('\x44', '\x44'),
    124: ('\x0c', '\x0c'),
    125: ('\x09', '\x09'),
    126: ('\x31', '\x31'),
    127: ('\x34', '\x34'),
    128: ('\x16', '\x16'),
    129: ('\x21', '\x21'),
    130: ('\x16', '\x16'),
    131: ('\x0b', '\x4b'),
    132: ('\x07', '\x07'),
    133: ('\x32', '\x32'),
    134: ('\x0b', '\x0b'),
    135: ('\x0a', '\x0a'),
    136: ('\x12', '\x12'),
    137: ('\x24', '\x24'),
    138: ('\x21', '\x4b'),
    139: ('\x21', '\x4b'),
    140: ('\x21', '\x04'),
    141: ('\x21', '\x04'),
    142: ('\x45', '\x2e'),
    143: ('\x11', '\x2f'),
    144: ('\x2e', '\x2e'),
    145: ('\x2e', '\x2e'),
    146: ('\x2e', '\x2e'),
    147: ('\x3d', '\x3d'),
    148: ('\x3d', '\x3d'),
    149: ('\x27', '\x27'),
    150: ('\x2e', '\x2e'),
    151: ('\x1c', '\x1c'),
    152: ('\x41', '\x41'),
    153: ('\x41', '\x41'),
    154: ('\x41', '\x41'),
    155: ('\x42', '\x42'),
    156: ('\x42', '\x42'),
    157: ('\x42', '\x42'),
    158: ('\x43', '\x43'),
    159: ('\x43', '\x43'),
    160: ('\x43', '\x43'),
    161: ('\x32', '\x33'),
    162: ('\x32', '\x33'),
    163: ('\x0f', '\x33'),
    164: ('\x0f', '\x33'),
    165: ('\x44', '\x30'),
    166: ('\x44', '\x30'),
    167: ('\x0f', '\x44'),
    168: ('\x0f', '\x44'),
    169: ('\x27', '\x27'),
    170: ('\x0a', '\x23'),
    171: ('\x0a', '\x23'),
    172: ('\x09', '\x09'),
    173: ('\x38', '\x38'),
    174: ('\x38', '\x38'),
    175: ('\x37', '\x20'),
    176: ('\x37', '\x20'),
    177: ('\x1c', '\x30'),
    178: ('\x1c', '\x30'),
    179: ('\x09', '\x09'),
    180: ('\x09', '\x09'),
    181: ('\x09', '\x09'),
    182: ('\x22', '\x22'),
    183: ('\x2f', '\x25'),
    184: ('\x2f', '\x25'),
    185: ('\x45', '\x05'),
    186: ('\x06', '\x0b'),
    187: ('\x22', '\x22'),
    188: ('\x22', '\x22'),
    189: ('\x22', '\x22'),
    190: ('\x32', '\x35'),
    191: ('\x22', '\x22'),
    192: ('\x22', '\x22'),
    193: ('\x03', '\x0e'),
    194: ('\x06', '\x0b'),
    195: ('\x06', '\x0b'),
    196: ('\x1c', '\x1c'),
    197: ('\x1c', '\x1c'),
    198: ('\x0f', '\x0f'),
    199: ('\x0c', '\x14'),
    200: ('\x1a', '\x1a'),
    201: ('\x1a', '\x1a'),
    202: ('\x17', '\x17'),
    203: ('\x27', '\x30'),
    204: ('\x05', '\x05'),
    205: ('\x05', '\x05'),
    206: ('\x20', '\x32'),
    207: ('\x08', '\x34'),
    208: ('\x45', '\x05'),
    209: ('\x16', '\x32'),
    210: ('\x16', '\x16'),
    211: ('\x21', '\x26'),
    212: ('\x44', '\x44'),
    213: ('\x05', '\x05'),
    214: ('\x44', '\x3e'),
    215: ('\x27', '\x33'),
    216: ('\x35', '\x35'),
    217: ('\x3e', '\x3e'),
    218: ('\x28', '\x31'),
    219: ('\x28', '\x31'),
    220: ('\x0c', '\x0c'),
    221: ('\x0c', '\x0c'),
    222: ('\x37', '\x1e'),
    223: ('\x37', '\x37'),
    224: ('\x15', '\x15'),
    225: ('\x37', '\x48'),
    226: ('\x21', '\x0b'),
    227: ('\x33', '\x05'),
    228: ('\x30', '\x12'),
    229: ('\x30', '\x12'),
    230: ('\x21', '\x21'),
    231: ('\x35', '\x35'),
    232: ('\x05', '\x05'),
    233: ('\x24', '\x24'),
    234: ('\x16', '\x16'),
    235: ('\x14', '\x14'),
    236: ('\x3e', '\x3e'),
    237: ('\x16', '\x16'),
    238: ('\x0c', '\x0c'),
    239: ('\x09', '\x09'),
    240: ('\x31', '\x31'),
    241: ('\x2f', '\x2f'),
    242: ('\x1e', '\x20'),
    243: ('\x2e', '\x2e'),
    244: ('\x2e', '\x2e'),
    245: ('\x2e', '\x2e'),
    246: ('\x3e', '\x3e'),
    247: ('\x3d', '\x3d'),
    248: ('\x2d', '\x2d'),
    249: ('\x2e', '\x2e'),
    250: ('\x2e', '\x2e'),
    251: ('\x1e', '\x1e'),
    252: ('\x41', '\x41'),
    253: ('\x41', '\x41'),
    254: ('\x41', '\x41'),
    255: ('\x42', '\x42'),
    256: ('\x42', '\x42'),
    257: ('\x42', '\x42'),
    258: ('\x43', '\x43'),
    259: ('\x43', '\x43'),
    260: ('\x43', '\x43'),
    261: ('\x32', '\x32'),
    262: ('\x16', '\x16'),
    263: ('\x35', '\x35'),
    264: ('\x35', '\x35'),
    265: ('\x13', '\x13'),
    266: ('\x3d', '\x3d'),
    267: ('\x44', '\x44'),
    268: ('\x3d', '\x3d'),
    269: ('\x13', '\x13'),
    270: ('\x21', '\x2c'),
    271: ('\x21', '\x2c'),
    272: ('\x21', '\x2c'),
    273: ('\x22', '\x30'),
    274: ('\x22', '\x30'),
    275: ('\x22', '\x30'),
    276: ('\x3e', '\x3e'),
    277: ('\x3e', '\x3e'),
    278: ('\x33', '\x33'),
    279: ('\x33', '\x33'),
    280: ('\x1c', '\x24'),
    281: ('\x1c', '\x24'),
    282: ('\x1c', '\x24'),
    283: ('\x21', '\x21'),
    284: ('\x16', '\x16'),
    285: ('\x1b', '\x1b'),
    286: ('\x1b', '\x1b'),
    287: ('\x36', '\x36'),
    288: ('\x48', '\x48'),
    289: ('\x36', '\x36'),
    290: ('\x0e', '\x0e'),
    291: ('\x03', '\x03'),
    292: ('\x19', '\x19'),
    293: ('\x2b', '\x2b'),
    294: ('\x2b', '\x2b'),
    295: ('\x2b', '\x2b'),
    296: ('\x2f', '\x3e'),
    297: ('\x2f', '\x3e'),
    298: ('\x2f', '\x3e'),
    299: ('\x05', '\x2a'),
    300: ('\x38', '\x38'),
    301: ('\x38', '\x38'),
    302: ('\x33', '\x33'),
    303: ('\x34', '\x16'),
    304: ('\x45', '\x05'),
    305: ('\x45', '\x05'),
    306: ('\x45', '\x05'),
    307: ('\x4a', '\x4a'),
    308: ('\x4a', '\x4a'),
    309: ('\x09', '\x1f'),
    310: ('\x09', '\x1f'),
    311: ('\x39', '\x39'),
    312: ('\x3a', '\x3a'),
    313: ('\x23', '\x44'),
    314: ('\x0c', '\x0c'),
    315: ('\x1e', '\x26'),
    316: ('\x40', '\x3c'),
    317: ('\x40', '\x3c'),
    318: ('\x18', '\x18'),
    319: ('\x18', '\x18'),
    320: ('\x29', '\x0c'),
    321: ('\x29', '\x0c'),
    322: ('\x0c', '\x0c'),
    323: ('\x28', '\x28'),
    324: ('\x49', '\x49'),
    325: ('\x2f', '\x14'),
    326: ('\x2f', '\x14'),
    327: ('\x14', '\x14'),
    328: ('\x34', '\x47'),
    329: ('\x1a', '\x1a'),
    330: ('\x1a', '\x1a'),
    331: ('\x08', '\x08'),
    332: ('\x08', '\x08'),
    333: ('\x1e', '\x1e'),
    334: ('\x1e', '\x1e'),
    335: ('\x11', '\x11'),
    336: ('\x3d', '\x3d'),
    337: ('\x1a', '\x1a'),
    338: ('\x1a', '\x1a'),
    339: ('\x0c', '\x0c'),
    340: ('\x0c', '\x0c'),
    341: ('\x34', '\x4b'),
    342: ('\x34', '\x4b'),
    343: ('\x1a', '\x1a'),
    344: ('\x1a', '\x1a'),
    345: ('\x15', '\x15'),
    346: ('\x15', '\x15'),
    347: ('\x04', '\x04'),
    348: ('\x04', '\x04'),
    349: ('\x21', '\x21'),
    350: ('\x3f', '\x3f'),
    351: ('\x3b', '\x3b'),
    352: ('\x10', '\x10'),
    353: ('\x0f', '\x0f'),
    354: ('\x0f', '\x0f'),
    355: ('\x1a', '\x1a'),
    356: ('\x2e', '\x2e'),
    357: ('\x22', '\x22'),
    358: ('\x1a', '\x1a'),
    359: ('\x2e', '\x2e'),
    360: ('\x17', '\x17'),
    361: ('\x27', '\x27'),
    362: ('\x27', '\x27'),
    363: ('\x2f', '\x2f'),
    364: ('\x2f', '\x2f'),
    365: ('\x2f', '\x2f'),
    366: ('\x4b', '\x4b'),
    367: ('\x21', '\x21'),
    368: ('\x21', '\x21'),
    369: ('\x21', '\x45'),
    370: ('\x21', '\x21'),
    371: ('\x45', '\x45'),
    372: ('\x45', '\x45'),
    373: ('\x16', '\x16'),
    374: ('\x1d', '\x1d'),
    375: ('\x1d', '\x1d'),
    376: ('\x1d', '\x1d'),
    377: ('\x1d', '\x1d'),
    378: ('\x1d', '\x1d'),
    379: ('\x1d', '\x1d'),
    380: ('\x1a', '\x1a'),
    381: ('\x1a', '\x1a'),
    382: ('\x02', '\x02'),
    383: ('\x46', '\x46'),
    384: ('\x4c', '\x4c'),
    385: ('\x20', '\x20'),
    386: ('\x2e', '\x2e')
}

gender = {
    1: '87.5 %',
    2: '87.5 %',
    3: '87.5 %',
    4: '87.5 %',
    5: '87.5 %',
    6: '87.5 %',
    7: '87.5 %',
    8: '87.5 %',
    9: '87.5 %',
    10: '50 %',
    11: '50 %',
    12: '50 %',
    13: '50 %',
    14: '50 %',
    15: '50 %',
    16: '50 %',
    17: '50 %',
    18: '50 %',
    19: '50 %',
    20: '50 %',
    21: '50 %',
    22: '50 %',
    23: '50 %',
    24: '50 %',
    25: '50 %',
    26: '50 %',
    27: '50 %',
    28: '50 %',
    29: '0 %',
    30: '0 %',
    31: '0 %',
    32: '100 %',
    33: '100 %',
    34: '100 %',
    35: '25 %',
    36: '25 %',
    37: '25 %',
    38: '25 %',
    39: '25 %',
    40: '25 %',
    41: '50 %',
    42: '50 %',
    43: '50 %',
    44: '50 %',
    45: '50 %',
    46: '50 %',
    47: '50 %',
    48: '50 %',
    49: '50 %',
    50: '50 %',
    51: '50 %',
    52: '50 %',
    53: '50 %',
    54: '50 %',
    55: '50 %',
    56: '50 %',
    57: '50 %',
    58: '75 %',
    59: '75 %',
    60: '50 %',
    61: '50 %',
    62: '50 %',
    63: '75 %',
    64: '75 %',
    65: '75 %',
    66: '75 %',
    67: '75 %',
    68: '75 %',
    69: '50 %',
    70: '50 %',
    71: '50 %',
    72: '50 %',
    73: '50 %',
    74: '50 %',
    75: '50 %',
    76: '50 %',
    77: '50 %',
    78: '50 %',
    79: '50 %',
    80: '50 %',
    81: '0 %',
    82: '0 %',
    83: '50 %',
    84: '50 %',
    85: '50 %',
    86: '50 %',
    87: '50 %',
    88: '50 %',
    89: '50 %',
    90: '50 %',
    91: '50 %',
    92: '50 %',
    93: '50 %',
    94: '50 %',
    95: '50 %',
    96: '50 %',
    97: '50 %',
    98: '50 %',
    99: '50 %',
    100: '0 %',
    101: '0 %',
    102: '50 %',
    103: '50 %',
    104: '50 %',
    105: '50 %',
    106: '100 %',
    107: '100 %',
    108: '50 %',
    109: '50 %',
    110: '50 %',
    111: '50 %',
    112: '50 %',
    113: '0 %',
    114: '50 %',
    115: '0 %',
    116: '50 %',
    117: '50 %',
    118: '50 %',
    119: '50 %',
    120: '0 %',
    121: '0 %',
    122: '50 %',
    123: '50 %',
    124: '0 %',
    125: '75 %',
    126: '75 %',
    127: '50 %',
    128: '100 %',
    129: '50 %',
    130: '50 %',
    131: '50 %',
    132: '0 %',
    133: '87.5 %',
    134: '87.5 %',
    135: '87.5 %',
    136: '87.5 %',
    137: '0 %',
    138: '87.5 %',
    139: '87.5 %',
    140: '87.5 %',
    141: '87.5 %',
    142: '87.5 %',
    143: '87.5 %',
    144: '0 %',
    145: '0 %',
    146: '0 %',
    147: '50 %',
    148: '50 %',
    149: '50 %',
    150: '0 %',
    151: '0 %',
    152: '87.5 %',
    153: '87.5 %',
    154: '87.5 %',
    155: '87.5 %',
    156: '87.5 %',
    157: '87.5 %',
    158: '87.5 %',
    159: '87.5 %',
    160: '87.5 %',
    161: '50 %',
    162: '50 %',
    163: '50 %',
    164: '50 %',
    165: '50 %',
    166: '50 %',
    167: '50 %',
    168: '50 %',
    169: '50 %',
    170: '50 %',
    171: '50 %',
    172: '50 %',
    173: '25 %',
    174: '25 %',
    175: '87.5 %',
    176: '87.5 %',
    177: '50 %',
    178: '50 %',
    179: '50 %',
    180: '50 %',
    181: '50 %',
    182: '50 %',
    183: '50 %',
    184: '50 %',
    185: '50 %',
    186: '50 %',
    187: '50 %',
    188: '50 %',
    189: '50 %',
    190: '50 %',
    191: '50 %',
    192: '50 %',
    193: '50 %',
    194: '50 %',
    195: '50 %',
    196: '87.5 %',
    197: '87.5 %',
    198: '50 %',
    199: '50 %',
    200: '50 %',
    201: '0 %',
    202: '50 %',
    203: '50 %',
    204: '50 %',
    205: '50 %',
    206: '50 %',
    207: '50 %',
    208: '50 %',
    209: '25 %',
    210: '25 %',
    211: '50 %',
    212: '50 %',
    213: '50 %',
    214: '50 %',
    215: '50 %',
    216: '50 %',
    217: '50 %',
    218: '50 %',
    219: '50 %',
    220: '50 %',
    221: '50 %',
    222: '25 %',
    223: '50 %',
    224: '50 %',
    225: '50 %',
    226: '50 %',
    227: '50 %',
    228: '50 %',
    229: '50 %',
    230: '50 %',
    231: '50 %',
    232: '50 %',
    233: '0 %',
    234: '50 %',
    235: '50 %',
    236: '100 %',
    237: '100 %',
    238: '0 %',
    239: '75 %',
    240: '75 %',
    241: '0 %',
    242: '0 %',
    243: '0 %',
    244: '0 %',
    245: '0 %',
    246: '50 %',
    247: '50 %',
    248: '50 %',
    249: '0 %',
    250: '0 %',
    251: '0 %',
    252: '87.5 %',
    253: '87.5 %',
    254: '87.5 %',
    255: '87.5 %',
    256: '87.5 %',
    257: '87.5 %',
    258: '87.5 %',
    259: '87.5 %',
    260: '87.5 %',
    261: '50 %',
    262: '50 %',
    263: '50 %',
    264: '50 %',
    265: '50 %',
    266: '50 %',
    267: '50 %',
    268: '50 %',
    269: '50 %',
    270: '50 %',
    271: '50 %',
    272: '50 %',
    273: '50 %',
    274: '50 %',
    275: '50 %',
    276: '50 %',
    277: '50 %',
    278: '50 %',
    279: '50 %',
    280: '50 %',
    281: '50 %',
    282: '50 %',
    283: '50 %',
    284: '50 %',
    285: '50 %',
    286: '50 %',
    287: '50 %',
    288: '50 %',
    289: '50 %',
    290: '50 %',
    291: '50 %',
    292: '0 %',
    293: '50 %',
    294: '50 %',
    295: '50 %',
    296: '75 %',
    297: '75 %',
    298: '75 %',
    299: '50 %',
    300: '25 %',
    301: '25 %',
    302: '50 %',
    303: '50 %',
    304: '50 %',
    305: '50 %',
    306: '50 %',
    307: '50 %',
    308: '50 %',
    309: '50 %',
    310: '50 %',
    311: '50 %',
    312: '50 %',
    313: '100 %',
    314: '0 %',
    315: '50 %',
    316: '50 %',
    317: '50 %',
    318: '50 %',
    319: '50 %',
    320: '50 %',
    321: '50 %',
    322: '50 %',
    323: '50 %',
    324: '50 %',
    325: '50 %',
    326: '50 %',
    327: '50 %',
    328: '50 %',
    329: '50 %',
    330: '50 %',
    331: '50 %',
    332: '50 %',
    333: '50 %',
    334: '50 %',
    335: '50 %',
    336: '50 %',
    337: '0 %',
    338: '0 %',
    339: '50 %',
    340: '50 %',
    341: '50 %',
    342: '50 %',
    343: '0 %',
    344: '0 %',
    345: '87.5 %',
    346: '87.5 %',
    347: '87.5 %',
    348: '87.5 %',
    349: '50 %',
    350: '50 %',
    351: '50 %',
    352: '50 %',
    353: '50 %',
    354: '50 %',
    355: '50 %',
    356: '50 %',
    357: '50 %',
    358: '50 %',
    359: '50 %',
    360: '50 %',
    361: '50 %',
    362: '50 %',
    363: '50 %',
    364: '50 %',
    365: '50 %',
    366: '50 %',
    367: '50 %',
    368: '50 %',
    369: '87.5 %',
    370: '25 %',
    371: '50 %',
    372: '50 %',
    373: '50 %',
    374: '0 %',
    375: '0 %',
    376: '0 %',
    377: '0 %',
    378: '0 %',
    379: '0 %',
    380: '0 %',
    381: '100 %',
    382: '0 %',
    383: '0 %',
    384: '0 %',
    385: '0 %',
    386: 'Genderless'
}

unown = {
    0: 0x00,
    1: 0x08,
    2: 0x10,
    3: 0x18,
    4: 0x20,
    5: 0x28,
    6: 0x30,
    7: 0x38,
    8: 0x40,
    9: 0x48,
    10: 0x50,
    11: 0x58,
    12: 0x60,
    13: 0x68,
    14: 0x70,
    15: 0x78,
    16: 0x80,
    17: 0x88,
    18: 0x90,
    19: 0x98,
    20: 0xa0,
    21: 0xa8,
    22: 0xb0,
    23: 0xb8,
    24: 0xc0,
    25: 0xc8,
    26: 0xd0,
    27: 0xd8
}

pokemonindex = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
    16: 16,
    17: 17,
    18: 18,
    19: 19,
    20: 20,
    21: 21,
    22: 22,
    23: 23,
    24: 24,
    25: 25,
    26: 26,
    27: 27,
    28: 28,
    29: 29,
    30: 30,
    31: 31,
    32: 32,
    33: 33,
    34: 34,
    35: 35,
    36: 36,
    37: 37,
    38: 38,
    39: 39,
    40: 40,
    41: 41,
    42: 42,
    43: 43,
    44: 44,
    45: 45,
    46: 46,
    47: 47,
    48: 48,
    49: 49,
    50: 50,
    51: 51,
    52: 52,
    53: 53,
    54: 54,
    55: 55,
    56: 56,
    57: 57,
    58: 58,
    59: 59,
    60: 60,
    61: 61,
    62: 62,
    63: 63,
    64: 64,
    65: 65,
    66: 66,
    67: 67,
    68: 68,
    69: 69,
    70: 70,
    71: 71,
    72: 72,
    73: 73,
    74: 74,
    75: 75,
    76: 76,
    77: 77,
    78: 77,
    79: 79,
    80: 80,
    81: 81,
    82: 82,
    83: 83,
    84: 84,
    85: 85,
    86: 86,
    87: 87,
    88: 88,
    89: 89,
    90: 90,
    91: 91,
    92: 92,
    93: 93,
    94: 94,
    95: 95,
    96: 96,
    97: 97,
    98: 98,
    99: 99,
    100: 100,
    101: 101,
    102: 102,
    103: 103,
    104: 104,
    105: 105,
    106: 106,
    107: 107,
    108: 108,
    109: 109,
    110: 110,
    111: 111,
    112: 112,
    113: 113,
    114: 114,
    115: 115,
    116: 116,
    117: 117,
    118: 118,
    119: 119,
    120: 120,
    121: 121,
    122: 122,
    123: 123,
    124: 124,
    125: 125,
    126: 126,
    127: 127,
    128: 128,
    129: 129,
    130: 130,
    131: 131,
    132: 132,
    133: 133,
    134: 134,
    135: 135,
    136: 136,
    137: 137,
    138: 138,
    139: 139,
    140: 140,
    141: 141,
    142: 14,
    143: 14,
    144: 14,
    145: 145,
    146: 146,
    147: 147,
    148: 148,
    149: 149,
    150: 150,
    151: 151,
    152: 152,
    153: 153,
    154: 154,
    155: 155,
    156: 156,
    157: 157,
    158: 158,
    159: 159,
    160: 160,
    161: 161,
    162: 162,
    163: 163,
    164: 164,
    165: 165,
    166: 166,
    167: 167,
    168: 168,
    169: 169,
    170: 170,
    171: 171,
    172: 172,
    173: 173,
    174: 174,
    175: 175,
    176: 176,
    177: 177,
    178: 178,
    179: 179,
    180: 180,
    181: 181,
    182: 182,
    183: 183,
    184: 184,
    185: 185,
    186: 186,
    187: 187,
    188: 188,
    189: 189,
    190: 190,
    191: 191,
    192: 192,
    193: 193,
    194: 194,
    195: 195,
    196: 196,
    197: 197,
    198: 198,
    199: 199,
    200: 200,
    201: 201,
    202: 202,
    203: 203,
    204: 204,
    205: 205,
    206: 206,
    207: 207,
    208: 208,
    209: 209,
    210: 210,
    211: 211,
    212: 212,
    213: 213,
    214: 214,
    215: 215,
    216: 216,
    217: 217,
    218: 218,
    219: 219,
    220: 220,
    221: 221,
    222: 222,
    223: 223,
    224: 224,
    225: 225,
    226: 226,
    227: 227,
    228: 228,
    229: 229,
    230: 230,
    231: 231,
    232: 232,
    233: 233,
    234: 234,
    235: 235,
    236: 236,
    237: 237,
    238: 238,
    239: 239,
    240: 240,
    241: 241,
    242: 242,
    243: 243,
    244: 244,
    245: 245,
    246: 246,
    247: 247,
    248: 248,
    249: 249,
    250: 250,
    251: 251,
    277: 252,
    278: 253,
    279: 254,
    280: 255,
    281: 256,
    282: 257,
    283: 258,
    284: 259,
    285: 260,
    286: 261,
    287: 262,
    288: 263,
    289: 264,
    290: 265,
    291: 266,
    292: 267,
    293: 268,
    294: 269,
    295: 270,
    296: 271,
    297: 272,
    298: 273,
    299: 274,
    300: 275,
    301: 290,
    302: 291,
    303: 292,
    304: 276,
    305: 277,
    306: 285,
    307: 286,
    308: 327,
    309: 278,
    310: 279,
    311: 283,
    312: 284,
    313: 320,
    314: 321,
    315: 300,
    316: 301,
    317: 352,
    318: 343,
    319: 344,
    320: 299,
    321: 324,
    322: 302,
    323: 339,
    324: 340,
    325: 370,
    326: 341,
    327: 342,
    328: 349,
    329: 350,
    330: 318,
    331: 319,
    332: 328,
    333: 329,
    334: 330,
    335: 296,
    336: 297,
    337: 309,
    338: 310,
    339: 322,
    340: 323,
    341: 363,
    342: 364,
    343: 365,
    344: 331,
    345: 332,
    346: 361,
    347: 362,
    348: 337,
    349: 338,
    350: 298,
    351: 325,
    352: 326,
    353: 311,
    354: 312,
    355: 303,
    356: 307,
    357: 308,
    358: 333,
    359: 334,
    360: 360,
    361: 355,
    362: 356,
    363: 315,
    364: 287,
    365: 288,
    366: 289,
    367: 316,
    368: 317,
    369: 357,
    370: 293,
    371: 294,
    372: 295,
    373: 366,
    374: 367,
    375: 368,
    376: 359,
    377: 353,
    378: 354,
    379: 336,
    380: 335,
    381: 369,
    382: 304,
    383: 305,
    384: 306,
    385: 351,
    386: 313,
    387: 314,
    388: 345,
    389: 346,
    390: 347,
    391: 348,
    392: 280,
    393: 281,
    394: 282,
    395: 371,
    396: 372,
    397: 373,
    398: 374,
    399: 375,
    400: 376,
    401: 377,
    402: 378,
    403: 379,
    404: 382,
    405: 383,
    406: 384,
    407: 380,
    408: 381,
    409: 385,
    410: 386,
    411: 358
}
