from django import forms

from .models import (
    Blog,
    Category,
    Destination,
    GalleryImage,
    Testimonial,
    TourPackage,
)


# ============================================================
# TOUR PACKAGE FORM
# ============================================================

class TourPackageForm(forms.ModelForm):

    class Meta:
        model = TourPackage

        fields = [
            "name",
            "description",
            "main_image",
            "duration",
            "price_from",
            "package_type",
            "highlights",
            "inclusions",
        ]


# ============================================================
# DESTINATION FORM
# ============================================================

class DestinationForm(forms.ModelForm):

    class Meta:
        model = Destination

        fields = [
            "name",
            "description",
            "image",
            "location",
            "destination_type",
        ]


# ============================================================
# BLOG FORM
# ============================================================

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog

        fields = [
            "title",
            "description",
            "image",
        ]


# ============================================================
# CATEGORY FORM
# ============================================================

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
        ]


# ============================================================
# GALLERY IMAGE FORM
# ============================================================

class GalleryImageForm(forms.ModelForm):

    class Meta:
        model = GalleryImage

        fields = [
            "category",
            "title",
            "image",
        ]


# ============================================================
# TESTIMONIAL FORM
# ============================================================

class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial

        fields = [
            "name",
            "image",
            "review",
        ]