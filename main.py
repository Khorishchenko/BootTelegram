import config
import logging
import aiogram
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.contrib.middlewares.logging import LoggingMiddleware 


# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# prices
PRICE = types.LabeledPrice(label="Оплата Курсу", amount=10*100)

channel_names = ['https://t.me/Kh_Sergii']
channel_invite_link = 'https://t.me/+Jzbl7JEEXZgzN2My'  # Замініть на посилання на ваш канал


# ===================================================================
# VERSIO 1.0

# # buy
# @dp.message_handler(commands=['start'])
# async def buy(message: types.Message):
#     if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
#         await bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}, ....')

#     await bot.send_invoice(message.chat.id,
#                            title="Оплата Курсу",
#                            description="Після Оплати вам буде надіслано посилання до закритого каналу з курсом.",
#                            provider_token=config.PAYMENTS_TOKEN,
#                            currency="UAH",
#                            photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
#                            photo_width=416,
#                            photo_height=234,
#                            photo_size=416,
#                            is_flexible=False,
#                            prices=[PRICE],
#                            start_parameter="one-month-subscription",
#                            payload="test-invoice-payload")


# # pre checkout  (must be answered in 10 seconds)
# @dp.pre_checkout_query_handler(lambda query: True)
# async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# # successful payment
# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
# async def successful_payment(message: types.Message):
#     user_id = message.from_user.id
#     total_amount = message.successful_payment.total_amount
#     currency = message.successful_payment.currency

#     try:
#         await bot.send_message(user_id, f"Платіж у сумі {total_amount // 100} {currency} пройшов успішно!!!")

#         # Відправте запит на додавання користувача до каналу за посиланням
#         invite_link = f"https://t.me/+VZ0RzJ4yzahiZjMy"  # Генеруємо посилання на канал
#         await bot.send_message(user_id,
#                                f"{message.from_user.first_name} Перейдіть за посиланням та надішли запит для вступу: {invite_link}")
#         await message.answer("Запрошення до каналу було надіслано!")

#         my_user_id = 482266948

#         # Надішліть посилання на профіль користувача
#         username = message.from_user.username
#         if username:
#             profile_link = f"[@{username}](https://t.me/{username})"
#         else:
#             profile_link = "Користувач без ім'я користувача"
#         await bot.send_message(my_user_id,
#                                f"{message.from_user.first_name} {message.from_user.last_name}.\nПосилання на профіль: {profile_link}\n"
#                                f"ID: {message.from_user.id}\n[>Виконав оплату Курсу_NameCurs<]")


#     except Exception as e:
#         logging.exception("Помилка після успішного платежу", e)
#         await bot.send_message(user_id, "Виникла помилка після успішного платежу. Спробуйте пізніше.")


# @dp.message_handler(commands=['help'])
# async def main(message: types.Message):
#     markup = types.InlineKeyboardMarkup()
#     await bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} '
#                                             f'для отримання консультації, перейди за посиланням до чату {channel_names}', reply_markup=markup)

# # run long-polling
# if __name__ == "__main__":
#     executor.start_polling(dp, skip_updates=False)




# ===================================================================
# VERSIO 2.0
#
@dp.message_handler(commands=['start'])
async def buy(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Оплата Курса', callback_data='oplata'))
    markup.add(types.InlineKeyboardButton('Допомога', callback_data='help'))
    await bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name} {message.from_user.last_name}, '
                                            f'Після оплати надішли скірн/або квитанції оплати у форматі фото.', reply_markup=markup)

@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    user_id = message.from_user.id

    try:
        await bot.send_message(user_id, f"Платіж у сумі 10 пройшов успішно !" )

        # Відправте запит на додавання користувача до каналу за посиланням
        invite_link = f"https://t.me/+VZ0RzJ4yzahiZjMy"  # Генеруємо посилання на канал
        await bot.send_message(user_id,
                               f"{message.from_user.first_name} Перейдіть за посиланням та надішли запит для вступу: {invite_link}")
        await message.answer("Запрошення до каналу було надіслано!")

        my_user_id = 482266948

        # Надішліть посилання на профіль користувача
        username = message.from_user.username
        if username:
            profile_link = f"[@{username}](https://t.me/{username})"
        else:
            profile_link = "Користувач без ім'я користувача"
        await bot.send_message(my_user_id,
                               f"{message.from_user.first_name} {message.from_user.last_name}.\nПосилання на профіль: {profile_link}\n"
                               f"ID: {message.from_user.id}\n[>Виконав оплату Курсу_NameCurs<]")

        # Отримайте фотографію користувача
        photo = message.photo[-1]  # Останнє (найвища якість) зображення зі списку

        # Надішліть цю фотографію іншому користувачеві
        await bot.send_photo(chat_id=my_user_id, photo=photo.file_id)


    except Exception as e:
        logging.exception("Помилка після успішного платежу", e)
        await bot.send_message(user_id, "Виникла помилка після успішного платежу. Спробуйте пізніше.")


@dp.callback_query_handler(lambda call: call.data == 'oplata')
async def callback_handler(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, 'Для оплати, перейдіть за посиланням: https://prt.mn/JI2LuB7lU');


@dp.callback_query_handler(lambda call: call.data == 'help')
async def callback_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    user_id = message.from_user.id
    await bot.send_message(user_id, f'Привіт, {message.from_user.first_name} '
                                            f'для отримання консультації, перейди за посиланням до чату {channel_names}',
                           reply_markup=markup)

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)