# ts-django-filtering

In-house solution for kwarg and attribute access based filtering 
of Django ORM models.

## Install

```sh
$ pip install ts-django-filtering
```

## Usage

```python
from my_app.models import Person
from django_filtering import Filter, FilterSet

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

filters = Filter.from_list(my_filters)
print(Filter.merge_to_dict(*filters))
# {'job__name__iexact': 'Engineer', 'job__requirement__name__icontains': 'Plumbing'}

print(FilterSet(filters=filters).filter(Person))
# <QuerySet [<Person: Person object (1)>]>
```
