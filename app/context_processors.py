from .models import EmployerDetails, UserDetails


def navbar_user(request):
    """
    Provide navbar-friendly profile info for authenticated users.
    """
    if not request.user.is_authenticated:
        return {}

    user = request.user
    profile_image = None
    edit_url_name = "user_details_edit"

    employer_details = EmployerDetails.objects.filter(employer=user).first()
    if employer_details:
        if employer_details.company_logo:
            profile_image = employer_details.company_logo.url
        edit_url_name = "user_details_edit"
    else:
        user_details = UserDetails.objects.filter(user=user).first()
        if user_details and user_details.profile_img:
            profile_image = user_details.profile_img.url
        edit_url_name = "user_details_edit"

    return {
        "navbar_user_profile_image": profile_image,
        "navbar_user_edit_url": edit_url_name,
    }
