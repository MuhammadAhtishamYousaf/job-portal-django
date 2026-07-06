from django.urls import path # type: ignore
from .import views
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView # type: ignore
from app.views import home


from django.urls import path
from .views import CustomPasswordResetView

urlpatterns = [
    path('swiper/',views.swiper, name= 'swiper'),
    path('search/',views.search, name='search'),
    # path('reset_password/',PasswordResetView.as_view(template_name='parmeen/password_reset_form.html'), name='password_reset'),
    # path('reset_password/done/', PasswordResetDoneView.as_view(template_name='parmeen/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='parmeen/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset_password/complete/',PasswordResetCompleteView.as_view(template_name='parmeen/password_reset_complete.html'), name='password_reset_complete'),


    path('reset_password/', CustomPasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password/complete/', PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),



    path('swiper/',views.swiper, name='swiper'),
    path('',views.home, name='home'),
    path('jobs/',views.jobs, name='jobs'),
    
    path('candidate_registration/', views.candidate_registration, name='candidate_registration'), 
    path('candidate_login/',views.candidate_login, name='candidate_login'),
    path('employer_registration/',views.employer_registration, name='employer_registration'),
    path('employer_login/',views.employer_login, name='employer_login'),
    path('check-registration-field/', views.check_registration_field, name='check_registration_field'),
    path('user_logout/',views.user_logout, name= 'user_logout'),
    
    
    path('about_us/',views.about_us, name='about_us'),
    
    path('terms_for_users/',views.terms_for_users, name='terms_for_users'),
    
    path('contact_us/',views.contact_us, name='contact_us'),
    
    path('job_posting/',views.job_posting, name='job_posting'),
    path('privacy_and_policy/',views.privacy_and_policy, name='privacy_and_policy'),
    path('things_you_should_know/',views.things_you_should_know, name='things_you_should_know'),
    path('writing_resume/',views.writing_resume, name='writing_resume'),
    path('most_asked/',views.most_asked, name='most_asked'),
    path('stay_confident/',views.stay_confident, name='stay_confident'),
    path('writing_email/',views.writing_email, name='writing_email'),

    path('user_dashboard/',views.user_dashboard, name='user_dashboard'),
   
   path('delete_user/<int:id>',views.delete_user, name='delete_user'),
    #  path('update_user/',views.update_user, name='update_user'),
     
    path ('AdminPanel/',views.AdminPanel, name= 'AdminPanel'),
    path ('AdminPanel/Candidate_details/',views.Candidate_details, name= 'Candidate_details'),
    path ('AdminPanel/Employer_details/',views.Employer_details, name= 'Employer_details'),
    path ('AdminPanel/JobPosted/',views.JobPosted, name= 'JobPosted'),
   
    
    path ('user_edit/<int:id>',views.user_edit, name= 'user_edit'),
    # path ('employer_edit/<int:id>',views.employer_edit, name= 'employer_edit'),
    
    # path ('employer_details_edit/<int:id>',views.employer_details_edit, name= 'employer_details_edit'),
    
    path ('user_details_edit/<int:id>',views.user_details_edit, name= 'user_details_edit'),
    path("profile/", views.profile, name="profile"),
    
    path(
        "candidate/profile/edit/",
        views.candidate_profile_edit,
        name="candidate_profile_edit",
    ),
    path(
        "employer/profile/edit/",
        views.employer_profile_edit,
        name="employer_profile_edit",
    ),
    # path('custom_candidate_registration/',views.custom_candidate_registration, name='custom_candidate_registration'), 
    # path('custom_candidate_login/',views.custom_candidate_login, name='custom_candidate_login'), 
    path('candidates/',views.candidates, name='candidates'), 
    path('Employers/',views.employers, name='Employers'), 
    path('myprofile/',views.myprofile, name='myprofile'), 

    path('profile_page/', views.profile_page, name='profile_page'), 
    # path('employer_profile_page/<str:username>',views.employer_profile_page, name='employer_profile_page'), 

    path('home/full_job_profile/',views.full_job_profile, name='full_job_profile'), 

    path('change_password/',views.change_password, name='change_password'),
    # path('edit_custom_user/',views.edit_custom_user, name='edit_custom_user'), 
    path('navbar/',views.Navbar, name='navbar'),
    path('companies/',views.companies, name='companies'),
]
