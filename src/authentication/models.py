'''
Created on Jan 6, 2017

@author: roadd
'''
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.fields.related import ForeignKey
from school.models import School
from material.frontend.templatetags.material_frontend import verbose_name
from subject.models import Subject


class ExtendedUserManager(BaseUserManager):
  def create_user(self, username, first_name, last_name, password):
    if not username:
      raise ValueError('Users must have an username')
    
    if not first_name:
      raise ValueError('Users must have a first name')
      
    if not last_name:
      raise ValueError('Users must have a last name')
    
    if not password:
      raise ValueError('Users must have a password')

    user = self.model(
      first_name = first_name,
      last_name = last_name,
      username = self.normalize_username(username),
      status = 0
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, username, first_name, last_name, status, password):
    user = self.create_user(username, first_name, last_name, password)
    user.is_admin = True
    user.status = 3
    user.save(using=self._db)
    return user


class ExtendedUser(AbstractBaseUser):
  class Meta:
    index_text = "Manage"
    verbose_name = 'User'
    verbose_name_plural = 'Users'
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50, unique=True)
  
  school = ForeignKey(School, blank=True, null=True)
  date_of_birth = models.DateField(blank=True, null=True)
  phone_number = models.CharField(max_length=20, blank=True, null=True)
  
  STATUS_CHOICES = (
      (0, "Personal"),
      (1, "Director"),
      (2, "Inspector"),
      (3, "Admin"),
  )
  status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="author status")
  subjects = models.ManyToManyField(Subject, blank=True, null=True)
  
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=(status == 3))

  objects = ExtendedUserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['first_name', 'last_name', 'status']

  def get_full_name(self):
    return self.first_name + " " + self.last_name

  def get_short_name(self):
    return self.first_name

  def __unicode__(self):              
    return self.first_name + " " + self.last_name

  def has_perm(self, perm, obj=None):
    if perm == "frontend.view_module":
      return True
    if perm == "frontend.change_module":
      return False
    if self.status == 3:
      return True
    elif self.status == 0:
      if perm == "post.view_post":
        return True
      if perm == "post.change_own_post":
        return True
      return False
    elif self.status == 1:
      if perm == "school.change_own_school":
        return True
      if perm == "post.view_post":
        return True
      if perm == "post.change_own_post":
        return True
      return False
    elif self.status == 2:
      if perm == "post.view_post":
        return True
      if perm == "post.change_own_post":
        return True
      if perm == "event.change_own_event":
        return True
      if perm == "news.change_own_news":
        return True
      if perm == "subject.change_own_subjectpost":
        return True
      if perm == "gallery.change_own_gallery":
        return True
      return False
    return False

  def has_module_perms(self, app_label):
    return True

  @property
  def is_staff(self):
    return True