from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from courses.models import ClassEntry, Timing, ClassSchedule, User, Source, CourseGroup, Topic, Commitment, PublicHolidays
from courses.forms import ClassEntryForm, ClassEntryEditForm 
from django.http import JsonResponse 
from datetime import datetime, timedelta, date 
from django.db.models import Q 
from django.db import connection 


def get_daily_entries(request):
    # daily_entries = ClassEntry.objects.all() #.prefetch_related("lecturers") 

    #Display only today' classes
    daily_entries = ClassEntry.objects.filter(entry_date=date.today())

    return render(request, "courses/daily_entries/daily_entries_layout.html", {
        "title": "الحصص اليومية", # "Daily Entries",
        "data": daily_entries,
    })


# Not thread-safe method 
# This method cannot be accessed by multiple threads once, that will result in inconsistent data,
# Because we didn't access the database inside the loop, and totally depend on the previous result stored in memory 
def create_daily_entry(request):
    if request.method == "POST":
        data = request.POST.copy()
        form = ClassEntryForm(data)
        if form.is_valid():
            # Custom validation 
            # 1. Validate date
            entry_date = data.get('entry_date', 0)
            entry_date = datetime.strptime(entry_date, "%Y-%m-%d")
            timing_id = data.get('timing', 0)
            timing_set = Timing.objects.filter(id__exact=timing_id, start_date__lte=entry_date, end_date__gte=entry_date)
            timing = timing_set[0] if timing_set.exists() else None 
            if not timing:
                raise Exception("Date doesn't belongs to any season!, Enter Valid date Or update course's seasons data")
            
            break_start = timing.break_time
            delta = timedelta(minutes=timing.break_duration)
            break_end = (datetime(1, 1, 1, hour=break_start.hour, minute=break_start.minute) + delta).time()

            # 2. Validate class schedule 
            class_schedule_id = data.get('class_schedule', 0)
            class_schedule = ClassSchedule.objects.get(id=class_schedule_id)
            # Is it in break_time (Overlapped)?
            skd_start = class_schedule.start_time
            delta = timedelta(minutes=class_schedule.class_duration)
            skd_end = (datetime(1, 1, 1, hour=skd_start.hour, minute=skd_start.minute) + delta).time()

            if skd_start >= break_start and skd_start < break_end: 
                #overlapped
                raise Exception(f"The time is reserved, The break starts at {break_start}, end at {break_end}")

            if break_start >= skd_start and break_start < skd_end:
                #overlapped
                raise Exception(f"The time is reserved, The break starts at {break_start}, end at {break_end}")        
            
            # 2. Validate uniqueness of class schedule 
            # [delegated to db] => unique constraint         


            # 3. Validate under the limit  [ Number of Remaining Classes ]
            group_id = data.get('course_group', None)
            topic_id = data.get('topic', None)
            topic = Topic.objects.get(pk=topic_id)
            total = topic.no_of_classes  
            classes = ClassEntry.objects.filter(course_group_id=group_id, topic_id=topic.id)
            remaining_classes = total - len(classes)
            if remaining_classes < 1:
                raise Exception(f"You have reached the target number of classes")
            

            # 4. Validate users are free 
            users_ids = data.getlist('users', None)

            if len(users_ids) > len(set(users_ids)):
                raise Exception("There is a duplicate in user list") #Multiple select for the same user

            # if topic.t_type == Topic.Type.EXAM:
            # Users 
            users = list_inactive_user(class_schedule.id, entry_date)
            # duplicates 
            for user in users:
                if str(user.id) in users_ids:
                    raise Exception(f'The user: {user.name} is busy for another class')

            
            # 5. Validate Not in Public Holidays
            holidays = PublicHolidays.objects.filter(course_id=topic.course_id)
            for ph in holidays:
                if entry_date.date() >= ph.start_date and entry_date.date() <= ph.end_date:
                    raise Exception(f'You cannot give a class on: {entry_date.date()}, There is public holiday: {ph.event_name}')

            #IMPORTANT
            # Django Many To Many Insert Ordering
            # Django doesn't guarantee to preserve the order of many-to-many relationships. 
            # If you need this, you should use a through table with an explicit 'order' field.
            # instance = form.save(commit=True) # will take care of all entities
            #When use commit=False
            #A save_m2m() method added to the form which can be called after the instance is saved manually at a later time.
            #Or u can provide your custom save for m2m fields (Note: you don't have to worry about One-to-Many,)
            instance = form.save(commit=False) 
            instance.save()
            count = 0
            for uid in users_ids:
                if not count:
                    Commitment(user_id=uid, class_entry=instance, role=Commitment.Role.PRIMARY).save()
                else:
                    Commitment(user_id=uid, class_entry=instance, role=Commitment.Role.ASSISTANT).save()
                count += 1

            repeat_times = int(data.get("repeat_times", 0))
            for _ in range(1, repeat_times):
                entry_date = data.get("entry_date", None)
                entry_date = datetime.strptime(entry_date, "%Y-%m-%d")
                class_schedule_id = data.get("class_schedule", None)
                class_num = class_schedule.class_num
                class_schedule = ClassSchedule.objects.get(timing_id=timing_id, class_num=class_num+1)
                data.update({"class_schedule" : class_schedule.id})
                
                # Is it in break_time (Overlapped)?
                skd_start = class_schedule.start_time
                delta = timedelta(minutes=class_schedule.class_duration)
                skd_end = (datetime(1, 1, 1, hour=skd_start.hour, minute=skd_start.minute) + delta).time()

                if skd_start >= break_start and skd_start < break_end: 
                    #overlapped
                    raise Exception(f"The time is reserved, The break starts at {break_start}, end at {break_end}")

                if break_start >= skd_start and break_start < skd_end:
                    #overlapped
                    raise Exception(f"The time is reserved, The break starts at {break_start}, end at {break_end}")
                    
                # 2. Validate uniqueness of class schedule 
                # [delegated to db] => unique constraint                 
                
                # 3. Validate under the limit  [ Number of Remaining Classes ]
                remaining_classes -= 1 
                if remaining_classes < 1:
                    raise Exception(f"You have reached the target number of classes")
                                                
                # 4. Validate users are free 
                # if topic.t_type == Topic.Type.EXAM:
                # Users 
                users = list_inactive_user(class_schedule.id, entry_date)
                # duplicates 
                for user in users:
                    if str(user.id) in users_ids:
                        raise Exception(f'The user: {user.name} is busy for another class')
            
                # 5. Validate Not in Public Holidays 
                for ph in holidays:
                    if entry_date.date() >= ph.start_date and entry_date.date() <= ph.end_date:
                        raise Exception(f'You cannot give a class on: {entry_date.date()}, There is public holiday: {ph.event_name}')
                
                form = ClassEntryForm(data)
                instance = form.save(commit=False) 
                instance.save()
                count = 0
                for uid in users_ids:
                    if not count:
                        Commitment(user_id=uid, class_entry=instance, role=Commitment.Role.PRIMARY).save()
                    else:
                        Commitment(user_id=uid, class_entry=instance, role=Commitment.Role.ASSISTANT).save()
                    count += 1
            
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    return HttpResponseRedirect(reverse("get_daily_entries"))


def edit_daily_entry(request, entry_id):
    instance = ClassEntry.objects.get(pk=entry_id) 
    if request.method == "POST": 
        form = ClassEntryEditForm(request.POST, instance=instance)
        if form.is_valid():
            # 1.
            # entry_date = form.get('entry_date')
            # IN form.get('timing')
            # NOT in PublicHolidays
            
            # 2.
            # form.get('course_group')
            # form.get('topic')
            # NOT exceeded limit

            # 3. 
            # ClassSchedule 
            # NOT in timing' break_time

            users = []
            # NOTE: cleaned_data will change the order of users in the list 
            new_users = form.cleaned_data["users"]

            #Time changed [do not ignore pre-selected users] 
            # new_date and new_schedule 
            if 'entry_date' in form.changed_data or 'class_schedule' in form.changed_data:
                users = list_inactive_user(instance.class_schedule.id, instance.entry_date)

            #Time is the same [exclude pre-selected users]
            # old_date and old_schedule
            else: 
                pre_selected = instance.users.all().values("id") #This
                users = list_inactive_user(instance.class_schedule.id, instance.entry_date).exclude(id__in=pre_selected)

            for u in new_users:
                if u in users:
                    raise Exception(f'The user: {u.name} is busy for another class')            
            
            instance = form.save(commit=False) 
            instance.save()

            # Using .order_by('id') => So, the first go first, the second go second, and so on...
            commitments = Commitment.objects.filter(class_entry_id=instance.id).order_by('id') #To change them in order 
            
            # NOTE: form.cleaned_data returns different order of users in the list 
            new_users = request.POST.getlist('users', None) #So pick the original 

            index = 0
            for index in range(0, len(new_users)):
                uid = new_users[index]
                if index < len(commitments):
                    obj = commitments[index]
                    obj.user_id = uid
                    obj.save()
                else:
                    role = Commitment.Role.PRIMARY if index == 0 else Commitment.Role.ASSISTANT
                    Commitment(user_id=uid, class_entry=instance, role=role).save()

            for index in range(len(new_users), len(commitments)):
                commitments[index].delete()

            return render(request, 'courses/daily_entries/edit_entry.html', context={
                'instance': instance,
                'success': True
            })
        else:            
            raise Exception(form.errors.as_data())

    form = ClassEntryEditForm(instance=instance)
    return render(request, "courses/daily_entries/edit_entry.html", context={
            'instance': instance,
            'form': form,
            'success': False,
        })


def delete_daily_entry(request, id):
    if request.method == "DELETE":  
        entry = ClassEntry.objects.get(pk=id)
        entry.is_deleted = True 
        entry.save()
        return JsonResponse({"status_code": 204, })
    else:
        return JsonResponse({"status_code": 400, })
    

def get_related_models(request, crs_id):
    try:
        groups = CourseGroup.objects.filter(course_id=crs_id)
        topics = Topic.objects.filter(course_id=crs_id)
        users = User.objects.all()  
        timings = Timing.objects.filter(course_id=crs_id)
        schedules = ClassSchedule.objects.filter(timing_id__in=timings.values("id"))
        return JsonResponse({"status_code": 200,
                             "data": {
                             "groups": list([group.id, str(group)] for group in groups),
                             "topics": list([topic.id, topic.t_type, str(topic)] for topic in topics),
                             "users": list([user.id, str(user)] for user in users),
                             "timings": list([timing.id, str(timing)] for timing in timings),
                             "schedules": list([schedule.id, str(schedule)] for schedule in schedules), 
                             },})
    except Exception as e:
        print(e)
        print(repr(e))
        return JsonResponse({"status_code": 404,
                             "message": "Something Went Wrong!"})
    

def filter_active_users(request, skd_id):
    try:
        if request.GET:
            date = request.GET["date"]
            _type = request.GET["type"]
            # Exclude busy users from the final result
            excluded_entries = list_inactive_user(skd_id, date).values("id")
            users = User.objects.exclude(id__in=excluded_entries.values("id")).exclude(~Q(source=_type))

            # When apply editing...
            exclude_entry = request.GET.get("exclude-entry", None)
            if exclude_entry is not None and type(exclude_entry) is str: 
                users = users.union(ClassEntry.objects.get(pk=exclude_entry).users.all())
                print("users: ", users)

            return JsonResponse({"status_code": 200,
                                "data": {
                                "users": list([user.id, str(user)] for user in users), 
                                },})
                
    except Exception as e: 
        print(e)
        return JsonResponse({"status_code": 404,
                            "message": str(e)})


def list_inactive_user(skd_id, date): 
    # Filter by date 
    cls_skd = ClassSchedule.objects.get(id=skd_id)
    skd_start = datetime(1, 1, 1, cls_skd.start_time.hour, cls_skd.start_time.minute) 
    skd_end = (skd_start + timedelta(minutes=cls_skd.class_duration)).time()
    skd_start = skd_start.time()
    
    classes = ClassEntry.objects.filter(entry_date=date)
    excluded_entries = []
    for cls in classes:
        if cls.class_schedule is None:
            continue

        cls_start = datetime(1, 1, 1, cls.class_schedule.start_time.hour, cls.class_schedule.start_time.minute)
        cls_end = (cls_start + timedelta(minutes=cls.class_schedule.class_duration)).time()
        cls_start = cls_start.time()
        if cls_start >= skd_start and cls_start < skd_end:
            #overlapped            
            excluded_entries.append(cls)
            continue
                
        if skd_start >= cls_start and skd_start < cls_end: 
            #overlapped
            excluded_entries.append(cls) 
            continue

    # Exclude busy users from the final result
    # List of active [FREE] users 
    # users = User.objects.exclude(id__in=Commitment.objects.filter(class_entry__in=excluded_entries).values("user_id")) 

    # Exclude busy users from the final result
    # List of inactive [BUSY] users 
    sources = Source.objects.filter(can_oversee_multiple_classes=True).all()
    users = User.objects.filter(
        ~Q(source__in=sources), # translated to AND 
        id__in=Commitment.objects.filter(class_entry__in=excluded_entries).values("user_id")
    ) 

    # In-case above not work => Try: 
    # excluded_ids = [e.id for e in excluded_entries]
    # users = User.objects.filter(id__in=Commitment.objects.filter(class_entry_id__in=excluded_ids).values("user_id")) 

    return users 


def get_remaining_classes(request, group_id, topic_id): 
    try:
        if request.method == "GET":
            # Number of Remaining Classes [For a specific topic]
            topic = Topic.objects.get(pk=topic_id) 
            total = topic.no_of_classes
            classes = ClassEntry.objects.filter(course_group_id=group_id, topic_id=topic.id)
                        
            # When apply editing... 
            exclude_entry = request.GET.get("exclude-entry", None)
            if exclude_entry is not None and type(exclude_entry) is str: 
                classes = classes.exclude(pk=exclude_entry)
            
            remaining_classes = total - len(classes)


            return JsonResponse({"status_code": 200, "data": {
                                    "remainingClasses": remaining_classes, 
                                },})
    except Exception as e:    
        return JsonResponse({"status_code": 404,
                                "message": str(e),
                            })
    
def get_valid_classes(request, group_id, timing_id):
    try:
        # Valid classes 
        date = request.GET["date"]
        daily_entries = ClassEntry.objects.filter(course_group_id=group_id, entry_date=date)
        classes = [entry.class_schedule for entry in daily_entries] 
        schedules = ClassSchedule.objects.filter(timing_id=timing_id).exclude(id__in=classes)
        return JsonResponse({"status_code": 200, "data": {
                                "schedules": list([skd.id, str(skd)] for skd in schedules), 
                            },})
    except Exception as e:    
        return JsonResponse({"status_code": 404,
                                "message": str(e),
                            })


def get_schedules(request, season_id):    
    try:
        season = Timing.objects.get(id__exact=season_id)
        # __range(season.start_date, season.end_date)
        date_str = season.start_date.strftime("%Y-%m-%d")        
        schedules = ClassSchedule.objects.filter(timing_id=season)
        return JsonResponse(
            {"status_code": 200,
             "data": {
                 "start_date": date_str, 
                 "schedules": [[skd.id, str(skd)] for skd in schedules],
                 },
            }
        )    
    
    except Exception as e:
        print(e)
        return JsonResponse(
            {"status_code": 404,
            "message": "Something Went Wrong!"
            }
        )
