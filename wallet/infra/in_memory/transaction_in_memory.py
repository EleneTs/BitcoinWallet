from dataclasses import dataclass, field
from typing import List

from wallet.core.transaction.transaction import ITransaction, Transaction
from wallet.core.transaction.transaction_interactor import \
    TransactionRepository


@dataclass
class TransactionRepositoryInMemory(TransactionRepository):
    transactions: List[ITransaction] = field(default_factory=list)

    def create_transaction(
        self, wallet_from: str, wallet_to: str, amount: float
    ) -> int:
        transaction_id = len(self.transactions) + 1
        transaction = Transaction(
            wallet_from=wallet_from,
            wallet_to=wallet_to,
            amount=amount,
            id=transaction_id,
        )
        self.transactions.append(transaction)
        return transaction_id

    def fetch_transactions(self, wallet_address) -> list[ITransaction]:
        fetched_transactions: list[ITransaction] = []
        for transaction in self.transactions:
            if (
                transaction.get_wallet_to() == wallet_address
                or transaction.get_wallet_from() == wallet_address
            ):
                fetched_transactions.append(transaction)

        return fetched_transactions
