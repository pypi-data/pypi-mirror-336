SEED = 1250390.0

HASH_MIXING_CONSTANT = 0x85ebca6b

# Prime numbers so they won't loop in a short interval
# Make sure the smallest is a big number because if any other number can loop that amount to form an interval
PRIME_1 = 4294967197
PRIME_2 = 4294967231
PRIME_3 = 4294967279
PRIME_4 = 4294967291
PRIME_5 = 4294967311


def random_1f1(x : float, scale : float = 1.0, seed : float = SEED) -> float:
    hash = int(PRIME_1 * seed + PRIME_2 * x * scale)
    
    hash ^= (hash >> 13)
    hash *= HASH_MIXING_CONSTANT
    hash ^= (hash >> 16)

    return (hash & 0x7FFFFFFF) / 0x7FFFFFFF


def random_2f1(x : float, y : float, scale : float = 1.0, seed : float = SEED) -> float:
    hash = int(PRIME_1 * seed + PRIME_2 * x * scale + PRIME_3 * y * scale)
    
    hash ^= (hash >> 13)
    hash *= HASH_MIXING_CONSTANT
    hash ^= (hash >> 16)

    return (hash & 0x7FFFFFFF) / 0x7FFFFFFF

def random_2f2(x : float, y : float, scale : float = 1000, seed : float = SEED) -> tuple[float, float]:
    hash_1 = int(PRIME_1 * seed + PRIME_2 * x * scale + PRIME_3 * y * scale)
    
    hash_1 ^= (hash_1 >> 13)
    hash_1 *= HASH_MIXING_CONSTANT
    hash_1 ^= (hash_1 >> 16)

    hash_2 = int(PRIME_1 * seed + PRIME_4 * x * scale + PRIME_5 * y * scale)
    
    hash_2 ^= (hash_2 >> 13)
    hash_2 *= HASH_MIXING_CONSTANT
    hash_2 ^= (hash_2 >> 16)
    return ((hash_1 & 0x7FFFFFFF) / 0x7FFFFFFF, (hash_2 & 0x7FFFFFFF) / 0x7FFFFFFF)

def random_1f2(x : float, scale : float = 1000, seed : float = SEED) -> tuple[float, float]:
    hash_1 = int(PRIME_1 * seed + PRIME_2 * x * scale)
    
    hash_1 ^= (hash_1 >> 13)
    hash_1 *= HASH_MIXING_CONSTANT
    hash_1 ^= (hash_1 >> 16)

    hash_2 = int(PRIME_1 * seed + PRIME_3 * x * scale)
    
    hash_2 ^= (hash_2 >> 13)
    hash_2 *= HASH_MIXING_CONSTANT
    hash_2 ^= (hash_2 >> 16)

    return ((hash_1 & 0x7FFFFFFF) / 0x7FFFFFFF, (hash_2 & 0x7FFFFFFF) / 0x7FFFFFFF)

def random_1f3(x : float, scale : float = 1000, seed : float = SEED) -> tuple[float, float]:
    hash_1 = int(PRIME_1 * seed + PRIME_2 * x * scale)
    
    hash_1 ^= (hash_1 >> 13)
    hash_1 *= HASH_MIXING_CONSTANT
    hash_1 ^= (hash_1 >> 16)

    hash_2 = int(PRIME_1 * seed + PRIME_3 * x * scale)
    
    hash_2 ^= (hash_2 >> 13)
    hash_2 *= HASH_MIXING_CONSTANT
    hash_2 ^= (hash_2 >> 16)

    hash_3 = int(PRIME_1 * seed + PRIME_4 * x * scale)
    
    hash_3 ^= (hash_2 >> 13)
    hash_3 *= HASH_MIXING_CONSTANT
    hash_3 ^= (hash_2 >> 16)

    return ((hash_1 & 0x7FFFFFFF) / 0x7FFFFFFF, (hash_2 & 0x7FFFFFFF) / 0x7FFFFFFF, (hash_3 & 0x7FFFFFFF) / 0x7FFFFFFF)

def random_1f4(x : float, scale : float = 1000, seed : float = SEED) -> tuple[float, float]:
    hash_1 = int(PRIME_1 * seed + PRIME_2 * x * scale)
    
    hash_1 ^= (hash_1 >> 13)
    hash_1 *= HASH_MIXING_CONSTANT
    hash_1 ^= (hash_1 >> 16)

    hash_2 = int(PRIME_1 * seed + PRIME_3 * x * scale)
    
    hash_2 ^= (hash_2 >> 13)
    hash_2 *= HASH_MIXING_CONSTANT
    hash_2 ^= (hash_2 >> 16)

    hash_3 = int(PRIME_1 * seed + PRIME_4 * x * scale)
    
    hash_3 ^= (hash_2 >> 13)
    hash_3 *= HASH_MIXING_CONSTANT
    hash_3 ^= (hash_2 >> 16)

    hash_4 = int(PRIME_1 * seed + PRIME_5 * x * scale)
    
    hash_4 ^= (hash_2 >> 13)
    hash_4 *= HASH_MIXING_CONSTANT
    hash_4 ^= (hash_2 >> 16)

    return ((hash_1 & 0x7FFFFFFF) / 0x7FFFFFFF, (hash_2 & 0x7FFFFFFF) / 0x7FFFFFFF, (hash_3 & 0x7FFFFFFF) / 0x7FFFFFFF, (hash_4 & 0x7FFFFFFF) / 0x7FFFFFFF)