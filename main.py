from io import BytesIO
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging
from model import ArtPredictor
import os

token = os.getenv("token")

def answers(preds, n):
    '''
    Функция принимает на вход зип, содержащий предсказания модели, и колличество необходимых нам предсказаний,
    Далее он обрабатывает их и выдает ответы для нашего бота.
    '''
    pred = preds[0:n]
    classes, percents = pred
    answers_ = []
    answers_.append('Я думаю, что это: \n')
    for i in range(n):
        if(round(percents[i].item()) > 0):
            answers_.append(str(i + 1) + ') ' + str(classes[i])+ '\n'+'С шансом: '+str(round(percents[i].item()))+'%')
    return answers_

model = ArtPredictor()

def start(bot, update):

    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Привет! Я бот который умеет определять в стиле какого художника написана картина. "
                         "Просто отправь мне фотку, а дальше я все сделаю сам :)")
start_handler = CommandHandler('start', start)

def info(bot, update):
    '''
    Функция реализует вывод имен всех известных боту художников.
    '''
    classes = ['Albrecht Dürer', 'Alfred Sisley', 'Amedeo Modigliani', 'Andrei Rublev', 'Andy Warhol',
               'Camille Pissarro', 'Caravaggio',
               'Claude Monet', 'Diego Rivera', 'Diego Velazquez', 'Edgar Degas', 'Edouard Manet', 'Edvard Munch',
               'El Greco', 'Eugene Delacroix',
               'Francisco Goya', 'Frida Kahlo', 'Georges Seurat', 'Giotto di Bondone', 'Gustav Klimt',
               'Gustave Courbet', 'Henri Matisse', 'Henri Rousseau',
               'Henri de Toulouse-Lautrec', 'Hieronymus Bosch', 'Jackson Pollock', 'Jan van Eyck', 'Joan Miro',
               'Kazimir Malevich', 'Leonardo da Vinci',
               'Marc Chagall', 'Michelangelo', 'Mikhail Vrubel', 'Pablo Picasso', 'Paul Cezanne', 'Paul Gauguin',
               'Paul Klee', 'Peter Paul Rubens', 'Pierre-Auguste Renoir',
               'Piet Mondrian', 'Pieter Bruegel', 'Raphael', 'Rembrandt', 'Rene Magritte', 'Salvador Dali',
               'Sandro Botticelli', 'Titian', 'Vasiliy Kandinskiy', 'Vincent van Gogh', 'William Turner']
    answer = ''
    for clas in classes:
        answer += clas + '\n'
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Я знаю таких художников, как: \n" + answer)
info_handler = CommandHandler('info', info)

def send_prediction_on_photo(bot, update):
    '''
    Функция реализует ответ бота на полученную картинку.
    '''
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    image_stream = BytesIO()
    image_file.download(out=image_stream)
    # получение предсказаний модели
    preds = model.predict(image_stream)
    # кол-во предсказаний на выходе
    count_of_pred = 5
    # Получаем ответы для бота
    answered = answers(preds, count_of_pred)
    # теперь отправим результат
    out = ''
    for i in range(len(answered)):
        out += answered[i] + '\n'
    update.message.reply_text(out)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    updater = Updater(token=token)

    updater.dispatcher.add_handler(MessageHandler(Filters.photo, send_prediction_on_photo))
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(info_handler)
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("name")
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=token)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, token))
    updater.idle()
