import asyncio
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
from fastapi_cli.cli import callback
import database as db
from cfg import admins
import keyboard as kb
from Ai3D import generate3d
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiocryptopay import Networks, AioCryptoPay
from aiogram.utils.keyboard import InlineKeyboardBuilder
from cfg import CrypToken

client = AioCryptoPay(token=CrypToken) #if use testnet = network=Networks.TEST_NET


class priceT(StatesGroup):
    num = State()
class startTokens(StatesGroup):
    num = State()
class priceG(StatesGroup):
    num = State()
class numBuyTokens(StatesGroup):
    num = State()


router = Router()

@router.message(CommandStart())
async def start(message:Message):
    await message.answer(text='привет, это бот для генерации 3д моделей из ваших фото',reply_markup=kb.StartKb)
    id = message.from_user.id
    username = message.from_user.username
    token = await db.get_Start_tokens()
    await db.add_to_database_users(telegram_id=id,username=username,tokens=token)


@router.message(Command('admin'))
async def admin(message:Message):
    if message.from_user.id == admins:
        await message.answer(text='привет админ', reply_markup=kb.settings)

@router.callback_query(F.data == 'settings')
async def settings(message: Message):
    await message.answer(text="настройки", reply_markup=kb.settings)

@router.callback_query(F.data == 'price1token')
async def price1token(message: Message, state: FSMContext):
    await state.set_state(priceT.num)
    await message.answer(text='введите цену 100 токеннов')
@router.message(priceT.num)
async def price1token_add(message:Message, state:FSMContext):
    await state.update_data(num=message.text)
    data = await state.get_data()
    await db.add_pricet(data['num'])
    await message.answer(text=f'успешно изменено')
    await state.clear()

@router.callback_query(F.data == 'startTokens')
async def starttokens(message: Message, state: FSMContext):
    await state.set_state(startTokens.num)
    await message.answer(text='введите стартовое количество токенов')
@router.message(startTokens.num)
async def starttokens_add(message:Message, state:FSMContext):
    await state.update_data(num=message.text)
    data = await state.get_data()
    await db.add_startt(data['num'])
    await message.answer(text=f'успешно изменено')
    await state.clear()
@router.callback_query(F.data == 'priceGen')
async def pricegen(message: Message, state: FSMContext):
    await state.set_state(priceG.num)
    await message.answer(text='введите цену 1 генерации')
@router.message(priceG.num)
async def pricegen_add(message:Message, state:FSMContext):
    await state.update_data(num=message.text)
    data = await state.get_data()
    await db.add_priceg(data['num'])
    await message.answer(text=f'успешно изменено')
    await state.clear()



@router.message(F.text == 'профиль')
async def profile(message: Message):
    await db.get_price100()
    name =  message.from_user.username
    idus =  message.from_user.id
    token = await db.get_tokens(id=idus)
    await message.answer(text=f'имя:  {name} \n токены: {token}')



@router.message(F.text == 'покупка токенов')
async def buytoken(message: Message):
    sto = await db.get_price100()
    await message.answer(text=f'выберете количество токенов \n 100 - {sto}$ \n 500 - {sto * 5}$ \n 1000 - {sto * 10}$', reply_markup=kb.numtokens)

@router.callback_query(F.data == '100')
async def buy100(callback1: CallbackQuery):
    await callback1.answer('💵')
    amount = await db.get_price100()
    invoice = await client.create_invoice(asset='USDT', amount=amount)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Ссылка на оплату", url=invoice.bot_invoice_url))
    builder.add(InlineKeyboardButton(text="Проверить оплату", callback_data=f"CHECK1|{invoice.invoice_id}"))
    builder.adjust(1)
    await callback1.message.answer("Оплатите заказ по кнопке ниже", reply_markup=builder.as_markup())
@router.callback_query(F.data.startswith("CHECK1|"))
async def check_invoice100(call1: CallbackQuery):
    invoice_id = int(call1.data.split("|")[1])
    invoice = await client.get_invoices(invoice_ids=invoice_id)
    if invoice.status == "paid":
        await call1.message.delete()
        ID = call1.from_user.id
        await db.add100tokens(ID)
        await call1.message.answer("токены зачислены")  # ! выдача товара
    else:
        await call1.answer("Оплата не обнаружена!")

@router.callback_query(F.data == '500')
async def buy500(callback2: CallbackQuery):
    await callback2.answer('💵')
    amount = await db.get_price100()
    invoice = await client.create_invoice(asset='USDT', amount=amount*5)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Ссылка на оплату", url=invoice.bot_invoice_url))
    builder.add(InlineKeyboardButton(text="Проверить оплату", callback_data=f"CHECK2|{invoice.invoice_id}"))
    builder.adjust(1)
    await callback2.message.answer("Оплатите заказ по кнопке ниже", reply_markup=builder.as_markup())
@router.callback_query(F.data.startswith("CHECK2|"))
async def check_invoice500(call2: CallbackQuery):
    invoice_id = int(call2.data.split("|")[1])
    invoice = await client.get_invoices(invoice_ids=invoice_id)
    if invoice.status == "paid":
        await call2.message.delete()
        ID = call2.from_user.id
        await db.add500tokens(ID)
        await call2.message.answer("токены зачислены")  # ! выдача товара
    else:
        await call2.answer("Оплата не обнаружена!")

@router.callback_query(F.data == '1000')
async def buy1000(callback3: CallbackQuery):
    await callback3.answer('💵')
    amount = await db.get_price100()
    invoice = await client.create_invoice(asset='USDT', amount=amount*10)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Ссылка на оплату", url=invoice.bot_invoice_url))
    builder.add(InlineKeyboardButton(text="Проверить оплату", callback_data=f"CHECK3|{invoice.invoice_id}"))
    builder.adjust(1)
    await callback3.message.answer("Оплатите заказ по кнопке ниже", reply_markup=builder.as_markup())
@router.callback_query(F.data.startswith("CHECK3|"))
async def check_invoice1000(call3: CallbackQuery):
    invoice_id = int(call3.data.split("|")[1])
    invoice = await client.get_invoices(invoice_ids=invoice_id)
    if invoice.status == "paid":
        await call3.message.delete()
        ID = call3.from_user.id
        await db.add1000tokens(ID)
        await call3.message.answer("токены зачислены")  # ! выдача товара
    else:
        await call3.answer("Оплата не обнаружена!")



@router.message(F.text == 'генерация моделей')
async def genanswer(message: Message):
    await message.answer(text='для генерации отправте ваше фото в бота')




@router.message(F.photo)
async def GetPhoto(message:Message):
    tokensuser = await db.get_tokens(message.from_user.id)
    pricegen = await db.get_pricegen()
    if tokensuser >= pricegen:
        await db.buygen(message.from_user.id)
        from run import bot
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path
        save_path = f"userPhoto/{photo.file_id}.jpg"
        await bot.download_file(file_path, save_path)
        tokensuser2 = await db.get_tokens(message.from_user.id)
        await message.answer(text=f'фото загружено ожидайте \n у вас осталось {tokensuser2} токенов')
        path3d = str(await generate3d(save_path))
        filename = FSInputFile(path3d).filename
        await message.answer_document(document=FSInputFile(path3d), caption='ваш файл', reply_markup=await kb.CheckModel(filename))
    else:
        needtokens = pricegen - tokensuser
        await message.answer(text=f'у вас {tokensuser} токенов \n для оплаты не хватает {needtokens} токенов \n вы можете купить их ниже', reply_markup=kb.numtokens)