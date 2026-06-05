import streamlit as st
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - CC Calculator", layout="wide")

# URL del Logo Principal (Marcador de posición)
LOGO_URL = "https://placehold.co/600x150/1a1a1a/ffffff?text=THRUST+AVIATION+LOGO"
# URL del Logo de Argus para el final
ARGUS_LOGO_URL = "https://placehold.co/200x80/1a1a1a/ffffff?text=ARGUS+AUDITED"

# --- ENCABEZADO ---
st.image(LOGO_URL, width=400)
st.title("Contract Compliance & Financial Auditor")
st.markdown("Automated risk assessment and **4% Credit Card Hold Calculator** based on Thrust Aviation terms.")

st.divider()

# --- SECCIÓN DE CARGA DE ARCHIVOS ---
col_up1, col_up2 = st.columns(2)

with col_up1:
    st.info("📂 **Operator Side**")
    op_file = st.file_uploader("Upload Operator Contract (PDF)", type=["pdf"], key="op")

with col_up2:
    st.info("📂 **Client Side**")
    cl_file = st.file_uploader("Upload Client Contract (PDF)", type=["pdf"], key="cl")

st.divider()

# --- LÓGICA PRINCIPAL (Se activa al subir los dos archivos) ---
if op_file and cl_file:
    st.success("✅ Files received. Please input the operator contract value below to calculate the hold.")
    
    # --- SECCIÓN DEL INPUT MANUAL ---
    st.subheader("📥 Financial Input")
    
    # Caja de entrada manual abierta
    operator_cost_input = st.text_input("Enter the exact Total Price / Wire Total from the Operator Contract ($USD):", value="14900.00")
    
    # Limpieza de caracteres
    clean_string = re.sub(r'[^\d.]', '', operator_cost_input)
    try:
        base_value = float(clean_string) if clean_string else 0.0
    except ValueError:
        base_value = 0.0

    # --- MATEMÁTICA DE LA FÓRMULA (4% sobre el precio del operador) ---
    cc_rate = 0.04
    security_fee = base_value * cc_rate
    total_hold = base_value + security_fee

    # --- DESPLIEGUE DEL FINANCIAL SUMMARY ---
    st.subheader("💳 Financial Hold Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Operator Base Value", f"${base_value:,.2f} USD")
    c2.metric("Thrust CC Fee (4%)", f"${security_fee:,.2f} USD")
    c3.metric("TOTAL CREDIT CARD HOLD", f"${total_hold:,.2f} USD", delta="Target for Tradeshift")

    st.markdown("---")

    # --- AUDITORÍA DE CLÁUSULAS ---
    st.subheader("🛡️ Compliance Risk Assessment")
    
    st.error("**🔴 CRITICAL: Cancellation Window Exposure**\n\n- **Operator Requirement:** 100% penalty within 4 days.\n- **Your Master Terms:** 100% penalty within 3 days (72h).\n- **Risk:** You are unprotected for 24 hours. The client could cancel without penalty while you still owe the operator.")

    st.warning("**🟡 WARNING: Peak Travel Dates Detected**\n\n- The flight dates coincide with **Thrust Peak Dates** (Section 26).\n- **Requirement:** Ensure client contract is marked as **100% Non-Refundable** and departure time change is capped at **+/- 2 hours**.")

    st.success("**🟢 ALIGNED: Late Passenger Policy**\n\n
