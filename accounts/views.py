from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordChangeView as AuthPasswordChangeView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import SignupForm, ProfileForm, PasswordChangeForm
from .models import User

login = LoginView.as_view(template_name="accounts/login_form.html")


def logout(request):
    messages.success(request, "로그아웃되었습니다.")
    return logout_then_login(request)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입을 환영합니다.")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, "accounts/signup_form.html", {
        "form": form,
    })


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 수정/저장했습니다.")
            return redirect("profile_edit")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html", {
        "form": form,
    })


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy("password_change")
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, "암호를 변경했습니다.")
        return super().form_valid(form)


password_change = PasswordChangeView.as_view()


@login_required
def user_follow(request, username):

    login_user = request.user
    page_user = get_object_or_404(User, username=username, is_active=True)

    login_user.following_set.add(page_user)
    # TODO: 왜 이렇게 해야만 정상적으로 동작하는건지 이해가 안된다. 내가 모델 구조를 잘 못 이해하고 있나?
    page_user.following_set.add(login_user)

    messages.success(request, f"{page_user}님을 팔로우했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def user_unfollow(request, username):

    login_user = request.user
    page_user = get_object_or_404(User, username=username, is_active=True)

    login_user.following_set.remove(page_user)
    page_user.following_set.remove(login_user)

    messages.success(request, f"{page_user}님을 언팔로우했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)
