from django.shortcuts import render, HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request): 
    return render(request,'home/home.html')
def contact(request):

    if  request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(desc)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
            
        
    return render(request,'home/contact.html')

def about(request): 
    return render(request,'home/about.html')

def search(request):
    query = request.GET['search']

    if len(query)>70:
        allpost=Post.objects.none()

    else:

        allpostblog = Post.objects.filter(title__icontains=query)
        allpostconent = Post.objects.filter(content__icontains=query)
        allpost = allpostblog.union(allpostconent)

    params = {'allpost' : allpost,'query':query}
    if allpost.count()==0:
            messages.error(request,"no search results found for your search")
    return render(request,'home/search.html',params)



def handlesignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        #-----------------------
        if len(username) >10:
            messages.error(request, "username must be less than 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "username must contain only numbers and alphabets")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request,"your password didn't matched")

        #creating the user
        myuser = User.objects.create_user(username=username,email=email,password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"your icoder account has been successfuly created")
        return redirect('home')

    else:
        return HttpResponse("404 not found")

def handlelogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']

        user = authenticate(username = loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"succesfully logedin")
            return redirect('home')

        else:
            messages.error(request,"invalid username or password,try again")
            return redirect('home')

    return HttpResponse('handlelogin')


def handlelogout(request):
    
    logout(request)
    messages.success(request,"succesfully loged out")

    return redirect('home')
    return HttpResponse('handlelogout')