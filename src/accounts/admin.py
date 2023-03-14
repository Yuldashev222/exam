from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from accounts.models import CustomUser

admin.site.unregister(Group)


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'email', 'first_name', 'last_name', 'phone_number', 'is_active']
    list_display_links = ['group_name', 'first_name', 'last_name', 'phone_number', 'email']
    list_filter = ['group__name']
    list_editable = ['is_active']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    fields = [
        'group',
        ('email', 'password'),
        ('first_name', 'last_name'),
        'phone_number',
        'is_active',
        'date_joined',
        'last_login',
    ]
    readonly_fields = [
        'last_login',
        'date_joined'
    ]

    def save_model(self, request, obj, form, change):
        if not obj.pk or obj.pk and obj.password != CustomUser.objects.get(pk=obj.pk).password:
            obj.password = make_password(obj.password)
        obj.save()

    @admin.display
    def group_name(self, obj):
        return obj.group.name if obj.group else None

    def get_queryset(self, request):
        q = super().get_queryset(request)
        return q.filter(is_staff=False).select_related('group')
