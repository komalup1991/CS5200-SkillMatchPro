from django.db import models

class UserInfo(models.Model):
    userID = models.IntegerField(blank=False, null=False, primary_key=True)
    name = models.CharField(max_length=15, blank=True, null=True) 
    email = models.CharField(max_length=50, blank=True, null=True) 
    type = models.CharField(max_length=9, blank=True, null=True) 
    specialization = models.CharField(max_length=9, blank=True, null=True)
    password = models.CharField(max_length=9, blank=True, null=True)
    rating = models.CharField(max_length=9, blank=True, null=True)
    lastLogin = models.TimeField(blank=True, null=True)
    registrationDate = models.DateField(blank=True, null=True)
    class Meta:
        #managed = False
        db_table = 'UserInfo'

class Project(models.Model):
    projectID = models.IntegerField(blank=False, null=False, primary_key=True)
    freelancerID = models.IntegerField(blank=True, null=True)
    bidderID= models.IntegerField(blank=True, null=True)
    title=models.CharField(max_length=9, blank=True, null=True)
    description=models.CharField(max_length=255, blank=True, null=True)
    budget= models.IntegerField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    categoryID = models.IntegerField(blank=True, null=True)
    projectStatus = models.CharField(max_length=9, blank=True, null=True)
    startDate = models.TimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'Project'


class Profile(models.Model):
    # Field name made lowercase.
    profileid = models.AutoField(db_column='profileID', primary_key=True)
    # Field name made lowercase.
    userid = models.ForeignKey(
        'Userinfo', models.DO_NOTHING, db_column='userID', blank=True, null=True)
    # Field name made lowercase.
    firstname = models.CharField(
        db_column='firstName', max_length=20, blank=True, null=True)
    # Field name made lowercase.
    lastname = models.CharField(
        db_column='lastName', max_length=20, blank=True, null=True)
    # Field name made lowercase.
    profiletype = models.CharField(
        db_column='profileType', max_length=6, blank=True, null=True)
    # Field name made lowercase.
    profilepicture = models.CharField(
        db_column='profilePicture', max_length=255, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'Profile'
