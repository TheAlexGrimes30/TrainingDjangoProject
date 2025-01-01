from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils.text import slugify


class Fridge(models.Model):
    brand = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(800)])
    slug = models.SlugField(unique=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand + '-' + self.model)
        original_slug = self.slug
        queryset = Fridge.objects.filter(slug=self.slug)
        count = 1
        while queryset.exists():
            self.slug = f"{original_slug}-{count}"
            count += 1
            queryset = Fridge.objects.filter(slug=self.slug)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['brand', 'model']
        indexes = [
            models.Index(["date_created"], name="date_created_index"),
            models.Index(fields=["slug"], name="slug_index"),
        ]
        verbose_name = "fridge"
        verbose_name_plural = "fridges"
        db_table = "fridges"

class FridgeImage(models.Model):
    fridge = models.ForeignKey('Fridge',
                               on_delete=models.CASCADE,
                               related_name='images')
    image = models.ImageField(upload_to='images',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    alt_text = models.CharField(max_length=256, blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Images for {self.fridge.brand} {self.fridge.model}"

    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = f"Images for {self.fridge.brand} {self.fridge.model}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "fridge_image"
        verbose_name_plural = "fridge_images"
        indexes = [
            models.Index(['date_uploaded'], name="date_uploaded_index"),
        ]
        db_table = "fridge_image"
