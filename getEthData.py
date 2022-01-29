from etherscan import Etherscan
from dotenv import load_dotenv
from brownie import Wei
from defillama import DefiLlama
import time
import os

load_dotenv()  # take environment variables from .env.
llama = DefiLlama()

# Get all protocols data
llama_res = llama.get_all_protocols()

eth = Etherscan(os.environ.get("ETHERSCAN_APIKEY"))  # key in quotation marks


def fix_protocol_address(protocol_address: str) -> str:

    addr = protocol_address.strip()

    if addr[0] != "0":
        return False

    return addr


for protocol in llama_res:
    if "Ethereum" in protocol["chain"] and protocol["symbol"] != "-":

        print(protocol["symbol"])
        protocol_address = protocol["address"]
        try:

            if fix_protocol_address(protocol_address):

                ethBalance = eth.get_acc_balance_by_token_and_contract_address(
                    contract_address=protocol_address,
                    address="0x5dd596c901987a2b28c38a9c1dfbf86fffc15d77",
                )
                if ethBalance == "0" or protocol["symbol"] == "WBTC":
                    print(ethBalance)
                else:
                    print(Wei(ethBalance).to("ether"))
        except Exception as e:
            print(e)

    time.sleep(0.5)
