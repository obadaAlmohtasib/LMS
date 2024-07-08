WITH RECURSIVE date_range_splitter AS 
	(
		SELECT id, course_id, event_name, start_date, end_date 
		FROM public_holidays
		WHERE course_id=2 
		UNION
		SELECT id, course_id_id, event_name, DATE(start_date, "+1 day"), end_date FROM date_range_splitter
		WHERE start_date < end_date
	)
SELECT E.id, E.entry_date, E.course_id, T.name, T.t_type AS "Type"
FROM class_entries E
INNER JOIN topics T
ON (E.topic_id = T.id)
WHERE E.course_id=2
UNION 
SELECT id, start_date, course_id, event_name, "PublicHoliday" AS "Type" FROM date_range_splitter
-- ORDER BY start_date;
-- ORDER BY event_name


