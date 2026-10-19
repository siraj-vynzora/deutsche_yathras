from functools import wraps
from urllib import request

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    BlogForm,
    CategoryForm,
    DestinationForm,
    TestimonialForm,
    TourPackageForm,
)

from .models import (
    Blog,
    BookingEnquiry,
    Category,
    ContactMessage,
    Destination,
    GalleryImage,
    Testimonial,
    TourPackage,
)



# ============================================================
# ADMIN ACCESS DECORATOR
# ============================================================

def admin_required(view_func):

    @wraps(view_func)
    @login_required(login_url="admin-login")
    def wrapper(request, *args, **kwargs):

        if not request.user.is_staff:
            messages.error(
                request,
                "You do not have permission to access the admin dashboard."
            )

            logout(request)

            return redirect("admin_login")

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper


# ============================================================
# ADMIN LOGIN
# ============================================================

def admin_login(request):

    # Already logged in as an admin
    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect("admin_dashboard")

        logout(request)


    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )


        # Required fields
        if not username or not password:

            messages.error(
                request,
                "Username and password are required."
            )

            return render(
                request,
                "authenticate/login.html",
            )


        # Authenticate
        user = authenticate(
            request,
            username=username,
            password=password,
        )


        if user is not None and user.is_staff:

            login(
                request,
                user
            )

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect(
                "admin_dashboard"
            )


        messages.error(
            request,
            "Invalid username, password, or unauthorized access."
        )


    return render(
        request,
        "authenticate/login.html",
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

@admin_required
def admin_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect(
        "admin-login"
    )






# ============================================================
# ADMIN DASHBOARD
# ============================================================

@admin_required
def admin_dashboard(request):

    now = timezone.now()

    month_start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


    # ========================================================
    # STATISTICS
    # ========================================================

    stats = {

        "total_packages":
            TourPackage.objects.count(),

        "total_destinations":
            Destination.objects.count(),

        "total_blogs":
            Blog.objects.count(),

        "blogs_this_month":
            Blog.objects.filter(
                created_at__gte=month_start
            ).count(),

        "total_gallery":
            GalleryImage.objects.count(),

        "total_testimonials":
            Testimonial.objects.count(),

        "total_contacts":
            ContactMessage.objects.count(),

        "total_enquiries":
            BookingEnquiry.objects.count(),
    }


    # ========================================================
    # RECENT DATA
    # ========================================================

    recent_packages = (
        TourPackage.objects
        .order_by("-created_at")[:5]
    )

    recent_destinations = (
        Destination.objects
        .order_by("-created_at")[:5]
    )

    recent_blogs = (
        Blog.objects
        .order_by("-created_at")[:5]
    )

    recent_contacts = (
        ContactMessage.objects
        .order_by("-created_at")[:5]
    )

    recent_enquiries = (
        BookingEnquiry.objects
        .order_by("-created_at")[:5]
    )


    context = {

        "stats": stats,

        "recent_packages":
            recent_packages,

        "recent_destinations":
            recent_destinations,

        "recent_blogs":
            recent_blogs,

        "recent_contacts":
            recent_contacts,

        "recent_enquiries":
            recent_enquiries,
    }


    return render(
        request,
        "admin_pages/dashboard.html",
        context,
    )





# ============================================================
# BLOGS
# ============================================================

@admin_required
def admin_blog_list(request):

    blogs = Paginator(
        Blog.objects.order_by("-created_at"),
        10,
    ).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/blog_list.html",
        {
            "blogs": blogs,
        },
    )


@admin_required
def blog_create(request):

    form = BlogForm(
        request.POST or None,
        request.FILES or None,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Blog created successfully."
        )

        return redirect(
            "admin_blog_list"
        )

    return render(
        request,
        "admin_pages/create_blog.html",
        {
            "form": form,
        },
    )


@admin_required
def blog_update(request, pk):

    blog = get_object_or_404(
        Blog,
        pk=pk,
    )

    form = BlogForm(
        request.POST or None,
        request.FILES or None,
        instance=blog,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Blog updated successfully."
        )

        return redirect(
            "admin_blog_list"
        )

    return render(
        request,
        "admin_pages/create_blog.html",
        {
            "form": form,
            "blog": blog,
        },
    )


@admin_required
def blog_delete(request, pk):

    blog = get_object_or_404(
        Blog,
        pk=pk,
    )

    if request.method == "POST":

        blog.delete()

        messages.success(
            request,
            "Blog deleted successfully."
        )

    return redirect(
        "admin_blog_list"
    )





# ============================================================
# TOUR PACKAGES
# ============================================================

@admin_required
def admin_package_list(request):

    packages = Paginator(
        TourPackage.objects.order_by("-created_at"),
        10,
    ).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/package_list.html",
        {
            "packages": packages,
        },
    )


@admin_required
def package_create(request):

    form = TourPackageForm(
        request.POST or None,
        request.FILES or None,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Tour package created successfully."
        )

        return redirect(
            "admin_package_list"
        )

    return render(
        request,
        "admin_pages/create_package.html",
        {
            "form": form,
        },
    )


@admin_required
def package_update(request, pk):

    package = get_object_or_404(
        TourPackage,
        pk=pk,
    )

    form = TourPackageForm(
        request.POST or None,
        request.FILES or None,
        instance=package,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Tour package updated successfully."
        )

        return redirect(
            "admin_package_list"
        )

    return render(
        request,
        "admin_pages/create_package.html",
        {
            "form": form,
            "package": package,
        },
    )


@admin_required
def package_delete(request, pk):

    package = get_object_or_404(
        TourPackage,
        pk=pk,
    )

    if request.method == "POST":

        package.delete()

        messages.success(
            request,
            "Tour package deleted successfully."
        )

    return redirect(
        "admin_package_list"
    )




# ============================================================
# DESTINATIONS
# ============================================================

@admin_required
def admin_destination_list(request):

    destinations = Paginator(
        Destination.objects.order_by("-created_at"),
        10,
    ).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/destination_list.html",
        {
            "destinations": destinations,
        },
    )


@admin_required
def destination_create(request):

    form = DestinationForm(
        request.POST or None,
        request.FILES or None,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Destination created successfully."
        )

        return redirect(
            "admin_destination_list"
        )

    return render(
        request,
        "admin_pages/create_destination.html",
        {
            "form": form,
        },
    )


@admin_required
def destination_update(request, pk):

    destination = get_object_or_404(
        Destination,
        pk=pk,
    )

    form = DestinationForm(
        request.POST or None,
        request.FILES or None,
        instance=destination,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Destination updated successfully."
        )

        return redirect(
            "admin_destination_list"
        )

    return render(
        request,
        "admin_pages/create_destination.html",
        {
            "form": form,
            "destination": destination,
        },
    )


@admin_required
def destination_delete(request, pk):

    destination = get_object_or_404(
        Destination,
        pk=pk,
    )

    if request.method == "POST":

        destination.delete()

        messages.success(
            request,
            "Destination deleted successfully."
        )

    return redirect(
        "admin_destination_list"
    )





# ============================================================
# GALLERY
# ============================================================

@admin_required
def gallery_images(request):

    categories = (
        Category.objects
        .prefetch_related("images")
        .order_by("name")
    )

    return render(
        request,
        "admin_pages/image_list.html",
        {
            "categories": categories,
        },
    )


@admin_required
def add_image(request):

    categories = Category.objects.order_by(
        "name"
    )

    if request.method == "POST":

        category_id = request.POST.get(
            "category"
        )

        files = request.FILES.getlist(
            "images"
        )

        if not category_id:

            messages.error(
                request,
                "Please select a category."
            )

            return render(
                request,
                "admin_pages/add_image.html",
                {
                    "categories": categories,
                },
            )


        category = get_object_or_404(
            Category,
            pk=category_id,
        )


        if not files:

            messages.error(
                request,
                "Please select at least one image."
            )

            return render(
                request,
                "admin_pages/add_image.html",
                {
                    "categories": categories,
                },
            )


        for image_file in files:

            GalleryImage.objects.create(
                category=category,
                title=image_file.name,
                image=image_file,
            )


        messages.success(
            request,
            "Gallery images uploaded successfully."
        )

        return redirect(
            "list_image"
        )


    return render(
        request,
        "admin_pages/add_image.html",
        {
            "categories": categories,
        },
    )


@admin_required
def delete_image(request, image_id):

    image = get_object_or_404(
        GalleryImage,
        pk=image_id,
    )

    if request.method == "POST":

        image.delete()

        messages.success(
            request,
            "Gallery image deleted successfully."
        )

    return redirect(
        "list_image"
    )





# ============================================================
# CATEGORIES
# ============================================================

@admin_required
def category_list(request):

    categories = Category.objects.order_by(
        Lower("name")
    )

    return render(
        request,
        "admin_pages/category_list.html",
        {
            "categories": categories,
        },
    )


@admin_required
def add_category(request):

    form = CategoryForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Category added successfully."
        )

        return redirect(
            "category_list"
        )

    return render(
        request,
        "admin_pages/add_category.html",
        {
            "form": form,
        },
    )


@admin_required
def update_category(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
    )

    form = CategoryForm(
        request.POST or None,
        instance=category,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Category updated successfully."
        )

        return redirect(
            "category_list"
        )

    return render(
        request,
        "admin_pages/add_category.html",
        {
            "form": form,
            "category": category,
        },
    )


@admin_required
def delete_category(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
    )

    if request.method == "POST":

        category.delete()

        messages.success(
            request,
            "Category deleted successfully."
        )

    return redirect(
        "category_list"
    )






# ============================================================
# TESTIMONIALS
# ============================================================

@admin_required
def testimonial_list(request):

    testimonials = Paginator(
        Testimonial.objects.order_by("-created_at"),
        10,
    ).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/review_list.html",
        {
            "testimonials": testimonials,
        },
    )


@admin_required
def testimonial_create(request):

    form = TestimonialForm(
        request.POST or None,
        request.FILES or None,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Testimonial created successfully."
        )

        return redirect(
            "review_list"
        )

    return render(
        request,
        "admin_pages/create_review.html",
        {
            "form": form,
        },
    )


@admin_required
def testimonial_update(request, pk):

    testimonial = get_object_or_404(
        Testimonial,
        pk=pk,
    )

    form = TestimonialForm(
        request.POST or None,
        request.FILES or None,
        instance=testimonial,
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Testimonial updated successfully."
        )

        return redirect(
            "review_list"
        )

    return render(
        request,
        "admin_pages/create_review.html",
        {
            "form": form,
            "testimonial": testimonial,
        },
    )


@admin_required
def testimonial_delete(request, pk):

    testimonial = get_object_or_404(
        Testimonial,
        pk=pk,
    )

    if request.method == "POST":

        testimonial.delete()

        messages.success(
            request,
            "Testimonial deleted successfully."
        )

    return redirect(
        "review_list"
    )




# ============================================================
# CONTACT MESSAGES
# ============================================================

@admin_required
def view_contacts(request):

    contacts = Paginator(
        ContactMessage.objects.order_by("-created_at"),
        10,
    ).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/view_contacts.html",
        {
            "contacts": contacts,
        },
    )


@admin_required
def delete_contact(request, pk):

    contact = get_object_or_404(
        ContactMessage,
        pk=pk,
    )

    if request.method == "POST":

        contact.delete()

        messages.success(
            request,
            "Contact message deleted successfully."
        )

    return redirect(
        "view_contacts"
    )




# ============================================================
# BOOKING ENQUIRIES
# ============================================================

@admin_required
def admin_enquiry_list(request):

    enquiries = Paginator(
        BookingEnquiry.objects.order_by("-created_at"),
        10,
    ).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/enquiry_list.html",
        {
            "enquiries": enquiries,
        },
    )


@admin_required
def admin_enquiry_delete(request, pk):

    enquiry = get_object_or_404(
        BookingEnquiry,
        pk=pk,
    )

    if request.method == "POST":

        enquiry.delete()

        messages.success(
            request,
            "Booking enquiry deleted successfully."
        )

    return redirect(
        "admin_enquiry_list"
    )



# ---------------------------
# frontend
# -------------------------



def home(request):
    packages = TourPackage.objects.all()[:12]

    destinations = Destination.objects.all()

    gallery_images = (
        GalleryImage.objects
        .select_related("category")
        .order_by("-uploaded_at", "-id")[:5]
    )
    latest_blogs = Blog.objects.order_by(
          "-created_at", "-id"
         )[:3]

    testimonials = Testimonial.objects.all().order_by(
    "-created_at", "-id"
    )
    
    
    context = {
        "packages": packages,
        "destinations": destinations,
        "gallery_images": gallery_images,
        "latest_blogs": latest_blogs,
        "testimonials":testimonials,
    }

    return render(request, "frontend/home.html", context)



def about(request):
    return render(request,"frontend/about.html")

def services(request):
    return render(request, "frontend/services.html")


def blog(request):
    # Get blogs from database
    blog_list = Blog.objects.all()

    # Show 6 blogs per page
    paginator = Paginator(blog_list, 6)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "blogs": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
    }

    return render(
        request,
        "frontend/blog.html",
        context
    )


def blog_detail(request, slug):
    blog_post = get_object_or_404(
        Blog,
        slug=slug
    )

    # Latest blogs excluding current article
    recent_blogs = (
        Blog.objects
        .exclude(pk=blog_post.pk)
        .order_by("-created_at")[:3]
    )

    context = {
        "blog": blog_post,
        "recent_blogs": recent_blogs,
    }

    return render(
        request,
        "frontend/blog_details.html",
        context
    )



def contact(request):
    return render(request, "frontend/contact.html")


from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Category, GalleryImage


def gallery(request):

    # Get selected category ID from URL
    selected_category = request.GET.get("category", "all")

    # Get all categories for filter buttons
    categories = Category.objects.all().order_by("name")

    # Get gallery images from database
    gallery_images = (
        GalleryImage.objects
        .select_related("category")
        .order_by("-uploaded_at", "-id")
    )

    # Filter images by selected category
    if selected_category != "all":

        try:
            category_id = int(selected_category)

            if category_id <= 0:
                raise ValueError

            if categories.filter(id=category_id).exists():

                gallery_images = gallery_images.filter(
                    category_id=category_id
                )

                selected_category = str(category_id)

            else:
                selected_category = "all"

        except (ValueError, TypeError):
            selected_category = "all"

    # Pagination: 9 images per page
    paginator = Paginator(gallery_images, 9)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "gallery_images": page_obj,
        "page_obj": page_obj,
        "selected_category": selected_category,
        "total_images": paginator.count,
    }

    return render(
        request,
        "frontend/gallery.html",
        context
    )



from django.shortcuts import render, get_object_or_404
from .models import TourPackage


def packages(request):
    package_type = request.GET.get("type", "all")

    valid_types = {
        "international",
        "domestic",
        "hot_selling",
    }

    packages_qs = TourPackage.objects.all()

    if package_type in valid_types:
        packages_qs = packages_qs.filter(
            package_type=package_type
        )
    else:
        package_type = "all"

    context = {
        "packages": packages_qs,
        "selected_type": package_type,
    }

    return render(
        request,
        "frontend/packages.html",
        context
    )


def package_detail(request, slug):
    package = get_object_or_404(
        TourPackage,
        slug=slug
    )

    related_packages = (
        TourPackage.objects
        .filter(package_type=package.package_type)
        .exclude(pk=package.pk)[:3]
    )

    context = {
        "package": package,
        "related_packages": related_packages,
    }

    return render(
        request,
        "frontend/package-detail.html",
        context
    )



from django.shortcuts import render, get_object_or_404
from .models import Destination


def destinations(request):
    destination_type = request.GET.get("type", "all")

    valid_types = {
        Destination.DOMESTIC,
        Destination.INTERNATIONAL,
    }

    if destination_type not in valid_types:
        destination_type = "all"

    destination_list = Destination.objects.all()

    if destination_type != "all":
        destination_list = destination_list.filter(
            destination_type=destination_type
        )

    context = {
        "destinations": destination_list,
        "selected_type": destination_type,
        "total_destinations": destination_list.count(),
    }

    return render(
        request,
        "frontend/destinations.html",
        context
    )


def destination_detail(request, slug):
    destination = get_object_or_404(
        Destination,
        slug=slug
    )

    related_destinations = (
        Destination.objects
        .filter(destination_type=destination.destination_type)
        .exclude(pk=destination.pk)[:4]
    )

    context = {
        "destination": destination,
        "related_destinations": related_destinations,
    }

    return render(
        request,
        "frontend/destination_detail.html",
        context
    )


def booking(request):
    return render(request,'frontend/booking.html')


