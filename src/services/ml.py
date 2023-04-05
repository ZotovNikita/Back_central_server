from typing import List


class MLService:
    async def predict(self, bot_guid: str, message: str) -> int:
        intent_rank = 0
        return intent_rank

    async def train(self, bot_guid: str, X: List[str], y: List[int]) -> None:
        print(X)
        print(y)

    async def transfer(self):
        ...
