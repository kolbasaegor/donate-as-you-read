from web3 import Web3
from web3.exceptions import InvalidAddress


def transact(
    web3: Web3,
    from_account: str,
    to_account: str,
    value: float,
    private_key: str,
):
    try:
        transaction = {
            'nonce': web3.eth.get_transaction_count(from_account),
            'to': to_account,
            'from': from_account,
            'value': web3.to_wei(value, 'ether'),
            'gas': 21000,
            'gasPrice': web3.to_wei(40, 'gwei')
        }

        signed_tx = web3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    except InvalidAddress as error:
        return {
            'success': False,
            'details': error
        }
    
    except ValueError as error:
        return {
            'success': False,
            'details': error
        }

    return {
        'success': True,
        'details': {
            'hash': tx_hash.hex()
        }
    }
