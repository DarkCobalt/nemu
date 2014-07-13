from django.contrib import admin
from models import *


class AssignedAdmin(admin.ModelAdmin):
    list_display = ['project_id', 'display_user', 'chapter_id']
    search_fields = ['project_id']
    save_on_top = True


admin.site.register(Role)
admin.site.register(Assigned, AssignedAdmin)
admin.site.register(RoleInAssigned)
