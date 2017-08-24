from datetime import date, timedelta

from django.test import TestCase

from .models import AbstractCondition, ModelForTesting, ConditionForTesting

class ConditionTestCase(TestCase):

    def check_condition(self, cond, instance, begin_date, end_date, value):
        self.assertEquals(cond.instance, instance)
        self.assertEquals(cond.begin_date, begin_date)
        self.assertEquals(cond.end_date, end_date)
        self.assertEquals(cond.value, value)
        
    def test_new(self):

        instance1 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance1,
            value=10
            )

        self.assertEquals(cond.begin_date, date.today())
        self.assertEquals(cond.end_date, date(9999, 12, 31))

    def test_new_inside_condition(self):

        instance1 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance1,
            value=10
            )
        
        cond.save()

        cond = ConditionForTesting(
            instance=instance1,
            value=20,
            begin_date=date.today()+timedelta(days=1),
            end_date=date.today()+timedelta(days=3),
            )

        cond.save()

        conditions = ConditionForTesting.objects.filter(
            instance=instance1).order_by('begin_date')

        self.assertEquals(len(conditions), 3)

        self.check_condition( conditions[0], 
            instance1, date.today(),
            date.today(), 10)

        self.check_condition( conditions[1], 
            instance1, date.today()+timedelta(days=1),
            date.today()+timedelta(days=3), 20)

        self.check_condition( conditions[2], 
            instance1, date.today()+timedelta(days=4),
            date(9999, 12, 31), 10)


    def test_new_outside_condition(self):

        instance1 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance1,
            value=20,
            begin_date=date.today()+timedelta(days=1),
            end_date=date.today()+timedelta(days=3),
            )

        cond.save()

        cond = ConditionForTesting(
            instance=instance1,
            value=10
            )

        cond.save()

        conditions = ConditionForTesting.objects.filter(
            instance=instance1).order_by('begin_date')

        self.assertEquals(len(conditions), 1)

        self.check_condition(conditions[0], 
            instance1, date.today(),
            date(9999, 12, 31), 10)


    def test_new_before_condition(self):

        instance1 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance1,
            value=10
            )
        
        cond.save()

        cond = ConditionForTesting(
            instance=instance1,
            value=20,
            begin_date=date.today()-timedelta(days=1),
            end_date=date.today()+timedelta(days=3),
            )

        cond.save()

        conditions = ConditionForTesting.objects.filter(
            instance=instance1).order_by('begin_date')

        self.assertEquals(len(conditions), 2)

        self.check_condition( conditions[0], 
            instance1, date.today()-timedelta(days=1),
            date.today()+timedelta(days=3), 20)

        self.check_condition( conditions[1], 
            instance1, date.today()+timedelta(days=4),
            date(9999, 12, 31), 10)


    def test_new_after_condition(self):

        instance1 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance1,
            value=20,
            begin_date=date.today()-timedelta(days=2),
            end_date=date.today()+timedelta(days=3),
            )

        cond.save()

        cond = ConditionForTesting(
            instance=instance1,
            value=10
            )
        
        cond.save()

        conditions = ConditionForTesting.objects.filter(
            instance=instance1).order_by('begin_date')

        self.assertEquals(len(conditions), 2)

        self.check_condition( conditions[0], 
            instance1, date.today()-timedelta(days=2),
            date.today()-timedelta(days=1), 20)

        self.check_condition( conditions[1], 
            instance1, date.today(),
            date(9999, 12, 31), 10)


    def test_new_different_instance(self):

        instance1 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance1,
            value=20,
            begin_date=date.today()-timedelta(days=2),
            end_date=date.today()+timedelta(days=3),
            )

        cond.save()

        instance2 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance2,
            value=10
            )
        
        cond.save()

        conditions = ConditionForTesting.objects.filter(
            instance__in=[instance1,instance2]).order_by('begin_date')

        self.assertEquals(len(conditions), 2)

        self.check_condition( conditions[0], 
            instance1, date.today()-timedelta(days=2),
            date.today()+timedelta(days=3), 20)

        self.check_condition( conditions[1], 
            instance2, date.today(),
            date(9999, 12, 31), 10)


    def test_new_same_condition(self):

        instance1 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance1,
            value=10
            )

        cond.save()

        cond = ConditionForTesting(
            instance=instance1,
            value=20
            )

        cond.save()

        conditions = ConditionForTesting.objects.filter(
            instance=instance1).order_by('begin_date')

        self.assertEquals(len(conditions), 1)

        self.check_condition( conditions[0], 
            instance1, date.today(),
            date(9999, 12, 31), 20)


    def test_new_condition_complex(self):

        instance1 = ModelForTesting.objects.create()

        cond = ConditionForTesting(
            instance=instance1,
            value=30,
            begin_date=date.today()-timedelta(days=10),
            end_date=date.today()+timedelta(days=20),
            )

        cond.save()

        cond = ConditionForTesting(
            instance=instance1,
            value=20,
            begin_date=date.today()+timedelta(days=10),
            end_date=date.today()+timedelta(days=30),
            )

        cond.save()

        cond = ConditionForTesting(
            instance=instance1,
            value=10
            )

        cond.save()

        conditions = ConditionForTesting.objects.filter(
            instance=instance1).order_by('begin_date')

        self.assertEquals(len(conditions), 2)

        self.check_condition(conditions[0], 
            instance1, date.today()-timedelta(days=10),
            date.today()-timedelta(days=1), 30)

        self.check_condition(conditions[1], 
            instance1, date.today(),
            date(9999, 12, 31), 10)


