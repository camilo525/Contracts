import streamlit as st
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - Compliance Copilot", layout="wide")

# URL del Logo de la empresa
LOGO_URL = "https://placehold.co/600x150/1a1a1a/ffffff?text=THRUST+AVIATION+LOGO"

# --- ENCABEZADO ---
st.image(LOGO_URL, width=400)
st.title("✈️ Thrust Aviation Holdings LLC")
st.subheader("Contract Compliance Copilot & Hold Calculator")
st.markdown("Calculate the required **4% credit card authorization hold** on operator costs and generate AI audit prompts instantly.")

st.divider()

# --- PANEL DE CONTROL COMPACTO ---
col_input, col_calc = st.columns([1, 1])

with col_input:
    st.markdown("### 📥 1. Financial Input")
    # Entrada manual del valor del contrato del operador (abierto y variable)
    operator_cost_input = st.text_input("Enter Operator Contract Net Cost ($USD):", value="14900.00")
    
    # Limpieza básica del número ingresado por el usuario
    clean_string = re.sub(r'[^\d.]', '', operator_cost_input)
    try:
        operator_net_cost = float(clean_string) if clean_string else 0.0
    except ValueError:
        operator_net_cost = 0.0

with col_calc:
    st.markdown("### 💳 2. Credit Card Hold Formula (4%)")
    # Aplicación de la fórmula exacta basada en la Sección 9 y 160 del contrato maestro
    cc_rate = 0.04
    calculated_fee = operator_net_cost * cc_rate
    total_cc_hold = operator_net_cost + calculated_fee
    
    st.metric(label="TOTAL CC HOLD AMOUNT (Target for Tradeshift)", value=f"${total_cc_hold:,.2f} USD", delta=f"+4% CC Fee: ${calculated_fee:,.2f} USD")

st.divider()

# --- ÁREA DE TRABAJO E INTEGRACIÓN ---
st.markdown("### 🚀 3. Execution & Portals")
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    st.write("Copy calculated figure for your processor:")
    st.text_input("Amount to process:", value=f"{total_cc_hold:.2f}", key="hold_val")
    st.caption("Copy this clean number directly into Tradeshift.")

with col_btn2:
    st.write("Launch Portal:")
    tradeshift_url = "https://platform.tradeshift.com/"
    st.markdown(
        f'<a href="{tradeshift_url}" target="_blank">'
        f'<button style="background-color:#FF4B4B; color:white; border:none; padding:12px 24px; '
        f'border-radius:8px; cursor:pointer; font-weight:bold; font-size:16px;">'
        f'🌐 Open Tradeshift Portal</button></a>', 
        unsafe_allow_html=True
    )

st.divider()

# --- GENERADOR DE PROMPTS DE COMPLIANCE (IA EXTERNA) ---
st.markdown("### 🛡️ 4. AI Compliance Auditor Prompt Generator")
st.write("Since cloud library limits are active, copy this customized system prompt and paste it into ChatGPT, Gemini, or Claude along with the text from your contracts to get a full risk analysis instantly.")

# Render del Prompt Dinámico en inglés que incluye las reglas de tu contrato maestro
prompt_text = f"""You are the Core Risk & Legal Compliance Auditor for Thrust Aviation. 
Analyze the upcoming "Operator Contract" and compare it against our strict "Master Client Contract Terms" to protect us from financial liability.

OUR GOLDEN RULE:
The Client Contract must ALWAYS be MORE RESTRICTIVE or EQUAL to the Operator Contract.

CRITICAL CLAUSES TO VERIFY:
1. Cancellation Penalties (Section 26):
   - One-Way Flights: 100% non-refundable immediately upon confirmation.
   - Domestic Round-Trips: > 5 days out = 30% fee | 5 days to 72 hours out = 50% fee | Within 72 hours = 100% fee.
   - International Flights: 100% non-refundable immediately.
2. Peak Travel Dates (Section 26): Any flight segment touching peak travel windows forces 100% non-refundable terms instantly and restricts schedule changes to max +/- 2 hours (Section 12).
3. Late Passenger Policy (Section 5): Passengers > 30 minutes late without prior notice are a "No Show" subject to a 100% cancellation penalty
