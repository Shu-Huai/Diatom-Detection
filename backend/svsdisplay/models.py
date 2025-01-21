from django.db import models


class DiatomSlice(models.Model):
    image = models.ImageField(upload_to='diatom_slices/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description or f"Slice {self.id}"


class DiatomPatch(models.Model):
    image = models.ImageField(upload_to='diatom_patches/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description or f"Patch {self.id}"
