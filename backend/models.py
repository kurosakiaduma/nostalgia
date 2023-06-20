from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser
from uuid import uuid1, uuid4
import PIL.Image, imageio

GENDER_CHOICES = (
    ("Male","Male"),
    ("Female", "Female"),
    ("Non-Binary", "Non-Binary"),
    ("Prefer Not To Say","Prefer Not To Say")
)
"""
Family and member models
"""    
class Member(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid1)
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message="Please enter a valid email address in the format"), RegexValidator(regex='^name@name.name', inverse_match=True, message="Please provide a valid email address.")])
    fname = models.CharField(max_length=50, null=False)
    other_names = models.CharField(max_length=50, blank=True) 
    lname = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, default="Prefer Not To Say", max_length=20)
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=8, message="Please ensure the password is at least 8 characters"), RegexValidator(regex='^password', inverse_match=True, message="Please use a different password")], default="password")
    family = models.ForeignKey('Family', on_delete=models.CASCADE)
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='children_mother')
    father = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='children_father')
    spouse_of = models.ManyToManyField('self', blank=True)
    is_housekeeper = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    
    def __str__(self):
        return f'{self.fname} {self.lname} of {self.family}'
        
class Family(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(null=False, blank=False, max_length=50)
    founder = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True, related_name='founded_family')
    
    def __str__(self):
        return f'The {self.name} family that was founded by {self.founder}'

"""
Image uploads
"""    
def get_upload_path(instance, filename):
    return f'member_images/{instance.member.family.uuid}/{filename}'

class MemberImageManager(models.Manager):
    def add_image(self, member, image):
        member_image = self.create(member=member, image=image)
        return member_image

    def remove_image(self, member_image):
        member_image.delete()

class MemberImage(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = MemberImageManager()
       
"""
Family stories
"""    
class StoryManager(models.Manager):
    def add_story(self, title, content, family, author):
        story = self.create(title=title, content=content,
                            family=family, author=author)
        return story

    def remove_story(self, story):
        story.delete()

class Story(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = StoryManager()