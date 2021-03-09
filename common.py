from decimal import Decimal

import typing

AVERAGE_BLOCK_TIME_SECONDS = 600
AVERAGE_BLOCKS_COUNT_PER_DAY = 144

DAY_IN_SECONDS = 24 * 60 * 60


def average(_list: typing.Collection):
    if len(_list) == 0:
        return 0
    return sum(_list) / len(_list)


def share_to_hashrate(share: int, _seconds: int) -> Decimal:
    if not share or not _seconds:
        return Decimal(0)
    return (Decimal(share << 32) / Decimal(_seconds)).quantize(Decimal('1.000'))


def difficulty_to_hashrate(difficulty: Decimal, duration: int = AVERAGE_BLOCK_TIME_SECONDS):
    return difficulty * pow(2, 32) / duration
