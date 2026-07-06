from .start import register as register_start
from .upload import register as register_upload

def register_handlers(app):
    register_start(app)
    register_upload(app)