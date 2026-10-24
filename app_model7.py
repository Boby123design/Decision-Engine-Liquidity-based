import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image, ImageGrab
import os
import pandas as pd
from datetime import datetime
import time

# Apne banaye hue custom modules import karna (Model_7 specific)
from model_architecture import ForexMultiModalModel

# PyWin32 libraries for OS level window automation
try:
    import win32gui
    import win32con
except ImportError:
    st.error("🚨 Critical Error: 'pywin32' library nahi mili. Terminal mein 'pip install pywin32' run karein!")

# ==========================================
# 1. PAGE SETUP & STYLING (The Wide UI - Green Theme)
# ==========================================
st.set_page_config(page_title="Model_7 Scalper Terminal", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for exact button colors and UI aesthetics
st.markdown("""
    <style>
    /* Analyze Probability (Primary Button) styling */
    button[kind="primary"] { 
        background-color: #00c853 !important; 
        color: white !important; 
        border: none !important;
        border-radius: 8px; 
        font-weight: bold; 
        transition: 0.3s; 
    }
    button[kind="primary"]:hover { 
        transform: scale(1.02); 
        background-color: #00e676 !important; 
    }
    
    /* Secondary Buttons (Paste, Save to Live Dataset) styling */
    button[kind="secondary"] { 
        border-radius: 8px; 
        font-weight: bold; 
        transition: 0.3s; 
    }
    button[kind="secondary"]:hover { 
        transform: scale(1.02); 
        border-color: #00c853 !important;
        color: #00c853 !important;
    }
    
    /* Radio Button Active Dot turning Green */
    div[data-testid="stRadio"] input[type="radio"]:checked + div {
        background-color: #00c853 !important;
        border-color: #00c853 !important;
    }
    
    .metric-card { background-color: #1e222d; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Model_7: Multi-Modal Scalping Terminal")
st.markdown("---")

# ==========================================
# 2. MODEL_7 ARCHITECTURE & DIRECTORY SETUP
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
base_dir = r"C:\Models\Model_7"
model_path = os.path.join(base_dir, "forex_model.pth")
live_img_dir = os.path.join(base_dir, "live_dataset_images")
live_csv_path = os.path.join(base_dir, "live_cleaned_dataset.csv")

os.makedirs(live_img_dir, exist_ok=True)

@st.cache_resource
def load_model():
    # Calling the exact Model_7 Architecture
    model = ForexMultiModalModel(num_tabular_features=2, num_classes=3)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

if 'current_image' not in st.session_state:
    st.session_state.current_image = None

# ==========================================
# 3. USER INTERFACE (SIDE-BY-SIDE LAYOUT)
# ==========================================
col_img, col_logic = st.columns([1.5, 1])

# --- LEFT COLUMN: Image Capture ---
with col_img:
    st.markdown("### 📸 Trade Chart")
    
    # 📋 BACKUP PASTE FEATURE
    if st.button("📋 1-Click Paste Chart (Ctrl+C from TradingView)"):
        try:
            img = ImageGrab.grabclipboard()
            if img is not None and isinstance(img, Image.Image):
                st.session_state.current_image = img
            else:
                st.warning("⚠️ Clipboard khali hai! Pehle chart ko copy karein.")
        except Exception as e:
            st.error(f"Clipboard error: {e}")
            
    # 🤖 ULTRA-SMART AUTO-CAPTURE
    if st.button("📸 Auto-Capture Live Chart", type="primary"):
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            time.sleep(0.7) 
            
            my_bbox = (167, 104, 1385, 1004)
            img = ImageGrab.grab(bbox=my_bbox)
            
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            st.session_state.current_image = img
            st.rerun()
            
        except Exception as e:
            st.error(f"⚠️ Auto-Capture Automation Error: {e}")

    uploaded_file = st.file_uploader("Ya manual upload karein (Optional)", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if uploaded_file is not None:
        st.session_state.current_image = Image.open(uploaded_file)

    if st.session_state.current_image is not None:
        st.image(st.session_state.current_image, caption='Live Market Setup', use_container_width=True)

# --- RIGHT COLUMN: Logic & Logging ---
with col_logic:
    st.markdown("### ⚙️ Setup Details")
    
    c1, c2 = st.columns(2)
    with c1: trade_type = st.selectbox("Setup Quality:", ["Blind", "Good", "Best"])
    with c2: trade_dir = st.selectbox("Direction:", ["Buy", "Sell"])
    
    # ⚡ PREDICTION ENGINE (Model_7 Multi-Modal Method)
    if st.button("🚀 Analyze Probability", type="primary"):
        if st.session_state.current_image is not None:
            with st.spinner('Analyzing Multi-Modal Matrix...'):
                img_tensor = transform(st.session_state.current_image.convert('RGB')).unsqueeze(0).to(device)
                
                # Model_7 Text Feature Encoding
                t_type_enc = {'blind': 0, 'good': 1, 'best': 2}[trade_type.lower()]
                dir_enc = {'buy': 0, 'sell': 1}[trade_dir.lower()]
                tabular_tensor = torch.tensor([[t_type_enc, dir_enc]], dtype=torch.float32).to(device)
                
                with torch.no_grad():
                    # Feeding both image and text to Model_7
                    output = model(img_tensor, tabular_tensor)
                    probs = F.softmax(output, dim=1)[0]
                
                # Model_7 Class Mapping Sync: ctc=0, sl=1, tp=2
                prob_ctc = probs[0].item() * 100
                prob_sl = probs[1].item() * 100
                prob_tp = probs[2].item() * 100
                combined_tp_ctc = prob_tp + prob_ctc
                
                st.markdown("### 📊 AI Verdict")
                if prob_sl > 40 or combined_tp_ctc < 45:
                    st.error(f"❌ **SKIP.** (SL Risk: {prob_sl:.1f}%)")
                elif 45 <= combined_tp_ctc <= 55:
                    st.warning(f"⚠️ **CAUTION.** (TP+CTC: {combined_tp_ctc:.1f}%)")
                else:
                    st.success(f"✅ **ENTRY!** (TP+CTC: {combined_tp_ctc:.1f}%)")
                    
                st.write(f"*TP: {prob_tp:.1f}% | CTC: {prob_ctc:.1f}% | SL: {prob_sl:.1f}%*")
        else:
            st.error("Pehle chart capture karein!")

    st.markdown("---")
    
    # ⚡ LIVE DATA HARVESTING
    st.markdown("### 💾 Log Live Trade")
    st.caption("Trade complete hone ke baad result log karein")
    actual_result = st.radio("Actual Outcome:", ["TP", "SL", "CTC"], horizontal=True)
    
    if st.button("💾 Save to Live Dataset"):
        if st.session_state.current_image is not None:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                img_name = f"live_trade_{timestamp}.png"
                img_full_path = os.path.join(live_img_dir, img_name)
                
                # Save Raw Image
                st.session_state.current_image.convert('RGB').save(img_full_path)
                
                # Structuring standard dataset row
                new_data = {
                    "Image_Path": img_full_path,
                    "Trade_Type": trade_type.lower(),
                    "Result": actual_result.lower(),
                    "Type": trade_dir.lower()
                }
                new_df = pd.DataFrame([new_data])
                
                # Append to CSV
                if not os.path.exists(live_csv_path):
                    new_df.to_csv(live_csv_path, index=False)
                else:
                    new_df.to_csv(live_csv_path, mode='a', header=False, index=False)
                    
                st.success(f"✅ Data Saved in 'live_cleaned_dataset.csv'!")
                st.session_state.current_image = None
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"Error saving data: {e}")
        else:
            st.error("Save karne ke liye koi image nahi hai!")