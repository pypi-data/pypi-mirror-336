import logging

from django.contrib.admin.utils import quote
from django.contrib.admin.utils import unquote
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import path
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.generic import TemplateView

from wagtail.admin import messages
from wagtail.admin.views.generic import HookResponseMixin
from wagtail.admin.views.generic import WagtailAdminTemplateMixin
from wagtail.admin.views.generic.base import WagtailAdminTemplateMixin
from wagtail.admin.views.generic.mixins import HookResponseMixin
from wagtail.models import ReferenceIndex

from .action import NeuralyzeAction

logger = logging.getLogger("wagtail_neuralyzer")


class NeuralyzeView(
    HookResponseMixin,
    WagtailAdminTemplateMixin,
    TemplateView,
):
    """
    Copied and adapted from UnpublishedView
    """

    model = None
    index_url_name = None
    edit_url_name = None
    neuralyze_url_name = None
    usage_url_name = None
    success_message = gettext_lazy("'%(object)s' neuralyzed.")
    template_name = "wagtailadmin/generic/confirm_neuralyze.html"
    neuralyzer_class = None

    def setup(self, request, pk, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pk = pk
        self.object = self.get_object()

    def dispatch(self, request, *args, **kwargs):
        self.objects_to_neuralyze = self.get_objects_to_neuralyze()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not self.model:
            raise Http404
        return get_object_or_404(self.model, pk=unquote(str(self.pk)))

    def get_usage(self):
        return ReferenceIndex.get_grouped_references_to(self.object)

    def get_objects_to_neuralyze(self):
        # Hook to allow child classes to have more objects to neuralyze (e.g. page descendants)
        return [self.object]

    def get_object_display_title(self):
        return str(self.object)

    def get_success_message(self):
        if self.success_message is None:
            return None
        return self.success_message % {"object": str(self.object)}

    def get_success_buttons(self):
        if self.edit_url_name:
            return [
                messages.button(
                    reverse(self.edit_url_name, args=(quote(self.object.pk),)),
                    _("Edit"),
                )
            ]

    def get_next_url(self):
        if not self.index_url_name:
            raise ImproperlyConfigured(
                "Subclasses of wagtail.admin.views.generic.models.neuralyzeView "
                "must provide an index_url_name attribute or a get_next_url method"
            )
        return reverse(self.index_url_name)

    def get_neuralyze_url(self):
        if not self.neuralyze_url_name:
            raise ImproperlyConfigured(
                "Subclasses of wagtail.admin.views.generic.models.neuralyzeView "
                "must provide an neuralyze_url_name attribute or a get_neuralyze_url method"
            )
        return reverse(self.neuralyze_url_name, args=(quote(self.object.pk),))

    def get_neuralyzer(self):
        if not self.neuralyzer_class:
            raise ImproperlyConfigured(
                "Subclasses of NeuralyzeView "
                "must provide an neuralyzer_class attribute or a get_neuralyzer method"
            )
        return self.neuralyzer_class()

    def get_usage_url(self):
        # Usage URL is optional, allow it to be unset
        if self.usage_url_name:
            return reverse(self.usage_url_name, args=(quote(self.object.pk),))

    def neuralyze(self):
        hook_response = self.run_hook("before_neuralyze", self.request, self.object)
        if hook_response is not None:
            return hook_response

        for object in self.objects_to_neuralyze:
            action = NeuralyzeAction(
                object,
                neuralyzer=self.get_neuralyzer(),
                user=self.request.user,
            )
            action.execute(skip_permission_checks=True)

        hook_response = self.run_hook("after_neuralyze", self.request, self.object)
        if hook_response is not None:
            return hook_response

    def post(self, request, *args, **kwargs):
        hook_response = self.neuralyze()
        if hook_response:
            return hook_response

        success_message = self.get_success_message()
        success_buttons = self.get_success_buttons()
        if success_message is not None:
            messages.success(request, success_message, buttons=success_buttons)

        return redirect(self.get_next_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_opts"] = self.object._meta
        context["object"] = self.object
        context["object_display_title"] = self.get_object_display_title()
        context["neuralyze_url"] = self.get_neuralyze_url()
        context["next_url"] = self.get_next_url()
        context["usage_url"] = self.get_usage_url()
        if context["usage_url"]:
            usage = self.get_usage()
            context["usage_count"] = usage.count()
        return context


class NeuralyzeSnippetViewSetMixin:
    neuralyze_view_class = NeuralyzeView

    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()
        urlpatterns += [path("neuralyze/<str:pk>/", self.neuralyze_view, name="neuralyze")]
        return urlpatterns

    @property
    def neuralyze_view(self):
        view = self.construct_view(
            self.neuralyze_view_class,
            template_name=self.get_templates(
                "neuralyze", fallback=self.neuralyze_view_class.template_name
            ),
        )
        return view

    def get_common_view_kwargs(self, **kwargs):
        return super().get_common_view_kwargs(
            **{"neuralyze_url_name": self.get_url_name("neuralyze")}, **kwargs
        )
