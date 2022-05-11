from django.contrib import admin
from django.http import HttpResponse
from .models import User, Request

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "name", "username", "created_at")
    readonly_fields = ("user_id", "username", "created_at")
    fields = ("user_id", "name", "username", "created_at")

@admin.register(Request)
class RequestAdmine(admin.ModelAdmin):
    list_display = ( "id", "name_product","created_at", "updated_at", "name_user", "type_request", "quantity", "promptness", "comment", "status", )
    list_filter = ("promptness", "status")
    readonly_fields = ("name_user", "type_request", "quantity", "promptness", "comment", 'fieldname_download')
    fields = ("name_user", "type_request", "quantity", "promptness", "comment", "status", 'fieldname_download')

admin.site.site_header = 'Админка бота'
