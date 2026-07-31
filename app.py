import streamlit as st
import json
import urllib.request
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Thrust Aviation - Compliance & Risk Auditor", layout="wide")

LOGO_URL = "https://placehold.co/600x150/1a1a1a/ffffff?text=THRUST+AVIATION+LOGO"
ARGUS_LOGO_URL = "https://placehold.co/200x80/1a1a1a/ffffff?text=ARGUS+AUDITED"

# --- FIXED THRUST AVIATION MASTER TERMS (SECTION 26) ---
THRUST_MASTER_POLICY = """
THRUST AVIATION MASTER CANCELLATION POLICY (SECTION 26):
1. One-Way Bookings: 100% cancellation fee upon booking confirmation.
2. International Bookings: 100% non-refundable once confirmed (any flight outside or originating outside US).
3. Domestic Round-Trip Bookings:
   - > 5 Days before departure: 30% penalty.
   - 5 Days to 72 Hours before departure: 50% penalty.
   - Within 72 Hours of departure: 100% penalty.
   - If aircraft repositioned/en route: Up to 100% penalty.
4. Peak Travel Dates (100% Non-Refundable regardless of lead time):
   - Jan 15 - Jan 16 | Feb 15 - Feb 20 | Mar 28 - Apr 2 | Apr 8 - Apr 9
   - May 24 - May 28 | Jun 29 - Jun 30 | Jul 3 - Jul 8 | Aug 30 - Sep 3
   - Oct 4 - Oct 10 | Nov 10 - Nov 15 | Nov 17 - Nov 26 | Dec 7 - Dec 9
   - Dec 21 - Jan 7
"""

# --- HEADER ---
st.image(LOGO_URL, width=400)
st.title("Contract Compliance & Risk Auditor")
st.markdown("Automated comparison: **Thrust Master Terms (Section 26)** vs. **Operator Contract**.")

st.divider()

# --- RETRIEVE API KEY FROM STREAMLIT SECRETS ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    st.sidebar.success("⚡ Live AI Risk Analysis Active")
except Exception:
    api_key = None
    st.sidebar.warning("⚠️ Running in Static Mode. Configure OPENAI_API_KEY in Streamlit Secrets.")

st.sidebar.markdown("---")
with st.sidebar.expander("📌 View Fixed Thrust Terms (Sec. 26)"):
    st.caption(THRUST_MASTER_POLICY)

# --- STEP 1: OPERATOR TEXT INPUT BOX ---
st.subheader("📄 Step 1: Input Operator Contract / Cancellation Clause")
op_text_manual = st.text_area(
    "Paste the Operator Contract text or cancellation terms below:",
    placeholder="Example: Cancellation of domestic flights 4 days prior to departure incurs a 100% cancellation penalty...",
    height=200
)

st.divider()

# --- MAIN AUDIT & CALCULATION LOGIC ---
if op_text_manual.strip():
    st.success("✅ Operator Terms Received.")
    
    # --- STEP 2: FINANCIAL INPUT (4% HOLD) ---
    st.subheader("📥 Step 2: Financial Input (Credit Card Hold)")
    operator_cost_input = st.text_input("Enter Total Price / Wire Total from Operator Contract ($USD):", value="14900.00")
    
    clean_string = re.sub(r'[^\d.]', '', operator_cost_input)
    try:
        base_value = float(clean_string) if clean_string else 0.0
    except ValueError:
        base_value = 0.0

    cc_rate = 0.04
    security_fee = base_value * cc_rate
    total_hold = base_value + security_fee

    c1, c2, c3 = st.columns(3)
    c1.metric("Operator Base Value", f"${base_value:,.2f} USD")
    c2.metric("Thrust CC Fee (4%)", f"${security_fee:,.2f} USD")
    c3.metric("TOTAL CREDIT CARD HOLD", f"${total_hold:,.2f} USD", delta="Target for Tradeshift")

    st.markdown("---")

    # --- STEP 3: COMPLIANCE & EXPOSURE ASSESSMENT ---
    st.subheader("🛡️ Compliance & Risk Assessment")
    
    operator_content = op_text_manual.strip()

    if not api_key:
        st.caption("ℹ️ *Displaying baseline simulation rules. Configure OPENAI_API_KEY in Streamlit Secrets to activate live AI analysis.*")
        st.error("""
        **🔴 CRITICAL EXPOSURE: Cancellation Window Gap (Static Baseline)**
        - **Operator Policy:** 100% penalty within 4 days (96h).
        - **Thrust Terms (Sec. 26):** 50% penalty between 5 days and 72h.
        - **Exposure:** If the client cancels 80 hours before flight, Thrust collects 50% from the client but owes 100% to the operator. **Thrust is exposed to financial loss.**
        """)
        st.warning("""
        **🟡 WARNING: Peak Travel Date Verification Required**
        - Verify if the flight date matches any Thrust Peak Dates (Sec. 26). Peak dates enforce 100% non-refundable status.
        """)
    else:
        with st.spinner("🤖 AI is cross-referencing Operator terms against Thrust Section 26..."):
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            prompt = f"""
            You are the Risk Auditor for Thrust Aviation. 
            Compare the OPERATOR CANCELLATION TERMS against THRUST AVIATION MASTER TERMS (SECTION 26).
            
            RULE: Thrust must ALWAYS be fully protected. If the Operator imposes a higher penalty than what Thrust charges its Client at any point, THRUST IS EXPOSED TO FINANCIAL LOSS.

            {THRUST_MASTER_POLICY}

            OPERATOR TERMS TO AUDIT:
            {operator_content}

            Format your response in markdown:
            1. State clearly if Thrust is PROTECTED or EXPOSED.
            2. Use 🔴 CRITICAL for gaps where the Operator charges more than Thrust collects from the client.
            3. Use 🟡 WARNING for Peak Date or International flight risks.
            4. Use 🟢 ALIGNED for terms where Thrust is fully protected.
            """
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            
            try:
                req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    audit_result = res_data['choices'][0]['message']['content']
                    st.markdown(audit_result)
            except Exception as e:
                st.error("❌ Connection Error. Please verify your OpenAI API Key or account balance.")

    st.divider()

    # --- STEP 4: TRADESHIFT EXECUTION ---
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
    st.warning("Please paste the Operator cancellation terms in the box above to run the compliance audit.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Thrust Aviation Internal Risk Tool v3.3")
st.sidebar.info("Bounded by Thrust Aviation Section 26 Master Terms.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f'<p align="center"><img src="{ARGUS_LOGO_URL}" width="180"></p>', unsafe_allow_html=True)
