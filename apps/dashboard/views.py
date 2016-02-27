import json

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render

from .serializers import *
from apps.companies.api.serializers import CompanySerializer


class LoginRequiredMixin(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class SetSessionData(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Sets the data to set the company information inside the session
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.request.user
        if user and user.memberships.count() > 0:
            membership = user.memberships.get(is_default=True)
            if company.is_active:
                request.session['company'] = membership.company.id
            else:
                return redirect('/users/suspended/')

            if membership.is_owner or membership.is_superuser:
                request.session['superuser'] = True
            else:
                request.session['superuser'] = False

            return super(SetSessionData, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('/users/create-company/')


class DashboardView(SetSessionData):

    def get_template_names(self):
        from django.conf import settings

        if settings.DEBUG:
            template = '__dashboard.html'
        else:
            template = '__dashboard.html'
        return [template]

    def get_context_data(self, **kwargs):
        """
        sets the context data and global defaults for angular
        """
        from django.conf import settings
        request = self.request
        membership = request.user.memberships.prefetch_related(
            'company__coupons').select_related(
            'company').get(is_default=True)
        user = DashboardUserSerializer(request.user).data
        company = CompanySerializer(
                membership.company
            ).data
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['globals'] = {
            'user': user,
            'company': company,
            'coupons': {
                    'total': membership.company.coupons.all().count(),
                    'claimed': membership.company.coupons.claimed().count(),
                    'remaining': membership.company.coupons.remaining().count(),
                },
            'budget': membership.company.campaigns.active().active_budget(),
            'cxt': {
                'staticUrl': settings.STATIC_URL,
                'mediaUrl': settings.MEDIA_URL,
            }
        }
        return context


class AngularPartials(LoginRequiredMixin):

    def get_template_names(self):
        from django.conf import settings

        if settings.DEBUG:
            base = 'debug/partials/'
        else:
            base = 'debug/partials/'

        template_name = base + self.kwargs['template_name']
        return [template_name]


def redirect_to_dashboard(request):
    return redirect('dashboard', permanent=True)


def user_opt_out(request):
    """
    This doesn't belong here!!
    This view is called when the user clicks on the 'Opt-Out' button.
    It fetches the ImpressionUser object for the current customer and
    sets the opt_out_flag to true.
    """
    if (request.method == POST) and ("optOutButton" in request.POST) and request.visitor:
        impression_user = ImpressionUser.objects.get(key=request.visitor)
        impression_user.set_opt_out_flag()
    return render(request, 'debug/opt-out-child.html', {})


def display_coupon(request, code):
    from apps.campaigns.models import Coupon
    try:
        coupon = Coupon.objects.get(code=code)
        #coupon = coupon.redeem()
    except Coupon.DoesNotExist:
        coupon = False
    return render(request, 'coupons/redeem.html', { 'coupon': coupon })

def redeem_coupon(request, code):
    from apps.campaigns.models import Coupon
    try:
        coupon = Coupon.objects.get(code=code)
        coupon.redeem()
    except Coupon.DoesNotExist:
        coupon = False
    print coupon
    return render(request, 'coupons/redeem.html', { 'coupon': coupon, 'redeemed': True })
