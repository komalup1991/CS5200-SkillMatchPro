# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bid(models.Model):
    bidid = models.AutoField(db_column='bidID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    projectid = models.ForeignKey('Project', models.DO_NOTHING, db_column='projectID', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bid'


class Category(models.Model):
    categoryid = models.IntegerField(db_column='categoryID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Category'


class Dispute(models.Model):
    disputeid = models.AutoField(db_column='disputeID', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    fromuserid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='fromUserID', blank=True, null=True)  # Field name made lowercase.
    touserid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='toUserID', related_name='dispute_touserid_set', blank=True, null=True)  # Field name made lowercase.
    projectid = models.ForeignKey('Project', models.DO_NOTHING, db_column='projectID', blank=True, null=True)  # Field name made lowercase.
    disputestatus = models.CharField(db_column='disputeStatus', max_length=13, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dispute'


class Invoice(models.Model):
    invoiceid = models.AutoField(db_column='invoiceID', primary_key=True)  # Field name made lowercase.
    projectid = models.ForeignKey('Project', models.DO_NOTHING, db_column='projectID', blank=True, null=True)  # Field name made lowercase.
    clientuserid = models.IntegerField(db_column='clientUserID', blank=True, null=True)  # Field name made lowercase.
    paymentid = models.IntegerField(db_column='paymentID', blank=True, null=True)  # Field name made lowercase.
    freelanceruserid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='freelancerUserID', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Invoice'


class Message(models.Model):
    messageid = models.AutoField(db_column='messageID', primary_key=True)  # Field name made lowercase.
    fromuserid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='fromUserID', blank=True, null=True)  # Field name made lowercase.
    touserid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='toUserID', related_name='message_touserid_set', blank=True, null=True)  # Field name made lowercase.
    projectid = models.ForeignKey('Project', models.DO_NOTHING, db_column='projectID', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=150, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Message'


class Notification(models.Model):
    notificationid = models.AutoField(db_column='notificationID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Notification'


class Payment(models.Model):
    paymentid = models.AutoField(db_column='paymentID', primary_key=True)  # Field name made lowercase.
    payerid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='payerID', blank=True, null=True)  # Field name made lowercase.
    payeeid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='payeeID', related_name='payment_payeeid_set', blank=True, null=True)  # Field name made lowercase.
    projectid = models.ForeignKey('Project', models.DO_NOTHING, db_column='projectID', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=7, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Payment'


class Profile(models.Model):
    profileid = models.AutoField(db_column='profileID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    profiletype = models.CharField(db_column='profileType', max_length=6, blank=True, null=True)  # Field name made lowercase.
    profilepicture = models.CharField(db_column='profilePicture', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Profile'


class Project(models.Model):
    projectid = models.AutoField(db_column='projectID', primary_key=True)  # Field name made lowercase.
    freelancerid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='freelancerID', blank=True, null=True)  # Field name made lowercase.
    bidderid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='bidderID', related_name='project_bidderid_set', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=10000, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryID', blank=True, null=True)  # Field name made lowercase.
    projectstatus = models.CharField(db_column='projectStatus', max_length=15, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Project'


class Qa(models.Model):
    qaid = models.AutoField(db_column='QAID', primary_key=True)  # Field name made lowercase.
    projectid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projectID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    questioncontent = models.CharField(db_column='questionContent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    answercontent = models.CharField(db_column='answerContent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'QA'


class Rating(models.Model):
    ratingid = models.AutoField(db_column='ratingID', primary_key=True)  # Field name made lowercase.
    rateduserid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='ratedUserID', blank=True, null=True)  # Field name made lowercase.
    ratingbyuserid = models.ForeignKey('Userinfo', models.DO_NOTHING, db_column='ratingByUserID', related_name='rating_ratingbyuserid_set', blank=True, null=True)  # Field name made lowercase.
    rating = models.CharField(max_length=1, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Rating'


class Shipping(models.Model):
    shippingid = models.AutoField(db_column='shippingID', primary_key=True)  # Field name made lowercase.
    projectid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projectID', blank=True, null=True)  # Field name made lowercase.
    trackingnumber = models.IntegerField(db_column='trackingNumber', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Shipping'


class Userinfo(models.Model):
    userid = models.AutoField(db_column='userID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)
    registrationdate = models.DateTimeField(db_column='registrationDate', blank=True, null=True)  # Field name made lowercase.
    lastlogin = models.DateTimeField(db_column='lastLogin', blank=True, null=True)  # Field name made lowercase.
    specialization = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserInfo'


class AdminhomepageCategory(models.Model):
    categoryid = models.IntegerField(db_column='categoryID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'adminHomePage_category'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
