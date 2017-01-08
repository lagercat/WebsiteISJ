'''
Created on Jan 6, 2017

@author: roadd
'''
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.fields.related import ForeignKey
from school.models import School


class ExtendedUserManager(BaseUserManager):
  def create_user(self, email, first_name, last_name, password):
    if not email:
      raise ValueError('Users must have an email address')
    
    if not first_name:
      raise ValueError('Users must have a first name')
      
    if not last_name:
      raise ValueError('Users must have a last name')
    
    if not password:
      raise ValueError('Users must have a password')

    user = self.model(
      first_name = first_name,
      last_name = last_name,
      email = self.normalize_email(email),
      status = 0
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, first_name, last_name, status, password):
    user = self.create_user(email, first_name, last_name, password)
    user.is_admin = True
    user.status = 3
    user.save(using=self._db)
    return user


class ExtendedUser(AbstractBaseUser):
  class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'Users'
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(
    verbose_name='email address',
    max_length=255,
    unique=True,
  )
  school = ForeignKey(School, blank=True, null=True)
  date_of_birth = models.DateField(blank=True, null=True)
  phone_number = models.CharField(max_length=20, blank=True, null=True)
  
  STATUS_CHOICES = (
      (0, "Personal"),
      (1, "Director"),
      (2, "Inspector"),
      (3, "Admin"),
  )
  status = models.IntegerField(choices=STATUS_CHOICES)
  subjects = models.ManyToManyField("subject.Subject", blank=True)
  
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=(status == 3))

  objects = ExtendedUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name', 'status']
  
  @property
  def username(self):
    return self.email

  def get_full_name(self):
    return self.first_name + " " + self.last_name

  def get_short_name(self):
    return self.first_name

  def __unicode__(self):              
    return self.first_name + " " + self.last_name

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True

  @property
  def is_staff(self):
    return self.is_admin