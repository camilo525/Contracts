import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - Smart Auditor", layout="wide")

# URL del Logo (Reemplaza esta URL por la ruta de tu logo real cuando lo tengas)
LOGO_URL = "https://thrust-aviation.com/wp-content/uploads/2024/02/Logo-White-500-2-e1710003051285.png"

# --- ENCABEZADO ---
st.image(LOGO_URL, width=400)
st.title("Contract Compliance & Financial Auditor")
st.markdown("Automated risk assessment based on **Thrust Aviation Holdings LLC** master terms.")

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

# --- LÓGICA PRINCIPAL (Solo se activa si hay archivos) ---
if op_file and cl_file:
    st.success("✅ Files received. Analyzing clauses and financial holds...")
    
    # 1. CÁLCULOS FINANCIEROS (Basado en tu fórmula de 5%)
    # Simulamos que la IA extrajo 14,900.00 del contrato del operador
    base_value = 14900.00 
    hold_percentage = 0.05
    security_fee = base_value * hold_percentage
    total_hold = base_value + security_fee

    st.subheader("💳 Financial Hold Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Operator Base Value", f"${base_value:,.2f}")
    c2.metric("OPR Hold Fee (5%)", f"${security_fee:,.2f}")
    c3.metric("TOTAL CREDIT CARD HOLD", f"${total_hold:,.2f}", delta="Target for Tradeshift")

    st.markdown("---")

    # 2. AUDITORÍA DE CLÁUSULAS (Flags de Seguridad)
    st.subheader("🛡️ Compliance Risk Assessment")
    
    # Flag Crítica (Simulada para el ejemplo)
    st.error("""
    **🔴 CRITICAL: Cancellation Window Exposure**
    - **Operator Requirement:** 100% penalty within 4 days.
    - **Your Master Terms:** 100% penalty within 3 days (72h).
    - **Risk:** You are unprotected for 24 hours. The client could cancel without penalty while you still owe the operator.
    """)

    # Flag de Peak Travel
    st.warning("""
    **🟡 WARNING: Peak Travel Dates Detected**
    - The flight dates coincide with **Thrust Peak Dates** (Section 26).
    - **Requirement:** Ensure client contract is marked as **100% Non-Refundable** and departure time change is capped at **+/- 2 hours**.
    """)

    # Flag de Éxito
    st.success("""
    **🟢 ALIGNED: Late Passenger Policy**
    - Both contracts enforce the 30-minute 'No Show' rule. No risk detected.
    """)
