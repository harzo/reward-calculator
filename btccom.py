import logging
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import TypedDict, TypeVar, Generic, Optional, Tuple, List, NamedTuple, Dict

from apiclient import APIClient, retry_request, endpoint, JsonResponseHandler, JsonRequestFormatter

from common import DAY_IN_SECONDS, average

BTCCOM_API_URL = 'https://chain.api.btc.com/v3'

T = TypeVar('T')


class BtcComBlock(TypedDict):
    height: int
    version: int
    mrkl_root: str
    curr_max_timestamp: int
    timestamp: int
    bits: int
    nonce: int
    hash: str
    size: int
    pool_difficulty: int
    difficulty: int
    tx_count: int
    reward_block: int
    reward_fees: int
    created_at: int
    confirmations: int
    extras: dict
    prev_block_hash: Optional[str]
    next_block_hash: Optional[str]


BtcComBlockList = List[BtcComBlock]


class BtcComResponse(Dict, Generic[T]):
    data: T
    err_code: int
    err_no: int
    message: str
    status: str


@endpoint(base_url=BTCCOM_API_URL)
class BtcComEndpoint:
    block_list = "block/date/{date}"


class BtcComClient(APIClient):

    def __init__(self, host=BtcComEndpoint):
        super().__init__(response_handler=JsonResponseHandler, request_formatter=JsonRequestFormatter)
        self.endpoint = host

    @retry_request
    def get_block_list(self, d: date) -> BtcComResponse[BtcComBlockList]:
        """
        :param: d Blocks returned mining date
        :type: date
        :return: block_list List of blocks
        :type: BtcComResponse[BtcComBlock]
        """
        return self.get(BtcComEndpoint.block_list.format(date=d.strftime("%Y%m%d")))


class BlocksStats(NamedTuple):
    average_reward: Decimal
    average_difficulty: Decimal
    total_fees: Decimal
    total_blocks: int


class BtcComData:

    def __init__(self):
        self.client = BtcComClient()

    def get_blocks_stats(self, dt: datetime, delta: int = DAY_IN_SECONDS) -> BlocksStats:
        response = self.client.get_block_list(dt.date())
        if response['status'] != 'success':
            logging.error(f'btccom.get_block_list unsuccessful: {response["message"]}')
            return BlocksStats(Decimal(0), Decimal(0), Decimal(0))

        rewards, fees, difficulty = [], [], []
        total_blocks = 0
        for block in response['data']:
            block_dt = datetime.utcfromtimestamp(block['timestamp'])
            if dt <= block_dt <= dt + timedelta(seconds=delta):
                rewards.append(block['reward_block'])
                fees.append(block['reward_fees'])
                difficulty.append(block['difficulty'])
                total_blocks += 1

        return BlocksStats(Decimal(average(rewards)),
                           Decimal(average(difficulty)),
                           Decimal(sum(fees)),
                           total_blocks)
