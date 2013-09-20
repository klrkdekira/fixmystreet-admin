from admin import models
import logging

log = logging.getLogger(__name__)


def includeme(config):
    settings = config.registry.settings.get('admin.fa_settings}}', {})

    # Example to add a specific model
    #config.formalchemy_model("/my_model", package='admin',
    #                         model='admin.models.MyModel')
    #                         **settings)

    log.info('admin.faroutes loaded')
