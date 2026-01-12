# app/forms/multi_checkboxes_field.py
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

class MultiCheckBoxField(SelectMultipleField):
    """ Renders a list of checkboxes instead of a <select multiple>"""
    widget = ListWidget()