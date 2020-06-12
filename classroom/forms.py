from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Answer, Question, Student, StudentAnswer,
                              Subject, User)


class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):


    INTEGER_CHOICES= [tuple([x,x]) for x in range(1,5)]

    DEPARTMENTS= [
        ('SE', 'Software Engineering'),
        ('IT', 'Information Technology'),
        ('IS', 'Informatin System'),
        ('CS', 'Computer Science'),
            ]

    email = forms.EmailField(max_length=200)
    student_id = forms.CharField(max_length=15, required = True)
    dep= forms.CharField(label='Department', widget=forms.Select(choices=DEPARTMENTS))


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
    #    student.email.add(*self.cleaned_data.get('email'))
    #    student.enroll.add(*self.cleaned_data.get('enroll'))
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student

        fields = ('enroll', )
        widgets = {
            'enroll': forms.CheckboxSelectMultiple,

        }




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
