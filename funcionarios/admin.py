from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'salary', 'work_section']

admin.site.register(Employee, EmployeeAdmin)

# Register your models here.
