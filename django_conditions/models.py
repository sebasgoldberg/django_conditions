from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import date, timedelta

INSIDE = 1
OUTSIDE = 2
BEFORE = 3
AFTER = 4


class CurrentManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            begin_date__lte=date.today(),
            end_date__gte=date.today())

class AbstractCondition(models.Model):

    begin_date = models.DateField(_('Fecha de inicio'), default=date.today)
    end_date = models.DateField(_('Fecha de fin'), default=date(9999, 12, 31))
    value = models.DecimalField(max_digits=12, decimal_places=4,
            verbose_name=_('Valor'))

    objects = models.Manager()
    current = CurrentManager()

    class Meta:
        abstract = True
        manager_inheritance_from_future = True

    def get_manager(self):
        return type(self).objects

    def get_intersections(self):
        queryset = self.get_manager().filter(instance=self.instance)
        if self.id is not None:
            queryset = queryset.exclude(id=self.id)
        # Conditions inside self
        for cond in queryset.filter(begin_date__gte=self.begin_date, end_date__lte=self.end_date):
            yield (INSIDE, cond)
        # Conditions outside self
        for cond in queryset.filter(begin_date__lte=self.begin_date, end_date__gte=self.end_date):
            yield (OUTSIDE, cond)
        # Conditions before self
        for cond in queryset.filter(begin_date__lte=self.begin_date, end_date__gte=self.begin_date):
            yield (BEFORE, cond)
        # Conditions after self
        for cond in queryset.filter(begin_date__lte=self.end_date, end_date__gte=self.end_date):
            yield (AFTER, cond)

    def delete_and_divide(self, inside_cond):

        self.delete()

        if self.begin_date < inside_cond.begin_date:
            self.get_manager().create(
                begin_date = self.begin_date,
                end_date = (inside_cond.begin_date - timedelta(days=1)),
                value = self.value,
                instance = self.instance
            )
        

        if self.end_date > inside_cond.end_date:
            self.get_manager().create(
                begin_date = (inside_cond.end_date + timedelta(days=1)),
                end_date = self.end_date,
                value = self.value,
                instance = self.instance
            )

    def change_end_date_or_delete(self, after_cond):
        if self.begin_date < after_cond.begin_date:
            self.end_date = after_cond.begin_date - timedelta(days=1)
            self.save(verify_intersections=False)
        else:
            self.delete()

    def change_begin_date_or_delete(self, before_cond):
        if self.end_date > before_cond.end_date:
            self.begin_date = before_cond.end_date + timedelta(days=1)
            self.save(verify_intersections=False)
        else:
            self.delete()

    def save(self, verify_intersections=True, *args, **kwargs):
        if verify_intersections:
            for inter_type, cond in self.get_intersections():
                if inter_type == INSIDE:
                    cond.delete()
                elif inter_type == OUTSIDE:
                    cond.delete_and_divide(self)
                elif inter_type == BEFORE:
                    cond.change_end_date_or_delete(self)
                elif inter_type == AFTER:
                    cond.change_begin_date_or_delete(self)
                else:
                    raise Exception(_('Caso de intersección no conocido.'))
        super(AbstractCondition, self).save()

