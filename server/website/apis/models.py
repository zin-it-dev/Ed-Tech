from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.contrib import admin
from django.utils.html import mark_safe


class User(AbstractUser):
    """
    Represents a user available in system.
    """

    email = models.EmailField(
        max_length=100,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d/",
        default=None,
        null=True,
        blank=True,
        help_text="Upload avatar of the user",
        storage=MediaCloudinaryStorage(),
    )
    reset_code = models.CharField(max_length=7, null=True, blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-date_joined"]

    @admin.display(description="Preview")
    def avatar_preview(self):
        if self.avatar:
            return mark_safe(
                f'<img src="{self.avatar.url}" alt="{self.username}" width="75" height="75" class="img-thumbnail rounded-circle shadow" />'
            )


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
    """
    Represents a category available in system.
    """

    title = models.CharField(unique=True, max_length=80)

    class Meta(Common.Meta):
        ordering = Common.Meta.ordering + ["title"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Tag(Common):
    """
    Represents a tag available in system.
    """

    title = models.CharField(unique=True, max_length=80)

    def __str__(self):
        return self.title


class Base(Common):
    tags = models.ManyToManyField(
        Tag,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta(Common.Meta):
        abstract = True


class Course(Base):
    """
    Represents a course available in system.
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")

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

    @admin.display(description="Banner")
    def banner(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" alt="{self.title}" title="{self.title}" width="80" height="80" class="img-thumbnail rounded shadow" />'
            )

    def __str__(self):
        return self.title


class Lesson(Base):
    """
    Represents a lesson available in system.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    title = models.CharField(max_length=125)
    content = CKEditor5Field("Text", config_name="extends")

    class Meta(Base.Meta):
        ordering = Base.Meta.ordering + ["id"]
        unique_together = ("course", "title")

    def __str__(self):
        return self.title


class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    url = models.URLField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.url
