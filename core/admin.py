from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import Profile,League, Answer, Question, Room, User
# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['user_id','facebook_name']
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        (_('Personal Info'), {'fields': ('facebook_name', 'facebook_image', 'facebook_id', 'friend','flag',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', )})
    )

    add_fieldsets = (

        (None, {
            'classes': ('wide', ),
            'fields': ('user_id', 'password1', 'password2')
            }),

    )

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(League)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Room)

# admin.site.register(User)
