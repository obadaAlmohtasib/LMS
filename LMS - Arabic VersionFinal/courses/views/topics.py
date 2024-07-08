from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from courses.models import Institution, Topic, Course, PublicHolidays, CourseGroup, SuspensionTime, ClassEntry, Timing, ClassSchedule 
from courses.forms import TopicForm, PublicHolidaysForm, CourseGroupForm, ClassEntryForm, TimingForm, ClassScheduleForm, CustomBaseInlineFormSet
from django.forms import inlineformset_factory
from urllib import parse
import json
from datetime import date, datetime, timedelta
from django.db import connection

#
# Topics 
def view_course_details_land_page(request):
    institutions = Institution.objects.all()
    return render(request, 'courses/topics/course_details_land_page.html', {
        'institutions': institutions
    })


def get_topics(request, id, name):
    course  = Course.objects.get(pk=id)
    topics = Topic.objects.filter(course_id=id)
    public_holidays = PublicHolidays.objects.filter(course_id=id)
    timings = Timing.objects.filter(course_id=id) 
    course_groups = CourseGroup.objects.filter(course_id=id)
    course_status = course.status
    remaining_time = None   
    if course_status == Course.Status.SUSPENDED:	
        susp_date = SuspensionTime.objects.get(course_id=id)
        resume_date = susp_date.resume_date
        if resume_date is not None:
            suspend_date = susp_date.suspended_since
            remaining_time = (resume_date - suspend_date).days


    return render(request, 'courses/topics/table_course_detail.html',  {
        'fileToInclude': './table_course_detail.html', # For "Generalization"
        'title': f"{course.name}", #f'Topics for {name}',
        'id': id,
        'topics': topics,
        "public_holidays": public_holidays,
        "timings": timings,
        "course_groups": course_groups,
        "public_holidays_form": PublicHolidaysForm(),
        "course_groups_form": CourseGroupForm(),
        "suspended": course_status == Course.Status.SUSPENDED,
        "remaining_time": remaining_time
    })


def create_topic(request, id):
    course = Course.objects.get(pk=id)
    if request.method == "POST":
        form_topic = TopicForm(request.POST)
        if form_topic.is_valid():
            instance_topic = form_topic.save(commit=False)
            instance_topic.course = course
            instance_topic.save()

            return render(request, 'courses/topics/create_topic.html', {
                'request_handler': "create_topic",
                'entity_name': 'Topic',
                'id': id,
                'course': course,
                'success': True
            })

    return render(request, 'courses/topics/create_topic.html',  {        
        'request_handler': "create_topic",
        'topic_form': TopicForm(),
        'id': id,
        'course': course,
        'success': False
    })


def edit_topic(request, id):
    topic_obj = Topic.objects.get(pk=id) 
    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic_obj)
        if form.is_valid():
            form.save()
            return render(request, "courses/topics/edit_topic.html", {
                "topic": topic_obj,
                "success": True
            })

    form = TopicForm(instance=topic_obj)
    return render(request, "courses/topics/edit_topic.html", {
        "request_handler": "edit_topic",
        "id": id,
        "topic": topic_obj,
        "form": form,
        "success": False
    }) 


def delete_topic(request, id):
    if request.method == "DELETE":
        instance = Topic.objects.get(pk=id)
        instance.is_deleted = True 
        instance.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })


#
#
# Timings 
def add_timing(request, crs_id):
    course = Course.objects.get(pk=crs_id) 
    print(course.no_daily_classes)
    if request.method == "POST":
        form = TimingForm(request.POST)
        if form.is_valid():
            if course:
                instance = form.save(commit=False)
                instance.course = course
                instance.save()
                ClassScheduleFormSet = inlineformset_factory(
                    Timing, ClassSchedule, ClassScheduleForm, fields=('class_num', 'start_time',  'class_duration'),
                    min_num=course.no_daily_classes, max_num=course.no_daily_classes
                )
                formset = ClassScheduleFormSet(request.POST, instance=instance)
                for form_b in formset:
                    if form_b.is_valid() and form_b.cleaned_data:
                        form_b.save()
                
                return render(request, 'courses/topics/add_timing.html', {
                    'request_handler': "add_timing",
                    'entity_name': 'Timing',
                    'id': crs_id,
                    'course': course,
                    'success': True
                })

    ClassScheduleFormSet = inlineformset_factory(
        Timing, ClassSchedule, ClassScheduleForm, 
        formset=CustomBaseInlineFormSet, 
        fields=('class_num', 'start_time',  'class_duration'), 
        min_num=course.no_daily_classes, max_num=course.no_daily_classes
        # max_num=len() #(Timing.Season.choices 
    )

    return render(request, 'courses/topics/add_timing.html',  { 
        'request_handler': "add_timing",
        'timing_form': TimingForm(),
        'class_schedule_formset': ClassScheduleFormSet(),
        'id': crs_id,
        'course': course,
        'success': False
    })


def edit_timing(request, timing_id):
    if request.method == "POST":
        obj = Timing.objects.get(pk=timing_id)
        form = TimingForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            ClassScheduleFormSet = inlineformset_factory(
                Timing, ClassSchedule, ClassScheduleForm, fields=('class_num', 'start_time',  'class_duration')
            )
            formset = ClassScheduleFormSet(request.POST, instance=obj)
            for form in formset:
                if form.is_valid() and form.cleaned_data:
                    form.save()       

            return render(request, "courses/topics/edit_timing.html", {
                "timing": obj,
                "success": True
            })
    
    obj = Timing.objects.get(pk=timing_id)
    form = TimingForm(instance=obj)
    ClassScheduleFormSet = inlineformset_factory(
        Timing, ClassSchedule, ClassScheduleForm, 
        formset=CustomBaseInlineFormSet, 
        fields=('class_num', 'start_time',  'class_duration') 
        # max_num=len() #Timing.Season.choices
    )
    formset = ClassScheduleFormSet(instance=obj)
    return render(request, "courses/topics/edit_timing.html", {
        "request_handler": "edit_timing",
        "id": timing_id, 
        "timing": obj,
        "timing_form": form,
        "class_schedule_formset": formset, 
        "success": False
    })


def delete_timing(request, timing_id):
    if request.method == "DELETE":
        instance = Timing.objects.get(pk=timing_id)
        instance.is_deleted = True 
        instance.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })

#
#
# Public Holidays
def add_public_holiday(request, crs_id):
    data_in = request.body # bytes
    # data_out = parse.unquote(data_in) # str
    data_json = json.loads(data_in) # dict
    form = PublicHolidaysForm(data_json)
    if form.is_valid():
        instance = form.save(commit=False)
        course = Course.objects.get(pk=crs_id)
        shift_end_date(course, form.cleaned_data["start_date"], form.cleaned_data["end_date"])
        course.save()
        instance.course = course
        instance.save()

        start_date = datetime.strptime((data_json["event_start_date"]), "%Y-%m-%d").strftime("%b %d, %Y")
        end_date = datetime.strptime(data_json["event_end_date"], "%Y-%m-%d").strftime("%b %d, %Y")       
        return JsonResponse({ "status_code": 201,
                         "data": {
                            "type": "Public Holiday",
                            "object": {
                                'id': instance.id,
                                'event_name': data_json["event_name"],
                                'start_date': start_date,
                                'end_date': end_date,
                            },
                         },})

    # HttpResponseRedirect(redirect_to=("index"))
    return JsonResponse({ "status_code": 400, })



def shift_end_date(course, public_holiday_start_date, public_holiday_end_date):
    if public_holiday_start_date > public_holiday_end_date or \
        public_holiday_end_date < course.start_date:
            return print("Don't Care")            


    #1: public_holiday_start_date < course.start_date < public_holiday_end_date < course.end_date
    if public_holiday_start_date < course.start_date and \
        public_holiday_end_date > course.start_date:
            day_count = (public_holiday_end_date - course.start_date).days + 1 # For the end_date to be included
            single_date = course.start_date
    
    #2: course.start_date < public_holiday_start_date < course.end_date < public_holiday_end_date
    # elif public_holiday_start_date < course.end_date and \
    #     public_holiday_end_date > course.end_date:
    #         day_count = (course.end_date - public_holiday_start_date).days + 1 # For the end_date to be included
    #         single_date = public_holiday_start_date


    #2: 
    # course.start_date < public_holiday_start_date < course.end_date < public_holiday_end_date
    # OR    
    # course.start_date < public_holiday_start_date < public_holiday_end_date < course.end_date
    # Normal case (The public holiday in between the course' start_date and end_date)
    else:
        day_count = (public_holiday_end_date - public_holiday_start_date).days + 1 # For the end_date to be included
        single_date = public_holiday_start_date
        

    # Fetch all prev public holidays, 
    public_holidays = PublicHolidays.objects.filter(course_id=course.id)
    dates = list([public_holiday.start_date, public_holiday.end_date] for public_holiday in public_holidays)

    days_to_shift = 0
    delta = timedelta(days=1)
    # Count public holiday' days
    for i in range(day_count):
        skip = False

        # skip, # pre-exist
        for i in range(len(dates)):
            check_date = lambda date_x: date_x >= dates[i][0] and date_x <= dates[i][1] 
            if check_date(single_date):
                print(single_date) # pre-exist detected
                skip = True
                break

        if skip:
            single_date += delta
            continue

        day = single_date.weekday() # Monday is ZERO, and Sunday is SIX
        if day not in (4, 5): # not in ("Fri.", "Sat.")
            days_to_shift += 1
        else: 
            print("Fri  &  Sat") # skip, # Friday and Saturday

        single_date += delta


    print("Before Start: ", course.end_date)
    print("Days to shift: ", days_to_shift)
    # Shift the course' end date
    while days_to_shift:
        # NOTE: changing the order of the next two statements will change the result
        course.end_date += delta # Plus # Go forward
        day = course.end_date.weekday()
        if day in (4, 5):
            continue

        days_to_shift -= 1

    print("After Finish: ", course.end_date)



    for i in daterange(public_holiday_start_date, public_holiday_end_date):
        print(i)


def daterange(start_date, end_date):
    return []


def delete_public_holiday(request, id):
    if request.method == "DELETE":
        instance = PublicHolidays.objects.get(pk=id)
        course = instance.course
        shift_end_date_back(course, instance.id, instance.start_date, instance.end_date)
        instance.is_deleted = True 
        instance.save()
        course.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })
    


# NOTE:
# The result of shifting the end date back in time, may differ in one or two days, 
# if the original end date was for a friday or saturday, since we are ignoring/skipping these days because they are days off
def shift_end_date_back(course, public_holiday_id, public_holiday_start_date, public_holiday_end_date):
    if public_holiday_start_date > public_holiday_end_date or \
        public_holiday_end_date < course.start_date:
            return print("Don't Care")            

    #1: public_holiday_start_date < course.start_date < public_holiday_end_date < course.end_date
    if public_holiday_start_date < course.start_date and \
        public_holiday_end_date > course.start_date:
            day_count = (public_holiday_end_date - course.start_date).days + 1 # For the end_date to be included
            single_date = course.start_date
    
    #2: 
    # course.start_date < public_holiday_start_date < course.end_date < public_holiday_end_date
    # OR
    # course.start_date < public_holiday_start_date < public_holiday_end_date < course.end_date
    else:
        day_count = (public_holiday_end_date - public_holiday_start_date).days + 1 # For the end_date to be included
        single_date = public_holiday_start_date
        

    # Fetch all public holidays, 
    public_holidays = PublicHolidays.objects.filter(course_id=course.id)
    # Exclude current public holiday
    public_holidays = public_holidays.exclude(id=public_holiday_id)
    dates = list([public_holiday.start_date, public_holiday.end_date] for public_holiday in public_holidays)

    days_to_shift = 0
    delta = timedelta(days=1)
    # Count public holiday' days
    for i in range(day_count):
        skip = False

        # skip, # pre-exist
        for i in range(len(dates)):
            check_date = lambda date_x: date_x >= dates[i][0] and date_x <= dates[i][1] 
            if check_date(single_date):
                print(single_date) # pre-exist detected
                skip = True
                break

        if skip:
            single_date += delta
            continue

        day = single_date.weekday() # Monday is ZERO, and Sunday is SIX
        if day not in (4, 5): # not in ("Fri.", "Sat.")
            days_to_shift += 1
        else: 
            print("Fri  &  Sat") # skip, # Friday and Saturday

        single_date += delta


    print("Before Start: ", course.end_date)
    print("Days to shift: ", days_to_shift)
    # Shift the course' end date
    while days_to_shift:
        # NOTE: changing the order of the next two statements will change the result
        course.end_date -= delta # Minus # Go back
        day = course.end_date.weekday()
        if day in (4, 5):
            continue

        days_to_shift -= 1

    print("After Finish: ", course.end_date)


def add_course_group(request, crs_id):
    course = Course.objects.get(pk=crs_id)
    if request.method == "POST":
        data_json = json.loads(request.body) # bytes
        form = CourseGroupForm(data_json)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.course = course
            instance.save()
            return JsonResponse({ "status_code": 201, 
                                "data": {
                                "type": "Course Group",
                                "object": {
                                    "id": instance.id,
                                    "name": form.cleaned_data.get("name", "new_course_group")
                                },
                            },})

    return JsonResponse({ "status_code": 400 })


def edit_course_group(request, id):
    instance = CourseGroup.objects.get(pk=id)
    
    if request.method == "POST": 
        form = CourseGroupForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            return render(request, 'courses/topics/edit_course_group.html', context={
                "course_group": instance,
                'success': True
            })
    
    form = CourseGroupForm(instance=instance)
    return render(request, "courses/topics/edit_course_group.html", context={
            'success': False,
            "course_group": instance,
            'form': form
        })


def view_course_group(request, id): # course_group_id
    course_group = CourseGroup.objects.get(pk=id)
    entries = ClassEntry.objects.raw(
        f"""
            SELECT * 
            FROM class_entries 
            WHERE course_group_id = {course_group.id} AND is_deleted=False
            ORDER BY 
                CASE WHEN entry_date >= CURRENT_DATE THEN entry_date END ASC, 
                CASE WHEN entry_date < CURRENT_DATE THEN entry_date END DESC;
        """)    

    return render(request, 'courses/topics/course_group_entries.html', context= {
        'entries': entries,
        'course_id': course_group.course_id,
        'course_group_id': course_group.id
    })


def delete_course_group(request, id):
    if request.method == "DELETE":
        instance = CourseGroup.objects.get(pk=id)
        instance.is_deleted = True 
        instance.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })    


def get_daily_entry_form(request, course_group_id):
    course_group = CourseGroup.objects.get(pk=course_group_id)
    return render(request, 'courses/daily_entries/create_entry.html', context= {
        'form': ClassEntryForm(course_group_instance=course_group),
        'course_id': course_group.course_id,
        'course_group_id': course_group.id,
        'callback_path': reverse("view_course_group", kwargs={'id': course_group_id})
    })

