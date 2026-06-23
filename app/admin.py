from django.contrib import admin
from .models import JobPosting , EmployerDetails, UserDetails

#  Register your models here.

class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('id','job_title','job_location','skills_required','posting_date','salary','industry','education','experience_required', 'gender', 'company_name')

admin.site.register(JobPosting,JobPostingAdmin)


class EmployerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','industry','company','contact_no','location','employer','type','company_logo') 

admin.site.register(EmployerDetails,EmployerDetailsAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','location','mobile_no','skills','specialization','education','university','priveus_job','interests', 'gender','user_id','type','profile_img' )

admin.site.register(UserDetails,UserDetailsAdmin)
# # admin.site.register(Myuser,MyAdmin)