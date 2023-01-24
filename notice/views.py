from django.shortcuts import render,redirect
from .forms import NoticeWriteForm
from .models import Notice
from user.models import User
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required


# Create your views here.

def notice_list(request):
    notice= Notice.objects.all().order_by('id')
    length = len(notice)
    return render(request, 'notice_list.html', {"notice":notice,'length':length})

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    
    context = {
        'notice': notice,
    }
    response = render(request,'notice_detail.html',context)
    expire_date, now = datetime.now(),datetime.now()
    expire_date+=timedelta(days = 1)
    expire_date = expire_date.replace (hour=0,minute=0,second=0,microsecond=0)
    expire_date -= now
    max_page = expire_date.total_seconds()
    
    cookie_value = request.COOKIES.get('hitboard','_')
    
    if f'_{pk}_' not in cookie_value:
        cookie_value +=f'{pk}_'
        response.set_cookie('hitboard',value = cookie_value,max_age = max_page,httponly=True)
        notice.hits +=1
        notice.save()
    return render(request, 'notice_detail.html', context)


@login_required(login_url='/user/login/')
def notice_write(request):
    login_session = request.session.get('login_id','')
    
    context = {'login_session':login_session}
    
    if request.method == "GET":
        form = NoticeWriteForm()
        context['forms'] = form
        return render(request,'notice_write.html',context)

    elif request.method == "POST":
        form = NoticeWriteForm(request.POST)
        
        if form.is_valid():
            writer = User.objects.get(username = login_session)
            
            notice = Notice(
                title=form.title,
                contents = form.contents,
                writer = writer,
                category = '서비스안내'
            )
            notice.save()
            return redirect('/notice/list')
        
        else:
            context['forms'] = form
            if form.errors:
                for value in  form.values():
                    context['error']=value
            return render(request,'notice_write.html',context)
        

@login_required(login_url='/user/login/')
def notice_modify(request,pk):
    login_session = request.session.get('login_id','')
    context = {'login_session':login_session}
    
    notice = get_object_or_404(Notice, pk= pk)
    context['notice'] = notice
    
    if notice.writer.username != login_session:
        
        return redirect(f'/notice/{pk}/')
    if request.method == "GET":
        form = NoticeWriteForm(instance = notice)
        context['forms'] = form
        return render(request,'notice_modify.html',context)

    elif request.method == "POST":
        form = NoticeWriteForm(request.POST)
        
        if form.is_valid():
            
            notice.title=form.title
            notice.contents = form.contents  
            notice.save()
            return redirect('/notice/list')
        
        else:
            context['forms'] = form
            if form.errors:
                for value in form.values():
                    context['error']=value
            return render(request,'notice_modify.html',context)

@login_required(login_url='/user/login/')
def notice_delete(request,pk):
    login_session = request.session.get('login_id','')
    notice = get_object_or_404(Notice,pk=pk)
    if notice.writer.username ==login_session:
        notice.delete()
        return redirect('/notice/list')
    else:
        return redirect(f'/notice/{pk}')
