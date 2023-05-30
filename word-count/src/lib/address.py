class Address:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

    def __str__(self) -> str:
        return f"{self.ip}:{self.port}"
