# Python Ethereum Transaction Signer

This Python script, sign.py, is a tool for signing Ethereum transactions using the Web3 library. It facilitates the creation of properly formatted Ethereum transactions by encoding function calls and generating the required transaction parameters. The script also calculates recommended gas fees based on the latest block's information.

## Prerequisites

Before using this script, ensure you have the following prerequisites set up:
- Ensure you have [Poetry](https://python-poetry.org/) installed.
- Ethereum node connection information provided in a .env file
- Required environment variables set in `.env`: RPC, OWNER_ADDRESS, MAX_GAS, PRIVATE_KEY, CHAIN_ID, MAX_PRIORITY_FEE_PER_GAS

## Usage

Execute the script with the following command:

```bash
poetry run python sign.py <contract> <value> <function_sig> <args>
```

### Example

```sh
$ poetry run python sign.py 0xb4fe1c9a7068586f377eCaD40632347be2372E6C 0 "setMinWithdrawal(uint128)" 100000000000000000
block: 10163271
maxFeePerGas: 65366058
maxPriorityFeePerGas: 30000000
nonce: 35
transaction_dict: {'chainId': 5, 'nonce': 35, 'maxFeePerGas': 65366058, 'maxPriorityFeePerGas': 30000000, 'gas': 500000, 'to': '0xb4fe1c9a7068586f377eCaD40632347be2372E6C', 'value': 0, 'data': b'\x88e\xcfP\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01cEx]\x8a\x00\x00'}
signed_tx: 0x02f88f05238401c9c3808403e5682a8307a12094b4fe1c9a7068586f377ecad40632347be2372e6c80a48865cf50000000000000000000000000000000000000000000000000016345785d8a0000c080a0045e63586c3678b15c27634c13a5d4326cf156ddbb151c1826b41c171bd5d268a057e552fedd61f7cbc30585ee8b0f0598ffea8fd31e8911f88980e2f74e844625
simulating tx
b''
```