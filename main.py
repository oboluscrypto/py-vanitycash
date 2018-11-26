import sys, os, binascii, hashlib
import base58, ecdsa
import cashaddress
from datetime import datetime, timedelta
import math

_can_decode = True
_d = hashlib.new('ripemd160')

def ripemd160(x):
    global _d
    _d.update(x)
    return _d

def gen_and_compare(cmp: str, anywhere: bool, nposs: int):
    global _can_decode
    start_time = last_print = datetime.now()
    priv_key_init_byte = os.urandom(32)
    priv_key_int = int.from_bytes(priv_key_init_byte, 'big')
    i=0
    while True:   # number of key pairs to generate`
        priv_key_int += -1
        priv_key = priv_key_int.to_bytes(32, byteorder="big") # back to bytes
        # generate private key , uncompressed WIF starts with "5"
        fullkey = '80' + binascii.hexlify(priv_key).decode()
        sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
        sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
        WIF = base58.b58encode(binascii.unhexlify(fullkey+sha256b[:8]))

        # get public key , uncompressed address starts with "1"
        sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
        hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
        publ_addr_a = b"\x00" + hash160
        checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
        publ_addr_b = base58.b58encode(publ_addr_a + checksum)
        i += 1

        if _can_decode:
            try:
                WIF = WIF.decode()
                publ_addr_b = publ_addr_b.decode()
            except AttributeError as e:
                print(f"This part is python 3.7. Exception was: {e}. Skipping conversion")
                _can_decode = False

        addr = cashaddress.convert.to_cash_address(publ_addr_b)
        if anywhere and cmp in addr[13:]:
            break
        elif (not anywhere) and addr[13:].startswith(cmp):
            break

        if i % 10 == 0:
            now = datetime.now()
            if (now - last_print).total_seconds() > 10:
                last_print = now
                print(f"{i} hashes ({i/((now-start_time).total_seconds())} H/s), lastest address {addr}")
    print(f"Found hash with \"{cmp}\" after {(datetime.now() - start_time).total_seconds():.2f}s.")
    return WIF, publ_addr_b, addr, i

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, help=" e.g. qhi, starts with q/r/z/p", required=True)
    parser.add_argument("-p", "--position", type=int, help="1 if searchString can show up anywhere, 0 for in beginning", default=0)
    args = parser.parse_args()

    if len(args.search) == 0:
        parser.print_help()
        exit(1)
    if args.search[0] not in "qrzp":
        print("Not starting with bitcoincash:q(q/r/z/p) might take a long time if it works at all", file=sys.stderr)
    if any(ch in args.search for ch in ['o','i','1','b']):
        print("Characters 1/i/o/b not supported in Bech32", file=sys.stderr)
        exit(1)
    nposs = 4 + 32**(len(args.search)-1)
    prob = 1./nposs
    tests = [1,1e3,1e6,1e9,1e12]
    prob_after = [1 - ((1-prob) ** ev) for ev in tests]
    print(f"Vanity address with {nposs} possibilities requested. Prob after many tries is:")
    for tr,pr in zip(tests, prob_after):
        print(f"Tries: {tr} -> {pr}")
    WIF, btc, bch, i = gen_and_compare(cmp=args.search, anywhere=args.position, nposs=nposs)
    print(f"Checked {i} addresses")
    print("Private Key         : " + WIF)
    print("Bitcoin Address     : " + btc)
    print("Bitcoin Cash Address: " + bch)
