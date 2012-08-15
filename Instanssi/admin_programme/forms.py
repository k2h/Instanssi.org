# -*- coding: utf-8 -*-

from django import forms
from uni_form.helper import FormHelper
from uni_form.layout import Submit, Layout, Fieldset, ButtonHolder
from Instanssi.ext_programme.models import ProgrammeEvent

class ProgrammeEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgrammeEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                u'',
                'title',
                'description',
                'presenters',
                'presenters_titles',
                'icon_original',
                'email',
                'home_url',
                'twitter_url',
                'github_url',
                'facebook_url',
                'linkedin_url',
                'wiki_url',
                ButtonHolder (
                    Submit('submit', u'Tallenna')
                )
            )
        )
                
    class Meta:
        model = ProgrammeEvent
        exclude = ('event',)
