import os
import logging
from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import Web3RPCError

# Load the private key from the .env file
load_dotenv()
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

# RPC connection
rpc_url = "https://sepolia-rpc.scroll.io"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Addresses, chain ID, and log name
source_address = '0x7C9E9d4F38a01FC7cBf0F603c3E5F40470c9F80b'
target_address = '0x776638E10cBe0ea5E6Ce9f07005A2F6764D97e32'
chain_id = 534351
log_name = 'fix_script.log'

# Logging configuration
logging.basicConfig(filename=log_name, level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Function to send a transaction
def send_transaction(web3, source, target, private_key, nonce, chain_id):
    txn = {
        'from': source,
        'to': target,
        'value': web3.to_wei(0.001, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': nonce,
        'chainId': chain_id
    }
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return tx_hash
    except Web3RPCError as e:
        if 'already known' in str(e):
            logger.warning(f"Transaction with nonce {nonce} already known, retrying with incremented nonce.")
            return send_transaction(web3, source, target, private_key, nonce + 1, chain_id)
        else:
            raise e

# Function to get the latest transaction count
def get_latest_nonce(web3, address):
    return web3.eth.get_transaction_count(address, 'pending')

# Main function
def main():
    nonce = get_latest_nonce(web3, source_address)
    for i in range(10):
        tx_hash = send_transaction(web3, source_address, target_address, PRIVATE_KEY, nonce, chain_id)
        logger.info(f"Iteration {i+1}: Nonce: {nonce}, Transaction Hash: {web3.to_hex(tx_hash)}")
        nonce += 1  # Increment nonce after each successful transaction
    print("Script ran successfully. Output is in the log file:", log_name)

if __name__ == '__main__':
    main()
