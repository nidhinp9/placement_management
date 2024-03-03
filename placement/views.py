from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Profile as profile, Other_Details as other_details, Current_Education_Details, Past_Education_Details
from django.contrib.auth.models import User
from placement.models import Company as company, registered_companies, placed_students, job_profile
from django import forms
import json
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
# Create your views here.


def Home(request):
    return render(request, 'placement/home.html', {
        'posts': ["hello", "world", "test"]
    })


@login_required
def About(request):
    return render(request, 'placement/about.html')


@login_required
def Profile(request):
    current_profile = profile.objects.filter(user=request.user).first()
    current_other_details = other_details.objects.filter(
        profile=current_profile).first()
    current_edu_details = Current_Education_Details.objects.filter(
        profile=current_profile).first()
    past_edu_details = Past_Education_Details.objects.filter(
        profile=current_profile).first()
    return render(request, 'placement/profile.html', {
        'profile': current_profile,
        'other_details': current_other_details,
        'current_edu_details': current_edu_details,
        'past_edu_details': past_edu_details
    })


@login_required
def AllCompanies(request):
    companies_data = company.objects.all()
    companies_list = []
    # get all profiles from job profile for all companies
    for company_detail in companies_data:
        company_detail.job_profile = job_profile.objects.filter(
            company=company_detail).values_list('job_profile', flat=True).all()
    return render(request, 'placement/AllCompanies.html', {'companies': companies_data})


@login_required
def RegisteredCompanies(request):
    registered_companies_data = registered_companies.objects.filter(
        student=request.user)
    companies_data = []
    for registered_company in registered_companies_data:
        registered_company.company.job_profile = registered_company.job_profile
        companies_data.append(registered_company.company)
    # get all profiles from job profile for all companies
    return render(request, 'placement/RegisteredCompanies.html', {'companies': companies_data})


@login_required
def Dashboard(request):
    # if student is placed from placed students
    # isPlaced = False
    # if placed_students.objects.filter(student=request.user).exists():
    #     isPlaced = True

    # return render(request, 'placement/Dashboard.html', {'isPlaced': isPlaced, 'company_name': placed_students.objects.filter(student=request.user).first().company.name})
    return render(request, 'placement/Dashboard.html')


@login_required
def RegisterDeregister(request):
    all_companies = company.objects.all()
    # get profile from each company and add to all_companies
    companiesList = []
    for individualCompany in all_companies:
        profiles = job_profile.objects.filter(
            company=individualCompany).all()
        for profileName in profiles:
            companiesList.append({
                'value': {'id': individualCompany.id,
                          'profile_id': profileName.id},
                'display': f'{individualCompany.name} - {profileName.job_profile}'
            })

    registered_companies_data = registered_companies.objects.filter(
        student=request.user).all()
    registered_companies_list = []
    for registered_company in registered_companies_data:
        registered_companies_list.append({
            'value': {'id': registered_company.company.id,
                      'profile_id': registered_company.job_profile.id},
            'display': f'{registered_company.company.name} - {registered_company.job_profile.job_profile}'
        })
    print(registered_companies_list)
    if request.method == 'POST':
        if 'register' in request.POST:
            selected_value = request.POST.get('register_company')
            json_acceptable_string = selected_value.replace("'", "\"")
            dict = json.loads(json_acceptable_string)
            company_id = dict['id']
            profile_id = dict['profile_id']
            selected_company = company.objects.filter(
                id=company_id).first()
            selected_profile = job_profile.objects.filter(
                id=profile_id).first()
            # check if already registered
            if registered_companies.objects.filter(company=selected_company, student=request.user, job_profile=selected_profile).exists():
                # deregister
                print("deregister")
            else:
                registered_companies.objects.create(
                    company=selected_company, student=request.user, job_profile=selected_profile)
                return redirect('register-deregister')
        else:
            selected_value = request.POST.get('deregister_company')
            json_acceptable_string = selected_value.replace("'", "\"")
            dict = json.loads(json_acceptable_string)
            company_id = dict['id']
            profile_id = dict['profile_id']
            selected_company = company.objects.filter(
                id=company_id).first()
            selected_profile = job_profile.objects.filter(
                id=profile_id).first()
            # check if already registered
            if registered_companies.objects.filter(company=selected_company, student=request.user).exists():
                # deregister
                registered_companies.objects.filter(
                    company=selected_company, student=request.user, job_profile=selected_profile).delete()
                return redirect('register-deregister')
            else:
                print("register")

    return render(request, 'placement/Register-Deregister.html', {'all_companies': companiesList, 'registered_companies': registered_companies_list})


class EditProfile(LoginRequiredMixin, UpdateView):
    model = other_details
    fields = ['address', 'dob', 'father_name', 'mother_name', 'category']
    template_name = 'placement/EditProfile.html'
    success_url = '/profile'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object.address = form.cleaned_data['address']
            self.object.dob = form.cleaned_data['dob']
            self.object.father_name = form.cleaned_data['father_name']
            self.object.mother_name = form.cleaned_data['mother_name']
            self.object.category = form.cleaned_data['category']
            print(self.object)
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_object(self, queryset=None):
        obj = other_details.objects.filter(
            profile=self.request.user.profile).first()
        return obj


# give access to super user only
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AddCompany(LoginRequiredMixin, CreateView):
    model = company
    template_name = 'placement/CompanyForm.html'
    success_url = '/job-profile'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AddJobProfile(LoginRequiredMixin, CreateView):
    model = job_profile
    template_name = 'placement/JobProfile.html'
    success_url = '/allcompanies'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            if 'add-another' in request.POST:
                self.success_url = '/job-profile'
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CreateUser(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'placement/CreateUser.html'
    success_url = '/create-profile'
    fields = ['username', 'password']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            if 'add-another' in request.POST:
                self.success_url = '/job-profile'
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Create User'
        context['postUrl'] = 'create-user'
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CreateProfile(LoginRequiredMixin, CreateView):
    model = profile
    template_name = 'placement/CreateUser.html'
    success_url = '/add-other-details'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Create Profile'
        context['postUrl'] = 'create-profile'
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AddOtherDetails(LoginRequiredMixin, CreateView):
    model = other_details
    template_name = 'placement/CreateUser.html'
    success_url = '/add-current-education-details'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Add Other Details'
        context['postUrl'] = 'add-other-details'
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AddCurrentEducationDetails(LoginRequiredMixin, CreateView):
    model = Current_Education_Details
    template_name = 'placement/CreateUser.html'
    success_url = '/add-past-education-details'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Add Current Education Details'
        context['postUrl'] = 'add-current-education-details'
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AddPastEducationDetails(LoginRequiredMixin, CreateView):
    model = Past_Education_Details
    template_name = 'placement/CreateUser.html'
    success_url = '/'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Add Past Education Details'
        context['postUrl'] = 'add-past-education-details'
        return context
