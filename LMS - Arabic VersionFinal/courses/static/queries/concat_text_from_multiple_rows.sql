-- Use group_concat function to concatenate text from multiple rows into a single text string 
--

SELECT E.id, E.entry_date, E.course_id, T.name, T.t_type AS "Type", group_concat(ES.name, "\n") AS names
FROM class_entries E
INNER JOIN topics T
ON (E.topic_id = T.id)
LEFT JOIN courses_classsupervisor CS
ON (E.id = CS.class_entry_id)
INNER JOIN courses_examsupervisor ES
ON (CS.supervisor_id = ES.id)
WHERE E.course_id={course_id} AND E.course_group_id={group_id}
GROUP BY E.id
UNION 
SELECT E.id, E.entry_date, E.course_id, T.name, T.t_type AS "Type", group_concat(U.name, "\n") AS names
FROM class_entries E
INNER JOIN topics T
ON (E.topic_id = T.id)
LEFT JOIN commitments cmit
ON (E.id = cmit.class_entry_id)
LEFT JOIN users U 
ON (cmit.user_id = U.id)
WHERE E.course_id={course_id} AND E.course_group_id={group_id}
GROUP BY E.id


