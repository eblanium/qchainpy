# Usage
## Installation
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


2. If you plan to use contracts, you need to create one in QNode:
   1) Open QNode
   2) Open Product tab
   3) Select QContracts
   4) Press "Create Contract now"
   5) Put names for `Contract` (ie: `eblanium`) and Vendor (ie: Eblanium.com)
   6) Pay QDT to create contract
   7) Done


3. Generate a private key for transfer and payments interactions:
```bash
# transfer
openssl genrsa -out transfer.key 2048
openssl rsa -in transfer.key -pubout -out transfer.pub

# payments, contractname = eblanium in Eblanium case
openssl genrsa -out payments-contractname.key 2048
openssl rsa -in payments-contractname.key -pubout -out payments-contractname.pub
```
4. Put inside your QNode folder:
```
C:\QNode\> dir
qnode.main.exe
transfer.pub                  <-- Recently generated
payments-contractname.pub     <-- Recently generated
libeay32.dll    <-- Copy from dll/ of the repo
ssleay32.dll    <-- Copy from dll/ of the repo
...blockain folders
```
5. Done

## Client

In order to make requests, initialize `qchainpy.Client` with appropriate private key.
```python
import os
from pathlib import Path
from qchainpy.client import Client

# Get full path inside current folder
# transfer.key for Transfer
# payments-contractname.key for Payments
key_path = os.path.join(Path(__file__).resolve().parent, '[PRIVATE].key')

# Get IP or domain of your node
api_url = 'NODE_URL/api/'

# Initialize Client
client = Client(
    api_url=api_url,
    key_path=key_path,
    passphrase=None
).get_client()
```


## Transfer
Transfer tokens from your node to any node.

```python
# Transfer funds to some node_id, address is not supported yet
response = client.transfer(
    token='ebl',
    amount=0.01,
    recipient=12345  # node_id
)
print(response.get('success')) >> 'true'
```

## Payments
Interact with contracts: create payments and check their statuses.

### Get index
Index is used to search for transactions after creating a payment.

> Each time you call `client.get_payments()`, it returns you `index`, store it in your DB.
```python
# Payments
# Get index to search for transactions after creating a payment
response = client.get_payments(
   contract='payments/contractname'
)
transactions_index = response.get('index')
```

### Create payment
1. Generate local_payment_id in your DB
2. Create payment with local_payment_id
```python
# Payments
# Create payment
response = client.create_payment(
   contract='payments/contractname', 
   token='ebl',
   amount=0.01,
   sender=0,  # node_id or address
   recipient=1,  # node_id or address
   local_payment_id=123456789,  # Local payment id, which you store in DB
)
print(response.get('success')) >> 'true'
```

### Get all payments
Returns all payments of a contract.

> It will take long when payments list grows, use `get_payments(local_payment_id, index)` instead.
```python
# Payments
# Get payments
response = client.get_payments(
   contract='payments/contractname'
)
print(response) 
>> {
      'success': 'true',
      'payments': [{
         'index': 3888839, 
         'payment': 123456789, 
         'account': 1, 
         'status': 'paid', 
         'amount': 10, 
         'currency': 'EBL', 
         'time': '2021-08-18T07:34:23.000Z'
      },{
         'index': 3895925, 
         'payment': 151242141, 
         'account': 1, 
         'status': 'declain', 
         'amount': 10, 
         'currency': 'EBL', 
         'time': '2021-10-18T07:34:23.000Z'
      }...],
      'index': 3000999
   }
   
```

### Get payment with `local_payment_id` and `index`
Index is `transactions_index` we get before.
```python
# Payments
# Get payments with params
response = client.get_payments(
   contract='payments/contractname',
   local_payment_id=123456789,
   index=transactions_index
)
print(response) 
>> {
      'success': 'true',
      'payments': [{
         'index': 3888839, 
         'payment': 123456789, 
         'account': 1, 
         'status': 'paid', 
         'amount': 10, 
         'currency': 'EBL', 
         'time': '2021-08-18T07:34:23.000Z'
      }],
      'index': 3200999
   }
```
> You can still call `client.get_payments()` with `contract` and `local_payment_id`, but it will take long.