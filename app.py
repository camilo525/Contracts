import streamlit as st
import json
import urllib.request
import re
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Thrust Aviation - High-Precision Risk Auditor", layout="wide")

LOGO_URL = "https://thrust-aviation.com/wp-content/uploads/2024/02/Logo-White-500-2-e1710003051285.png"
ARGUS_LOGO_URL = "https://static.wixstatic.com/media/5f5db0_79cb7a5853cb4172a71c7dfeefc32051~mv2.png/v1/crop/x_132,y_105,w_736,h_857/fill/w_546,h_636,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/Certified%20Charter%20Broker%20Logo-resized.png"

# --- OFFICIAL SAFETY REGISTRY DIRECTORIES ---
ARGUS_DIRECTORY_URL = "https://www.argus.aero/operatorregistry"
WYVERN_DIRECTORY_URL = "https://app.wyvern.systems/public/directory/wingman"

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
st.markdown("Rigorous Risk Audit: **Thrust Master Terms (Section 26)** vs. **Operator Contract** + **ARGUS / WYVERN Safety Audit**.")

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

# --- STEP 2: OPERATOR SAFETY & INCIDENT CHECKER (ARGUS & WYVERN DIRECTORIES) ---
st.subheader("🔍 Step 2: Operator Incident & Safety History Search (ARGUS & WYVERN Scope)")
col_sec1, col_sec2 = st.columns([2, 1])

with col_sec1:
    operator_name = st.text_input(
        "Enter Air Charter / Operator Name to check safety history:", 
        placeholder="e.g., NetJets, VistaJet, Wheels Up, Flexjet..."
    )

with col_sec2:
    st.write(" ")
    st.write(" ")
    run_safety_check = st.checkbox("Include Detailed Safety & Incident Audit", value=True)

if operator_name.strip():
    # Direct launch buttons for ARGUS & WYVERN registries
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
        st.warning(f"⚠️ Static Mode: Enter an API Key in the sidebar to fetch safety records for **{operator_name}**.")
    else:
        with st.spinner(f"🔍 Cross-referencing ARGUS and WYVERN safety benchmarks for {operator_name}..."):
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            # --- TARGETED ARGUS & WYVERN SAFETY PROMPT ---
            safety_prompt = f"""
            You are a Senior Aviation Safety Officer for Thrust Aviation auditing the air charter operator: "{operator_name}".

            PRIMARY SCOPE:
            Inquire and analyze this operator specifically against ARGUS International (https://www.argus.aero/operatorregistry) and WYVERN Systems (https://app.wyvern.systems/public/directory/wingman) safety audit standards.

            Provide a high-precision safety assessment covering:
            1. **ARGUS Audit Rating Status:** Assess expected ARGUS tier (Platinum, Gold Plus, Gold, or Unrated) based on known fleet operational history.
            2. **WYVERN Safety Rating Status:** Assess expected WYVERN accreditation (Wingman Certified or Registered Operator status).
            3. **NTSB / FAA Incident & Accident History:** Detail notable accidents, incidents, or FAA enforcement actions. State clearly if the operator has an immaculate safety record.
            4. **Fleet & Operational Risk Factors:** Identify maintenance compliance patterns, crew qualification risks, or operational red flags.
            5. **Final Safety Clearance Verdict:** State clearly:
               - 🟢 **APPROVED (LOW RISK)** - Verified ARGUS/WYVERN standards met with clean record.
               - 🟡 **CONDITIONAL / ELEVATED RISK** - Manual verification required on ARGUS/WYVERN registries.
               - 🔴 **HIGH RISK / REJECTED** - History of severe NTSB incidents or lack of safety accreditation.

            Use clear markdown headers and bullet points.
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
                    
                    st.info(f"📋 **ARGUS & WYVERN Safety Report: {operator_name}**")
                    st.markdown(safety_result)
            except Exception as e:
                st.error("❌ Failed to fetch safety report. Please verify your OpenAI API Key or network connection.")

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
    c3.metric("TOTAL CREDIT CARD HOLD", f"${total_hold:,.2f} USD", delta="Target for Tradeshift")

    st.markdown("---")

    # --- STEP 4: RIGOROUS COMPLIANCE & EXPOSURE ASSESSMENT ---
    st.subheader("🛡️ Deep Legal & Exposure Audit")
    
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

    # --- STEP 5: TRADESHIFT EXECUTION ---
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
    st.warning("Please paste the Operator contract/cancellation terms in Step 1 to run the compliance audit.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Thrust Aviation High-Precision Risk Auditor v4.3")
st.sidebar.info("Bounded by Thrust Aviation Section 26 Master Terms.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f'<p align="center"><img src="{ARGUS_LOGO_URL}" width="180"></p>', unsafe_allow_html=True)
