# py-vanitycash
Python generator for vanity addresses for Bitcoin Cash (BCH)

## How to generate vanity addresses
The address is generated as a "cashaddress" e.g. bitcoincash:q**qqqqqq**5y7z5p7k442mhjzge974qqdwd6v6yvzvzls  
The first **qqqqqq**s are chosen when running the program:
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
 * [cashaddress](https://github.com/oskyk/cashaddress)

## Performance
The program is not super fast since it has to derive a pubkey from a privkey and check the cashaddr against your search pattern.  
Vanitygen does about 60 times better than the python program.  

Corei5-4300U:
 * Pure python      per CPU core -> ~10 H/s
 * C-implementation per CPU core -> ~5 kH/s
 
### Accelerate with C library

The pubkey generation can be greatly accelerated if a C implementation is used. We support [libbtc](https://github.com/libbtc/libbtc). To use use it
 * compile libbtc with CLI
 * set environtment variable
   * `export libbtcpath="PATHTOLIBBTC"`
   * `export LD_LIBRARY_PATH=$libbtcpath:$LD_LIBRARY_PATH`
   * `export wrappath=PY-VANITYCASHPATH`
 * now we need to compile a small wrapper around libbtc so python can use it with ctypes. In py-vanitycash
 `gcc -shared -fPIC -std=gnu99 wraplibbtc.c -I $libbtcpath/include/ -o wraplibbtc.so -L $libbtcpath/.libs/ -lbtc`
 * Run the main program with the `-l` or `--uselibbtc` option

