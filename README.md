# QChainPy [under development]

This is a Python package to interact with [QChain](https://qchain.ai) blockchain API.

Requires `python3`, `m2crypto` with `openssl`.

## Supported methods

### `client.transfer(token, amount, recipient)`
Transfer funds from your node to any node.

### `client.create_payment(payment_index, contract, token, amount, sender, recipient)`
Create payment using a smart contract.

### `client.get_payment(payment_index, contract)`
Get specific payment of a smart contract.

### `client.get_payments(contract)`
Get all payments of a smart contract.

## Usage
Read [Usage Guidelines](USAGE.md)

## Development
Read [Development Guidelines](USAGE.md)

## Support
* _Preferred_. Make [an issue](https://github.com/eblanium/qchainpy/issues).
* Write to [dev@eblanium.com](mailto:dev@eblanium.com) with subject: QChainPY

## Made with 💙 by @EblaniumTeam
* Visit [eblanium.com](https://eblanium.com)
* Join our telegram channel: [@eblanium_news](https://t.me/eblanium_news)
* Telegram chat: [@eblanium_chat](https://t.me/eblanium_chat)

## More API packages:
* [QChainPHP](https://github.com/qchainai/QchainPHP)