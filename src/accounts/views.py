from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView,DetailView, View
from django.utils.safestring import mark_safe
from django.contrib import messages
from .forms import LoginForm, RegisterForm,GuestForm
from.models import GuestEmail, EmailActivation
from .signals import user_logged_in
from django.urls import reverse
from django import forms
from phone_field import PhoneField
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy


User = get_user_model()
def AccountHomeView(request):
    if request.method =='POST': 
        username=request.POST.get('username')
        contact=request.POST.get('contact')
        dob=request.POST.get('dob')
        print("dob:",dob,username)
        email=request.POST.get('email')
        password1=request.POST['password1']
        password2=request.POST['password2']
        if not email:
            messages.error(request,'email cannot be empty')
        elif not password1 or not password2:
            messages.error(request,'password cannot be empty')
        elif password1 != password2:
            messages.error(request,'password doesnt match')
        else:
            user = request.user
            print(user)
            user.full_name=username
            user.contact= contact
            user.dob= dob
            user.email= email               
            user.set_password(password1)
            # user.password1= password1
            # user.password2= password2
            user.save()
            messages.success(request,'Your profile is successfully updated')
        return redirect("account:home")

    return render(request, 'accounts/home.html', {})

class AccountEmailActivateView(View):
    def get(self, request, key, *args, **kwargs):
        qs = EmailActivation.objects.filter(key__iexact=key)
        confirm_qs = qs.confirmable()
        if confirm_qs.count() == 1:
            obj = confirm_qs.first()
            obj.activate()
            messages.success(request, "Your email has been confirmed. Please login.")
            return redirect("login")
        else:
            activated_qs = qs.filter(activated=True)
            if activated_qs.exists():
                reset_link = reverse("password_reset")
                msg = """Your email has already been confirmed
                Do you need to <a href="{link}">reset your password</a>?
                """.format(link=reset_link)
                messages.success(request, mark_safe(msg))
                return redirect("login") 
        return render(request, 'registeration/activation-error.html', {})

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        pass

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
            email       = form.cleaned_data.get("email")
            new_guest_email = GuestEmail.objects.create(email=email)
            request.session['guest_email_id'] = new_guest_email.id
        # messages.success(request,"User added")
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/register/")
    return redirect("/register/")

# class PasswordResetView(auth_views.PasswordResetView):
#     form_class = forms.PasswordResetForm
#     template_name = 'accounts/registeration/password-reset.html'
#     success_url = reverse_lazy('accounts:password-reset-done')
#     subject_template_name = 'accounts/registeration/password-reset-email.txt'
#     email_template_name = 'accounts/registeration/password-reset-email.html'

# class LoginView(FormView):
#     form_class = LoginForm
#     success_url = '/'
#     template_name = 'accounts/login.html'

#     def form_valid(self, form):
#         request = self.request
#         next_ = request.GET.get('next')
#         next_post = request.POST.get('next')
#         redirect_path = next_ or next_post or None
#         email  = form.cleaned_data.get("email")
#         password  = form.cleaned_data.get("password")
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         return super(LoginView, self).form_invalid(form)


# class RegisterView(CreateView):
#     form_class = RegisterForm
#     print(form_class)
#     template_name = 'accounts/register.html'
#     success_url = '/applogin/'
#     def RegisterView(request):
#         if request.method =='POST':
#             # email = request.POST['email']
#             password1 = request.POST['password1']
#             password2 = request.POST['password2']
#             print(password1)


def login_page(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            if not username:
                messages.error(request,'username is empty. Please enter a valid Username or Kiss Me ')
            elif not password:
                messages.error(request,'password is empty. Please enter a valid Password')
            else:
                messages.error(request,'username or password not correct')
            return redirect('login')
    return render(request, "accounts/index.html", {})

User = get_user_model()
def RegisterView(request):
    if request.method =="POST":
        full_name=request.POST['full_name']
        contact=request.POST['contact']
        dob=request.POST['dob']
        print("dob:",dob)
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        qs = User.objects.filter(email=email)
        if qs.count() == 1:
            messages.error(request,'User is already registered')
        elif not email:
            messages.error(request,'email cannot be empty')
        elif not password1 or not password2:
            messages.error(request,'password cannot be empty')
        elif password1 != password2:
            messages.error(request,'password doesnt match')
        else:
            user = User.objects.create(email=email,full_name=full_name,dob=dob,contact=contact,is_active=False,staff=False,admin=False)
            user.set_password(password1)
            user.save()
            print(user)
            # print("User:", user)
            messages.success(request,'A link has been sent to your email.Follow the link to activate your account')
            return redirect('login')
        
        # return redirect('login')
    return render(request, "accounts/register.html")


    
# User = get_user_model()
# def RegisterView(request):
#     form = RegisterForm(request.POST or None)
#     if request.method =="POST":
#         full_name=form['full_name'].value()
#         email=form['email'].value()
#         password1=form['password1'].value()
#         password2=form['password2'].value()
#         qs = User.objects.filter(email=email)
#         if qs.count() == 1:
#             messages.error(request,'User is already registered')
#         elif form.is_valid():
#             form.save()
#             # print("User:", user)
#             messages.error(request,'A link has been sent to your email.Follow the link to activate your account')
#             return redirect('login')
#         elif not email:
#             messages.error(request,'email cannot be empty')
#         elif not password1 or not password2:
#             messages.error(request,'password cannot be empty')
#         elif password1 != password2:
#             messages.error(request,'password doesnt match')
#         # return redirect('login')
#     return render(request, "accounts/register.html")