from django.contrib.auth import get_user_model
from django.db import models
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from recipes.models import RecipeIngredient

User = get_user_model()


def get_shopping_list(user):
    """Создания файла со списком покупок"""
    ingredients = (
        RecipeIngredient.objects.filter(
            recipe__shoppingcart__user=user
        )
        .order_by("ingredient__name")
        .values("ingredient__name", "ingredient__measurement_unit")
        .annotate(amount=models.Sum("amount"))
    )
    shopping_list = "Купить в магазине:"
    for ingredient in ingredients:
        shopping_list += (
            f"\n{ingredient['ingredient__name']} "
            f"({ingredient['ingredient__measurement_unit']}) - "
            f"{ingredient['amount']}"
        )
    # Временный файл PDF в памяти
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    # Добавляем шрифт
    dejavu_file = "fonts/DejaVuSans.ttf"
    dejavu_font = ttfonts.TTFont("DejaVuSans", dejavu_file)
    pdfmetrics.registerFont(dejavu_font)
    # Добавление списка покупок на страницу PDF
    x_offset = 50
    y_offset = letter[1] - 100
    pdf.setFont("DejaVuSans", 12)
    for line in shopping_list.splitlines():
        pdf.drawString(x_offset, y_offset, line)
        y_offset -= 20
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
