from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.conf import settings


class UserModelAdmin(BaseUserAdmin):
  list_display = ('id', 'email', 'name','display_avatar' ,'phone_no', 'is_user','is_agent','is_admin','is_sub_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name', 'phone_no','image')}),
      ('Permissions', {'fields': ('is_admin','is_sub_admin','is_user','is_agent','groups')}),
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  # filter_horizontal = ('groups', 'user_permissions')

  def display_avatar(self, obj):
        avatar_url = obj.image.url if obj.image else settings.DEFAULT_UNKNOWN_PERSON_IMAGE_URL
        return format_html('<img src="{}" width="50" height="50" />', avatar_url)

  display_avatar.short_description = 'Avatar'

admin.site.register(User, UserModelAdmin)

