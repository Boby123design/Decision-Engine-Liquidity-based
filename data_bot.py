import streamlit as st
from PIL import ImageGrab
import os
import pandas as pd
from datetime import datetime

# ==========================================
# 1. PAGE SETUP & STYLING
# ==========================================
st.set_page_config(page_title="Data Bot - 5000 Trades", layout="centered")

st.markdown("""
    <style>
    .stButton>button { height: 70px; font-size: 18px; font-weight: bold; border-radius: 12px; transition: 0.2s; }
    .stButton>button:hover { transform: scale(1.03); border-color: #00b56a; color: #00b56a; }
    .preview-btn>button { height: 40px !important; font-size: 14px !important; border-color: #f39c12 !important; color: #f39c12 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ 1-Click Historical Auto-Bot")
st.caption("TradingView se chart copy karein (Ctrl+C) aur niche apna result select karein.")
st.markdown("---")

# ==========================================
# 2. DIRECTORY SETUP
# ==========================================
base_dir = r"C:\Models\Model_7"
hist_img_dir = os.path.join(base_dir, "historical_5000_images")
hist_csv_path = os.path.join(base_dir, "historical_dataset.csv")

os.makedirs(hist_img_dir, exist_ok=True)

# ==========================================
# 3. PREVIEW FEATURE
# ==========================================
st.markdown("<div class='preview-btn'>", unsafe_allow_html=True)
if st.button("👀 Preview Clipboard Image (Check before saving)"):
    img = ImageGrab.grabclipboard()
    if img is not None:
        st.image(img, caption="Current Image in Clipboard", use_column_width=True)
    else:
        st.warning("⚠️ Clipboard khali hai! Pehle TradingView se chart copy karein.")
st.markdown("</div>", unsafe_allow_html=True)
st.write("") # Spacing

# ==========================================
# 4. AUTOMATION LOGIC
# ==========================================
def process_and_save(quality, direction, outcome):
    try:
        img = ImageGrab.grabclipboard()
        
        if img is None:
            st.error("⚠️ Clipboard khali hai! Pehle TradingView se chart copy karein.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_name = f"{quality}_{direction}_{outcome}_{timestamp}.png"
        img_full_path = os.path.join(hist_img_dir, img_name)

        img.save(img_full_path)

        new_data = {
            "Image_Path": img_full_path,
            "Trade_Type": quality,
            "Type": direction,
            "Result": outcome
        }
        new_df = pd.DataFrame([new_data])

        if not os.path.exists(hist_csv_path):
            new_df.to_csv(hist_csv_path, index=False)
        else:
            new_df.to_csv(hist_csv_path, mode='a', header=False, index=False)

        st.success(f"✅ Fast Saved: {img_name}")
        
    except Exception as e:
        st.error(f"Error: {e}")

# ==========================================
# 5. ULTRA-FAST USER INTERFACE
# ==========================================
quality = st.radio("Setup Quality:", ["best", "good", "blind"], horizontal=True)
st.write("") 

st.markdown("### 🟢 BUY Setups")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📈 BUY + TP"): process_and_save(quality, "buy", "tp")
with c2:
    if st.button("📉 BUY + SL"): process_and_save(quality, "buy", "sl")
with c3:
    if st.button("➖ BUY + CTC"): process_and_save(quality, "buy", "ctc")

st.markdown("---")

st.markdown("### 🔴 SELL Setups")
c4, c5, c6 = st.columns(3)
with c4:
    if st.button("📉 SELL + TP"): process_and_save(quality, "sell", "tp")
with c5:
    if st.button("📈 SELL + SL"): process_and_save(quality, "sell", "sl")
with c6:
    if st.button("➖ SELL + CTC"): process_and_save(quality, "sell", "ctc")