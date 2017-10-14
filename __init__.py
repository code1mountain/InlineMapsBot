from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultLocation, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, InlineKeyboardButton
from mapsapi import Geocoding
import logging
import country_codes

GEOCODER = Geocoding("AIzaSyB80EH6gdj5n7C135PilDzLhNtGrsIUtmQ")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def inline(bot, update):
    query = update.inline_query.query
    if not query:
        """
        If the users sends an empty location request, these capitals of the countries with the most telegram users will
        be displayed.
        """
        results = [InlineQueryResultLocation(id=0, latitude=40.7127753, longitude=-74.0059728, title="New York, NY, USA"),
                   InlineQueryResultLocation(id=1, latitude=51.5073509, longitude=-0.1277583, title="London, UK"),
                   InlineQueryResultLocation(id=2, latitude=52.52000659999999, longitude=13.404954,
                                             title="Berlin, Germany"),
                   InlineQueryResultLocation(id=3, latitude=55.755826, longitude=37.6172999, title="Moscow, Russia"),
                   InlineQueryResultLocation(id=4, latitude=41.9027835, longitude=12.4963655, title="Rome, Italy"),
                   InlineQueryResultLocation(id=5, latitude=28.6139391, longitude=77.2090212,
                                             title="New Delhi, Delhi, India"),
                   InlineQueryResultLocation(id=6, latitude=35.6894875, longitude=139.6917064, title="Tokyo, Japan"),
                   InlineQueryResultLocation(id=7, latitude=-6.17511, longitude=106.8650395, title="Jakarta, Indonesia"),
                   InlineQueryResultLocation(id=8, latitude=35.6891975, longitude=51.3889736, title="Teheran, Iran"),
                   InlineQueryResultLocation(id=9, latitude=-22.9068467, longitude=-43.1728965,
                                             title="Rio de Janeiro, Brazil"),
                   InlineQueryResultLocation(id=10, latitude=40.4167754, longitude=-3.7037902, title="Madrid, Spain"),
                   InlineQueryResultLocation(id=11, latitude=24.7135517, longitude=46.6752957,
                                             title="Riyadh Saudi Arabia"),
                   InlineQueryResultLocation(id=12, latitude=41.2994958, longitude=69.2400734,
                                             title="Tashkent, Uzbekistan"),
                   InlineQueryResultLocation(id=13, latitude=37.566535, longitude=126.9779692,
                                             title="Seoul, South Korea"),
                   InlineQueryResultLocation(id=14, latitude=33.3128057, longitude=44.3614875, title="Baghdad, Iraq"),
                   InlineQueryResultLocation(id=15, latitude=52.3702157, longitude=4.895167900000001,
                                             title="Amsterdam, Netherlands"),
                   InlineQueryResultLocation(id=16, latitude=8.9806034, longitude=38.7577605,
                                             title="Addis Ababa, Ethiopia"),

                   ]
        if len(update.effective_user.language_code) > 4:
            """
            Telegram provides a country code to the bot. This country code is resolved to the country and to it's
            capital, so if a user searches with an empty query, the capital of his own country is displayed on the top 
            of the results
            """
            country_code = update.effective_user.language_code[-2:]
            country = country_codes.codes[country_code]
            capital = country_codes.capitals[country]
            coords = GEOCODER.format_output(capital)[0]
            loc = InlineQueryResultLocation(id=hash(coords[0]), latitude=coords[1], longitude=coords[2], title=coords[0])
            results.insert(0, loc)
    else:
        locations = GEOCODER.format_output(query)
        results = []
        for res in locations:
            results.append(InlineQueryResultLocation(id=hash(res[0]), latitude=res[1], longitude=res[2], title=res[0]))
        if not results:
            text =InputTextMessageContent("Can't find that location. Try again!")
            keyboard = [[InlineKeyboardButton("Try again", switch_inline_query_current_chat="")]]
            results.append(InlineQueryResultArticle(id=-1, title="No location found", input_message_content=text,
                                                    reply_markup=InlineKeyboardMarkup(keyboard)))
    bot.answer_inline_query(update.inline_query.id, results, cache_time=20)

def start(bot, update):
    text = "Use this bot in inline mode to search a location. You can search for countries, cities or addresses.\n\n" \
           "<i>Example: @inlinemapsbot Cairo</i>\n\n" \
           "Source: https://github.com/code1mountain/InlineMapsBot/"
    keyboard = [[InlineKeyboardButton("Use Inline", switch_inline_query="")]]
    bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup(keyboard),
                     parse_mode="HTML")


updater = Updater("458202590:AAFM3jNhS9czFG57bmyOoYClxIaGuE-KMlM")
updater.dispatcher.add_handler(InlineQueryHandler(inline))
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle()
