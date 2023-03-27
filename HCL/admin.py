from django.contrib import admin

# Register your models here.

from .models import user_info, test_info, contact_info

class User_info(admin.ModelAdmin):
    list_display = ['uname','fname','lname','email','mobile','city']

class Test_info(admin.ModelAdmin):
    list_display = ['testname','fname','lname','email','mobile']

class Contact_info(admin.ModelAdmin):
    list_display = ['name','email','comments']


admin.site.register(user_info, User_info)
admin.site.register(test_info, Test_info)
admin.site.register(contact_info, Contact_info)