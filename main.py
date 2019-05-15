import sys
import time
import pprint
import pickle # save to list

# from web3.auto.gethdev import w3
from web3 import Web3, IPCProvider
from solc import compile_source
from web3.middleware import geth_poa_middleware

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    # tx_hash = w3.eth.contract(
    #     abi=contract_interface['abi'],
    #     bytecode=contract_interface['bin']).deploy()

    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor().transact()

    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt.contractAddress


def wait_for_receipt(w3, tx_hash, poll_interval):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)

# w3.isConnected()
# w3.eth.getBlock('latest')

w3 = Web3(IPCProvider(ipc_path='/tmp/geth.ipc', testnet=True))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

w3.eth.defaultAccount = w3.eth.accounts[0]

print(w3.version.node)

compiled_sol = compile_source_file('./queue.sol')

contract_id, contract_interface = compiled_sol.popitem()

address = deploy_contract(w3, contract_interface)
print("Deployed {0} to: {1}\n".format(contract_id, address))
print("address {0} \n ABI: {1}\n".format(address, contract_interface['abi']))

# Write ABI and address to file
with open('ABI.txt', 'wb') as fp:
    pickle.dump(contract_interface['abi'], fp)

f = open("address.txt", "w")
f.write(address)
f.close()

# Create users

# this generate address + private key but not add to node
# myAccount = w3.eth.account.create('entropy')
# myAddress = myAccount.address
# myPrivateKey = myAccount.privateKey
# print('my address is     : {}'.format(myAccount.address))
# print('my private key is : {}'.format(myAccount.privateKey.hex()))

# Add new addres and keep private_key in node
my_address = w3.personal.newAccount("pass")
print('Accounst: {}'.format(w3.personal.listAccounts))

w3.eth.sendTransaction({'to': my_address, 'from': w3.eth.coinbase, 'value': 1})
print('Address {} Money {}'.format(my_address, w3.eth.getBalance(my_address)))


# Test
queue = w3.eth.contract(
    address=address,
    abi=contract_interface['abi']
)

print('Default contract greeting: {}'.format(
    queue.functions.greet().call()
))

tx_hash = queue.functions.enqueue("Damian").transact()
w3.eth.waitForTransactionReceipt(tx_hash)

print('Size: {}'.format(queue.functions.lenght().call()))

print('First test user: {}'.format(
    queue.functions.dequeue().call()
))
