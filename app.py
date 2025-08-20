import streamlit as st
import pandas as pd
import os
from sklearn.ensemble import IsolationForest
import pywifi
import time

CSV_FILE = "wifi_scans.csv"
WIFI_ICON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="22" height="22">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.5 12.75a5 5 0 016.995 0m2.01-2.86a9 9 0 00-11.65 0M2.927 9.317a13 13 0 0118.146 0" />
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 20.25v.008h.008v-.008H12z" />
  <circle cx="12" cy="16" r="1" fill="currentColor" />
</svg>
"""

def scan_wifi_pywifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(3)
    results = iface.scan_results()
    networks = []
    for network in results:
        ssid = network.ssid.strip()
        bssid = network.bssid.strip()
        signal = network.signal
        if ssid != "":
            networks.append({'SSID': ssid, 'BSSID': bssid, 'Signal': signal})
    return networks

def save_scan_to_csv(networks):
    if not networks:
        return
    df_new = pd.DataFrame(networks)
    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(CSV_FILE, index=False)

def extract_features(df):
    hist_stats = df.groupby('SSID').agg({
        'BSSID': pd.Series.nunique,
        'Signal': 'mean'
    }).rename(columns={'BSSID':'hist_bssid_count', 'Signal':'hist_avg_signal'})
    return hist_stats

def prepare_current_features(networks, hist_stats):
    df_current = pd.DataFrame(networks)
    current_stats = df_current.groupby('SSID').agg({
        'BSSID': pd.Series.nunique,
        'Signal': 'mean'
    }).rename(columns={'BSSID':'curr_bssid_count', 'Signal':'curr_avg_signal'})
    features = hist_stats.join(current_stats, how='outer').fillna(0)
    return features

def train_model(features):
    clf = IsolationForest(contamination=0.1, random_state=42)
    clf.fit(features)
    return clf

# Custom CSS for professional look
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #1f2937 !important;
        color: white;
    }
    .css-1d391kg a {
        color: white !important;
    }
    /* Main content */
    .css-18e3th9 {
        background-color: #f9fafb;
    }
    .title {
        font-weight: 700;
        font-size: 2rem;
        color: white;
        margin-bottom: 0.25rem;
    }
    .wifi-suspicious {
        color: #dc2626;
        font-weight: 700;
    }
    .wifi-normal {
        color: #22c55e;
        font-weight: 700;
    }
    div.stButton > button:first-child {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        padding: 8px 16px;
        border-radius: 6px;
        border: none;
        transition: background-color 0.2s ease;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #1d4ed8;
        cursor: pointer;
    }
    .header-logo {
        height: 48px;
        margin-bottom: 10px;
    }
    .stat-box {
        background: white;
        border-radius: 8px;
        padding: 15px 20px;
        box-shadow: 0 2px 8px rgb(0 0 0 / 0.05);
        margin-bottom: 12px;
        text-align: center;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2563eb;
    }
    .stat-label {
        font-size: 0.95rem;
        color: #6b7280;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar content + Filters
st.sidebar.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=140)
st.sidebar.markdown("## Filters & Navigation")
filter_ssid = st.sidebar.text_input("Filter by SSID (case insensitive):")
filter_suspicious = st.sidebar.selectbox("Show networks:", ["All", "Only Suspicious", "Only Normal"])
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by EvilTwinner")

# Main content
st.markdown(f"<div class='title'>{WIFI_ICON_SVG} AI-based Evil Twin Wi-Fi Detector</div>", unsafe_allow_html=True)

if st.button("🔄 Scan Wi-Fi"):
    with st.spinner("Scanning Wi-Fi networks..."):
        networks = scan_wifi_pywifi()
        if not networks:
            st.warning("No Wi-Fi networks detected or scanning failed.")
        else:
            save_scan_to_csv(networks)

            df_history = pd.read_csv(CSV_FILE)
            hist_stats = extract_features(df_history)
            features = prepare_current_features(networks, hist_stats)
            model = train_model(features)
            preds = model.predict(features)
            features['anomaly'] = preds
            suspicious_ssids = features[features['anomaly'] == -1].index.tolist()

            # Filtering logic
            filtered = features.copy()
            if filter_ssid.strip():
                filtered = filtered[filtered.index.str.contains(filter_ssid.strip(), case=False)]
            if filter_suspicious == "Only Suspicious":
                filtered = filtered[filtered['anomaly'] == -1]
            elif filter_suspicious == "Only Normal":
                filtered = filtered[filtered['anomaly'] != -1]

            # Stats summary
            total_networks = len(features)
            suspicious_count = (features['anomaly'] == -1).sum()
            avg_signal = round(features[['curr_avg_signal','hist_avg_signal']].mean().mean(), 1)
            avg_bssid_count = round(features[['curr_bssid_count','hist_bssid_count']].mean().mean(), 2)

            # Stats display in columns
            st.markdown("### Network Statistics")
            cols = st.columns(4)
            cols[0].markdown(f"<div class='stat-box'><div class='stat-number'>{total_networks}</div><div class='stat-label'>Total Networks</div></div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div class='stat-box'><div class='stat-number'>{suspicious_count}</div><div class='stat-label'>Suspicious Networks</div></div>", unsafe_allow_html=True)
            cols[2].markdown(f"<div class='stat-box'><div class='stat-number'>{avg_signal} dBm</div><div class='stat-label'>Avg Signal Strength</div></div>", unsafe_allow_html=True)
            cols[3].markdown(f"<div class='stat-box'><div class='stat-number'>{avg_bssid_count}</div><div class='stat-label'>Avg BSSID Count</div></div>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Nearby Wi-Fi Networks")
            if filtered.empty:
                st.info("No networks match the filter criteria.")
            else:
                for ssid in filtered.index:
                    is_suspicious = filtered.loc[ssid, 'anomaly'] == -1
                    if is_suspicious:
                        st.markdown(
                            f"<span class='wifi-suspicious'>{WIFI_ICON_SVG} {ssid} (⚠️ Suspicious)</span>",
                            unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f"<span class='wifi-normal'>{WIFI_ICON_SVG} {ssid}</span>",
                            unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### How this Evil Twin Detection Works:")
            st.markdown("""
            1. The app **scans nearby Wi-Fi networks** when you click the Scan button.
            2. It **automatically saves** scan data to learn over time.
            3. It tracks normal patterns: how many unique access points (BSSIDs) each network (SSID) usually has and their typical signal strength.
            4. An **AI model (Isolation Forest)** detects Wi-Fi networks with unusual behavior — like new or changed access points or abnormal signals.
            5. Networks with abnormal behavior are **flagged as suspicious** — potentially evil twins trying to impersonate legit networks.
            6. This is an **unsupervised, self-learning approach** that improves detection by learning from ongoing scans.
            """)
            st.caption("Click 'Scan Wi-Fi' regularly to keep the detection updated!")
else:
    st.info("Click the 'Scan Wi-Fi' button above to start detecting suspicious networks.")
