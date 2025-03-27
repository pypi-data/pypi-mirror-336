from dataclasses import dataclass


@dataclass
class CloudBucket:
    name: str
    region: str
