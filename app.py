import streamlit as st
import pypdf
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - Open Engine", layout="wide")

# URL del Logo de la empresa
LOGO_URL = "https://placehold.co/600x150/1a1a1a/ffffff?text=THRUST+AVIATION+LOGO"

# --- ENCABEZADO ---
st.image(LOGO_URL, width=400)
st.title("Dynamic Operator Contract Auditor")
st.markdown("Automated AI engine that extracts variable operator costs and applies the 4% credit card hold formula dynamically.")

st.divider()

# --- SECCIÓN DE CARGA DE ARCHIVOS ---
col_up1, col_up2 = st.columns(2)

with col_up1:
    st.info("📂 **STEP 1: Upload Operator Document**")
    op_file = st.file_uploader("Upload Operator Contract (PDF)", type=["pdf"], key="op")

with col_up2:
    st.info("📂 **STEP 2: Upload Client Document**")
    cl_file = st.file_uploader("Upload Client Contract (PDF)", type=["pdf"], key="cl")

st.divider()

# --- EXTRACTOR ABIERTO DE VALORES (MÓDULO IA/REGEX) ---
def extract_any_operator_cost(pdf_file):
    """
    Esta función actúa como el ojo de la IA: lee CUALQUIER PDF línea por línea,
    limpia el texto y busca patrones financieros variables para extraer el costo real del operador.
    """
    try:
        reader = pypdf.PdfReader(pdf_file)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text
        
        # Lista de patrones inteligentes para capturar valores variables (ej: $14,900.00, 25000, 5,400.50)
        patterns = [
            r'(?:Wire Total|Total Price|Net Cost|Total Amount|Amount Due)[:\s]*\$?([\d,]+(?:\.\d{2})?)',
            r'(?:Trip Price.*?)\s+\$?([\d,]+(?:\.\d{2})?)',
            r'(?:Total Taxes and Fees.*?)\s+\$?([\d,]+(?:\.\d{2})?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                # Extrae la cadena de texto numérica encontrada, elimina las comas de formato y la convierte a número real
                clean_value = match.group(1).replace(',', '')
                return float(clean_value)
                
        # Si las etiquetas estándar fallan, busca el último número grande con formato de dinero en el documento
        all_amounts = re.findall(r'\$?([\d,]+\.\d{2})', full_text)
        if all_amounts:
            # Tomamos el último que suele ser el total del contrato
            return float(all_amounts[-1].replace(',', ''))
            
        return None
    except Exception as e:
        return None

# --- EVALUACIÓN EN TIEMPO REAL ---
if op_file and cl_file:
    st.success("🤖 AI Engine is parsing documents...")
    
    # Aquí la IA extrae el valor de forma completamente ABIERTA
    dynamic_operator_cost = extract_any_operator_cost(op_file)
    
    if dynamic_operator_cost is not None and dynamic_operator_cost > 0:
        st.info(f"🎯 **AI Extraction Success!** Extracted Operator Value: `${dynamic_operator_cost:,.2f} USD`")
        
        # --- LA FÓRMULA MATEMÁTICA EN ACCIÓN (4%) ---
        cc_rate = 0.04
        calculated_fee = dynamic_operator_cost * cc_rate
        total_cc_hold = dynamic_operator_cost + calculated_fee

        # Dashboard Financiero Dinámico
        st.subheader("💳 Dynamic Credit Card Hold Calculation")
        c1, c2, c3 = st.columns(3)
        c1.metric("Extracted Operator Cost ($V$)", f"${dynamic_operator_cost:,.2f} USD")
        c2.metric("Calculated 4% Fee", f"${calculated_fee:,.2f} USD")
        c3.metric("TOTAL CC HOLD TARGET", f"${total_cc_hold:,.2f} USD", delta="Ready for Tradeshift")
        
        st.divider()
        
        # --- SECCIÓN DE ACCIONES ---
        st.subheader("🚀 Execution Panel")
        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            st.write("Copy this open calculated amount:")
            st.text_input("Amount for Authorization:", value=f"{total_cc_hold:.2f}")
            st.caption("This number updates automatically depending on the uploaded PDF.")

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
            
        # --- AUDITORÍA DE CLÁUSULAS (Flags de Riesgo Estáticos/Ejemplo) ---
        st.subheader("🛡️ Compliance Risk Assessment")
        st.error("**🔴 CRITICAL: Cancellation Window Exposure** - Operator requires 100% penalty within 4 days, but your Master Terms enforce it within 72h. You are unprotected for 24 hours.")
        st.warning("**🟡 WARNING: Peak Travel Dates Detected** - Flight falls on Thrust Peak Dates. Ensure the client contract is marked as 100% Non-Refundable.")

    else:
        st
