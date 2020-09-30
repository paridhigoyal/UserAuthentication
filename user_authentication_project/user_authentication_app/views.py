from django.conf import settings
from django.contrib.auth import (authenticate, login,
                                 logout, update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, render
from django.views import generic
from django.views.generic.base import TemplateView
from .forms import CustomSignupForm, UpdateUserProfileForm


class HomePage(TemplateView):

    template_name = 'index.html'


class LoginView(generic.View):
    form_class = AuthenticationForm
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request=request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        return render(request, "index.html")


class LogoutView(generic.RedirectView):

    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ChangeUserPasswordView(LoginRequiredMixin, generic.FormView):
    form_class = PasswordChangeForm
    template_name = 'account/change_password.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial, user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class SignUpView(generic.CreateView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('login')

        return render(request, self.template_name, {'form': form})


class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateUserProfileForm
    template_name = 'account/profile_update.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial, instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})
