from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import ImageFields
from .forms import ImageForm



def home(request):
    img = ImageFields.objects.all()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ImageForm()
    return render(request, 'home.html', {'form': form, 'img': img})



def delete_image(request, id):
    if request.method == "POST":
        img = get_object_or_404(ImageFields, id=id)
        img.delete()
    return redirect("home")  