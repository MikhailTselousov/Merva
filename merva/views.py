from django.shortcuts import render, redirect
from .forms import SignupForm

def sign_up(request):
    signupForm = SignupForm()

    if request.method == 'POST':
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            signupForm.save()
            return redirect('login')
    
    context = {
        'form': signupForm,
    }
    return render(request, 'registration/sign_up.html', context)