# ============================================
# CYBERTWIN SIMULATED MULTI-PLATFORM DASHBOARD
# ============================================

import streamlit as st
import numpy as np
import pandas as pd
import random
import plotly.graph_objects as go
import networkx as nx

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# ✅ NEW IMPORTS (EMAIL)
import imaplib
import email
from email.header import decode_header

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="CyberTwin Simulation", layout="wide")

# -----------------------------
# SESSION STATE
# -----------------------------
if "connected" not in st.session_state:
    st.session_state.connected = False

if "platform_data" not in st.session_state:
    st.session_state.platform_data = {}

# -----------------------------
# SYNTHETIC DATA
# -----------------------------
@st.cache_data
def generate_data(n=5000):
    data = []
    for _ in range(n):
        accounts = random.randint(1, 20)
        reuse = random.randint(0, 100)
        twofa = random.choice([0, 1])
        exposure = random.randint(0, 2)
        phishing = random.choice([0, 1])

        risk = (
            reuse * 0.3 +
            (1 - twofa) * 25 +
            exposure * 15 +
            phishing * 20 +
            accounts * 1.5
        )

        risk = min(100, int(risk))
        label = 1 if risk > 50 else 0

        data.append([accounts, reuse, twofa, exposure, phishing, label])

    return pd.DataFrame(data, columns=[
        "accounts", "reuse", "twofa", "exposure", "phishing", "risk"
    ])

# -----------------------------
# TRAIN MODELS
# -----------------------------
@st.cache_resource
def train_models():
    df = generate_data()
    X = df.drop("risk", axis=1)
    y = df["risk"]

    models = {
        "Logistic Regression": LogisticRegression(),
        "Random Forest": RandomForestClassifier(),
        "Decision Tree": DecisionTreeClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(),
        "SVM": SVC(probability=True),
        "KNN": KNeighborsClassifier()
    }

    for m in models.values():
        m.fit(X, y)

    return models

models = train_models()

# -----------------------------
# PLATFORM LIST
# -----------------------------
platforms = ["Email", "Facebook", "Instagram", "Twitter", "LinkedIn"]

# -----------------------------
# TITLE
# -----------------------------
st.title("🛡️ CyberTwin AI Simulation Dashboard")

# -----------------------------
# PLATFORM CONNECT UI
# -----------------------------
st.header("🔌 Connect Your Platforms (Simulated)")

selected_platform = st.selectbox("Choose Platform", platforms)
dummy_email = st.text_input("Enter Account ID (simulated)")
connect_btn = st.button("Connect")

if connect_btn:
    st.session_state.platform_data[selected_platform] = {
        "accounts": random.randint(1, 20),
        "reuse": random.randint(0, 100),
        "twofa": random.choice([0, 1]),
        "exposure": random.randint(0, 2),
        "phishing": random.choice([0, 1])
    }
    st.session_state.connected = True
    st.success(f"{selected_platform} connected (simulated)")

# -----------------------------
# MAIN DASHBOARD
# -----------------------------
if st.session_state.connected:

    st.header("📊 Platform Risk Overview")

    results = {}

    cols = st.columns(len(st.session_state.platform_data))

    for i, (p, data) in enumerate(st.session_state.platform_data.items()):
        risk = (
            data["reuse"] * 0.4 +
            (1 - data["twofa"]) * 25 +
            data["exposure"] * 20 +
            data["phishing"] * 20
        )
        risk = min(100, int(risk))
        results[p] = risk

        cols[i].metric(p, f"{risk}%")

    avg_data = {
        "accounts": np.mean([d["accounts"] for d in st.session_state.platform_data.values()]),
        "reuse": np.mean([d["reuse"] for d in st.session_state.platform_data.values()]),
        "twofa": int(np.mean([d["twofa"] for d in st.session_state.platform_data.values()])),
        "exposure": int(np.mean([d["exposure"] for d in st.session_state.platform_data.values()])),
        "phishing": int(np.mean([d["phishing"] for d in st.session_state.platform_data.values()]))
    }

    input_data = np.array([[ 
        avg_data["accounts"],
        avg_data["reuse"],
        avg_data["twofa"],
        avg_data["exposure"],
        avg_data["phishing"]
    ]])

    st.header("🧠 AI Risk Prediction (6 Models)")

    model_results = {}

    for name, model in models.items():
        prob = model.predict_proba(input_data)[0][1]
        model_results[name] = int(prob * 100)

    cols = st.columns(3)
    for i, (name, score) in enumerate(model_results.items()):
        cols[i % 3].metric(name, f"{score}%")

    best_model = max(model_results, key=model_results.get)
    st.success(f"🏆 Highest Risk by: {best_model}")

    final_risk = int(np.mean(list(model_results.values())))

    st.subheader("📊 Final Risk Score")
    st.progress(final_risk / 100)
    st.write(f"### {final_risk}% Overall Risk")

    df_models = pd.DataFrame(model_results.items(), columns=["Model", "Risk"])
    fig_models = go.Figure([go.Bar(x=df_models["Model"], y=df_models["Risk"])])
    st.plotly_chart(fig_models, use_container_width=True)

    st.header("⚠️ Attack Simulation")

    attack_map = {
        "Email": "Phishing → Credential Theft → Account Takeover",
        "Facebook": "Fake Friend → Malware Link → Profile Hijack",
        "Instagram": "DM Scam → Link Click → Account Compromise",
        "Twitter": "Malicious Link → Session Hijack",
        "LinkedIn": "Fake Recruiter → Data Theft"
    }

    sim_platform = st.selectbox("Select Platform for Attack", list(results.keys()))
    st.warning(attack_map[sim_platform])

    st.header("🕸️ Attack Graph")

    G = nx.DiGraph()
    G.add_edge("User", "Email")

    if avg_data["reuse"] > 50:
        G.add_edge("Email", "Social Media")

    if avg_data["phishing"]:
        G.add_edge("Phishing", "Credentials")
        G.add_edge("Credentials", "All Accounts")

    if avg_data["twofa"] == 0:
        G.add_edge("Weak Security", "Account Takeover")

    pos = nx.spring_layout(G)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines')

    node_x, node_y, text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=text,
        textposition="bottom center",
        marker=dict(size=20)
    )

    fig_graph = go.Figure(data=[edge_trace, node_trace])
    st.plotly_chart(fig_graph, use_container_width=True)

    st.header("📧 Phishing Simulation")

    emails = [
        "⚠️ Urgent! Your account is locked!",
        "🔐 Reset password immediately!"
    ]

    sample_email = random.choice(emails)
    st.write(sample_email)

    if st.button("Simulate Click"):
        st.error("🚨 Credentials Compromised!")

    st.header("🔑 Password Strength Checker")

    password = st.text_input("Enter Password", type="password")

    if password:
        score = 0
        if len(password) > 8: score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c in "!@#$%^&*" for c in password): score += 1

        if score <= 1:
            st.error("Weak Password")
        elif score == 2:
            st.warning("Moderate Password")
        else:
            st.success("Strong Password")

    st.header("🛡️ Recommendations")

    for p, r in results.items():
        if r > 70:
            st.write(f"🔴 {p}: Enable 2FA, change password")
        elif r > 40:
            st.write(f"🟠 {p}: Improve security")
        else:
            st.write(f"🟢 {p}: Good security")

    # ====================================================
    # 📩 REAL EMAIL FETCH + SPAM DETECTION (NEW FEATURE)
    # ====================================================
    st.header("📩 Email Spam Analyzer (Real Inbox)")

    def fetch_emails(username, app_password, num_emails=100):
        emails_data = []
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(username, app_password)
            mail.select("inbox")

            status, messages = mail.search(None, "ALL")
            mail_ids = messages[0].split()

            latest_ids = mail_ids[-num_emails:]

            for i in latest_ids:
                res, msg = mail.fetch(i, "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])

                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")

                        from_ = msg.get("From")

                        emails_data.append({
                            "subject": subject,
                            "from": from_
                        })

            mail.logout()

        except Exception as e:
            st.error(f"Error: {e}")

        return pd.DataFrame(emails_data)

    def detect_spam(text):
        spam_keywords = ["free", "win", "urgent", "click", "offer", "money", "prize"]
        text = str(text).lower()
        score = sum(word in text for word in spam_keywords)
        return "Spam" if score >= 2 else "Safe"

    email_user = st.text_input("Enter Gmail ID")
    email_pass = st.text_input("Enter App Password", type="password")

    if st.button("Fetch Emails"):
        df_emails = fetch_emails(email_user, email_pass)

        if not df_emails.empty:
            df_emails["Spam_Status"] = df_emails["subject"].apply(detect_spam)

            st.dataframe(df_emails)

            spam_count = (df_emails["Spam_Status"] == "Spam").sum()
            safe_count = (df_emails["Spam_Status"] == "Safe").sum()

            st.write(f"🚨 Spam Emails: {spam_count}")
            st.write(f"✅ Safe Emails: {safe_count}")