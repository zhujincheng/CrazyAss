from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

#Myuser改名为UserProfile
class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,

    )
    name = models.CharField(max_length=64, verbose_name="姓名")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    #is_admin = models.BooleanField(default=False)
    bind_hosts=models.ManyToManyField('BindHost',blank=True)
    host_groups=models.ManyToManyField('HostGroup',blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True


    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    # class Meta:
    #     permissions = (
    #         ('crm_table_name_list','可以查看所有app下注册的表名'),
    #         ('crm_table_list', '可以查看kingadmin每张表里所有的数据'),
    #         ('crm_table_list_view', '可以访问kingadmin表里每条数据的修改页'),
    #         ('crm_table_list_change', '可以对kingadmin表里的每条数据进行修改'),
    #         ('crm_table_obj_add_view', '可以访问kingadmin每张表的数据增加页'),
    #         ('crm_table_obj_add', '可以对kingadmin每张表进行数据添加'),
    #
    #     )


class Host(models.Model):
    """主机信息"""
    hostname=models.CharField(max_length=64)
    #专用ip字段
    ip_addr=models.GenericIPAddressField(unique=True)
    port=models.PositiveIntegerField(default=22)
    idc=models.ForeignKey('IDC')

    enabled=models.BooleanField(default=True)

    def __str__(self):
        return self.hostname

class IDC(models.Model):
    """机房信息"""
    name=models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.name

class HostGroup(models.Model):
    """主机组"""
    name=models.CharField(max_length=64,unique=True)
    bind_hosts=models.ManyToManyField("BindHost",blank=True,null=True)

    def __str__(self):
        return self.name

class HostUser(models.Model):
    """主机登录账户"""
    auth_type_choices=((0,'ssh-password'),(1,'ssh-key'))
    auth_type=models.SmallIntegerField(choices=auth_type_choices,default=0)
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=128,blank=True,null=True)

    def __str__(self):
        return self.username
    class Meta:
        unique_together=('auth_type','username','password')

class BindHost(models.Model):
    """绑定主机和主机账号"""
    host=models.ForeignKey('Host')
    host_user=models.ForeignKey("HostUser")

    def __str__(self):
        return "%s@%s"%(self.host,self.host_user)

    class Meta:
        unique_together=('host','host_user')