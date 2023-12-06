import os
import sys
import web3
from eth_abi import encode
from eth_utils import keccak
from dotenv import load_dotenv
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

def format_arguments(args, function_sig_types):
    formatted_args = []
    for i in range(len(args)):
        if function_sig_types[i].find("int") > -1:
            formatted_args.append(int(args[i]))
        else:
            formatted_args.append(args[i])
    return formatted_args

# expecetd execution: poetry run python sign.py <contract> <value> <function_sig> <args>
# eg poetry run python sign.py 0x24Ae2dA0f361AA4BE46b48EB19C91e02c5e4f27E 0 "setMinWithdrawal(uint128)" 1000000000000000000
# .env expected params to be set: RPC, OWNER_ADDRESS, MAX_GAS, PRIVATE_KEY, CHAIN_ID, MAX_PRIORITY_FEE_PER_GAS
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Ethereum Transaction Signer")
    parser.add_argument("contract", type=str, help="Ethereum contract address")
    parser.add_argument("value", type=int, help="Transaction value")
    parser.add_argument("function_sig", type=str, help="Function signature")
    parser.add_argument("args", nargs="*", help="Function arguments")
    args = parser.parse_args()
    # connect to a node
    w3 = web3.Web3(web3.Web3.HTTPProvider(os.environ.get("RPC")))
    # encode calldata
    # contract: str = str(sys.argv[1])
    # function_sig: str = str(sys.argv[3])
    # args: list = list(sys.argv[4:])
    contract = args.contract
    logging.info(f"contract: {contract}")
    value = args.value
    logging.info(f"value: {value}")
    function_sig = args.function_sig
    logging.info(f"function_sig: {function_sig}")
    function_arguments = args.args
    logging.info(f"function_arguments: {function_arguments}")
    sig: bytes = keccak(text=function_sig)
    function_sig_types_str: str = str(function_sig[function_sig.find("(") + 1: function_sig.find(")")])
    logging.info(f"function_sig_types_str: {function_sig_types_str}")
    function_sig_types = function_sig_types_str.split(",")
    logging.info(f"function_sig_types: {function_sig_types}")
    format_args = format_arguments(function_arguments, function_sig_types)
    logging.info(f"format_args: {format_args}")        
    params: bytes = encode(function_sig_types, format_args);
    calldata: bytes = sig[0:4] + params
    logging.info(f"calldata: {calldata}")
    # get recommended fees
    block = w3.eth.get_block('latest')
    logging.info(f"block: {block.number}")
    maxFeePerGas = 2 * block["baseFeePerGas"]
    logging.info(f"maxFeePerGas: {maxFeePerGas}")
    maxPriorityFeePerGas = int(os.environ.get("MAX_PRIORITY_FEE_PER_GAS"))
    logging.info(f"maxPriorityFeePerGas: {maxPriorityFeePerGas}")
    # set value
    value=int(sys.argv[2])
    # get nonce
    nonce=w3.eth.get_transaction_count(os.environ.get("OWNER_ADDRESS"))
    logging.info(f"nonce: {nonce}")
    # populate tx dict
    transaction_dict = dict(
        chainId=int(os.environ.get("CHAIN_ID")),
        nonce=nonce,
        maxFeePerGas=maxFeePerGas,
        maxPriorityFeePerGas=maxPriorityFeePerGas,
        gas=int(os.environ.get("MAX_GAS")),
        to=contract,
        value=value,
        data=calldata,
        )
    logging.info(f"transaction_dict: {transaction_dict}")
    # sign transaction
    signed_tx = w3.eth.account.sign_transaction(
        transaction_dict,
        os.environ.get("PRIVATE_KEY"),
    )
    # logging.info result
    logging.info(f"signed_tx: {signed_tx.rawTransaction.hex()}")
    # optional: simulate tx
    logging.info("simulating tx")
    transaction_dict["from"] = os.environ.get("OWNER_ADDRESS")
    logging.info(w3.eth.call(transaction_dict))
    # end
    sys.exit()
    