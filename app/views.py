import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .djangoForms.password_change_form import PasswordCustomChangeForm
from .djangoForms.password_edit_form import (
    AccountForm,
    UserDetailsForm,
    EmployerDetailsForm,
)
from .djangoForms.job_posting import JobPostingForm
from .djangoForms.registration import BuiltinUserCreationForm, BuiltinEmployerCreationForm

from .models import JobPosting, EmployerDetails, UserDetails


class CustomPasswordResetView(PasswordResetView):
    html_email_template_name = 'password_reset/password_reset_email.html'
    html_subject_template_name = 'password_reset/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

def candidate_registration(request: WSGIRequest):
    if request.method == 'POST':
        form = BuiltinUserCreationForm(request.POST)
        if form.is_valid():
            try:
                specialization = form.cleaned_data.get('specialization')
                with transaction.atomic():
                    user = form.save()
                    UserDetails.objects.create(specialization=specialization, user=user, type=0)
                messages.success(request, 'User registered successfully.')
                return redirect('candidate_login')
            except Exception:
                messages.error(request, 'Something went wrong.')
    else:
        form = BuiltinUserCreationForm()

    return render(request, 'candidate/registration.html', {'form_data': form})

def candidate_login(request):
    
    if request.method == 'GET':
        return render(request, 'candidate/login.html')
  
    username = request.POST.get('username')
    user_password = request.POST.get('password')

    user = authenticate(request, username=username, password=user_password)

    if user is not None:
        
        if user.is_superuser or user.is_staff:
            login(request, user)
            messages.success(request, "logged In succesfully!")
            return redirect(home)

        try:
            user_details = UserDetails.objects.get(user = user)
            if user_details.type == 0:
                login(request, user)
                messages.success(request, 'Logged In successfully!')
                return redirect(home)
            
            else:
                messages.error(request, 'You are not registered as an candidate.')
                return redirect(candidate_login)
            
        except UserDetails.DoesNotExist as e:
            messages.error(request, str(e))
            return redirect('candidate_login')

        
    else:
        messages.error(request, "Username or Password is incorrect")
        return redirect(candidate_login)

def employer_registration(request):
    if request.method == 'POST':
        form = BuiltinEmployerCreationForm(request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                company = form.cleaned_data.get('company')
                EmployerDetails.objects.create(employer=user, company=company, type=1)
            
            messages.success(request, 'Employer registered successfully.')
            return redirect('employer_login')
                
    else:
        form = BuiltinEmployerCreationForm()
        
    return render(request, 'employer/registration.html', {'form_data': form})

def check_registration_field(request):
    field = request.GET.get('field')
    value = request.GET.get('value', '').strip()

    if not field or not value:
        return JsonResponse({'exists': False})

    if field == 'username':
        exists = User.objects.filter(username__iexact=value).exists()
    elif field == 'email':
        exists = User.objects.filter(email__iexact=value).exists()
    else:
        return JsonResponse({'exists': False})

    return JsonResponse({'exists': exists})

def employer_login(request: WSGIRequest):
    
    if request.method == 'GET':
        return render(request, 'employer/login.html')
    
    username = request.POST.get('username', '').strip()
    employer_password = request.POST.get('password', '')
    
    employer = authenticate(request, username=username, password=employer_password)
    
    if employer is None:
        messages.error(request, "Username or Password is incorrect")
        return redirect('employer_login') # Redirect back to the login page regardless of the error
        
    if not (employer.is_staff or employer.is_superuser):
        
        try:
            employer_details = EmployerDetails.objects.filter(employer=employer).first()
        except EmployerDetails.DoesNotExist:
            messages.error(request, 'Your account is not linked to an employer profile.')
            return redirect('employer_login')
        
        if employer_details.type != 1:
            messages.error(request, 'You are not registered as an employer.')
            return redirect('employer_login')

    login(request, employer)
    messages.success(request, 'Logged In successfully!')
    return redirect('home')

def user_logout(request):
    logout(request)
    messages.success(request,"Logged out successfully!.")
    return redirect('candidate_login')

def search (request):
    query = request.GET.get('query', '')  # Use .get() to safely retrieve the query
    if len(query) > 60:
        # Handle the case where the query is too long
        job_postings = []
        error_message = "Your search query is too long. Please enter a shorter query."
    else:
        job_postings = JobPosting.objects.filter(
            Q(job_title__icontains=query) | 
            Q(job_location__icontains=query) | 
            Q(industry__icontains=query)
        )
        error_message = None  # No error if query length is valid

    return render(request, 'search.html', {
        'jobs': job_postings,
        'query': query,
        'error_message': error_message,
    })




def swiper (request):
    return render (request,'swiper.html')

def home(request):
    if request.user.is_authenticated:
        return  render(request , 'main.html')
    
    else:
        messages.error(request,'Kindley login first!')
        return redirect(candidate_login)

def companies(request):
    return render(request, 'companies.html')


def jobs(request):
    job_postings = JobPosting.objects.all()
    return render(request, 'jobs.html', {'jobs': job_postings})
 
def Navbar(request):
    user = User.objects.get(id=request.user.id)
    
    if request.user.is_authenticated:
        current_user = UserDetails.objects.get(user=request.user)
        # return HttpResponse(current_user)
        return render(request, '_navbar.html', {'current_user': current_user})
    else:
        return HttpResponse("User not authenticated.")
    
def AdminPanel (request):
    return render (request,'ForAdmin/AdminNav.html')
 
def swiper (request):
    return render (request,'swiper.html')

@login_required
def profile_page(request: WSGIRequest):
    user = request.user
    user_details = UserDetails.objects.filter(user=user).first()
    if user_details:
        return render(request, 'candidate/candidate_profile_page.html', {'user_details': user_details})

    employer_details = EmployerDetails.objects.filter(employer=user).first()
    if employer_details:
        return render(request, 'employer/employer_profile_page.html', {'employer_details': employer_details})

    return HttpResponse('User Details Does not Exist!')
    
# def candidate_registration (request):
    # if request.method == 'GET':
    #  form = BuiltinUserCreationForm()
    # #  return HttpResponse (form)
    #  return render (request, 'Candidate/registration.html' ,{ 'form_data':form})
    # else:
    #     form = BuiltinUserCreationForm(request.POST,request.FILES)
    #     # return HttpResponse(form)

    #     first_name= request.POST['first_name']
    #     email= request.POST['email']
    #     username= request.POST['username']
    #     password1= request.POST['password1']
    #     password2= request.POST['password2']

    #     if not password1:
    #              messages.error(request, 'Password cannot be empty')
    #              return  HttpResponse (form.errors)
    #              return redirect('candidate_registration')     
    #     elif User.objects.filter(first_name=first_name).exists():
    #            messages.error(request,'Name already exist')
    #            return redirect('candidate_registration')
    #     elif User.objects.filter(username=username).exists():
    #           messages.error(request,'Username already exist')
    #           return redirect('candidate_registration')
    #     elif User.objects.filter(email=email).exists():
    #          messages.error(request,'email already exist')
    #          return redirect('candidate_registration')
    #     # elif User.objects.filter(password1=password2).exists():
    #     #       messages.error(request,'password is already taken')
    #     #       return redirect('candidate_registration')
    #     elif password1 != password2:
    #          messages.error(request, 'Passwords do not match')
  
    #          return redirect('candidate_registration')
    #     # return  HttpResponse (form.errors)
        
    #     if form.is_valid():
    #         # return HttpResponse ('suscuss')
    #         form.save()
    #         # return HttpResponse(form)
    #         messages.success(request,'User Registered succussfully')
    #         return redirect(candidate_login)
    #     else:
    #         messages.error(request,'Please try again')
    #         return  HttpResponse (form.errors)
    
    

def candidates (request):
    # users = User.objects.all()
    user_details = UserDetails.objects.all()
    #    return HttpResponse (users)
    return render(request, 'candidate/candidates.html',{'user_details':user_details})



def myprofile (request):
    # Get the currently logged-in user
    user = request.user
    # return HttpResponse (user)
    return render(request, 'candidate/myprofile.html', {'user': user})
 
 



def about_us (request):
    return render (request, 'about_us.html')

def terms_for_users (request):
    return render (request, 'terms_for_users.html')

def contact_us(request):
    return render (request, 'contact_us.html')

def job_posting(request):
    if request.method == "GET":
        jobs= JobPostingForm()
        return render (request, 'employer/job_posting.html',{'job_posting':jobs})
    else:
        job_posting = JobPostingForm(request.POST,request.FILES)
        if job_posting.is_valid():
            job_posting.save()
            messages.success(request,'Job Posted Successfully!')
            return redirect ('full_job_profile')
        else:
            messages.error (request,'Same Job has already posted')
            # return redirect( 'job_posting')
            return HttpResponse (job_posting.errors)

def JobPosted(request):
    jobs=JobPosting.objects.all()
    return render (request,'ForAdmin/JobPosted.html',{'jobs':jobs})

def full_job_profile (request):

    jobs = JobPosting.objects.all()
    return render(request,'full_job_profile.html',{'jobs':jobs})

def privacy_and_policy(request):
    return render (request, 'terms_for_users.html')

def things_you_should_know(request):
    return render (request,'blogs/things_you_should_know.html')

def writing_resume(request):
    return render (request,'blogs/writing_resume.html')

def stay_confident(request):
    return render (request,'blogs/stay_confident.html')

def most_asked(request):
    return render (request,'blogs/most_asked.html')

def writing_email(request):
    return render (request,'blogs/writing_email.html')

def user_dashboard (request):
    # return HttpResponse(request.user.is_authenticated)
    users = User.objects.all()
    return render(request,'ForAdmin/Users.html',{'users':users})

def employers (request):
    #  employers=User.objects.all()
     employer_details=EmployerDetails.objects.all()
     return render (request, 'Employer/employers.html',{'employer_details':employer_details})

     
def employer_dashboard (request):
    employers = User.objects.all ()
    return render (request,'Employer/employer_dashboard.html',{'employers':employers})

def delete_user(request,id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request,'User deleted Successfully!')
    return redirect('dashboard')

def user_edit(request, id):
    try:
        # user = User.objects.get(id=id)
        user = User.objects.filter(id=id).first()
        user_details = UserDetails.objects.filter(user=user).first()
        employer_details = EmployerDetails.objects.filter(employer=user).first()

        if employer_details:  # User is an employer
            if request.method == 'POST':
                form = EmployerChangeCustomForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Employer details updated successfully!')
                    return redirect('user_details_edit',id)
                else:
                    messages.error(request, 'Invalid data')
                    return redirect('user_edit', id)
            else:
                form = EmployerChangeCustomForm(instance=user)
                return render(request, 'Employer/employer_edit.html', {'form_data': form, 'user_id': id})
        else:  # User is a candidate
            if request.method == 'POST':
                form = UserChangeCustomForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'User details updated successfully!')
                    return redirect('user_details_edit',id)
                else:
                    messages.error(request, 'Invalid data')
                    return redirect('user_edit', id=id)
            else:
                form = UserChangeCustomForm(instance=user)
                return render(request, 'Candidate/user_edit.html', {'form_data': form, 'user_id': id})

    except UserDetails.DoesNotExist:
        messages.error(request, 'No User Details Found!')
        return redirect('home')

def Candidate_details(request):
   user_details=UserDetails.objects.all()
   return render (request,'ForAdmin/CandidateDetails.html',{'user_details':user_details})
  
def Employer_details(request):
   employer_details=EmployerDetails.objects.all()
   return render (request,'ForAdmin/EmployerDetails.html',{'employer_details':employer_details})
 

@login_required
def profile(request: WSGIRequest):
    """
    Decide which profile edit page the logged-in user should see.
    """

    if UserDetails.objects.filter(user=request.user).exists():
        return redirect("candidate_profile_edit")

    if EmployerDetails.objects.filter(employer=request.user).exists():
        return redirect("employer_profile_edit")

    messages.error(request, "Profile not found.")
    return redirect("home")

@login_required
def candidate_profile_edit(request: WSGIRequest):
    
    user = request.user
    user_details = get_object_or_404(UserDetails, user=user)

    if request.method == "POST":
        
        user_form = AccountForm(request.POST, instance=user)

        profile_form = UserDetailsForm(
            request.POST,
            request.FILES,
            instance=user_details,
        )

        if (user_form.is_valid() and profile_form.is_valid()):
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            
            messages.success(request, "Profile updated successfully.")
            return redirect("profile_page")
    else:

        user_form = AccountForm(
            instance=user
        )

        profile_form = UserDetailsForm(
            instance=user_details
        )

    return render(
        request,
        "candidate/user_details_edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )

@login_required
def employer_profile_edit(request):
    employer_details = get_object_or_404(
        EmployerDetails,
        employer=request.user,
    )

    if request.method == "POST":
        form = EmployerDetailsForm(
            request.POST,
            request.FILES,
            instance=employer_details,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile_page", id = request.user.id)
    else:
        form = EmployerDetailsForm(instance=employer_details)

    return render(
        request,
        "employer/employer_details_edit.html",
        {
            "full_employer_details_form": form,
            "user_id": request.user.id
        },
    )
    
    
def user_details_edit(request, id):
    # Retrieve the user based on the id
    user = User.objects.get(id=id)

    try:    
        # Check if the user is an employer or a candidate
        employer_details = EmployerDetails.objects.get(employer=user)

        if employer_details.type == 1:  # If the user is an employer
            if request.method == 'GET':
                # Pass the EmployerDetails instance to the form if it exists
                full_employer_details_form = EmployerDetailsForm(instance=employer_details)
                return render(request, 'employer/employer_details_edit.html', {
                    'full_employer_details_form': full_employer_details_form,
                    'user_id': id
                })
            elif request.method == 'POST':
                company = request.POST.get('company')  # Use get to avoid KeyError
                
                # Pass the instance and additional data to the form
                full_employer_details_form = EmployerDetailsForm(request.POST, instance=employer_details)

                if full_employer_details_form.is_valid() and company:
                    full_employer_details_instance = full_employer_details_form.save(commit=False)
                    full_employer_details_instance.company = company  # Update company field
                    full_employer_details_instance.save()
                    
                    messages.success(request, 'Employer details updated successfully!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid information')
                    # Redirect back to the edit page with the current user id
                    return redirect('user_details_edit', id=id)

    except EmployerDetails.DoesNotExist:
        # If EmployerDetails does not exist, the user is a candidate
        try:
            # Try to retrieve UserDetails
            user_details = UserDetails.objects.get(user=user)
            
            if request.method == 'GET':
                # Pass the UserDetails instance to the form if it exists
                full_user_details_form = UserDetailsForm(instance=user_details)
                return render(request, 'candidate/user_details_edit.html', {
                    'form': full_user_details_form,
                    'user_id': id                                                                                                                       
                })
            elif request.method == 'POST':
                specialization = request.POST.get('specialization')  # Use get to avoid KeyError
                if 'profile_img' in request.FILES:
                    if user_details.profile_img:
                        # Remove the existing profile image file
                        os.remove(user_details.profile_img.path)
                    # Update the profile_img field with the new image
                    user_details.profile_img = request.FILES['profile_img']
                   
                # Pass the instance and additional data to the form
                full_user_details_form = UserDetailsForm(request.POST,request.FILES, instance=user_details)
                full_user_details_form.type=0
                full_user_details_form.user=request.user

                if full_user_details_form.is_valid() and specialization:
                    full_user_details_instance = full_user_details_form.save(commit=False)
                    full_user_details_instance.specialization = specialization  # Update specialization field
                    full_user_details_instance.save()
                    
                    messages.success(request, 'User details updated successfully!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid information')
                    # Redirect back to the edit page with the current user id
                    # return HttpResponse(full_user_details_form.errors)
                    return redirect('user_details_edit',id)

        except UserDetails.DoesNotExist:
            messages.error(request, 'User details not found')
            return redirect('home')
        
def change_password(request):
    
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = PasswordCustomChangeForm(request.user)
            # return HttpResponse(form)
            return render(request,'password_change.html', {'form' : form})
        else:
            form = PasswordCustomChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request,user)
                messages.success(request,'password updated successfully!')
                return redirect('candidate_login')
            else:
                for error in form.errors:
                    messages.error(request,f'provide valid information in {error}')
                return redirect('change_password') 
    else:
        return redirect('home')
