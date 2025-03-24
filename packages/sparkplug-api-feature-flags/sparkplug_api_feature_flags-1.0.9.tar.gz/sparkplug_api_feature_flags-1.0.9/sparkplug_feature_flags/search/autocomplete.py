from typing import TYPE_CHECKING

from elasticsearch_dsl.query import Q
from sparkplug_core.pagination import SearchPagination

from ..documents import FeatureFlag

if TYPE_CHECKING:
    from django_elasticsearch_dsl.search import Search


def autocomplete(
    term: str,
) -> "Search":
    # Edge ngram
    query = Q(
        "match",
        title__edge_ngram=term,
    )

    start = 0
    end = SearchPagination.page_size - 1

    return FeatureFlag.search().query(query)[start:end]
