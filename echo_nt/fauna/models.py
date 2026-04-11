from django.db import models

class Habitat(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Species(models.Model):
    # db_index=True optimizes the database for faster searching (Scalability)
    name = models.CharField(max_length=100, db_index=True)
    scientific_name = models.CharField(max_length=150)
    
    # ManyToMany: A species can have many habitats, a habitat has many species
    habitats = models.ManyToManyField(Habitat, related_name='species')

    def __str__(self):
        return self.name