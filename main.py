from io import BytesIO
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging
from model import ArtPredictor
import os
token = os.getenv("token")

reply_text= {
    'pred_answer': 'I predicted class with index {}. To show class name you will need to extract it from' +
                   'dataloader you used while training'
}

model = ArtPredictor()

def start(bot, update):

    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Привет! Я бот который умеет определять в стиле какого художника написана картина. "
                         "Просто отправь мне фотку, а дальше я все сделаю сам :)")
start_handler = CommandHandler('start', start)

def info(bot, update):
    classes = ['Albrecht_Dürer', 'Alfred_Sisley', 'Amedeo_Modigliani', 'Andrei_Rublev', 'Andy_Warhol',
               'Camille_Pissarro', 'Caravaggio',
               'Claude_Monet', 'Diego_Rivera', 'Diego_Velazquez', 'Edgar_Degas', 'Edouard_Manet', 'Edvard_Munch',
               'El_Greco', 'Eugene_Delacroix',
               'Francisco_Goya', 'Frida_Kahlo', 'Georges_Seurat', 'Giotto_di_Bondone', 'Gustav_Klimt',
               'Gustave_Courbet', 'Henri_Matisse', 'Henri_Rousseau',
               'Henri_de_Toulouse-Lautrec', 'Hieronymus_Bosch', 'Jackson_Pollock', 'Jan_van_Eyck', 'Joan_Miro',
               'Kazimir_Malevich', 'Leonardo_da_Vinci',
               'Marc_Chagall', 'Michelangelo', 'Mikhail_Vrubel', 'Pablo_Picasso', 'Paul_Cezanne', 'Paul_Gauguin',
               'Paul_Klee', 'Peter_Paul_Rubens', 'Pierre-Auguste_Renoir',
               'Piet_Mondrian', 'Pieter_Bruegel', 'Raphael', 'Rembrandt', 'Rene_Magritte', 'Salvador_Dali',
               'Sandro_Botticelli', 'Titian', 'Vasiliy_Kandinskiy', 'Vincent_van_Gogh', 'William_Turner']
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Я знаю таких художников, как Albrecht_Dürer, Alfred_Sisley, Amedeo_Modigliani, Andrei_Rublev, Andy_Warhol, Camille_Pissarro, Caravaggio, Claude_Monet, Diego_Rivera, Diego_Velazquez, Edgar_Degas, Edouard_Manet, Edvard_Munch, El_Greco, Eugene_Delacroix, Francisco_Goya, Frida_Kahlo, Georges_Seurat, Giotto_di_Bondone, Gustav_Klimt, Gustave_Courbet, Henri_Matisse, Henri_Rousseau, Henri_de_Toulouse-Lautrec, Hieronymus_Bosch, Jackson_Pollock, Jan_van_Eyck, Joan_Miro, Kazimir_Malevich, Leonardo_da_Vinci, Marc_Chagall, Michelangelo, Mikhail_Vrubel, Pablo_Picasso, Paul_Cezanne, Paul_Gauguin, Paul_Klee, Peter_Paul_Rubens, Pierre-Auguste_Renoir, Piet_Mondrian, Pieter_Bruegel, Raphael, Rembrandt, Rene_Magritte, Salvador_Dali, Sandro_Botticelli, Titian, Vasiliy_Kandinskiy, Vincent_van_Gogh, William_Turner")
info_handler = CommandHandler('info', info)

def send_prediction_on_photo(bot, update):
    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = bot.get_file(image_info)
    image_stream = BytesIO()
    image_file.download(out=image_stream)

    class_, percent= model.predict(image_stream)

    # теперь отправим результат
    update.message.reply_text(str(class_)+' Accuracy: '+str(percent.item))
    print("Sent Answer to user, predicted: {}".format(class_))


if __name__ == '__main__':
    # Включим самый базовый логгинг, чтобы видеть сообщения об ошибках
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    # используем прокси, так как без него у меня ничего не работало(

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