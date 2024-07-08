SELECT *
FROM public_holidays;

-- Q1: Splitting date range into separate (Per Day) records
WITH RECURSIVE date_range_splitter AS 
	(
		SELECT id, course_id, event_name, start_date, end_date 
		FROM public_holidays
		WHERE course_id_id=2
		UNION
		SELECT id, course_id, event_name, DATE(start_date, "+1 day"), end_date FROM date_range_splitter
		WHERE start_date < end_date
	)
SELECT * FROM date_range_splitter
-- ORDER BY start_date;
ORDER BY event_name;

