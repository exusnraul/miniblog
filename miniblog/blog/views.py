from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .import forms,models

#Home
def home(request):
    posts = models.Post.objects.all()
    return render (request,'blog/home.html',{'posts':posts})
# About Page
def about(request):
    return render (request,'blog/about.html')
#Contact Page
def contact(request):
    return render (request,'blog/contact.html')
#Dashboard
def dashboard(request):
    if  request.user.is_authenticated:
        posts=models.Post.objects.all()
        user = request.user
        full_name=user.get_full_name()
        grps = user.groups.all() #User Grou is being displayed on the page
        return render (request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':grps})
    else:
        return HttpResponseRedirect('/login/')
#Login
def user_login(request):
    if not request.user.is_authenticated: #USer is being checked being authenticated 
        if request.method=='POST':
            form = forms.LoginForm(request=request,data=request.POST)
            if form.is_valid(): #validaing the form
                uname = form.cleaned_data['username']
                pwd = form.cleaned_data['password']
                user = authenticate(username=uname,password=pwd) #Use is being authenticated with supplied data against database
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Succesfully')
                    """
                    Messages module used to pass in all the  important success,warning,danger
                     or info messages to the page
                    """
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = forms.LoginForm()
        return render (request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
#signup
def user_signup(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form = forms.SignupForm(request.POST)
            if form.is_valid():
                messages.success(request,'Congratulations You have created an Account')
                user=form.save()
                #Saving user to Author Group
                group = Group.objects.get(name='Author')  #USed to pass onn the selected User to a selected
                user.groups.add(group)  # already created group to give permissions.

        else:

            form = forms.SignupForm()
        return render (request,'blog/signup.html',{'form':form})
    else:
        return HttpResponseRedirect('/')



# deleting Blog Data

def delete_data(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            user = models.Post.objects.get(pk=id)
            user.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


#add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = forms.PostupdateForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst = models.Post(title=title,desc=desc) 
                messages.success(request,'Post Added Successfully!!')
                pst.save()
                return HttpResponseRedirect('/addpost/')
        else:
            form = forms.PostupdateForm()
        return render (request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


#Update Existing Post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            model_data = models.Post.objects.get(pk=id)
            form = forms.PostupdateForm(request.POST,instance=model_data)
            if form.is_valid():
                # title = form.cleaned_data['title']
                # desc=form.cleaned_data['desc']
                # pst = models.Post(title=title,desc=desc) 
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            model_data = models.Post.objects.get(pk=id)
            form = forms.PostupdateForm(instance=model_data)

        return render (request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
