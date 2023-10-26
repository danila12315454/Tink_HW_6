from typing import Dict


class DataManager:
    _data_dict: Dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        self._data_dict[key] = value

    def get(self, key: str) -> str | bool:
        if key in self._data_dict:
            return self._data_dict[key]
        return False
