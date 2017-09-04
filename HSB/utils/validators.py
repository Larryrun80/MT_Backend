from wtforms.validators import ValidationError


class Unique(object):
    def __init__(self, message='something exists'):
        # init data to check here
        self.message = message
        pass

    def __call__(self, form, field):
        success = True  # write your check code here
        if not success:
            raise ValidationError(self.message)
