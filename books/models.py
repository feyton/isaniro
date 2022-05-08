from django.contrib.sites.models import Site
from django.db.models.signals import post_save, pre_save
from autoslug.fields import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from cloudinary.models import CloudinaryField

from books.utils import notify_email, ref_code_generator, sign_book_token
User = get_user_model()
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)


class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    sample = models.FileField(upload_to='books/sample')
    published = models.BooleanField(default=False)
    downloads = models.IntegerField(default=0)
    cover = CloudinaryField('image', null=True)
    slug = AutoSlugField(_('slug'), populate_from='title',
                         unique=True, primary_key=False)
    price = models.PositiveIntegerField(default=0,)
    orders = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    discounted_price = models.PositiveIntegerField(default=0)
    digital = models.BooleanField(default=True)
    downloadable_copy = models.FileField(
        upload_to="secure/books/", blank=True, null=True)

    @property
    def imgURL(self):
        try:
            url = self.cover.url
        except:
            url = ""
        return url

    @property
    def download_link(self):
        try:
            url = self.downloadable_copy.url
        except:
            url = ""
        return url

    @property
    def on_discount(self):
        return self.discounted_price < self.price

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-view", kwargs={"pk": self.pk, 'slug': self.slug})

    def get_cart_url(self):
        return reverse("add-to-cart", kwargs={"pk": self.pk})

    def get_sample_download_link(self):
        return reverse("sample-download", kwargs={"pk": self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.discounted_price:
            self.discounted_price = self.price
        if self.discounted_price > self.price:
            self.discounted_price = self.price
        return super().save(*args, **kwargs)

    def addOrder(self, quantity=1):
        self.orders = self.orders + quantity
        self.save()

    @property
    def discount_percent(self):
        if self.discounted_price < self.price:
            discount = (self.price - self.discounted_price) * 100/self.price
            return int(discount)
        return 0


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, null=False, blank=False)
    ordered_date = models.DateTimeField(auto_now=False, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100, unique=True)
    completed = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)
    notified_customer = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = ref_code_generator()
        return super().save(*args, **kwargs)

    def notify_seller(self):
        print("Notifying seller")
        if not self.notified == True:
            print("Sending emails")
            orderitems = self.orderitem_set.all()
            self.notified = True
            for item in orderitems:
                notify_email("email/to_author.html",
                             item.product.author.email, {"item": item}, "Order received")
            self.save()
            return
        else:
            print("Notifications are already sent")
        return

    def notify_customer(self):
        print("Notifying email to the customer")
        if not self.notified_customer == True:
            print("Sending email")
            notify_email("email/order.html",
                         self.customer.user.email, {"order": self})
            self.notified_customer = True
            self.save()
            return
        else:
            print("Notifications are already sent")
        return


class OrderItem(models.Model):
    product = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    shipped = models.BooleanField(default=False)

    @property
    def get_total(self):
        if self.product.on_discount:
            return self.quantity * self.product.discounted_price
        total = self.product.price * self.quantity
        return total

    def record_order(self):
        self.product.addOrder(self.quantity)

    def __str__(self):
        return "Order for for %s >> %s" % (self.product.title, self.quantity)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Address(models.Model):
    province_choices = [
        ("NORTH", "North"),
        ("SOUTH", "South"),
        ("KIGALI", "Kigali"),
        ("WEST", "West")
    ]
    vicinity_choice = [
        ("Gacuriro", "Gacuriro"),
        ("Yaounde", "Yaounde"),
        ("Kabuga", "Kabuga"),
    ]
    region_choice = [
        ("Gasabo", "Gasabo"),
        ("Kicukiro", "Kicukiro"),
        ("Huye", "Huye"),
        ("Musanze", "Musanze")
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=False)
    telephone = models.CharField(max_length=14, blank=True)
    province = models.CharField(
        max_length=20, choices=province_choices, default="Kigali")
    district = models.CharField(
        max_length=30, default="Gasabo", choices=region_choice)
    vicinity = models.CharField(
        max_length=233, blank=True, choices=vicinity_choice, default='Kabuga')
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s-Address" % self.customer.user.first_name


class BookUser(models.Model):
    email = models.EmailField(unique=True)


class Payment(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=50, default="mobilemoney")
    status = models.CharField(max_length=20)
    payment_id = models.CharField(max_length=100, unique=True)
    currency = models.CharField(max_length=4, default="RWF")
    amount = models.PositiveIntegerField()
    amount_settled = models.PositiveIntegerField()


class PayedBook(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    token = models.TextField()

    @property
    def download_link(self, *args, **kwargs):
        return reverse('book-download', kwargs={'token': self.token})

    def save(self, *args, **kwargs):
        if not self.token:
            data = {
                'book': self.book.id,
                'payment': self.payment.id,
                'customer': self.customer.id,
                'payment_id': self.payment.payment_id
            }
            self.token = sign_book_token(data)
        return super().save(*args, **kwargs)


def provision_book_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print("Created")
        link = "%s%s" % (Site.objects.get_current().domain,
                         instance.download_link)
        data = {'payment': instance, 'link': link}
        notify_email('email/purchased_book.html', instance.customer.user.email, data,
                     message="Thank you for purchase")


post_save.connect(provision_book_receiver, sender=PayedBook)
