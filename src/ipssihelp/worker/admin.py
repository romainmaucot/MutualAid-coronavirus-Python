from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from dateutil import relativedelta
from .models import Ad, User, Category, Address, Conversation, Message, Mission


class AdInline(StackedInline):
    model = Ad
    verbose_name_plural = _('Ads')
    show_change_link = True
    extra = 0


class MissionInline(StackedInline):
    model = Mission
    verbose_name_plural = _('Missions')
    show_change_link = True
    extra = 0


class AddressInline(StackedInline):
    model = Address
    verbose_name_plural = _('Addresses')
    show_change_link = True
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', '_name', '_age', 'phone', '_address_full', 'is_staff', 'updated', 'username')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'username')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()
    inlines = [
        AdInline,
        AddressInline,
        MissionInline
    ]

    def _age(self, obj):
        age = '--'
        if obj.birth_date:
            my_birth_date = obj.birth_date
            diff = relativedelta.relativedelta(datetime.now(), my_birth_date)

            age = format_html('<strong>{}</strong> ans'.format(
                diff.years,
            ))
        return age
    _age.short_description = _('Age')

    def _address_full(self, obj):
        output = '{}'.format(
            obj.address
        )
        return output
    _address_full.short_description = _('Address')

    def _name(self, obj):
        output = '{}. {}'.format(
            obj.first_name[0:1],
            obj.last_name
        )
        return output
    _name.short_description = _('Name')


class MissionInline(StackedInline):
    model = Mission
    verbose_name_plural = _('Missions')
    show_change_link = True
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')


class MessageInline(StackedInline):
    model = Message
    verbose_name_plural = _('Messages')
    show_change_link = True
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('ad', 'updated', 'created')
    inlines = [MessageInline]