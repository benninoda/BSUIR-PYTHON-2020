from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group
from django.forms import ModelForm


class CheckInEntry(models.Model):
    YEAR_OF_EDUCATION = [
        ('1', 'first'),
        ('2', 'second'),
        ('3', 'third'),
        ('4', 'forth'),
        ('1m', 'first master'),
        ('2m', 'second master'),
    ]
    name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    # telephone = models.CharField(max_length=12, default=None)
    email = models.EmailField(default=None)
    faculty = models.CharField(max_length=20)
    course = models.CharField(max_length=2, choices=YEAR_OF_EDUCATION)

    def __str__(self):
        return 'Заявление {}'.format(self.pk)


class CheckInForm(ModelForm):
    class Meta:
        model = CheckInEntry
        fields = '__all__'


class RulesEntry(models.Model):
    rule = models.TextField()
    fine = models.IntegerField()

    def __str__(self):
        return 'Правило {}'.format(self.pk)


# class GymJournalEntry(models.Model):
#     lodger = models.ForeignKey('Lodger', on_delete=models.CASCADE)
#     date = models.DateField()
#
#
# class VisitorJournalEntry(models.Model):
#     lodger = models.ForeignKey('Lodger', on_delete=models.CASCADE)
#     date_come = models.DateField()
#     date_quit = models.DateField()
#     document = models.CharField(max_length=50)
#
#
# class ServiceJournalEntry(models.Model):
#     lodger = models.ForeignKey('Lodger', on_delete=models.CASCADE)
#     date = models.DateField()
#     problem = models.CharField(max_length=50)


class Room(models.Model):
    checking = models.DateField()
    room_number = models.IntegerField()

    def __str__(self):
        return 'Room {}'.format(self.room_number)


class RentEntry(models.Model):
    name = models.CharField(max_length=20, default=None)
    email = models.EmailField(default=None)
    telephone = models.CharField(max_length=13)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return 'Договор {}'.format(self.pk)


class RentForm(ModelForm):
    class Meta:
        model = RentEntry
        exclude = ['cost']


class Furniture(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField(default=10)
    room = models.ForeignKey('Room', related_name='furniture', on_delete=models.CASCADE)


class User(AbstractUser):
    """User model."""
    telephone = models.CharField(max_length=12)
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=20)
    faculty = models.CharField(max_length=30)
    current_clocks = models.PositiveIntegerField(default=0)
    middle_name = models.CharField(max_length=20)
    your_clocks = models.PositiveIntegerField(default=40)
    verified = models.BooleanField(default=False)

    def is_lodger(self):
        return self.groups.filter(name='Lodger').exists()

    def is_personnel(self):
        return self.groups.filter(name='Personnel').exists()


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class WorkEntry(models.Model):
    name = models.CharField(max_length=50)
    exec_men = models.ManyToManyField('User', default=None)
    clock = models.PositiveIntegerField()
    date_from = models.DateField()
    date_to = models.DateField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return 'Отработка "{}"'.format(self.name)


class WorkEntryCreateForm(ModelForm):
    class Meta:
        model = WorkEntry
        exclude = ['ecex_men']

    def __init__(self, *args, **kwargs):
        super(WorkEntryCreateForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class MessageTo(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(default=None)
    text = models.TextField()


class MessageToForm(ModelForm):
    class Meta:
        model = MessageTo
        fields = '__all__'


class MessageToAnswerRent(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(default=None)
    text = models.TextField()
    cost = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Ответ {} на аренду'.format(self.pk)


class MessageToAnswerRentForm(ModelForm):
    class Meta:
        model = MessageToAnswerRent
        fields = '__all__'

