from django.db import models

class User(models.Model):
	username=models.CharField(max_length=200,primary_key=True)
	password=models.CharField(max_length=200)
	user_type=models.IntegerField(default=0)
# Create your models here.
class Issue(models.Model):
	issues=(("Food","Food"),("House Keeping","House Keeping"),("Electrical","Electrical"))
	type_issue=models.CharField(max_length=200,choices=issues)
	complainer=models.ForeignKey(User,related_name='issuer')
	issue=models.CharField(max_length=1000)
	issue_open_date=models.DateTimeField()
	issue_close_date=models.DateTimeField()
	issue_user_close=models.IntegerField(default=0)
	issue_maintenance_close=models.IntegerField(default=0)
