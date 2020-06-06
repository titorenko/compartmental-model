from typeguard import typechecked
from typing import List, Dict, Any
from abc import ABC, abstractmethod
import pandas as pd
import os
import pickle


@typechecked
class ModelResultStore(ABC):
    @abstractmethod
    def store(self, model_id: str, result_id: str, obj: Any):
        pass

    @abstractmethod
    def load(self, model_id: str, result_id: str) -> Any:
        pass

    @abstractmethod
    def exists(self, model_id: str, result_id: str) -> bool:
        pass


@typechecked
class SimpleModelResultStore(ModelResultStore):

    local_path_suffix = '../../result_store'

    def store(self, model_id: str, result_id: str, obj: Any):
        p = self._path(f"{model_id}_{result_id}.pkl")
        with open(p, 'wb') as handle:
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, model_id: str, result_id: str) -> Any:
        p = self._path(f"{model_id}_{result_id}.pkl")
        with open(p, 'r') as handle:
            pickle.load(handle)

    def exists(self, model_id: str, result_id: str) -> bool:
        p = self._path(f"{model_id}_{result_id}.pkl")
        return os.path.exists(p)

    def _path(self, name: str) -> pd.DataFrame:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        base_dir = os.path.join(__location__, self.local_path_suffix)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, name)
