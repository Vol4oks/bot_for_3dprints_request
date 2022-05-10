from django.contrib import admin
from django.http import HttpResponse
from .models import User, Request

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "name", "username", "created_at")

@admin.register(Request)
class RequestAdmine(admin.ModelAdmin):
    list_display = ("id","name_user", "type_request", "quantity", "promptness", "comment", "readiness", )
    list_filter = ("promptness", "readiness")
    readonly_fields = ("name_user", "type_request", "quantity", "promptness", "comment", 'fieldname_download')
    fields = ("name_user", "type_request", "quantity", "promptness", "comment", "readiness", 'fieldname_download')
    