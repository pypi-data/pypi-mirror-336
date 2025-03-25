from datetime import datetime
import os
import pathlib
import sys

class freenove:
    def init_(self, name, number):
        sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

        os.system("rm -r freenove_Kit")
        os.system(f"git clone --depth 1 https://github.com/Freenove/{name} freenove_Kit")

        project = f"fnk00{number}-docs"
        copyright = '2016-2025, Freenove'
        author = 'Freenove'
        release = 'v1.0.0'
        version = 'v1.0.0'

        extensions = [
            "sphinx.ext.duration",
            "sphinx.ext.doctest",
            "sphinx.ext.extlinks",
            "sphinx.ext.intersphinx",
            "sphinx.ext.extlinks",
            "sphinx.ext.autosectionlabel",
            "sphinxcontrib.googleanalytics",
        ]

        autosectionlabel_prefix_document = True
        googleanalytics_id="G-THC0SQQTDX"

        source_suffix = {
            '.rst': 'restructuredtext',
        }

        templates_path = ['_templates']
        exclude_patterns = []

        html_static_path = ['_static']

        html_theme = 'sphinx_rtd_theme'
        html_theme_options = {
            'collapse_navigation': False,
            'logo_only': True,
            'navigation_depth': -1,
            'includehidden': True,
            'flyout_display': 'hidden',
            'version_selector': True,
            'prev_next_buttons_location': 'both',
            'style_external_links': True,
            'language_selector': True,
        }

        language = 'en'
        locale_dirs = ['../locales/']   # path is example but recommended.
        gettext_compact = False  # optional.
        gettext_uuid = True  # optional.

        rst_prolog = """
        .. include:: <s5defs.txt>
        .. include:: ../../../_static/style/custom-style.txt
        """

        variables_to_export = [
            "project",
            "copyright",
            "version",
        ]
        frozen_locals = dict(locals())
        prolog = "\n".join(
            map(lambda x: f".. |{x}| replace:: {frozen_locals[x]}",
                variables_to_export)
        )

        print(rst_prolog)
        del frozen_locals

        html_css_files = [
            'https://cdn.jsdelivr.net/gh/Freenove/freenove-docs/docs/source/_static/css/color-roles.css',
            'https://cdn.jsdelivr.net/gh/Freenove/freenove-docs/docs/source/_static/css/custom.css',
            'https://cdn.jsdelivr.net/gh/Freenove/freenove-docs/docs/source/_static/css/navigationStyle.css',
        ]

        html_js_files = [
            'https://cdn.jsdelivr.net/gh/Freenove/freenove-docs/docs/source/_static/js/custom.js',
            # 'js/custom.js'
        ]

        extlinks = {
            "Freenove": (
                "https://docs.freenove.com/projects/%s/en/latest/", None
            )
        }

        html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")

        intersphinx_mapping = {
            
        }
        intersphinx_disabled_reftypes = ["*"]

        suppress_warnings = ['autosectionlabel.*']