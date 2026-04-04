class Environment:
    _instance = None

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__dict__.update(kwargs)
        return cls._instance
