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


class Invoice(models.Model):
    invoiceID = models.AutoField(primary_key=True)
    projectID = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    clientUserID = models.ForeignKey(UserInfo,related_name='clientID', on_delete=models.SET_NULL, null=True)
    paymentID = models.PositiveIntegerField(null=True)
    freelancerUserID = models.ForeignKey(UserInfo,related_name='freelancerID', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'Invoice'







class Dispute(models.Model):
    disputeID = models.AutoField(primary_key=True)
    date = models.DateTimeField(null=True)
    DISPUTE_TYPES = [
        ('payment_issues', 'Payment Issues'),
        ('non-payment', 'Non-Payment'),
        ('service_issues', 'Service Issues'),
        ('non-performance', 'Non-Performance'),
        ('fraud', 'Fraud'),
    ]
    type = models.CharField(max_length=15, choices=DISPUTE_TYPES, null=True)
    content = models.CharField(max_length=255, null=True)
    fromUserID = models.ForeignKey(UserInfo, related_name='from_user', on_delete=models.SET_NULL, null=True)
    toUserID = models.ForeignKey(UserInfo, related_name='to_user', on_delete=models.SET_NULL, null=True)
    projectID = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    DISPUTE_STATUSES = [
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('awaiting_bids', 'Awaiting Bids'),
    ]
    disputeStatus = models.CharField(max_length=15, choices=DISPUTE_STATUSES, null=True)

    class Meta:
        managed = False
        db_table = 'Dispute'





class Message(models.Model):
    messageID = models.AutoField(primary_key=True)
    fromUserID = models.ForeignKey(UserInfo, related_name='sender', on_delete=models.SET_NULL, null=True)
    toUserID = models.ForeignKey(UserInfo, related_name='receiver', on_delete=models.SET_NULL, null=True)
    projectID = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=150, null=True)
    type = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'Message'



class Payment(models.Model):
    paymentID = models.AutoField(primary_key=True)
    payerID = models.ForeignKey(UserInfo, related_name='payer', on_delete=models.SET_NULL, null=True)
    payeeID = models.ForeignKey(UserInfo, related_name='payee', on_delete=models.SET_NULL, null=True)
    projectID = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    PAYMENT_TYPES = [
        ('offline', 'Offline'),
        ('online', 'Online'),
    ]

    type = models.CharField(max_length=7, choices=PAYMENT_TYPES, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'Payment'



class Profile(models.Model):
    profileID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20, null=True)
    lastName = models.CharField(max_length=20, null=True)
    PROFILE_TYPES = [
        ('admin', 'Admin'),
        ('normal', 'Normal'),
    ]
    profileType = models.CharField(max_length=6, choices=PROFILE_TYPES, null=True)
    profilePicture = models.CharField(max_length=255, null=True)
    bio = models.CharField(max_length=255, null=True)

    class Meta:
        managed = False
        db_table = 'Profile'






class QA(models.Model):
    QAID = models.AutoField(primary_key=True)
    projectID = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    userID = models.ForeignKey(UserInfo, on_delete=models.SET_NULL, null=True)
    questionContent = models.CharField(max_length=255, null=True)
    answerContent = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(null=True)
    class Meta:
        managed = False
        db_table = 'QA'


from django.db import models

class Rating(models.Model):
    ratingID = models.AutoField(primary_key=True)
    ratedUserID = models.ForeignKey(UserInfo, related_name='rated_user', on_delete=models.SET_NULL, null=True)
    ratingByUserID = models.ForeignKey(UserInfo, related_name='rated_by_user', on_delete=models.SET_NULL, null=True)
    
    RATINGS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    
    rating = models.CharField(max_length=1, choices=RATINGS, null=True)
    comment = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'Rating'




class Shipping(models.Model):
    shippingID = models.AutoField(primary_key=True)
    projectID = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    trackingNumber = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(null=True)
    class Meta:
        managed = False
        db_table = 'Shipping'
