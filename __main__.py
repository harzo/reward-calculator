import argparse
import logging
import pytz as pytz
import sys

from btccom import BtcComData
from common import difficulty_to_hashrate, AVERAGE_BLOCKS_COUNT_PER_DAY, DAY_IN_SECONDS, satoshi_to_btc
from datetime import datetime
from reward import calculate_fpps

parser = argparse.ArgumentParser(prog='reward-calculator', description='Rewards Calculator')
parser.add_argument('hashrate', nargs='?', type=float, help='Mining hashrate (H/s) used to calculate reward')
parser.add_argument('datetime', nargs='?', type=datetime.fromisoformat, help='Date (and time) when mining has started')
parser.add_argument('-m', '--method', nargs='?', choices=['fpps', 'pps'], default='fpps',
                    help='Reward calculation method')
parser.add_argument('-p', '--period', nargs='?', choices=['day', 'hour'], default='day',
                    help='Reward calculation period (mining duration from the start)')

logging.basicConfig(format='reward-calculator: %(levelname)s: %(message)s', level=logging.DEBUG)

if __name__ == '__main__':
    args = parser.parse_args()
    if not args.hashrate:
        logging.error(f'missing `hashrate` argument')
        sys.exit()
    elif not args.datetime:
        logging.error(f'missing `datetime` argument')
        sys.exit()

    hashrate = args.hashrate
    dt = args.datetime
    dt = dt.replace(tzinfo=pytz.UTC, hour=0, minute=0, second=0, microsecond=0)

    btccom_data = BtcComData()
    blocks_stats = btccom_data.get_blocks_stats(dt, delta=DAY_IN_SECONDS)

    difficulty = blocks_stats.average_difficulty
    reward_per_block = blocks_stats.average_reward
    total_fees = blocks_stats.total_fees
    total_blocks = blocks_stats.total_blocks

    network_hashrate = difficulty_to_hashrate(difficulty)
    block_rewards = AVERAGE_BLOCKS_COUNT_PER_DAY * reward_per_block

    print(f'Difficulty: {difficulty} ({difficulty / pow(10, 12)} x 10^12)')
    print(f'Network hashrate: {network_hashrate} ({network_hashrate / pow(10, 18)} EH)')
    print(f'Average coinbase rewards: {satoshi_to_btc(block_rewards)} from {AVERAGE_BLOCKS_COUNT_PER_DAY} blocks')
    print(f'Total txs fees: {satoshi_to_btc(total_fees)} from {total_blocks} blocks')

    print(f'\nMining stats:')
    print(f'- Hashrate: {hashrate} ({hashrate / pow(10, 15)} PH)')

    fpps_reward = calculate_fpps(hashrate, network_hashrate, block_rewards, total_fees, total_blocks,
                                 AVERAGE_BLOCKS_COUNT_PER_DAY)
    print(f'- FPPS reward: {satoshi_to_btc(fpps_reward)} BTC')
