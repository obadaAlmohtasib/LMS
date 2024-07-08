from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from courses.models import Institution, Course, CourseGroup, SuspensionTime, User, Source, Commitment, ClassEntry
from django.http import JsonResponse
from courses.RawSQL import sql_queries, sql_queries_v2, sql_general_report
from datetime import timedelta, datetime, date 


def create_report(request):
    institutions = Institution.objects.all()
    return render(request, "courses/reports/create_report.html", {
        "institutions": institutions
    })


def get_related_courses(request, id):
    try:
        courses = Course.objects.filter(institution_id=id)
        return JsonResponse({"status_code": 200,
                             "data": {
                             "courses": list([course.id, str(course)] for course in courses),
                             },})
    except Exception as e:
        # print(e)
        # print(repr(e))
        return JsonResponse({"status_code": 404,
                             "message": "Something Went Wrong!"})


def get_related_groups(request, id):
    try:
        groups = CourseGroup.objects.filter(course_id=id)        
        return JsonResponse({"status_code": 200,
                             "data": {
                             "groups": list([group.id, str(group)] for group in groups),
                             },})
    except Exception as e:
        # print(e)
        # print(repr(e))
        return JsonResponse({"status_code": 404,
                             "message": "Something Went Wrong!"})

#
# 
def generate_summarized_report(request):
    try:
        id = request.GET["group"]
        group = CourseGroup.objects.get(pk=id)
        course = Course.objects.get(pk=group.course_id)
        entries = sql_queries.course_schedule_view(course_id=group.course.id, group_id=group.id)
        
        # Shift dates, W/O saving
        if course.status == Course.Status.SUSPENDED:
            resume_course_without_save(entries, course.id)

        report = c_report(entries)
        return render(request, "courses/reports/course_summarized_report.html", {
            "course_name": course.name,
            "weeks_count": range(1, len(report)+1), # Number of dict_keys
            'report': report,
        })
    except Exception as e: 
        return HttpResponseRedirect(reverse("get_institutions"))



def c_report(course_entries):
    report = {}
    week = 1    
    entries = course_entries
    entry = 0
    # NOTE: The algorithm is O(n), since we are looping one time over the array.
    while entry < len(entries):
        # Skipping Friday & Saturday in Public_Holidays_set => you may delegate the task to the database
        if entries[entry].entry_date.weekday() in (4, 5): # not in ("Fri.", "Sat."):              
            entry+=1
            continue

        report[week] = {} # Walk through data week by week        
        week_of_year = (entries[entry].entry_date+timedelta(days=1)).strftime("%W")
        while entry < len(entries):
            # Let date as key
            date_key = entries[entry].entry_date.strftime("%b. %d, %Y")
            report[week][date_key] = []
            
            for _ in range(entry, len(entries)):
                changed_key = entries[entry].entry_date.strftime("%b. %d, %Y") # date for the new entry
                if report[week].get(changed_key, -1) == -1:
                    # New date                    
                    break
                else:
                    # Same date - Defined key
                    report[week][date_key].append(entries[entry])
                
                entry += 1

            if entry < len(entries) and \
                ((entries[entry].entry_date+timedelta(days=1)).strftime("%W") != week_of_year or
                 entries[entry-1].entry_date.strftime("%Y") != entries[entry].entry_date.strftime("%Y") or
                 entries[entry].entry_date.weekday() in (4, 5)):
                
                report[week] = fill_date_gap(report[week])

                # New week
                break
        week += 1


    if report:
        report[week-1] = fill_date_gap(report[week-1])

    return report



def generate_detailed_report(request):
    try:
        id = request.GET["group"]
        group = CourseGroup.objects.get(pk=id)
        course = Course.objects.get(pk=group.course_id)
        
        entries = sql_queries_v2.course_schedule_view_2(course_id=course.id, group_id=group.id)

        # Shift dates, W/O saving
        if course.status == Course.Status.SUSPENDED:
            resume_course_without_save(entries, course.id)

        report = c_report_with_time(entries)

        return render(request, "courses/reports/course_detailed_report.html", {
            "course_name": course.name,
            "weeks_count": range(1, len(report)+1), # Number of dict_keys
            'report': report,
            'course': course,
            'group': group,
        })
    except Exception as e:
        print("view: generate_report_v2")
        print("Exception thrown")
        print(repr(e))
        return HttpResponseRedirect(reverse("get_institutions"))


def c_report_with_time(course_entries):
    report = {}
    week = 1    
    entries = course_entries
    entry = 0
    time_list = []
    # NOTE: The algorithm is O(n), since we are looping one time over the array.
    while entry < len(entries):
        # Skipping Friday & Saturday in Public_Holidays_set => you may delegate the task to the database
        if entries[entry].entry_date.weekday() in (4, 5): # not in ("Fri.", "Sat."):              
            entry+=1
            continue

        report[week] = {} # Walk through data week by week        
        week_of_year = (entries[entry].entry_date+timedelta(days=1)).strftime("%W")
        classes_per_day_count = 0
        break_start, break_end = '', ''
        while entry < len(entries):
            # Let date as key
            date_key = entries[entry].entry_date.strftime("%b. %d, %Y")
            report[week][date_key] = []
            
            for _ in range(entry, len(entries)):
                changed_key = entries[entry].entry_date.strftime("%b. %d, %Y") # date for the new entry
                if report[week].get(changed_key, -1) == -1:
                    # New date
                    classes_per_day_count = 0    
                    break
                else:
                    # Same date - Defined key
                    classes_per_day_count += 1
                    # we don't want to override previous time, all classes must [ Start-End ] at the same time
                    # and entries[entry].belongs_to!="PublicHoliday" # because it get '00:00:00' = NO Time
                    if entries[entry].belongs_to!="PublicHoliday" and \
                        classes_per_day_count > len(time_list): # because some days may have more classes
                            # Handle class time [Start - End]                        
                            start_time = entries[entry].start_time
                            delta = timedelta(minutes=entries[entry].class_duration)
                            end_time = (datetime(1, 1, 1, start_time.hour, start_time.minute) + delta).strftime('%H:%M')
                            start_time = start_time.isoformat(timespec='minutes') # convert to "%H:%M" format
                            time_list.append(f"{start_time}-{end_time}")
                                                    
                            # Handle break time [Start - End]
                            break_start = entries[entry].break_time
                            delta = timedelta(minutes=entries[entry].break_duration) 
                            break_end = (datetime(1, 1, 1, break_start.hour, break_start.minute) + delta).strftime("%H:%M")
                            break_start = break_start.isoformat(timespec='minutes') # convert to "%H:%M" format 
                    report[week][date_key].append(entries[entry])
                
                entry += 1

            if entry < len(entries) and \
                ((entries[entry].entry_date+timedelta(days=1)).strftime("%W") != week_of_year or
                 entries[entry-1].entry_date.strftime("%Y") != entries[entry].entry_date.strftime("%Y") or
                 entries[entry].entry_date.weekday() in (4, 5)):
                # New week
                report[week] = fill_date_gap(report[week])
                # time column, must be inserted last for L2R direction 
                # report[week]["Time"] = time_list 

                # time column, must be inserted first for R2L direction 
                # Noting that dictionaries in python are ordered
                report[week] = { "Time": time_list, **report[week] }
                time_list = []
                report[week]["break_time"] = [f"{break_start}-{break_end}"]
                break
        week += 1

    if report and report[week-1].get("Time") is None: # have not processed yet 
        report[week-1] = fill_date_gap(report[week-1])
        # report[week-1]["Time"] = time_list # L2R direction 
        report[week-1] = { "Time": time_list, **report[week-1] } # R2L direction 
        report[week-1]["break_time"] = [f"{break_start}-{break_end}"]

    return report


# Get all dates of week based on a single date
def fill_date_gap(dates):
    single_date = next(iter(dates), None) # Extract one date_key
    if not single_date:
        return 

    date_list = []
    date_time_obj = datetime.strptime(single_date, "%b. %d, %Y")
    weekday = date_time_obj.weekday()

    start_date = None
    if weekday == 6:
        # It's Sunday
        start_date = date_time_obj
    else: 
        # go back to zero, and since 0 is monday, we have to step back -1
        delta = timedelta(days=weekday+1)
        start_date = date_time_obj-delta
    # print("First date in the week: ", start_date)
    
    for i in range(0, 5): # Ignore Friday & Saturday
        delta = timedelta(days=i)
        date_list.append((start_date+delta).strftime("%b. %d, %Y"))

    res = dict()
    for single_date in date_list:
        if single_date in dates:
            # print("Pre-Exist: ", single_date)
            res[single_date] = dates[single_date]
        else:
            # print("Not-Exist: ", single_date)
            res[single_date] = []

    return res


def resume_course_without_save(entries, course_id):
    susp_time = SuspensionTime.objects.get(course_id=course_id)
    entries = [entry for entry in entries if entry.entry_date>=susp_time.suspended_since]
    suspended_since = susp_time.suspended_since
    resume_date = susp_time.resume_date
    if resume_date is None: #Not provided 
        resume_date = date.today()

    shift_dates(suspended_since, resume_date, entries)


def shift_dates(susp_date, resume_date, entries):    
    day_count = (resume_date - susp_date).days
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



def create_general_report(request): 
    institutions = Institution.objects.all()
    return render(request, "courses/reports/create_general_report.html", {
        "institutions": institutions
    })


def generate_general_report(request):
    inst_id = request.GET.get('institution', None)
    date_input = request.GET.get('date-input', None)

    institution = Institution.objects.get(pk=inst_id)
    
    # Check if date is for sunday OR return back in time to the first sunday 
    date_time_obj = datetime.strptime(date_input, "%Y-%m-%d")
    weekday = date_time_obj.weekday()

    start_date = None
    if weekday == 6:
        # It's Sunday
        start_date = date_time_obj.date()
    else: 
        # go back to zero, and since 0 is monday, we have to step back -1
        delta = timedelta(days=weekday+1)
        start_date = (date_time_obj-delta).date()
    # print("First date in the week: ", start_date)

    # Fetch all courses on that date
    entries = sql_general_report.general_report_view(institution.id, start_date) # .strftime('%Y-%m-%d')

    # Manage courses in reports 
    report = make_general_report_with_time(entries)

    # Return template and pass report data to it 
    return render(request, 'courses/reports/general_report.html', { 
        "institution_name": institution.name,
        # "courses_count": range(1, len(report)+1), # Number of dict_keys
        'report': report,
    })



def make_general_report_with_time(course_entries):
    report = {}
    entries = course_entries
    entry = 0
    time_list = []
    # NOTE: The algorithm is O(n), since we are looping one time over the array.
    while entry < len(entries):
        entry_obj = entries[entry]
        group = entry_obj.course_group 
        report[group] = {} # Walk through data group by group         
        classes_per_day_count = 0
        break_start, break_end = '', ''

        # Skipping Friday & Saturday in Public_Holidays_set => you may delegate the task to the database
        # We don't need to perform this step, since the data is already filtered by the database 
        while entry < len(entries):
            # Let date as key
            date_key = entries[entry].entry_date.strftime("%b. %d, %Y")
            report[group][date_key] = [] 

            for _ in range(entry, len(entries)):
                if entry < len(entries) and entries[entry].course_group != group:
                    # New Group 
                    report[group] = fill_date_gap(report[group])
                    # time column, must be inserted last for L2R direction 
                    # report[week]["Time"] = time_list 

                    # time column, must be inserted first for R2L direction 
                    # Noting that dictionaries in python are ordered
                    report[group] = { "Time": time_list, **report[group] }
                    time_list = []
                    report[group]["break_time"] = [f"{break_start}-{break_end}"]
                    break

                changed_key = entries[entry].entry_date.strftime("%b. %d, %Y") # date for the new entry
                if report[group].get(changed_key, -1) == -1:
                    # New date
                    classes_per_day_count = 0    
                    break
                else:
                    # Same date - Defined key
                    classes_per_day_count += 1
                    # we don't want to override previous time, all classes must [ Start-End ] at the same time,
                    # One Time-List for each week (5 days) 
                    # and entries[entry].belongs_to!="PublicHoliday" # because it get '00:00:00' = NO Time
                    if entries[entry].belongs_to!="PublicHoliday" and \
                        classes_per_day_count > len(time_list): # because some days may have more classes
                            # Handle class time [Start - End]
                            start_time = entries[entry].start_time 
                            delta = timedelta(minutes=entries[entry].class_duration)
                            end_time = (datetime(1, 1, 1, start_time.hour, start_time.minute) + delta).strftime('%H:%M')
                            start_time = start_time.isoformat(timespec='minutes') # convert to "%H:%M" format
                            time_list.append(f"{start_time}-{end_time}")
                            
                            # Handle break time [Start - End]
                            break_start = entries[entry].break_time
                            delta = timedelta(minutes=entries[entry].break_duration) 
                            break_end = (datetime(1, 1, 1, break_start.hour, break_start.minute) + delta).strftime("%H:%M")
                            break_start = break_start.isoformat(timespec='minutes') # convert to "%H:%M" format 
                    report[group][date_key].append(entries[entry])
            
                entry += 1 
            
            if entry < len(entries) and entries[entry].course_group != group:
                # New Group 
                # break to change key 
                break 

    if report: 
        report[group] = fill_date_gap(report[group])
        report[group] = { "Time": time_list, **report[group] }
        time_list = []
        report[group]["break_time"] = [f"{break_start}-{break_end}"]

    return report 


def get_user_selection_page(request):
    user_sources = Source.objects.all()
    return render(request, 'courses/reports/user_selection.html', {
        'user_sources': user_sources,
        'users': []
    })

def get_users_for_source(request, source):
    try:
        return JsonResponse({
            'status_code': 200,
            'data': {
                'users': list([user.id, user.name] for user in User.objects.filter(source=source))
            }
        })
    except:
        return JsonResponse({
            "status_code": 404,"message": "Something Went Wrong!"        
        })

def get_user_profile(request):
    user_id = request.GET.get('user', None)
    users = User.objects.filter(id=user_id)
    user = users.first()
    return render(request, 'courses/reports/user_profile.html', {
        'user': user,
        'experiences':  user.experience_set.all(),
        'sci_degrees':  user.scientificdegree_set.all(),
        'certificates':  user.certificate_set.all(),
        'training_courses':  user.trainingcourse_set.all(),
    })


def get_users_month_selection_page(request):
    user_sources = Source.objects.all()
    return render(request, 'courses/reports/users_month_selection.html', {
        'user_sources': user_sources
    })

def get_user_worksheet(request):
    u_source = request.GET.get('u-source', None)
    date_input = request.GET.get('date-input', None)

    selected_source = Source.objects.get(pk=u_source)

    year, month = map(int, date_input.split('-'))
    users = User.objects.filter(source=selected_source)
    entries = ClassEntry.objects.filter(entry_date__year=year, entry_date__month=month)
    
    from django.db.models import Count
    commitments = Commitment.objects.filter(user_id__in=users, class_entry_id__in=entries).values(
        "user", "user__name"
        ).annotate(classes_count=Count("id"))
    # SQL-Like:
    # SELECT user_id, COUNT(comm.id) AS classes_count
    # FROM commitments AS comm GROUP BY user_id;
            
    # User.objects.first().commitment_set.first().class_entry.entry_date # The time of first class given by specific user
    
    import calendar
    return render(request, 'courses/reports/user_worksheet.html', {
        'u_source': selected_source.name,
        'year_month': f'{calendar.month_name[month]}, {year}',
        'commitments': commitments
    })
