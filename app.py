import io
import datetime
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

# PDF Generation Imports (ReportLab)
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Safe Import for Visualizations (Plotly with Matplotlib Fallback)
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    import matplotlib.pyplot as plt
    HAS_PLOTLY = False

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
LOGO_URL = "https://zain-tech-automation-solutions-insight-buddy.lovable.app/__l5e/assets-v1/300bc5af-71cd-47cb-b63c-d0432713caee/zaintech-logo.png"

st.set_page_config(
    page_title="Zain Tech Automation Solutions | ChurnPulse",
    page_icon=LOGO_URL,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ADVANCED CSS & FORCED BLUE STYLING
# -----------------------------------------------------------------------------
st.markdown(f"""
<style>
    /* Main Canvas Setup */
    .stApp {{
        background-color: #030712 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%) !important;
        overflow-x: hidden;
    }}

    /* ENTERPRISE LOGIN BACKGROUND ANIMATION */
    .login-bg-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }}

    .glow-orb {{
        position: absolute;
        border-radius: 50%;
        filter: blur(90px);
        opacity: 0.45;
        animation: floatOrb 20s infinite ease-in-out alternate;
    }}

    .glow-orb-1 {{
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, #2563eb 0%, rgba(37, 99, 235, 0) 70%);
        top: -100px;
        left: -100px;
        animation-duration: 18s;
    }}

    .glow-orb-2 {{
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, #7c3aed 0%, rgba(124, 58, 237, 0) 70%);
        bottom: -150px;
        right: -100px;
        animation-duration: 22s;
        animation-delay: -5s;
    }}

    .glow-orb-3 {{
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, #06b6d4 0%, rgba(6, 182, 212, 0) 70%);
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation-duration: 15s;
        animation-delay: -10s;
    }}

    @keyframes floatOrb {{
        0% {{ transform: translate(0px, 0px) scale(1) rotate(0deg); }}
        33% {{ transform: translate(60px, -80px) scale(1.1) rotate(120deg); }}
        66% {{ transform: translate(-40px, 50px) scale(0.95) rotate(240deg); }}
        100% {{ transform: translate(0px, 0px) scale(1) rotate(360deg); }}
    }}

    .rotating-tech-ring {{
        width: 110px;
        height: 110px;
        margin: 0 auto -95px auto;
        border: 2px dashed rgba(59, 130, 246, 0.4);
        border-top: 2px solid #3b82f6;
        border-right: 2px solid #8b5cf6;
        border-radius: 50%;
        animation: spinRing 12s linear infinite;
    }}

    @keyframes spinRing {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    div[data-testid="stForm"] {{
        background: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 20px !important;
        padding: 35px 30px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(37, 99, 235, 0.15) !important;
        backdrop-filter: blur(16px) !important;
        position: relative;
        z-index: 10;
    }}

    .stTextInput input {{
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
    }}

    div.stButton > button,
    div.stButton > button:first-child,
    .stButton button,
    div.stDownloadButton > button,
    div.stDownloadButton > button:first-child,
    .stDownloadButton button,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
        transition: all 0.25s ease-in-out !important;
        width: 100% !important;
    }}

    div.stButton > button:hover,
    .stButton button:hover,
    div.stDownloadButton > button:hover,
    .stDownloadButton button:hover {{
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        border-color: #60a5fa !important;
        color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6) !important;
        transform: translateY(-2px) !important;
    }}

    section[data-testid="stFileUploader"] {{
        background: rgba(15, 23, 42, 0.7) !important;
        border: 2px dashed #2563eb !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }}

    section[data-testid="stFileUploader"]:hover {{
        border-color: #60a5fa !important;
        background: rgba(30, 41, 59, 0.8) !important;
    }}

    section[data-testid="stFileUploader"] button {{
        width: auto !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 6px !important;
        padding: 6px 16px !important;
    }}

    section[data-testid="stFileUploader"] span, 
    section[data-testid="stFileUploader"] small,
    section[data-testid="stFileUploader"] label {{
        color: #cbd5e1 !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}

    div[data-testid="stMetric"] {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }}

    div[data-testid="stMetricLabel"] p {{
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #9ca3af !important;
        text-transform: uppercase;
    }}

    div[data-testid="stMetricValue"] div {{
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        color: #ffffff !important;
    }}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def load_config():
    with open('config.yaml') as file:
        return yaml.load(file, Loader=SafeLoader)

def save_config(config_data):
    with open('config.yaml', 'w') as file:
        yaml.dump(config_data, file, default_flow_style=False)

def about_df(df): 
    df_sample = df.sample(min(10, len(df))) if len(df) > 0 else df
    size = df.shape 
    buffer = io.StringIO() 
    df.info(buf=buffer) 
    info = buffer.getvalue() 
    columns = df.dtypes 
    missing_values = df.isnull().sum() 
    stats_dataset = df.describe(include='all') 
    return df_sample, size, info, columns, missing_values, stats_dataset 

def customer_statistics(df): 
    if len(df) == 0:
        return {}
    average_age = df.iloc[:, 1].mean() 
    average_tenure = df.iloc[:, 3].mean() 
    total_spend = df.iloc[:, 9].sum() 
    average_support_calls = df.iloc[:, 5].mean() 
    churn_rate = df.iloc[:, 11].mean() * 100 
    payment_delay_std_dev = df.iloc[:, 6].std() 
    
    return { 
        'Average Age': average_age, 
        'Average Tenure': average_tenure, 
        'Total Spend': total_spend, 
        'Average Support Calls': average_support_calls, 
        'Churn Rate (%)': churn_rate, 
        'Payment Delay Std Dev': payment_delay_std_dev 
    } 

def future_insights(df): 
    if len(df) == 0:
        return {}
    average_monthly_spend = df.iloc[:, 9].mean() 
    projected_total_spend_year = average_monthly_spend * 12 * len(df) 
    churn_rate = df.iloc[:, 11].mean() 
    projected_churn_next_year = churn_rate * len(df) 
    average_support_calls = df.iloc[:, 5].mean() 
    projected_support_calls_increase = average_support_calls * 1.1 
    average_payment_delay = df.iloc[:, 6].mean() 
    projected_payment_delay_increase = average_payment_delay * 1.05 
    standard_and_basicd_users = df[(df.iloc[:, 7] == 'Standard') | (df.iloc[:, 7] == 'Basic')] 
    projected_upgrades = len(standard_and_basicd_users) * 0.15 
    average_tenure = df.iloc[:, 3].mean() 
    project_tenure_growth_year = average_tenure * 1.2 
    
    return { 
        'Project Total Spend Next year': projected_total_spend_year, 
        'Project Churn Next year': projected_churn_next_year, 
        'Project Support Calls Increase': projected_support_calls_increase, 
        'Project Payment Delay Increase': projected_payment_delay_increase, 
        'Project Subscription Upgrade': projected_upgrades, 
        'Project Tenure Growth': project_tenure_growth_year 
    } 

# -----------------------------------------------------------------------------
# CACHED EXPORT GENERATION FUNCTIONS
# -----------------------------------------------------------------------------
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def convert_df_to_excel_cached(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Filtered_Customers')
    return output.getvalue()

@st.cache_data
def generate_pdf_report(filtered_df, filter_info, stats):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#2563eb"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=8
    )

    story.append(Paragraph("Zain Tech Automation Solutions", title_style))
    story.append(Paragraph("Enterprise ChurnPulse Intelligence Report", ParagraphStyle('Sub', parent=title_style, fontSize=14, textColor=colors.HexColor("#1e293b"))))
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"<b>Generated Date/Time:</b> {current_time} | <b>Platform Version:</b> ChurnPulse v2.4", subtitle_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Active Dynamic Filters Snapshot", heading_style))
    filter_data = [["Filter Dimension", "Applied Criteria"]]
    for k, v in filter_info.items():
        filter_data.append([str(k), str(v)])
    
    t_filter = Table(filter_data, colWidths=[200, 340])
    t_filter.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2563eb")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_filter)
    story.append(Spacer(1, 15))

    story.append(Paragraph("2. Executive Retention Metrics & KPIs", heading_style))
    kpi_data = [
        ["Metric Name", "Evaluated Value"],
        ["Total Evaluated Accounts", f"{len(filtered_df):,}"],
        ["Mean Tenure", f"{stats.get('Average Tenure', 0):.1f} Months"],
        ["Total Gross Revenue", f"${stats.get('Total Spend', 0):,.2f}"],
        ["Avg Support Calls", f"{stats.get('Average Support Calls', 0):.2f}"],
        ["Aggregate Churn Loss Rate", f"{stats.get('Churn Rate (%)', 0):.1f}%"]
    ]
    t_kpi = Table(kpi_data, colWidths=[270, 270])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#ffffff")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 15))

    story.append(Paragraph("3. Executive Insights & High-Risk Observations", heading_style))
    insights = [
        "• High Support Ticket Friction: Accounts triggering >4 support tickets show elevated churn risk.",
        "• Payment Delay Impact: Payment delays beyond 15 days in early tenure correlate strongly with loss rates.",
        "• Subscription Plan Variance: Monthly contract models demonstrate higher churn compared to annual commitments."
    ]
    for ins in insights:
        story.append(Paragraph(ins, ParagraphStyle('Ins', parent=styles['Normal'], fontSize=9, spaceAfter=4)))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# -----------------------------------------------------------------------------
# RENDER VISUALIZATIONS
# -----------------------------------------------------------------------------
def render_charts(df):
    if HAS_PLOTLY:
        color_seq = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df, x='Age', nbins=10, title="Customer Age Distribution", color_discrete_sequence=['#3b82f6'], template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            avg_spend = df.groupby('Subscription Type')['Total Spend'].mean().reset_index()
            fig = px.bar(avg_spend, x='Subscription Type', y='Total Spend', title='Avg Revenue by Subscription Plan', color='Subscription Type', color_discrete_sequence=color_seq, template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            fig = px.pie(df, names='Gender', title='Demographic Gender Split', color_discrete_sequence=['#3b82f6', '#ec4899'], template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col4:
            contract_spend = df.groupby('Contract Length')['Total Spend'].sum().reset_index()
            fig = px.pie(contract_spend, names='Contract Length', values='Total Spend', title='Total Revenue Contribution by Contract Term', color_discrete_sequence=color_seq, template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        col5, col6 = st.columns(2)
        with col5:
            churn_df = (df.groupby('Gender')['Churn'].mean() * 100).reset_index()
            fig = px.bar(churn_df, x='Gender', y='Churn', title='Churn Concentration Rate (%)', color='Gender', color_discrete_sequence=['#ef4444', '#f59e0b'], template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with col6:
            fig = px.histogram(df, x='Age', color='Gender', barmode='overlay', title='Demographic Overlay (Age vs Gender)', color_discrete_sequence=['#3b82f6', '#ec4899'], template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    else:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(facecolor='#030712')
            ax.set_facecolor('#0b0f19')
            df['Age'].plot(kind='hist', bins=10, ax=ax, color='#3b82f6')
            ax.set_title("Distribution of Age", color='white')
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots(facecolor='#030712')
            ax.set_facecolor('#0b0f19')
            df.groupby('Subscription Type')['Total Spend'].mean().plot(kind='bar', ax=ax, color='#10b981')
            ax.set_title('Avg Total Spend by Subscription Type', color='white')
            st.pyplot(fig)


# -----------------------------------------------------------------------------
# REAL CHURN ANALYSIS
# -----------------------------------------------------------------------------
def render_churn_analysis(df):
    st.subheader("📌 Retention Overview")
    
    churn_counts = df['Churn'].value_counts()
    retained_count = churn_counts.get(0, 0)
    churned_count = churn_counts.get(1, 0)
    total_cust = len(df)
    overall_churn_rate = (churned_count / total_cust * 100) if total_cust > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Evaluated Volume", f"{total_cust:,}")
    c2.metric("Retained Active", f"{retained_count:,}")
    c3.metric("Churn Risk Accounts", f"{churned_count:,}")
    c4.metric("Aggregate Churn Rate", f"{overall_churn_rate:.1f}%")

    st.divider()
    st.subheader("🔎 Multi-Dimensional Risk Segmentation")

    col_a, col_b = st.columns(2)

    with col_a:
        if 'Subscription Type' in df.columns and HAS_PLOTLY:
            sub_churn = df.groupby('Subscription Type')['Churn'].agg(['count', 'mean']).reset_index()
            sub_churn['mean'] = sub_churn['mean'] * 100
            fig = px.bar(sub_churn, x='Subscription Type', y='mean', title="Churn Loss by Subscription Plan (%)", color='mean', color_continuous_scale='Reds', template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        if 'Support Calls' in df.columns and HAS_PLOTLY:
            supp_churn = df.groupby('Support Calls')['Churn'].mean().reset_index()
            supp_churn['Churn'] = supp_churn['Churn'] * 100
            fig = px.line(supp_churn, x='Support Calls', y='Churn', title="Churn Likelihood vs Support Call Velocity (%)", markers=True, template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        if 'Payment Delay' in df.columns and HAS_PLOTLY:
            delay_churn = df.groupby('Payment Delay')['Churn'].mean().reset_index()
            delay_churn['Churn'] = delay_churn['Churn'] * 100
            fig = px.bar(delay_churn, x='Payment Delay', y='Churn', title="Payment Delay Impact on Churn Rate (%)", color='Churn', color_continuous_scale='Oranges', template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        if 'Contract Length' in df.columns and HAS_PLOTLY:
            contract_churn = df.groupby('Contract Length')['Churn'].mean().reset_index()
            contract_churn['Churn'] = contract_churn['Churn'] * 100
            fig = px.bar(contract_churn, x='Contract Length', y='Churn', title="Risk Exposure by Contract Commitment (%)", color='Contract Length', template="plotly_dark")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------------------------
# MAIN APP EXECUTION
# -----------------------------------------------------------------------------
config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authentication_status = st.session_state.get("authentication_status")

if not authentication_status:
    st.markdown("""
        <div class="login-bg-container">
            <div class="glow-orb glow-orb-1"></div>
            <div class="glow-orb glow-orb-2"></div>
            <div class="glow-orb glow-orb-3"></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px; margin-top: 15px; position: relative; z-index: 10;">
            <div class="rotating-tech-ring"></div>
            <img src="{LOGO_URL}" style="height: 70px; margin-bottom: 15px; position: relative; z-index: 2;" />
            <h1 style="color: #ffffff; font-weight: 800; font-size: 2.2rem; margin: 0; letter-spacing: -0.5px;">Zain Tech Automation Solutions</h1>
            <p style="color: #3b82f6; font-size: 0.95rem; font-weight: 600; margin-top: 5px;">Enterprise ChurnPulse Intelligence Engine</p>
        </div>
    """, unsafe_allow_html=True)

    col_auth1, col_auth2, col_auth3 = st.columns([1, 1.8, 1])
    with col_auth2:
        auth_tab1, auth_tab2 = st.tabs(["🔒 Secure Login", "📝 Sign Up / Register"])
        
        with auth_tab1:
            authenticator.login()
            if st.session_state.get("authentication_status") == False:
                st.error('❌ Username/password is incorrect')

        with auth_tab2:
            try:
                res = authenticator.register_user()
                if res and isinstance(res, tuple) and res[0]:
                    email_of_registered_user, username_of_registered_user, name_of_registered_user = res
                    config['credentials']['usernames'][username_of_registered_user]['role'] = 'Analyst'
                    save_config(config)
                    st.success('✅ Account created successfully! Please switch to the Login tab.')
            except Exception as e:
                st.error(f"Error registering user: {e}")

else:
    username = st.session_state.get("username")
    name = st.session_state.get("name")
    user_role = config['credentials']['usernames'].get(username, {}).get('role', 'Analyst')

    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <img src="{LOGO_URL}" style="height: 38px; margin-right: 12px;" />
            <div>
                <span style="font-size: 1.05rem; font-weight: 800; color: #ffffff;">Zain Tech</span><br/>
                <span style="font-size: 0.75rem; color: #3b82f6; font-weight: 600;">Automation Solutions</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.caption(f"👤 User: **{name}** | Role: **{user_role}**")
    authenticator.logout('Sign Out', 'sidebar')
    st.sidebar.markdown("---")

    nav_options = [
        "Executive Dashboard", 
        "Churn Driver Analysis", 
        "Dataset Metadata", 
        "Customer Statistics", 
        "Predictive Forecasts",
        "📥 Export & Reporting"
    ]
    if user_role == "Admin":
        nav_options.append("👥 User Access Control (Admin)")

    uploaded_file = st.sidebar.file_uploader("Data Source Pipeline", type='csv')

    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        
        st.sidebar.markdown("---")
        menu_selection = st.sidebar.radio("Navigation Views", nav_options)

        st.sidebar.markdown("---")
        st.sidebar.subheader("🎛️ Dynamic Filters")

        min_age, max_age = int(raw_df['Age'].min()), int(raw_df['Age'].max())
        min_tenure, max_tenure = int(raw_df['Tenure'].min()), int(raw_df['Tenure'].max())
        min_delay, max_delay = int(raw_df['Payment Delay'].min()), int(raw_df['Payment Delay'].max())

        if 'filter_key' not in st.session_state:
            st.session_state.filter_key = 0

        def reset_filters():
            st.session_state.filter_key += 1

        if st.sidebar.button("🔄 Reset All Filters", on_click=reset_filters, use_container_width=True):
            st.rerun()

        fk = st.session_state.filter_key

        selected_genders = st.sidebar.multiselect("Gender", options=raw_df['Gender'].unique().tolist(), default=raw_df['Gender'].unique().tolist(), key=f"gender_{fk}")
        selected_subs = st.sidebar.multiselect("Subscription Plan", options=raw_df['Subscription Type'].unique().tolist(), default=raw_df['Subscription Type'].unique().tolist(), key=f"sub_{fk}")
        selected_contracts = st.sidebar.multiselect("Contract Term", options=raw_df['Contract Length'].unique().tolist(), default=raw_df['Contract Length'].unique().tolist(), key=f"contract_{fk}")
        
        churn_options = ["All Records", "Active (0)", "Churned (1)"]
        selected_churn = st.sidebar.selectbox("Churn Cohort", options=churn_options, index=0, key=f"churn_{fk}")

        selected_age = st.sidebar.slider("Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age), key=f"age_{fk}")
        selected_tenure = st.sidebar.slider("Tenure Window (Months)", min_value=min_tenure, max_value=max_tenure, value=(min_tenure, max_tenure), key=f"tenure_{fk}")
        selected_delay = st.sidebar.slider("Payment Delay (Days)", min_value=min_delay, max_value=max_delay, value=(min_delay, max_delay), key=f"delay_{fk}")

        filtered_df = raw_df[
            (raw_df['Gender'].isin(selected_genders)) &
            (raw_df['Subscription Type'].isin(selected_subs)) &
            (raw_df['Contract Length'].isin(selected_contracts)) &
            (raw_df['Age'].between(selected_age[0], selected_age[1])) &
            (raw_df['Tenure'].between(selected_tenure[0], selected_tenure[1])) &
            (raw_df['Payment Delay'].between(selected_delay[0], selected_delay[1]))
        ]

        if selected_churn == "Active (0)":
            filtered_df = filtered_df[filtered_df['Churn'] == 0]
        elif selected_churn == "Churned (1)":
            filtered_df = filtered_df[filtered_df['Churn'] == 1]

        applied_filters = {
            "Genders": ", ".join(selected_genders),
            "Subscriptions": ", ".join(selected_subs),
            "Contracts": ", ".join(selected_contracts),
            "Cohort": selected_churn,
            "Age Range": f"{selected_age[0]} - {selected_age[1]}",
            "Tenure Window": f"{selected_tenure[0]} - {selected_tenure[1]} Mos",
            "Payment Delay": f"{selected_delay[0]} - {selected_delay[1]} Days"
        }

        if filtered_df.empty:
            st.markdown("""
                <div style="padding: 20px; border-radius: 12px; border: 1px solid rgba(245, 158, 11, 0.3); background: rgba(245, 158, 11, 0.05); text-align: center;">
                    <h3 style="color: #f59e0b; margin-top:0;">⚠️ No Data Matching Selection</h3>
                    <p style="color: #d1d5db; margin-bottom: 0;">Adjust your filter sliders or click 'Reset All Filters' in the sidebar to restore views.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            df_sample, size, info, columns, missing_values, stats_dataset = about_df(filtered_df)
            stats = customer_statistics(filtered_df)
            future_ints = future_insights(filtered_df)

            if menu_selection == "👥 User Access Control (Admin)" and user_role == "Admin":
                st.title("👥 User Access Management")
                st.caption("Manage registered users and system authorization levels.")
                users_data = [{"Username": u_id, "Name": u_info.get("name"), "Email": u_info.get("email"), "Role": u_info.get("role", "Analyst")} for u_id, u_info in config['credentials']['usernames'].items()]
                st.dataframe(pd.DataFrame(users_data), use_container_width=True)

            elif menu_selection == "Executive Dashboard":
                st.title("🎯 Executive Retention Dashboard")
                st.caption(f"Real-time pipeline analytics for **{len(filtered_df):,}** active segment records.")
                
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Total Account Scope", f"{len(filtered_df):,}")
                k2.metric("Mean Tenure", f"{stats.get('Average Tenure', 0):.1f} Mos")
                k3.metric("Gross Revenue", f"${stats.get('Total Spend', 0):,.2f}")
                k4.metric("Churn Rate", f"{stats.get('Churn Rate (%)', 0):.1f}%")
                
                st.divider()
                render_charts(filtered_df)

            elif menu_selection == "Churn Driver Analysis":
                st.title("🎯 Churn Intelligence & Risk Analysis")
                st.caption("Identify churn hotspots and optimize retention interventions.")
                render_churn_analysis(filtered_df)

            elif menu_selection == "Dataset Metadata":
                st.title("📋 Dataset Telemetry & Schema")
                st.subheader("Data Matrix Dimensions")
                st.info(f"Filtered Records: **{size[0]:,}** | Attributes: **{size[1]}**")
                st.subheader("Random Data Sample")
                st.dataframe(df_sample, use_container_width=True)
                st.subheader("Missing Value Audit")
                st.write(missing_values)
                st.subheader("Attribute Types")
                st.write(columns)
                st.subheader("Internal Info Log")
                st.code(info, language="text")
                st.subheader("Descriptive Summary")
                st.dataframe(stats_dataset, use_container_width=True)

            elif menu_selection == "Customer Statistics":
                st.title("📈 Aggregated Customer KPIs")
                st.caption("Deep statistical summary of customer behavior.")
                grid = st.columns(3)
                for idx, (k, v) in enumerate(stats.items()):
                    with grid[idx % 3]:
                        st.metric(label=k, value=f"{v:,.2f}" if isinstance(v, (int, float)) else str(v))

            elif menu_selection == "Predictive Forecasts":
                st.title("🔮 Forward Revenue Projections")
                st.caption("Model-driven 12-month run rate projections.")
                grid = st.columns(3)
                for idx, (k, v) in enumerate(future_ints.items()):
                    with grid[idx % 3]:
                        st.metric(label=k, value=f"{v:,.2f}" if isinstance(v, (int, float)) else str(v))

            elif menu_selection == "📥 Export & Reporting":
                st.title("📥 Export Data & Executive Reports")
                st.caption("Download structured customer datasets and generate executive summary PDF reports.")

                st.subheader("📌 Current Filter Context Snapshot")
                filter_cols = st.columns(3)
                for idx, (f_name, f_val) in enumerate(applied_filters.items()):
                    with filter_cols[idx % 3]:
                        st.caption(f"**{f_name}:** `{f_val}`")
                
                st.divider()

                exp_col1, exp_col2, exp_col3 = st.columns(3)

                with exp_col1:
                    st.markdown("""
                        <div style="padding: 20px; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.3); background: rgba(15, 23, 42, 0.6);">
                            <h4 style="color: #3b82f6; margin-top: 0;">📄 Filtered Dataset (CSV)</h4>
                            <p style="font-size: 0.85rem; color: #9ca3af;">Download full filtered raw data as a clean CSV file.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if not filtered_df.empty:
                        csv_bytes = convert_df_to_csv(filtered_df)
                        st.download_button(
                            label="📥 Download CSV Dataset",
                            data=csv_bytes,
                            file_name=f"ChurnPulse_Filtered_Data_{datetime.date.today()}.csv",
                            mime="text/csv",
                            key="btn_csv_download",
                            use_container_width=True
                        )

                with exp_col2:
                    st.markdown("""
                        <div style="padding: 20px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.3); background: rgba(15, 23, 42, 0.6);">
                            <h4 style="color: #10b981; margin-top: 0;">📊 Filtered Dataset (Excel)</h4>
                            <p style="font-size: 0.85rem; color: #9ca3af;">Export data into an Excel spreadsheet for off-grid analysis.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if not filtered_df.empty:
                        excel_bytes = convert_df_to_excel_cached(filtered_df)
                        st.download_button(
                            label="📥 Download Excel File",
                            data=excel_bytes,
                            file_name=f"ChurnPulse_Filtered_Data_{datetime.date.today()}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="btn_excel_download",
                            use_container_width=True
                        )
                    else:
                        st.warning("No data available to export.")

                with exp_col3:
                    st.markdown("""
                        <div style="padding: 20px; border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.3); background: rgba(15, 23, 42, 0.6);">
                            <h4 style="color: #8b5cf6; margin-top: 0;">📑 PDF Executive Summary</h4>
                            <p style="font-size: 0.85rem; color: #9ca3af;">Generate branded PDF containing KPIs & insights snapshot.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if not filtered_df.empty:
                        pdf_bytes = generate_pdf_report(filtered_df, applied_filters, stats)
                        st.download_button(
                            label="📑 Export Branded PDF Report",
                            data=pdf_bytes,
                            file_name=f"ZainTech_ChurnPulse_Report_{datetime.date.today()}.pdf",
                            mime="application/pdf",
                            key="btn_pdf_download",
                            use_container_width=True
                        )

                st.divider()

                st.subheader("🎯 Individual High-Risk Account Data Downloader")
                st.caption("Filter and isolate individual customer records exhibiting churn indicators for manual outreach.")
                
                if 'Churn' in filtered_df.columns:
                    high_risk_customers = filtered_df[filtered_df['Churn'] == 1]
                    st.write(f"High-Risk Churn Cohort Count: **{len(high_risk_customers):,} Records**")
                    st.dataframe(high_risk_customers.head(10), use_container_width=True)
                    
                    if not high_risk_customers.empty:
                        risk_csv = convert_df_to_csv(high_risk_customers)
                        st.download_button(
                            label="🚨 Download High-Risk Accounts Cohort (CSV)",
                            data=risk_csv,
                            file_name=f"High_Risk_Churn_Cohort_{datetime.date.today()}.csv",
                            mime="text/csv",
                            key="btn_risk_csv_download",
                            use_container_width=True
                        )

    else:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(139, 92, 246, 0.08) 100%);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 20px;
                padding: 60px 40px;
                text-align: center;
                margin-top: 15px;
                margin-bottom: 35px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            ">
                <span style="
                    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
                    color: #ffffff; 
                    font-size: 0.8rem; 
                    font-weight: 800; 
                    padding: 6px 16px; 
                    border-radius: 30px; 
                    letter-spacing: 1px;
                    text-transform: uppercase;
                ">Enterprise Intelligence Platform</span>
                <h1 style="font-size: 3rem; font-weight: 900; margin-top: 20px; margin-bottom: 15px; color: #ffffff; line-height: 1.15;">
                    Predict Customer Churn.<br><span style="color: #3b82f6;">Maximize Lifetime Value.</span>
                </h1>
                <p style="font-size: 1.15rem; color: #9ca3af; max-width: 680px; margin: 0 auto 25px auto; line-height: 1.6;">
                    Upload raw usage & billing datasets to instantly generate cohort diagnostics, key risk factors, and actionable retention playbooks.
                </p>
            </div>
        """, unsafe_allow_html=True)