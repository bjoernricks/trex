from trex.settings_global import *

DEBUG = False

REST_FRAMEWORK = {
    # don't use BrowsableAPIRenderer
    "DEFAULT_RENDERER_CLASSES": {
        "rest_framework.renderers.JSONRenderer"
    },
    # deactivate "browser enhancements"
    "FORM_CONTENT_OVERRIDE": None,
    "FORM_METHOD_OVERRIDE": None,
    "FORM_CONTENTTYPE_OVERRIDE": None,
}
