from vyper import compile_code
from web3 import Web3  
from dotenv import load_dotenv
import os
from encrypt_key import KEYSTORE_PATH
import getpass
from eth_account import Account

load_dotenv()
MY_ADDR = os.getenv("MY_ADDR")
RPC_URL = os.getenv("RPC_URL")
ADDRESS_TO_USE = os.getenv("ADDRESS_TO_USE")


def main():
    print("Reading into Vyper contract: \n......\n")
    with open("buy_me_coffee.vy", "r") as coffee_file:
        coffee_code = coffee_file.read()
        compilation_details = compile_code(coffee_code, output_formats = ["bytecode", "abi"])
        print(f"{compilation_details}\n")

    coffee3 = Web3(Web3.HTTPProvider(RPC_URL))
    coffee_contract = coffee3.eth.contract(bytecode = compilation_details["bytecode"], abi = compilation_details["abi"])

    print("Building the transaction: \n......\n")
    coffee_nonce = coffee3.eth.get_transaction_count(MY_ADDR)
    coffee_txn = coffee_contract.constructor(ADDRESS_TO_USE).build_transaction({
        "nonce": coffee_nonce,
        "from": MY_ADDR,
        "gasPrice": coffee3.eth.gas_price
    })
    print(f"{coffee_txn}\n")

    print("Signing transaction: \n......\n")
    private_key = decrypt_key()
    coffee_signed_txn = coffee3.eth.account.sign_transaction(coffee_txn, private_key = private_key)
    print(f"{coffee_signed_txn}\n")

    print("Sending transaction: \n......\n")
    coffee_txn_hash = coffee3.eth.send_raw_transaction(coffee_signed_txn.raw_transaction)
    print(f"Transaction hash is: {coffee_txn_hash}\n")

    print("Getting transaction receipt: \n......\n")
    coffee_txn_receipt = coffee3.eth.wait_for_transaction_receipt(coffee_txn_hash)

    print(f"Done!!! Contract deployed to: {coffee_txn_receipt.contractAddress}")

def decrypt_key() -> str:
    with open (KEYSTORE_PATH, "r") as fp:
        encrypted_account = fp.read()
        password = getpass.getpass("Enter your password: ")
        key = Account.decrypt(encrypted_account, password)
        return key

if __name__ == "__main__":
    main()
