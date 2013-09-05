class MetaMixin(object):
    '''
    Functions that answer common questions about model. 
    The code asking these questions at the moment reside 
    in BeterModelAdmin and also in various templates. 
    This started as being a part of the viewmixins but I 
    soon found myself writing the same functions for the 
    admin. In order to keep things DRY, I am moving it here. 
    For historical reasons it is important to mention here 
    that I seriously considered making template tags out of
    some of these functions. I didn't because template tags 
    would not have been usable in the admin resulting again
    in code duplication.
    Finally, for the record, this mixin assumes that the
    get_queryset function has been defined.
    '''
    def get_model(self):
        '''
        Returns model of defined queryset
        '''
        return self.get_queryset().model

    def get_model_name(self):
        '''
        Returns name of the model
        '''
        model = self.get_model()
        return model._meta.object_name

    def get_model_name_plural(self):
        '''
        Returns plural name of the model
        '''
        model = self.get_queryset().model
        return model._meta.verbose_name_plural.title()

    def get_app_name(self):
        '''
        Reutrns the app name that the model for self.queryset
        belongs to
        '''
        model = self.get_queryset().model
        return model._meta.app_label

    def get_view_name(self, viewtype):
        '''
        Returns a friendly name for our view for use in reverse
        and the likes.
        '''
        return '%s_%s_%s' % (self.get_app_name().lower(),
                             self.get_model_name().lower(),
                             viewtype)

    def get_model_fields(self):
        '''
        Returns the field names of model
        '''
        model = self.get_model()
        return model._meta.fields
