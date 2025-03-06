<img width="1236" alt="Screenshot 2025-03-05 at 9 44 45 PM" src="https://github.com/user-attachments/assets/5eddafad-442b-4da0-9926-326d83004606" />
# Chatty-Box: Home Taste Chatbot Integration

Welcome to **Chatty-Box**, the AI-powered chatbot for **Home Taste**, a Vietnamese fast food restaurant. This chatbot is built using **Dialogflow** and integrated into a modern **Tailwind CSS-based** website.

## 🚀 Features
- 🍜 **Order Food:** Add or remove menu items to your order.
- 📦 **Track Orders:** Check the status of your order using an order ID.
- 💬 **Chat Widget:** Embedded chatbot for seamless customer interaction.
- 🌐 **Fully Responsive:** Optimized for all devices using Tailwind CSS.

## 🛠️ Setup & Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo/chatty-box.git
cd chatty-box
```

### **2️⃣ Install Dependencies**
Navigate to the backend folder and install dependencies:
```sh
cd backend
pip install -r requirements.txt
```

### **3️⃣ Run FastAPI Webhook Server**
```sh
uvicorn main:app --reload
```

If running locally, expose it using **ngrok**:
```sh
ngrok http 8000
```
Copy the generated **public URL** and update it in **Dialogflow Console → Fulfillment**.

### **4️⃣ Launch the Website**
Serve the frontend using a simple HTTP server:
```sh
cd frontend
python3 -m http.server 8000
```
Visit **http://localhost:8000/** to see the website.

## 📌 Dialogflow Integration
1. **Enable Webhooks** in **Dialogflow Console → Fulfillment**.
2. **Set Webhook URL** to your **ngrok public URL**.
3. Ensure intents like `order.add`, `order.remove`, and `track.order` have **Webhook enabled**.

## 📄 How to Embed Chatbot in Website
Add the following **iframe** inside your website’s HTML:
```html
<iframe width="350" height="430" allow="microphone;" 
    src="https://console.dialogflow.com/api-client/demo/embedded/35d7754b-cced-44b9-ac7a-19aa15451a38">
</iframe>
```

## 🔧 Troubleshooting
- ❌ **Bot Not Responding?** Check **Dialogflow Logs** for errors.
- 🔄 **Webhook Error?** Ensure your FastAPI server is running and accessible.
- 🖼️ **Image Not Loading?** Serve static assets properly with a local HTTP server.

## 📌 Screenshots
### 🖥️ Website with Chatbot
![Chatbot Screenshot](images/chatbot-screenshot.png)

## 🎉 Contributing
Feel free to submit PRs to improve this chatbot!

---
**Made with ❤️ for Home Taste 🇻🇳**
