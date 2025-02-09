from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary_storage.storage import MediaCloudinaryStorage


class User(AbstractUser):
    pass


class Common(models.Model):
    slug = models.SlugField(
        default="",
        null=False,
        verbose_name="URL",
        help_text="A short label, generally used in URLs.",
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this object should be treated as active. Unselect this instead of deleting objects.",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["slug", "-date_created"]


class Category(Common):
    label = models.CharField(unique=True, max_length=80)

    class Meta(Common.Meta):
        ordering = Common.Meta.ordering + ["label"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.label


class Tag(Common):
    label = models.CharField(unique=True, max_length=80)

    def __str__(self):
        return self.label


class Base(Common):
    tags = models.ManyToManyField(
        Tag,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta(Common.Meta):
        abstract = True


class Course(Base):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=80)
    description = models.TextField()
    image = models.ImageField(
        upload_to="courses/%Y/%m/%d/",
        default=None,
        null=True,
        blank=True,
        help_text="Upload banner of the course",
        storage=MediaCloudinaryStorage(),
    )

    class Meta(Base.Meta):
        unique_together = ("category", "title")

    def __str__(self):
        return self.title


class Chapter(Base):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    title = models.CharField(max_length=125)
    description = models.TextField()

    class Meta(Base.Meta):
        ordering = Base.Meta.ordering + ["id"]
        unique_together = ("course", "title")

    def __str__(self):
        return self.title


class Lesson(Base):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="lessons")

    title = models.CharField(max_length=125)
    video_url = models.URLField(
        blank=True,
        null=True,
    )
    content = CKEditor5Field("Text", config_name="extends")

    class Meta(Base.Meta):
        ordering = Base.Meta.ordering + ["id"]
        unique_together = ("chapter", "title")

    def __str__(self):
        return self.title
