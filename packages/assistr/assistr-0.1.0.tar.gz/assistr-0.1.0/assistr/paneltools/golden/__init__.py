"""
GoldenTemplate based on the golden-layout library.
"""
from __future__ import annotations

import pathlib

from typing import TYPE_CHECKING, Literal

import param

from panel import config
from panel.io.resources import JS_URLS
from panel.template.base import BasicTemplate

if TYPE_CHECKING:
    from panel.io.resources import ResourcesType
    #from ...io.resources import ResourcesType

class IRISGoldenTemplate(BasicTemplate):
    """
    GoldenTemplate is built on top of golden-layout library.
    """

    sidebar_width = param.Integer(default=74, constant=True, doc="""
        The width of the sidebar in percent.""")

    # _css = './golden.css'
    # _template = './golden.html'

    _css = pathlib.Path(__file__).parent / 'golden.css'
    _template = pathlib.Path(__file__).parent / 'golden.html'

    # TODO - change this to use root based dir
    logo = pathlib.Path(__file__).parent / '../static/intersystems-logo.svg'
    print(f"logo: {logo}")
    #logo = '../static/intersystems-logo.svg'
    
    _resources = {
        'css': {
            'goldenlayout': f"{config.npm_cdn}/golden-layout@1.5.9/src/css/goldenlayout-base.css",
            'golden-theme-dark': f"{config.npm_cdn}/golden-layout@1.5.9/src/css/goldenlayout-dark-theme.css",
            'golden-theme-light': f"{config.npm_cdn}/golden-layout@1.5.9/src/css/goldenlayout-light-theme.css",
        },
        'js': {
            'jquery': JS_URLS['jQuery'],
            'goldenlayout': f"{config.npm_cdn}/golden-layout@1.5.9/dist/goldenlayout.min.js",
        }
    }

    def _apply_root(self, name, model, tags):
        if 'main' in tags:
            model.margin = (10, 15, 10, 10)
            model.margin = (0, 0, 0, 0)

    def resolve_resources(
        self,
        cdn: bool | Literal['auto'] = 'auto',
        extras: dict[str, dict[str, str]] | None = None
    ) -> ResourcesType:
        resources = super().resolve_resources(cdn=cdn, extras=extras)
        del_theme = 'dark' if self._design.theme._name =='default' else 'light'
        del resources['css'][f'golden-theme-{del_theme}']
        return resources
