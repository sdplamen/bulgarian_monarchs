from django.contrib import admin
from .models import Monarch, Capital

# Register your models here.
@admin.register(Monarch)
class MonarchAdmin(admin.ModelAdmin):
    ...
@admin.register(Capital)
class CapitalAdmin(admin.ModelAdmin):
    ...
