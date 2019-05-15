Ethereum

Python Web3 documentation
https://web3py.readthedocs.io/en/stable

Website to develop contract
https://remix.ethereum.org/

Requirements

We need:
 - etherum node, my choice is Geth 
(https://geth.ethereum.org/install-and-build/Installing-Geth)
 - python3
 - python lib web3, which help connect to etherum node
 - solc, compiler smart contracs 

Install
```bash
apt-get install software-properties-common
add-apt-repository -y ppa:ethereum/ethereum
apt-get update
apt-get install ethereum geth python3.6 python3.6-dev python3.6-pip wget
pip install py-solc
pip install -r requirements.txt
python -m solc.install v0.4.25
# python need older version solc in version v0.4.25; 1.05.19
# DO NOT! apt-get install solc 
```

To run node eherum in dev mode
```bash
geth --dev console --rpc
```

