from django.contrib import admin

# Register your models here.
from .models import User, Request

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "name", "username", "created_at")

@admin.register(Request)
class RequestAdmine(admin.ModelAdmin):
    list_display = ("id","name_user", "type_request", "quantity", "promptness",
                        "comment", "readiness", "path_to_file")
    list_filter = ("promptness", "readiness")
    fields = ("readiness",)
 