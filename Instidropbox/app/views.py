"""
Definition of views.
"""
from django.shortcuts import render,redirect,render_to_response
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm
from django.contrib.auth.models import User
from app.models import Faculty,Students,Profile,Faculty_subjects,ReqDetails
from app.forms import RequestDetailsForm
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            flag=False
            uname=form.cleaned_data.get('username')
            fcount=Faculty.objects.filter(Faculty_Id=uname).count()
            scount=Students.objects.filter(Student_Id=uname).count()
            if fcount==1 or scount==1:
                user = form.save() 
                user.refresh_from_db()  # load the profile instance created by the signal
                if fcount==1:
                    user.profile.is_faculty=True
                elif scount==1:
                    user.profile.is_student=True           
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('home')
            flag=True
            return render(request, 'sign_up.html', {'form': form,"notfound":flag,'year':datetime.now().year})
 
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form,'year':datetime.now().year})

def mydashboard(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated():
        usr=User.objects.all().filter(username=request.user)[0]
        if usr.profile.is_student:
            std=Students.objects.all().filter(Student_Id=request.user)[0]
            if request.method=="POST":
                std.Student_Name=request.POST.get("s_fname")
                std.Contact=request.POST.get("s_contact")
                std.Semester=request.POST.get("s_sem")
                std.Email=request.POST.get("s_email")
                std.save() 
            return render(
              request,
             'app/studentpanel.html',
             {
            'std':std,
            'title':'Student_Dashboard',
            'message':'Student Updated ',
            'heading':'My Profile',
            'year':datetime.now().year,
             }
           )                           
        elif usr.profile.is_faculty:
            staff=Faculty.objects.all().filter(Faculty_Id=request.user)[0]
            if usr.profile.is_hod:                
                return render(
                request,
                 'app/facultypanel.html',
                 {
                   'staff':staff,
                   'title':'Faculty panel ',
                   'year':datetime.now().year,
                   }
                 )
            elif usr.profile.is_principal:
               return render(
                      request,
                    'app/facultypanel.html',
                     {
                       'staff':staff,
                      'title':'Principal  desk',
                      'year':datetime.now().year,
                     }
                     )
            else:
               return render(
           request,
           'app/facultypanel.html',
            {
            'staff':staff,
            'title':'Home Page',
            'year':datetime.now().year,
            })
        elif usr.profile.is_hod:
            staff=Faculty.objects.all().filter(Faculty_Id=request.user)[0]
            return render(
                request,
                 'app/facultypanel.html',
                 {
                   'staff':staff,
                   'title':'HOD panel ',
                   'year':datetime.now().year,
                   }
                 )
        elif usr.profile.is_principal:
            staff=Faculty.objects.all().filter(Faculty_Id=request.user)[0]
            return render(
                request,
                 'app/facultypanel.html',
                 {
                   'staff':staff,
                   'title':'Principal panel ',
                   'year':datetime.now().year,
                   }
                 )
        else:
             return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def studentgrievances(request):
    assert isinstance(request,HttpRequest)
    if request.user.is_authenticated():
        grews=ReqDetails.objects.all().filter(sender_id=request.user).order_by("-dateof_request")
        return render(request,'app/studentgrievances.html',{"grews":grews})

def sendgrievance(request):
    assert isinstance(request,HttpRequest)
    if request.user.is_authenticated():
        faculty=Faculty.objects.all().filter(Department='CSE')
        if request.method=="GET":
            form=RequestDetailsForm()            
            return render(request,'app/sendgrievance.html',{"form":form,"faculty":faculty})
        elif request.method=="POST":
            form=RequestDetailsForm(request.POST)
            if form.is_valid():
                reqs= form.save()
                reqs.refresh_from_db()
                reqs.save()                
        return render(request,'app/sendgrievance.html',{"form":form,"faculty":faculty,"message":"Request Sent successfully"})

def viewfaculty(request,id):
    assert isinstance(request,HttpRequest)
    if request.user.is_authenticated():
        faculty=Faculty.objects.get(pk=id)
        subjects=Faculty_subjects.objects.all().filter(Faculty_Id__id=id)
        return render_to_response("app/viewfaculty.html",{"faculty":faculty,"subjects":subjects})

def f_viewgrievances(request):
    assert isinstance(request,HttpRequest)
    if request.user.is_authenticated():
       grews=ReqDetails.objects.all().filter(receiver_id=request.user).order_by("-dateof_request")
       return render(request,'app/f_viewgrievances.html',{"grews":grews})

def deptgrievances(request):
    if request.user.is_authenticated():
        usr=User.objects.all().filter(username=request.user)[0]
        dept=Faculty.objects.values('Department').filter(Faculty_Id=request.user)[0]
        if usr.profile.is_hod :
            if 'CSE' in dept.values():
                grews=ReqDetails.objects.all().filter(receiver_id__contains='CS').order_by("-dateof_request")
            elif 'MECH' in dept.vlaues():
                grews=ReqDetails.objects.all().filter(receiver_id__contains='ME').order_by("-dateof_request")
            elif 'ENC' in dept.values():
                grews=ReqDetails.objects.all().filter(receiver_id__contains='EC').order_by("-dateof_request")
            elif 'Civil' in dept.values():
                grews=ReqDetails.objects.all().filter(receiver_id__contains='CV').order_by("-dateof_request")
            return render(request,'app/deptgrievances.html',{"grews":grews})            
        elif usr.profile.is_principal:
            grews=ReqDetails.objects.all().order_by("-dateof_request")
            return render(request,'app/deptgrievances.html',{"grews":grews})


def viewstudent(request,uid):
    if request.user.is_authenticated():
        student=Students.objects.get(Student_Id=uid)
        return render_to_response(request,"app/f_viewgrievances.html",{"student":student})

def editstudentreq(request,id):
    if request.user.is_authenticated():
        success=False
        faculty=Faculty.objects.all().filter(Department='CSE')
        if request.method=="GET":
            req=ReqDetails.objects.get(pk=id)
            return render(request,'app/editstudentreq.html',{"req":req,"faculty":faculty})
        elif request.method=="POST":
            req=ReqDetails.objects.get(pk=id)
            req.Req_Type=request.POST.get("req_type")
            req.Req_details=request.POST.get("req_details")
            req.receiver_id=request.POST.get("receiver_id")
            req.visibilty_sender_id=request.POST.get('visible_sender_id', '') == 'on'
            req.visible_to_Hod=request.POST.get('visible_to_Hod', '') == 'on'
            req.visible_to_Principal=request.POST.get('visible_to_Principal', '') == 'on'
            req.save()
            success=True
            return render(request,'app/editstudentreq.html',{"Success":success})

def destroy(request,id):
     if request.user.is_authenticated():
        req=ReqDetails.objects.get(pk=id)
        req.delete()
                                              #grews=ReqDetails.objects.all().filter(sender_id=request.user).order_by("-dateof_request")
        return redirect('/studentgrievances') #render(request,'app/studentgrievances.html',{"grews":grews})

        

def updatereq(request,id):
    if request.user.is_authenticated():
        success=False
        if request.method=="GET":
            req=ReqDetails.objects.get(pk=id)
            return render(request,'app/f_updatereq.html',{"req":req})
        elif request.method=="POST" and request.FILES['rep_doc']:
            req=ReqDetails.objects.get(pk=id)
            myfile = request.FILES['rep_doc']
            fs = FileSystemStorage(location='/media/documents')
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url=fs.url(filename)
           # filepath = settings.MEDIA_ROOT + 'documents/'
            #local_file_path=handle_uploaded_file(request.FILES['rep_doc'],str(request.FILES['rep_doc']))                         #os.path.join(filepath,filename)
            req.reply_details=request.POST.get("reply")
            req.document=uploaded_file_url
            req.Req_Status=request.POST.get("status")
            req.save()
            success=True
            return render(request,'app/f_updatereq.html',{"Success":success})
         


'''def handle_uploaded_file(file, filename):
    if not os.path.exists(settings.MEDIA_ROOT+'documents/'):
        os.mkdir(settings.MEDIA_ROOT+'documents/')

    with open(settings.MEDIA_ROOT+'documents/'+ filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return settings.MEDIA_ROOT+'documents/'+filename
'''




