from django.urls import path 
from . import views 
from .views import home,clock,add_department,\
      add_roles,add_employee,add_info,approvals,list_employee,\
      view_approvals,Post,Event,leave,get_emp_files,get_attendance,\
      upload_leave,approve,upload_process,register,list_files,profile,EditEmpView,ResetPasswordView,\
      get_employee,reject_approval,approve_by_details,get_notify,departments,dep_details, recall_approval,\
            add_event,del_event,show_map,files_details,iframe_redirect

      

urlpatterns = [
     path('',views.home,name="management-home"),
     path('clock',views.clock,name="management-clock"),
     path('get_attendance',views.get_attendance,name="management-get-attendance"),
     path('add_info',views.add_info,name="management_add_info"),
     path('add_departments',views.add_department,name="management_add_department"),
     path('add_roles',views.add_roles,name="management_add_roles"),
     path('add_employees',views.add_employee,name="management_add_employee"),
     path('approvals',views.approvals,name="management_approvals"),
      path('list_employee',views.list_employee,name="management_list_employee"),
       path('list_departments',views.departments,name="management_list_departments"),
       path('department_details/<str:name>',views.dep_details,name="management_departments_details"),
       path('get_employee',views.get_employee,name="management_get_employee"),
      path('get_files',views.get_employee,name="management_get_files"),
      path('files_details/<str:id>',views.files_details,name="management_files_details"),
      path('list_approvals',views.view_approvals,name="management_list_approvals"),
      path('leave',views.leave,name="management_leave"),
      path('upload_leave',views.upload_leave,name="management_upload_leave"),
      path('approve',views.approve,name="management_approve"),
      path('reject',views.reject_approval,name="management_reject"),
      path('approve_by_details',views.approve_by_details,name="management_approve_by_details"),
      path('recall_approval',views.recall_approval,name="management_recall_approval"),
      path('upload_process',views.upload_process,name="management_upload_process"),
      path('events',views.Event,name="management_events"),
      path('add_event',views.add_event,name="management_add_event"),
      path('delete_event',views.del_event,name="management_del_event"),
      path('posts',views.Post,name="management_post"),
      path('register',views.register,name="management_register"),
      path('list_files',views.list_files,name="management_files"),
      path('iframe_redirect',views.iframe_redirect,name="management_iframe_redirect"),
      path('profile',views.profile,name="management_profile"),
      path('get_notify',views.get_notify, name='management_get_notify'),
      path('show_map/<str:coords>',views.show_map, name='management_show_map'),
      path('edit_employee/<int:pk>',EditEmpView.as_view(),name="management-edit-employee"),
      path('password-reset', ResetPasswordView.as_view(), name='password_reset'),

]