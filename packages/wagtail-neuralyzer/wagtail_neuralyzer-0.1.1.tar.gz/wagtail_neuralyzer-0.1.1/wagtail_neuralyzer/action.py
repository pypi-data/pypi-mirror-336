import logging

from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from wagtail.log_actions import log
from wagtail.snippets.bulk_actions.snippet_bulk_action import SnippetBulkAction

logger = logging.getLogger("wagtail_neuralyzer")


class NeuralyzePermissionError(PermissionDenied):
    """
    Raised when the object unpublish cannot be performed due to insufficient permissions.
    """

    pass


class NeuralyzeAction:
    def __init__(self, object, commit=True, user=None, log_action=True, neuralyzer=None):
        self.object = object
        self.commit = commit
        self.user = user
        self.log_action = log_action
        self.neuralyzer = neuralyzer

    def check(self, skip_permission_checks=False):
        if (
            self.user
            and not skip_permission_checks
            and not self.object.permissions_for_user(self.user).can_neuralyze()
        ):
            raise NeuralyzePermissionError("You do not have permission to neuralyze this object")

    def _commit_neuralyze(self, object):
        object.save()

    def _after_neuralyze(self, object):
        pass
        # utilisé pour lancer un signal
        # neuralyzed.send(sender=type(object), instance=object)

    def _neuralyze_object(self, object, commit, user, log_action):
        """
        Neuralyze the object using Neuralyzer

        :param log_action: flag for logging the action. Pass False to skip logging. Can be passed an action string.
            Defaults to 'wagtail.neuralyze'
        """
        self.neuralyzer.run(filters={"pk": object.pk})

        if commit:
            self._commit_neuralyze(object)

        if log_action:
            log(
                instance=object,
                action=log_action
                if isinstance(log_action, str)
                else "wagtail_neuralyzer.neuralyze",
                user=user,
            )

        logger.info('Neuralyzed: "%s" pk=%s', str(object), str(object.pk))

        self._after_neuralyze(object)

    def execute(self, skip_permission_checks=False):
        self.check(skip_permission_checks=skip_permission_checks)

        self._neuralyze_object(
            self.object,
            commit=self.commit,
            user=self.user,
            log_action=self.log_action,
        )


class NeuralyzeBulkAction(SnippetBulkAction):
    models = None
    neuralyzer_class = None
    display_name = _("Neuralyze")
    aria_label = _("Neuralyze")
    action_type = "neuralyze"
    template_name = "wagtailadmin/wagtail_neuralyzer/bulk_actions/confirm_bulk_neuralyze.html"

    @classmethod
    def execute_action(
        cls,
        objects,
        user=None,
        permission_checker=None,
        **kwargs,
    ):
        num_parent_objects, num_child_objects = 0, 0
        neuralyzer = cls.neuralyzer_class()
        for obj in objects:
            neuralyzer.run(filters={"pk": obj.pk})
            num_parent_objects += 1

        return num_parent_objects, num_child_objects

    def get_success_message(self, num_parent_objects, num_child_objects):
        return ngettext(
            "%(num_parent_objects)d object has been neuralyzed",
            "%(num_parent_objects)d objects have been neuralyzed",
            num_parent_objects,
        ) % {"num_parent_objects": num_parent_objects}
