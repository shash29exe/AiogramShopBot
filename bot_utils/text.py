def text_for_caption(name, description, price):
    """
        Текст для изображения
    """

    return f'<b>{name}</b>\n{description}\n{price:.2f}₽'

def gen_cart_text(cart_items):
    if not cart_items:
        return "Ваша корзина пуста."

    text = "Ваша корзина:\n"
    total = 0.0

    for item in cart_items:
        name = item.get("product_name", "без названия")
        quantity = item.get("quantity", 0)
        total_price = item.get("total_price", 0)

        try:
            subtotal = float(total_price)
        except (TypeError, ValueError):
            subtotal = 0.0

        total += subtotal
        text += f"{name} ({quantity} шт.): {subtotal:.2f} ₽\n"

    text += f"\nИтого: {total:.2f} ₽"
    return text
