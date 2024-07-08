from django.shortcuts import render
from ..models import Source
from ..forms import SourceForm, EditSourceForm
from django.http import JsonResponse


def get_user_sources(request):
    sources = Source.objects.all()
    return render(request, template_name="courses/user_sources/list_user_sources.html", context={
        "data": sources
    })


def create_user_source(request):
    if request.method == "POST":
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()

            return render(request, "courses/user_sources/create_user_source.html", {
                "success": True
            })
    
    return render(request, "courses/user_sources/create_user_source.html", {
        'form': SourceForm(),
        "success": False
    })


def edit_user_source(request, user_source_id):
    if request.method == "POST":
        obj = Source.objects.get(pk=user_source_id)
        form = EditSourceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

            return render(request, "courses/user_sources/edit_user_source.html", {
                "success": True
            })

    obj = Source.objects.get(pk=user_source_id)
    form = EditSourceForm(instance=obj)
    return render(request, "courses/user_sources/edit_user_source.html", { 
        "id": user_source_id, 
        "form": form,
        "success": False
    })


def delete_user_source(request, user_source_id):
    if request.method == "DELETE":
        source = Source.objects.get(pk=user_source_id)
        source.is_deleted = True 
        source.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })
