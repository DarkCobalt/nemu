from django.contrib import admin
from models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, )


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)
admin.site.register(ScanlationGroup)
admin.site.register(MangaStatus)
admin.site.register(ChapterStatus)
admin.site.register(Project)
admin.site.register(Chapter)
admin.site.register(ScanlationGroupProjects)
admin.site.register(Role)
admin.site.register(Assigned)
admin.site.register(RoleInAssigned)