## rewards calulator

This tool allows calculating BTC mining rewards out of a given hash rate.

### Source of network data: https://btc.com

### Currently supported calculation methods:
- PPS
- FPPS

### Dependencies

- Python >= 3.7
- [Pipenv](https://pypi.org/project/pipenv/)

### Usage

Go to the project folder (`cd reward-calculator`) and run:
- `pipenv install`
- `pipenv shell`
- `python . hashrate datetime [-m [{fpps,pps}]] [-p [{day,hour}]]`


#### Example

```
python . 8644948859909036.563 '2021-03-09'
python . 8644948859909036.563 '2021-03-09 10:00:00' -p hour
python . 8644948859909036.563 '2021-03-09 10:00:00' -p hour -m pps
```

#### Arguments

- `hashrate` - Mining hashrate (H/s) used to calculate reward.
- `datetime` - Date (and time) when mining has started.
- `-m`, `--method` - Reward calculation method. Options: `fpps`,`pps`. Default `fpps`.
- `-p`, `--period` - Reward calculation period (mining duration from the start). Options: `day`,`hour`. Default `day`.
