from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator
from uuid import uuid4, uuid5

GENDER_CHOICES = (
    ("Male","Male"),
    ("Female", "Female"),
    ("Non-Binary", "Non-Binary"),
    ("Prefer Not To Say","Prefer Not To Say")
)

class FamilyManager(models.Manager):
    def create_family(self, name, founder):
        family = self.create(name=name, founder=founder)
        return family

class MemberManager(models.Manager):
    def add_member(self, family, fname, lname, birth_date, gender, email=None):
        member = self.create(family=family, fname=fname, lname=lname,
                             birth_date=birth_date, gender=gender,
                             email=email)
        return member

    def remove_member(self, member):
        member.delete()


class Member(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid5)
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message="Please enter a valid email address in the format"), RegexValidator(regex='^name@name.name', inverse_match=True, message="Please provide a valid email address.")])
    fname = models.CharField(max_length=50, null=False)
    other_names = models.CharField(max_length=50, blank=True) 
    lname = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    gender = models.CharField(choices=GENDER_CHOICES, default="Prefer Not To Say", max_length=20)
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=8, message="Please ensure the password is at least 8 characters"), RegexValidator(regex='^password', inverse_match=True, message="Please use a different password")], default="password")
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    is_founder = models.BooleanField()
    child_of = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='children')
    spouse_of = models.ManyToManyField('self', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return f'{self.fname} {self.lname} of {self.family}'


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    objects = MemberManager()


    def __str__(self):
        return f'{self.fname} {self.lname}'

class Family(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(null=False, blank=False, max_length=50)
    founder = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True, related_name='founded_family')
    
    objects = FamilyManager()
    
    def __str__(self):
        return f'The {self.name} family that was founded by {self.founder}'
    
class MemberImage(models.Model):
    member = models.ForeignKey(Member, related_name="images")
    image = models.ImageField()
    