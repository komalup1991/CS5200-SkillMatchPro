from django.db import models

# Create your models here.

class Category(models.Model):
    categoryID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    class Meta:
        managed = False
        db_table = 'Category'

class UserInfo(models.Model):
    # User information
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Use a hashed password field
    type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('normal', 'Normal')])
    registrationDate = models.DateTimeField(auto_now_add=True)
    lastLogin = models.DateTimeField(auto_now=True)
    specialization = models.CharField(max_length=50, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=3)  # A user's rating (1-5)

    class Meta:
        managed = False
        db_table = 'UserInfo'


from django.db import models

class Project(models.Model):
    projectID = models.AutoField(primary_key=True)
    freelancerID = models.ForeignKey(UserInfo, related_name='freelancer', on_delete=models.SET_NULL, null=True)
    bidderID = models.ForeignKey(UserInfo, related_name='bidder', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50, null=True)
    description=models.CharField(max_length=1000, blank=True, null=True)
    budget = models.PositiveIntegerField(null=True)
    deadline = models.DateTimeField(null=True)
    categoryID = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    PROJECT_STATUSES = [
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('awaiting_bids', 'Awaiting Bids'),
    ]
    
    projectStatus = models.CharField(max_length=15, choices=PROJECT_STATUSES, null=True)
    startDate = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'Project'

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)








