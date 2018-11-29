#include <btc/chainparams.h>
#include <btc/tool.h>

#include <stdbool.h>
#include <assert.h>

void get_pubkey(const char* pkey, char* pubkey_hex)
{
  const btc_chainparams* chain = &btc_chainparams_main;
  size_t sizeout = 128;
  bool ret = pubkey_from_privatekey(chain, pkey, pubkey_hex, &sizeout);
  assert(ret);
  return;
}
