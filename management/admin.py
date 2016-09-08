from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from management.models import *


class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)
    
class CarouselAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('create_time',)
    fields = ('title',  'img', 'summary')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Comic)
admin.site.register(Img)
admin.site.register(Carousel, CarouselAdmin)