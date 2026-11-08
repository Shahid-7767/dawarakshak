from dataclasses import dataclass

@dataclass(frozen=True)
class Validator:
    validator_id: str
    display_name: str

DEFAULT_VALIDATORS = [
    Validator("VAL-01", "Validator Alpha"),
    Validator("VAL-02", "Validator Beta"),
    Validator("VAL-03", "Validator Gamma"),
    Validator("VAL-04", "Validator Delta"),
]
