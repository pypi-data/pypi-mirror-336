from .annoy_index import AnnoyIndex, AnnoyIndexConfig
from .faiss_index import FaissIndex, FaissIndexConfig
from .index_base import DenseIndexBase, DenseIndexBaseConfig, DENSE_INDEX
from .scann_index import ScaNNIndex, ScaNNIndexConfig


DenseIndexConfig = DENSE_INDEX.make_config(
    default="faiss", config_name="DenseIndexConfig"
)


__all__ = [
    "AnnoyIndex",
    "AnnoyIndexConfig",
    "FaissIndex",
    "FaissIndexConfig",
    "ScaNNIndex",
    "ScaNNIndexConfig",
    "DenseIndexBase",
    "DenseIndexBaseConfig",
    "DENSE_INDEX",
    "DenseIndexConfig",
]
