from flask import Flask, jsonify, request, render_template
from web3 import Web3, IPCProvider, Account
from web3.middleware import geth_poa_middleware

# abi is changin when you change contract
ABI =  [{'constant': False, 'inputs': [{'name': 'data', 'type': 'string'}], 'name': 'enqueue', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'lenght', 'outputs': [{'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'position', 'type': 'uint256'}], 'name': 'get_patient', 'outputs': [{'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [{'name': '', 'type': 'uint256'}], 'name': 'receptionistAccts', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'dequeue', 'outputs': [{'name': 'data', 'type': 'string'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'greet', 'outputs': [{'name': 'greet', 'type': 'string'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}]
# addres change when you deploy contract (if you not reset blockchain, old contract exists)
ADDRESS = '0x31E9FbdBc7Fc7387e32251406B2D820193eAd72E'

app = Flask(__name__, template_folder='./templates')

def connect_to_blockchain():
    w3 = Web3(IPCProvider(ipc_path='/tmp/geth.ipc', testnet=True))
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    queue = w3.eth.contract(address=ADDRESS, abi=ABI)
    print('Default contract greeting: {}'.format(
        queue.functions.greet().call()
    ))

    return w3, queue

def add_patient_to_queue(patient):
    tx_hash = queue.functions.enqueue(patient).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)


def read_all_patient():
    patients = []
    lenght = queue.functions.lenght().call()
    print(lenght)

    for i in range(lenght):
        patients.append(queue.functions.get_patient(i).call())

    return patients


w3, queue = connect_to_blockchain()

w3.eth.defaultAccount = w3.eth.accounts[0]
Account.create()

add_patient_to_queue("Damian")
add_patient_to_queue("Kasia")
print(read_all_patient())
# app.run(host='0.0.0.0', port=5000)
