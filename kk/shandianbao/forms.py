# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django import forms
from . import models
from . import dbutils

from easy_select2 import apply_select2
from easy_select2.widgets import Select2


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


class AdminSDBPosProxyForm(forms.Form):
    """
    判断terminal值
    """
    terminals = forms.CharField(widget=forms.Textarea)
    user = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        fields = ["user", "terminals"]
        widgets = {
            'user': apply_select2(forms.Select),
        }

    def clean_terminals(self):
        terminals = self.cleaned_data["terminals"]
        terminals = terminals.split()
        objs = models.SDBTerminal.objects.filter(terminal__in=terminals)
        terminal_list = [obj.terminal for obj in objs]
        self.terminals = terminal_list
        print "clean_terminals"
        return terminal_list

    # def save_model(self, request, obj, form, change):
    #     print self.terminals
    #     print "save_model"

    # def save(self, commit=False):
    #     extra_field = self.cleaned_data.get('terminals', None)
    #     print "save"
    #     print self.terminals, 'xx'
    #     print extra_field
