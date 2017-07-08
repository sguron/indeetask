from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django import forms
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate


class LoginView(TemplateView):
    template_name = "accounts/login/login.html"
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse('tasks-app')

    def get(self, request, *args, **kwargs):
        self.context = self.get_context_data()
        form = self.form_class()
        self.context['form'] = form

        return self.render_to_response(self.context)

    def post(self, request, *args, **kwargs):
        self.context = self.get_context_data()
        form = self.form_class( data=request.POST)
        self.context['form'] = form
        if form.is_valid():
            login(self.request, form.user_cache)
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)
        else:
            return self.render_to_response(self.context)


class SignupView(TemplateView):
    template_name = "accounts/login/signup.html"
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('tasks-app')

    def get(self, request, *args, **kwargs):
        self.context = self.get_context_data()
        form = self.form_class()
        self.context['form'] = form

        return self.render_to_response(self.context)

    def post(self, request, *args, **kwargs):
        self.context = self.get_context_data()
        form = self.form_class( data=request.POST)
        self.context['form'] = form
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # create new user
            form.save()

            #Login the new user
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password1'])
            login(self.request, user)

            #redirect to app
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)
        else:
            return self.render_to_response(self.context)