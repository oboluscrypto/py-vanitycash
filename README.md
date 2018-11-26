# py-vanitycash
Python generator for vanity addresses for Bitcoin Cash (BCH)

## How to generate vanity addresses
The address is generated as a "cashaddress" e.g. bitcoincash:qqqqqqq5y7z5p7k442mhjzge974qqdwd6v6yvzvzls
The first q's are chosen like:
```
python main.py -s qqqqqq -p 0
```

## Installation (requires Python3)
```
pip install -r requirements.txt
python main.py
```

## Multithreading
For now, just run multiple instances according to number of cores

## Requirements
We thankfully use the following external libraries:
https://github.com/oskyk/cashaddress
