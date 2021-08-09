# QChainPy [under development]

This is a Python package to interact with [QChain](https://qchain.ai) blockchain API.

Requires `python3`.

## Supported methods

### `client.transfer`
Transfer funds from your node to any node.

## Usage
The package is under development, the only way to use it — is to clone the `src` folder, append `requirements.txt` to your project's requirements and run `pip install -r requirements.txt`.

*This will be fixed soon* and the package will be distributed from pypi repo.

1. In order to use QChain API you need a QNode wallet running on Windows Server machine. 

    1) Use [Amazon EC2 free tier](https://aws.amazon.com/ec2/?ec2-whats-new.sort-by=item.additionalFields.postDateTime&ec2-whats-new.sort-order=desc) to start. Exaple AMI: Windows_Server-2012-R2_RTM-English-64Bit-Base-2021.06.09
    2) [Download QNode wallet](https://qchain.ai/dashboard/downloads)
    3) Install it inside the dedicated folder of the disk `C:\QNode\`


2. Generate a private key for transfer:
```bash
openssl genrsa -out transfer.key 2048
openssl rsa -in transfer.key -pubout -out transfer.pub
```
3. Put inside your QNode folder:
```
C:\QNode\> dir
qnode.main.exe
transfer.pub    <-- Recently generated
libeay32.dll    <-- Copy from dll/ of the repo
ssleay32.dll    <-- Copy from dll/ of the repo
...blockain folders
```

4. Put `transfer.key` inside your project, initiate `qchainpy.Client` and make a transfer:
```
# Example

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
    recipient='37542'
)
print(response.get('success')) >> 'true'
```


## Development
1. Fork the repo.

2. Use new virtual environment.
```python
pip install -r requirements.txt
```

3. Write new classes in `src/qchainpy`.


4. Write unit tests in `tests` using environment variables.


5. Test against your node:

Put `private.key` in `tests/keys` and run:
```python
API_URL='NODE_URL' TOKEN='YOUR_TOKEN' pytest
```

6. Make [an issue](https://github.com/eblanium/qchainpy/issues).

## Support
* _Preferred_. Make [an issue](https://github.com/eblanium/qchainpy/issues).
* Write to [dev@eblanium.com](mailto:dev@eblanium.com) with subject: QChainPY

## Made with 💙 by @EblaniumTeam
* Visit [eblanium.com](https://eblanium.com)
* Join our telegram channel: [@eblanium_news](https://t.me/eblanium_news)
* Telegram chat: [@eblanium_chat](https://t.me/eblanium_chat)

## More API packages:
* [QChainPHP](https://github.com/qchainai/QchainPHP)