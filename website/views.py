from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from website.forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()


    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ' successfully! LoggedIn')
            return redirect('home')
        else:
            messages.success(request, ' Fail! To LoggedIn')
            return redirect('home')
    else:
          return render(request,'website/home.html',{'records': records})
    
def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, ' successfully! LoggedOut')
    return redirect('home')

 
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate the user after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully registered and logged in!')
                return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    # Always return a response
    return render(request, 'website/register.html', {'form': form})






def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'website/record.html', {'customer_record': customer_record})
    else:
        messages.error(request, 'You need to be logged in to view this page.')
        return redirect('home')
        
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()

        messages.success(request, 'Record deleted successfully!')
        return redirect('home')
    else:
        messages.error(request, 'You need to be logged in to delete a record.')
        return redirect('home')




def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
       
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record added successfully!')
                return redirect('home')
        return render(request, 'website/add_record.html', {'form': form})
    else:
        messages.success(request, 'You need to be logged in to add a record.')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record updated successfully!')
                return redirect('home')
        return render(request, 'website/update_record.html', {'form': form, 'record': record})
    else:
        messages.error(request, 'You need to be logged in to update a record.')
        return redirect('home')