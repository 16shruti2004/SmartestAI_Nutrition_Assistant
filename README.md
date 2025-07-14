# 🥗 WellnessGenie — Smart AI Nutrition Assistant

**WellnessGenie** is an AI-powered nutrition assistant that helps users get **personalized meal plans**, detect food items using real-time image classification, and receive nutritional advice and healthy living tips — all through a simple, interactive **Streamlit web app**.

---

## 🚀 **Key Features**

✅ **Personalized Meal Plans** — Tailored to age, gender, and health conditions (e.g., diabetes, anemia, obesity, cardiovascular diseases).  
✅ **Vegetarian & Non-Vegetarian Options** — Choose your dietary preference.  
✅ **Food Detection with AI** — Upload a food image or use your webcam — the app uses **MobileNetV2** to classify food items instantly.  
✅ **Nutritional Insights** — Get calories, protein, fat, vitamins, and health ratings for detected food.  
✅ **Voice Assistant (TTS)** — Powered by **gTTS**, the app can speak your meal plan and tips out loud.  
✅ **Hydration & Exercise Tips** — Recommended water intake and exercises with helpful videos.  
✅ **Beautiful & Simple UI** — Built with Streamlit, custom CSS, Seaborn, and Matplotlib for smooth charts and visuals.

---

## 🛠️ **Tech Stack**

- **Language:** Python 3.x  
- **Framework:** Streamlit  
- **Deep Learning:** TensorFlow Keras — MobileNetV2 (pre-trained on ImageNet)  
- **Image Processing:** PIL (Pillow)  
- **Text-to-Speech:** gTTS  
- **Visualization:** Matplotlib, Seaborn  
- **Data:** Custom Excel/CSV nutrition plan and food health dataset

---

## 📸 **How It Works**

1. **Select your profile:** Gender, age, and health condition.  
2. **Get your meal plan:** View personalized meals, calories, exercise recommendations, and water reminders.  
3. **Use AI detection:** Upload or capture a food image — see real-time classification and nutrition details.  
4. **Listen:** Enable the voice assistant to hear your plan and tips.  
5. **Stay healthy!**

---


---

## ⚙️ **How To Run**

1️⃣ Clone this repo:
```bash
git clone https://github.com/yourusername/WellnessGenie.git
cd WellnessGenie

2️⃣ Install requirements:
pip install streamlit tensorflow pillow gTTS matplotlib seaborn pandas numpy speechrecognition

3️⃣ Make sure your Excel/CSV data files (Main_Nutrition_plan.xlsx & Nutrion_check.csv) are in the same folder as the app.

4️⃣ Run the app:
streamlit run WellnessGenieApp.py

5️⃣ Open the URL Streamlit gives you (usually http://localhost:8501).

🔬 Future Improvements
Fine-tune MobileNetV2 with local/regional food datasets.

Add speech recognition for hands-free voice input.

Improve food detection for mixed dishes.

Deploy on Streamlit Cloud or Heroku for public access.

Develop a mobile version or PWA.

🤝 Team
Manisa Mondal

Kanya Kumari Bikram

Dipanwita Mondal

Shruti Kumari Hela

📄 License
This project is for educational purposes under the NSTIW Kolkata AI Programming Certificate (2024–2025).
Feel free to fork, improve, and share!

## Happy healthy coding! 🥑💧


---

## ✅ **Next Step**

1️⃣ Copy the above into a file named **`README.md`** in your project folder.  
2️⃣ Replace `https://github.com/yourusername/WellnessGenie` with your actual GitHub repo link.  
3️⃣ Push it to GitHub!

If you want, I can **package this as a ready `.md` file** — just say **“Yes, export the README”** and I’ll generate it for you! 🚀✨


