class Worker:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id = None

    def set_id(self, id):
        self.id = id
