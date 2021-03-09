from decimal import Decimal

AVERAGE_BLOCK_TIME_SECONDS = 600
AVERAGE_BLOCKS_COUNT_PER_DAY = 144


def average(l: list):
    if len(l) == 0:
        return 0
    return sum(l) / len(l)


def share_to_hashrate(share: int, _seconds: int) -> Decimal:
    if not share or not _seconds:
        return Decimal(0)
    return (Decimal(share << 32) / Decimal(_seconds)).quantize(Decimal('1.000'))


def difficulty_to_hashrate(difficulty: Decimal, duration: int = AVERAGE_BLOCK_TIME_SECONDS):
    return difficulty * pow(2, 32) / duration
