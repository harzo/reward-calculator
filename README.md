## rewards calulator

This tool allows calculating BTC mining rewards out of a given hash rate.

### Source of network data: https://btc.com

### Currently supported calculation methods:
- PPS
- FPPS

### Usage

```
reward-calculator hashrate datetime [-m [{fpps,pps}]] [-p [{day,hour}]]
```

#### Example

```
reward-calculator 8644948859909036.563 '2021-03-09'
reward-calculator 8644948859909036.563 '2021-03-09 10:00:00' -p hour
reward-calculator 8644948859909036.563 '2021-03-09 10:00:00' -p hour -m pps
```

#### Arguments

- `hashrate` - Mining hashrate (H/s) used to calculate reward.
- `datetime` - Date (and time) when mining has started.
- `-m`, `--method` - Reward calculation method. Options: `fpps`,`pps`. Default `fpps`.
- `-p`, `--period` - Reward calculation period (mining duration from the start). Options: `day`,`hour`. Default `day`.
