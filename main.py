import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from schedule import get_schedule

TOKEN = ""
GROUP_ID = "199"  # По умолчанию для вашего примера

bot = Bot(token=TOKEN)
dp = Dispatcher()


def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Сегодня 📌", callback_data="day_0"))
    builder.row(types.InlineKeyboardButton(text="Завтра ⏭", callback_data="day_1"))
    builder.row(types.InlineKeyboardButton(text="Вся неделя 🗓", callback_data="week"))
    return builder.as_markup()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        f"👋 Привет! Я твой помощник по расписанию ГУЗ.\nГруппа: **{GROUP_ID}**",
        reply_markup=main_menu_kb(),
        parse_mode="Markdown"
    )


@dp.callback_query(F.data.startswith("day_"))
async def show_day(callback: types.CallbackQuery):
    offset = int(callback.data.split("_")[1])
    text = get_schedule(GROUP_ID, day_offset=offset)
    # Добавляем кнопку "Назад", чтобы интерфейс был зациклен
    back_kb = InlineKeyboardBuilder()
    back_kb.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="to_main"))

    await callback.message.edit_text(text, reply_markup=back_kb.as_markup(), parse_mode="Markdown")


@dp.callback_query(F.data == "week")
async def show_week(callback: types.CallbackQuery):
    text = get_schedule(GROUP_ID)
    back_kb = InlineKeyboardBuilder()
    back_kb.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="to_main"))

    await callback.message.edit_text(text, reply_markup=back_kb.as_markup(), parse_mode="Markdown")


@dp.callback_query(F.data == "to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"Выберите период для группы {GROUP_ID}:",
        reply_markup=main_menu_kb()
    )


async def run():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run())
