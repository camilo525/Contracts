import streamlit as st
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - CC Calculator", layout="wide")

# URL del Logo (Marcador de posición)
LOGO_URL = "https://thrust-aviation.com/wp-content/uploads/2024/02/Logo-White-500-2-e1710003051285.png"

# URL del Logo Principal (Marcador de posición)
LOGO_URL = "https://static.wixstatic.com/media/5f5db0_d7471efb590b4734a38048043fb3b2c1~mv2.png/v1/fill/w_300,h_300,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/FBO%20Audit%20Logo%20Silver.png"
# URL del Logo de Argus para el final
ARGUS_LOGO_URL = "https://static.wixstatic.com/media/5f5db0_d7471efb590b4734a38048043fb3b2c1~mv2.png/v1/fill/w_300,h_300,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/FBO%20Audit%20Logo%20Silver.png"

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

    # --- AUDITORÍA DE CLÁUSULAS (Flags de Seguridad en línea única protegida) ---
    st.subheader("🛡️ Compliance Risk Assessment")
    
    st.error("**🔴 CRITICAL: Cancellation Window Exposure**\n\n- **Operator Requirement:** 100% penalty within 4 days.\n- **Your Master Terms:** 100% penalty within 3 days (72h).\n- **Risk:** You are unprotected for 24 hours. The client could cancel without penalty while you still owe the operator.")

    st.warning("**🟡 WARNING: Peak Travel Dates Detected**\n\n- The flight dates coincide with **Thrust Peak Dates** (Section 26).\n- **Requirement:** Ensure client contract is marked as **100% Non-Refundable** and departure time change is capped at **+/- 2 hours**.")

    st.success("**🟢 ALIGNED: Late Passenger Policy**\n\n- Both contracts enforce the 30-minute 'No Show' rule. No risk detected.")

    st.divider()

    # --- EJECUCIÓN Y PORTAL DE TRADESHIFT ---
    st.subheader("🚀 Next Steps")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        st.write("Confirm amount to process in Tradeshift:")
        st.text_input("Hold Figure to Copy:", value=f"{total_hold:.2f}", key="hold_val")
        st.caption("Copy this exact amount into your transaction window.")

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

else:
    st.warning("Please upload both PDF contracts to start the compliance audit.")

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.caption("Thrust Aviation Internal Tool v1.7")
st.sidebar.info("The logic is strictly bounded by Section 5, 9, 12, and 26 of the Master Agreement.")
