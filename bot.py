from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import httpx

# Replace with your actual token
TOKEN = "8596383774:AAE2f4S_u-qc-lvGi33tSNatklymA6UpsqE"
STOCK_URL = "https://raw.githubusercontent.com/xSv5/86RFV79tFouygB976rv/refs/heads/main/stock.txt"

# Modern "Certificate" Style Banner using geometric elements
BANNER_TEXT = """
<pre>
◤━━━━━━━━━━━━━━━━━━━━━━━━━━━━◥
    ✨ GFT DROP - KINGDOM STORE ✨
    💎 OFFICIAL PREMIUM STORE
    🛡️ SECURED BY MOON VENDOR
◣━━━━━━━━━━━━━━━━━━━━━━━━━━━━◢
</pre>
"""

MAIN_MESSAGE = f"""{BANNER_TEXT}
🔥 <b><u>WELCOME TO THE KINGDOM</u></b> 🔥

📢 <b><u>CHANNEL:</u></b> <a href="https://t.me/P4jamaMan">Join Support Channel</a>
⭐ <b><u>VOUCHES:</u></b> 1,500+ Positive
💳 <b><u>CC SOURCE:</u></b> 100% Private / Non-VBV

━━━━━━━━━━━━━━━━━━━━━━━━
📊 <b><u>LIVE NETWORK STATS:</u></b>
🟢 <b>Gateway:</b> Active & Encrypted
🛰️ <b>Nodes:</b> Global Distribution
💳 <b>Stock:</b> Daily Refills (Fresh Fullz)
⚡ <b>Uptime:</b> 99.9% Reliable
━━━━━━━━━━━━━━━━━━━━━━━━

👋🏻 <b>Welcome, King!</b>
Your one-stop shop for premium, high-balance digital assets. 

📲 <b>Main Operator:</b> @P4jamaMan

👇 <b><u>SELECT YOUR REGION TO BROWSE:</u></b>"""

TOS_TEXT = f"""{BANNER_TEXT}
⚖️ <b><u>TERMS OF SERVICE</u></b>

1. <b><u>NO REFUNDS:</u></b> Once digital assets are delivered, all sales are final.
2. <b><u>REPLACEMENTS:</u></b> Replacements are only provided if the card is dead on arrival (DOA). You must provide proof within 30 minutes of purchase.
3. <b><u>USAGE:</u></b> We are not responsible for how you use these assets once purchased.
4. <b><u>CONDUCT:</u></b> Any attempt to scam or chargeback will result in a permanent ban from the Kingdom and reporting to the Moon Vendor network.

<i>By purchasing from KINGDOM STORE, you agree to these terms.</i>"""

CASHOUT_TEXT = f"""{BANNER_TEXT}
📖 <b><u>HOW TO CASH-OUT & PROTOCOL</u></b>

⚡️ <b><u>DELIVERY PROCESS:</u></b>
Once your purchase is confirmed <b>3 times</b> on the blockchain, our system will automatically send the card information directly to your DM.

🛡️ <b><u>BEST OPTION: VISA / MASTERCARD</u></b>
- These are the safest and most successful options in the shop.
- <b>Success Rate:</b> Works 8/10 times for all users.
- <b>DOA Policy:</b> If the card arrives Dead on Arrival, you can request a refund. If confirmed dead, the refund is processed automatically within 5 minutes.

💰 <b><u>CASH-OUT METHODS:</u></b>
1. <b>Online Shopping:</b> Use the details directly on any e-commerce site.
2. <b>Instant Cash:</b> Link the card to Apple Pay or Google Pay.
3. <b>Withdrawal:</b> Add the linked Apple/Google Pay card to Cash App or Venmo to transfer the balance to your personal bank instantly.

Follow these steps for the highest success rate."""

# Product Pricing Configuration
PRODUCT_DETAILS = {
    "amazon": "🛒 Amazon (Physical/E-Gift)",
    "apple": "🍎 Apple / iTunes",
    "uber": "🚗 Uber / Uber Eats",
    "airbnb": "🏡 Airbnb Luxe",
    "nike": "👟 Nike Store",
    "steam": "🎮 Steam Wallet",
    "google": "📱 Google Play",
    "ebay": "🛍️ Ebay Shopping",
    "gaming": "🎮 PlayStation / XBOX",
    "retail": "🏬 Walmart / Target",
    "streaming": "📺 Netflix / Hulu",
    "cards": "💳 Visa/Mastercard (Prepaid)"
}

PRICE_TIERS = {
    "p1": {"balance": "$50 - $55", "price": "$5.00"},
    "p2": {"balance": "$100 - $110", "price": "$10.00"},
    "p3": {"balance": "$150 - $155", "price": "$15.00"},
    "p4": {"balance": "$200 - $220", "price": "$20.00"},
    "p5": {"balance": "$500 - $550", "price": "$45.00"}
}

# Crypto Wallet Configuration
CRYPTO_WALLETS = {
    "BTC": "bc1pjck83gak46fgerssyjpmc5mu5au9g7ufkklm2hjcazzan5n8laeqxzmsce",
    "ETH": "0xF52279583b5AaDFEC29411C05Fa23aEf9284aD1E",
    "SOL": "CSBF58dqRZ5Lj8gJckVxFSt1mG6NNiBU6e9aERWJCEda",
    "MATIC": "0xFEa65d2AF680A47b5AE561c0657c9D8821A86d74"
}

async def fetch_stock():
    """Fetches and parses the stock file from GitHub with improved timeout handling."""
    stock_data = {}
    try:
        # Reduced connect timeout but increased read timeout for GitHub
        timeout = httpx.Timeout(5.0, read=10.0) 
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(STOCK_URL)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        key, val = line.split(':', 1)
                        stock_data[key.strip().lower()] = val.strip()
    except Exception as e:
        print(f"Stock fetch error: {e}")
    return stock_data

def get_main_keyboard():
    return [
        [
            InlineKeyboardButton("🇺🇸 UNITED STATES", callback_data="country_usa"),
            InlineKeyboardButton("🇬🇧 UNITED KINGDOM", callback_data="country_uk")
        ],
        [
            InlineKeyboardButton("🇨🇦 CANADA", callback_data="country_canada"),
            InlineKeyboardButton("🇦🇺 AUSTRALIA", callback_data="country_aus")
        ],
        [
            InlineKeyboardButton("📊 CHECK STOCK", callback_data="check_stock")
        ],
        [
            InlineKeyboardButton("📖 HOW TO CASH-OUT", callback_data="how_to"),
            InlineKeyboardButton("⚖️ TERMS OF SERVICE", callback_data="tos")
        ]
    ]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        MAIN_MESSAGE, 
        reply_markup=InlineKeyboardMarkup(get_main_keyboard()),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # We answer the query immediately to stop the "loading" circle in Telegram
    # which helps prevent some timeout issues.
    await query.answer()

    country_map = {
        "country_usa": ("🇺🇸", "UNITED STATES"),
        "country_uk": ("🇬🇧", "UNITED KINGDOM"),
        "country_canada": ("🇨🇦", "CANADA"),
        "country_aus": ("🇦🇺", "AUSTRALIA")
    }

    if query.data in country_map:
        flag, name = country_map[query.data]
        keyboard = []
        for key, label in PRODUCT_DETAILS.items():
            display_label = label
            if key == "apple":
                display_label = f"🍎 Apple / iTunes ({flag})"
            keyboard.append([InlineKeyboardButton(display_label, callback_data=f"prod_{key}_{query.data}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ RETURN TO MAIN MENU", callback_data="back")])
        text = f"{BANNER_TEXT}\n{flag} <b><u>{name} STOREFRONT</u></b>\n\n<i>All {name} stock is filtered for high-balance results.</i>\n\nSelect your product below:"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "check_stock":
        await query.edit_message_text(f"{BANNER_TEXT}\n⏳ <i>Connecting to secure inventory database...</i>", parse_mode="HTML")
        stock = await fetch_stock()
        
        if not stock:
            # Fallback if the URL times out
            stock_list = "⚠️ <i>Inventory server is currently busy. Please try again in a moment.</i>"
        else:
            stock_list = ""
            for key, name in PRODUCT_DETAILS.items():
                qty = stock.get(key, "OUT OF STOCK")
                status_emoji = "✅" if qty != "0" and qty != "OUT OF STOCK" else "❌"
                stock_list += f"{status_emoji} <b>{name}:</b> {qty}\n"

        text = f"{BANNER_TEXT}\n📊 <b><u>CURRENT LIVE INVENTORY</u></b>\n\n{stock_list}\n\n<i>Stock is updated every 6 hours by @P4jamaMan.</i>"
        keyboard = [[InlineKeyboardButton("⬅️ RETURN TO MAIN MENU", callback_data="back")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data.startswith("prod_"):
        parts = query.data.split("_")
        product_key = parts[1]
        country_code = "_".join(parts[2:])
        flag, country_name = country_map[country_code]
        product_name = PRODUCT_DETAILS.get(product_key, "Product")

        keyboard = []
        for tid, tier in PRICE_TIERS.items():
            btn_text = f"💎 Balance: {tier['balance']} | Price: {tier['price']}"
            keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"sel_{product_key}_{tid}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ BACK TO PRODUCTS", callback_data=country_code)])
        text = f"{BANNER_TEXT}\n{flag} <b><u>{product_name} ({country_name})</u></b>\n\n💰 <b><u>SELECT YOUR LOAD AMOUNT:</u></b>\n\n<i>High success rate guaranteed on all loads.</i>"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data.startswith("sel_"):
        _, prod, tid = query.data.split("_")
        product_name = PRODUCT_DETAILS.get(prod, "Product")
        tier = PRICE_TIERS[tid]
        text = f"{BANNER_TEXT}\n✅ <b><u>SELECTION CONFIRMED</u></b>\n\n<b>Product:</b> {product_name}\n<b>Balance:</b> {tier['balance']}\n<b>Total Price:</b> {tier['price']}\n\nDo you wish to continue to payment?"
        keyboard = [
            [InlineKeyboardButton("💳 CONTINUE TO PAYMENT", callback_data=f"payopt_{prod}_{tid}")],
            [InlineKeyboardButton("❌ CANCEL & GO BACK", callback_data="back")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data.startswith("payopt_"):
        _, prod, tid = query.data.split("_")
        text = f"{BANNER_TEXT}\n🪙 <b><u>SELECT PAYMENT METHOD</u></b>\n\nChoose your preferred cryptocurrency to complete the purchase:"
        keyboard = []
        for coin in CRYPTO_WALLETS.keys():
            keyboard.append([InlineKeyboardButton(coin, callback_data=f"final_{prod}_{tid}_{coin}")])
        keyboard.append([InlineKeyboardButton("⬅️ BACK", callback_data=f"sel_{prod}_{tid}")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data.startswith("final_"):
        _, prod, tid, coin = query.data.split("_")
        tier = PRICE_TIERS[tid]
        address = CRYPTO_WALLETS.get(coin, "ADDRESS_NOT_FOUND")
        await query.edit_message_text(f"{BANNER_TEXT}\n⏳ <b>Generating unique payment address...</b>", parse_mode="HTML")
        await asyncio.sleep(1.5)
        text = f"""{BANNER_TEXT}
💳 <b><u>OFFICIAL PAYMENT INVOICE</u></b>

💎 <b>Order:</b> {PRODUCT_DETAILS.get(prod)}
💰 <b>Load:</b> {tier['balance']}
💵 <b>Amount Due:</b> {tier['price']} in {coin}

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ <b><u>CRITICAL INSTRUCTIONS:</u></b>
1. Send <b>NO LESS</b> than the required amount.
2. Ensure you are using the <b>{coin}</b> network.
3. Your card will be sent automatically after <b>3 network confirmations</b>.
━━━━━━━━━━━━━━━━━━━━━━━━

📮 <b><u>SEND {coin} TO THIS ADDRESS:</u></b>
<code>{address}</code>

<i>(Tap the address above to copy)</i>

📲 After sending, wait for the network to confirm. DM @P4jamaMan if you have any issues."""
        keyboard = [[InlineKeyboardButton("⬅️ RETURN TO MAIN MENU", callback_data="back")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "how_to":
        keyboard = [[InlineKeyboardButton("⬅️ BACK TO MENU", callback_data="back")]]
        await query.edit_message_text(CASHOUT_TEXT, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "tos":
        keyboard = [[InlineKeyboardButton("⬅️ BACK TO MENU", callback_data="back")]]
        await query.edit_message_text(TOS_TEXT, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "back":
        await query.edit_message_text(MAIN_MESSAGE, reply_markup=InlineKeyboardMarkup(get_main_keyboard()), parse_mode="HTML", disable_web_page_preview=True)

if __name__ == "__main__":
    # Increased read_timeout and connect_timeout for the bot's requests to Telegram servers
    app = ApplicationBuilder().token(TOKEN).read_timeout(30).connect_timeout(30).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    print("Kingdom Store is live...")
    app.run_polling()
