from django.db import connection
from courses.models import Topic 


class CourseScheduleView_V2:
    def __init__(self, id, start_date, course_id, name, belongs_to, place, names_in_charge, week_number, start_time, class_duration, break_time, break_duration):
        # The order is matter
        self.id = id
        self.entry_date = start_date
        self.course_id = course_id
        self.name = name
        self.belongs_to = belongs_to
        self.place = place
        self.names_in_charge = names_in_charge
        self.week_number = week_number
        self.start_time = start_time
        self.class_duration = class_duration
        self.break_time = break_time
        self.break_duration = break_duration

    def __str__(self):
        # if self.belongs_to == "PublicHoliday": # Then, skip the time 
        # if self.belongs_to not in map(lambda x,y :x, Topic.Type.choices)

        # return f"{self.start_time.isoformat(timespec='minutes')}\nV#2 Topic: {self.name}\n{self.names_in_charge}\n{self.place}"
        # return f"\nV#2 Topic: {self.name}\n{self.names_in_charge}\n{self.place}"
        return f"\n{self.name}\n{self.names_in_charge}\n{self.place}"


    @property
    def priority(self):
        return 1 if self.belongs_to == Topic.Type.ACADEMIC else 0


def course_schedule_view_2(course_id, group_id):
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
        {join_tables(course_id, group_id)}
        UNION
        SELECT id, start_date, course_id, event_name, 'PublicHoliday' AS "Type", ' ' AS place, ' ' AS names, 
            null AS week_number, null AS start_time, null AS class_duration, null AS break_time, null AS break_duration
        FROM date_range_splitter
        ORDER BY entry_date, start_time;
    """
    query = cte + union
    cursor.execute(query)
    res = [CourseScheduleView_V2(*entity) for entity in cursor.fetchall()]
    return res



def join_tables(course_id, group_id):
    return f"""        
        SELECT 
            E.id, E.entry_date, E.course_id, T.name, T.t_type AS "Type", place, 
            STRING_AGG(u.name, E'\n' ORDER BY cmit.id ASC) AS names,
            CEIL(DENSE_RANK() OVER (ORDER BY E.entry_date) / 5.0) AS "week_number",
            skd.start_time, skd.class_duration, TM.break_time, TM.break_duration
        FROM class_entries E
        INNER JOIN topics T
        ON (E.topic_id = T.id)        
        LEFT JOIN commitments cmit
        ON (E.id = cmit.class_entry_id)
        LEFT JOIN users u
        ON (cmit.user_id = u.id)
        INNER JOIN timings AS TM
        ON (E.timing_id = TM.id)
        LEFT JOIN class_schedule AS skd 
        ON (E.class_schedule_id=skd.id)
        WHERE E.course_id={course_id} AND E.course_group_id={group_id} AND E.is_deleted=False 
        GROUP BY E.id, t.name, T.t_type, TM.id, skd.id
    """

