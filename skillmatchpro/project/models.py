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
    projectid = models.AutoField(primary_key=True, db_column='projectID')  # Field name made lowercase.
    freelancerid = models.ForeignKey('Userinfo', on_delete=models.DO_NOTHING, db_column='freelancerID', blank=True, null=True, related_name='freelancer_projects')
    bidderid = models.ForeignKey('Userinfo', on_delete=models.DO_NOTHING, db_column='bidderID', blank=True, null=True, related_name='bidder_projects')
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Changed to TextField for larger text
    budget = models.IntegerField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    categoryid = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_column='categoryID', blank=True, null=True)  # Field name made lowercase.
    projectstatus = models.CharField(max_length=15, blank=True, null=True, db_column='projectStatus')  # Field name made lowercase.
    startdate = models.DateTimeField(blank=True, null=True, db_column='startDate')  # Field name made lowercase.
    photo = models.CharField(max_length=75, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Project'

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
