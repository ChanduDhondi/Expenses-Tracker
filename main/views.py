from django.shortcuts import render, redirect
from .forms import TrackerForm, CustomUserCreation, UserUpdateForm, ProfileUpdateFrom, FilterForm
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from .models import TrackerModel
from django.core.paginator import Paginator
from django.db.models import Sum

@login_required
def home(request):
    chart_I_data = {}
    chart_E_data = {}
    user = request.user
    # total income of current user
    total_income =  TrackerModel.objects.filter(category__exact='I').aggregate(Sum('amount'))
    total_expense =  TrackerModel.objects.filter(category__exact='E').aggregate(Sum('amount'))
    # last 4 transactions qs
    data = TrackerModel.objects.filter(user__exact=user).order_by('-date','-id')[:4]
    # income qs data for chart 
    chart_I_qs = TrackerModel.objects.filter(user=user, category__exact='I').values()
    for i in chart_I_qs:
         chart_I_data[i['date'].strftime('%Y-%m-%d')] = i['amount']

    # expense qs data for chart 
    chart_E_qs = TrackerModel.objects.filter(user=user, category__exact='E').values()
    for i in chart_E_qs:
         chart_E_data[i['date'].strftime('%Y-%m-%d')] = i['amount']

    return render(request, 'main/home.html', {'title':'Home', 'data':data, 'chart_income':chart_I_data, 
                                              'chart_expense':chart_E_data, 'total_income': total_income['amount__sum'],
                                              'total_expense':total_expense['amount__sum']})


class Createview(LoginRequiredMixin, CreateView):
    model = TrackerModel
    fields = ['date', 'category', 'amount', 'description']
    success_url = '/adddata'
    extra_context = {'title':'Add Data'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
@login_required
def viewTransactions(request):
    form = FilterForm(request.POST)
    if request.method == 'POST':
        user = request.user
        sort_by = request.POST.get('sort_by')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date > to_date:
             messages.warning(request, f'From Date({from_date}) must be lessthan To Date({to_date})')
             return redirect('main-transactions')
        elif sort_by == 'last':
             qs =  TrackerModel.objects.filter(user__exact=user, date__gte=from_date, date__lte=to_date).order_by('-date')
             paginator = Paginator(qs, 15) # 25 rows for page
             page_number = request.GET.get('page')
             page_obj = paginator.get_page(page_number)
        else:
             qs =  TrackerModel.objects.filter(user__exact=user, date__gte=from_date, date__lte=to_date).order_by('date')
             paginator = Paginator(qs, 15) # 25 rows for page
             page_number = request.GET.get('page')
             page_obj = paginator.get_page(page_number)
    else:
         form = FilterForm()
         user = request.user
         qs = TrackerModel.objects.filter(user__exact=user).order_by('-date','-id')
         paginator = Paginator(qs, 15) # 25 rows for page
         page_number = request.GET.get('page')
         page_obj = paginator.get_page(page_number)
    return render(request, 'main/view_transactions.html', {'title':'All Transactions', 'form': form, 'data':page_obj})

@login_required
def profile(requset):
    if requset.method == 'POST':
        u_form = UserUpdateForm(requset.POST, instance=requset.user)
        p_form = ProfileUpdateFrom(requset.POST, requset.FILES, instance=requset.user.profile)
        if u_form.is_valid and p_form.is_valid:
                u_form.save()
                p_form.save()
                messages.success(requset, 'User profile successfully updated')
                return redirect('main-profile')
    else:
          u_form = UserUpdateForm(instance=requset.user)
          p_form = ProfileUpdateFrom(instance=requset.user.profile)
    return render(requset, 'main/profile.html', {'title':'Profile', 'u_form':u_form, 'p_form':p_form})

def register(request):  
    if request.method == 'POST':
        form = CustomUserCreation(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}')
            return redirect('main-home')
    else:
        form = CustomUserCreation()
    return render(request, 'main/register.html', {'form':form})

def logout_view(request):
	logout(request)
	return render(request,'main/logout.html')