from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from dateutil import relativedelta
from datetime import datetime
from .managers import WorkerUserManager


class User(AbstractUser):
    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='Slug',
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name=_('Email'),
        unique=True,
    )
    gender = models.CharField(
        max_length=1,
        choices=(
            ('m', _('Man')),
            ('w', _('Women')),
            ('o', _('Other')),
        ),
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=16,
        blank=True,
        null=True,
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Birth date')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = WorkerUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'user'
        unique_together = ('email', 'phone')
        indexes = [
            models.Index(fields=[
                'email',
                'phone',
            ]),
        ]

    def __str__(self):
        try:
            return '{}. {}'.format(
                self.first_name[0] or '',
                self.last_name
            )
        except IndexError:
            return str(self.pk)

    @property
    def age(self):
        if self.birth_date:
            my_birth_date = self.birth_date
            diff = relativedelta.relativedelta(datetime.now(), my_birth_date)

        return diff.years

    def save(self, **kwargs):
        super(User, self).save(**kwargs)
        if not self.slug:
            self.slug = slugify(
                '%s' % (self.username.lower())
            )

        super(User, self).save(**kwargs)


class Address(models.Model):
    user = models.OneToOneField(
        'User',
        null=True,
        on_delete=models.PROTECT,
    )
    address1 = models.CharField(
        max_length=255,
        blank=False
    )
    address2 = models.CharField(
        max_length=255,
        blank=True
    )
    postal_code = models.CharField(
        max_length=255,
        blank=False
    )
    city = models.CharField(
        max_length=255,
        blank=False
    )
    country = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        default='FR',
        verbose_name=_('Country'),
        help_text='ISO Alpha-2'
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name=_('Latitude')
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name=_('Latitude')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        indexes = [
            models.Index(fields=['address1', 'postal_code']),
        ]
        db_table = 'address'

    def __str__(self):
        return '{}. {} - {}'.format(
            self.address1,
            self.city,
            self.country
        )


class Ad(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='Slug',
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        verbose_name=_('Title')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Description')
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        verbose_name=_('Category')
    )
    type = models.CharField(
        max_length=32,
        choices=(
            ('supply', _('Supply')),
            ('demand', _('Demand')),
        ),
        default='supply',
        verbose_name=_('Type')
    )
    status = models.CharField(
        max_length=32,
        choices=(
            ('waiting', _('Waiting')),
            ('online', _('Online')),
            ('cancelled', _('Cancelled')),
        ),
        default='waiting'
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('AD')
        verbose_name_plural = _('Ads')
        db_table = 'ad'
        indexes = [
            models.Index(fields=[
                'title',
                'status',
            ]),
        ]

    def __str__(self):
        return '{} ({})'.format(
            self.title,
            self.pk
        )

    @property
    def is_supply(self):
        if self.type == 'supply':
            return True

    @property
    def is_demand(self):
        if self.type == 'demand':
            return True

    def save(self, **kwargs):
        super(Ad, self).save(**kwargs)
        if not self.slug:
            self.slug = slugify(
                '%s %s' % (self.pk, self.title.lower())
            )

        super(Ad, self).save(**kwargs)


class Mission(models.Model):
    customer = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_('User')
    )
    ad = models.ForeignKey(
        'Ad',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_('Ad')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('Mission')
        verbose_name_plural = _('Missions')
        db_table = 'mission'

    def __str__(self):
        return '{} - {}'.format(
            self.ad,
            self.customer
        )


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('title')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('description')
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = 'category'
        indexes = [
            models.Index(fields=[
                'name',
            ]),
        ]

    def __str__(self):
        return str(self.name)


class Conversation(models.Model):
    ad = models.ForeignKey(
        'Ad',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        db_table = 'conversation'

    def __str__(self):
        return '{} - {}'.format(
            self.pk,
            self.ad
        )


class Message(models.Model):
    sender = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_('User'),
    )
    conversation = models.ForeignKey(
        'Conversation',
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name=_('Conversation')
    )
    content = models.TextField(
        null=False,
        blank=False,
        verbose_name=_('Content')
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_('Updated')
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('Created')
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        db_table = 'message'

    def __str__(self):
        return 'Message - {}'.format(
            self.conversation
        )
