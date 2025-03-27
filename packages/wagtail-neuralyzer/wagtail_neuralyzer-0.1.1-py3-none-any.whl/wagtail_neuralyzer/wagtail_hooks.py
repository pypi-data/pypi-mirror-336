from django.utils.translation import gettext_lazy as _

from wagtail import hooks


@hooks.register("register_log_actions")
def additional_log_actions(actions):
    actions.register_action("wagtail_neuralyzer.neuralyze", _("Neuralyze"), _("Was anonymize"))


# @hooks.register("register_bulk_action")
# class PersonBulkAction(NeuralyzeBulkAction):
#     models = [Person]
#     neuralyzer_class = PersonNeuralyzer
