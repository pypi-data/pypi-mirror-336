📖 Usage Example (English)
1️⃣ Initialize the SDK
You can initialize the SDK using default parameters:

from liberal_alpha import initialize, liberal

initialize()
Or customize the parameters:

initialize(host="127.0.0.1", port=8128)
2️⃣ Send Data

JSON_Object = {
    "Price": 100000,
    "Volume": 50,
    "Volume_USD": 5000000,
}

liberal.send_data("BTC_SOURCE1", JSON_Object, record_id="1")
3️⃣ Send Alpha Signal

alpha_data = {
    "signal": "buy",
    "confidence": 0.85
}

liberal.send_alpha("Alpha_ID", alpha_data, record_id="1")
4️⃣ Subscribe to Data
If you need to subscribe to real-time data, use the subscribe_data method. Make sure you have subscribed to the desired records via the website's Subscribe Channel.

liberal.subscribe_data(
    api_key="YOUR_API_KEY",
    base_url="http://your-backend-url",
    private_key="YOUR_PRIVATE_KEY",  # Optional, used for decrypting messages
    record_id=1,                     # Subscribe to a specific record; omit to subscribe to all subscribed records
    max_reconnect=5
)
Ensure that your API Key and private key are correct, and that you have subscribed to the data you wish to receive in the website's subscribe channel.