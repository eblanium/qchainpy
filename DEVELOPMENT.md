# Development
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