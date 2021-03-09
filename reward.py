from decimal import Decimal


def calculate_pps(user_hashrate: int, network_hashrate: int, blocks_rewards: Decimal):
    if not network_hashrate:
        return Decimal(0)
    return Decimal(user_hashrate)/Decimal(network_hashrate) * Decimal(blocks_rewards)


def calculate_fpps(user_hashrate: int, network_hashrate: int, blocks_rewards: Decimal, blocks_fees: Decimal,
                   actual_blocks_count: int, avg_blocks_count: int):
    if not network_hashrate:
        return Decimal(0)
    pps_reward = calculate_pps(user_hashrate, network_hashrate, blocks_rewards)
    fee_reward = Decimal(user_hashrate) / Decimal(network_hashrate) * Decimal(
        blocks_fees/actual_blocks_count * avg_blocks_count)

    return pps_reward + fee_reward
