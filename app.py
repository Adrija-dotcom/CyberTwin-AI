# ============================================
# CYBER AI DASHBOARD
# Machine-Learning-Powered Cybersecurity
# Simulation Dashboard
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

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Cyber AI Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# ============================================
# SESSION STATE
# ============================================

if "connected" not in st.session_state:
    st.session_state.connected = False

if "platform_data" not in st.session_state:
    st.session_state.platform_data = {}


# ============================================
# SYNTHETIC DATA GENERATION
# ============================================

@st.cache_data
def generate_data(n=5000):

    data = []

    for _ in range(n):

        accounts = random.randint(1, 20)
        reuse = random.randint(0, 100)
        twofa = random.choice([0, 1])
        exposure = random.randint(0, 2)
        phishing = random.choice([0, 1])

        risk_score = (
            reuse * 0.3 +
            (1 - twofa) * 25 +
            exposure * 15 +
            phishing * 20 +
            accounts * 1.5
        )

        risk_score = min(100, int(risk_score))

        # Binary risk label
        label = 1 if risk_score > 50 else 0

        data.append([
            accounts,
            reuse,
            twofa,
            exposure,
            phishing,
            label
        ])

    return pd.DataFrame(
        data,
        columns=[
            "accounts",
            "reuse",
            "twofa",
            "exposure",
            "phishing",
            "risk"
        ]
    )


# ============================================
# TRAIN AND EVALUATE ML MODELS
# ============================================

@st.cache_resource
def train_models():

    df = generate_data()

    X = df.drop("risk", axis=1)
    y = df["risk"]

    # ----------------------------------------
    # Train/Test Split
    # ----------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # ----------------------------------------
    # Models
    # ----------------------------------------

    models = {

        "Logistic Regression":
            LogisticRegression(max_iter=1000),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=100,
                random_state=42
            ),

        "Decision Tree":
            DecisionTreeClassifier(
                random_state=42
            ),

        "Gradient Boosting":
            GradientBoostingClassifier(
                random_state=42
            ),

        "SVM":
            SVC(
                probability=True,
                random_state=42
            ),

        "KNN":
            KNeighborsClassifier()
    }

    # ----------------------------------------
    # Evaluation
    # ----------------------------------------

    evaluation_results = {}

    for name, model in models.items():

        # Train model
        model.fit(X_train, y_train)

        # Predictions
        predictions = model.predict(X_test)

        # Metrics
        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        # ------------------------------------
        # 5-Fold Cross Validation
        # ------------------------------------

        cv_scores = cross_val_score(
            model,
            X,
            y,
            cv=5,
            scoring="accuracy"
        )

        # ------------------------------------
        # Confusion Matrix
        # ------------------------------------

        cm = confusion_matrix(
            y_test,
            predictions
        )

        evaluation_results[name] = {

            "Accuracy": accuracy,

            "Precision": precision,

            "Recall": recall,

            "F1 Score": f1,

            "CV Accuracy": cv_scores.mean(),

            "Confusion Matrix": cm
        }

    return models, evaluation_results


# ============================================
# TRAIN MODELS
# ============================================

models, evaluation_results = train_models()


# ============================================
# PLATFORM SIMULATION
# ============================================

platforms = [
    "Email",
    "Facebook",
    "Instagram",
    "Twitter",
    "LinkedIn"
]


# ============================================
# MAIN TITLE
# ============================================

st.title("🛡️ Cyber AI Dashboard")

st.caption(
    "Machine-Learning-Powered Cybersecurity Simulation Dashboard"
)


# ============================================
# SIMULATED PLATFORM CONNECTION
# ============================================

st.header("🔌 Connect Your Platforms (Simulated)")

selected_platform = st.selectbox(
    "Choose Platform",
    platforms
)

dummy_email = st.text_input(
    "Enter Account ID (simulated)"
)

connect_btn = st.button(
    "Connect"
)


if connect_btn:

    st.session_state.platform_data[selected_platform] = {

        "accounts": random.randint(1, 20),

        "reuse": random.randint(0, 100),

        "twofa": random.choice([0, 1]),

        "exposure": random.randint(0, 2),

        "phishing": random.choice([0, 1])
    }

    st.session_state.connected = True

    st.success(
        f"{selected_platform} connected (simulated)"
    )


# ============================================
# PLATFORM RISK ANALYSIS
# ============================================

if st.session_state.connected:

    st.header("📊 Platform Risk Overview")

    results = {}

    cols = st.columns(
        len(st.session_state.platform_data)
    )

    for i, (platform, data) in enumerate(
        st.session_state.platform_data.items()
    ):

        risk = (
            data["reuse"] * 0.4 +
            (1 - data["twofa"]) * 25 +
            data["exposure"] * 20 +
            data["phishing"] * 20
        )

        risk = min(
            100,
            int(risk)
        )

        results[platform] = risk

        cols[i].metric(
            platform,
            f"{risk}%"
        )


    # ========================================
    # AVERAGE SECURITY FEATURES
    # ========================================

    avg_data = {

        "accounts":
            np.mean([
                d["accounts"]
                for d in st.session_state.platform_data.values()
            ]),

        "reuse":
            np.mean([
                d["reuse"]
                for d in st.session_state.platform_data.values()
            ]),

        "twofa":
            int(np.mean([
                d["twofa"]
                for d in st.session_state.platform_data.values()
            ])),

        "exposure":
            int(np.mean([
                d["exposure"]
                for d in st.session_state.platform_data.values()
            ])),

        "phishing":
            int(np.mean([
                d["phishing"]
                for d in st.session_state.platform_data.values()
            ]))
    }


    # ========================================
    # ML RISK PREDICTION
    # ========================================

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

        probability = model.predict_proba(
            input_data
        )[0][1]

        model_results[name] = int(
            probability * 100
        )


    # Display model predictions

    cols = st.columns(3)

    for i, (name, score) in enumerate(
        model_results.items()
    ):

        cols[i % 3].metric(
            name,
            f"{score}%"
        )


    # Highest risk model

    best_model = max(
        model_results,
        key=model_results.get
    )

    st.success(
        f"🏆 Highest Risk Prediction: {best_model}"
    )


    # Overall risk

    final_risk = int(
        np.mean(
            list(model_results.values())
        )
    )

    st.subheader("📊 Final Risk Score")

    st.progress(
        final_risk / 100
    )

    st.write(
        f"### {final_risk}% Overall Risk"
    )


    # ========================================
    # MODEL RISK CHART
    # ========================================

    df_models = pd.DataFrame(
        model_results.items(),
        columns=["Model", "Risk"]
    )

    fig_models = go.Figure(
        [
            go.Bar(
                x=df_models["Model"],
                y=df_models["Risk"]
            )
        ]
    )

    fig_models.update_layout(
        title="Risk Prediction by ML Model",
        yaxis_title="Risk (%)",
        xaxis_title="Model"
    )

    st.plotly_chart(
        fig_models,
        use_container_width=True
    )


    # ========================================
    # MODEL EVALUATION
    # ========================================

    st.header("📈 Model Evaluation")

    evaluation_table = []


    for name, metrics in evaluation_results.items():

        evaluation_table.append({

            "Model":
                name,

            "Accuracy":
                round(
                    metrics["Accuracy"] * 100,
                    2
                ),

            "Precision":
                round(
                    metrics["Precision"] * 100,
                    2
                ),

            "Recall":
                round(
                    metrics["Recall"] * 100,
                    2
                ),

            "F1 Score":
                round(
                    metrics["F1 Score"] * 100,
                    2
                ),

            "5-Fold CV Accuracy":
                round(
                    metrics["CV Accuracy"] * 100,
                    2
                )
        })


    evaluation_df = pd.DataFrame(
        evaluation_table
    )


    st.dataframe(
        evaluation_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================
    # CONFUSION MATRIX
    # ========================================

    st.subheader("🔢 Confusion Matrix")

    selected_model = st.selectbox(
        "Select Model for Confusion Matrix",
        list(evaluation_results.keys())
    )


    cm = evaluation_results[
        selected_model
    ]["Confusion Matrix"]


    cm_df = pd.DataFrame(

        cm,

        index=[
            "Actual Low Risk",
            "Actual High Risk"
        ],

        columns=[
            "Predicted Low Risk",
            "Predicted High Risk"
        ]
    )


    st.dataframe(
        cm_df,
        use_container_width=True
    )


    # ========================================
    # ATTACK SIMULATION
    # ========================================

    st.header("⚠️ Attack Simulation")


    attack_map = {

        "Email":
            "Phishing → Credential Theft → Account Takeover",

        "Facebook":
            "Fake Friend → Malware Link → Profile Hijack",

        "Instagram":
            "DM Scam → Link Click → Account Compromise",

        "Twitter":
            "Malicious Link → Session Hijack",

        "LinkedIn":
            "Fake Recruiter → Data Theft"
    }


    sim_platform = st.selectbox(
        "Select Platform for Attack",
        list(results.keys())
    )


    st.warning(
        attack_map[sim_platform]
    )


    # ========================================
    # ATTACK GRAPH
    # ========================================

    st.header("🕸️ Attack Graph")


    G = nx.DiGraph()

    G.add_edge(
        "User",
        "Email"
    )


    if avg_data["reuse"] > 50:

        G.add_edge(
            "Email",
            "Social Media"
        )


    if avg_data["phishing"]:

        G.add_edge(
            "Phishing",
            "Credentials"
        )

        G.add_edge(
            "Credentials",
            "All Accounts"
        )


    if avg_data["twofa"] == 0:

        G.add_edge(
            "Weak Security",
            "Account Takeover"
        )


    pos = nx.spring_layout(
        G,
        seed=42
    )


    edge_x = []
    edge_y = []


    for edge in G.edges():

        x0, y0 = pos[edge[0]]

        x1, y1 = pos[edge[1]]

        edge_x += [
            x0,
            x1,
            None
        ]

        edge_y += [
            y0,
            y1,
            None
        ]


    edge_trace = go.Scatter(

        x=edge_x,

        y=edge_y,

        mode="lines",

        hoverinfo="none"
    )


    node_x = []
    node_y = []
    text = []


    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)

        node_y.append(y)

        text.append(node)


    node_trace = go.Scatter(

        x=node_x,

        y=node_y,

        mode="markers+text",

        text=text,

        textposition="bottom center",

        marker=dict(
            size=20
        )
    )


    fig_graph = go.Figure(
        data=[
            edge_trace,
            node_trace
        ]
    )


    fig_graph.update_layout(
        title="Simulated Attack Propagation Graph",
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False
        )
    )


    st.plotly_chart(
        fig_graph,
        use_container_width=True
    )


    # ========================================
    # PHISHING SIMULATION
    # ========================================

    st.header("📧 Phishing Simulation")


    emails = [

        "⚠️ Urgent! Your account is locked!",

        "🔐 Reset password immediately!"
    ]


    sample_email = random.choice(
        emails
    )


    st.write(
        sample_email
    )


    if st.button(
        "Simulate Click"
    ):

        st.error(
            "🚨 Credentials Compromised!"
        )


    # ========================================
    # PASSWORD STRENGTH CHECKER
    # ========================================

    st.header("🔑 Password Strength Checker")


    password = st.text_input(
        "Enter Password",
        type="password"
    )


    if password:

        score = 0


        if len(password) > 8:

            score += 1


        if any(
            c.isdigit()
            for c in password
        ):

            score += 1


        if any(
            c.isupper()
            for c in password
        ):

            score += 1


        if any(
            c in "!@#$%^&*"
            for c in password
        ):

            score += 1


        if score <= 1:

            st.error(
                "Weak Password"
            )

        elif score == 2:

            st.warning(
                "Moderate Password"
            )

        else:

            st.success(
                "Strong Password"
            )


    # ========================================
    # SECURITY RECOMMENDATIONS
    # ========================================

    st.header("🛡️ Security Recommendations")


    for platform, risk in results.items():

        if risk > 70:

            st.write(
                f"🔴 {platform}: "
                "Enable 2FA and change password"
            )

        elif risk > 40:

            st.write(
                f"🟠 {platform}: "
                "Improve security"
            )

        else:

            st.write(
                f"🟢 {platform}: "
                "Good security posture"
            )
            # ============================================
# EMAIL SPAM ANALYZER
# ============================================

st.header("📩 Email Spam Analyzer")

st.write(
    "Analyze a sample email or paste your own email content "
    "to identify potential spam and phishing indicators."
)

sample_emails = {
    "🚨 Phishing Email": {
        "subject": "URGENT: Your account has been suspended!",
        "body": (
            "Your account has been temporarily suspended. "
            "Click here immediately to verify your password and "
            "restore access to your account."
        )
    },

    "💰 Prize Scam": {
        "subject": "Congratulations! You won $10,000!",
        "body": (
            "Congratulations! You have won a cash prize of $10,000. "
            "Click the link now to claim your money. "
            "You must provide your account information immediately."
        )
    },

    "📢 Promotional Spam": {
        "subject": "FREE OFFER - Limited Time Deal!",
        "body": (
            "Get an exclusive free offer today! "
            "Click now to claim your special discount and prize."
        )
    },

    "✅ Legitimate Email": {
        "subject": "Your project meeting is scheduled for tomorrow",
        "body": (
            "Hi team, our project meeting is scheduled for tomorrow "
            "at 10 AM. Please review the latest project updates "
            "before the meeting."
        )
    }
}

# Choose a sample email
selected_sample = st.selectbox(
    "Choose a sample email",
    list(sample_emails.keys())
)

sample = sample_emails[selected_sample]

# Email subject
email_subject = st.text_input(
    "Email Subject",
    value=sample["subject"],
    key="spam_subject"
)

# Email body
email_body = st.text_area(
    "Email Content",
    value=sample["body"],
    height=150,
    key="spam_body"
)

# Analyze button
analyze_email = st.button("🔍 Analyze Email")

if analyze_email:

    email_text = (
        email_subject + " " + email_body
    ).lower()

    # Suspicious indicators
    indicators = {
        "urgent": "Urgency language",
        "immediately": "Pressure to act immediately",
        "click": "Suspicious call-to-action",
        "verify": "Account verification request",
        "password": "Credential/password request",
        "account information": "Request for sensitive information",
        "won": "Prize/reward language",
        "prize": "Prize/reward language",
        "free": "Promotional/free-offer language",
        "money": "Financial language",
        "$": "Financial language",
        "claim": "Prize/offer claim request"
    }

    detected_indicators = []

    for keyword, description in indicators.items():

        if keyword in email_text:
            detected_indicators.append(description)

    # Remove duplicates
    detected_indicators = list(
        dict.fromkeys(detected_indicators)
    )

    # Calculate risk score
    risk_score = min(
        100,
        len(detected_indicators) * 15
    )

    # Strong indicators
    strong_keywords = [
        "password",
        "account information",
        "verify",
        "click",
        "won",
        "prize"
    ]

    strong_matches = sum(
        1
        for keyword in strong_keywords
        if keyword in email_text
    )

    risk_score = min(
        100,
        risk_score + strong_matches * 5
    )

    # Classification
    if risk_score >= 50:

        classification = "🚨 SPAM / PHISHING"

    elif risk_score >= 25:

        classification = "⚠️ SUSPICIOUS"

    else:

        classification = "✅ LIKELY LEGITIMATE"

    st.divider()

    st.subheader("📊 Email Analysis Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Classification",
            classification
        )

    with col2:
        st.metric(
            "Risk Score",
            f"{risk_score}%"
        )

    st.progress(risk_score / 100)

    # Detected indicators
    if detected_indicators:

        st.subheader("🔎 Detected Indicators")

        for indicator in detected_indicators:
            st.write(f"• {indicator}")

    else:

        st.success(
            "No major spam or phishing indicators were detected."
        )

    # Recommendation
    st.subheader("🛡️ Security Recommendation")

    if risk_score >= 50:

        st.error(
            "Avoid clicking links or providing passwords, "
            "financial information, or other sensitive data."
        )

    elif risk_score >= 25:

        st.warning(
            "Verify the sender and email content before taking action."
        )

    else:

        st.success(
            "The email appears relatively safe, but always verify "
            "unexpected requests independently."
        )