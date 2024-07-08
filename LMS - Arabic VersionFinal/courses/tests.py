from django.test import TestCase

# Create your tests here.


#1
# By default => the week number starts counting from Sunday 
def c_report_v2(course_entries):
    report = {}
    week = 1
    week_days = { "6":"San", "0":"Mon", "1":"Thu", "2":"Wed", "3":"Tue", "4":"Fri", "5":"Sat", }  
    entries = course_entries
    entry = 0
    # NOTE: The algorithm is O(n), since we are looping one time over the array.
    while entry < len(entries):
        report[week] = {} # Walk through data week by week
        week_of_year = entries[entry].entry_date.strftime("%U")
        while entry < len(entries):
            # Skipping Friday & Saturday in Public_Holidays_set
            if entries[entry].entry_date.weekday() in (4, 5): # not in ("Fri.", "Sat."):
                entry+=1
                continue

            # Let date as key
            date_key = entries[entry].entry_date.strftime("%b. %d, %Y")
            report[week][date_key] = []
            # i = entry
            for _ in range(entry, len(entries)):
                changed_key = entries[entry].entry_date.strftime("%b. %d, %Y") # date for the new entry
                if report[week].get(changed_key, -1) == -1:
                    # New date
                    break
                else:
                    # Same date - Defined key
                    report[week][date_key].append(entries[entry])
                
                entry += 1

            if entry < len(entries) and entries[entry].entry_date.strftime("%U") != week_of_year:
                # New week
                break
        week += 1
        
    return report


