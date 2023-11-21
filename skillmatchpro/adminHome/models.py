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

# class Message(models.Model):
#     messageID = models.AutoField(primary_key=True)
#     fromUserID = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='senderID')
#     toUserID = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='receiverID')
#     projectID = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
#     content = models.CharField(max_length=150, null=True, blank=True)
#     type = models.CharField(max_length=50, null=True, blank=True)
#     date = models.DateTimeField(null=True, blank=True)

#     # def __str__(self):
#     #     return f"Message {self.messageID} - {self.content}"

#     class Meta:
#         managed = False
#         db_table = 'Message'

class Dispute(models.Model):
    disputeID = models.AutoField(primary_key=True)
    date = models.DateTimeField(null=True, blank=True)
    DISPUTE_TYPES = [
        ('payment_issues', 'Payment Issues'),
        ('non-payment', 'Non-Payment'),
        ('service_issues', 'Service Issues'),
        ('non-performance', 'Non-Performance'),
        ('fraud', 'Fraud'),
    ]
    type = models.CharField(max_length=20, choices=DISPUTE_TYPES, null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    fromUserID = models.ForeignKey(UserInfo, related_name='disputeBy', on_delete=models.SET_NULL, null=True)
    toUserID = models.ForeignKey(UserInfo, related_name='disputeFor', on_delete=models.SET_NULL, null=True)
    projectID = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    DISPUTE_STATUSES = [
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('awaiting_bids', 'Awaiting Bids'),
    ]
    disputeStatus = models.CharField(max_length=20, choices=DISPUTE_STATUSES, null=True, blank=True)

    # def __str__(self):
    #     return f"Dispute {self.disputeID} - {self.content}"
    class Meta:
        managed = False
        db_table = 'Dispute'







