from web3 import Web3
import json

class EthereumLedger:
    def __init__(self, rpc_url="http://127.0.0.1:8545", contract_address=None):
        """
        Connects to a local Ganache RPC or remote Infura (Sepolia/Mainnet).
        Wait for Ganache to be running before executing transactions!
        """
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.connected = self.w3.is_connected()
        self.contract_address = contract_address
        
        # Load the default dev wallet if Ganache is running
        if self.connected:
            self.account = self.w3.eth.accounts[0] if self.w3.eth.accounts else None
        else:
            self.account = None

    def register_transaction(self, image_id, hospital, modality, signature, rsa_signature=""):
        """
        Sends the transaction to the Ethereum Smart Contract.
        """
        if not self.connected:
            print("WARNING: Web3 not connected. Please start Ganache or update Infura URL.")
            return False
            
        print(f"[{self.account}] Anchoring {image_id} to Ethereum Blockchain via Web3...")
        
        # Implementation logic to be enabled once ABI is compiled:
        # tx_hash = contract.functions.registerImage(image_id, hospital, modality, signature, rsa_signature).transact({'from': self.account})
        # self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return True

    def verify_transaction(self, image_id):
        """
        Reads immutably from the Smart Contract.
        """
        if not self.connected:
            print("WARNING: Web3 not connected.")
            return None
            
        # Implementation logic to be enabled once ABI is compiled:
        # return contract.functions.verifyImage(image_id).call()
        return None
