from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'bio',
        'role',
        'is_staff',
    )
    search_fields = ('username', 'bio',)


admin.site.register(User, UserAdmin)
