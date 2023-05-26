from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Tag(models.Model):
    """Модель тегов для рецептов."""

    name = models.CharField(
        'Название',
        max_length=50,
        unique=True
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        'Адрес',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиентов для рецептов."""

    name = models.CharField(
        'Название',
        max_length=50
    )
    amount = models.IntegerField(
        'Количество'
    )
    unit = models.CharField(
        'Единица измерения',
        max_length=50
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} - {self.amount}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название',
        max_length=50
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/'
    )
    description = models.TextField(
        'Описание'
    )
    # through='RecipeIngredient'
    Ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовдения в минутах',
        validators=[
            MinValueValidator(
                1, message='Минимальное время приготовления - 1 минута.'
            ),
            MaxValueValidator(
                360, message='Максимальное время приготовления - 6 часов.'
            )
        ]
    )
    created = models.DateTimeField(
        'Время создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
