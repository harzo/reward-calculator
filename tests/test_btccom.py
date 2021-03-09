from datetime import datetime
from decimal import Decimal

from btccom import BtcComClient, BtcComData

client = BtcComClient()
data = BtcComData()


def test_get_blocks_list_on_01012021():
    d = datetime.strptime('2021-01-01', "%Y-%m-%d").date()
    block_list = client.get_block_list(d)

    assert len(block_list['data']) == 149
    assert block_list['data'][0]['hash'] == '0000000000000000000e5ac8accffaa7ba73e200354b799133a29464cac7b8a6'
    assert block_list['data'][-1]['hash'] == '00000000000000000003f8a45967fe6a84a22a9deb86ddea0b2b78b0b859ea1d'


def test_get_blocks_stats_on_01012021():
    d = datetime.strptime('2021-01-01', "%Y-%m-%d")
    stats = data.get_blocks_stats(d)
    assert stats.average_difficulty == Decimal(18599593048299)
    assert stats.average_reward == Decimal(625000000)
    assert stats.total_fees == Decimal(4894270140)
    assert stats.total_blocks == 149
