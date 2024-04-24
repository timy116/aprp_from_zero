from django.db import models
from django.db.models import Model, DateTimeField, ManyToManyField, ForeignKey, SET_NULL, Q
from django.db.models.fields import CharField, IntegerField, BooleanField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator


class AbstractProduct(Model):
    """
    Abstract classes here as AbstractProduct which inherit from third
    party package model_utils.InheritanceManage, will not work with
    abstract attribute specified true:

        class Meta:
            abstract = True

    For this reason, its subclass will cause create issue when load
    fixtures data by running this command:

        manage.py loaddata <file-name>

    So, we have to remove abstract attribute and add a custom manager

    Note:
    該命令的工作原理如下：
    1. 該命令會讀取指定的文件。該文件必須是 JSON 或 YAML 格式的資料轉儲。
    2. 該命令會解析文件中的資料。
    3. 該命令會根據解析出的資料創建或更新資料庫中的模型實例。
    """
    name = CharField(max_length=50, verbose_name=_('Name'))
    code = CharField(max_length=50, verbose_name=_('Code'))
    config = ForeignKey('configs.Config', null=True, on_delete=SET_NULL, verbose_name=_('Config'))
    type = ForeignKey('configs.Type', null=True, on_delete=SET_NULL, verbose_name=_('Type'))
    unit = ForeignKey('configs.Unit', null=True, blank=True, verbose_name=_('Unit'))
    parent = ForeignKey('self', null=True, blank=True, on_delete=SET_NULL, verbose_name=_('Parent'))
    track_item = BooleanField(default=True, verbose_name=_('Track Item'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    objects = InheritanceManager()

    class Meta:
        verbose_name = _('Abstract Product')
        verbose_name_plural = _('Abstract Products')
        ordering = ('id',)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    @property
    def to_direct(self):
        """
        set true to navigate at front end
        """
        type_level = self.config.type_level
        return self.level >= type_level

    @property
    def level(self):
        level = 1

        lock = False
        product = self

        while not lock:

            if product.parent is not None:
                product = product.parent
                level = level + 1
            else:
                lock = True

        return level

    def children(self):
        """
        如果在 select_subclasses() 方法中指定了子類別，那麼實際上的 SQL 會使用 join。

        e.g.
        products = AbstractProduct.objects.select_subclasses('product').filter(price__gt=100)

        該程式碼將生成以下 SQL 語句：
        SELECT *
        FROM
        `django_content_type` AS `content_type`
        INNER JOIN
        `product` AS `product`
        ON
        `content_type`.`model` = `product`.`content_type_id`
        WHERE
        `product`.`price` > 100

        補充說明:
        如果不指定子類別，那麼 select_subclasses() 方法將包含所有子類別。這將導致 SQL 語句包含多個 JOIN 語句。
        這可能會導致性能問題，因為每個 JOIN 都需要額外的時間。

        如果你在子類別呼叫 select_subclasses() 方法，那麼實際上的 SQL 會使用 join，但只會包含該子類別及其子類別。
        """
        products = AbstractProduct.objects.filter(parent=self).select_subclasses()

        return products.order_by('id')

    def children_all(self):
        q_object = Q()
        parent_attr = 'parent'
        for _ in range(5):
            q_object |= Q(**{parent_attr: self})
            parent_attr += '__parent'

        return AbstractProduct.objects.filter(q_object).select_subclasses().order_by('id')

    @property
    def related_product_ids(self):
        ids = list(self.children().values_list('id', flat=True))

        lock = False
        product = self

        while not lock:
            ids.append(product.id)
            if product.parent is not None:
                product = product.parent
            else:
                lock = True

        return ids


class SourceQuerySet(models.QuerySet):
    """ for case like Source.objects.filter(config=config).filter_by_name(name) """

    def filter_by_name(self, name):
        if not isinstance(name, str):
            raise TypeError('Name must be a string')

        name = name.replace('台', '臺')
        qs = self.filter(name=name)

        if not qs:
            qs = self.filter(alias__icontains=name)

        return qs


class Source(Model):
    """
    單一市場須定義產品種類(Config)及供應種類(Type)，初始化市場資料名稱統一使用臺字。
    """
    name = CharField(max_length=50, verbose_name=_('Name'))
    alias = CharField(max_length=255, null=True, blank=True, verbose_name=_('Alias'))
    code = CharField(max_length=50, null=True, blank=True, verbose_name=_('Code'))
    configs = ManyToManyField('configs.Config', verbose_name=_('Config'))
    type = ForeignKey('configs.Type', null=True, blank=True, on_delete=SET_NULL, verbose_name=_('Type'))
    enable = BooleanField(default=True, verbose_name=_('Enable'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    objects = SourceQuerySet.as_manager()

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')
        ordering = ['id']

    def __str__(self):
        flat = self.configs_flat
        return f'{self.name}({flat}-{self.type.name})'

    def __unicode__(self):
        flat = self.configs_flat
        return f'{self.name}({flat}-{self.type.name})'

    @property
    def simple_name(self):
        return self.name.replace('臺', '台')

    @property
    def configs_flat(self):
        return ','.join([config.name for config in self.configs.all()])

    @property
    def to_direct(self):
        """
        set true to navigate at front end
        """
        return True


class Config(Model):
    """
    產品種類，目前初始化有 crop, fruit, rice...等12種，
    有各自代表的 app(crops, fruits, rices)，也是網頁選單的第一層物件。

    e.g.
    type_level: 在產生選單時，決定 type 要出現在哪一層，預設為 1
    type_level = 1: config -> product -> type -> product -> source
    type_level = 2: config -> product -> product -> type -> product -> source
    """
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    code = CharField(max_length=50, null=True, blank=True, verbose_name=_('Code'))
    charts = models.ManyToManyField('configs.Chart', blank=True, verbose_name=_('Chart'))
    type_level = IntegerField(choices=[(1, 1), (2, 2)], default=1, verbose_name=_('Type Level'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Config')
        verbose_name_plural = _('Configs')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    @property
    def to_direct(self):
        """
        set true to navigate at front end
        """
        return False

    def products(self):
        return AbstractProduct.objects.filter(config=self).select_subclasses().order_by('id')

    def types(self):
        products_qs = self.products().values('type').distinct()
        types_ids = [product['type'] for product in products_qs]
        return Type.objects.filter(id__in=types_ids)


class TypeQuerySet(models.QuerySet):
    """
    TypeQuerySet is a subclass of models.QuerySet.
    It allows us to define custom methods that can be chained with other QuerySet methods.
    """
    pass


class Type(Model):
    """
    供應種類，目前初始化資料有批發、產地、零售。
    """
    name = CharField(max_length=50, unique=True, verbose_name=_('Name'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    objects = TypeQuerySet.as_manager()

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)

    @property
    def to_direct(self):
        """
        set true to navigate at front end
        """
        return True

    def sources(self):
        """取得特定供應種類的市場"""
        return Source.objects.filter(type=self)


class Unit(Model):
    price_unit = CharField(max_length=50, null=True, blank=True, verbose_name=_('Price Unit'))
    volume_unit = CharField(max_length=50, null=True, blank=True, verbose_name=_('Volume Unit'))
    weight_unit = CharField(max_length=50, null=True, blank=True, verbose_name=_('Weight Unit'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')

    def __str__(self):
        return f'{self.price_unit}, {self.volume_unit}, {self.weight_unit}'

    def __unicode__(self):
        return f'{self.price_unit}, {self.volume_unit}, {self.weight_unit}'

    def attr_list(self) -> list:
        """
        Unit._meta:
        This is Django's way of accessing the metadata of the Unit model.
        The _meta attribute is a special attribute provided by Django for this purpose.

        get_field(attr):
        This method is used to retrieve a field instance given a field name.
        The attr variable is expected to be a string that matches the name of a field in the Unit model.

        title():
        This is a Python string method that converts the first character of each word to uppercase and
        the remaining characters to lowercase. It's used here to ensure that the verbose name is in title case.
        """
        return [
            (Unit._meta.get_field(attr).verbose_name.title(), value)
            for attr, value in self.__dict__.items()
            if attr in ['price_unit', 'volume_unit', 'weight_unit'] and value
        ]


class Chart(Model):
    """
    Define the URL for AJAX requests and the path to the JavaScript file for Highcharts setup.
    """

    name = CharField(max_length=120, unique=True, verbose_name=_('Name'))
    code = CharField(max_length=50, unique=True, null=True, verbose_name=_('Code'))
    template_name = CharField(max_length=255, verbose_name=_('Template Name'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Chart')
        verbose_name_plural = _('Charts')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class Month(Model):
    name = CharField(max_length=120, unique=True, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Month')
        verbose_name_plural = _('Months')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class Festival(Model):
    roc_year = CharField(max_length=3, default=timezone.now().year - 1911, verbose_name='ROC Year')
    name = ForeignKey('configs.FestivalName', null=True, blank=True, on_delete=SET_NULL, verbose_name=_('Name'))
    enable = BooleanField(default=True, verbose_name=_('Enabled'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))
    create_time = DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Created'))

    class Meta:
        verbose_name = _('Festival')
        verbose_name_plural = _('Festivals')
        ordering = ('id',)

    def __str__(self):
        return f"{self.roc_year}_{self.name.name}"

    def __unicode__(self):
        return f"{self.roc_year}_{self.name.name}"


class FestivalName(Model):
    name = CharField(max_length=20, unique=True, verbose_name=_('Name'),
                     validators=[MaxLengthValidator(20, message='Name cannot exceed 20 characters')])
    enable = BooleanField(default=True, verbose_name=_('Enabled'))
    lunar_month = CharField(max_length=2, default='01', verbose_name=_('Lunar Month'))
    lunar_day = CharField(max_length=2, default='01', verbose_name=_('Lunar Day'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))
    create_time = DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Created'))

    class Meta:
        verbose_name = _('Festival Name')
        ordering = ('id',)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class FestivalItems(Model):
    name = CharField(max_length=20, verbose_name=_('Name'))
    enable = BooleanField(default=True, verbose_name=_('Enabled'))
    order_sn = IntegerField(default=9, verbose_name=_('Order SN'))
    festival_name = ManyToManyField('configs.FestivalName', verbose_name=_('Festival Name'))
    product_id = ManyToManyField('configs.AbstractProduct', verbose_name=_('Product ID'))
    source = ManyToManyField('configs.Source', verbose_name=_('Source'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))
    create_time = DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Created'))

    class Meta:
        verbose_name = _('Festival Item')
        ordering = ('order_sn',)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)


class Last5YearsItems(Model):
    name = CharField(max_length=60, verbose_name=_('Name'))
    enable = BooleanField(default=True, verbose_name=_('Enabled'))
    product_id = ManyToManyField('configs.AbstractProduct', verbose_name=_('Product ID'))
    source = ManyToManyField('configs.Source', verbose_name=_('Source'))
    update_time = DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Updated'))
    create_time = DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Created'))

    class Meta:
        verbose_name = _('Last5YearsItems')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return str(self.name)
