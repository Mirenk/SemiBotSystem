from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm
from django import forms
from semi_app.models import TaskRequest

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
        print(value)
        try:
            int(value)
        except ValueError:
            pass
        else:
            value = str(value) + ' days'

        return super(DayDurationField, self).to_python(value)

# 依頼入力フォーム
class TaskRequestForm(ModelForm):
    start_matching_datetime = forms.DateTimeField(label='募集開始時間')
    rematching_duration = DayDurationField(label='再募集期間(日)')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TaskRequest
        fields = '__all__'
        labels = {
            'task_datetime': 'ゼミ日時',
            'bachelor_num': '学部生人数',
            'master_num': '院生人数',
        }