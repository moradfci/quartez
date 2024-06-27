from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class TimeStampeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=125,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
       
        return self.name
        return full_name if full_name else self.email
    
    def __str__(self):
        return self.email


class BusinessOwner(TimeStampeModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="owner")

    def __str__(self):
        return self.user.email


class Company(TimeStampeModel):
    owner = models.ForeignKey(
        BusinessOwner, on_delete=models.CASCADE, related_name="owner_companies")
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('owner', 'name',)


class Employee(TimeStampeModel):
    owner = models.ForeignKey(
        BusinessOwner, on_delete=models.CASCADE, related_name="owner_employees")
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee")
    company = models.ForeignKey(
        Company,  on_delete=models.CASCADE, related_name="company_employees")
    department = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.name


class Review(TimeStampeModel):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"Review {self.id}  - employee:{self.employee.name}"
