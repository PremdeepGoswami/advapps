import streamlit as st
import matplotlib.pyplot as plt

# ---- Page Configuration ----
st.set_page_config(
    page_title="EMI Calculator | Premdeep",
    page_icon="💰",
    layout="centered",   # or "wide" for more horizontal space
    initial_sidebar_state="expanded"
)

# ---- Custom CSS for basic styling ----
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar (acts like a nav/info panel) ----
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This EMI Calculator helps you estimate your monthly loan installment, total interest, and affordability based on your salary.")
    st.markdown("---")
    st.write("Made by **Premdeep**")

# ---- Header Section ----
st.title("💰 EMI Calculator")
st.caption("Plan your loan repayments smartly")
st.divider()

# ---- Input Section (organized in columns) ----
st.subheader("📥 Loan Details")

col1, col2 = st.columns(2)
with col1:
    Principal_Loan_Amount = st.number_input("Loan Amount (₹)", min_value=0.0)
    Tenure_type = st.selectbox("Tenure Unit", ["Months", "Years"])
    Monthly_income = st.number_input("Monthly Salary (₹)", min_value=0.0)
with col2:
    Annual_Interest_Rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    Tenure = st.number_input("Loan Tenure", min_value=1)

st.divider()

# ---- Calculate Button ----
if st.button("Calculate EMI"):
    # Convert tenure to months
    months = Tenure * 12 if Tenure_type == "Years" else Tenure

    # Monthly interest rate
    monthly_rate = (Annual_Interest_Rate / 12) / 100

    # EMI Calculation
    if monthly_rate > 0:
        emi = (
            Principal_Loan_Amount
            * monthly_rate
            * (1 + monthly_rate) ** months
        ) / (((1 + monthly_rate) ** months) - 1)
    else:
        emi = Principal_Loan_Amount / months

    total_payment = emi * months
    total_interest = total_payment - Principal_Loan_Amount

    # ---- Results Section ----
    st.subheader("📋 EMI Result")

    r1, r2, r3 = st.columns(3)
    r1.metric("Monthly EMI", f"₹{emi:,.2f}")
    r2.metric("Total Payment", f"₹{total_payment:,.2f}")
    r3.metric("Total Interest", f"₹{total_interest:,.2f}")

    st.write(f"**Loan Tenure:** {int(months)} months")

    # Optional: EMI as % of salary
    if Monthly_income > 0:
        emi_percent = (emi / Monthly_income) * 100
        st.write(f"EMI is **{emi_percent:.1f}%** of your monthly salary.")
        if emi_percent <= 40:
            st.success("✅ Your EMI is within a comfortable range.")
        else:
            st.warning("⚠️ Your EMI is more than 40% of your salary.")

    # ---- Pie Chart ----
    st.subheader("📊 Principal vs Interest Breakdown")
    fig, ax = plt.subplots()
    ax.pie(
        [Principal_Loan_Amount, total_interest],
        labels=["Principal", "Interest"],
        autopct="%1.1f%%",
        colors=["#4CAF50", "#e63946"],
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)
