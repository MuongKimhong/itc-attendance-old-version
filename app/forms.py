from .models import Class, EnterCode, Attendance, LeaveForm
from django import forms

departmentAttr = {'id': 'class-department-field', 'class': 'form-control'}
yearAttr = {'id': 'class-years-field', 'class': 'form-control'}
subjectAttr = {'id': 'class-subject-field', 'class': 'form-control', 'type': 'text'}
lfdAttr = {'id': 'leave-from-date', 'class': 'form-control', 'type': 'date'}
ltdAttr = {'id': 'leave-from-date', 'class': 'form-control', 'type': 'date'}
lrAttr = {'id': 'leave-reason', 'class': 'form-control md-textarea text-justify', 'type': 'textarea'}

# Class Form
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['department', 'years', 'subject']

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        self.fields['department'].required = True
        self.fields['years'].required = True
        self.fields['subject'].required = True
        self.fields['department'].widget.attrs.update(departmentAttr)
        self.fields['years'].widget.attrs.update(yearAttr)
        self.fields['subject'].widget.attrs.update(subjectAttr)

# AttendanceForm
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', ]
        widgets = {'student': forms.CheckboxSelectMultiple()}

    def __init__(self, class_pk, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        current_class = Class.objects.get(id=class_pk)
        self.fields['student'].queryset = current_class.student.order_by('first_name')


class AttendanceFormUpdate(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', ]
        widgets = {'student': forms.CheckboxSelectMultiple()}

# Enter Code
class EnterCodeForm(forms.ModelForm):
    class Meta:
        model = EnterCode
        fields = ['code', ]

    def __init__(self, *args, **kwargs):
        super(EnterCodeForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'class': 'form-control', 'id': 'enter-code-field'})
        self.fields['code'].required = True

    def clean_code(self):
        code = self.cleaned_data.get('code')
        print(code)
        if not Class.objects.filter(random_code=code).exists():
            print("not found")
            raise forms.ValidationError("Class with this code not found!")
        return code


class LeaveFormForm(forms.ModelForm):
    class Meta:
        model = LeaveForm
        fields = ['leaveFromDate', 'leaveTillDate', 'leaveReason']
        widgets = {
            'leaveFromDate': forms.DateInput(lfdAttr),
            'leaveTillDate': forms.DateInput(ltdAttr),
            'leaveReason': forms.Textarea(lrAttr)
        }
    
    def __init__(self, *args, **kwargs):
        super(LeaveFormForm, self).__init__(*args, **kwargs)
        self.fields['leaveFromDate'].required = True
        self.fields['leaveTillDate'].required = True
        self.fields['leaveReason'].required = True
