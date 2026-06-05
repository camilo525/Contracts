import streamlit as st
import json
import urllib.request
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - Smart AI Auditor", layout="wide")

LOGO_URL = "https://placehold.co/600x150/1a1a1a/ffffff?text=THRUST+AVIATION+LOGO"
st.image(LOGO_URL, width=400)
st.title("Contract Compliance & AI Financial Auditor")
st.markdown("Automated value extraction and **4% Credit Card Hold Calculation**.")

st.divider()

# --- CONFIGURACIÓN DE LA API KEY EN LA SIDEBAR ---
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
if not api_key:
    st.sidebar.warning("⚠️ Please enter your OpenAI API Key to activate the automatic PDF extraction.")

# --- SECCIÓN DE CARGA DE ARCHIVOS ---
col_up1, col_up2 = st.columns(2)

with col_up1:
    st.info("📂 **Operator Side**")
    op_file = st.file_uploader("Upload Operator Contract (PDF)", type=["pdf"], key="op")

with col_up2:
    st.info("📂 **Client Side**")
    cl_file = st.file_uploader("Upload Client Contract (PDF)", type=["pdf"], key="cl")

st.divider()

# --- FUNCIÓN LIGERA PARA EXTRAER TEXTO ---
def fast_pdf_to_text(uploaded_file):
    if uploaded_file is None:
        return ""
    try:
        binary_data = uploaded_file.read()
        text = binary_data.decode('utf-8', errors='ignore')
        clean_text = "".join([c for c in text if c.isalnum() or c in " \n.,:$-\n"])
        return clean_text[:4000]
    except:
        return ""

# --- LÓGICA PRINCIPAL ---
if op_file and cl_file:
    st.success("✅ Files received.")
    
    # Valor base de respaldo (Don Mcgrath Example)
    detected_value = 14900.00 
    
    if api_key:
        with st.spinner("🤖 AI is reading the Operator PDF to extract the contract value..."):
            raw_text = fast_pdf_to_text(op_file)
            
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            # Estructura JSON corregida detalladamente línea por línea
            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a financial auditor. Look at the text and extract ONLY the total wire contract price or net value as a plain number. No symbols, no commas. Example: 14900.00"},
                    {"role": "user", "content": f"Extract the contract value from this text:\n\n{raw_text}"}
                ],
                "temperature": 0.0
            }
            
            try:
                # Envío seguro de la petición HTTP
                req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    ai_result = res_data['choices'][0]['message']['content'].strip()
                    detected_value = float(re.sub(r'[^\d.]', '', ai_result))
                    st.info(f"🎯 AI successfully extracted the value from the document!")
            except:
                st.warning("⚠️ AI Extraction failed or PDF text is not selectable. Using baseline template value ($14,900.00).")

    # --- INPUT MANUAL (Rellenado automáticamente o modificable por ti) ---
    st.subheader("📥 Financial Verification")
    operator_cost_input = st.text_input(
        "Verify or update the Operator Contract Net Cost ($USD):", 
        value=f"{detected_value:.2f}"
    )
    
    clean_string = re.sub(r'[^\d.]', '', operator_cost_input)
    try:
        base_value = float(clean_string) if clean_string else 0.0
    except ValueError:
        base_value = 0.0

    # --- MATEMÁTICA DEL 4% ---
    cc_rate = 0.04  # 4% según Sección 9 del contrato maestro
    security_fee = base_value * cc_rate
    total_hold = base_value + security_fee

    # --- DESPLIEGUE DEL SUMMARY ---
    st.subheader("💳 Financial Hold Summary")
    c1, c2, c3 = st.columns(3)
    c
    
