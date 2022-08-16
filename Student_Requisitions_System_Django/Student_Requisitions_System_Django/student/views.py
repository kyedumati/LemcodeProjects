from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from student.models import *
from django.contrib.auth.models import User
from django.views.generic import TemplateView
import datetime, random
# Create your views here.


def index_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        username=email
        password = request.POST.get('password')
        tab_selected = request.POST.get('tab_selected')
        print("username ", email, " password ",password)
        #username = User.objects.get(email=email).username
        #print('email ',username)
        user = authenticate(username=email, password=password)
        print("user",user)

        if user:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                request.session['email'] = email
                request.session['tab_selected'] = tab_selected
                print("inside success user ",tab_selected)
                if tab_selected == 'student_tab':
                    return HttpResponseRedirect(reverse('student:stud_home'))
                elif tab_selected == 'dept_tab':
                    if username[:3] == 'hod':
                        return HttpResponseRedirect(reverse('student:hod_home'))
                    else:
                        return HttpResponseRedirect(reverse('student:dep_home'))
                elif tab_selected == 'office_tab':
                    return HttpResponseRedirect(reverse('student:off_home'))
            else:
                user_login = 'inactive'
                return render(request, 'student/index.html', context={'login': user_login})
        else:
            user_login = 'invalid'
            return render(request, 'student/index.html', context={'login': user_login})
    else:
        return render(request, 'student/index.html', context={})


@login_required
def user_logout(request):
    logout(request)
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return HttpResponseRedirect(reverse('index'))


@login_required()
def home(request):
    tab_selected = request.session['tab_selected']
    username = request.session['username']
    if tab_selected == 'student_tab':
        return HttpResponseRedirect(reverse('student:stud_home'))
    elif tab_selected == 'dept_tab':
        if username[:3] == 'hod':
            return HttpResponseRedirect(reverse('student:hod_home'))
        else:
            return HttpResponseRedirect(reverse('student:dep_home'))
    elif tab_selected == 'office_tab':
        return HttpResponseRedirect(reverse('student:off_home'))


class AboutView(TemplateView):
    template_name = 'student/about.html'


class DeptsView(TemplateView):
    template_name = 'student/depts_navbar.html'


class ContactUsView(TemplateView):
    template_name = 'student/contact_us.html'


class StudentView(TemplateView):
    template_name = 'student/student_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = self.request.session['email']
        student = Student.objects.get(email=email)
        requisitions = Requisitions.objects.filter(usn=student.usn)
        context['student_data'] = student
        context['req_done'] = requisitions
        return context


@login_required()
def form_submit(request):
    email = request.session['email']
    student = Student.objects.get(email=email)
    if request.method == 'POST':

        dates = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        issu = request.POST.get('issue')
        issu = issu[:2]
        off_sec = request.POST.get('office_section')
        off_sec = off_sec[:2]
        num = random.randint(0, 100)
        reqid = issu + off_sec + str(num)
        try:
            db = Requisitions.objects.create(name=student.name,
                                             usn=student,
                                             facid=student.facid,
                                             reqid=reqid,
                                             phone=student.phone,
                                             email=student.email,
                                             date=dates,
                                             subject=request.POST.get('subject'),
                                             office_section=request.POST.get('office_section'),
                                             issue=request.POST.get('issue'),
                                             reason=request.POST.get('reason'),
                                            )
            db.save()
            db_save_status = True
        except:
            db_save_status = False
        return render(request, 'student/student_home.html', {'db_handle': db_save_status,
                                                             'student_data': student,
                                                             'req_done': Requisitions.objects.filter(usn=student.usn)})
    else:
        return render(request, 'student/student_home.html', {})


class DeptView(TemplateView):
    template_name = 'student/department_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.session['username']
        faculty = Faculty.objects.get(email=username)
        requisitions = Requisitions.objects.filter(facid=faculty.facid, proc_appr=0)
        requisitions_approved = Requisitions.objects.exclude(facid=faculty.facid, proc_appr=0)
        context['faculty_data'] = faculty
        context['req_data'] = requisitions
        context['req_done'] = requisitions_approved
        return context


class OfficeView(TemplateView):
    template_name = 'student/office_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.session['username']
        office = Office.objects.get(email=username)
        requisitions = Requisitions.objects.filter(proc_appr=1, hod_appr=1, office_appr=0)
        requisitions_approved = Requisitions.objects.filter(proc_appr=1, hod_appr=1).exclude(office_appr=0)
        context['office_data'] = office
        context['req_data'] = requisitions
        context['req_done'] = requisitions_approved
        return context


class HodView(TemplateView):
    template_name = 'student/hod_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.session['username']
        faculty = Faculty.objects.get(email=username)
        requisitions = Requisitions.objects.filter(proc_appr=1, hod_appr=0)
        requisitions_approved = Requisitions.objects.exclude(facid=faculty.facid, proc_appr=1, hod_appr=0)
        context['faculty_data'] = faculty
        context['req_data'] = requisitions
        context['req_done'] = requisitions_approved
        return context


@login_required()
def accept_reject(request):
    username = request.session['username']
    tab_selected = request.session['tab_selected']
    if tab_selected == 'office_tab':
        office = Office.objects.get(email=username)
    if tab_selected == 'dept_tab':
        faculty = Faculty.objects.get(email=username)
    req_id = request.POST.get('req_id')
    btn_appr = request.POST.get('appr_btn')
    rej_btn = request.POST.get('rej_btn')
    if btn_appr == '1' and tab_selected == 'dept_tab' and username[:3] != 'hod':
        reqsns_table = Requisitions.objects.get(reqid=req_id)
        reqsns_table.proc_appr = 1
        reqsns_table.save()
        return render(request, 'student/department_home.html', {'faculty_data': faculty,
                                                                'req_data': Requisitions.objects.filter(facid=faculty.facid, proc_appr=0),
                                                                'req_done': Requisitions.objects.exclude(facid=faculty.facid, proc_appr=0)})

    if btn_appr == '1' and tab_selected == 'dept_tab' and username[:3] == 'hod':
        reqsns_table = Requisitions.objects.get(reqid=req_id)
        reqsns_table.hod_appr = 1
        reqsns_table.save()
        return render(request, 'student/hod_home.html', {'faculty_data': faculty,
                                                         'req_data': Requisitions.objects.filter(proc_appr=1, hod_appr=0),
                                                         'req_done': Requisitions.objects.exclude(facid=faculty.facid, proc_appr=1, hod_appr=0)})

    if btn_appr == '1' and tab_selected == 'office_tab':
        reqsns_table = Requisitions.objects.get(reqid=req_id)
        reqsns_table.office_appr = 1
        reqsns_table.save()
        return render(request, 'student/office_home.html', {'office_data': office,
                                                            'req_data': Requisitions.objects.filter(proc_appr=1, hod_appr=1, office_appr=0),
                                                            'req_done': Requisitions.objects.filter(proc_appr=1, hod_appr=1).exclude(office_appr=0)})

    if rej_btn == '1' and tab_selected == 'dept_tab' and username[:3] != 'hod':
        reqsns_table = Requisitions.objects.get(reqid=req_id)
        reqsns_table.proc_appr = 2
        reqsns_table.save()
        return render(request, 'student/department_home.html', {'faculty_data': faculty,
                                                                'req_data': Requisitions.objects.filter(facid=faculty.facid, proc_appr=0),
                                                                'req_done': Requisitions.objects.exclude(facid=faculty.facid, proc_appr=0)})

    if rej_btn == '1' and tab_selected == 'dept_tab' and username[:3] == 'hod':
        reqsns_table = Requisitions.objects.get(reqid=req_id)
        reqsns_table.hod_appr = 2
        reqsns_table.save()
        return render(request, 'student/hod_home.html', {'faculty_data': faculty,
                                                         'req_data': Requisitions.objects.filter(proc_appr=1, hod_appr=0),
                                                         'req_done': Requisitions.objects.exclude(facid=faculty.facid, proc_appr=1, hod_appr=0)})

    if rej_btn == '1' and tab_selected == 'office_tab':
        print("hi")
        reqsns_table = Requisitions.objects.get(reqid=req_id)
        reqsns_table.office_appr = 2
        reqsns_table.save()
        return render(request, 'student/office_home.html', {'office_data': office,
                                                            'req_data': Requisitions.objects.filter(proc_appr=1, hod_appr=1, office_appr=0),
                                                            'req_done': Requisitions.objects.filter(proc_appr=1, hod_appr=1).exclude(office_appr=0)})












