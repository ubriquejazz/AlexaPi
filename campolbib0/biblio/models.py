from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.utils import timezone


class Book(models.Model):
    """
    An Book class - to describe book in the system.
    """
    title = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    # publisher = models.ForeignKey('Publisher')
    author = models.CharField(max_length=200)
    # author = models.ForeignKey('Author')
    # lend_period = models.ForeignKey('LendPeriods')
    # page_amount = models.IntegerField()
    # lend_by = models.ForeignKey('UserProfile', null=True, blank=True)
    # lend_from = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return 'Book: ' + self.title

    class Meta:
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"
