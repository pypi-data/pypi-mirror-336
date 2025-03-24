from .bm25s_retriever import BM25SRetriever, BM25SRetrieverConfig
from .dense_retriever import DenseRetriever, DenseRetrieverConfig
from .elastic_retriever import ElasticRetriever, ElasticRetrieverConfig
from .retriever_base import (
    EditableRetriever,
    EditableRetrieverConfig,
    RetrieverBase,
    RetrieverBaseConfig,
    LocalRetriever,
    LocalRetrieverConfig,
    RETRIEVERS,
)
from .typesense_retriever import TypesenseRetriever, TypesenseRetrieverConfig
from .web_retrievers import (
    SimpleWebRetriever,
    SimpleWebRetrieverConfig,
    WikipediaRetriever,
    WikipediaRetrieverConfig,
)
from .hyde_retriever import HydeRetriever, HydeRetrieverConfig


RetrieverConfig = RETRIEVERS.make_config(config_name="RetrieverConfig", default=None)


__all__ = [
    "BM25SRetriever",
    "BM25SRetrieverConfig",
    "EditableRetriever",
    "EditableRetrieverConfig",
    "LocalRetriever",
    "LocalRetrieverConfig",
    "RetrieverBase",
    "RetrieverBaseConfig",
    "DenseRetriever",
    "DenseRetrieverConfig",
    "ElasticRetriever",
    "ElasticRetrieverConfig",
    "TypesenseRetriever",
    "TypesenseRetrieverConfig",
    "SimpleWebRetriever",
    "SimpleWebRetrieverConfig",
    "RETRIEVERS",
    "RetrieverConfig",
    "WikipediaRetriever",
    "WikipediaRetrieverConfig",
    "HydeRetriever",
    "HydeRetrieverConfig",
]
