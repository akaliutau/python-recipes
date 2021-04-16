import os
import sys

import jinja2
from flask import app, url_for
from jinja2 import Environment, PackageLoader, select_autoescape
from nameko.extensions import DependencyProvider

HOMEPAGE = 'home.html'


class Jinja2(DependencyProvider):
    """This code havely uses templating, see the details at
        https://medium.com/swlh/baking-static-sites-with-python-and-jinja-330fe29bbe08
    """

    def setup(self):
        self.template_renderer = TemplateRenderer(
            'messenger.core', 'templates'
        )

    def get_dependency(self, worker_ctx):
        return self.template_renderer


@jinja2.contextfunction
def include_file(ctx, name):
    env = ctx.environment
    return jinja2.Markup(env.loader.get_source(env, name)[0])


class TemplateRenderer:

    def __init__(self, package_name, template_dir):
        self.template_env = Environment(
            loader=PackageLoader(package_name, template_dir),
            autoescape=select_autoescape(['html'])
        )

        self.template_env.globals['include_file'] = include_file

    def render_home(self, messages):
        template = self.template_env.get_template(HOMEPAGE)
        return template.render(messages=messages)
