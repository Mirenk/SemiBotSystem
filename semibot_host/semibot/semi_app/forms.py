from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm
from django import forms
from semi_app.models import TaskRequest
from datetime import datetime, timedelta
from django.utils import timezone

# placeholder内に入力すべき値を表示させるためにやってる
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

# これも同じ
class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# 数字→日付間隔フィールド
class DayDurationField(forms.DurationField):
    widget = forms.NumberInput

    def to_python(self, value):
        try:
            int(value)
        except ValueError:
            pass
        else:
            value = str(value) + ' days'

        return super(DayDurationField, self).to_python(value)

# 依頼入力フォーム
class TaskRequestForm(ModelForm):
    start_matching_datetime = forms.DateTimeField(label='募集開始時刻', required=False)
    start_matching_now = forms.BooleanField(label='今すぐ募集を開始する', required=False)
    rematching_duration = DayDurationField(label='再募集期間(日)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if key != 'start_matching_now' or key != 'is_random':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

    def clean_start_matching_datetime(self):
        start_matching_datetime = self.cleaned_data.get('start_matching_datetime')
        matching_end_datetime = self.cleaned_data.get('matching_end_datetime')
        if start_matching_datetime is not None:
            if start_matching_datetime <= timezone.now() + timedelta(minutes=30):
                raise forms.ValidationError('募集開始時刻は現在時刻より30分以上空けてください。')
            if start_matching_datetime >= matching_end_datetime:
                raise forms.ValidationError('募集開始時刻は募集終了時刻より前にしてください。')
        return start_matching_datetime

    def clean_matching_end_datetime(self):
        matching_end_datetime = self.cleaned_data.get('matching_end_datetime')
        task_datetime = self.cleaned_data.get('task_datetime')
        if matching_end_datetime > task_datetime:
            raise forms.ValidationError('募集終了時刻はゼミ日より前にしてください。')
        return matching_end_datetime

    def clean(self):
        cleaned_data = super(TaskRequestForm, self).clean()
        start_matching_datetime = cleaned_data.get('start_matching_datetime')
        start_matching_now = cleaned_data.get('start_matching_now')
        if not (start_matching_datetime or start_matching_now):
            raise forms.ValidationError('募集開始時刻を入力するか、今すぐ募集を開始するにチェックを入れてください。')
        return cleaned_data

    class Meta:
        model = TaskRequest
        fields = '__all__'
        labels = {
            'task_datetime': 'ゼミ日時',
            'bachelor_num': '学部生人数',
            'master_num': '院生人数',
            'matching_end_datetime': '募集終了時刻',
            'is_random': 'ランダムゼミ'
        }