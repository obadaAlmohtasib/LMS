from django.db import connection
from courses.models import Topic 

class GeneralReportView:

    def __init__(self, institution, course_name, course_group, no_of_weeks, week_number, 
                  entry_id, start_date, name, belongs_to, place, names_in_charge, start_time, class_duration, break_time, break_duration):
        # The order is matter
        self.institution = institution
        self.course_name = course_name
        self.course_group = course_group
        self.no_of_weeks = no_of_weeks 
        self.week_number = week_number 
        self.entry_id = entry_id 
        self.entry_date = start_date
        self.name = name # Name of Topic/Event 
        self.belongs_to = belongs_to
        self.place = place
        self.names_in_charge = names_in_charge
        self.start_time = start_time
        self.class_duration = class_duration
        self.break_time = break_time
        self.break_duration = break_duration

    def __str__(self):
        # if self.belongs_to == "PublicHoliday": # Then, skip the time 
        # return f"{self.start_time.isoformat(timespec='minutes')}\nV#2 Topic: {self.name}\n{self.names_in_charge}\n{self.place}"
        # return f"\nV#2 Topic: {self.name}\n{self.names_in_charge}\n{self.place}"
        return f"\n{self.name}\n{self.names_in_charge}\n{self.place}"


    @property
    def priority(self):
        return 1 if self.belongs_to == Topic.Type.ACADEMIC else 0



DAYS_COUNT_LIMIT = 4 # From start_date=Sunday To start_date+4=Thursday

def general_report_view(inst_id, start_date):
    cursor = connection.cursor()

    gen_series = f""" 
        SELECT 
            inst.name AS institution, crs.name AS course_name, cg.name AS course_group, null AS no_of_weeks, null AS week_number, 
            tabl.id AS entry_id, dates.dates AS entry_date, event_name, 'PublicHoliday' AS "Type", ' ' AS place, ' ' AS names, 
            null AS start_time, null AS class_duration, null AS break_time, null AS break_duration
        FROM (SELECT id, course_id, event_name, start_date, end_date
            FROM public_holidays  
            WHERE course_id IN (SELECT crs.id FROM courses AS crs WHERE institution_id = {inst_id})) AS tabl
        INNER JOIN courses AS crs 
        ON (tabl.course_id=crs.id)
        INNER JOIN institutions AS inst 
        ON (inst.id=crs.institution_id) 
        INNER JOIN c_groups AS cg 
        ON (cg.course_id=crs.id)
        INNER JOIN (SELECT dates::DATE 
                    FROM generate_series (DATE '{start_date}', DATE '{start_date}' + {DAYS_COUNT_LIMIT}, '1 Day') AS dates) AS dates
        ON (dates.dates BETWEEN tabl.start_date AND tabl.end_date)        
    """

    union = f"""        
        {join_tables(inst_id, start_date)}
        UNION
        {gen_series}
        ORDER BY course_name, course_group, entry_date, start_time;
    """

    cursor.execute(union) 
    res = [GeneralReportView(*entity) for entity in cursor.fetchall()]
    return res


def join_tables(inst_id, start_date):
    return f"""
        SELECT * 	 
        FROM (SELECT 
                    inst.name AS institution, crs.name AS course_name, cg.name AS course_group, 
                    CEIL(crs.no_of_classes::DECIMAL / crs.no_daily_classes / 5) AS no_of_weeks, -- Friday & Saturday are free
                    CEIL(DENSE_RANK() OVER (PARTITION BY cg.id ORDER BY E.entry_date) / 5.0) AS "week_number",
                    E.id AS entry_id, E.entry_date, T.name AS topic_title, T.t_type AS "Type", place, 
                    STRING_AGG(u.name, E'\n' ORDER BY cmit.id ASC) AS names,
                    skd.start_time, skd.class_duration, TM.break_time, TM.break_duration
                FROM institutions AS inst 
                INNER JOIN courses AS crs 
                ON (inst.id=crs.institution_id) 
                INNER JOIN class_entries E
                ON (crs.id=E.course_id) 
                INNER JOIN c_groups AS cg 
                ON (E.course_group_id=cg.id)
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
                WHERE inst.id = {inst_id} AND E.is_deleted=False
                GROUP BY inst.name, crs.id, E.id, cg.id, t.name, T.t_type, TM.id, skd.id
            )AS t
        WHERE t.entry_date::DATE BETWEEN '{start_date}' AND DATE'{start_date}' + {DAYS_COUNT_LIMIT}
    """