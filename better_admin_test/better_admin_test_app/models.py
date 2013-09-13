from django.db import models


"""
This file contains a test database. The purpose is to test
as many as possible from the available model field types in
order to get maximum coverage for the tests. We need only 
test for field that render differently. The code for rendering
fields lies in templates/better_admin/field.html. I have tried 
to group the fields accordingly. 

+AutoField

SmallIntegerField
+IntegerField
BigIntegerField
PositiveIntegerField
PositiveSmallIntegerField
+CommaSeparatedIntegerField
+DecimalField
+FloatField

+BooleanField
+NullBooleanField

+DateField
+DateTimeField
TimeField

+FileField
FilePathField
+ImageField

+IPAddressField
GenericIPAddressField
+EmailField
+URLField

+CharField
+TextField
SlugField

+ForeignKey
+ManyToManyField
+OneToOneField
"""


def get_file_path(instance, filename):
    return 'library/%s' % filename 


class Company(models.Model):
    name = models.CharField(max_length=30)
    address = models.TextField()
    url = models.URLField()
    ip_address = models.IPAddressField()
    volume = models.IntegerField()
    revenue = models.FloatField()

    def __unicode__(self):
        return self.name


class KAM(models.Model):
    user = models.OneToOneField('auth.User')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    snap = models.ImageField(upload_to=get_file_path) 
    permanent = models.BooleanField()
    sales = models.DecimalField(decimal_places=2, max_digits=16)
    joining = models.DateField()

    def __unicode__(self):
        return self.name


class Tariff(models.Model):
    company = models.ForeignKey(Company)
    kams = models.ManyToManyField(KAM)
    valid_from = models.DateTimeField()
    expired = models.NullBooleanField()
    rates = models.FileField(upload_to=get_file_path)
    codes = models.CommaSeparatedIntegerField(max_length=256)

    def __unicode__(self):
        return '%s - %s' % (self.company, self.valid_from)