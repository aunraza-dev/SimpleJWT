from django.db import models

class Plan(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ]

    subscription = models.CharField(max_length=100, choices=SUBSCRIPTION_CHOICES)
    pricingModel = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=250)
    button_text = models.CharField(max_length=100)

    def __str__(self):
        return self.pricingModel
    
    class Meta:
        verbose_name= "Plan"
        verbose_name_plural= "Plan"

class Feature(models.Model):
    plan = models.ForeignKey(Plan, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name= "Feature"
        verbose_name_plural= "Feature"

class ContactUs(models.Model):
    fullName= models.CharField(max_length=50)
    email= models.CharField(max_length=100)
    message= models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.fullName
    
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

class BuyPackage(models.Model):
    email= models.CharField(max_length=100)
    message= models.CharField(max_length=1000)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name= "Buy Package"
        verbose_name_plural = "Buy Package"


