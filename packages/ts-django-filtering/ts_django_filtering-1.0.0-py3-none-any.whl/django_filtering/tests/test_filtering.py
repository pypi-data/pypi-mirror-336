from django.test import TestCase

from .. import FilterSet, Filter
from ..models import Requirement, Job, Person


class TestFiltering(TestCase):
    def setUp(self):
        self.requirements = Requirement.objects.bulk_create([
            Requirement(
                details=f"REQ{i}"
            ) for i in range(0, 3)
        ])

        self.jobs = Job.objects.bulk_create([
            Job(
                name=f"JOB{i}",
                value=i,
                requirement=self.requirements[i],
            ) for i in range(0, 3)
        ])

        self.people = Person.objects.bulk_create([
            Person(
                name=name,
                value=idx,
                job=self.jobs[idx]
            ) for idx, name in enumerate(["Joe Mama", "Ben Bunger", "Larry"])
        ])

    def test_filtering(self):
        filter_1 = Filter(
            path="name",
            operator="exact",
            value="Joe Mama"
        )
        filter_2 = Filter(
            path="job.name",
            operator="exact",
            value="JOB1"
        )
        filter_3 = Filter(
            path="job.requirement.details",
            operator="exact",
            value="REQ2"
        )
        filter_4 = Filter(
            path="name",
            operator="contains",
            value="TEST BAD DATA",
        )
        filter_5 = Filter(
            path="job.value",
            operator="gte",
            value="1",
        )

        a = FilterSet(filters=[filter_1]).filter(Person)
        b = FilterSet(filters=[filter_2]).filter(Person)
        c = FilterSet(filters=[filter_3]).filter(Person)
        d = FilterSet(filters=[filter_4]).filter(Person)
        e = FilterSet(filters=[filter_5]).filter(Person)

        self.assertQuerySetEqual(a, [Person.objects.get(pk=1)])
        self.assertQuerySetEqual(b, [Person.objects.get(pk=2)])
        self.assertQuerySetEqual(c, [Person.objects.get(pk=3)])
        self.assertQuerySetEqual(d, [])
        self.assertQuerySetEqual(list(e), [Person.objects.get(pk=2), Person.objects.get(pk=3)])
