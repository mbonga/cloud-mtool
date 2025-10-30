import threading
from typing import Dict, Type


class SingletonMeta(type):
    """Thread-safe implementation of Singleton.

    Use as metaclass for classes that should only have one instance.
    """

    _instances: Dict[Type, object] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # fast path
        if cls in cls._instances:
            return cls._instances[cls]

        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
