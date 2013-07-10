from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def get_fields(self):
        fields = Publisher._meta.fields
        return [(f.name, f.value_to_string(self)) for f in fields]

    def __unicode__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

    def get_fields(self):
        fields = Author._meta.fields
        return [(f.name, f.value_to_string(self)) for f in fields]

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()

    def get_fields(self):
        fields = Book._meta.fields
        return [(f.name, f.value_to_string(self)) for f in fields]

    def __unicode__(self):
        return self.title
