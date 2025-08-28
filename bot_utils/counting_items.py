from database.utils import db_get_products_from_final_cart


def counting_items(chat_id, user_text):
    """
        Подсчет товаров в корзине и формирование текста для менеджера
    """
    products = db_get_products_from_final_cart(chat_id)
    if not products:
        return None

    text_lines = [f'{user_text}\n']
    total_products = total_price = count = 0
    cart_id = None

    for name, quantity, price, cart_id_item in products:
        count += 1
        total_products += quantity
        total_price += price
        cart_id = cart_id_item
        text_lines.append(f'{count}. {name}\nКоличество: {quantity}\nЦена за ед.: {price}₽\n')

    text_lines.append(f'Общее количество товаров: {total_products}\nОбщая стоимость: {total_price}₽')
    text = "\n".join(text_lines)

    return count, text, total_price, cart_id
