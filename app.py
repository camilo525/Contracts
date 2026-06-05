import streamlit as st

# Configuración de la página en inglés
st.set_page_config(page_title="Thrust Aviation - Compliance Auditing Tool", layout="wide")

st.title("✈️ Thrust Aviation Holdings LLC")
st.subheader("Contract Compliance & Smart Risk Auditor Engine")
st.write("Upload the Operator contract to evaluate financial exposure and automatically calculate the required credit card authorization hold.")

st.markdown("---")

# 1. Zona de Carga de Archivos (UI)
col1, col2 = st.columns(2)

with col1:
    operator_file = st.file_uploader("📁 Upload Operator Contract (PDF)", type=["pdf"])

with col2:
    client_file = st.file_uploader("📁 Upload Client Contract (PDF)", type=["pdf"])

st.markdown("---")

# Valores de prueba simulando la extracción de la IA si se sube un archivo
if operator_file and client_file:
    st.success("✅ Both contracts uploaded successfully! Running AI Restrictiveness Check...")
    
    # Simulación de extracción de valor base (puedes cambiar este número para probar)
    base_value = 14900.00 
    
    # 2. Bloque de Cálculo Financiero (Fórmula Matemática)
    # Valor del contrato + 5% para el Hold de la tarjeta
    hold_amount = base_value * 1.05
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric(label="Extracted Operator Base Value", value=f"${base_value:,.2f} USD")
    with col_stat2:
        st.metric(label="Thrust Security Fee (5%)", value=f"${base_value * 0.05:,.2f} USD")
    with col_stat3:
        st.metric(label="Total Credit Card Hold Amount", value=f"${hold_amount:,.2f} USD")
        
    st.markdown("### 🛡️ AI Compliance & Liability Guard Report")
    
    # 3. Panel de control de Flags basado en tus cláusulas reales
    st.markdown("#### 🔴 Critical Discrepancies (Risk Detected)")
    st.error("""
    **CRITICAL FLAG: Cancellation Window Deficit Detected**
    * **Operator Policy:** Requires 100% non-refundable penalty within 4 days of departure.
    * **Your Master Terms:** Only enforces 100% penalty within 72 hours (3 days) of departure.
    * **Financial Exposure:** You have a 24-hour blind spot where the client can cancel for free with you, but you will still owe 100% to the operator.
    * *Recommendation:* Manually amend the Client Contract Section 26 for this trip to require a minimum 4-day cancellation window.
    """)
    
    st.markdown("#### 🟡 Warnings")
    st.warning("""
    **PEAK TRAVEL CALENDAR WARNING**
    * The flight itinerary dates match the **Thrust Peak Travel Schedule** (Section 26). 
    * Ensure the client contract strictly enforces **100% non-refundable terms immediately** and caps schedule changes to **+/- 2 hours max**.
    """)
    
    st.markdown("#### 🟢 Aligned & Safe Clauses")
    st.success("""
    **Late Passenger Policy Approved**
    * Both contracts successfully dictate a hard 30-minute cutoff rule for passenger delays before a 100% forfeiture applies.
    """)
    
    st.markdown("---")
    
    # 4. Integración con Tradeshift y portapapeles
    st.markdown("### 🚀 Next Steps & Execution")
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        # Botón para copiar la cifra exacta fácilmente
        st.text_input("Copy Hold Amount for Tradeshift:", value=f"{hold_amount:.2f}")
        st.caption("Copy this number directly into your transaction window.")
        
    with col_btn2:
        st.write("") # Espaciador
        st.write("") 
        # Enlace directo que simula el botón abriendo Tradeshift en una nueva pestaña
        tradeshift_url = "https://platform.tradeshift.com/"
       st.markdown(f'<a href="{tradeshift_url}" target="_blank"><button style="background-color:#FF4B4B; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-size:16px;">🌐 Open Tradeshift Portal</button></a>', unsafe_allow_html=True)

else:
    st.info("💡 Please upload both the Operator and Client PDF files above to simulate the compliance analysis.")
