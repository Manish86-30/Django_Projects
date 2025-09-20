from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Employee
import openpyxl



def read_data(request):
    employees_list = Employee.objects.all().order_by("id")
    paginator = Paginator(employees_list, 5)

    page_number = request.GET.get("page")
    form = paginator.get_page(page_number)

    return render(request, 'app/home.html', {'form': form})


def create_data(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        new = Employee.objects.create(First_Name=first_name, Last_Name=last_name, Email=email, Mobile=mobile, Address=address, City=city, State=state, Pincode=pincode)
        new.save()
        return redirect('read')
    

def update_data(request, id):
    form = Employee.objects.get(id=id)

    if request.method == "POST":
        form.First_Name = request.POST.get("first_name")
        form.Last_Name = request.POST.get("last_name")
        form.Email = request.POST.get("email")
        form.Mobile = request.POST.get("mobile")
        form.Address = request.POST.get("address")
        form.City = request.POST.get("city")
        form.State = request.POST.get("state")
        form.Pincode = request.POST.get("pincode")

        form.save()
        return redirect("read")
    
    return render(request, 'app/home.html', {'form': form})


def delete_data(request, id):
    emp = Employee.objects.get(pk=id)
    emp.delete()
    return redirect("read")



def delete_all(request):
    if request.method == "POST":
        Employee.objects.all().delete()
        return redirect('/')


def export_excel(request):
    wb = openpyxl.Workbook()  
    ws = wb.active
    ws.title = "Employees"


    headers = ["ID", "First Name", "Last Name", "Email", "Mobile", "Address", "City", "State", "Pincode"]
    ws.append(headers)


    for emp in Employee.objects.all():
        ws.append([emp.id, emp.First_Name, emp.Last_Name, emp.Email, emp.Mobile, emp.Address, emp.City, emp.State, emp.Pincode])


    response = HttpResponse(content_type='app/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
    wb.save(response)
    return response