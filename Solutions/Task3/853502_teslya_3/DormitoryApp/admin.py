from gevent import pool

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserCreationFormAdmin, MyUserChangeForm
from .models import User, Room, CheckInEntry, RentEntry, RulesEntry, WorkEntry, MessageTo
from .utils import Sender


def send_email_to_user(modeladmin, request, queryset):
    p = pool.Pool(10)
    p.map(Sender(request), queryset)


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationFormAdmin
    form = MyUserChangeForm
    model = User
    actions = [send_email_to_user]

    list_display = ['username', 'room', 'middle_name', 'telephone', 'faculty', 'position', 'verified']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('room', 'middle_name', 'telephone', 'faculty', 'position', 'current_clocks')}),
    )
    readonly_fields = ('verified',)
    # this will allow to change these fields in admin module


admin.site.register(MessageTo)
admin.site.register(User, MyUserAdmin)
admin.site.register(Room)
admin.site.register(CheckInEntry)
admin.site.register(RentEntry)
admin.site.register(RulesEntry)
admin.site.register(WorkEntry)


# Register your models here.
