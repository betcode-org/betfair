class Available:
    prices: list
    deletion_select: int
    reverse: bool
    serialise: list
    def __init__(self, prices: list, deletion_select: int, reverse: bool = False): ...
    def sort(self) -> None: ...
    def clear(self) -> None: ...
    def update(self, book_update: list) -> None: ...