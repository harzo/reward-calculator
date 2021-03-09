from datetime import datetime

import pytz as pytz

from common import difficulty_to_hashrate, AVERAGE_BLOCKS_COUNT_PER_DAY
from decimal import Decimal
from reward import calculate_fpps

import argparse

parser = argparse.ArgumentParser(prog='reward-calculator', description='Rewards Calculator')
parser.add_argument('hashrate', nargs='+', type=int, help='Mining hashrate (H/s) used to calculate reward')
parser.add_argument('datetime', nargs='+', type=datetime.fromisoformat, help='Date (and time) when mining has started')
parser.add_argument('-m', '--method', nargs='?', choices=['fpps', 'pps'], default='fpps',
                    help='Reward calculation method')
parser.add_argument('-p', '--period', nargs='?', choices=['day', 'hour'], default='day',
                    help='Reward calculation period (mining duration from the start)')

if __name__ == '__main__':
    args = parser.parse_args()
    args['datetime'].replace(tzinfo=pytz.UTC)

    difficulty = Decimal(0)
    reward_per_block = Decimal(0)
    total_fees = Decimal(0)
    total_blocks = 0
    hashrate = 0

    network_hashrate = difficulty_to_hashrate(difficulty)
    block_rewards = AVERAGE_BLOCKS_COUNT_PER_DAY * reward_per_block

    print(f'Difficulty: {difficulty} ({difficulty / pow(10, 12)} x 10^12)')
    print(f'Network hashrate: {network_hashrate} ({network_hashrate / pow(10, 18)} EH)')
    print(f'Coinbase rewards: {block_rewards} from {AVERAGE_BLOCKS_COUNT_PER_DAY} blocks')
    print(f'TX Fees: {total_fees} from {total_blocks} blocks')

    print(f'\nMining stats:')
    print(f'- Hashrate: {hashrate} ({hashrate / pow(10, 15)} PH)')

    fpps_reward = calculate_fpps(hashrate, network_hashrate, block_rewards, total_fees, total_blocks,
                                 AVERAGE_BLOCKS_COUNT_PER_DAY)
    print(f'- FPPS reward: {fpps_reward} BTC')
