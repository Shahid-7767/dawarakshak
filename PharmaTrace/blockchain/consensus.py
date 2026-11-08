from .validators import DEFAULT_VALIDATORS

class FourValidatorConsensus:
    """
    Educational, deterministic 3-of-4 validator consensus simulation.
    This is NOT a production Byzantine fault tolerant protocol or a
    distributed Proof-of-Authority network.
    """
    def __init__(self, validators=None, threshold=3):
        self.validators = validators or DEFAULT_VALIDATORS
        self.threshold = threshold
        if len(self.validators) != 4 or threshold != 3:
            raise ValueError("This demo requires exactly four validators and a 3-of-4 threshold.")

    def evaluate(self, votes):
        if len(votes) != 4 or not all(type(vote) is bool for vote in votes):
            raise ValueError("Exactly four boolean votes are required.")
        approvals = sum(votes)
        return {
            "accepted": approvals >= self.threshold,
            "approvals": approvals,
            "required": self.threshold,
            "votes": [
                {"validator_id": validator.validator_id,
                 "name": validator.display_name,
                 "approved": vote}
                for validator, vote in zip(self.validators, votes)
            ],
            "message": "Consensus reached" if approvals >= self.threshold else "Consensus not reached"
        }
