from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import *
from django.http import JsonResponse,HttpResponse,FileResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.decorators.cache import cache_page
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.conf import settings
from django.db.models import Count,Sum
from django.db.models.functions import ExtractMonth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmpForm,ApprovalForm,LeaveForm,Employee,UserRegForm,filesForm,profileUpdateForm,UserUpdateForm,ChatForm,PostsForm,SettingsForm,CreateApprovalForm
from django.contrib.auth import update_session_auth_hash
from .models import *
from .temps import gen_temp,emp_attendance
from payroll.models import PayRoll
from datetime import datetime,date,timedelta
import string
import pandas
import geopy.distance
import numpy 
import math
import folium
import time
import json
import os
# Create your views here.
@login_required
def home(request):
    todos = []
    for todo in Applications.objects.all().order_by('pk'):
        if request.user.username == todo.approvers.split(',')[0]:
            apps = [
                 todo.pk,todo.approvers,todo.created_date,todo.details,todo.attachment.url,todo.type.name,f'{Employee.objects.filter(emp_id = todo.applicant.username)[0].first_name}' if len(Employee.objects.filter(emp_id = todo.applicant.username))>0 else f'{todo.applicant.username} name not found',
                 todo.created_time
    
            ]
            todos.append(apps)
    event = Events.objects.last()
    department = Department.objects.count()
    payrolls = PayRoll.objects.filter(employee_id = request.user.username,status="audited").order_by('-created_date')[:4]
    attendance = Attendance.objects.filter(employee__emp_id = request.user.username).order_by('-day')[:5]
    context = {"todos":todos,"employees":Employee.objects.count()-4,"event":event,"department":department,"payrolls":payrolls,"attendance":attendance,"nots":len(Notifications.objects.filter(recipient=request.user,seen=False))}
    return render(request,'management/index.html',context)


@login_required
def register(request):
    form=UserRegForm()
    if request.method=='POST':
        form=UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")


            employee = Employee(
                emp_id = form.cleaned_data.get("username"),
                status = 'incomplete'
            )
       
            send_mail(
                subject='Beezy new login details',
                message='username: '+str(form.cleaned_data.get("username"))+'\n'+ "password: "+str(form.cleaned_data.get("password1"))+'\n'+"if you didn't register kindly ignore",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data.get("email")])
            

            employee.save()

            new_profile = Profile(user=User.objects.get(username = username))
            new_profile.save()

            messages.success(request,f'{username} account created')
            
            return redirect('management-home')
    return render(request,'management/register.html',{'form':form})

@login_required
def view_notifications(request):

    context = {"notifications":Notifications.objects.filter(recipient = request.user).order_by('-pk')}

    return render(request,'management/notifications.html',context)

@login_required
def notifications_actions(request):
    if request.POST:

        pks = request.POST.get("pks").split(',')

        for pk in pks:

            notification = Notifications.objects.get(pk=int(pk))
            notification.seen = True
            notification.save()

        return JsonResponse("done",safe=False)
@csrf_exempt
@login_required
def notifications_details(request):

    if request.POST:

        pk = request.POST.get("pk")

        notification = Notifications.objects.filter(application=pk)[0]
        

        return JsonResponse(notification.details,safe=False)





    
def add_info(request):

    return render(request,'management/add_info.html')

'''
==========================================
render application  form
==========================================
'''
def approvals(request):
    context = {"appForm":ApprovalForm,'leave_form':LeaveForm(),"settings":AttSettings.objects.filter(employee_id=request.user.username)}
    return render(request,'management/approvals.html',context)

'''
==========================================
list of approvals initiated by current user
==========================================
'''
def view_approvals(request):

    context = {
        "applications":Applications.objects.filter(applicant=request.user).order_by('-pk'),
        "tracks":approvalTrack.objects.all(),
        
        
        }

    return render(request,'management/approval_list.html',context)
'''
==========================================
get the name of approver 
==========================================
'''
@csrf_exempt
def get_approvals_name(request):

    if request.POST:
        pk = request.POST.get("pk")
      
        apps = Applications.objects.get(pk=pk)
        
        names = []
        for id in Employee.objects.get(emp_id = apps.applicant.username).departments.approvers.split('\n'):
            
            
            if id in apps.approvers.split(','):
                
                
            
                try:
                    Employee.objects.get(emp_id = id)

                    names.append({"name":str(Employee.objects.get(emp_id = id).first_name)+" "+str(Employee.objects.get(emp_id = id).second_name),"status":"pending"})
                except:

                    names.append({"name":"couldn't find name for "+str(id),"status":"pending"})
            else:

                try:
                    print(id)
                    Employee.objects.get(emp_id = id)

                    names.append({"name":str(Employee.objects.get(emp_id = id).first_name)+" "+str(Employee.objects.get(emp_id = id).second_name),"status":"processed"})
                except:

                    names.append({"name":"couldn't find name for "+str(id),"status":"processed"})
           

        return JsonResponse(names,safe=False)


'''
==========================================
save leave approvals
==========================================
'''

@login_required
def leave(request):

  
    if request.POST:

        type_ = request.POST.get("type")
 
        category_ = request.POST.get("category")
        start = request.POST.get("start")
        end = request.POST.get("end")
        remarks = request.POST.get("remarks")

        new_leave =  Leave(
             applicant = request.user, Approvals_type = Approvals.objects.get(type=type_),
             category = category_, start=start,end=end,remarks=remarks
        )

        new_leave.save() 

        process = Process(

             applicant = request.user.username ,
             approvals = Approvals.objects.get(type=type_),
             details = str(type_)+"\n"+str(remarks),created = datetime.now(),
             status = "pending"
        )

        process.save()

        todo = Todo(

             recpient_id = Approvals.objects.get(type=type_).approvers.Employee_ids,
             details = str(type_)+": "+str(remarks),
             
        )
        todo.save()

        return JsonResponse("applied successfully",safe=False)
    
# create departments overview

def departments(request):

    departments = Department.objects.all()

    context =  {'departments':departments}

    return render(request,'management/departments.html',context)

def dep_details(request,name):

    details = Employee.objects.filter(departments=Department.objects.get(name=name))
    dep_attendance = Attendance.objects.filter(employee__departments = Department.objects.get(name=name))
    context = {"details":details,"attendances":dep_attendance}

    return render(request,'management/dep_details.html',context)


def add_department(request):

    pass

def add_roles(request):

    pass

def add_employee(request):

    context = {"emp_form":EmpForm()}

    return render(request,'management/add_employees.html',context)
@login_required
@csrf_exempt
def resign_employee(request):

    if request.POST:

        emp_id = request.POST.get("emp_id")
        remarks = request.POST.get("remarks")

        emp = Employee.objects.get(emp_id=emp_id)
        emp.status = "resigned"
        emp.remarks = remarks
        emp.dol = datetime.now()
        emp.save()

        user_del = User.objects.get(username = emp_id)
        user_del.delete()

        return JsonResponse("resignation successfully set",safe=False)


@login_required
def list_employee(request):
    
    dep_count =  Employee.objects.values('departments__name').annotate(all_deps = Count('departments__name'))

    turnovers = Employee.objects.values('status').annotate(all_status = Count('status'))

    joining_trends = Employee.objects.annotate(month=ExtractMonth('doj')).values('month').annotate(size=Count('month'))

    resign_trends = Employee.objects.annotate(month=ExtractMonth('dol')).values('month').annotate(size=Count('month'))

    try:

        rate = (len([turnover["status"] for turnover in turnovers if turnover["status"] == "resigned" ])/((len([turnover["status"] for turnover in turnovers if turnover["status"] == "resigned" ])+len([turnover["status"] for turnover in turnovers if turnover["status"] == "active" ]))/2))*100
    except:
        rate = 0;
    
    context = {
        
        "employee":Employee.objects.all(),

        "dep_names":[dep["departments__name"] for dep in dep_count],

        "dep_total":[dep["all_deps"] for dep in dep_count],

        "status": [turnover["status"] for turnover in turnovers],

        "total_status":[turnover["all_status"] for turnover in turnovers],

        "rate": rate,

        "month":[trend["month"] for trend in joining_trends],

        "size":[trend["size"] for trend in joining_trends],

        "r_month":[trend["month"] for trend in resign_trends],

        "r_size":[trend["size"] for trend in resign_trends]

        }
    
    return render(request,'management/list_employees.html',context)
@login_required
def get_employee(request):

    if request.POST:

        id = request.POST.get("id")

      

        employee = Employee.objects.get(emp_id = str(id))

        employee = serializers.serialize('json',[employee,])
        
        print(employee)
        return JsonResponse(employee, safe=False)
@login_required   
def employee_profile(request,id):

    employee = Employee.objects.get(emp_id = id)

    context = {"employee":employee}

    return render(request,'management/employee_profile.html',context)

@csrf_exempt   
def get_emp_other_details(request):

    if request.POST:

        emp_id = request.POST.get("id")

        other_fields = Employee.objects.get(emp_id = emp_id ).other_fields.split("\n")
        
        other_fields_all = []
        for other_field in other_fields:
            
            other_fields_all.append({"name":str(other_field.split(":")[0]),"value":str(other_field.split(":")[1])})
        
        return JsonResponse(other_fields_all,safe=False)
@login_required
def get_employee_template(request):

    filename = 'employee_template.xlsx'

    filepath =  os.path.join(settings.MEDIA_ROOT, 'emp_temp',filename)
    gen_temp(filepath)

    path = open(filepath,'rb')

    response = FileResponse(path,as_attachment=True)

    return response
@login_required
@csrf_exempt
def import_employee_data(request):

        try:
            file = request.FILES.get("file")
            emp_df = pandas.read_excel(file ,sheet_name='employee')
            settings_df = pandas.read_excel(file,sheet_name='attendance')
            settings_df[settings_df.select_dtypes(include=numpy.number).columns.tolist()] = settings_df[settings_df.select_dtypes(include=numpy.number).columns.tolist()].applymap(lambda x:math.trunc(x) if math.isnan(x)==False else 0)
            for items in emp_df.to_dict('records'):
                # create the user

                passwd = str(hash(date.today()))+str(items["emp_id"])
                # load employe data
                if Employee.objects.filter(emp_id=items["emp_id"]).exists() == False:
                    emp = Employee(
                        emp_id = items["emp_id"], first_name = items["first_name"],second_name = items["second_name"],national_no = items["national_no"],
                        kra_pin = items["kra_pin"],email = items["email"],dob=items["dob"],phone=items["phone"],next_kin_name = items["next_kin_name"],next_kin_id=items["next_kin_id"],
                        next_kin_phone = items["next_kin_phone"],address = items["address"],location = items["location"],station = Station.objects.filter(name = items["station_id"])[0],
                        role = Roles.objects.filter(name = items["role_id"])[0],departments = Department.objects.filter(name = items["departments_id"])[0], education_level = items["education_level"],doj=items["doj"],
                        dol = items["dol"],payroll_settings = PayRollSetting.objects.filter(category = items["payroll_settings_id"])[0],
                        account_no = items["account_no"], bank_name = items["bank_name"],salary = items["salary"],
                        allowance = items["allowance"], add_ons = items["add_ons"],status = "incomplete"

                    )
                    emp.save()
                else:

                    return JsonResponse(str(items["emp_id"])+" already exists",safe=False)
                # create user
                user = User(
                    username = math.trunc(items["emp_id"]),password=passwd,email = items["email"]
                )
                user.save()

                # create the profile
                profile = Profile(user=User.objects.get(username = items["emp_id"]))
                profile.save()

                

                send_mail(
                    subject='Beezy new login details',
                    message='username: '+str(items["emp_id"])+'\n'+ "password: "+str(passwd)+'\n'+"if you didn't register kindly ignore",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[items['email']])


            for items in settings_df.to_dict('records'):
                sett = AttSettings(
                    **items
                )
                sett.save()

            return JsonResponse("done",safe=False)
        
        except Exception as err:

            return JsonResponse(str(err),safe=False)

@login_required
@csrf_exempt
def import_att_settings(request):

    

        file = request.FILES.get("file")
        settings_df = pandas.read_excel(file,sheet_name='attendance')
        for items in settings_df.to_dict('records'):
            sett = AttSettings(
                    **items
                )
            sett.save()
        return JsonResponse("done",safe=False)
   


@login_required
@csrf_exempt
def lookup_employee(request):

    try:

        file = request.FILES.get("file")
        settings_df = pandas.read_excel(file,sheet_name='employee')
        settings_df[settings_df.select_dtypes(include=numpy.number).columns.tolist()] = settings_df[settings_df.select_dtypes(include=numpy.number).columns.tolist()].applymap(lambda x:math.trunc(x) if math.isnan(x)==False else 0)
        for items in settings_df.to_dict('records'):
            employee = Employee.objects.get(emp_id = items["emp_id"])
            print(employee)
            employee.update(**items)
            
        return JsonResponse("done",safe=False)
    except Exception as err:

        return JsonResponse(str(err),safe=False)




    


@login_required
def list_files(request):

    context ={"files":EmpFiles.objects.all(),"file_form":filesForm()}
    if request.POST:
        file_form = filesForm(request.POST,request.FILES)

        if file_form.is_valid():
            instance = file_form.save(commit = False)
            instance.properties = file_form.cleaned_data.get("document")
            instance.save()
            
            return JsonResponse("file uploaded successfully",safe=False)
    return render(request,'management/files.html',context)
@login_required
def get_emp_files(request):

    if request.POST:
        emp_id = request.POST.get("emp_id")
        emp_id = str(emp_id)
        my_files = EmpFiles.objects.filter(employee=Employee.objects.get(emp_id="001"))
        all_my_files = []
        for my_file in my_files:
            file_inst ={
                "category":my_file.category.category_name,
                "file_name":my_file.file_name,
                "document":my_file.document.url,
                "created":my_file.created 
            }
            all_my_files.append(file_inst)
        print(all_my_files)
        return JsonResponse(all_my_files,safe=False)
@login_required    
def files_details(request,id):

        emp_files = EmpFiles.objects.filter(employee=Employee.objects.get(emp_id=id))
        app_files = Applications.objects.filter(applicant = User.objects.get(username = id ))
        
        context = {
            "emp_files":emp_files,
            "app_files":app_files
        }

        return render(request,'management/files_details.html',context)
# delete all selected files
@login_required
@csrf_exempt
def files_del(request):

    if request.POST:

        pks = request.POST.get("pks")
        count = 0
        for pk in pks.split(","):
            # get file primary key and delete
            EmpFiles.objects.get(pk=pk).delete()
            count+=1
        
        return JsonResponse(str(count)+" file(s) deleted successfully",safe=False)
    
@login_required
def clock(request):

    context = {'leave_form':LeaveForm(),"approvals":Approvals.objects.all()}
   
    if request.POST:

        try:

            if len(AttSettings.objects.filter(employee_id = request.user.username))< 1:

                return JsonResponse("no settings found, contact admin",safe=False)

            att_settings =  AttSettings.objects.filter(employee_id = request.user.username)[0]
            lat = request.POST.get('latitude')
            long = request.POST.get('longitude')
            image_info = request.POST.get('image_str')
            #print(image_info)
            empty = ""
            att_filt = Attendance.objects.filter(day=date.today()).filter(employee = Employee.objects.get(emp_id=request.user.username))
            
            early_diff = ((datetime.strptime(datetime.now().strftime("%H:%M:%S"),'%H:%M:%S') -datetime.strptime(att_settings.end.strftime("%H:%M:%S"),"%H:%M:%S")).total_seconds())//60
            '''
                condition to determine if employee  left on time or early; early denoted by -ve
            '''
            if early_diff < 0:

                early_diff = early_diff*-1
            else:
                early_diff = 0
            
            late_diff = ((datetime.strptime(datetime.now().strftime("%H:%M:%S"),'%H:%M:%S') - datetime.strptime(att_settings.start.strftime("%H:%M:%S"),"%H:%M:%S")).total_seconds())//60
            
            if late_diff > 0:

                late_diff =  late_diff 

            else:

                late_diff = 0
            
            coords1 = (float(att_settings.clock_in_latitude),float(att_settings.clock_in_longitude))
            coords2 = (float(lat),float(long))

            distance_ = (geopy.distance.geodesic(coords1,coords2).km)*1000

            #print(distance_)

            #print(late_diff)
            
                           
            
            if len(att_filt) == 0 and (datetime.now().hour+3 > 0 and datetime.now().hour+3 <= 14): #record initial data
                attendance = Attendance(
                        employee =  Employee.objects.get(emp_id = request.user.username),
                        day = date.today(),
                        clock_in = datetime.now()+timedelta(hours=3),
                        clock_out = empty,
                        lat =lat ,long=long,image1=image_info,
                        lat1 = empty , long1 = empty, image2 = empty,remarks="clock in",
                        deductions  = 0,
                        days = 1,
                        clock_in_distance = str(distance_)

                        

                    )
                attendance.save()

                resp = f'''
                  clock in successful

                  {distance_} Metres registered from set zone.

                '''
                return JsonResponse(resp,safe=False)
            
            elif len(att_filt)>0 and att_filt[0].clock_out == '':
                
                att_filt[0].clock_out = datetime.now()+timedelta(hours=3)
                att_filt[0].lat1 = lat
                att_filt[0].long1 = long 
                att_filt[0].image2 = image_info
                att_filt[0].status = "present"
                att_filt[0].remarks = att_filt[0].remarks+" clock out"
                att_filt[0].deductions =  0
                att_filt[0].clock_out_distance = str(distance_)
                att_filt[0].save()

                resp = f'''
                  clock out successful

                  {distance_} Metres registered from set zone.

                '''

                return JsonResponse(resp,safe=False)
            
            elif len(att_filt)>0 and  (att_filt[0].clock_in != '' and att_filt[0].clock_out != ''):

                return JsonResponse("clock in and clockout already completed",safe=False)
            elif (datetime.now().hour+3 > 14 and datetime.now().hour+3 <= 24) and len(att_filt)==0:

                attendance = Attendance(
                        employee =  Employee.objects.get(emp_id = request.user.username),
                        day = date.today(),
                        clock_in = empty,
                        clock_out = datetime.now()+timedelta(hours=3),
                        lat = empty ,long=empty,image1=empty,
                        lat1 = lat, long1 = long, image2 = image_info,remarks="clock out",
                        deductions  = 0,
                        days = 1,
                        clock_out_distance = str(distance_)


                        

                    )
                attendance.save()

                resp = f'''
                  clock out successful

                  {distance_} Metres registered from set zone.

                '''
                return JsonResponse(resp,safe=False)
            
            elif (datetime.now().hour+3 > 14 and datetime.now().hour+3 <= 24) and (att_filt[0].clock_out != ''):
                return JsonResponse("clock out already completed",safe=False)

            else:

                return JsonResponse("out of scope",safe=False)




        except Exception as e:


            return JsonResponse(str(e),safe=False)


            



    return render(request,'management/clock.html',context)

'''
=========================================================================
    get today attendance and attendance settings for current user
    purpose compare with input details in clock in page
========================================================================
'''
@login_required
def get_attendance(request):

    today_att = Attendance.objects.filter(day=date.today()).filter(employee = Employee.objects.get(emp_id=request.user.username))
    att_settings = AttSettings.objects.filter(employee_id = request.user.username)

    if len(att_settings)>0:

        att_settings = att_settings[0]
       
        if len(today_att) > 0:

            details = {
                "clock_in":today_att[0].clock_in,
                "clock_out":today_att[0].clock_out,
                "h1":att_settings.start.hour,
                "m1":att_settings.start.minute,
                "h2":att_settings.end.hour,
                "m2":att_settings.end.minute,
                "lat1":att_settings.clock_in_latitude,
                "long1":att_settings.clock_in_longitude,
                "leave":att_settings.leave_days,
                "sick":att_settings.sick_leave_days,
                "comp":att_settings.compassionate_leave_days,
                "days":sum([att.days if att.day.month == datetime.now().month else 0 for att in Attendance.objects.filter(employee = Employee.objects.get(emp_id=request.user.username))])

                
            
            }

            return JsonResponse(details,safe=False)
        
        details = {"h1":att_settings.start.hour,
                "m1":att_settings.start.minute,
                "h2":att_settings.end.hour,
                "m2":att_settings.end.minute,
                "clock_in":"",
                "clock_out":"",
                "lat1":att_settings.clock_in_latitude,
                "long1":att_settings.clock_in_longitude,
                "leave":att_settings.leave_days,
                "sick":att_settings.sick_leave_days,
                "comp":att_settings.compassionate_leave_days,
                "days":sum([att.days if att.day.month == datetime.now().month else 0 for att in Attendance.objects.filter(employee=request.user.username)])
            }
        #print(details)
        return JsonResponse(details,safe=False)
    else:

        details = {
            "error":"no settings found"

            }
        
        return JsonResponse(details,safe=False)
    
'''
============================================================================================
        display recorded attendance details for employees
        divided into; overall details, late employee, employee on leave and absent details
============================================================================================

'''
def splitter(strng):
    if ' ' in strng:
        return strng.split(' ')[1]
    else:
        return ''
@csrf_exempt
@login_required
def view_attendance(request):

    deps = Department.objects.all()
    
    #print(attendances)
    
    if request.POST:

        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")
        dep = request.POST.get("dep")

        att_filt_by_date = Attendance.objects.filter(day__gte=date1,day__lte=date2,employee__departments__pk=int(dep))
        att_filt_by_date_list = []
        for attendance in att_filt_by_date:
            print(attendance)
            att_filt_by_date_list.append({
            
            "emp_id":attendance.employee.emp_id,"name":str(attendance.employee.first_name)+" "+str(attendance.employee.second_name),

            "department":attendance.employee.departments.name,
            
            "day":str(attendance.day),"clock_in":splitter(attendance.clock_in),"clock_out":splitter(attendance.clock_out),"lat":attendance.lat,

            "long":attendance.long,"lat1":attendance.lat1,"long1":attendance.long1,"image1":attendance.image1,"image2":attendance.image2,

            "distance1":str(attendance.clock_in_distance),

            "distance2":str(attendance.clock_out_distance),


            "status":attendance.status,"counts":attendance.days,"deductions":attendance.deductions,"leave":attendance.is_leave,

            "leave_days":attendance.leave_days,"remarks":attendance.remarks,
                                  
                                  
                                  
                                  })
            
        
        return JsonResponse(json.dumps(att_filt_by_date_list),safe=False)
                    


    context = {"deps":deps}

    return render(request,'management/list_attendance.html',context)

@csrf_exempt
@login_required 
def view_leave(request):

    if request.POST:

        start = request.POST.get("date1")
        end = request.POST.get("date2") 

        filt_leave = Applications.objects.filter(created_date__gte=start,created_date__lte=end,type__name__icontains = "leave")

        leaves = []

        for leave in filt_leave:

            leaves.append(

                {
                    "emp_id": leave.applicant.username,

                    "name": str(Employee.objects.get(emp_id=leave.applicant.username).first_name)+" "+str(Employee.objects.get(emp_id=leave.applicant.username).second_name),

                    "department": str(Employee.objects.get(emp_id=leave.applicant.username).departments.name),

                    "category": leave.category,

                    "status": leave.status,

                    "rate": leave.rate,

                    "start":str(leave.start),

                    "end": str(leave.end),

                    "days": leave.days





                }
            )
        
        
        return JsonResponse(json.dumps(leaves),safe=False)





@csrf_exempt
@login_required
def view_overall_attendance(request):
    
    if request.POST:

        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")

        overall_filt_by_date = Attendance.objects.filter(day__gte=date1,day__lte=date2)

        att_filt_by_date_list = []
        for attendance in overall_filt_by_date:


           
            att_filt_by_date_list.append({
            
            "emp_id":attendance.employee.emp_id,"name":str(attendance.employee.first_name)+" "+str(attendance.employee.second_name),

            "department":attendance.employee.departments.name,

            "email":attendance.employee.email,
            
            "day":str(attendance.day),"clock_in":splitter(attendance.clock_in),"clock_out":splitter(attendance.clock_out),

            "location1":attendance.lat+","+attendance.long,

            "location2":attendance.lat1+","+attendance.long1,

            "distance1":str(attendance.clock_in_distance),

            "distance2":str(attendance.clock_out_distance),

            "status":attendance.status,"counts":attendance.days,"deductions":attendance.deductions,"leave":attendance.is_leave,

            "leave_days":attendance.leave_days,"remarks":attendance.remarks,
                                  
                                  
                                  
                                  })
            
        
        return JsonResponse(json.dumps(att_filt_by_date_list),safe=False)



''' 
=========================================================
    return list of employees late on a given date
=========================================================
'''

@csrf_exempt
@login_required
def view_late_attendance(request):

    if request.POST:

        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")

        attendances = Attendance.objects.filter(day__gte=date1,day__lte=date2)

        late = []
        for attendance in attendances:
            if attendance.clock_in != '':
                try:
                    if datetime.strptime(attendance.clock_in, '%Y-%m-%d %H:%M:%S.%f').time() > AttSettings.objects.get(employee_id = attendance.employee.emp_id).start:
                
                        late_dict = {
                        "employee":attendance.employee.emp_id,
                        "employee_name":attendance.employee.first_name + " "+attendance.employee.second_name,
                        "department":attendance.employee.departments.name,
                        "day":str(attendance.day),
                        "clock_in":str(attendance.clock_in),
                        "clock_out":str(attendance.clock_out),
                        "clock_in_distance":str(attendance.clock_in_distance),
                        "clock_out_distance":str(attendance.clock_out_distance),
                        "set_clock_in":str(AttSettings.objects.get(employee_id = attendance.employee.emp_id).start),
                        "set_clock_out":str(AttSettings.objects.get(employee_id = attendance.employee.emp_id).end),
                        "count": attendance.days,
                        "status":attendance.status,
                        

                    }
                        late.append(late_dict)
                except:
                    late.append({})
        return JsonResponse(json.dumps(late),safe=False)    

'''
===============================================================
     return list of absent employees in a given range of date   
===============================================================
'''
@csrf_exempt
@login_required
def view_absent_attendance(request):

    if request.POST:

        date1 = request.POST.get("date1")
        date2 = request.POST.get("date2")

        absents = []

        for employee in Employee.objects.all():

            if employee.emp_id not in [att.employee.emp_id for att in Attendance.objects.filter(day__gte = date1,day__lte=date2)]:
                
                try:
                    absent_dict = {
                        "employee_id":employee.emp_id,
                        "name":employee.first_name +" "+employee.second_name ,
                        "email":employee.email ,
                        "department":employee.departments.name,
                        "phone":employee.phone ,
                        "next_of_kin":employee.next_kin_name,
                        "next_kin_phone":employee.next_kin_phone,
                        "address":employee.address + employee.location,
                        "set_clock_in":str(AttSettings.objects.get(employee_id = employee.emp_id).start),
                        "expected_days":AttSettings.objects.get(employee_id = employee.emp_id).expected_days
                    }
                except:
                    absent_dict = {
                        "employee_id":employee.emp_id,
                        "name":employee.first_name + " "+employee.second_name ,
                        "email":employee.email ,
                        "department":employee.departments.name,
                        "phone":employee.phone ,
                        "next_of_kin":employee.next_kin_name,
                        "next_kin_phone":employee.next_kin_phone,
                        "address":employee.address + employee.location,
                        "set_clock_in":"no settings",
                        "expected_days":"no settings"
                    }


                absents.append(absent_dict)
        

        return JsonResponse(json.dumps(absents),safe=False)

def download_attendance(request):

    filename = 'employee_attendance.xlsx'

    filepath =  os.path.join(settings.MEDIA_ROOT, 'emp_attendance',filename)
    emp_attendance(filepath)

    path = open(filepath,'rb')

    response = FileResponse(path,as_attachment=True)

    return response

@login_required
def edit_att_settings(request,emp_id):

    settings = AttSettings.objects.filter(employee_id = emp_id)[0]

    context = {"settings":settings,"form":SettingsForm()}

    if request.POST:
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request,'management/edit_attendance.html',context)

'''
==========================================
create approval process shortcut
==========================================
'''
@csrf_exempt
@login_required
def create_approval(request):
    
    if request.POST:

        department = request.POST.get("department")
        approvers = "\n".join(request.POST.get("approvers").split(','))
        notifiers = "\n".join(request.POST.get("notifiers").split(','))

        department_edit = Department.objects.get(pk=department)
        department_edit.approvers = approvers
        department_edit.notifiers = notifiers
        
        department_edit.save()

        

        return JsonResponse("created successfully",safe=False)


    context = {"employees":Employee.objects.all(),"deps":Department.objects.all()}
    return render(request,'management/create_approval.html',context)

'''
==========================================
get template for approval initiated
==========================================
'''
@csrf_exempt
def get_approval_temp(request):

    if request.POST:
        approval = request.POST.get("approval")
       
        try:

            data = Applications.objects.filter(type=Approvals.objects.get(pk=int(approval))).filter(applicant=request.user).filter(status="complete")[0].details
            
            return JsonResponse(data,safe=False)
        except:

            data = Approvals.objects.filter(pk=int(approval))[0].template
         
            return JsonResponse(data,safe=False)

        
'''
==========================================
upload leave details and pass as an application process
==========================================
'''
@login_required
def upload_leave(request):
    if request.POST:
       form = LeaveForm(request.POST)
       if form.is_valid():
            
            form.instance.applicant = request.user
            form.save()
            
            try:
                emp = Employee.objects.get(emp_id = request.user.username)
                
                approvers = emp.departments.approvers.split('\n')
                
                notifiers = emp.departments.notifiers.split('\n')
                
            except:
                return JsonResponse("employee details not added",safe=False)
            #approvers = Approvals.objects.get(name=form.cleaned_data.get("Approvals_type"))
            approvers = [app.rstrip() for app in approvers if app!=request.user.username]
            
            


            new_line = '\n'
            application = Applications(
                type = Approvals.objects.get(name=form.cleaned_data.get("Approvals_type")),
                applicant = request.user,
                
                        
                attachment = form.cleaned_data.get("attachments"),remarks = "",
                approvers = ",".join(approvers),expected = len(approvers),
                created_date = datetime.now(),created_time = datetime.now()+timedelta(hours=3),
                start = form.cleaned_data.get("start"), end = form.cleaned_data.get("end"),
                days = form.cleaned_data.get("days"),
                category = form.cleaned_data.get("category"),

                details = f'''
                <html>
               
                <h4>Work Assignment Details:</h4>
                <br>

                <p>{form.cleaned_data.get("work_assignment")}</p>
                <br>
                <br>

            

                <h4>Remaining Leave Days: <h4> <strong>{form.cleaned_data.get("remaining_leave_days")}</strong>
                <br>
                <br>
                
                <h4>Other Details:</h4>
                <br>
                <p>{form.cleaned_data.get("details")}{new_line}{new_line}</p>
                <br>
                <br>
                created: {datetime.now()}
               </html>

                '''

    
            )

            application.save()
           

            for approve in approvers+notifiers:
                # create notofication for the process
                if User.objects.filter(username=approve).exists():
                        notify = Notifications(
                        recipient = User.objects.get(username=approve),
                        info = str(request.user.username)+" "+str(form.cleaned_data.get("approvals"))+" new approval",
                        date = datetime.now(),
                        time = datetime.now()+timedelta(hours=3),
                        url = "{}",
                        application = application.pk,
                        details = f'''
                                    <html>
                                    <h4>Type:</h4>
                                    <br>
                                    Leave
                                    <br>
                                    <h4> Requested by: </h4>
                                        <br>
                                            <p>{emp.first_name} {emp.second_name}</p>
                                        <br>
                                        <h4>Work Assignment Details</h4>:
                                        <br>

                                        <p>{form.cleaned_data.get("work_assignment")}</p>
                                        <br>
                                        <br>

                                    

                                        <h4>Remaining Leave Days: <h4> <strong>{form.cleaned_data.get("remaining_leave_days")}</strong>
                                        <br>
                                        <br>
                                        <h4>Start:<h4>
                                        <p>{form.cleaned_data.get("start")}</p>
                                        <br>
                                        <h4>End:<h4>
                                        <p>{form.cleaned_data.get("end")}</p>
                                        <br>

                                        <h4> Days </h4>
                                        <br>
                                        {form.cleaned_data.get("days")}

                                        <h4>Other Details:</h4>
                                        <br>
                                        <p>{form.cleaned_data.get("details")}{new_line}{new_line}</p>
                                        <br>
                                        <br>
                                        created: {datetime.now()}
                                    </html>

                    '''
            
                    )

                        notify.save()
                else:
                    pass


            return JsonResponse("application submitted successfully",safe=False)

'''
==========================================
uploads application details
==========================================
'''
@login_required    
def upload_process(request):
    if request.POST:
       form = ApprovalForm(request.POST,request.FILES)
       if form.is_valid():
            ''''
            form.instance.applicant = request.user
            form.instance.created = datetime.now()
            form.save()
            '''
            try:
                emp = Employee.objects.get(emp_id = request.user.username)
                approvers = emp.departments.approvers.split('\n')
                notifiers = emp.departments.notifiers.split('\n')
            except:
                return JsonResponse("not created as employee",safe=False)
            #approvers = Approvals.objects.get(name=form.cleaned_data.get("approvals"))
            approvers = [app.rstrip() for app in approvers if app!=request.user.username]
            
            if "leave" in str(Approvals.objects.get(name=form.cleaned_data.get("approvals")).name):
                return JsonResponse("kindly, submit leave applications on attendance page!!",safe=False)
            else:
                
            
                application = Applications(
                    type = Approvals.objects.get(name=form.cleaned_data.get("approvals")),
                    applicant = request.user,details = form.cleaned_data.get("details"),
                    attachment = form.cleaned_data.get("attachments"),remarks = "",
                    approvers = ",".join(approvers),expected = len(approvers),
                    created_date = datetime.now(),
                    created_time = datetime.now()+timedelta(hours=3)
                
                    
                )
                application.save()

                for approve in approvers+notifiers:

                    if User.objects.filter(username=approve).exists():
                
                        notify = Notifications(
                            recipient = User.objects.get(username=approve),
                            info = str(request.user.username)+" "+str(form.cleaned_data.get("approvals"))+" new approval",
                            date = datetime.now(),
                            time = datetime.now()+timedelta(hours=3),
                            application = application.pk,
                            url = "{}",
                            details = f'''
                            <html>
                                    <h4>Type:</h4>
                                    <br>
                                    {Approvals.objects.get(name=form.cleaned_data.get("approvals")).name}
                                    <br>
                                    <h4> Requested by: </h4>
                                        <br>
                                            <p>{emp.first_name} {emp.second_name}</p>
                                        <br>

                                    {form.cleaned_data.get("details")}


                            </html>
                            '''
                
                        )

                        notify.save()
                    else:
                        pass

                
                return JsonResponse("application submitted successfully",safe=False)
    


'''
==========================================
direct processing all applications i.e approving applications
==========================================
'''
@login_required
def approve(request):

    if request.POST:
        id = request.POST.get("id")
        application = Applications.objects.get(pk=id)
        application.approvers = ",".join([i for i in application.approvers.split(',') if i!=request.user.username])
        #print(application.approvers)

        application.stage +=1
        if application.stage == application.expected:
        
            application.status = "complete"
            application.rate = 100
            application.save()
            
            try:
                settings = AttSettings.objects.get(employee_id = application.applicant.username )
            except:
                return JsonResponse("attendance settings not added",safe=False)

            if application.category == "annual":
                
                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = "",
                        leave_days = settings.leave_days - application.days
                        
                    )

                    att.save()

                    settings.leave_days = settings.leave_days - application.days
                    settings.save()

            elif application.category == "sick":

                    
                    

                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "sick-leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = "",
                        
                        
                    )

                    att.save()

                    settings.sick_leave_days = settings.sick_leave_days - application.days
                    settings.save()
            
            elif application.category == "compassionate":

                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "compassionate-leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = "",
                        
                        
                    )

                    att.save()

                    settings.compassionate_leave_days = settings.compassionate_leave_days - application.days
                    settings.save()




        else:
            application.status = "pending"
            application.rate = int((application.stage / application.expected)*100)
            application.save()



        return JsonResponse("approved successfully",safe=False)


'''
==========================================
processing all applications i.e rejecting applications
==========================================
'''
@login_required
def reject_approval(request):

    if request.POST:

        id = request.POST.get("id")
        application = Applications.objects.get(pk=id)
        application.status = "rejected"
        application.approvers = ''
        application.save()

        return JsonResponse("rejected successfully",safe=False)

'''
==========================================
processing all applications by adding comments approving and rejecting applications
==========================================
'''
@login_required() 
def approve_by_details(request):

    if request.POST:
        id = request.POST.get("id")
        status = request.POST.get("status")
        comments = request.POST.get("comments")

        if status == "approve":
            application = Applications.objects.get(pk=id)
            application.approvers = ",".join([i for i in application.approvers.split(',') if i!=request.user.username])
            

            application.stage +=1
            if application.stage == application.expected:
                application.status = "complete"
                application.rate = 100
                application.save()
                try:
                    settings = AttSettings.objects.get(employee_id = application.applicant.username )
                except:
                    return JsonResponse("attendance settings not added",safe=False)
                if application.category == "annual":
                    
                    

                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = "",
                        leave_days = settings.leave_days - application.days
                        
                    )

                    att.save()

                    settings.leave_days = settings.leave_days - application.days
                    settings.save()

                elif application.category == "sick":

                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "sick-leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = "",
                        
                        
                    )

                    att.save()

                    settings.sick_leave_days = settings.sick_leave_days - application.days
                    settings.save()
            
                elif application.category == "compassionate":

                    att = Attendance(
                        employee = Employee.objects.get(emp_id = application.applicant.username),
                        is_leave = True,
                        days = application.days,
                        counts = application.days,
                        remarks = "compassionate-leave "+str(application.start)+" to "+str(application.end),
                        image1 = "", 
                        image2 = "",
                        
                        
                    )

                    att.save()

                    settings.compassionate_leave_days = settings.compassionate_leave_days - application.days
                    settings.save()

                    
                    

                track = approvalTrack(
                    application = Applications.objects.get(pk=id),
                    user = request.user,
                    comments = comments,
                    status = status,
                    date = date.today(),
                    time = datetime.now()+timedelta(hours=3)
                )
                track.save()
                
            else:
                application.status = "pending"
                application.rate = int((application.stage / application.expected)*100)
                application.save()
             
                track = approvalTrack(
                    application = Applications.objects.get(pk=id),
                    user = request.user,
                    comments = comments,
                    status = status,
                    date = date.today(),
                    time = datetime.now()+timedelta(hours=3)
                )
                track.save()
        
            return JsonResponse("approved successfully",safe=False)
        elif status == "reject":
            application = Applications.objects.get(pk=id)
            application.status = "rejected"
            application.approvers = ''
            application.save()

            track = approvalTrack(
                application = Applications.objects.get(pk=id),
                user = request.user,
                comments = comments,
                status = status,
                date = date.today(),
                time = datetime.now()+timedelta(hours=3)
            )
            track.save()

            return JsonResponse("application rejected successfully",safe=False)

'''
==========================================
cancel application initiated: recall initiated by applicant
==========================================
'''
@login_required        
def recall_approval(request):

    if request.POST:

        pk = request.POST.get("id")

        if Applications.objects.get(pk=pk).stage > 0:

            return JsonResponse("application already read cannot be recalled, add comment instead",safe=False)
        else:

            application = Applications.objects.get(pk=pk)
            application.status = "cancelled"
            application.save()

            return JsonResponse("recalled successful",safe=False)

'''
==========================================
adding comments to indicate application recall: recall initiated by applicant.
incase the applications is processed by atleats one approver
==========================================
'''
def recall_by_comment(request):

    if request.POST:

        remark = request.POST.get("remark")
        id = request.POST.get("id")
        print(id)
        application = Applications.objects.get(pk = id)
        track = approvalTrack(
            application = application,
            user = request.user,
            comments =remark,
            status = "cancelled",
            date = datetime.now(),
            time = datetime.now()+timedelta(hours=3)
        )
        track.save()
        return JsonResponse("remark added successfully",safe=False)

'''
==========================================
list of application details
==========================================
'''
@login_required
@csrf_exempt
def view_approval_details(request):

    if request.POST:

        id = request.POST.get("id")

        details = {
            "title":str(Applications.objects.get(pk=id).type.name),
            "details":Applications.objects.get(pk=id).details,
            "start":Applications.objects.get(pk=id).start,
            "end":Applications.objects.get(pk=id).end,
            "days":Applications.objects.get(pk=id).days,
            "applicant":"".join([str(emp.first_name)+ " "+str(emp.second_name) if len(Employee.objects.filter(emp_id=Applications.objects.get(pk=id).applicant.username))>0 else "no employee details" for emp in Employee.objects.filter(emp_id=Applications.objects.get(pk=id).applicant.username)]),
            "category":Applications.objects.get(pk=id).category,
            "department":"".join([": "+str(emp.departments.name)+ " Role: "+str(emp.role.name) if len(Employee.objects.filter(emp_id=Applications.objects.get(pk=id).applicant.username))>0 else "no employee details" for emp in Employee.objects.filter(emp_id=Applications.objects.get(pk=id).applicant.username)])

        }

        return JsonResponse(details,safe=False)
@login_required
def profile(request):
    try:
        profile_form = profileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(request.user)


        context = {"profile_form":profile_form,"password_form":password_form, "profiles":Profile.objects.all()}

        if request.method == 'POST':

        
            profile_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
            
            
            if profile_form.is_valid():
        
                profile_form.save()
                

            return JsonResponse("profile updated",safe=False)
    except Exception as error:

        context = {}

        
        


    return render(request,'management/profile.html',context)

# changing current user passwords
@login_required
def change_password(request):

    if request.POST:
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():

            new_user = form.save()
            update_session_auth_hash(request, new_user) 
            
            return JsonResponse("password updated successfully",safe=False)
        else:
            return JsonResponse("check the errors and correct",safe=False)

''''
    displays both announcements and events
'''
@login_required
def Event(request):
    
    events = Events.objects.all().order_by('-created')
    all_events = []
    for event in events:

        event_dict = {

            "title":event.title,
            "details":event.details,
            "created":event.created,
            "image":event.creator.profile.image.url,
            "file":event.files.url,
            "viewers_list":event.viewers_list.split(','),
            "viewers":event.viewers
        }
        all_events.append(event_dict)
    
    context = {"events":all_events,"form":PostsForm()}

    return render(request,'management/events.html',context)

'''
    saves created post
'''
@login_required
def add_event(request):

    if request.method == 'POST':
        
       post_form = PostsForm(request.POST,request.FILES)

       if post_form.is_valid():
           
           instance = post_form.save(commit=False)
           instance.creator = request.user
           if instance.viewers == "all":
               instance.viewers_list = ",".join([user.username for user in User.objects.all()])
           elif instance.viewers == "admins":
               instance.viewers_list = ",".join([user.username for user in User.objects.all() if user.is_staff])
           elif instance.viewers == "members":
               department = Employee.objects.get(emp_id=request.user.username).departments
             
               instance.viewers_list = ",".join([emp.emp_id for emp in Employee.objects.filter(departments=department)])

           instance.save()

           #print("yes")

           return JsonResponse("created successfully",safe=False)

@login_required
def del_event(request):

    if request.POST:

        pk = request.POST.get("pk")

        Events.objects.get(pk=pk).delete()

        return JsonResponse("deleted successfully",safe=False)
@login_required
def Post(request):

    return render(request,'management/post.html')

def get_notify(request):

    notifications = Notifications.objects.filter(recipient=request.user).filter(seen=False).order_by('-pk')[:5]
    popups = []
    for notification in notifications:
        notifs = {
            "image":notification.recipient.profile.image.url,"info":notification.info,
            "date":notification.date,"time":notification.time
            
            }
        popups.append(notifs)
        
    
    notifications = json.dumps(popups,default=str)


    return JsonResponse(notifications,safe=False)
@login_required
def show_map(request,coords):
   
   try:
        
        coords = [float(cord) for cord in coords.split('_')]

        map = folium.Map(coords)
        folium.Marker(coords).add_to(map)
        folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
        folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
        folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
        folium.LayerControl().add_to(map)

        
        map = map._repr_html_()

        context = {
            'map':map
        }
        
        return render(request,'management/map.html',context)
   except:
       
       return HttpResponse("No coordinates recorded!!")

def iframe_redirect(request):

    return render(request,'management/iframe_redirect.html')

@login_required
def live_chat(request):

    profiles = Profile.objects.all()
    
    messages = ChatMessage.objects.filter(recep=request.user.profile,seen=False).order_by('-pk')[:5]
    contxt = {
        
        "messages":messages,"profiles":profiles,
    }
    return render(request,'management/chats.html',contxt)

@login_required
def live_chat_user(request,pk):
    
    
    ind_profile = Profile.objects.get(user_id=pk)
    
    chats = ChatMessage.objects.all().order_by('pk')
    in_chats = ChatMessage.objects.filter(sender = ind_profile , recep = request.user.profile)
    in_chats.update(seen=True)
    chat_form = ChatForm()

    contxt = {
        
        "ind":ind_profile,
        "chats":chats,
        "counts":in_chats.count(),
        "form": chat_form
    }
    
            
            
    
    return render(request,'management/chat.html',contxt)
@login_required
@csrf_exempt
def sent_msg(request,pk):
    
        ind_profile = Profile.objects.get(user_id=pk)
        
        data = json.loads(request.body)
        
        # filter chat from the req body
        chat = data["msg"]
        anony = data["anony"]
      
   
        #Profile.objects.get(user__username="hummingbird")
        if anony == "yes":
     
            new_chat = ChatMessage(
                body = chat , 
                sender = Profile.objects.get(user__username="anonymous") ,
                anonymous_sender = request.user.profile,
                recep = ind_profile,
                sent = datetime.now()+timedelta(hours=3),
                seen = False
                
                )
            new_chat.save()
            return JsonResponse({"mssg":new_chat.body,"date":str(new_chat.sent)},safe=False)
       
        else:
           
            new_chat = ChatMessage(
                body = chat , 
                sender = request.user.profile,
                anonymous_sender = request.user.profile,
                recep = ind_profile,
                sent = datetime.now()+timedelta(hours=3),
                seen = False
                
                )
            new_chat.save()
            return JsonResponse({"mssg":new_chat.body,"date":str(new_chat.sent)},safe=False)

@login_required           
@csrf_exempt
def chat_reply(request):

 

        data = json.loads(request.body)

        id = data["id"]
        msg = data["msg"]
        anony = data["anony"]

        chats = ChatMessage.objects.get(pk=id)

        if anony!="yes":
            new_chat = ChatMessage(
                body = msg , 
                sender = request.user.profile,
                anonymous_sender = request.user.profile,
                recep = chats.sender,
                sent = datetime.now()+timedelta(hours=3),
                seen = False
                
                )
            new_chat.save()
            return JsonResponse({"mssg":new_chat.body,"date":str(new_chat.sent)},safe=False)
        else:

            new_chat = ChatMessage(
                body = msg, 
                sender = request.user.profile ,
                anonymous_sender = request.user.profile,
                recep = chats.sender,
                sent = datetime.now()+timedelta(hours=3),
                seen = False
                
                )
            new_chat.save()

            return JsonResponse({"mssg":new_chat.body,"date":str(new_chat.sent)},safe=False)




@login_required
def chat_notify(request):
    
    
    usrs = Profile.objects.all()

    
    
    usrs_arr,chats_arr,send_arr,dates_arr,pk_arr = [],[],[],[],[]

    for usr in usrs:
        chats = ChatMessage.objects.filter(sender__id = usr.id , recep = request.user.profile,seen=False).order_by('-pk')
        usrs_arr.append(chats.count())
        for chat in chats:
            chats_arr.append(chat.body)
            send_arr.append(str(chat.sender.first)+"@"+str(chat.sender.user.username))
            dates_arr.append(chat.sent)
            

    res_dict = {

                    "no":usrs_arr,"msg":chats_arr,"sender":send_arr,"dates":dates_arr,

                    


                }
   
    return JsonResponse(res_dict,safe=False)

@login_required
def recv_msg(request,pk):
    
    ind_profile = Profile.objects.get(user_id=pk)
    
    chats = ChatMessage.objects.filter(sender = ind_profile , recep = request.user.profile)
    
    chats_arr = []
    
    for chat in chats:
        
        chats_arr.append(chat.body)
        
    return JsonResponse(chats_arr,safe=False)
@login_required
def del_chat(request):

    if request.POST:

        id = request.POST.get("id")

        mssg_del = ChatMessage.objects.get(pk=id)

        mssg_del.delete()

        return JsonResponse("message deleted",safe=False)
@login_required 
def mail_box(request):

    employee = Employee.objects.all()
    

    messages_list = MailMessage.objects.all().order_by('-created')
    page = request.GET.get('page', 1)

    paginator = Paginator(messages_list, 10)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)


    if request.POST:
        
        to = request.POST.get("to")
        body = request.POST.get("message")
        subject = request.POST.get("subject")
        category = request.POST.get("category")

        if category == "anonymous":
            sender_ = Profile.objects.get(user__username="anonymous")
        else:
            sender_ = request.user.profile

       
        try:
                attachment = request.FILES["attachment"]
            
                

                mail = MailMessage(

                    sender = sender_,
                    masked_sender = str(request.user.username),
                    recipient = Profile.objects.get(user__username=to),
                    subject = subject,
                    body = body,
                    attachment = attachment,
                    created = datetime.now()+timedelta(hours=3)
                )

                mail.save()
        except:

                mail = MailMessage(

                    sender = sender_,
                    masked_sender = str(request.user.username),
                    recipient = Profile.objects.get(user__username=to),
                    subject = subject,
                    body = body,
                
                    created = datetime.now()+timedelta(hours=3)
                )

                mail.save()

        
        

        return JsonResponse("message sent successfully",safe=False)

    context= {"employees":employee,"messages":messages}

    return render(request,'management/mail_box.html',context)
@login_required
@csrf_exempt
def mail_actions(request):

    if request.POST:

        id = request.POST.get("id")
        pks = request.POST.get("pks").split(',')
        msg = ''
        if int(id) == 1:
            
            for pk in pks:
                mail_filt_pk = MailMessage.objects.get(pk=int(pk))
                mail_filt_pk.label = "star"
                mail_filt_pk.save()
                msg+="starred"

        elif int(id) == 2:

            for pk in pks:

                mail_filt_pk = MailMessage.objects.get(pk=int(pk))
                mail_filt_pk.delete()
                msg+="deleted"

        return JsonResponse(msg,safe=False)
@login_required  
@csrf_exempt
def get_mail_body(request):

    if request.POST:
        
        pk = request.POST.get("id")

        message_filt =  MailMessage.objects.get(pk=pk)

        message_filt.seen = True

        message_filt.save()
        try:
            message_dict = {

                "subject":message_filt.subject, "body":message_filt.body,
                "attachment":message_filt.attachment.url
            }
        except:

            message_dict = {

                "subject":message_filt.subject, "body":message_filt.body,
                "attachment":""
            }


        return JsonResponse(message_dict,safe=False)
@login_required   
@csrf_exempt
def mail_notify(request):

    messages = MailMessage.objects.filter(recipient = request.user.profile).filter(seen=False).order_by('-pk')[:5]
 
    msg_list = []
    for message in messages:

        msg_dict ={

             "sender":str(message.sender.first)+" @ " +str(message.sender.user.username),
             "subject":message.subject,
             "time":message.created,
        }

        msg_list.append(msg_dict)

    msg_dict_list = json.dumps(msg_list,default=str)
    
    return JsonResponse(msg_dict_list,safe=False)





class EditEmpView(LoginRequiredMixin,UpdateView):
    
    model = Employee
    template_name = 'management/add_employees.html'
    fields = '__all__'
    
    raise_exception = True

    success_url = '/iframe_redirect'
   

    def form_valid(self,form):
        return super().form_valid(form)
    
    

    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'management/password_reset.html'
    email_template_name = 'management/password_reset_email.html'
    subject_template_name = 'management/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('management-home')    


'''
    ===============data Analytics views===================

'''