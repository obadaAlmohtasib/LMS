from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from courses.models import User, Experience, ScientificDegree, Certificate, TrainingCourse
from courses.forms import UserForm, ExperienceForm, ScientificDegreeForm, CertificateForm, TrainingCourseForm
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


def get_users(request):
    users = User.objects.all()
    return render(request, 'courses/users/list_users.html', { 
        'title': "المدرّبين", # "users",        
        'data': users, 
    })


# @never_cache
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        # print(form.cleaned_data) # object has no attribute 'cleaned_data' 
        # The is_valid method runs validation and returns a boolean value. 
        # During the call of the is_valid method Django runs the data cleaning process,  
        # Cleaning up data means converting it from strings to pyhton objects.
        # Note the cleaned_data attribute is only available after the form has been cleaned.
        if form.is_valid():
            user_instance = form.save()

            # Experiences
            i = 1
            while True:
                mapping = {}
                mapping.update({'company_name': request.POST.get(f"company-name-{i}", None)})
                mapping.update({'role': request.POST.get(f"role-{i}", None)})
                mapping.update({'start_date': request.POST.get(f"start-date-{i}", None)})
                mapping.update({'end_date': request.POST.get(f"end-date-{i}", None)})
                mapping.update({'description': request.POST.get(f"description-{i}", None)})
                mapping.update({'user': user_instance.id})
                exp_form = ExperienceForm(mapping)
                if not exp_form.is_valid():
                    break
                exp_form.save()
                i += 1

            # Scientific Degrees
            i = 1
            while True:
                mapping = {}
                mapping.update({'sci_degree': request.POST.get(f"sci-degree-{i}", None)})
                mapping.update({'educational_institution': request.POST.get(f"educational-institution-{i}", None)})
                mapping.update({'major': request.POST.get(f"major-{i}", None)})
                mapping.update({'year_obtained': request.POST.get(f"year-obtained-{i}", None)})
                mapping.update({'grade': request.POST.get(f"grade-{i}", None)})
                mapping.update({'user': user_instance.id})
                sci_degree_form = ScientificDegreeForm(mapping)
                if not sci_degree_form.is_valid():
                    break
                sci_degree_form.save()
                i += 1

            # Certificates
            i = 1
            while True:
                mapping = {}
                mapping.update({'certificate': request.POST.get(f"c-certificate-{i}", None)})
                mapping.update({'certif_provider': request.POST.get(f"c-certif-provider-{i}", None)})
                mapping.update({'year_obtained': request.POST.get(f"c-year-obtained-{i}", None)})
                mapping.update({'validity': request.POST.get(f"c-validity-{i}", None)})
                mapping.update({'user': user_instance.id})
                certif_form = CertificateForm(mapping)
                if not certif_form.is_valid():
                    break
                certif_form.save()
                i += 1

            # Training Courses
            i = 1
            while True:
                mapping = {}
                mapping.update({'name': request.POST.get(f"crs-name-{i}", None)})
                mapping.update({'party': request.POST.get(f"crs-party-{i}", None)})
                mapping.update({'start_date': request.POST.get(f"crs-start-date-{i}", None)})
                mapping.update({'end_date': request.POST.get(f"crs-end-date-{i}", None)})
                mapping.update({'description': request.POST.get(f"crs-description-{i}", None)})
                mapping.update({'user': user_instance.id})
                training_course_form = TrainingCourseForm(mapping)
                if not training_course_form.is_valid():
                    break
                training_course_form.save()
                i += 1
                
            return render(request, 'courses/users/create_user.html', context={ 
                'entity_name': 'user',
                'success': True
            })

        
    return render(request, 'courses/users/create_user.html', context={
        'form':UserForm(),
        'success': False 
    })


def edit_user(request, id):
    if request.method == "POST":
        obj = User.objects.get(pk=id)
        form = UserForm(request.POST, instance=obj) 
        experiences = Experience.objects.filter(user_id=obj.id)
        if form.is_valid():
            user_instance = form.save()

            #
            # Experiences
            experiences = Experience.objects.filter(user_id=user_instance.id)
            i = 1
            while True:
                mapping = {}
                mapping.update({'company_name': request.POST.get(f"company-name-{i}", None)})
                mapping.update({'role': request.POST.get(f"role-{i}", None)})
                mapping.update({'start_date': request.POST.get(f"start-date-{i}", None)})
                mapping.update({'end_date': request.POST.get(f"end-date-{i}", None)})
                mapping.update({'description': request.POST.get(f"description-{i}", None)})
                mapping.update({'user': user_instance.id})
                #Update - Old/Exist
                if i-1 < len(experiences):
                    exp_form = ExperienceForm(mapping, instance=experiences[i-1])
                #Create - New
                else:
                    exp_form = ExperienceForm(mapping)
                
                if not exp_form.is_valid():
                    break
                exp_form.save()
                i += 1
            
            #Delete
            while i-1 < len(experiences):
                experiences[i-1].delete()
                i += 1

            #
            # Scientific Degrees
            sci_degrees = ScientificDegree.objects.filter(user_id=user_instance.id)
            i = 1
            while True:
                mapping = {}
                mapping.update({'sci_degree': request.POST.get(f"sci-degree-{i}", None)})
                mapping.update({'educational_institution': request.POST.get(f"educational-institution-{i}", None)})
                mapping.update({'major': request.POST.get(f"major-{i}", None)})
                mapping.update({'year_obtained': request.POST.get(f"year-obtained-{i}", None)})
                mapping.update({'grade': request.POST.get(f"grade-{i}", None)})
                mapping.update({'user': user_instance.id})
                #Update - Old/Exist
                if i-1 < len(sci_degrees):
                    sci_degree_form = ScientificDegreeForm(mapping, instance=sci_degrees[i-1])
                #Create - New
                else:
                    sci_degree_form = ScientificDegreeForm(mapping)
                
                if not sci_degree_form.is_valid():
                    break
                sci_degree_form.save()
                i += 1

            #Delete
            while i-1 < len(sci_degrees):
                sci_degrees[i-1].delete()
                i += 1

            #
            # Certificates
            certificates = Certificate.objects.filter(user_id=user_instance.id)
            i = 1
            while True:
                mapping = {}
                mapping.update({'certificate': request.POST.get(f"c-certificate-{i}", None)})
                mapping.update({'certif_provider': request.POST.get(f"c-certif-provider-{i}", None)})
                mapping.update({'year_obtained': request.POST.get(f"c-year-obtained-{i}", None)})
                mapping.update({'validity': request.POST.get(f"c-validity-{i}", None)})
                mapping.update({'user': user_instance.id})
                print(i, request.POST.get(f"c-certificate-{i}"))
                print(mapping)
                #Update - Old/Exist
                if i-1 < len(certificates):
                    certif_form = CertificateForm(mapping, instance=certificates[i-1])
                #Create - New
                else:
                    certif_form = CertificateForm(mapping)
                
                if not certif_form.is_valid():
                    break
                print("SAVE")
                certif_form.save()
                i += 1

            #Delete
            while i-1 < len(certificates):
                print("DELETE")
                certificates[i-1].delete()
                i += 1

            #
            # Training Courses
            training_courses = TrainingCourse.objects.filter(user_id=user_instance.id)
            i = 1
            while True:
                mapping = {}
                mapping.update({'name': request.POST.get(f"crs-name-{i}", None)})
                mapping.update({'party': request.POST.get(f"crs-party-{i}", None)})
                mapping.update({'start_date': request.POST.get(f"crs-start-date-{i}", None)})
                mapping.update({'end_date': request.POST.get(f"crs-end-date-{i}", None)})
                mapping.update({'description': request.POST.get(f"crs-description-{i}", None)})
                mapping.update({'user': user_instance.id})
                #Update - Old/Exist
                if i-1 < len(training_courses):
                    training_course_form = TrainingCourseForm(mapping, instance=training_courses[i-1])
                #Create - New
                else:
                    training_course_form = TrainingCourseForm(mapping)
                
                if not training_course_form.is_valid():
                    break
                training_course_form.save()
                i += 1

            #Delete
            while i-1 < len(training_courses):
                training_courses[i-1].delete()
                i += 1


        return render(request, "courses/users/edit_user.html", {
            "success": True
        })
    
    else:
        obj = User.objects.get(pk=id)
        form = UserForm(instance=obj)
        experiences = Experience.objects.filter(user=obj)
        experiences_forms = []
        for exp in experiences:
            experiences_forms.append(ExperienceForm(instance=exp))

        sci_degrees = ScientificDegree.objects.filter(user=obj)
        sci_degrees_forms = []
        for sci_degree in sci_degrees:
            sci_degrees_forms.append(ScientificDegreeForm(instance=sci_degree))

        certificates = Certificate.objects.filter(user=obj)
        certificates_forms = []
        for certif in certificates:
            certificates_forms.append(CertificateForm(instance=certif))

        training_courses = TrainingCourse.objects.filter(user=obj)
        training_courses_forms = []
        for training_course in training_courses:
            training_courses_forms.append(TrainingCourseForm(instance=training_course))

        return render(request, "courses/users/edit_user.html", {
            "request_handler": "edit_user", 
            "id": id, 
            "form": form,
            "experiences_forms": experiences_forms, 
            "sci_degrees_forms": sci_degrees_forms, 
            "certificates_forms": certificates_forms, 
            "training_courses_forms": training_courses_forms, 
            "success": False
        })


def delete_user(request, id):
    if request.method == "DELETE":
        instance = User.objects.get(pk=id)
        instance.is_deleted = True 
        instance.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })
    
