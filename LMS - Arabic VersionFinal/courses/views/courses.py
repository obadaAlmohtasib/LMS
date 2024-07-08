from django.shortcuts import render
from courses.models import Course, Timing, Institution, SuspensionTime, ClassEntry, Topic
from courses.forms import CourseForm, TopicForm, TimingForm 
from django.forms import inlineformset_factory 
from django.http import JsonResponse
from django.db import transaction, connection
from datetime import date, datetime, timedelta
import json


def get_courses(request, id, name):
    # print(id)
    courses = Course.objects.filter(institution_id=id)
    # print(courses)
    # print(connection.queries)
    
    return render(request, 'courses/courses/table_courses.html',  {
        'fileToInclude': './table_courses.html', # For "Generalization"
        'title': f"{name}", #f'Courses from {name}',
        'id': id,
        'data': courses
    })

def get_land_page(request):
    institutions = Institution.objects.all()
    return render(request, 'courses/courses/courses_land_page.html', {
        'institutions': institutions
    })

def create_course(request, inst_id):
    institution = Institution.objects.get(pk=inst_id)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            if institution:
                instance = form.save(commit=False)
                instance.institution = institution 
                instance.save()
                
                return render(request, 'courses/courses/create_course.html', {
                    'request_handler': "create_course",
                    'entity_name': 'Course',
                    'id': inst_id,
                    'institution': institution,
                    'success': True
                })

    return render(request, 'courses/courses/create_course.html',  {        
        'request_handler': "create_course",
        'course_form': CourseForm(), 
        'id': inst_id,
        'institution': institution,
        'success': False
    })


def edit_course(request, crs_id):
    if request.method == "POST":
        obj = Course.objects.get(pk=crs_id)
        form = CourseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()     

            return render(request, "courses/courses/edit_course.html", {
                "course": obj,
                "success": True
            })
    
    obj = Course.objects.get(pk=crs_id)
    form = CourseForm(instance=obj)    
    return render(request, "courses/courses/edit_course.html", {
        "request_handler": "edit_course",
        "id": crs_id,
        "course": obj,
        "form": form,
        "success": False
    })



def delete_course(request, crs_id):
    if request.method == "DELETE":
        instance = Course.objects.get(pk=crs_id)
        instance.is_deleted = True 
        instance.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })
    

def copy_course_page(request):
    institutions = Institution.objects.all()
    return render(request, 'courses/courses/copy_course_page.html', {
        "institutions": institutions
    })


def copy_course_data(request):
    try:
        course_id = request.GET["course"]
        institution_id = request.GET["copy-to-institution"]
        course = Course.objects.get(pk=course_id)
        institution = Institution.objects.get(pk=institution_id)
        
        with transaction.atomic():
            course_form = CourseForm({
                'course_name': 'COPY - ' + course.name, 
                'no_of_classes': course.no_of_classes, 
                'no_daily_classes': course.no_daily_classes,
                'course_start_date': course.start_date,
                'course_end_date': course.end_date
            })
            if course_form.is_valid():
                new_course = course_form.save(commit=False)
                new_course.institution_id = institution.id
                new_course.save()

                topics = course.topic_set.all()
                for topic in topics:
                    topic_form = TopicForm({
                        'name': topic.name, 
                        'no_of_classes': topic.no_of_classes, 
                        't_type': topic.t_type
                    })
                    if topic_form.is_valid():
                        topic = topic_form.save(commit=False)
                        topic.course_id = new_course.id
                        topic.save()
                    else: 
                        raise Exception("Something went wrong, Try again later.")
                # Topic.objects.bulk_create(topics)
                
        return JsonResponse({"status_code": 204, "message": "Data copied successfully." })

    except Exception as e:
        return JsonResponse({"status_code": 400, "message": repr(e) })


def suspend_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        if course.status == Course.Status.SUSPENDED:
            raise Exception("The course is already suspended...")

        course.status = Course.Status.SUSPENDED 
        course.save()
        susp_time = SuspensionTime()
        susp_time.suspended_since = date.today()
        susp_time.course = course
        susp_time.save()

        return JsonResponse({ "status_code": 204, 
                            "course_status": course.status 
                            })
    except Exception as e:
        return JsonResponse({ "status_code": 400, 
                            "course_status": course.status 
                            })


def resume_course(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        if course.status == Course.Status.RUNNING: 
            raise Exception("The course is already running...")
        
        data = json.loads(request.body)
        release_opt = data.get("release_opt", None)
        resume_date = data.get("resume_date", None)
        if None in [release_opt, resume_date]:
            raise Exception("Plz, Provide the required values") 

        remaining_time = ''
        if release_opt == 'custom_date':
            susp_date = SuspensionTime.objects.get(course_id=course_id)
            susp_date.resume_date = resume_date
            susp_date.save()
            resume_date2 = datetime.strptime(susp_date.resume_date, '%Y-%m-%d')
            remaining_time = (resume_date2.date() - susp_date.suspended_since).days

        if release_opt == 'immediately':
            resume_course_helper(course)
            remaining_time = ''


        return JsonResponse({ "status_code": 204, 
                             "course_status": course.status,
                             "remaining_time": remaining_time,
                            })
    
    except Exception as e:
        return JsonResponse({ 
                            "status_code": 400, 
                             "course_status": course.status,
                            })
    


def resume_course_helper(course):
    # 1. Toggle state
    course.status = Course.Status.RUNNING
    course.save()

    # 2. shift days of date
    susp_time = SuspensionTime.objects.get(course_id=course.id)
    entries = ClassEntry.objects.filter(course_id=course.id, entry_date__gt=susp_time.suspended_since)    
    shift_dates(susp_time.suspended_since, entries)


    # 3. DELETE foreign record
    susp_time.is_deleted = True 
    susp_time.save()



def shift_dates(susp_date, entries):    
    day_count = (date.today() - susp_date).days
    single_date = susp_date

    days_to_shift = 0
    delta = timedelta(days=1)

    for _ in range(day_count):
        day = single_date.weekday() # Monday is ZERO, and Sunday is SIX
        if day not in (4, 5): # not in ("Fri.", "Sat.")
            days_to_shift += 1
        # else: 
        #     print("Fri  &  Sat") # skip, # Friday and Saturday

        single_date += delta


    # Shift entries' end date
    for entry in entries:
        count_down = days_to_shift
        while count_down:
        # NOTE: changing the order of the next two statements will change the result
            entry.entry_date += delta # Plus # Go forward
            
            day = entry.entry_date.weekday()
            if day in (4, 5): # Skip [ 'Friday' & 'Saturday' ]
                continue

            count_down -= 1
        entry.save()


