import streamlit as st
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import os
import pandas as pd
from datetime import datetime
import time

# Apne architecture ko import karna (Model_7 specific)
from model_architecture import ForexMultiModalModel

# ==========================================
# 1. PAGE SETUP & STYLING
# ==========================================
st.set_page_config(page_title="Model_7 Network Terminal", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for glowing metrics and clean buttons
st.markdown("""
    <style>
    /* Analyze Probability Button Styling */
    button[kind="primary"] { 
        background-color: #00c853 !important; 
        color: white !important; 
        border: none !important;
        border-radius: 8px; 
        font-weight: bold; 
        width: 100%;
        transition: 0.3s; 
    }
    button[kind="primary"]:hover { 
        transform: scale(1.02); 
        background-color: #00e676 !important; 
    }
    
    /* Save & Secondary Buttons Styling */
    button[kind="secondary"] { 
        border-radius: 8px; 
        font-weight: bold; 
        width: 100%;
        transition: 0.3s; 
    }
    button[kind="secondary"]:hover { 
        transform: scale(1.02); 
        border-color: #00c853 !important;
        color: #00c853 !important;
    }
    
    /* Green Radio Dot */
    div[data-testid="stRadio"] input[type="radio"]:checked + div {
        background-color: #00c853 !important;
        border-color: #00c853 !important;
    }
    .metric-card { background-color: #1e222d; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Model_7: Multi-Device Scalping Terminal (Network Synced)")
st.markdown("---")

# ==========================================
# 2. MODEL & DIRECTORY SETUP (SERVER STORAGE)
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ⚡ PATH INTEGRITY FOR SERVER HARD DRIVE
base_dir = r"C:\Models\Model_7"
model_path = os.path.join(base_dir, "forex_model.pth")
live_img_dir = os.path.join(base_dir, "live_dataset_images")
live_csv_path = os.path.join(base_dir, "live_cleaned_dataset.csv")

# Create live dataset folder if it doesn't exist on server
os.makedirs(live_img_dir, exist_ok=True)

@st.cache_resource
def load_model():
    model = ForexMultiModalModel(num_tabular_features=2, num_classes=3)
    try:
        # strict=False lagaya taaki kisi choti mismatch se app crash na ho
        model.load_state_dict(torch.load(model_path, map_location=device), strict=False)
        st.sidebar.success("✅ Model_7 Engine Online!")
    except Exception as e:
        st.sidebar.error(f"Error loading model: {e}")
    model.to(device)
    model.eval()
    return model

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Session state to hold the current image
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

# ==========================================
# 3. USER INTERFACE (SIDE-BY-SIDE LAYOUT)
# ==========================================
col_img, col_logic = st.columns([1.4, 1])

# --- LEFT COLUMN: Image Input via Browser Network ---
with col_img:
    st.markdown("### 📸 Trade Chart")
    
    st.info("💡 **Doosre Laptop se Paste Setup:** TradingView par chart ko `Ctrl+C` karke copy karein, fir niche wale Box par ek baar click karke seedha **`Ctrl+V`** daba dein!")
    
    # Browser native file input - seamlessly transfers images across devices
    uploaded_file = st.file_uploader("Chart Image Yahan Drop Karein Ya Click Karke Ctrl+V Se Paste Karein", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        st.session_state.current_image = Image.open(uploaded_file)

    if st.session_state.current_image is not None:
        st.image(st.session_state.current_image, caption='Live Synced Setup', use_container_width=True)

# --- RIGHT COLUMN: Business Logic & Server Data Logging ---
with col_logic:
    st.markdown("### ⚙️ Setup Details")
    
    c1, c2 = st.columns(2)
    with c1: trade_type = st.selectbox("Setup Quality:", ["Blind", "Good", "Best"])
    with c2: trade_dir = st.selectbox("Direction:", ["Buy", "Sell"])
    
    # ⚡ REMOTE PREDICTION ENGINE (Model_7 Logic)
    if st.button("🚀 Analyze Probability", type="primary"):
        if st.session_state.current_image is not None:
            with st.spinner('Server computing...'):
                img_tensor = transform(st.session_state.current_image.convert('RGB')).unsqueeze(0).to(device)
                
                # Model_7 specific tabular encoding
                t_type_enc = {'blind': 0, 'good': 1, 'best': 2}[trade_type.lower()]
                dir_enc = {'buy': 0, 'sell': 1}[trade_dir.lower()]
                tabular_tensor = torch.tensor([[t_type_enc, dir_enc]], dtype=torch.float32).to(device)
                
                with torch.no_grad():
                    output = model(img_tensor, tabular_tensor)
                    probs = F.softmax(output, dim=1)[0]
                
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
            st.error("Pehle chart uploader box me paste karein!")

    st.markdown("---")
    
    # ⚡ SERVER DATA HARVESTING
    st.markdown("### 💾 Log Live Trade")
    st.caption("Trade outcome select karke Server par pipeline store karein")
    actual_result = st.radio("Actual Outcome:", ["TP", "SL", "CTC"], horizontal=True)
    
    if st.button("💾 Save to Live Dataset"):
        if st.session_state.current_image is not None:
            try:
                # 1. Generate unique file name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                img_name = f"live_trade_{timestamp}.png"
                img_full_path = os.path.join(live_img_dir, img_name)
                
                # 2. Save image to Server Laptop folder directly
                st.session_state.current_image.convert('RGB').save(img_full_path)
                
                # 3. Create DataFrame row
                new_data = {
                    "Image_Path": img_full_path,
                    "Trade_Type": trade_type.lower(),
                    "Result": actual_result.lower(),
                    "Type": trade_dir.lower()
                }
                new_df = pd.DataFrame([new_data])
                
                # 4. Append to CSV on Server
                if not os.path.exists(live_csv_path):
                    new_df.to_csv(live_csv_path, index=False)
                else:
                    new_df.to_csv(live_csv_path, mode='a', header=False, index=False)
                    
                st.success(f"✅ Success! Data perfectly stored on Server Hard Drive (Model_7 Folder).")
                
                # Reset UI for next trade
                st.session_state.current_image = None
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"Server database saving failure: {e}")
        else:
            st.error("Save karne ke liye koi image nahi hai!")