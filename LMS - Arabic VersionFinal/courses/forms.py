from collections.abc import Mapping
from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models import Q
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from datetime import datetime


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name', 'can_oversee_multiple_classes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "اسم جهة العمل"
        self.fields['can_oversee_multiple_classes'].label = "التداخل"

class EditSourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "اسم جهة العمل"


class UserForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['name', 'source', 'identification', 'call', 'email', 'birth_date', 'address', 'nationality'] 
        widgets = {
            'name': forms.TextInput(),
            'birth_date': forms.DateInput(attrs={"type":"date"}), # The default: type="text"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "الإسم"
        self.fields['source'].label = "جهة العمل"
        self.fields['identification'].label = "رقم الهوية / الإقامة"
        self.fields['call'].label = "رقم الهاتف"
        self.fields['email'].label = "الإيميل"
        self.fields['birth_date'].label = "تاريخ الميلاد"
        self.fields['address'].label = "العنوان"
        self.fields['nationality'].label = "الجنسية"

    # custom_names = {"name":"user_name"}
    # def add_prefix(self, field_name):
    #     field_name = self.custom_names.get(field_name, field_name)
    #     return super(UserForm, self).add_prefix(field_name)

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company_name', 'role', 'start_date', 'end_date', 'description', 'user']
        widgets = { 
            'start_date': forms.DateInput(attrs={"type":"date", "name": "course_start_date"}), # The default: type="text"
            'end_date': forms.DateInput(attrs={"type":"date", "name":"course_end_date"}), # The default: type="text"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].label = "اسم الشركة"
        self.fields['role'].label = "الوظيفة"
        self.fields['start_date'].label = "تاريخ البداية"
        self.fields['end_date'].label = "تاريخ النهاية"
        self.fields['description'].label = "الوصف"
        

class ScientificDegreeForm(forms.ModelForm):
    class Meta:
        model = ScientificDegree
        fields = ['sci_degree', 'educational_institution', 'major', 'year_obtained', 'grade', 'user']

    # sci_degree = forms.ChoiceField(
    #     widget=forms.RadioSelect, 
    #     choices=ScientificDegree.Degree.choices
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sci_degree'].label = "الدرجة العلمية"
        self.fields['educational_institution'].label = "الجهة التعليمية"
        self.fields['major'].label = "التخصص"
        self.fields['year_obtained'].label = "السنة المكتسبة"
        self.fields['grade'].label = "التقدير"


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate', 'certif_provider', 'year_obtained', 'validity', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['certificate'].label = "الشهادة"
        self.fields['certif_provider'].label = "الشركة المزوّدة"
        self.fields['year_obtained'].label = "السنة المكتسبة"
        self.fields['validity'].label = "الصلاحية"


class TrainingCourseForm(forms.ModelForm):
    class Meta:
        model = TrainingCourse
        fields = ['name', 'party', 'start_date', 'end_date', 'description', 'user']
        widgets = { 
            'start_date': forms.DateInput(attrs={"type":"date", "name": "course_start_date"}), # The default: type="text"
            'end_date': forms.DateInput(attrs={"type":"date", "name":"course_end_date"}), # The default: type="text"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "اسم الدورة"
        self.fields['party'].label = "الجهة"
        self.fields['start_date'].label = "تاريخ البداية"
        self.fields['end_date'].label = "تاريخ النهاية"
        self.fields['description'].label = "الوصف"
     

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name']
        widgets = { 
            'name': forms.TextInput(), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "القسم"


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'no_of_classes', 'no_daily_classes', 'start_date', 'end_date'] # 
        widgets = { 
            'start_date': forms.DateInput(attrs={"type":"date", "name": "course_start_date"}), # The default: type="text"
            'end_date': forms.DateInput(attrs={"type":"date", "name":"course_end_date"}), # The default: type="text"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "الدورة"
        self.fields['no_of_classes'].label = "عدد الحصص"
        self.fields['no_daily_classes'].label = "عدد الحصص اليومية"
        self.fields['start_date'].label = "تاريخ البداية"
        self.fields['end_date'].label = "تاريخ النهاية"

    custom_names = {"name":"course_name", "start_date": "course_start_date", "end_date":"course_end_date"}
    def add_prefix(self, field_name):
        field_name = self.custom_names.get(field_name, field_name)
        return super(CourseForm, self).add_prefix(field_name)


class TimingForm(forms.ModelForm):
    class Meta: 
        model = Timing

        fields = ['timing', 'start_date', 'end_date', 'break_time', 'break_duration']        
        widgets = { 
            'start_date': forms.DateInput(attrs={"type":"date",}), # The default: type="text"
            'end_date': forms.DateInput(attrs={"type":"date",}), 
            'break_time': forms.TimeInput(attrs={"type":"time", }), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['timing'].label = "التوقيت"
        self.fields['start_date'].label = "تاريخ البداية"
        self.fields['end_date'].label = "تاريخ النهاية"
        self.fields['break_time'].label = "وقت بدء الإستراحة"
        self.fields['break_duration'].label = "مدة الإستراحة"


class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule 
        fields = ['class_num', 'start_time', 'class_duration']
        widgets = {
            'class_num' : forms.NumberInput(attrs={"min":1}), 
            'start_time': forms.TimeInput(attrs={"type":"time", }), # The default: type="text" 
            'class_duration' : forms.NumberInput(attrs={"min":1}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_num'].label = "رقم الحصة"
        self.fields['start_time'].label = "وقت بدء الحصة"
        self.fields['class_duration'].label = "مدة الحصة"


class CourseGroupForm(forms.ModelForm):
    class Meta:
        model = CourseGroup
        fields = ['name']
        widgets = {
            "name": forms.TextInput(attrs={"autofocus":True}),
        }

    custom_names = {"name":"course_group_name"}
    def add_prefix(self, field_name):
        field_name = self.custom_names.get(field_name, field_name)
        return super(CourseGroupForm, self).add_prefix(field_name)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "اسم المجموعة"


class CommitmentForm(forms.ModelForm): # |  Involvement  |  Participation
    class Meta:
        model = Commitment
        fields = ['role'] #, 'user', 'course']
        widgets = { 
            # user = models.ForeignKey(User, on_delete=models.CASCADE)
            # course = models.ForeignKey(Course, on_delete=models.CASCADE)
        }
        role = forms.MultipleChoiceField(choices=Commitment.Role.choices)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].label = "الدور"


class PublicHolidaysForm(forms.ModelForm):
    class Meta:
        model = PublicHolidays
        fields = ['start_date', 'end_date', 'event_name'] # , 'course_id']
        widgets = { 
            'start_date': forms.DateInput(attrs={"type":"date"}),
            'end_date': forms.DateInput(attrs={"type":"date"}),
            'event_name': forms.TextInput(),
            # 'course_id': models.ForeignKey(Course, on_delete=models.CASCADE)
        }

    custom_names = {"start_date": "event_start_date", "end_date":"event_end_date"}
    def add_prefix(self, field_name):
        field_name = self.custom_names.get(field_name, field_name)
        return super(PublicHolidaysForm, self).add_prefix(field_name)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].label = "تاريخ البداية"
        self.fields['end_date'].label = "تاريخ النهاية"
        self.fields['event_name'].label = "اسم الحدث/الطارئ"


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'no_of_classes', 't_type'] # , 'course_id']
        widgets = {
            'name': forms.TextInput(),
            'no_of_classes': forms.NumberInput()
        }

        t_type = forms.MultipleChoiceField(choices=Topic.Type.choices)
        # 'course_id': models.ForeignKey(Course, on_delete=models.CASCADE),            

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "اسم الموضوع"
        self.fields['no_of_classes'].label = "عدد الحصص"
        self.fields['t_type'].label = "التصنيف"


class ClassEntryForm(forms.ModelForm):

    user_sources = forms.ModelChoiceField(queryset=Source.objects.all(), required=False)
    users_filtered = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = ClassEntry
        fields = [
            'course', 'course_group', 'topic', 
            'timing', 'entry_date', 'class_schedule', 
            'user_sources', 'users_filtered', 'users', 
            "place", 
            ]
        # users = forms.ModelMultipleChoiceField(queryset=ClassEntry.objects.all())
        users = forms.MultipleChoiceField()
        widgets = {
            'entry_date': forms.DateInput(attrs={"type":"date",}), # The default: type="text"
            # 'entry_date': forms.DateTimeInput(attrs={"type": "datetime-local", 
            #                         "value": datetime.now().strftime("%Y-%m-%d %H:%M"), # must match HTML datetime-local format
            #                         #"readonly": True,
            #                     }),
        }

    def __init__(self, *args, **kwargs):
        course_group_instance = kwargs.pop('course_group_instance', None)

        super().__init__(*args, **kwargs)

        self.fields['course'].label = "الدورة"
        self.fields['course_group'].label = "المجموعة"
        self.fields['topic'].label = "الموضوع"
        self.fields['timing'].label = "التوقيت"
        self.fields['entry_date'].label = "التاريخ"
        self.fields['class_schedule'].label = "الحصة"
        self.fields['user_sources'].label = "جهات العمل"
        self.fields['users_filtered'].label = "المدرّبين المُتاحين"
        self.fields['users'].label = "المدرّبين"
        self.fields['place'].label = "المكان"

        if course_group_instance is not None:
            # NOTE: fields attribute doesn't exist before calling super().__init__ 
            course = Course.objects.filter(pk=course_group_instance.course.id)
            self.fields['course'].queryset = course 
            course = course.first()
            self.fields['course_group'].queryset = CourseGroup.objects.filter(pk=course_group_instance.id) 
            self.fields['topic'].queryset = Topic.objects.filter(course_id=course.id) 
            timings = Timing.objects.filter(course_id=course.id)
            self.fields['timing'].queryset = timings
            self.fields['class_schedule'].queryset = ClassSchedule.objects.filter(timing_id__in=timings.values('id')) 



class ClassEntryEditForm(forms.ModelForm):

    user_sources = forms.ModelChoiceField(queryset=Source.objects.all(), required=False)
    users_filtered = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = ClassEntry
        
        fields = [
            'course_group', 'topic', 
            'timing', 'entry_date', 'class_schedule', 
            'user_sources', 'users_filtered', 'users', 
            "place", 
            ]

        widgets = {
            'entry_date': forms.DateInput(attrs={"type":"date",}), # The default: type="text"
        }

    def __init__(self, *args, **kwargs):
        # You have to remove all custom kwargs before calling super().__init__  
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        self.fields['course_group'].label = "المجموعة"
        self.fields['topic'].label = "الموضوع"
        self.fields['timing'].label = "التوقيت"
        self.fields['entry_date'].label = "التاريخ"
        self.fields['class_schedule'].label = "الحصة"
        self.fields['user_sources'].label = "جهات العمل"
        self.fields['users_filtered'].label = "المدرّبين المُتاحين"
        self.fields['users'].label = "المدرّبين"
        self.fields['place'].label = "المكان"

        # NOTE: fields attribute doesn't exist before calling super().__init__ 
        self.fields['course_group'].queryset = CourseGroup.objects.filter(course_id=instance.course_id) 
        self.fields['topic'].queryset = Topic.objects.filter(course_id=instance.course_id) 
        self.fields['timing'].queryset = Timing.objects.filter(course_id=instance.course_id) 
        # self.fields['course_group'].queryset = CourseGroup.objects.filter(course_id=instance.course_id) 
        self.fields['class_schedule'].queryset = ClassSchedule.objects.filter(timing_id=instance.timing_id) 


        # entries = ClassEntry.objects.filter(entry_date=instance.entry_date)
        # entries = entries.exclude(id=instance.id) # Exclude this [For the already selected users not disappear] 
        # print(instance.entry_date) 
        # class_schedule = ClassSchedule.objects.get(id=instance.class_schedule_id)
        # skd_start = class_schedule.start_time
        # delta = timedelta(minutes=class_schedule.class_duration)
        # skd_end = (datetime(1, 1, 1, skd_start.hour, skd_start.minute) + delta).time() 
        
        # # entries.exclude(class_schedule) # Exclude overlapped schedules 
        # excluded_entries = []
        # for cls in entries:
        #     if cls.class_schedule is None:
        #         continue

        #     cls_start = datetime(1, 1, 1, cls.class_schedule.start_time.hour, cls.class_schedule.start_time.minute)
        #     cls_end = (cls_start + timedelta(minutes=cls.class_schedule.class_duration)).time()
        #     cls_start = cls_start.time()
        #     if cls_start >= skd_start and cls_start < skd_end:
        #         #overlapped            
        #         excluded_entries.append(cls)
        #         continue
                    
        #     if skd_start >= cls_start and skd_start < cls_end: 
        #         #overlapped
        #         excluded_entries.append(cls) 
        #         continue

        # # List of active [FREE] users 
        # users = User.objects.exclude(
        #     ~Q(source=User.Source.COMMITTEE), # translated to AND 
        #     id__in=Commitment.objects.filter(class_entry__in=excluded_entries).values("user_id")
        # )
        # self.fields['users'].queryset = users 


# Create a custom formset and override __init__
class CustomBaseInlineFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomBaseInlineFormSet, self).__init__(*args, **kwargs)
        no_of_forms = len(self)
        # print("In the custom formset")
        for i in range(0, no_of_forms): # Loop over each individual form
            # print(self[i]) # form

            # Rename the default label of 'DELETE' BooleanField
            delete_field = self[i].fields['DELETE'] # Get specific field by field_name
            delete_field.label = 'حذف' # default is 'DELETE'
          