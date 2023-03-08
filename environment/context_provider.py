import os
from typing import Optional


class ContextProvider:
    def get_variable(self, name: str) -> Optional[str]:
        return os.getenv(name)

    def set_variable(self, name: str, value: str):
        os.environ[name] = value
