# 🛡️ AI-based Evil Twin Wi-Fi Detector

![Streamlit App Screenshot](https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png)

A self-learning, AI-powered tool to detect suspicious Wi-Fi networks (potential Evil Twins) using unsupervised anomaly detection.

---

## 📌 Features

* 🔍 **Real-time Wi-Fi Scanning** via `pywifi`
* 🤖 **Anomaly Detection** with **Isolation Forest**
* 📊 **Self-learning**: stores scan history to improve future detections
* 🛑 Flags Wi-Fi SSIDs with:

  * Unexpected BSSIDs
  * Abnormal signal strengths
* 🧠 Built with **Streamlit**, **scikit-learn**, and **pandas**
* 🧪 Clean and responsive UI with modern CSS styling

---

## 🎯 What is an Evil Twin?

An **Evil Twin** is a rogue Wi-Fi access point that mimics a legitimate network (SSID) to trick users into connecting, potentially capturing data or launching attacks.
This app identifies them based on behavioral anomalies in:

* Number of broadcasting access points (BSSIDs)
* Signal strength variations over time

---

## 🚀 How It Works

1. **Scan nearby Wi-Fi networks**.
2. **Automatically logs data** for future reference.
3. Calculates:

   * Average signal strength
   * Number of unique BSSIDs per SSID
4. Trains an **Isolation Forest** model to learn what’s “normal”.
5. Flags any network with unusual characteristics as **Suspicious**.

---

## 📦 Installation

### 🔧 Prerequisites

* Python 3.7+
* Works **only on Windows and Linux** (for `pywifi`)

### 🐍 Create Virtual Environment (optional but recommended)

```bash
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
```

### 🔽 Install Requirements

```bash
pip install -r requirements.txt
```

**`requirements.txt`**

```txt
streamlit
pandas
scikit-learn
pywifi
```

---

## 🖥️ Usage

```bash
streamlit run app.py
```

### ✅ On Successful Launch

* Use the **sidebar** to filter results.
* Click **"Scan Wi-Fi"** to begin detection.
* View suspicious networks marked as **⚠️ Suspicious**.

---

## 📁 Files & Structure

```plaintext
.
├── app.py                # Main Streamlit application
├── wifi_scans.csv        # Auto-generated scan history
├── README.md             # You are here!
├── requirements.txt      # Python dependencies
```

---

## ⚠️ Notes

* Ensure your system has **Wi-Fi hardware** and permissions.
* On some systems, you may need to **run as administrator** to access scan results.
* Works best over time with **multiple scans** to build historical context.

---

## ❤️ Credits

Made with Streamlit and 💡 by **EvilTwinner**

---

## 🛡️ Disclaimer

This project is for **educational and ethical use only**.
Do **not** use it to interfere with, impersonate, or manipulate legitimate networks.
