from django.db import models 
import uuid

class FormData(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=200)
    phone_no = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    role = models.CharField(max_length=50, default='user')

    def __str__(self):
        return f"{self.user_id} - {self.email} - {self.password}"
    
class FormDataDetails(models.Model):
    user_id = models.ForeignKey(FormData, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.image}"