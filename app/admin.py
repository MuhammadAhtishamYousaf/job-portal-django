from django.contrib import admin
from .models import JobPosting , EmployerDetails, UserDetails

class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('id','job_title','job_location','skills_required','posting_date','salary','industry','education','experience_required', 'gender', 'company_name')

class EmployerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','industry','company','contact_no','location','employer','type','company_logo') 

admin.site.register(EmployerDetails,EmployerDetailsAdmin)

#  Register your models here.
admin.site.register(JobPosting,JobPostingAdmin)
# # admin.site.register(Myuser,MyAdmin)

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','location','mobile_no','skills','specialization','education','university','priveus_job','interests', 'gender','user','type','profile_img' )

#  Register your models here.
admin.site.register(UserDetails,UserDetailsAdmin)
# # admin.site.register(Myuser,MyAdmin)