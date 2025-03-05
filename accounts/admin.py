from django.contrib import admin
from accounts.models import User,Reward, UserRedeem,UserReward
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.conf import settings


class UserModelAdmin(BaseUserAdmin):
  list_display = ('id', 'email', 'name','display_avatar' ,'phone_no','is_staff', 'is_user','is_agent','is_admin','is_sub_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name', 'phone_no','image','address')}),
      ('Permissions', {'fields': ('is_admin','is_user','is_agent','is_sub_admin','groups')}),
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


class RewardAdmin(admin.ModelAdmin):
    model  =Reward
    list_display =['id','percentage']
admin.site.register(Reward,RewardAdmin)

class UserRewardAdmin(admin.ModelAdmin):
    model  = UserReward
    list_display =['user','points','total_transaction_amount']
admin.site.register(UserReward,UserRewardAdmin)


class UserRedeemAdmin(admin.ModelAdmin):
    model = UserRedeem
    list_display =['reward','redeem_points','redeem_date']
admin.site.register(UserRedeem, UserRedeemAdmin)