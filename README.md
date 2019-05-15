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
apt-get install ethereum geth python python-pip wget
python -m solc.install v0.4.25
# python need older version solc
# DO NOT! apt-get install solc 
```

