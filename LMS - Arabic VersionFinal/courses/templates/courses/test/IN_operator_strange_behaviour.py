# 
# The IN operator result in a strange behaviour when using it with NULL values
# NOTE: if we're using the IN operator to check if some value are available in a subquery that contains null values, 
# therefore all values will checked to be available and evaluate to true unless we exclude null results

# SQL way
# EXAMPLE: SELECT 1 WHERE 1 NOT IN (2, 3); -- => Returns 1
# EXAMPLE: SELECT 1 WHERE 1 NOT IN (2, 3, null); -- => Returns nothing
# Use: SELECT id ... WHERE id NOT IN (2, 3) AND id is NOT NULL;

# Django way
# Before using the __in= check either: 
# 1: Use filter where ( columnName__isnull=False )
# 2: Use exclude where ( columnName=None )
# data = Lecturer.objects.filter(id__in=Commitment.objects.filter(course_id=topic.course_id).values("lecturer_id"))
# temp = ClassEntry.objects.filter(entry_date__range=(start_time, end_time), lecturers__isnull=False).values("lecturers")
# data = data.exclude(id__in=temp)
