import streamlit as st
import json
import urllib.request
import re
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Thrust Aviation - High-Precision Risk Auditor", layout="wide")

LOGO_URL = "https://thrust-aviation.com/wp-content/uploads/2024/02/Logo-White-500-2-e1710003051285.png"
ARGUS_LOGO_URL = "https://static.wixstatic.com/media/5f5db0_79cb7a5853cb4172a71c7dfeefc32051~mv2.png/v1/crop/x_132,y_105,w_736,h_857/fill/w_546,h_636,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Certified%20Charter%20Broker%20Logo-resized.png"

# --- OFFICIAL EXTERNAL PORTALS ---
ARGUS_DIRECTORY_URL = "https://www.argus.aero/operatorregistry"
WYVERN_DIRECTORY_URL = "https://app.wyvern.systems/public/directory/wingman"
EFD_HOLDS_URL = "https://efd.thrust-aviation.com/#holds"
TRADESHIFT_URL = "https://platform.tradeshift.com/"

# --- COMPREHENSIVE THRUST AVIATION MASTER TERMS (SECTION 26) ---
THRUST_MASTER_POLICY = """
THRUST AVIATION MASTER TERMS & CONDITIONS (SECTION 26 & COMPLIANCE RULES):

1. ONE-WAY BOOKINGS:
   - 100% non-refundable / 100% cancellation fee immediately upon booking execution (signature).

2. INTERNATIONAL BOOKINGS:
   - 100% non-refundable once confirmed with operator.
   - Applies to any flight beginning, ending, or occurring entirely outside the United States.

3. DOMESTIC ROUND-TRIP BOOKINGS:
   - Confirmation to > 5 Days before departure: 30% penalty of total price.
   - Within 5 Days to 72 Hours before scheduled departure: 50% penalty of total price.
   - Within 72 Hours of scheduled departure: 100% penalty of total price.
   - En Route / Aircraft Repositioned: Up to 100% penalty if aircraft has moved.

4. PEAK TRAVEL DATES (100% NON-REFUNDABLE REGARDLESS OF LEAD TIME):
   - Jan 15 - Jan 16 | Feb 15 - Feb 20 | Mar 28 - Apr 2 | Apr 8 - Apr 9
   - May 24 - May 28 | Jun 29 - Jun 30 | Jul 3 - Jul 8 | Aug 30 - Sep 3
   - Oct 4 - Oct 10 | Nov 10 - Nov 15 | Nov 17 - Nov 26 | Dec 7 - Dec 9
   - Dec 21 - Jan 7

5. CREDIT CARD AUTHORIZATION & NO-DISPUTE MANDATE:
   - Client authorizes holds/charges for cancellations under this policy.
   - Client explicitly waives the right to dispute or chargeback any hold/fee through their CC issuer.
"""

# --- HEADER ---
st.image(LOGO_URL, width=400)
st.title("High-Precision Contract Compliance & Risk Auditor")
st.markdown("Rigorous Risk Audit: **Thrust Master Terms (Section 26)** vs. **Operator Contract** + **Comprehensive Operator & Fleet Analysis**.")

st.divider()

# --- SIDEBAR: DUAL API KEY RESOLUTION ---
st.sidebar.markdown("## 🤖 AI Engine Settings")

secret_key = None
try:
    secret_key = st.secrets.get("OPENAI_API_KEY", None)
except Exception:
    secret_key = None

manual_key = st.sidebar.text_input(
    "OpenAI API Key (sk-...):", 
    type="password", 
    help="Enter key if not configured in Streamlit Secrets"
)

api_key = manual_key.strip() if manual_key.strip() else secret_key

if api_key:
    st.sidebar.success("⚡ Deep AI Risk Engine Active")
else:
    st.sidebar.warning("⚠️ Running in Static Mode. Enter API Key above or set up Streamlit Secrets.")

st.sidebar.markdown("---")
with st.sidebar.expander("📌 View Complete Thrust Master Policy (Sec. 26)"):
    st.caption(THRUST_MASTER_POLICY)

# --- STEP 1: OPERATOR CONTRACT CANCELLATION CLAUSE ---
st.subheader("📄 Step 1: Input Operator Contract / Cancellation Clause")
op_text_manual = st.text_area(
    "Paste the Operator Contract text or terms & conditions below:",
    placeholder="Example: Operator requires 100% payment if canceled within 4 days. Repositioning costs are non-refundable...",
    height=200
)

st.divider()

# --- STEP 2: COMPREHENSIVE OPERATOR & FLEET AUDIT (ARGUS & WYVERN SCOPE) ---
st.subheader("🔍 Step 2: Comprehensive Operator & Fleet Analysis")
col_sec1, col_sec2 = st.columns([2, 1])

with col_sec1:
    operator_name = st.text_input(
        "Enter Air Charter / Operator Name for complete fleet & safety audit:", 
        placeholder="e.g., NetJets, VistaJet, Wheels Up, Flexjet, Clay Lacy..."
    )

with col_sec2:
    st.write(" ")
    st.write(" ")
    run_safety_check = st.checkbox("Include Full Fleet & Operational Scope", value=True)

if operator_name.strip():
    st.markdown("### 🌐 Live Registry Inquiry Portals")
    col_link1, col_link2 = st.columns(2)
    
    with col_link1:
        st.markdown(
            f'<a href="{ARGUS_DIRECTORY_URL}" target="_blank">'
            f'<button style="background-color:#003366; color:white; border:none; padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:bold; width:100%;">'
            f'🛡️ Open ARGUS Operator Registry</button></a>',
            unsafe_allow_html=True
        )
        st.caption("Verify ARGUS Rated / Gold / Platinum status live.")

    with col_link2:
        st.markdown(
            f'<a href="{WYVERN_DIRECTORY_URL}" target="_blank">'
            f'<button style="background-color:#1A5276; color:white; border:none; padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:bold; width:100%;">'
            f'🦅 Open WYVERN Wingman Directory</button></a>',
            unsafe_allow_html=True
        )
        st.caption("Verify WYVERN Wingman / Registered status live.")

    st.markdown("<br>", unsafe_allow_html=True)

    if not api_key:
        st.warning(f"⚠️ Static Mode: Enter an API Key in the sidebar to fetch full operator records for **{operator_name}**.")
    else:
        with st.spinner(f"🔍 Executing 360° Fleet & Safety Audit for {operator_name}..."):
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            safety_prompt = f"""
            You are the Senior Aviation Fleet & Risk Analyst for Thrust Aviation.
            Conduct a 360-degree comprehensive operational, safety, and fleet audit for the air charter operator: "{operator_name}".

            PRIMARY SCOPE OF ANALYSIS:
            Examine this operator across 5 key operational pillars:

            1. **Fleet Profile & Composition:**
               - Primary aircraft categories operated (e.g., Heavy Jets, Super-Mid, Midsize, Light, Turboprops).
               - Known flagship models in their fleet (e.g., Bombardier Global, Gulfstream G-Series, Citation X, Challenger, Phenom 300).
               - Estimated average fleet age profile and operational scale (Floating fleet vs. Base-managed aircraft).

            2. **Safety Accreditation & Audit Status:**
               - **ARGUS Rating Benchmark:** Expected tier (Platinum, Gold Plus, Gold, or Unrated) based on industry records (https://www.argus.aero/operatorregistry).
               - **WYVERN Rating Benchmark:** Expected accreditation (Wingman Certified or Registered) based on industry standards (https://app.wyvern.systems/public/directory/wingman).
               - **IS-BAO Stage:** Operational safety management system maturity.

            3. **Operational History & Regulatory Record:**
               - **NTSB & FAA Incident Analysis:** Summarize notable historical accidents, incidents, or FAA enforcement actions. Explicitly state if the operator maintains an immaculate safety record.
               - Pilot training standards (e.g., FlightSafety, CAE simulator training mandates).

            4. **Fleet Dispatch Reliability & Operational Risks:**
               - Mechanical AOG (Aircraft On Ground) risk indicators based on fleet age/mix.
               - Sourcing reliability and backup aircraft availability if an AOG occurs.

            5. **Final Operational Clearance Verdict:**
               - Provide a clear rating:
                 - 🟢 **APPROVED (LOW RISK)** - Verified top-tier fleet, clean safety record, ARGUS/WYVERN compliant.
                 - 🟡 **CONDITIONAL / ELEVATED RISK** - Older fleet mix or manual registry verification required.
                 - 🔴 **HIGH RISK / REJECTED** - History of severe NTSB incidents or regulatory non-compliance.

            Structure your response using clear markdown headers, bold highlights, and bullet points.
            """
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": safety_prompt}],
                "temperature": 0.1
            }
            
            try:
                req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    safety_result = res_data['choices'][0]['message']['content']
                    
                    st.info(f"📋 **360° Operator & Fleet Audit Report: {operator_name}**")
                    st.markdown(safety_result)
            except Exception as e:
                st.error("❌ Failed to fetch operator report. Please verify your OpenAI API Key or network connection.")

st.divider()

# --- MAIN AUDIT & CALCULATION LOGIC ---
if op_text_manual.strip():
    st.success("✅ Operator Terms Received.")
    
    # --- STEP 3: FINANCIAL INPUT (4% HOLD) ---
    st.subheader("📥 Step 3: Financial Input (Credit Card Hold)")
    operator_cost_input = st.text_input("Enter Total Price / Wire Total from Operator Contract ($USD):", value="")
    
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
    c3.metric("TOTAL CREDIT CARD HOLD", f"${total_hold:,.2f} USD", delta="Target for Hold Portal")

    st.markdown("---")

    # --- STEP 4: RIGOROUS COMPLIANCE & EXPOSURE ASSESSMENT ---
    st.subheader("🛡️ Step 4: Deep Legal & Exposure Audit")
    
    operator_content = op_text_manual.strip()

    if not api_key:
        st.caption("ℹ️ *Displaying baseline simulation rules. Insert API Key in sidebar or Secrets to trigger live AI analysis.*")
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
        with st.spinner("🤖 Performing rigorous comparative analysis..."):
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            deep_audit_prompt = f"""
            You are the Lead Risk & Compliance Counsel for Thrust Aviation.
            Conduct a mathematical and legal comparison between OPERATOR TERMS and THRUST AVIATION MASTER TERMS (SECTION 26).

            EXPOSURE DEFINITION (CRITICAL - READ CAREFULLY):
            Financial Exposure happens ONLY when: OPERATOR PENALTY > THRUST CLIENT PENALTY.
            Meaning: Thrust has to pay the Operator MORE money than Thrust is allowed to collect/retain from the Client.

            RULE OF THUMB FOR PROTECTION:
            1. If Thrust's penalty is HIGHER than or EQUAL to the Operator's penalty -> THRUST IS FULLY PROTECTED 🟢.
            2. If the Operator charges $0 penalty / No penalty, and Thrust charges 30% penalty -> THRUST IS FULLY PROTECTED 🟢 (Thrust retains 30% as profit with 0 operator liability).
            3. If the Operator charges 100% penalty, but Thrust only charges 50% penalty -> THRUST IS EXPOSED 🔴 (Thrust is short 50% out-of-pocket).

            {THRUST_MASTER_POLICY}

            OPERATOR TERMS TO AUDIT:
            {operator_content}

            INSTRUCTIONS FOR YOUR AUDIT REPORT:
            1. **Overall Verdict:** State clearly in bold: **FULLY PROTECTED** or **EXPOSED TO FINANCIAL RISK**.
            2. **Comparative Breakdown:**
               - **A. Cancellation Timeline & Penalty Comparison:** Compare each timeframe. Explicitly state both penalties (e.g., "Outside 7 days: Operator 0% vs Thrust 30% -> PROTECTED").
               - **B. Peak Travel Dates:** Note if the flight coincides with Thrust Peak Dates (which enforce 100% non-refundable status).
               - **C. One-Way / International Rules:** Verify if One-Way or International rules apply (100% non-refundable).
               - **D. Repositioning & Credit Card Defensibility:** Check positioning costs and chargeback protection.
            3. **Flag System:**
               - Use 🔴 **CRITICAL GAP** ONLY if Operator Penalty > Thrust Client Penalty.
               - Use 🟡 **WARNING / CONDITIONAL RISK** for items needing manual operational check (e.g., peak date verification).
               - Use 🟢 **ALIGNED / PROTECTED** whenever Thrust Penalty >= Operator Penalty (including when Operator has 0 penalty).
            4. **Actionable Summary:** Clear summary for the broker.
            """
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": deep_audit_prompt}],
                "temperature": 0.0
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

    # --- STEP 5: NEXT STEPS & PORTAL EXECUTION ---
    st.subheader("🚀 Step 5: Next Steps & Credit Card Hold Processing")
    
    col_exec1, col_exec2 = st.columns(2)

    with col_exec1:
          

    with col_exec2:
        st.markdown("### 🌐 Action Portals")
        
        # Primary Credit Card Hold Action Link
        efd_button_html = f'''
        <a href="{EFD_HOLDS_URL}" target="_blank">
            <button style="background-color:#28a745; color:white; border:none; padding:12px 24px; border-radius:8px; cursor:pointer; font-weight:bold; font-size:16px; width:100%; margin-bottom:12px;">
                💳 Create Credit Card Hold (EFD Portal)
            </button>
        </a>
        '''
        st.markdown(efd_button_html, unsafe_allow_html=True)
        st.caption("Directly process the credit card security hold on `efd.thrust-aviation.com/#holds`.")

        # Secondary Tradeshift Link
        tradeshift_button_html = f'''
        <a href="{TRADESHIFT_URL}" target="_blank">
            <button style="background-color:#4A5568; color:white; border:none; padding:8px 16px; border-radius:6px; cursor:pointer; font-weight:bold; font-size:14px; width:100%;">
                🌐 Open Tradeshift Portal
            </button>
        </a>
        '''
        st.markdown(tradeshift_button_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📌 Quick Reference Link: EFD Credit Card Hold Portal", expanded=True):
        st.markdown(f"🔗 **Direct Link to Create Hold:** [{EFD_HOLDS_URL}]({EFD_HOLDS_URL})")

else:
    st.warning("Please paste the Operator contract/cancellation terms in Step 1 to run the compliance audit.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Thrust Aviation High-Precision Risk Auditor v4.6")
st.sidebar.info("Bounded by Thrust Aviation Section 26 Master Terms.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f'<p align="center"><img src="{ARGUS_LOGO_URL}" width="180"></p>', unsafe_allow_html=True)
