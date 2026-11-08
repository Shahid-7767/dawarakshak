
from .block import Block
from .consensus import FourValidatorConsensus
from database.db import get_db
from psycopg.types.json import Jsonb


class Blockchain:

    def __init__(self):
        self.consensus = FourValidatorConsensus()
        self.blocks = []
        self.load_blocks()

    def load_blocks(self):
        """Load previously saved blocks from Neon."""

        db = get_db()

        try:
            rows = db.execute("""
                SELECT block_index, timestamp, transactions,
                       previous_hash, block_hash
                FROM blockchain_blocks
                ORDER BY block_index ASC
            """).fetchall()

            if not rows:
                genesis = Block(
                    0,
                    [{
                        "type": "GENESIS",
                        "message": "PharmaTrace ledger initialized"
                    }],
                    "0"
                )

                db.execute("""
                    INSERT INTO blockchain_blocks
                    (block_index, timestamp, transactions,
                     previous_hash, block_hash)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    genesis.index,
                    genesis.timestamp,
                    Jsonb(genesis.transactions),
                    genesis.previous_hash,
                    genesis.hash
                ))

                db.commit()
                self.blocks = [genesis]

            else:
                for row in rows:
                    block = Block(
                        row["block_index"],
                        row["transactions"],
                        row["previous_hash"],
                        row["timestamp"]
                    )

                    if block.hash != row["block_hash"]:
                        raise ValueError(
                            "Stored blockchain data failed hash verification."
                        )

                    self.blocks.append(block)

        finally:
            db.close()

        if not self.is_valid():
            raise ValueError("Blockchain integrity verification failed.")

    def add_transaction(self, transaction, votes=None):

        votes = votes if votes is not None else [
            True, True, True, True
        ]

        decision = self.consensus.evaluate(votes)

        if not decision["accepted"]:
            return {
                "accepted": False,
                "reason": decision["message"],
                "consensus": decision
            }

        block = Block(
            len(self.blocks),
            [transaction],
            self.blocks[-1].hash
        )

        db = get_db()

        try:
            db.execute("""
                INSERT INTO blockchain_blocks
                (block_index, timestamp, transactions,
                 previous_hash, block_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                block.index,
                block.timestamp,
                Jsonb(block.transactions),
                block.previous_hash,
                block.hash
            ))

            db.commit()

        finally:
            db.close()

        self.blocks.append(block)

        return {
            "accepted": True,
            "block_index": block.index,
            "block_hash": block.hash,
            "consensus": decision
        }

    def is_valid(self):

        for index, block in enumerate(self.blocks):

            if block.hash != block.calculate_hash():
                return False

            if index > 0:
                if block.previous_hash != self.blocks[index - 1].hash:
                    return False

        return True
