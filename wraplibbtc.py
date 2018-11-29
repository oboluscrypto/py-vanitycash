import ctypes
import os

libbtcpath = os.getenv("libbtcpath")
if libbtcpath is None or len(libbtcpath) == 0:
    print("Please set path to libbtc, e.g. in bash export libbtcpath=\"...\"")
    exit(1)
_lib = ctypes.CDLL(os.path.join(libbtcpath,'.libs/libbtc.so'))
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
