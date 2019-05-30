import sys
import time
import pprint
import pickle # save to list
from flask import Flask, jsonify, request, render_template

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

compiled_sol = compile_source_file('./queue2.sol')

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

tx = w3.eth.sendTransaction({'to': my_address, 'from': w3.eth.coinbase, 'value': 100})
w3.eth.waitForTransactionReceipt(tx)
print('Address {} Money {}'.format(my_address, w3.eth.getBalance(my_address)))


# Test
queue = w3.eth.contract(
    address=address,
    abi=contract_interface['abi']
)

print('Default contract greeting: {}'.format(
    queue.functions.greet().call()
))

doctors = []
receptionists = []
ADMIN = w3.eth.accounts[0]

def create_doctor(name):
    # Create account
    doctor = w3.personal.newAccount("pass")
    # Send money
    tx_hash = w3.eth.sendTransaction({'to': doctor, 'from': w3.eth.coinbase, 'value': w3.toWei(100, "ether")})
    w3.eth.waitForTransactionReceipt(tx_hash)
    # Add account to list doctors
    tx_hash = queue.functions.add_doctor(doctor, name).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    print('New doctor {} Address {} Money {}'.format(name, doctor, w3.eth.getBalance(doctor)))
    doctors.append({'name':name,'address':doctor})
    return doctor

def create_receptionist(name):
    # Create account
    receptionist = w3.personal.newAccount("pass")
    # Send money
    tx_hash = w3.eth.sendTransaction({'to': receptionist, 'from': w3.eth.coinbase, 'value': w3.toWei(100, "ether")})
    w3.eth.waitForTransactionReceipt(tx_hash)
    # Add account to list recepionist
    tx_hash = queue.functions.add_receptionist(receptionist).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)
    print('New receptionist Address {} Money {}'.format(receptionist, w3.eth.getBalance(receptionist)))
    receptionists.append({'name':name,'address':receptionist})
    return receptionist


doctor1 = create_doctor("Damian")
doctor2 = create_doctor("Grzegorz")
doctor3 = create_doctor("Marcin")
receptionist = create_receptionist("Recp1")
print('Accounst: {}'.format(w3.personal.listAccounts))


number_doctors = queue.functions.getNumberDoctors().call()
print('Number doctors: {}'.format(number_doctors))

def read_dotors():
    number_doctors = queue.functions.getNumberDoctors().call()

    names = []
    doctors = []
    addresses = []
    for doctor_id in range(number_doctors):
        name, address = queue.functions.getDoctorById(doctor_id).call()
        names.append(name)
        addresses.append(address)
        doctors.append({'name': name, 'address': address})

    print(names)
    print(addresses)
    print(doctors)

read_dotors()

def add_patient(address_doctor, name):
    tx_hash = queue.functions.newPatient(address_doctor, name).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

add_patient(doctor1, "Basia")
add_patient(doctor1, "Basia2")
add_patient(doctor1, "Basia3")
add_patient(doctor1, "Basia4")
add_patient(doctor1, "Basia5")

def add_visit(idPatient, addressDoctor, idVisit):
    tx_hash = queue.functions.addVisitToPatient(idPatient, addressDoctor, idVisit).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

add_visit(1, doctor2, 1);
add_patient(doctor2, "BasiaDoctor2")
add_visit(2, doctor2, 1);


def delete_first_patientB(address_doctor):
    tx_hash = queue.functions.deleteFirstPatient(address_doctor).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)


def get_next_patient(address_doctor):
    tx_hash = queue.functions.getNextPatient(address_doctor).call()
    return tx_hash


def delete_patient(address_doctor,id):
    tx_hash = queue.functions.deletePatient2(address_doctor, id).transact()
    w3.eth.waitForTransactionReceipt(tx_hash)


def get_patients():
    number_doctors = queue.functions.getNumberDoctors().call()

    doctors = []
    for doctor_id in range(number_doctors):
        name, address = queue.functions.getDoctorById(doctor_id).call()
        patients_id =  queue.functions.getDoctrorPatients(address).call()
        patients = []
        for patient in patients_id:
            patients.append({'id': patient, 'patients_name':queue.functions.getPatient(patient).call()})
        doctors.append({'name': name, 'address': address, 'patients': patients,
                        'next_patient': get_next_patient(address)})


    print(doctors)
    return doctors

get_patients()



#delete_first_patient(doctor1)
#delete_patient(doctor1,2);
w3.eth.defaultAccount = doctor1
w3.personal.unlockAccount(doctor1, "pass", 15000)
delete_first_patientB(doctor1)
#delete_first_patientB(doctor2)
get_patients()

def get_accounts():
    admin = [{'name':'ADMIN','address':ADMIN}]
    return doctors+receptionists+admin

app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
    return render_template('index.html', queue=get_patients(), user=w3.eth.defaultAccount, accounts=get_accounts(), doctors=doctors), 200

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    values = request.form

    # Check that the required fields are in the POST'ed data
    required = ['name']
    if not all(k in values for k in required):
        return 'Missing values', 400

    name = values['name']
    create_doctor(name)
    return render_template('index.html', queue=get_patients(), user=w3.eth.defaultAccount, accounts=get_accounts(), doctors=doctors), 200


@app.route('/set_user', methods=['POST'])
def set_user():
    values = request.form

    # Check that the required fields are in the POST'ed data
    required = ['user']
    if not all(k in values for k in required):
        return 'Missing values', 400

    user = values['user']

    w3.eth.defaultAccount = user
    # w3.personal.unlockAccount(w3.personal.listAccounts[0], "", 15000)
    #add_patient_to_queue(patient_name)

    return render_template('index.html', queue=get_patients(), user=w3.eth.defaultAccount, accounts=get_accounts(), doctors=doctors), 201


@app.route('/next_patient', methods=['POST'])
def next_patient():
    values = request.form

    # Check that the required fields are in the POST'ed data
    # required = ['user']
    # if not all(k in values for k in required):
    #     return 'Missing values', 400
    #
    # user = values['user']
    w3.personal.unlockAccount(w3.eth.defaultAccount, "pass", 15000)
    delete_first_patientB(w3.eth.defaultAccount)
    # w3.personal.unlockAccount(w3.personal.listAccounts[0], "", 15000)
    #add_patient_to_queue(patient_name)

    return render_template('index.html', queue=get_patients(), user=w3.eth.defaultAccount, accounts=get_accounts(), doctors=doctors), 201

@app.route('/delete_middle_patient', methods=['POST'])
def delete_middle_patient():
    values = request.form

    required = ['doctor', 'id']
    if not all(k in values for k in required):
        return 'Missing values', 400

    doctor = values['doctor']
    id = values['id']
    w3.personal.unlockAccount(w3.eth.defaultAccount, "pass", 15000)
    delete_patient(doctor,int(id))
    # w3.personal.unlockAccount(w3.personal.listAccounts[0], "", 15000)
    #add_patient_to_queue(patient_name)

    return render_template('index.html', queue=get_patients(), user=w3.eth.defaultAccount, accounts=get_accounts(), doctors=doctors), 201


@app.route('/add_patient', methods=['POST'])
def add_patient_response():
    values = request.form

    # Check that the required fields are in the POST'ed data
    required = ['doctor','name']
    if not all(k in values for k in required):
        return 'Missing values', 400

    name = values['name']
    doctor = values['doctor']
    add_patient(doctor, name)
    return render_template('index.html', queue=get_patients(), user=w3.eth.defaultAccount, accounts=get_accounts(), doctors=doctors), 200

@app.route('/add_visit', methods=['POST'])
def add_visit_response():
    values = request.form

    # Check that the required fields are in the POST'ed data
    required = ['doctor','id']
    if not all(k in values for k in required):
        return 'Missing values', 400

    id = values['id']
    doctor = values['doctor']
    add_visit(int(id), doctor, 0)
    return render_template('index.html', queue=get_patients(), user=w3.eth.defaultAccount, accounts=get_accounts(), doctors=doctors), 200



app.run(host='0.0.0.0', port=5000)
