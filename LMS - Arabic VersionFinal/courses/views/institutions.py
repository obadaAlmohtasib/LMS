from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from courses.models import *
from courses.forms import *
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

# Create your views here.
def index(request):
    # return render(request, template_name='courses/index.html')
    # return HttpResponseRedirect("get_institutions") # more cost
    # institutions = Institution.objects.all()
    return render(request, 'courses/index.html', {
        'title': "مدرسة سلاح الإشارة",
        # 'data': institutions,
    })


def get_institutions(request):
    institutions = Institution.objects.all()
    return render(request, 'courses/institutions/institutions_table.html', {
        'title': "الأقسام", # "Institutions",
        'data': institutions,
    })


# @never_cache
def create_institution(request):
    response = None

    if request.method == "POST":
        form = InstitutionForm(request.POST)
        # print(form.cleaned_data) # object has no attribute 'cleaned_data'
        # The is_valid method runs validation and returns a boolean value.
        # During the call of the is_valid method Django runs the data cleaning process, 
        # Cleaning up data means converting it from strings to pyhton objects.
        # Note the cleaned_data attribute is only available after the form has been cleaned.
        if form.is_valid():
            form.save()
            response = render(request, 'courses/institutions/create_institution.html', context={
                'request_handler': "create_institution",
                'entity_name': 'Institution',
                'success': True
            })


    if not response:
        response = render(request, 'courses/institutions/create_institution.html', context={
            'request_handler': 'create_institution',
            'form':InstitutionForm(),
            'success': False
        })

    headers = getattr(response, "headers", None)
    if headers:
        headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        headers["Pragma"] = "no-cache"
        headers["Expires"] = "0"


    return response


def edit_institution(request, id):
    if request.method == "POST":
        obj = Institution.objects.get(pk=id)
        form = InstitutionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

        return render(request, "courses/institutions/edit_institution.html", {
            "success": True
        })
    
    else:
        obj = Institution.objects.get(pk=id)
        form = InstitutionForm(instance=obj)
        return render(request, "courses/institutions/edit_institution.html", {
            "request_handler": "edit_institution",
            "id": id,
            "form": form,
            "success": False
        })


def delete_Institution(request, id):
    if request.method == "DELETE":
        instance = Institution.objects.get(pk=id)
        instance.is_deleted = True 
        instance.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })
    

