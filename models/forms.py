from wtforms import Form, StringField, TextAreaField, validators


class CommentForm(Form):
    """Blog entry comment form"""
    name = StringField('name', [validators.required(), validators.length(max=20)])
    email = StringField('email', [validators.optional(), validators.length(min=5, max=50)])
    content = TextAreaField('content', [validators.required(), validators.length(min=5, max=1000)])
    occupation = StringField('occupation', [validators.optional(), validators.length(max=100)])
