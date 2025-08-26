from database.utils import db_get_products_from_final_cart


def counting_items(chat_id, user_text):
    products = db_get_products_from_final_cart(chat_id)

    if products:
        text = f'{user_text}\n'
        total_products = total_price = count = 0
        for name, price, quantity, cart_id in products:
            count += 1
            total_products += quantity
            total_price += price * quantity
            text += (f'{count}.{name}.{quantity}.{price}\n')
        text += f'Общее количество:\n{total_products} {total_price}₽'
        context = (count, text, total_price, cart_id)
        return context

    return None
