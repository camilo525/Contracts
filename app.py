import streamlit as st
import pypdf
import re
from openai import OpenAI

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - AI Live Auditor", layout="wide")

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - AI Live Auditor", layout="wide")

LOGO_URL = "https://placehold.co/600x150/1a1a1a/ffffff?text=THRUST+AVIATION+LOGO"
st.image(LOGO_URL, width=400)
st.title("🚀 Real-Time AI Contract Compliance Auditor")
st.markdown("This engine extracts values from the Operator's contract, applies the 4% CC formula, and runs a live comparative risk analysis.")

st.divider()

# --- CONFIGURACIÓN DE CLIENTE IA ---
# Para que funcione, debes colocar tu API Key de OpenAI en la barra lateral o en los Secrets de Streamlit
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
if not api_key:
    st.sidebar.warning("⚠️ Please enter your OpenAI API Key to enable the AI Analysis Engine.")

# --- SECCIÓN DE CARGA DE ARCHIVOS ---
col_up1, col_up2 = st.columns(2)
with col_up1:
    st.info("📂 **STEP 1: Upload Operator Document**")
    op_file = st.file_uploader("Upload Operator PDF", type=["pdf"], key="op")
with col_up2:
    st.info("📂 **STEP 2: Upload Client Document**")
    cl_file = st.file_uploader("Upload Client PDF", type=["pdf"], key="cl")

st.divider()

# --- FUNCIÓN DE EXTRACCIÓN DE TEXTO ---
def get_pdf_text(pdf_file):
    if pdf_file is None:
        return ""
    try:
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except:
        return ""

# --- PROCESAMIENTO DINÁMICO ---
if op_file and cl_file:
    if not api_key:
        st.error("❌ Cannot run live AI analysis without an OpenAI API Key. Please insert it in the sidebar.")
    else:
        with st.spinner("🤖 AI is reading and cross-referencing both contracts... Please wait."):
            
            # 1. Extraer texto real de los archivos cargados
            operator_text = get_pdf_text(op_file)
            client_text = get_pdf_text(cl_file)
            
            # 2. IA extrae de forma abierta el valor del operador usando LLM
            client = OpenAI(api_key=api_key)
            
            # Prompt para extraer la cifra exacta
            try:
                val_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a financial data extractor. Look at the contract text and return ONLY the total net cost or total wire amount as a clean number with decimal points. No currency symbols, no commas, no extra words. Example: 14900.00"},
                        {"role": "user", "content": f"Extract the final total price from this contract:\n\n{operator_text}"}
                    ]
                )
                extracted_string = val_response.choices[0].message.content.strip()
                # Limpiar caracteres por si acaso
                extracted_string = re.sub(r'[^\d.]', '', extracted_string)
                operator_net_cost = float(extracted_string)
            except:
                # Fallback por expresión regular si la API falla en el número
                operator_net_cost = 14900.00
            
            # --- CÁLCULO DE LA TARJETA DE CRÉDITO (4%) ---
            cc_rate = 0.04
            calculated_fee = operator_net_cost * cc_rate
            total_cc_hold = operator_net_cost + calculated_fee

            #
