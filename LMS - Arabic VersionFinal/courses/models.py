from typing import Any
from django.db import models, IntegrityError 
from datetime import date
from datetime import timedelta


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False) 

class ClassEntryDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_deleted=False, 
            course__institution__is_deleted=False, 
            course__is_deleted=False, 
            course_group__is_deleted=False, 
            topic__is_deleted=False, 
            timing__is_deleted=False, 
            class_schedule__is_deleted=False
            )

class Source(models.Model):
    class Meta: 
        db_table = 'user_sources'
    
    name = models.CharField(max_length=128)
    can_oversee_multiple_classes = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self):
        # return f'Source: {self.name}'
        return f'{self.name}'


class User(models.Model):
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_users_is_deleted')
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name"], 
                condition=models.Q(is_deleted=False), 
                name='users_name_key'
                )
            ]
    
    # class Source(models.TextChoices):
    #     # (REAL_STORED_VALU, HUMAN_READABLE)
    #     INTERNAL_1 = 'INTERNAL-1', 'منسوب مدرسة سلاح الإشارة'
    #     INTERNAL_2 = 'INTERNAL-2', 'منسوب وزارة الحرس الوطني'
    #     CONTRACTED_1 = 'CONTRACTED-1', 'مقاول - شركات'
    #     CONTRACTED_2 = 'CONTRACTED-2', 'مقاول - أفراد'
    #     EXTERNAL = 'EXTERNAL', 'مقاول - حر'
    #     COMMITTEE = 'COMMITTEE', 'منسوب مدرسة سلاح الإشارة - لِجان'

    name = models.CharField(max_length=128)
    identification = models.CharField(max_length=10, null=True, blank=True) 
    call = models.CharField(max_length=15, null=True, blank=True) 
    email = models.CharField(max_length=220, null=True, blank=True) 
    birth_date = models.DateField(null = True, blank=True) # not required
    address = models.CharField(max_length=220, null=True, blank=True) # not required 
    nationality = models.CharField(max_length=128, null=True, blank=True) # not required
    is_deleted = models.BooleanField(default=False) 
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=False, null=True)

    objects = DeletedManager()

    def __str__(self):
        # return f'User: {self.name}'
        return f'{self.name}'


class Experience(models.Model):
    class Meta:
        db_table = "experiences"
        
    
    company_name = models.CharField(max_length=128)
    role = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField() 
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        # return f'Experience: {self.role}'
        return f'{self.role}'
    

class ScientificDegree(models.Model):
    class Meta:
        db_table = "scientific_degrees"

    class Degree(models.TextChoices):
        # (REAL_STORED_VALU, HUMAN_READABLE)
        HIGH_SCHOOL = 'HIGH_SCHOOL', 'الدراسة الثانوية'
        DIPLOMA = 'DIPLOMA', 'دبلوم'
        BACHELOR = 'BACHELOR', 'بكالوريوس'
        MASTER = 'MASTER', 'الماجستير' 
        DOCTORAL = 'DOCTORAL', 'دكتوراه' 


    sci_degree = models.CharField(max_length=128, choices=Degree.choices)
    educational_institution = models.CharField(max_length=128) # generalize university, college, and school in one name
    major = models.CharField(max_length=128)
    year_obtained = models.IntegerField()
    grade = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        # return f'Sci_ Degree: {self.sci_degree}'
        return f'{self.sci_degree}'
    

class Certificate(models.Model):
    class Meta:
        db_table = "certificates"
    
    class Validity(models.IntegerChoices):
        FOR_EVER = -1, 'مدى الحياة'
        ONE_YEAR = 1, 'سنة واحدة'
        FIVE_YEARS = 5, 'خمس سنوات'

    certificate = models.CharField(max_length=128)   
    certif_provider = models.CharField(max_length=128) # "certification providers" or "accreditation bodies."
    year_obtained = models.IntegerField()
    validity = models.SmallIntegerField(choices=Validity.choices) 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        # return f'Certificate: {self.certificate}'
        return f'{self.certificate}'
    

class TrainingCourse(models.Model):
    class Meta:
        db_table = "training_courses"
    
    name = models.CharField(max_length=128)
    party = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField() 
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        # return f'Training Course: {self.name}'
        return f'{self.name}'


class Institution(models.Model):
    class Meta:
        db_table = "institutions" 
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_institutions_is_deleted')
        ]

    name = models.CharField(max_length=128)   
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self):
        # return f'Institution: {self.name}'
        return f'{self.name}'
   

class Course(models.Model):
    class Meta:
        db_table = "courses" 
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_courses_is_deleted')
        ]

    class Status(models.TextChoices):
        # (REAL_STORED_VALU, HUMAN_READABLE)
        RUNNING = 'RUNNING', 'RUNNING'
        SUSPENDED = 'SUSPENDED', 'SUSPENDED' 

    name = models.CharField(max_length=128)
    no_of_classes = models.IntegerField()
    no_daily_classes = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()   
    status = models.CharField(choices=Status.choices, default=Status.RUNNING) # [ "Running"  || "Suspended" ]

    """ You may override the all() method and calculate the column or using/calling stored procedures """
    # status = models.Case(
    #     models.When(start_date__lt=date.today()-timedelta(days=1), then='START SOON'),
    #     models.When(end_date__lt=date.today()-timedelta(days=1), then='END'),
    #     default=models.Value("UNDERWAY") # جاري | قيد التنفيذ
    # )

    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=False, null=True)
    is_deleted = models.BooleanField(default=False) 
    
    objects = DeletedManager()

    def __str__(self):
        # return f'Course: {self.name}'
        return f'{self.name}'
    


class CourseGroup(models.Model):
    class Meta:
        db_table = "c_groups"
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_c_groups_is_deleted')
        ]

    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=False, null=True)
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self):
        # return f"Group: {self.name}"
        return f"{self.name}"


class SuspensionTime(models.Model):
    class Meta:
        db_table = "suspension_time"
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_suspension_time_is_deleted')
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["course"], 
                condition=models.Q(is_deleted=False), 
                name='course_suspend_key'
                )        
        ]

    suspended_since = models.DateField()
    resume_date = models.DateField(null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self) -> str:
        # return f"suspended_since: {self.suspended_since}"
        return f"{self.suspended_since}"


class Timing(models.Model):
    class Meta:
        db_table = 'timings'
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_timings_is_deleted')
        ]

    timing = models.CharField(max_length=128) 
    start_date = models.DateField()
    end_date = models.DateField()    
    break_time = models.TimeField()
    break_duration = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self) -> str:
        # return f"Timing: {self.timing}"
        return f"{self.timing}"
    

class ClassSchedule(models.Model):
    class Meta:
        db_table = "class_schedule"
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_class_schedule_is_deleted')
        ]

    class_num = models.SmallIntegerField()
    start_time = models.TimeField() 
    class_duration = models.IntegerField() 
    timing = models.ForeignKey(Timing, on_delete=models.SET_NULL, null=True) 
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self) -> str:
        return f"Class #{self.class_num}: at {self.start_time.isoformat(timespec='minutes')}"  



class PublicHolidays(models.Model):
    class Meta:
        db_table = "public_holidays"
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_public_holidays_is_deleted')
        ]

    start_date = models.DateField()
    end_date = models.DateField()
    event_name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=False, null=True)
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self):
        # return f'Event: {self.event_name}'
        return f'{self.event_name}'


class Topic(models.Model):
    class Meta:
        db_table = "topics" 
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_topics_is_deleted')
        ]

    class Type(models.TextChoices):
        # (REAL_STORED_VALU, HUMAN_READABLE)
        ACADEMIC = 'ACADEMIC', 'أكاديمي'
        NON_ACADEMIC = 'NON-ACADEMIC', 'غير أكاديمي' 
        EXAM = 'EXAM', 'إمتحان'
        TIME_GAP = 'TIME_GAP', 'فاصل زمني'
        INITIAL = 'INITIAL', 'حصص إبتدائية' 

    name = models.TextField()
    no_of_classes = models.IntegerField()
    t_type = models.CharField(max_length=128, choices=Type.choices, db_column='t_type') 
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=False, null=True)
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self):
        # return f'Topic: {self.name}'
        return f'{self.name}'


class ClassEntry(models.Model):
    class Meta:
        db_table = "class_entries" 
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_class_entries_is_deleted')
        ]
        # unique_together = ('course_group', 'entry_date', 'class_schedule')
        constraints = [
            models.UniqueConstraint(
                fields=['course_group', 'entry_date', 'class_schedule'], 
                condition=models.Q(is_deleted=False), 
                name='entries_sched_time'
                )
            ]

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    course_group = models.ForeignKey(CourseGroup, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    entry_date = models.DateField()
    place = models.CharField(max_length=128)    
    users = models.ManyToManyField(User, through="Commitment") 
    timing = models.ForeignKey(Timing, on_delete=models.SET_NULL, null=True)
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.SET_NULL, null=True) 
    is_deleted = models.BooleanField(default=False) 

    objects = ClassEntryDeletedManager()

    def save(self, *args, **kwargs):
        try:            
            super(ClassEntry, self).save(*args, **kwargs)
        except IntegrityError:
            #Override uniqueness error 
            skd = self.class_schedule
            raise Exception(f"There is already a class at the given inputs, Class number: {skd.class_num} at {skd.start_time}")

    def __str__(self):
        # return f'Class: {self.topic.name}'
        return f'{self.topic}'
    


class Commitment(models.Model): # |  Involvement  |  Participation
    class Meta:
        db_table = "commitments" 
        indexes = [
            models.Index(fields=['is_deleted'], name='ix_commitments_is_deleted')
        ]

    class Role(models.TextChoices):
        # (REAL_STORED_VALU, HUMAN_READABLE)
        PRIMARY = 'PRIMARY', 'PRIMARY'
        ASSISTANT = 'ASSISTANT', 'ASSISTANT' 
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True) 
    class_entry = models.ForeignKey(ClassEntry, on_delete=models.SET_NULL, blank=False, null=True) 
    role = models.CharField(max_length=128, choices=Role.choices) # أساسي | ثانوي-أول | ثانوي-ثاني
    is_deleted = models.BooleanField(default=False) 

    objects = DeletedManager()

    def __str__(self) -> str:
        # return f"Commitment: {self.role}" 
        return f"{self.role}" 
    