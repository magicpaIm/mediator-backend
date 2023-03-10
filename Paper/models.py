import django.db
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from Paper.helper import publisher_logo_path, journal_resource_path, submit_upload_path, censor_file_path, exchange_attachment_path
from django.apps import apps
from Account.services.NotificationService import NotificationService
from django.db.models import Q


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class ReviewType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    json = models.JSONField(null=True)
    description = models.TextField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=12, unique=True)
    description = models.CharField(max_length=255)


class Country(models.Model):
    iso = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=80, unique=True)
    nice_name = models.CharField(max_length=80)
    iso3 = models.CharField(max_length=3, null=True)
    num_code = models.IntegerField(null=True)
    phone_code = models.SmallIntegerField(null=True)


class Frequency(models.Model):
    name = models.CharField(max_length=12, unique=True)
    description = models.CharField(max_length=255)


class Language(models.Model):
    name = models.CharField(max_length=192, null=True)
    code = models.CharField(max_length=192, unique=True)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=12)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Publisher(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)
    name_translate = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    description_translate = models.TextField(null=True)
    logo_url = models.ImageField(upload_to=publisher_logo_path, null=True)
    site_address = models.URLField(null=True)

    def __str__(self):
        return self.name_translate


class JournalCategory(models.Model):
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE, related_name='journal_category')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_journal')


class JournalLanguage(models.Model):
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE, related_name='journal_country')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, related_name='journal_language')


class JournalProductType(models.Model):
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE, related_name='journal_product')
    product = models.ForeignKey('ProductType', on_delete=models.CASCADE, related_name='product_journal')


class Journal(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    logo_url = models.ImageField(null=True, upload_to=journal_resource_path, max_length=1024)
    issn = models.CharField(max_length=255, null=True)
    eissn = models.CharField(max_length=255, null=True)
    review_type = models.ForeignKey(ReviewType, on_delete=models.DO_NOTHING, related_name='journal_review_method',  null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING, related_name='journal_publisher', null=True)
    frequency = models.ForeignKey(Frequency, on_delete=models.DO_NOTHING, related_name='journal_frequency', null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name='journal_country', null=True)
    guide_url = models.FileField(null=True, upload_to=journal_resource_path, max_length=1024)
    url = models.URLField(null=True)
    start_year = models.SmallIntegerField(default=1990)
    impact_factor = models.FloatField(default=0.0)
    open_access = models.IntegerField(null=True)
    flag = models.BooleanField(default=False)
    issues_per_year = models.SmallIntegerField(null=True)
    languages = models.ManyToManyField(
        Language,
        through='JournalLanguage',
        through_fields=('journal', 'language'),
        blank=True,
    )

    products = models.ManyToManyField(
        ProductType,
        through='JournalProductType',
        through_fields=('journal', 'product'),
        blank=True,
    )

    categories = models.ManyToManyField(
        Category,
        through='JournalCategory',
        through_fields=('journal', 'category'),
        blank=True,
    )

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")

    def __str__(self):
        return self.name

    def assign_category(self, categories, is_update=True):
        self.categories.clear() if is_update else ''
        for category in categories:
            try:
                category = Category.objects.get(pk=category)
                if not self.categories.filter(pk=category.pk).exists():
                    self.categories.add(category)
            except Category.DoesNotExist:
                pass
        return True

    def assign_product(self, products, is_update=True):
        self.products.clear() if is_update else ''
        for product in products:
            try:
                product = ProductType.objects.get(pk=product)
                if not self.products.filter(pk=product.pk).exists():
                    self.products.add(product)
            except ProductType.DoesNotExist:
                pass
        return True

    def assign_language(self, languages, is_update=True):
        self.languages.clear() if is_update else ''
        for language in languages:
            try:
                language = Language.objects.get(pk=language)
                if not self.languages.filter(pk=language.pk).exists():
                    self.languages.add(language)
            except Language.DoesNotExist:
                pass
        return True


class Status(models.Model):
    class StatusType(models.TextChoices):
        SUBMISSION = 'submission', _('Submission')
        REQUEST = 'request', _('Request')
        RESOURCE_UPLOAD = 'resource upload', _('Resource Upload')
        EXCHANGE = 'exchange', _('Exchange')
    type = models.CharField(max_length=64, choices=StatusType.choices, default=StatusType.SUBMISSION, )
    name = models.CharField(max_length=255, unique=True)
    codename = models.CharField(max_length=255, unique=True, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Requirement(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    file_type = models.CharField(max_length=192, null=True)

    def __str__(self):
        return self.name


class Order(TimeStampMixin):    
    type = models.ForeignKey('Account.BusinessType', on_delete=models.CASCADE, related_name='order_type', null=True)
    user = models.ForeignKey('Account.User', on_delete=models.CASCADE, related_name='order_user')
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='order_status', null=True)
    product = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    status_logs = models.ManyToManyField(
        Status,
        through='OrderStatusLog',
        through_fields=('order', 'status'),
        blank=True,
    )
    download_at = models.DateTimeField(null=True)
    censor_input_info = models.JSONField(null=True)
    censor_output_info = models.JSONField(null=True)
    censor_document = models.CharField(max_length=255, null=True)
    censor_file = models.FileField(upload_to=censor_file_path, null=True)
    is_censor_download = models.BooleanField(default=False)


class OrderStatusLog(TimeStampMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)

    class Meta:
        unique_together = ('order', 'status',)


class Submit(TimeStampMixin):
    order = GenericRelation(Order, related_query_name='order_submit')
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name='submit_article', null=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField(null=True)
    keywords = models.TextField(null=True)
    major = models.TextField(null=True)
    user = models.ForeignKey('Account.User', on_delete=models.DO_NOTHING, related_name='submit_user', null=True)
    dealer = models.ForeignKey('Account.User', on_delete=models.DO_NOTHING, related_name='submit_dealer', null=True)
    journal = models.ForeignKey(Journal, on_delete=models.DO_NOTHING, related_name='submit_journal', null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, related_name='submit_status', null=True)

    def get_upload_files(self):
        return UploadFile.objects.filter(submit=self)

    def set_upload_files(self, files, require_ids):
        index = 0
        error = []
        for file in files:
            try:
                m_file = UploadFile()
                m_file.file = file
                m_file.name = str(file)
                m_file.submit = self
                m_file.requirement = Requirement.objects.get(pk=require_ids[index])
                if UploadFile.objects.filter(submit=self, requirement=m_file.requirement).exists():
                    UploadFile.objects.filter(submit=self, requirement=m_file.requirement).delete()
                m_file.save()
                index += 1
            except Requirement.DoesNotExist:
                print('incorrect requirement id')
                error.append('incorrect requirement id')
                continue
            except django.db.DatabaseError:
                print(' duplicated id')
                error.append('duplicated')

        return True

    def get_authors(self):
        return Author.objects.filter(submit=self)

    def set_authors(self, authors):
        import Paper.serializers
        errors = []
        try:
            for author in authors:
                author['type'] = 'author'
                try:
                    serializer = Paper.serializers.AuthorSerializer(data=author)
                    if serializer.is_valid():
                        serializer.save()
                        serializer.instance.submit = self
                        serializer.instance.save()
                        if Country.objects.filter(id=author.get('country_id')).exists():
                            serializer.instance.country = Country.objects.get(pk=author.get('country_id'))
                            serializer.instance.save()
                    else:
                        errors.append(serializer.errors)
                        continue
                    pass
                except django.db.DatabaseError as e:
                    print(e)
                    continue
        except Exception as e:
            print('add author to submit', e)
            return errors
        return errors

    def set_order(self) -> Order:
        try:
            if Order.objects.filter(order_submit=self).exists():
                return Order.objects.get(order_submit=self)
            else:
                order = Order()
                order.type = apps.get_model('Account.BusinessType').objects.get(codename='paper')
                order.user = self.user
                order.status = self.status
                order.product = self
                order.save()
                order.status_logs.add(self.status,  through_defaults={'message': f"Submission has been created by {self.user.real_name}"})
                return order
        except Exception as e:
            print('set order error on submission', e)
            return Order()

    def update_status(self, status, message=None):
        try:
            self.status = status
            order = self.set_order()
            prev_status = order.status
            order.status = status
            order.status_logs.add(self.status, through_defaults={'message': message})
            order.save()
            self.save()
            notify_msg = {
                'type': 'submission',
                'data': {
                    'order_id': order.id,
                    'previous_status': prev_status.name if prev_status else '',
                    'current_status': status.name if status else '',
                }
            }
            if self.dealer:
                users = apps.get_model('Account.User').objects.filter(
                    Q(id=self.dealer.id) | Q(id=order.user.id) | Q(is_superuser=True))
            else:
                users = apps.get_model('Account.User').objects.filter(
                    Q(role__permissions__codename='manage_paper') | Q(id=order.user.id) | Q(is_superuser=True))
            notification = NotificationService()
            for user in users.distinct():
                notification.set_user(user)
                notification.notify(notify_msg)
        except Exception as e:
            print('---------', e)
            return False

    def get_status_logs(self):
        order = self.set_order()
        return OrderStatusLog.objects.filter(order=order)


class UploadFile(TimeStampMixin):
    name = models.CharField(max_length=255)
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='submit_upload_paper_type')
    file = models.FileField(upload_to=submit_upload_path)
    submit = models.ForeignKey(Submit, on_delete=models.CASCADE, related_name='submit_upload_file', null=True)

    class Meta:
        unique_together = ('requirement', 'submit',)

    def __str__(self):
        return str(self.file)


class Resource(TimeStampMixin):
    order = GenericRelation(Order, related_query_name='order_resource')
    is_upload = models.BooleanField(default=True)
    is_allow = models.BooleanField(default=False)
    title = models.CharField(max_length=255, null=True)
    detail = models.TextField(null=True)    
    dealer = models.ForeignKey('Account.User', on_delete=models.DO_NOTHING, related_name='resource_dealer', null=True)
    flag = models.BooleanField(default=False)
    
    def get_upload_files(self):
        UpFile = apps.get_model('Contest.UploadFile')
        return UpFile.objects.filter(resource=self)

    def set_upload_files(self, files):
        index = 0
        error = []
        for file in files:
            try:
                UpFile = apps.get_model('Contest.UploadFile')
                m_file = UpFile()
                m_file.file = file
                m_file.name = str(file)
                m_file.resource = self
                m_file.save()
                index += 1
            except Exception as e:                
                return False
        return True

    def get_order(self):
        if Order.objects.filter(order_resource=self).exists():
            return Order.objects.get(order_resource=self)
        else:
            return None

    def set_order(self, user=None, status=None, business_type=None):
        try:
            if Order.objects.filter(order_resource=self).exists():
                return Order.objects.get(order_resource=self)
            else:
                order = Order()                
                order.user = user
                order.status = status
                order.product = self
                order.type = business_type
                order.save()
                return order        
        except Exception as e:
            print(e)
            return False
        
    def update_status(self, status, message=None):
        try:
            self.status = status
            order = self.set_order()
            prev_status = order.status
            order.status = status
            order.status_logs.add(self.status, through_defaults={'message': message})
            order.save()
            self.save()
            notify_msg = {
                'type': 'request',
                'data': {
                    'order_id': order.id,
                    'previous_status': prev_status.name if prev_status else '',
                    'current_status': status.name if status else '',
                }
            }
            if self.dealer:
                users = apps.get_model('Account.User').objects.filter(Q(id=self.dealer.id) | Q(id=order.user.id) | Q(is_superuser=True))
            else:
                users = apps.get_model('Account.User').objects.filter(Q(role__permissions__codename='manage_request') | Q(id=order.user.id) | Q(is_superuser=True))
            notification = NotificationService()
            for user in users.distinct():
                notification.set_user(user)
                notification.notify(notify_msg)
        except Exception as e:
            print('---------', e)
            return False

    def get_status_logs(self):
        order = self.set_order()
        return OrderStatusLog.objects.filter(order=order).order_by('-created_at')        


class Author(TimeStampMixin):
    class Appellation(models.TextChoices):
        DOCTOR = 'Dr', _('Doctor')
        MR = 'Mr', _('Mr')
        MRS = 'Mrs', _('Mrs')
        MISS = 'Miss', _('Miss')
        PROFESSOR = 'Professor', _('professor')

    class AuthorType(models.TextChoices):
        AUTHOR = 'author', _('Author')
        REVIEWER = 'reviewer', _('Reviewer')

    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=255, null=True)
    submit = models.ForeignKey(Submit, on_delete=models.CASCADE, related_name='submit_author', null=True)
    type = models.CharField(max_length=12, choices=AuthorType.choices, default=AuthorType.AUTHOR, )
    appellation = models.CharField(max_length=12,
                                   choices=Appellation.choices,
                                   default=Appellation.MR,)


class Exchange(TimeStampMixin):
    order = GenericRelation(Order, related_query_name='order_exchange')
    is_upload = models.BooleanField(default=True)
    title = models.CharField(max_length=255, null=True)
    purpose = models.CharField(max_length=255, null=True)
    site_url = models.CharField(max_length=255, null=True)
    additional_info = models.JSONField(null=True)
    detail = models.TextField(null=True)
    dealer = models.ForeignKey('Account.User', on_delete=models.DO_NOTHING, related_name='exchange_dealer', null=True)
    attachment = models.FileField(null=True, upload_to=exchange_attachment_path, max_length=1024)
    data_identifier = models.IntegerField(null=True)
    outer_username = models.CharField(max_length=255, null=True)
    outer_dealer_name = models.CharField(max_length=255, null=True)
    outer_dealer_real_name = models.CharField(max_length=255, null=True)
    input_size = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    input_count = models.PositiveIntegerField(null=True)

    def get_order(self):
        if Order.objects.filter(order_exchange=self).exists():
            return Order.objects.get(order_exchange=self)
        else:
            return None

    def set_order(self, user=None, status=None):
        try:
            if Order.objects.filter(order_exchange=self).exists():
                return Order.objects.get(order_exchange=self)
            else:
                order = Order()
                order.user = user
                order.status = status
                order.product = self
                order.save()
                return order
        except Exception as e:
            print(e)
            return False

    def update_status(self, status, message=None):
        try:
            self.status = status
            order = self.set_order()
            prev_status = order.status
            order.status = status
            order.status_logs.add(self.status, through_defaults={'message': message})
            order.save()
            self.save()
            notify_msg = {
                'type': 'exchange',
                'data': {
                    'order_id': order.id,
                    'previous_status': prev_status.name if prev_status else '',
                    'current_status': status.name if status else '',
                }
            }
            if self.dealer:
                users = apps.get_model('Account.User').objects.filter(
                    Q(id=self.dealer.id) | Q(id=order.user.id) | Q(is_superuser=True) |
                    Q(role__permissions__codename__in=['manage_exchange', 'manage_exchange_status']))
            else:
                users = apps.get_model('Account.User').objects.filter(
                    Q(role__permissions__codename__in=['manage_exchange', 'manage_exchange_status', 'collect_exchange']) |
                    Q(id=order.user.id) | Q(is_superuser=True))
            notification = NotificationService()
            for user in users.distinct():
                notification.set_user(user)
                notification.notify(notify_msg)
        except Exception as e:
            print('---------', e)
            return False

    def get_status_logs(self):
        order = self.set_order()
        return OrderStatusLog.objects.filter(order=order).order_by('-created_at')
