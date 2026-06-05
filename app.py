import streamlit as st
import json
import urllib.request
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - OpenAI Auditor", layout="wide")

LOGO_URL = "https://thrust-aviation.com/wp-content/uploads/2024/02/Logo-White-500-2-e1710003051285.png"
ARGUS_LOGO_URL = "https://static.wixstatic.com/media/5f5db0_d7471efb590b4734a38048043fb3b2c1~mv2.png/v1/fill/w_480,h_480,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/FBO%20Audit%20Logo%20Silver.png"

# --- ENCABEZADO ---
st.image(LOGO_URL, width=200)
st.title("Contract Compliance & OpenAI Financial Auditor")
st.markdown("Real-time variable risk assessment")

st.divider()

# --- ACTIVADOR DE OPENAI (SIDEBAR) ---
st.sidebar.markdown("## 🤖 OpenAI Activation")
api_key = st.sidebar.text_input("Enter OpenAI API Key (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):", type="password")
if not api_key:
    st.sidebar.warning("⚠️ Running in Simulation Mode. Enter your OpenAI API Key to enable the Live Auditor.")
else:
    st.sidebar.success("⚡ OpenAI GPT Engine Active!")

# --- SECCIÓN DE CARGA DE ARCHIVOS ---
col_up1, col_up2 = st.columns(2)

with col_up1:
    st.info("📂 **Operator Side**")
    op_file = st.file_uploader("Upload Operator Contract (PDF)", type=["pdf"], key="op")

with col_up2:
    st.info("📂 **Client Side**")
    cl_file = st.file_uploader("Upload Client Contract (PDF)", type=["pdf"], key="cl")

st.divider()

# --- LECTOR NATIVO DE TEXTO ---
def extract_clean_text(uploaded_file):
    if uploaded_file is None:
        return ""
    try:
        binary_data = uploaded_file.read()
        text = binary_data.decode('utf-8', errors='ignore')
        clean_text = "".join([c for c in text if c.isalnum() or c in " \n.,:$-\n"])
        return clean_text[:4000] # Límite seguro de texto para enviar por HTTP
    except:
        return ""

# --- LÓGICA PRINCIPAL ---
if op_file and cl_file:
    st.success("✅ Files received.")
    
    # --- INPUT MANUAL (4%) ---
    st.subheader("📥 Financial Input")
    operator_cost_input = st.text_input("Enter the exact Total Price / Wire Total from the Operator Contract ($USD):", value="14900.00")
    
    clean_string = re.sub(r'[^\d.]', '', operator_cost_input)
    try:
        base_value = float(clean_string) if clean_string else 0.0
    except ValueError:
        base_value = 0.0

    cc_rate = 0.04
    security_fee = base_value * cc_rate
    total_hold = base_value + security_fee

    # Despliegue de métricas financieras
    st.subheader("💳 Financial Hold Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Operator Base Value", f"${base_value:,.2f} USD")
    c2.metric("Thrust CC Fee (4%)", f"${security_fee:,.2f} USD")
    c3.metric("TOTAL CREDIT CARD HOLD", f"${total_hold:,.2f} USD", delta="Target for Tradeshift")

    st.markdown("---")

    # --- NÚCLEO DE AUDITORÍA: ¿SIMULADO O OPENAI REAL? ---
    st.subheader("🛡️ Compliance Risk Assessment")
    
    if not api_key:
        # MODO SIMULADO
        st.caption("ℹ️ *Displaying baseline simulation rules. Insert your OpenAI key to cross-reference with GPT.*")
        st.error("**🔴 CRITICAL: Cancellation Window Exposure (Simulated)**\n\n- Operator requires 100% penalty within 4 days, but your Master Terms enforce it within 72h. You are unprotected for 24 hours.")
        st.warning("**🟡 WARNING: Peak Travel Dates Detected (Simulated)**\n\n- Flight coincides with Thrust Peak Dates (Section 26). Ensure client contract is 100% Non-Refundable.")
        st.success("**🟢 ALIGNED: Late Passenger Policy (Simulated)**\n\n- Both contracts enforce the standard 30-minute 'No Show' rule.")
    else:
        # MODO OPENAI REAL ACTIVO
        with st.spinner("🤖 OpenAI GPT is auditing and cross-referencing both contracts..."):
            op_text = extract_clean_text(op_file)
            cl_text = extract_clean_text(cl_file)
            
            # Ajustado para la API oficial de OpenAI por HTTP directo
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            prompt = f"You are the Risk Auditor for Thrust Aviation. Compare these two contracts. Our rule: The Client Contract must be MORE RESTRICTIVE or EQUAL to the Operator Contract to protect us. Look at cancellation windows, peak dates, and passenger lateness. Output the audit in markdown using clear 🔴 CRITICAL, 🟡 WARNING, or 🟢 ALIGNED bullet points based ONLY on this text:\n\nOPERATOR:\n{op_text}\n\nCLIENT:\n{cl_text}"
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
            
            try:
                req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    openai_analysis = res_data['choices'][0]['message']['content']
                    # Imprime el análisis real directo de OpenAI en la pantalla
                    st.markdown(openai_analysis)
            except Exception as e:
                st.error("❌ OpenAI Connection Error. Please verify your API Key or account balance.")

    st.divider()

    # --- EJECUCIÓN Y TRADESHIFT ---
    st.subheader("🚀 Next Steps")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        st.write("Confirm amount to process in Tradeshift:")
        st.text_input("Hold Figure to Copy:", value=f"{total_hold:.2f}", key="hold_val")
        st.caption("Copy this exact amount into your transaction window.")

    with col_btn2:
        st.write("Launch Portal:")
        tradeshift_url = "https://platform.tradeshift.com/"
        button_html = f'<a href="{tradeshift_url}" target="_blank"><button style="background-color:#FF4B4B; color:white; border:none; padding:12px 24px; border-radius:8px; cursor:pointer; font-weight:bold; font-size:16px;">🌐 Open Tradeshift Portal</button></a>'
        st.markdown(button_html, unsafe_allow_html=True)

else:
    st.warning("Please upload both PDF contracts to start the compliance audit.")

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.caption("Thrust Aviation Internal Tool v2.2-OpenAI")
st.sidebar.info("Financial formulas strictly calculate the 4% Domestic CC Hold fee.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f'<p align="center"><img src="{ARGUS_LOGO_URL}" width="180"></p>', unsafe_allow_html=True)
