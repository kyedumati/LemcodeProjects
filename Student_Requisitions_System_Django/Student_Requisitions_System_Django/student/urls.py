from django.conf.urls import url
from student import views

# App Name Tag
app_name = 'student'

urlpatterns = [
    url(r'^student_home/', views.StudentView.as_view(), name='stud_home'),
    url(r'^department_home/', views.DeptView.as_view(), name='dep_home'),
    url(r'^office_home/', views.OfficeView.as_view(), name='off_home'),
    url(r'^hod_home/', views.HodView.as_view(), name='hod_home'),
    url(r'^requisition_apply/', views.form_submit, name='form_submit'),
    url(r'^accept_reject/', views.accept_reject, name='accept_reject'),

]