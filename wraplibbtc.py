import ctypes
import os

wrappath = "."
fname = os.path.join(wrappath,'wrappedlibbtc.so')
if not os.path.isfile(fname):
    wrappath = os.getenv("wrappath")
    if wrappath is None or len(wrappath) == 0:
        print("Please set path to location of wrappedlibbtc.so that you should have created, e.g. in bash export wrappath=\"...\"")
        exit(1)
    fname = os.path.join(wrappath,'wrappedlibbtc.so')
print("Opening dynamic library", fname)
_lib = ctypes.CDLL(fname)

_lib.btc_ecc_start.argtypes = ()
_lib.get_pubkey.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
_lib.btc_ecc_start()
_pubkey_hex = ("0" * 66).encode('utf-8')


def convert_priv_to_hex_pub(priv_key):
    global _lib, _pubkey_hex
    pkey = priv_key.encode('utf-8')
    _lib.get_pubkey(pkey, _pubkey_hex)
    return(_pubkey_hex)

if __name__ == "__main__":
    print(convert_priv_to_hex_pub("KwmAqzEiP7nJbQi6ofQywSEad4j5b9BXDJvyypQDDLSvrV6wACG8"))
