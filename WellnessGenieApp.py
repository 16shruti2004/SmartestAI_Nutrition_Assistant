import streamlit as st
import pandas as pd
from PIL import Image
import speech_recognition as sr
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
from gtts import gTTS
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="WellnessGenie", layout="wide", page_icon="🥗")

# --- Custom CSS for attractive UI ---
st.markdown("""
    <style>
        .main {background-color: #f9f9f9;}
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            border-radius: 1rem;
            background-color: #ffffff;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .sidebar .sidebar-content {background-color: #e6f2ff;}
        .stRadio > div {flex-direction: row; justify-content: space-around;}
        .stButton > button {background-color: #4CAF50; color: white; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

# --- Text-to-Speech ---
def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_data = audio_fp.read()
        if not audio_data:
            st.error("⚠️ Audio data is empty.")
            return
        audio_encoded = base64.b64encode(audio_data).decode()
        st.markdown(f"""
        <audio autoplay controls style="width: 100%;">
            <source src="data:audio/mp3;base64,{audio_encoded}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ TTS failed: {e}")

# --- Load Models and Data ---
@st.cache_resource
def load_all():
    df = pd.read_excel("Main_Nutrition_plan.xlsx")
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df['age'] = df['age'].astype(str).str.strip()
    df_food_health = pd.read_csv("Nutrion_check.csv")
    df_food_health.columns = [col.strip().lower().replace(" ", "_").replace("(kcal)", "kcal").replace("(g)", "g").replace("(mg)", "mg") for col in df_food_health.columns]
    model_img = MobileNetV2(weights="imagenet")
    return df, model_img, df_food_health

df, mobilenet_model, food_health_df = load_all()

if 'show_home' not in st.session_state:
    st.session_state['show_home'] = True

# --- Function to classify food image ---
@st.cache_data
def classify_food_image(_img):
    _img = _img.resize((224, 224))
    arr = image.img_to_array(_img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    preds = mobilenet_model.predict(arr)
    return decode_predictions(preds, top=1)[0][0][1]

st.title("💪🥗 WellnessGenie")
st.markdown("**Welcome to WellnessGeine!: Your Personalized Nutrition AI Assistant**", unsafe_allow_html=True)

# --- Main UI Logic ---
if st.session_state['show_home']:
    with st.sidebar:
        st.header("👤 User Info")
        gender = st.radio("Select Gender", ["Male", "Female"])
        age = st.selectbox("Select Age", sorted(df['age'].dropna().unique()))
        condition_input = st.session_state.get('voice_condition', '')
        filtered_conditions = df[
            (df['age'].astype(str) == str(age)) &
            (df['gender'].str.lower() == gender.lower())
        ]['condition'].dropna().str.strip().str.lower().unique()
        unique_conditions = pd.Series(filtered_conditions).str.title().sort_values().unique()
        if condition_input:
            condition = condition_input.title() if condition_input.title() in unique_conditions else st.selectbox("Health Condition", unique_conditions)
        else:
            condition = st.selectbox("Health Condition", unique_conditions)
        enable_tts = st.checkbox("🔊 Enable Voice Guide", value=True)

    query = condition.lower()
    df_filtered = df[
        (df['age'].astype(str) == str(age)) &
        (df['gender'].str.lower() == gender.lower()) &
        (df['condition'].str.strip().str.lower() == condition.strip().lower())
    ]

    if not df_filtered.empty:
        st.markdown("## 🍽 Your Personalized Meal Plan")
        meal_times = ["breakfast", "mid-morning snack", "lunch", "afternoon snack", "snack", "dinner", "bed-time"]
        nutrients_summary = []

        toggle = st.radio("Show Meal Type", ["Vegetarian", "Non-Vegetarian"], horizontal=True)

        for meal in meal_times:
            meal_df = df_filtered[df_filtered['meal_time'].str.lower().str.replace(" ", "").str.contains(meal.replace(" ", ""))]
            if not meal_df.empty:
                st.markdown(f"### 🍽 {meal.title()}")
                for _, row in meal_df.iterrows():
                    if toggle == "Vegetarian":
                        st.markdown(f"- 🥦 **Veg**: {row.get('veg_meal', '')} ({row.get('veg_portion', '')})")
                    elif toggle == "Non-Vegetarian":
                        st.markdown(f"- 🍗 **Non-Veg**: {row.get('nonveg_meal', '')} ({row.get('nonveg_portion', '')})")
                    st.markdown(f"- 🔥 **Calories**: {row.get('meal_calories', 'N/A')}")
                    nutrients_summary.append(row.get('meal_calories', 0))
                st.markdown("---")

        st.markdown("### 🏌 Recommended Exercise")
        exercises = df_filtered['recommended_exercise'].dropna().unique()
        if len(exercises):
            youtube_videos = [
                "https://www.youtube.com/embed/UBMk30rjy0o",
                "https://www.youtube.com/embed/ml6cT4AZdqI",
                "https://www.youtube.com/embed/v7AYKMP6rOE",
                "https://www.youtube.com/embed/8BcPHWGQO44"
            ]
            for i, ex in enumerate(exercises):
                st.markdown(f"#### 🏃 {ex}")
                st.video(youtube_videos[i % len(youtube_videos)])
        else:
            st.info("No specific exercise recommendations available.")

        st.markdown("### 🚰 Water Intake Advice")
        try:
            age_int = int(age)
            if age_int < 10:
                water = "5–6 glasses"
            elif age_int < 18:
                water = "6–8 glasses"
            elif age_int < 50:
                water = "8–10 glasses"
            else:
                water = "8–12 glasses"
            st.info(f"Recommended daily water intake: **{water}** based on your age group.")
        except:
            st.info("Recommended daily water intake: 8–10 glasses of water.")

        st.markdown("## 🔔 Reminders")
        if st.button("Set Reminder to Drink Water"):
            st.info("Reminder: Drink water every 2 hours!")

        if enable_tts:
            try:
                summary = "Here's your meal plan."
                for meal in ["breakfast", "lunch", "dinner"]:
                    part = df_filtered[df_filtered['meal_time'].str.lower().str.contains(meal)]
                    if not part.empty:
                        meals = part['veg_meal'] if toggle == "Vegetarian" else part['nonveg_meal']
                        items = ", ".join(meals.dropna().unique())
                        summary += f" For {meal}, {items}."
                summary += " Stay hydrated and stay healthy!"
                text_to_speech(summary)
            except Exception as e:
                st.warning(f"TTS issue: {e}")

        st.markdown("### 📊 Nutrient Summary")
        if nutrients_summary:
            fig, ax = plt.subplots()
            sns.histplot(nutrients_summary, bins=5, kde=True, ax=ax, color="green")
            ax.set_title("Meal Calories Distribution")
            ax.set_xlabel("Calories")
            st.pyplot(fig)

        st.markdown("### ⚠️ Health Warnings")
        if condition.lower() in ["diabetes", "cardiovascular diseases", "obesity"]:
            st.warning("Avoid foods high in sugar, saturated fat, and sodium.")
        elif condition.lower() in ["anemia"]:
            st.info("Focus on iron-rich foods like spinach, lentils, and meat.")
        elif condition.lower() in ["osteoporosis"]:
            st.info("Ensure adequate calcium intake from dairy or fortified foods.")

    st.markdown("---")
    st.markdown("### 🔍 Want to detect food from image?")
    if st.button("Go to Image Detection"):
        st.session_state['show_home'] = False
        st.rerun()

else:
    st.markdown("### 📷 Detect Food via Image")
    mode = st.radio("Choose Input Mode", ["📷 Live Camera", "📁 Upload Image"], horizontal=True)
    uploaded = None
    if mode == "📷 Live Camera":
        uploaded = st.camera_input("Take a food picture")
    elif mode == "📁 Upload Image":
        uploaded = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

    if uploaded:
        st.session_state['show_home'] = False
        img = Image.open(uploaded)
        image_label = classify_food_image(img)
        st.image(img, caption=f"🔍 Detected: {image_label}", use_column_width=True)
        st.success(f"✅ Food Detected: **{image_label}**")

        matched = food_health_df[food_health_df['food'].str.lower() == image_label.lower()]
        if not matched.empty:
            nutrients = matched.iloc[0]
            st.subheader("🧪 Nutritional Information")
            st.markdown(f"**Detected Food**: {image_label.title()}")
            st.markdown(f"**Category**: {nutrients.get('category', 'N/A')}")
            st.markdown(f"**Calories**: {nutrients.get('calories_kcal', 'N/A')} kcal")
            st.markdown(f"**Protein**: {nutrients.get('protein_g', 'N/A')} g")
            st.markdown(f"**Vitamins**: {nutrients.get('vitamins', 'N/A')}")
            st.markdown(f"**Calcium**: {nutrients.get('calcium_mg', 'N/A')} mg")
            st.markdown(f"**Fat**: {nutrients.get('fat_g', 'N/A')} g")

            rating = nutrients.get('health_rating', 'Unknown').capitalize()
            if rating == "Unhealthy":
                st.error(f"🧪 Health Status: {rating}")
                st.markdown("#### ⚠️ AI Suggestion: Try replacing with a healthier option like salad, fruit or low-fat yogurt.")
            else:
                st.success(f"🧪 Health Status: {rating}")
        else:
            st.warning("⚠️ No health info found for this item.")

    if st.button("🔙 Back to Home"):
        st.session_state['show_home'] = True
        st.rerun()
