import solcx
import json
import os
from solcx import compile_standard, install_solc
from web3 import Web3

# opens .sol file and imports it to Python
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

#installs Solc-X Compiler version 0.6.0 since we are compiling solidity in that version
install_solc("0.6.0")

# Compiled Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)
#opening JSon file and writing it to Compiled_Sol file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get byte code from Json File
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["DegreeDevelopment"]["evm"][
    "bytecode"
]["object"]

# get abi from Json File
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["DegreeDevelopment"]["abi"]

# for connecting to ganache
#update server IP and port based on your computer settings
#Using Infura.io to connect to testnet
#Update Chain ID depending or Block chain you are using or you will get an error
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/3b0238e078f447f19da8228e66e274a5"))
chain_id = 4

#update these values based on your ganache wallet
my_address = "0x3a07764BF1dB9ebb7dc6cf120F9a4C904E0a90bE"  # python requires an 0x in front of key
private_key = os.getenv("PRIVATE_KEY") #"fe82008d3832f9b2c2e996e43aa93c449fa14a6593182d7f9d820f7291dd48e2"

print("Contract Deployed")
#while loop to allows for multiple user input
while True:
    # Create the contract in Python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)
    # Submit the transaction that deploys the contract
    # 1. Build Tranasaction
    transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
    )
    # 2. Sign Transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    # 3. Send Transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    Continue_input = input("Would you like to enter a record? Yes/No ")
    if Continue_input == 'Yes' :
        #Contract input variables
        StudentId = int(input("Enter User ID: "))
        StudentName = input("Enter Student Name: ")
        DegreeType = input("Degree Type: ") #Ex. Masters, Bachelors, Associate
        AreaofStudy = input("Area of Study: ") #Electrical Engineering, Computer Science
        SchoolName = input("School Name: ") #UTPB, Texas Tech
        GraduationDate = input("Enter Graduation Date: ") #02/21/2021
        #working with the contract
        #pulls abi and contract address from json file 
        simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        #writes Degree parameters to .sol file and adds 1 to the nonce
        store_transaction = simple_storage.functions.addGraduate(StudentId, StudentName, DegreeType, AreaofStudy, SchoolName, GraduationDate).buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
        )
        signed_store_txn = w3.eth.account.sign_transaction(
        store_transaction, private_key=private_key
        )
        print("Updating contract...")
        #sends new signatures to Ganache
        send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
        print("Contract updated!")
    elif pick == 'no':
        break
    else:
        print("You have to chose Yes or No")