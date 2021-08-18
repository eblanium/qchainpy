# Usage
The package is under development, until the package is distributed from pypi, execute:

```bash
pip install m2cypto
pip install https://github.com/eblanium/qchainpy/raw/master/dist/qchainpy-0.0.1-py3-none-any.whl
```
You will have errors on `m2cypto`, follow the installation guide on [this page](https://gitlab.com/m2crypto/m2crypto/-/blob/master/INSTALL.rst).

## QChain API Requirements

1. In order to use QChain API, you need a QNode wallet running on Windows Server machine. 

    1) Use [Amazon EC2 free tier](https://aws.amazon.com/ec2/?ec2-whats-new.sort-by=item.additionalFields.postDateTime&ec2-whats-new.sort-order=desc) to start. Exaple AMI: Windows_Server-2012-R2_RTM-English-64Bit-Base-2021.06.09
    2) [Download QNode wallet](https://qchain.ai/dashboard/downloads)
    3) Install it inside the dedicated folder of the disk `C:\QNode\`


2. Generate a private key for transfer and contract interactions:
```bash
# transfer
openssl genrsa -out transfer.key 2048
openssl rsa -in transfer.key -pubout -out transfer.pub

# contract
openssl genrsa -out contract.key 2048
openssl rsa -in contract.key -pubout -out contract.pub
```
3. Put inside your QNode folder:
```
C:\QNode\> dir
qnode.main.exe
transfer.pub    <-- Recently generated
contract.pub    <-- Recently generated
libeay32.dll    <-- Copy from dll/ of the repo
ssleay32.dll    <-- Copy from dll/ of the repo
...blockain folders
```

## Transfer
Use this to transfer tokens from your node to any node.

Put `transfer.key` inside your project, initiate `qchainpy.Client` and make a transfer:
```
# Transfer

import os
from pathlib import Path
from qchainpy.client import Client

# Get full key_path inside current folder
key_path = os.path.join(Path(__file__).resolve().parent, 'transfer.key')

# Get IP or domain of your node
api_url = 'NODE_URL/api/'

# Initialize Client
client = Client(
    api_url=api_url,
    key_path=key_path,
    passphrase=None
).get_client()

# Transfer funds to some node_id, address is not supported yet
response = client.transfer(
    token='ebl',
    amount=0.01,
    recipient=12345  # node_id
)
print(response.get('success')) >> 'true'
```

## Payments
Use this to interact with contracts: create payments and check their statuses.

Put `contract.key` inside your project, initiate `qchainpy.Client` and make a transfer:
```
# Contract

import os
from pathlib import Path
from qchainpy.client import Client

# The same steps as for Transfer
key_path = os.path.join(Path(__file__).resolve().parent, 'contract.key')
api_url = 'NODE_URL/api/'
client = Client(
    api_url=api_url,
    key_path=key_path,
    passphrase=None
).get_client()

# Create payment
response = client.create_payment(
   payment_index=0, #Local payment index
   contract='payments/contract', 
   token='ebl',
   amount=0.01,
   sender=0,  # node_id or address
   recipient=1  # node_id or address
)
payment_index = response.get('index')
print(payment_index) >> 3888839

# Get payment and check its status
response = client.get_payment(
   payment_index=payment_index,
   contract='payments/contract',
)
print(response.get('payment')) 
>> {
      'index': 3888839, 
      'payment': 0, 
      'account': 1, 
      'status': 'paid', 
      'amount': 10, 
      'currency': 'EBL', 
      'time': '2021-08-18T07:34:23.000Z'
   }
```