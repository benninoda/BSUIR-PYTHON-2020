from pyexpat.errors import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, RedirectView, UpdateView, TemplateView, DeleteView

from .utils import send_email_to_user
from .models import CheckInForm, RentForm, RulesEntry, User, UserForm, WorkEntry, WorkEntryCreateForm, \
    MessageToDormitoryForm, MessageToDormitory
from .forms import create_groups, UserCreationPersonnelForm, UserCreationLodgerForm, MyUserChangeForm, \
    UserLodgerOrPersonnelChangeForm
import logging

logger = logging.getLogger('dormitoryApp.views.activate')


class HomeView(View):
    template = 'home.html'

    def get(self, request):
        if Group.objects.all().count() < 2:
            create_groups()
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('profile_page',
                                                kwargs={'pk': request.user.id, 'name': request.user.username}))
        return render(request, self.template)


class SignUpLodgerView(CreateView):
    form_class = UserCreationLodgerForm
    success_url = 'login'
    template_name = 'register_lodger.html'

    def form_valid(self, form):
        self.object = form.save()
        group = Group.objects.get(name='Lodger')
        self.object.groups.add(group)
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


class SignInView(LoginView):
    template_name = 'login.html'
    success_url = 'mdamdamda'

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


@login_required
def loginRequiredView(request):
    # if request.user.groups.filter(name='Lodger').exists():
    #     return HttpResponseRedirect(reverse('profile_lodger_page',
    #                                     kwargs={'pk': request.user.id, 'name': request.user.username}))

    return HttpResponseRedirect(reverse('profile_page',
                                        kwargs={'pk': request.user.id, 'name': request.user.username}))


class SignUpPersonnelView(CreateView):
    form_class = UserCreationPersonnelForm
    success_url = 'login'
    template_name = 'register_staff.html'

    def form_valid(self, form):
        self.object = form.save()
        group = Group.objects.get(name='Personnel')
        self.object.groups.add(group)
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


class SignUpView(View):
    template = 'register.html'

    def get(self, request):
        return render(request, self.template)


class CheckInView(CreateView):
    form_class = CheckInForm
    success_url = 'home_page'
    template_name = 'check_in.html'

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


class RentView(CreateView):
    form_class = RentForm
    success_url = 'home_page'
    template_name = 'rent_page.html'

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


class RulesView(ListView):
    model = RulesEntry
    template_name = 'rules_page.html'


class ProfileDetailView(UpdateView):
    model = User
    form_class = UserLodgerOrPersonnelChangeForm
    template_name = 'account_staff.html'
    success_url = 'mdamdamda'

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


class ProfileLodgerView(UpdateView):
    model = User
    form_class = UserLodgerOrPersonnelChangeForm
    template_name = 'account_staff.html'
    success_url = 'mdamdamda'

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


class LodgersView(ListView):
    model = User
    template_name = 'lodgers_page.html'


class ContactsView(ListView):
    model = User
    template_name = 'contacts_page.html'


class MessageToDormitoryView(CreateView):
    model = MessageToDormitory
    template_name = 'message_to_dormitory.html'
    form_class = MessageToDormitoryForm
    success_url = 'contacts_page'

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


@login_required
def login_required_works_view(request):
    logger = logging.getLogger('django')
    if request.user.groups.filter(name='Lodger').exists():
        logger.info('you are in lodger redirect')
        return HttpResponseRedirect(reverse('works_page_hi',
                                        kwargs={'pk': request.user.id, 'name': request.user.username}))
    logger.info('you are in personnel redirect')
    return HttpResponseRedirect(reverse('works_page_hi',
                                        kwargs={'pk': request.user.id, 'name': request.user.username}))


class WorkPersonnelView(CreateView, ListView):
    model = WorkEntry
    template_name = 'work_personnel_page.html'
    form_class = WorkEntryCreateForm
    success_url = 'redirect_works_page'
    ordering = ['-name']

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url)


class WorkPersonnelUpdateView(UpdateView):
    model = WorkEntry
    template_name = 'work_personnel_update_page.html'
    form_class = WorkEntryCreateForm
    success_url = 'redirect_works_page'

    def get_object(self, queryset=None):
        self.object = get_object_or_404(WorkEntry, pk=self.kwargs['num'])
        obj = self.object
        print(self.object.name)
        return obj

    def get_success_url(self, *args, **kwargs):
        print('alooo')
        return reverse(self.success_url)


class WorkEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkEntry
    template_name = 'work_personnel_page.html'
    success_url = 'redirect_works_page'
    success_msg = 'Запись удалена'

    def get_success_url(self, *args, **kwargs):
        print('alooo')
        return reverse(self.success_url)


class ActivateUserView(TemplateView):
    logger = logging.getLogger('django')
    template_name = 'verificated_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        uid = self.kwargs['uid']
        token = self.kwargs['token']
        logger.debug(context)
        try:
            id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            logger.error('One of error excepted: TypeError, ValueError, OverflowError, User.DoesNotExist')

        if user is not None and default_token_generator.check_token(user, token):
            user.verified = True
            user.save()
            context['is_success'] = True
            logger.info('verified successfully for {}'.format(user.username))
        else:
            context['is_success'] = False
            logger.warning('verified not successfully')

        return context


@login_required
def login_required_verification_send(request):
    send_email_to_user(request, request.user)
    return HttpResponseRedirect(reverse('profile_page',
                                        kwargs={'pk': request.user.id, 'name': request.user.username}))


class EggView(TemplateView):
    template_name = 'egg_page.html'

# Create your views here.
