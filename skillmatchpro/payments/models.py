from django.db import models
from django.contrib.auth.models import User
from project.models import Project,Category,Userinfo

class Payment(models.Model):
    payer = models.ForeignKey(User, related_name="payer_id",on_delete=models.CASCADE)
    payee = models.ForeignKey(User, related_name="payee_id",on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(choices=(('offline', 'Offline'), ('online', 'Online')), max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'Payment'
