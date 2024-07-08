from django.db import connection


class CourseScheduleView:
    def __init__(self, id, start_date, course_id, name, belongsTo, start_time, week_number):
        # The order is matter
        self.id = id
        self.entry_date = start_date
        self.course_id = course_id
        self.name = name
        self.belongsTo = belongsTo
        self.start_time = start_time
        self.week_number = week_number 

    def __str__(self):
        # return f"Topic: {self.name}"
        return f"{self.name}"



def course_schedule_view(course_id, group_id):
    cursor = connection.cursor()
    cte = f"""
        WITH RECURSIVE date_range_splitter AS
            (SELECT id, course_id, event_name, start_date, end_date
            FROM public_holidays WHERE course_id={course_id}
            UNION
            SELECT id, course_id, event_name, start_date + 1, end_date
            FROM date_range_splitter
            WHERE start_date < end_date)
    """
    union = f"""
        SELECT 
            E.id, E.entry_date, E.course_id, T.name, T.t_type AS "Type", skd.start_time as start_time,
            CEIL(DENSE_RANK() OVER (ORDER BY E.entry_date) / 5.0) AS "week_number" 
        FROM class_entries E
        INNER JOIN topics T
        ON (E.topic_id = T.id)
        INNER JOIN class_schedule skd
        ON (E.class_schedule_id=skd.id)
        WHERE E.course_id={course_id} AND E.course_group_id={group_id} AND E.is_deleted=False
        UNION
        SELECT id, start_date, course_id, event_name, 'PublicHoliday' AS "Type", null AS start_time, null AS "week_number"
        FROM date_range_splitter
        ORDER BY entry_date, start_time;
    """
    query = cte + union
    cursor.execute(query)
    res = [CourseScheduleView(*entity) for entity in cursor.fetchall()]
    return res



# Just for the intention of separating code
def splitting_date_range_query(course_id):
    return f"""
        WITH RECURSIVE date_range_splitter AS
            (SELECT id, course_id, event_name, start_date, end_date
            FROM public_holidays WHERE course_id={course_id}
            UNION
            SELECT id, course_id, event_name, start_date + 1, end_date
            FROM date_range_splitter
            WHERE start_date < end_date)
        SELECT id, start_date, course_id, event_name, 'PublicHoliday' AS "Type" 
        FROM date_range_splitter;
    """


