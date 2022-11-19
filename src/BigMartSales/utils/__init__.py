from BigMartSales.utils.common import *
from BigMartSales.constants import *
from pathlib import Path
import numpy as np
import dill

@ensure_annotations
def save_numpy_array_data(file_path: Path, array: np.ndarray):
    """
    Save numpy array data to file
    file_path: Path location of file to save
    array: np.ndarray data to save
    """
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'wb') as file_obj:
        np.save(file_obj, array)

@ensure_annotations
def save_object(file_path:Path,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as file_obj:
        dill.dump(obj, file_obj)

@ensure_annotations
def load_numpy_array_data(file_path: Path) -> np.ndarray:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)

@ensure_annotations
def load_object(file_path:Path):
    """
    file_path: str
    """
    with open(file_path, "rb") as file_obj:
        return dill.load(file_obj)