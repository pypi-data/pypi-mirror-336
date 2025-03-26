import operator
from dataclasses import dataclass
from datetime import datetime, date
from functools import reduce
from typing import Literal, get_args, Union, Type, TypeVar

from django.db import models
from django.db.models.query import QuerySet

Value = str | int | float | datetime | date | None
T = TypeVar("T", bound=models.Model)

# TODO: implement Q based querying for inverse lookups
Lookup = Literal[
    "exact",
    "iexact",
    "contains",
    "icontains",
    "in",
    "gt",
    "gte",
    "lt",
    "lte",
    "startswith",
    "istartswith",
    "endswith",
    "iendswith",
    "range",
    "date",
    "year",
    "iso_year",
    "month",
    "day",
    "week",
    "week_day",
    "iso_week_day",
    "quarter",
    "time",
    "hour",
    "minute",
    "second",
    "isnull",
    "regex",
    "iregex",
]


@dataclass
class Filter:
    path: str
    operator: Lookup
    value: Value | list[Value]

    def __post_init__(self):
        if self.operator not in get_args(Lookup):
            raise ValueError(f"Invalid Django lookup: {self.operator}")

    @property
    def json(self) -> dict:
        return {f"{self.path.replace('.', '__')}__{self.operator}": self.value}

    @staticmethod
    def merge_to_dict(*filters: Union["Filter", list["Filter"]]) -> dict:
        return reduce(operator.ior, [i.json for sub in filters for i in (sub if isinstance(sub, list) else [sub])], {})

    @staticmethod
    def from_list(*filter_dicts: dict | list[dict]) -> list["Filter"]:
        return [Filter(**_filter) for sub in filter_dicts for _filter in (sub if isinstance(sub, list) else [sub])]


@dataclass
class FilterSet:
    filters: list[Filter]

    def filter(self, model: Type[T]) -> QuerySet[T]:
        return model.objects.filter(**Filter.merge_to_dict(self.filters))
