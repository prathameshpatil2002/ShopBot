import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot
bot = telegram.Bot(token="")

# Create an Updater object
updater = Updater(
    token="", use_context=True)

# Create a dispatcher object
dispatcher = updater.dispatcher

# Define the list of inventory items
inventory = {
    'item1': {'price': 10, 'quantity': 5, 'weight': '1kg', 'type': 'food', 'brand': 'Brand1'},
    'item2': {'price': 20, 'quantity': 3, 'weight': '2kg', 'type': 'food', 'brand': 'Brand2'},
    'item3': {'price': 5, 'quantity': 10, 'weight': '500g', 'type': 'food', 'brand': 'Brand3'},
    'item4': {'price': 15, 'quantity': 2, 'weight': '1kg', 'type': 'non-food', 'brand': 'Brand4'},
    'item5': {'price': 25, 'quantity': 4, 'weight': '2kg', 'type': 'non-food', 'brand': 'Brand5'},
    'item6': {'price': 8, 'quantity': 8, 'weight': '500g', 'type': 'non-food', 'brand': 'Brand6'},
    'item7': {'price': 12, 'quantity': 7, 'weight': '1kg', 'type': 'food', 'brand': 'Brand7'},
    'item8': {'price': 18, 'quantity': 6, 'weight': '2kg', 'type': 'food', 'brand': 'Brand8'},
    'item9': {'price': 4, 'quantity': 12, 'weight': '500g', 'type': 'food', 'brand': 'Brand9'},
    'item10': {'price': 14, 'quantity': 3, 'weight': '1kg', 'type': 'non-food', 'brand': 'Brand10'}
}


# Define conversation states
CHOOSE_ITEM, CONFIRM_ORDER = range(2)


# Define the function to display the inventory items to the user


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to ShopBot, your personal shopping assistant on Telegram!\nHere are our available items:")
    for item, attributes in inventory.items():
        text = ""
        att = list(attributes.keys())
        text = text + \
            f" {item}\nPrice : {attributes[att[0]]}\nQuantity : {attributes[att[1]]}\nWeight : {attributes[att[2]]}\nType : {attributes[att[3]]}\nBrand : {attributes[att[4]]}"

        context.bot.send_message(
            chat_id=update.effective_chat.id, text=text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Use /commands to know supported commands")


def order(update, context):
    global selected_items, order_total
    selected_items = []
    order_total = 0
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please choose the items you wish to order. Type item name. (use done to finish):")

    return CHOOSE_ITEM


def choose_item(update, context):
    global selected_items, order_total
    item = update.message.text
    if item == "done":
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Your order is:")
        for item in selected_items:
            text = ""
            att = list(inventory[item].keys())
            text = text + \
                f" {item}\nPrice : {inventory[item][att[0]]}\nQuantity : {inventory[item][att[1]]}\nWeight : {inventory[item][att[2]]}\nType : {inventory[item][att[3]]}\nBrand : {inventory[item][att[4]]}"

            context.bot.send_message(
                chat_id=update.effective_chat.id, text=text)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Total cost: {order_total}. Please confirm your order with /confirm.")
        return CONFIRM_ORDER
    elif item in inventory:
        selected_items.append(item)
        order_total += inventory[item]["price"]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{item} added to your order. Current total: {order_total}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Invalid item. Please choose from the list of available items.")
    return CHOOSE_ITEM


def confirm_order(update, context):
    global selected_items, order_total
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Order confirmed. Thank you for shopping with us!")
    # Reset global variables
    selected_items = []
    order_total = 0
    return ConversationHandler.END


def all_commands(update, context):
    help_text = "Available commands:\n"
    text = ""

    c1 = "/start : Start the bot\n"
    c2 = "/order : Placing order\n"
    c3 = "/confirm : Confirming order\n"
    c4 = "/cancel : Cancelling order\n"
    c5 = "/commands : Displying commands"

    text = text + c1 + c2 + c3 + c4 + c5

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def cancel(update,  context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Order has been cancelled.")


def main():

    # Define the Telegram bot commands

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    order_handler = CommandHandler("order", order)
    dispatcher.add_handler(order_handler)
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, choose_item))
    dispatcher.add_handler(CommandHandler("confirm", confirm_order))
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(CommandHandler("commands", all_commands))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
