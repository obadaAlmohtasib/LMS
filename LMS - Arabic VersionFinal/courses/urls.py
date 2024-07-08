from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import users 
from .views import user_sources
from .views import institutions
from .views import courses
from .views import topics
from .views import daily_entries
from .views import reports

urlpatterns = [
    # path( URL_FORM_THAT_APPEARS_IN_BROWSER,  METHOD_NAME,  NAME_USED_BY_TEMPLATED_TO_REFER_TO_METHOD )
    # path('', institutions.index, name='index'),

    # CRUD opt for users 
    path('get_users', users.get_users, name='get_users'),
    path('create_user', users.create_user, name='create_user'),
    path("<int:id>/edit_user", users.edit_user, name="edit_user"),
    path("<int:id>/delete_user", users.delete_user, name="delete_user"),

    # CRUD opt for user sources 
    path('user-sources-list', user_sources.get_user_sources, name='user-sources-list'),
    path('user-sources', user_sources.create_user_source, name='user-sources'),
    path("<int:user_source_id>/edit-user-source", user_sources.edit_user_source, name="edit-user-source"),
    path("<int:user_source_id>/delete-user-source", user_sources.delete_user_source, name="delete-user-source"),

    # CRUD opt for institutions    
    path('', institutions.index, name='index'),
    path('get_institutions', institutions.get_institutions, name='get_institutions'),
    path('create_institution', institutions.create_institution, name='create_institution'),
    path("<int:id>/edit_institution", institutions.edit_institution, name="edit_institution"),
    path("<int:id>/delete_institution", institutions.delete_Institution, name="delete_institution"),

    # CRUD opt for courses
    path('courses-land-page', courses.get_land_page, name="courses-land-page"),        
    path('get_courses?institution_id=<int:id>&&institution_name=<str:name>', 
        courses.get_courses, name="get_courses?institution_id=&&institution_name="),

    path('<int:inst_id>/create_course', courses.create_course, name='create_course'),
    path("<int:crs_id>/edit_course", courses.edit_course, name="edit_course"),
    path("<int:crs_id>/delete_course", courses.delete_course, name="delete_course"),
    path("<int:course_id>/suspend_course", courses.suspend_course, name="suspend_course"),
    path("<int:course_id>/resume_course", courses.resume_course, name="resume_course"),
    path("copy-course-page", courses.copy_course_page, name="copy-course-page"),
    path("copy-course-data", courses.copy_course_data, name="copy-course-data"),


    # CRUD opt for course detail :: Topics, Public Holidays 
    # path('get_topics?course_id=<int:id>&&course_name=<str:name>', topics.get_topics, name='get_topics?course_id='),
    # Topics
    path('course-details-land-page', topics.view_course_details_land_page, name='course-details-land-page'),
    path('get_topics?course_id=<int:id>&&course_name=<str:name>', topics.get_topics, name='get_topics?course_id=&&course_name='),
    path('<int:id>/create_topic', topics.create_topic, name='create_topic'),
    path("<int:id>/edit_topic", topics.edit_topic, name="edit_topic"),
    path("<int:id>/delete_topic", topics.delete_topic, name="delete_topic"),
    # Timings 
    path("<int:crs_id>/add_timing", topics.add_timing, name="add_timing"),
    path("<int:timing_id>/edit_timing", topics.edit_timing, name="edit_timing"), 
    path("<int:timing_id>/delete_timing", topics.delete_timing, name="delete_timing"), 
    # Public Holidays
    path("<int:crs_id>/add_public_holiday", topics.add_public_holiday, name="add_public_holiday"),
    path("<int:id>/delete_public_holiday", topics.delete_public_holiday, name="delete_public_holiday"),
    # Course Groups
    path("<int:crs_id>/add_course_group", topics.add_course_group, name="add_course_group"),
    path("<int:id>/edit_course_group", topics.edit_course_group, name="edit_course_group"),
    path("<int:id>/delete_course_group", topics.delete_course_group, name="delete_course_group"),
    path("<int:id>/view_course_group", topics.view_course_group, name="view_course_group"),
    path("<int:course_group_id>/get_daily_entry_form", topics.get_daily_entry_form, name="get_daily_entry_form"),

    # Daily Entries opt
    path("get_daily_entries", daily_entries.get_daily_entries, name="get_daily_entries"),
    path("create_daily_entry", daily_entries.create_daily_entry, name="create_daily_entry"),
    path("<int:entry_id>/edit_daily_entry", daily_entries.edit_daily_entry, name="edit_daily_entry"),
    path("<int:id>/delete_daily_entry", daily_entries.delete_daily_entry, name="delete_daily_entry"),
    path("<int:crs_id>/get_related_models", daily_entries.get_related_models, name="get_related_models"),        
    path("<int:skd_id>/filter_active_users", daily_entries.filter_active_users, name="filter_active_users"), 
    
    path("<int:group_id>/<int:topic_id>/get_remaining_classes", 
         daily_entries.get_remaining_classes, name="get_remaining_classes"),

    path("<int:season_id>/get_schedules", daily_entries.get_schedules, name="get_schedules"),

    # Reports opt
    path("create_report", reports.create_report, name="create_report"),
    path("<int:id>/get_related_courses", reports.get_related_courses, name="get_related_courses"),
    path("<int:id>/get_related_groups", reports.get_related_groups, name="get_related_groups"),
    path("generate-summarized-report", reports.generate_summarized_report, name="generate-summarized-report"),
    path("generate-detailed-report", reports.generate_detailed_report, name="generate-detailed-report"),
    path("create_general_report", reports.create_general_report, name="create_general_report"),
    path("generate_general_report", reports.generate_general_report, name="generate_general_report"),

    path("user-selection-page", reports.get_user_selection_page, name="user-selection-page"),
    path("user-profile", reports.get_user_profile, name="user-profile"),
    path("<str:source>/users", reports.get_users_for_source, name="user-source-filter"),
    path("users-month-selection-page", reports.get_users_month_selection_page, name="users-month-selection-page"),
    path("user-worksheet", reports.get_user_worksheet, name="user-worksheet"),
]

urlpatterns += staticfiles_urlpatterns()
