from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
import os
# user authentication
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash

# user auth forms
from django.contrib.auth.forms import UserCreationForm
from .djangoForms.registration import BuiltinUserCreationForm,BuiltinEmployerCreationForm

# for editing
from .djangoForms.password_change_form import PasswordCustomChangeForm
from .djangoForms.password_edit_form import UserChangeCustomForm,FullUserDetailsForm,EmployerChangeCustomForm,FullEmployerDetailsForm
# user auth model
from django.contrib.auth.models import User

# flash messages
from django.contrib import messages

#  Custom forms
from .djangoForms.job_posting import JobPostingForm

from .djangoForms.password_edit_form import UserDetailsForm

# Custom Models
from .models import JobPosting , EmployerDetails ,UserDetails

# for search
from django.db.models import Q
# Create your views here.

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    html_email_template_name = 'parmeen/password_reset_email.html'
    html_subject_template_name = 'parmeen/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')



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

def home (request):
    # return HttpResponse( 'working')
   job_posting=JobPosting.objects.all()
   if request.user.is_authenticated:
      return  render (request , 'main.html',{'jobs':job_posting})
   else:
     messages.error(request,'Kindley login first!.')
     return redirect ('candidate_login')
 

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


def profile_page(request, id):
    # Try to retrieve the user
    user = User.objects.get(id=id)
    try:
        user_details = UserDetails.objects.filter(user=user)
        if user_details.exists():
        # return HttpResponse (user_details)
           return render(request, 'Candidate/candidate_profile_page.html', { 'user_details': user_details})
        else:
             employer_details = EmployerDetails.objects.filter(employer=user)
            # return HttpResponse (employer_details)
             return render(request, 'Employer/employer_profile_page.html', { 'employer_details': employer_details})
    except UserDetails or EmployerDetails.DoesNotExist:
        # If neither UserDetails nor EmployerDetails found, return a response indicating so
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
def candidate_registration (request):
    if request.method == 'GET':
        form = BuiltinUserCreationForm()
        return render(request, 'Candidate/registration.html', {'form_data': form})
    else:
        form = BuiltinUserCreationForm(request.POST, request.FILES)
        specialization= request.POST['specialization']
        
        if form.is_valid() and specialization:
            user=form.save()
            
            edit_user= UserDetails (specialization=specialization,user=user,type=0)
            edit_user.save()
            messages.success(request, 'User registered successfully.')
            # return HttpResponse (edit_user)
            return redirect (candidate_login)
        else:
            messages.error(request, 'Please fill out the form correctly.')
            return render(request, 'Candidate/registration.html', {'form_data': form})


def candidate_login(request):
    if request.method == 'GET':
        return render(request, 'Candidate/login.html')
    else:
        username = request.POST['username']
        user_password = request.POST['password']

        user = authenticate(request, username=username, password=user_password)

        if user is not None:
            try:
                user_details = UserDetails.objects.get(user=user)
                if user_details.type == 0:
                    login(request, user)
                    messages.success(request, 'Logged In successfull!')
                    return redirect('home')
                else:
                    messages.error(request, 'You are not registered as an candidate.')
                    return redirect('candidate_login')
                
            except UserDetails.DoesNotExist:
                messages.error(request, 'User account not associated with a user type. Please contact support.')
                return redirect('candidate_login')

            
        else:
            messages.error(request, "Username or Password is incorrect")
            return redirect('candidate_login')
            # return HttpResponse(user)
        # return HttpResponse(request.POST)

def candidate_logout(request):
    logout(request)
    messages.success(request,"Logged out successfully!.")
    return redirect('candidate_login')


def candidates (request):
    # users = User.objects.all()
    user_details = UserDetails.objects.all()
    #    return HttpResponse (users)
    return render(request, 'Candidate/candidates.html',{'user_details':user_details})

def candidate_profile_page (request,id):
    #  user=User.objects.get(id=id)
     try:  
        user_details = UserDetails.objects.filter(id=id)
        # user_details = UserDetails.objects.get(user_details=user_details)      
        return render (request,'Candidate/candidate_profile_page.html',{'user_details':user_details})

     except:
        
    #     return HttpResponse ('except')
        return HttpResponse (user_details)



def myprofile (request):
    # Get the currently logged-in user
    user = request.user
    # return HttpResponse (user)
    return render(request, 'Candidate/myprofile.html', {'user': user})
 

def employer_registration(request):
    if request.method == 'GET':
        form = BuiltinEmployerCreationForm()
        return render(request, 'Employer/registration.html', {'form_data': form})
    else:
        form = BuiltinEmployerCreationForm(request.POST, request.FILES)
        company = request.POST.get('company')
        
        if form.is_valid() and company:
            user = form.save(commit=False)  # Get user instance without saving to database yet
            user.save()  # Save user to database
            
            employer_details = EmployerDetails.objects.create(company=company, employer=user, type=1)
            
            messages.success(request, 'User registered successfully')
            return redirect('employer_login')
        else:
            messages.error(request, 'You did not follow the instructions')
            return HttpResponse (form.errors)
            return render(request, 'Employer/registration.html', {'form_data': form})       

def employer_login(request):
    if request.method == 'GET':
        return render(request, 'Employer/login.html')
    else:
        username = request.POST['username']
        employer_password = request.POST['password']

        employer = authenticate(request, username=username, password=employer_password)

        if employer is not None:
            try:
                employer_details = EmployerDetails.objects.get(employer=employer)
                if employer_details.type == 1:
                   login(request, employer)
                   messages.success(request, 'Logged In successfull!')
                   return redirect('home')
                else:
                    messages.error(request, 'You are not registered as an candidate.')
                    return redirect('candidate_login')
            
            except EmployerDetails.DoesNotExist:
                messages.error(request, 'User account not associated with a user type. Please contact support.')
                return redirect('employer_login')
                # return HttpResponse (EmployerDetails.type)

           
        else:
            messages.error(request, "Username or Password is incorrect")
            return redirect('candidate_login') # Redirect back to the login page regardless of the error

    
    

def about_us (request):
    return render (request, 'about_us.html')


def terms_for_users (request):
    return render (request, 'terms_for_users.html')

def contact_us(request):
    return render (request, 'contact_us.html')

def job_posting(request):
    if request.method == "GET":
        jobs= JobPostingForm()
        return render (request, 'Employer/job_posting.html',{'job_posting':jobs})
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



def employer_profile_page (request,id):
    
     try:  
        employer_details = EmployerDetails.objects.filter(id=id)
        # user_details = UserDetails.objects.get(user_details=user_details)      
        return render (request,'Employer/employer_profile_page.html',{'employer_details':employer_details})

     except:
        
    #     return HttpResponse ('except')
        return HttpResponse (employer_details)
     


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
        user = User.objects.get(id=id)
        user_details = UserDetails.objects.filter(user=user)
        employer_details = EmployerDetails.objects.filter(employer=user)

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
 

def user_details_edit(request, id):
    # Retrieve the user based on the id
    user = User.objects.get(id=id)

    try:
        # Check if the user is an employer or a candidate
        employer_details = EmployerDetails.objects.get(employer=user)

        if employer_details.type == 1:  # If the user is an employer
            if request.method == 'GET':
                # Pass the EmployerDetails instance to the form if it exists
                full_employer_details_form = FullEmployerDetailsForm(instance=employer_details)
                return render(request, 'Employer/employer_details_edit.html', {
                    'full_employer_details_form': full_employer_details_form,
                    'user_id': id
                })
            elif request.method == 'POST':
                company = request.POST.get('company')  # Use get to avoid KeyError
                
                # Pass the instance and additional data to the form
                full_employer_details_form = FullEmployerDetailsForm(request.POST, instance=employer_details)

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
                full_user_details_form = FullUserDetailsForm(instance=user_details)
                return render(request, 'Candidate/user_details_edit.html', {
                    'full_user_details_form': full_user_details_form,
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
                full_user_details_form = FullUserDetailsForm(request.POST,request.FILES, instance=user_details)
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
                    return HttpResponse(full_user_details_form.errors)
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
