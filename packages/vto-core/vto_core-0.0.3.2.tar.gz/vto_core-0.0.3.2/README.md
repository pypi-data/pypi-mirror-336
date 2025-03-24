# vto_core
This is a custom reusable Django core app.

It includes admin override templates (e.g., to display the project name and current environment in a header in the admin interface), a minimal login page template, a custom template tag to render Markdown partials, custom context processors to convey settings variables to templates, and middleware to activate user time zones in templates.

It also includes a time zones model, and a custom user model which uses the time zones model as a dropdown list *with autocomplete* in the admin UI (something which is missing from [django-timezone-field](https://pypi.org/project/django-timezone-field/)). Moreover, this allows one to only add the specific time zones desired, particularly choosing to use only the ones which are [canonical](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

The the user portion of the `admin.py` file is mostly copied verbatim from [upstream](https://github.com/django/django/tree/main/django/contrib/auth), and then tweaked to replace the stock `first_name` and `last_name` conventions from with slightly more international options, lightly inspired by the [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django/blob/master/{{cookiecutter.project_slug}}/{{cookiecutter.project_slug}}/users/models.py#L27) project.

The GitHub repository also has a sample backup script and sample JSON fixture.

## Disclaimer
This is just a personal test app, it is not intended for use by anyone else.

## Required By
- https://pypi.org/project/djinntoux/

## Requires
- [Markdown](https://pypi.org/project/Markdown/) (may switch to [commonmark](https://pypi.org/project/commonmark/) or [markdown2](https://pypi.org/project/markdown2/))