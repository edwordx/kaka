# -*- coding: utf-8 -*-
from django import forms
from . import models
from . import dbutils
from easy_select2 import apply_select2


class AdminSDBPosForm(forms.ModelForm):
    """
    判断terminal值
    """
    class Meta:
        model = models.SDBPos
        fields = ["user", "terminal"]
        widgets = {
            'user': apply_select2(forms.Select),
        }

    def clean_terminal(self):
        terminal = self.cleaned_data["terminal"]
        objs = models.SDBTerminal.objects.filter(terminal=terminal)
        if not objs:
            msg = u"终端号不存在"
            raise forms.ValidationError(msg)
        return terminal
