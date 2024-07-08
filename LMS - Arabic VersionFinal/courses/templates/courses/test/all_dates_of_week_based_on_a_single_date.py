from datetime import datetime, timedelta


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



