# wagtail-neuralyzer

Pairs with [django-neuralyzer](https://github.com/webu/django-neuralyzer/), with wagtail support.

## Install

```
pip install wagtail-neuralyzer
```

## Register a model to have neuralyze action

Add `wagtail_neuralyzer` to your `INSTALLED_APP`:

```py
INSTALLED_APP = [
    ...
    "django_neuralyzer",
    "wagtail_neuralyzer",
    ...
]
```

### Add item action

Add the `NeuralyzeSnippetViewSetMixin` to your snippet class:

```py

from wagtail_neuralyzer.views import NeuralyzeSnippetViewSetMixin
from wagtail_neuralyzer.views import NeuralyzeView

from my_app.neuralyzers import PersonNeuralyzer

# Create a new view that handle url and action as well as neuralyzer class
class OperatorNeuralyzeView(NeuralyzeView):
    neuralyzer_class = OperatorNeuralyzer


# inherit NeuralyzeSnippetViewSetMixin to register new url and neuralyze view
class PersonSnippetViewSet(NeuralyzeSnippetViewSetMixin, SnippetViewSet):
    model = Person
    neuralyze_view_class = OperatorNeuralyzeView
    ...
```

and finally register the new action:

```py
from wagtail import hooks
from wagtail_neuralyzer.menu_item import NeuralyzeMenuItem

@hooks.register("register_snippet_action_menu_item")
def register_anonymize_menu_item(model):
    if model == Person:
        return NeuralyzeMenuItem()
```

And _Tada_, your model should have an "Anonymize" action together with save/delete/publish/...

### Add bulk action

You can also add bulk action to the index view by registering wagtail hook

```py
from wagtail import hooks

from wagtail_neuralyzer.action import NeuralyzeBulkAction

from my_app.models import Person
from my_app.neuralyzers import StudentNeuralyzer

@hooks.register("register_bulk_action")
class PersonNeuralyzerBulkAction(NeuralyzeBulkAction):
    models = [Person] # specify model here
    neuralyzer_class = PersonNeuralyzer # and neuralyzer to use here
```
