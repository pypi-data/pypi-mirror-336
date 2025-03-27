from django.contrib.admin.utils import quote
from django.urls import reverse

from wagtail.snippets.action_menu import ActionMenuItem


class NeuralyzeMenuItem(ActionMenuItem):
    name = "anonymize"
    label = "Anonymize"
    icon_name = "no-view"

    def get_url(self, context):
        instance = context["instance"]
        url_name = instance.snippet_viewset.get_url_name("neuralyze")
        return reverse(url_name, args=[quote(instance.pk)])
