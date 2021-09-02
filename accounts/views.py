from django.shortcuts import redirect, render
from django.contrib.auth import login ,logout,authenticate 
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib import auth, messages 
from django.views.generic import ListView, DetailView, CreateView ,TemplateView ,UpdateView  ,DeleteView
from django.views import View
from django.utils.decorators import method_decorator 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# my uplod my files 
from .forms import *
from .models import *



# -----------------START SIGNUP & LOGIN PART ---------------------

class HomePage(TemplateView):
    template_name='accounts/Home.html'
   

# SIGNUP  
class Register(View): 

    def get(self,request):
        sform = RegisterForm()
        return render(request,'accounts/reglogin.html',{'sform':sform})
    
    def post(self,request):
        sform = RegisterForm(request.POST)
        if sform.is_valid(): 
            sform.save()
            username = sform.cleaned_data.get('phone')
            raw_password = sform.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  
        else:
            return redirect('signup')


# LOGIN  
class LoginPage(View): 
    def get(self,request): 
        lform =LoginForm() 
        if request.user.is_authenticated:
            return redirect('home') 
        
        return render(request,'accounts/login.html',{'lform':lform}) 
    
    def post(self,request):
        lform =LoginForm(data=request.POST) 
        if lform.is_valid():
            ph=lform.cleaned_data['phone'] 
            paw=lform.cleaned_data['password'] 
            
            try:
               user=authenticate(username=CustomUser.objects.get(email__iexact=ph),password=paw )
            
            except:
              user=authenticate(username=ph,password=paw) 

            if user is not None:
                login(request,user)
                return redirect('home')
            

# LOGOUT VIEWS 
def  LogoutPage(request):
    logout(request)
    return HttpResponseRedirect('signup') 


# ------------ -----END SIGNUP & LOGIN PART ---------------------

# PROFILE UPDATE 
# @method_decorator(login_required,name='dispatch') 
class Profile(UpdateView):
    model=Profile
    fields=['fullname','gender','pic','email']
 
    template_name='accounts/Profile.html'  
    success_url='/'


# -------------------------ADDRESS PART -------------------------------------------


# SHOW ADDRESS
# @method_decorator(login_required,name='dispatch')
class ShowAddress(ListView):
    template_name='accounts/AddressShow.html' 
    context_object_name='rat'
    model=Address 
    ordering=['fullname']
    

    def get_queryset(self):
        return Address.objects.filter(uplod=self.request.user)



# ADD ADDRESS
# @method_decorator(login_required,name='dispatch')
class AddAddress(CreateView):
    model= Address 
    form_class= AddressForm 
    template_name='accounts/Address.html'
  
    def form_valid(self, form): 
       
        self.object= form.save()
        self.object.uplod=self.request.user
        self.object.save()
        print('-------------par-------')
        par =self.request.user.id 
        print(par)
        return redirect('profile' ,par) 

# UPDATE ADDRESS 
# @method_decorator(login_required,name='dispatch') 
class UpAddress(UpdateView): 
    
    model=Address 
    form_class=AddressForm 
    template_name='accounts/Address.html'
    success_url='acc/home/' 

# Delete ADDRESS 
login_required()
def DelAddress(request,pk):
    par= request.user
    print('user',par)
    obj=Address.objects.get(id=pk) 
    obj.delete()  
   
    return redirect ('showaddress',par)