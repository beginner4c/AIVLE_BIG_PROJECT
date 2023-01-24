from django.shortcuts import render,redirect
from .forms import ReviewWriteForm
from .models import Review
from user.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from ai.models import Place

#Create your views here.

def review_list(request):
    review= Review.objects.all().order_by('id')
    length = len(review)
    return render(request, 'review_list.html', {"review":review,"length":length})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    context = {
        'review': review,
    }
    response = render(request,'review_detail.html',context)
    expire_date, now = datetime.now(),datetime.now()
    expire_date+=timedelta(days = 1)
    expire_date = expire_date.replace (hour=0,minute=0,second=0,microsecond=0)
    expire_date -= now
    max_page = expire_date.total_seconds()
    
    cookie_value = request.COOKIES.get('hitboard','_')
    
    if f'_{pk}_' not in cookie_value:
        cookie_value +=f'{pk}_'
        response.set_cookie('hitboard',value = cookie_value,max_age = max_page,httponly=True)
        review.hits +=1
        review.save()
    return render(request, 'review_detail.html', context)


@login_required(login_url='/user/login/')
def review_write(request):
    login_session = request.session.get('login_id','')
    place = request.GET.get("place_info",None)
    context = {'login_session':login_session,"place":place}
    
    if request.method == "GET":
        form = ReviewWriteForm()
        context['forms'] = form
        return render(request,'review_write.html',context)

    elif request.method == "POST":
        form = ReviewWriteForm(request.POST)
        
        if form.is_valid():
            writer = User.objects.get(username = login_session)
            myplace = Place.objects.get(place_name = place)
            review = Review(
                title=form.title,
                contents = form.contents,
                writer = writer,
                place = myplace,
            )
            review.save()
            return redirect('/review/list')
        
        else:
            context['forms'] = form
            if form.errors:
                for value in  form.values():
                    context['error']=value
            return render(request,'review_write.html',context)
        

@login_required(login_url='/user/login/')
def review_modify(request,pk):
    login_session = request.session.get('login_id','')
    context = {'login_session':login_session}
    
    review = get_object_or_404(Review, pk= pk)
    context['review'] = review
    
    if review.writer.username != login_session:
        
        return redirect(f'/review/{pk}/')
    if request.method == "GET":
        form = ReviewWriteForm(instance = review)
        context['forms'] = form
        return render(request,'review_modify.html',context)

    elif request.method == "POST":
        form = ReviewWriteForm(request.POST)
        
        if form.is_valid():
            
            review.title=form.title
            review.contents = form.contents          
            
            review.save()
            return redirect('/review/list')
        
        else:
            context['forms'] = form
            if form.errors:
                for value in  form.values():
                    context['error']=value
            return render(request,'review_modify.html',context)

@login_required(login_url='/user/login/')
def review_delete(request,pk):
    login_session = request.session.get('login_id','')
    review = get_object_or_404(Review,pk=pk)
    if review.writer.username ==login_session:
        review.delete()
        return redirect('/review/list')
    else:
        return redirect(f'/review/{pk}')
    