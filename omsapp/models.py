from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)
    


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('employee_number'),
        max_length=5,
        unique=True,
        # help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        # validators=[username_validator],
        error_messages={
            'unique': _("A user with that employee_number  already exists."),
        },
    )
    
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

class Customer(models.Model):
    customer_code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    date_created = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.customer_code +'/' + self.name)
    


class Supplier(models.Model):
    supplier_code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    date_created = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.supplier_code +'/' + self.name)
    

class Project(models.Model):
    prj_code = models.CharField(max_length=4, unique=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.PROTECT)
    def __str__(self):
        return self.prj_code
    

class Item(models.Model):
    item_code = models.CharField(max_length=5, unique=True)
    prj_code = models.ForeignKey(Project, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    parts_name = models.CharField(max_length=30)
    parts_number = models.CharField(max_length=30)
    sell_price = models.DecimalField(max_digits=9, decimal_places=2)
    buy_price = models.DecimalField(max_digits=9, decimal_places=2)
    date_created = models.DateTimeField(default=datetime.now)
    stock = models.IntegerField(default=0)
    def __str__(self):
        return self.item_code

class OrderNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=8, unique=True)
    date_created = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.order_number

class Order(models.Model):
    order_number = models.ForeignKey(OrderNumber, on_delete=models.CASCADE)
    item_code = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    supplier_delivery_date = models.DateField(default=datetime.today)
    customer_delivery_date = models.DateField(default=datetime.today)
    shipping_qty = models.IntegerField(default=0)
    receiving_qty = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.order_number)

class Shipping(models.Model):
    order_number = models.ForeignKey(OrderNumber, on_delete=models.CASCADE)
    item_code = models.ForeignKey(Item, on_delete=models.CASCADE)
    shipping_qty = models.IntegerField(default=0)
    shipped_date = models.DateField(default=datetime.today)
    def __str__(self):
        return str(self.order_number)

class Receiving(models.Model):
    order_number = models.ForeignKey(OrderNumber, on_delete=models.CASCADE)
    item_code = models.ForeignKey(Item, on_delete=models.CASCADE)
    receiving_qty = models.IntegerField(default=0)
    received_date = models.DateField(default=datetime.today)
    def __str__(self):
        return str(self.order_number)
