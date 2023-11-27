from django.db import models
from userInfo.models import UserInfo, Project

class Dispute(models.Model):
    DISPUTE_TYPES = [
        ('payment_issues', 'Payment Issues'),
        ('non-payment', 'Non-Payment'),
        ('service_issues', 'Service Issues'),
        ('non-performance', 'Non-Performance'),
        ('fraud', 'Fraud'),
    ]

    DISPUTE_STATUSES = [
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('awaiting_bids', 'Awaiting Bids'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=DISPUTE_TYPES)
    content = models.CharField(max_length=255)
    from_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='from_user_disputes',db_column='fromUserID')
    to_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='to_user_disputes',db_column='toUserID')
    project = models.ForeignKey(Project, on_delete=models.CASCADE,db_column='projectID')
    dispute_status = models.CharField(max_length=20, choices=DISPUTE_STATUSES,db_column='disputeStatus')

    def __str__(self):
        return f"Dispute #{self.id} - {self.type}"
    
    class Meta:
        db_table = 'Dispute'
