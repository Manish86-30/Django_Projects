from django.contrib import admin
from .models import Employee_Data


@admin.register(Employee_Data)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'First_Name', 'Last_Name', 'Email', 'Mobile', 'Address', 'City', 'State', 'Pincode')
