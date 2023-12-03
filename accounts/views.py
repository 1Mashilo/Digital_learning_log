from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """
    Handle user registration.

    If the request method is GET, display a blank registration form.
    If the request method is POST, process the submitted form:
        - Validate the form.
        - Save the new user.
        - Log in the user.
        - Redirect to the home page.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered registration template.
    """
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

