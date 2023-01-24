from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,reverse
# from .models import User
from .models import User
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms,models
from django.contrib.auth.hashers import check_password
from review.models import Review
def main(request):
    return render(request,'main.html')
def my_login(request):
    if request.method == "GET":
        id = request.GET.get("username", None)
        password = request.GET.get("password", None)

        res = {}

        if not id:
            res['error'] = '아이디를 입력해주세요.'
        elif not password:
            res['error'] = '비밀번호를 입력해주세요.'
        else:
            try:
                user = User.objects.get(username=id)
                email_verified = user.email_verified
                if email_verified ==0:
                    res['error'] = '발송된 이메일로 계정을 인증해주세요'
                else:
                    if check_password(password, user.password):
                        authenticated_user = authenticate(request, username=id, password=password)
                    if authenticated_user is not None:
                        request.session['login_id'] = id
                        login(request, user)
                        return redirect('/')
                    else:
                        res['error'] = '비밀번호가 틀렸습니다.'
            except:
                res['error'] = '이메일이 존재하지 않습니다.'
        return render(request, "login.html", res)

    elif request.method == "POST":
        id = request.POST.get("username", None)
        password = request.POST.get("password", None)

        res = {}

        if not id:
            res['error'] = '아이디를 입력해주세요.'
        elif not password:
            res['error'] = '비밀번호를 입력해주세요.'
        else:
            try:
                user = User.objects.get(username=id)
                email_verified = user.email_verified
                if email_verified ==0:
                    res['error'] = '발송된 이메일로 계정을 인증해주세요'
                else:
                    if check_password(password, user.password):
                        authenticated_user = authenticate(request, username=id, password=password)
                    if authenticated_user is not None:
                        request.session['login_id'] = id
                        login(request, user)
                        return redirect('/')
                    else:
                        res['error'] = '비밀번호가 틀렸습니다.'
            except:
                res['error'] = '이메일이 존재하지 않습니다.'
        return render(request, "login.html", res)
    
def log_out(request):
    logout(request) 
    return redirect('/')

class SignUpView(FormView):
    template_name = "signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("user:traivler")
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        user.verify_email() 
        return super().form_valid(form)
def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key) 
        user.is_active = True
        user.email_verified = True 
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        
        pass
    return redirect(reverse("user:traivler"))


def mypage(request):
    login_session = request.session.get('login_id','')
    text = Review.objects.filter(writer = login_session)
    
    context = {'reviews':text}
    return render(request, "mypage.html",context)

def traivler(request):
    return render(request,"traivler.html")