from django import template
from sys import maxsize
from datetime import datetime, timedelta
from courses.RawSQL.sql_queries_v2 import CourseScheduleView_V2
from courses.RawSQL.sql_general_report import GeneralReportView 
from courses.RawSQL.sql_queries import CourseScheduleView
from courses.models import Topic
from math import ceil
from ..models import User

register = template.Library()


@register.filter(name="get_keys")
def get_keys(_dict):
    return _dict.keys()


@register.filter(name="get_values")
def get_values(_dict):
    return _dict.values()


@register.filter(name="iter_greater_length")
# since each day may have different number of classes.
def iter_greater_length(_dict):    
    values = list(_dict.values())
    g_length = 0
    for i in values:
        if g_length < len(i):
            g_length = len(i)
    return range(g_length)



# Return 1D-list(or vector/row) of 2D-list
@register.filter(name="get_day")
def get_day(_dict, args):
    values = list(_dict.values())
    return [] if args >= len(values) else values[args]

# Return single value (or cell) in 1D-list
@register.filter(name="return_item")
def return_item(arr, args):
    return "No Data Available" if args >= len(arr) else arr[args]


@register.filter(name="join_items")
def join_items(arr):
    def get_name(obj):
        return obj.name if type(obj) is User else obj # get rid of "User: " prefix - console style

    return "\n".join(map(get_name, arr)) if len(arr)>0 else ""


@register.filter(name='get_break_time')
def get_break_time(_dict):
    break_time = _dict.get('break_time', None)
    return break_time[0] if break_time else ''


@register.filter(name='is_break_time')
def is_break_time(break_time, time):
    if break_time and time: # Both is not null or empty
        break_start_end = break_time.split('-')
        time_start_end = time.split('-')
        if len(break_start_end) == 2 and len(time_start_end) == 2:
            break_start, break_end = break_start_end
            time_start, time_end = time_start_end
            FMT = '%H:%M'
            _break = datetime.strptime(break_start, FMT)
            _time = datetime.strptime(time_start, FMT)
            tdelta = _time - _break
            hours = tdelta.seconds // 3600
            minutes = (tdelta.seconds // 60) % 60
            if tdelta.days >= 0:
                return True
 
    return False


@register.filter(name='format_and_remove_break_time')
def format_and_remove_break_time(break_time, _dict):
    _dict['break_time'] = None
    start, end = break_time.split('-')
    return {
        "start": start,
        "end": end, 
    }


@register.filter(name="build_formatted_time")
def build_formatted_time(arr, idx):
    if idx >= len(arr): 
        return "No Data Available"
    else:
        time_str = arr[idx]
        start_time, end_time = time_str.split("-")

    time_obj = {
        "class_num": idx+1,
        "start_time": start_time, 
        "end_time": end_time, 
    }
    return time_obj

# To highlight the row of initial class 
@register.filter(name="first_class_in_days")
def first_class_in_days(_dict, idx):
    if idx != 0:
        return 1  #Light 

    for k, v in _dict.items():
        if type(v) is list and len(v) > idx: 
            entry = v[idx] 
            if isinstance(entry, CourseScheduleView_V2) or isinstance(entry, GeneralReportView):
                if entry.belongs_to == Topic.Type.INITIAL: 
                    return 0 #Dark 

    # for val in values 
    return 1  #Light

# For general report [Single Object]
@register.filter(name="get_object")
def get_object(_dict):    
    if not _dict:
        return None
    
    ans = None 
    for key, value in _dict.items(): 
        if type(value) is list and len(value) > 0 and isinstance(value[0], GeneralReportView):
            #Already picked [NOT: public_holiday]
            if isinstance(ans, GeneralReportView) and ans.no_of_weeks is not None:
                return ans

            ans = value[0]

    return ans  

# For V2 report [Single Object]
@register.filter(name="get_object_v2")
def get_object_v2(_dict):
    if not _dict:
        return None
    
    ans = None 
    for key, value in _dict.items(): 
        if type(value) is list and len(value) > 0 and isinstance(value[0], CourseScheduleView_V2):
            #Already picked [NOT: public_holiday]
            if isinstance(ans, CourseScheduleView_V2) and ans.week_number is not None:
                return ans

            ans = value[0]

    return ans 

# For normal report [Single Object]
@register.filter(name="get_object_simple")
def get_object_simple(_dict):
    if not _dict:
        return None
    
    ans = None 
    for key, value in _dict.items(): 
        if type(value) is list and len(value) > 0 and isinstance(value[0], CourseScheduleView):
            #Already picked [NOT: public_holiday]
            if isinstance(ans, CourseScheduleView) and ans.week_number is not None:
                return ans

            ans = value[0]

    return ans  


@register.filter(name="divide")
def divide(dividend, divisor):
    try: 
        return ceil(dividend / divisor)
    except:
        return 0
