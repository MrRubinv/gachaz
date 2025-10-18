import random
from typing import Dict, List


"""Parody ZZZ pools.

Note: Names are for a fan demo and not affiliated with miHoYo/HoYoverse.
"""

FIVE_STAR_POOL = [
    "Ellen Joe",
    "Lycaon",
    "Soldier 11",
    "Rina",
    "Grace Howard",
]

FOUR_STAR_POOL = [
    "Anby Demara",
    "Nicole Demara",
    "Billy Kid",
    "Corin Wickes",
    "Anton Ivanov",
    "Ben Bigger",
    "Soukaku",
    "Piper Wheel",
]

THREE_STAR_POOL = [
    "Old Engine",
]


def _roll_rarity(pity4: int, pity5: int) -> int:
    """Return rarity 3, 4, or 5 with simple pity.

    - 5★ pity: guaranteed at 90
    - 4★ pity: guaranteed at 10
    - Base rates: 5★ 0.6%, 4★ 5.1%, 3★ 94.3%
    """
    if pity5 >= 89:
        return 5
    if pity4 >= 9:
        return 4

    roll = random.random() * 100.0
    if roll < 0.6:
        return 5
    if roll < 0.6 + 5.1:
        return 4
    return 3


def _pick_name(rarity: int) -> str:
    if rarity == 5:
        return random.choice(FIVE_STAR_POOL)
    if rarity == 4:
        return random.choice(FOUR_STAR_POOL)
    return random.choice(THREE_STAR_POOL)


def perform_pulls(count: int, banner: str = "standard") -> Dict:
    """Perform gacha pulls with pity counters (client-local, not persisted).

    Returns a dictionary with `results` (list of dicts) and `summary` counts.
    """
    pity4 = 0
    pity5 = 0
    results: List[Dict] = []
    counts = {3: 0, 4: 0, 5: 0}

    for _ in range(count):
        rarity = _roll_rarity(pity4, pity5)
        name = _pick_name(rarity)

        # Update pity
        if rarity == 5:
            pity5 = 0
            pity4 = 0
        elif rarity == 4:
            pity4 = 0
            pity5 += 1
        else:
            pity4 += 1
            pity5 += 1

        counts[rarity] += 1
        results.append({
            "rarity": rarity,
            "name": name,
            "pity4At": pity4,
            "pity5At": pity5,
        })

    summary = {
        "pulled3": counts[3],
        "pulled4": counts[4],
        "pulled5": counts[5],
    }

    return {"results": results, "summary": summary}


