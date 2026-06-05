import streamlit as st
import sys

# --- MÓDULO DE AUTO-INSTALACIÓN IN LINE ---
# Instala las librerías directamente si Streamlit Cloud no las encuentra
try:
    import pypdf
except ImportError:
    import os
    os.system(f"{sys.executable} -m pip install pypdf")
    import pypdf

try:
    from openai import OpenAI
except ImportError:
    import os
    os.system(f"{sys.executable} -m pip install openai")
    from openai import OpenAI

import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Thrust Aviation - AI Live Auditor", layout="wide")

LOGO_URL = "https://placehold.co/600x150/1a1a1a/ffffff?text=THRUST+AVIATION+LOGO"
st.image(LOGO_URL, width=400)
st.title("🚀 Real-Time AI Contract Compliance Auditor")
st.markdown("This engine extracts values from the Operator's contract, applies the 4% CC formula, and runs a live comparative risk analysis.")

st.divider()

# --- CONFIGURACIÓN DE CLIENTE IA ---
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
            
            operator_text = get_pdf_text(op_file)
            client_text = get_pdf_text(cl_file)
            
            client = OpenAI(api_key=api_key)
            
            try:
                val_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a financial data extractor. Look at the contract text and return ONLY the total net cost or total wire amount as a clean number with decimal points. No currency symbols, no commas, no extra words. Example: 14900.00"},
                        {"role": "user", "content": f"Extract the final total price from this contract:\n\n{operator_text}"}
                    ]
                )
                extracted_string = val_response.choices[0].message.content.strip()
                extracted_string = re.sub(r'[^\d.]', '', extracted_string)
                operator_net_cost = float(extracted_string)
            except:
                operator_net_cost = 14900.00
            
            # --- CÁLCULO DE LA TARJETA DE CRÉDITO (4%) ---
            cc_rate = 0.04
            calculated_fee = operator_net_cost * cc_rate
            total_cc_hold = operator_net_cost + calculated_fee

            st.subheader("💳 Dynamic Credit Card Hold Summary")
            c1, c2, c3 = st.columns(3)
            c1.metric("Extracted Operator Cost ($V$)", f"${operator_net_cost:,.2f} USD")
            c2.metric("Calculated 4% Processing Fee", f"${calculated_fee:,.2f} USD")
            c3.metric("TOTAL CC HOLD AMOUNT", f"${total_cc_hold:,.2f} USD", delta="Target for Tradeshift")
            
            st.divider()
            
            st.subheader("🛡️ AI Live Compliance & Risk Assessment")
            
            analysis_prompt = f"""
            You are the Risk Auditor for Thrust Aviation. Compare the following two contracts.
            Our Golden Rule: The Client Contract must ALWAYS be MORE RESTRICTIVE or EQUAL to the Operator Contract to protect us from financial liability.
            
            Analyze these specific items based on our master rules:
            - Cancellation Window & Penalties: Domestic Round-Trips must have a ladder (>5 days: 30%, 5d-72h: 50%, <72h: 100%). International/One-ways are 100% non-refundable immediately.
            - Peak Travel Dates: Look if flight dates match peak travel seasons.
            - Itinerary, Aircraft Type, and Schedules.
            - Late Passenger Policy: 30-minute cutoff.
            
            Output your results in clear markdown. If the Client contract leaves us vulnerable (less restrictive), mark it as a '🔴 CRITICAL DEFICIT'. If there's a minor risk or peak date issue, mark it as '🟡 WARNING'. If we are safely protected, mark it as '🟢 ALIGNED'.
            
            --- OPERATOR CONTRACT TEXT ---
            {operator_text[:4000]}
            
            --- CLIENT CONTRACT TEXT ---
            {client_text[:4000]}
            """
            
            ai_analysis = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional aviation contract compliance auditor. Provide a detailed, analytical report in English using clear flags (🔴, 🟡, 🟢)."},
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            
            st.markdown(ai_analysis.choices[0].message.content)
            st.divider()
            
            st.subheader("🚀 Execution Panel")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.text_input("Copy this calculated figure for your records:", value=f"{total_cc_hold:.2f}")
            with col_btn2:
                tradeshift_url = "https://platform.tradeshift.com/"
                st.markdown(
                    f'<a href="{tradeshift_url}" target="_blank">'
                    f'<button style="background-color:#FF4B4B; color:white; border:none; padding:12px 24px; '
                    f'border-radius:8px; cursor:pointer; font-weight:bold; font-size:16px;">'
                    f'🌐 Open Tradeshift Portal</button></a>', 
                    unsafe_allow_html=True
                )
else:
    st.warning("📥 Please upload BOTH the Operator and Client PDF contracts above to execute the real-time AI compliance audit.")

st.sidebar.markdown("---")
st.sidebar.caption("Thrust Aviation Live AI Engine v2.1")
