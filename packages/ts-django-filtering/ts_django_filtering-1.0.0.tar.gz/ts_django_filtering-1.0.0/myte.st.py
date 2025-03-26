from django.db import models
from functools import reduce
import operator

def merge(*args: str | list[str]) -> dict:
	return reduce(operator.ior, [{i: "1"} for sub in args for i in (sub if isinstance(sub, list) else [sub])], {})

print(merge(["a", "b", "c"]))
print(merge("a", "b", "c"))
print(merge("a", "b", "c", ["d", "e", "f"]))


from django_filtering import Filter, models

my_filters = [
    {
        "path": "job.name",
        "operator": "iexact",
        "value": "Engineer"
    },
    {
        "path": "job.requirement.name",
        "operator": "icontains",
        "value": "Plumbing"
    },
]

print(Filter.merge_to_dict(Filter.from_list(my_filters)))