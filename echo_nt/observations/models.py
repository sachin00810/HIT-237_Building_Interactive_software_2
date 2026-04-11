from django.db import models
from django.contrib.auth.models import User
from fauna.models import Species
from django.utils import timezone
import datetime

class Observation(models.Model):
    # ForeignKey: One-to-Many relationships
    # related_name optimizes reverse queries for scalability
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='observations')
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='observations')
    
    # db_index=True speeds up time-based filtering
    date_spotted = models.DateTimeField(default=timezone.now, db_index=True)
    notes = models.TextField()

    # Business Logic inside the Model (Fulfills: Encapsulation / Fat Models)
    def is_recent(self):
        """Returns True if the observation was made within the last 7 days."""
        return self.date_spotted >= timezone.now() - datetime.timedelta(days=7)

    def __str__(self):
        return f"{self.species.name} spotted by {self.user.username}"