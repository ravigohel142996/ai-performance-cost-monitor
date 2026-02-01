"""
AI Project Performance & Cost Monitor
A production-quality Streamlit dashboard for monitoring AI system health, cost, and performance.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="AI Performance & Cost Monitor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
def load_custom_css():
    """Load custom CSS for enhanced UI"""
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            font-weight: 600;
        }
        .risk-green {
            color: #28a745;
            font-weight: bold;
            font-size: 1.2em;
        }
        .risk-yellow {
            color: #ffc107;
            font-weight: bold;
            font-size: 1.2em;
        }
        .risk-red {
            color: #dc3545;
            font-weight: bold;
            font-size: 1.2em;
        }
        h1 {
            color: #1f77b4;
            text-align: center;
            padding-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def calculate_monthly_cost(api_calls, ram_gb, cpu_percent):
    """
    Calculate estimated monthly cloud cost
    Formula: cost = (api_calls * 0.002) + (ram * 15) + (cpu * 0.5)
    
    Args:
        api_calls: Daily API calls
        ram_gb: RAM usage in GB
        cpu_percent: CPU usage percentage
        
    Returns:
        float: Monthly cost in USD
    """
    try:
        # Convert daily API calls to monthly
        monthly_api_calls = api_calls * 30
        monthly_cost = (monthly_api_calls * 0.002) + (ram_gb * 15) + (cpu_percent * 0.5)
        return round(monthly_cost, 2)
    except Exception as e:
        st.error(f"Error calculating cost: {e}")
        return 0.0

def calculate_performance_score(response_time_ms, cpu_percent):
    """
    Calculate performance score (0-100) based on response time and CPU usage
    
    Args:
        response_time_ms: Average response time in milliseconds
        cpu_percent: CPU usage percentage
        
    Returns:
        int: Performance score (0-100)
    """
    try:
        # Response time scoring (50% weight)
        # Ideal: < 200ms = 50 points, > 2000ms = 0 points
        if response_time_ms < 200:
            response_score = 50
        elif response_time_ms > 2000:
            response_score = 0
        else:
            response_score = 50 * (1 - (response_time_ms - 200) / 1800)
        
        # CPU usage scoring (50% weight)
        # Ideal: < 50% = 50 points, > 90% = 0 points
        if cpu_percent < 50:
            cpu_score = 50
        elif cpu_percent > 90:
            cpu_score = 0
        else:
            cpu_score = 50 * (1 - (cpu_percent - 50) / 40)
        
        total_score = int(response_score + cpu_score)
        return max(0, min(100, total_score))
    except Exception as e:
        st.error(f"Error calculating performance score: {e}")
        return 0

def determine_risk_level(performance_score, response_time_ms, cpu_percent):
    """
    Determine risk level based on performance metrics
    
    Args:
        performance_score: Calculated performance score
        response_time_ms: Average response time
        cpu_percent: CPU usage percentage
        
    Returns:
        tuple: (risk_level: str, risk_color: str)
    """
    try:
        # High risk conditions
        if performance_score < 40 or response_time_ms > 1500 or cpu_percent > 85:
            return "RED - High Risk", "risk-red"
        # Medium risk conditions
        elif performance_score < 70 or response_time_ms > 800 or cpu_percent > 70:
            return "YELLOW - Medium Risk", "risk-yellow"
        # Low risk (healthy system)
        else:
            return "GREEN - Low Risk", "risk-green"
    except Exception as e:
        st.error(f"Error determining risk level: {e}")
        return "UNKNOWN", "risk-yellow"

def get_system_health(performance_score):
    """
    Get system health status based on performance score
    
    Args:
        performance_score: Performance score (0-100)
        
    Returns:
        str: Health status
    """
    if performance_score >= 80:
        return "Excellent 🟢"
    elif performance_score >= 60:
        return "Good 🟡"
    elif performance_score >= 40:
        return "Fair 🟠"
    else:
        return "Poor 🔴"

def get_optimization_tips(response_time_ms, cpu_percent, ram_gb, api_calls):
    """
    Generate optimization tips based on metrics
    
    Args:
        response_time_ms: Average response time
        cpu_percent: CPU usage percentage
        ram_gb: RAM usage
        api_calls: Daily API calls
        
    Returns:
        list: List of optimization tips
    """
    tips = []
    
    if response_time_ms > 1000:
        tips.append("⚠️ High response time detected. Consider implementing caching or optimizing algorithms.")
    if cpu_percent > 80:
        tips.append("⚠️ High CPU usage. Consider horizontal scaling or optimizing compute-intensive operations.")
    if ram_gb > 16:
        tips.append("💡 High RAM usage. Monitor for memory leaks and optimize data structures.")
    if api_calls > 100000:
        tips.append("💡 High API call volume. Implement rate limiting and consider batch processing.")
    if response_time_ms < 500 and cpu_percent < 50:
        tips.append("✅ System performing well! Continue monitoring for any changes.")
    if not tips:
        tips.append("✅ All metrics within normal ranges. Keep up the good work!")
    
    return tips

def create_performance_gauge(performance_score):
    """
    Create a gauge chart for performance score
    
    Args:
        performance_score: Performance score (0-100)
        
    Returns:
        plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=performance_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Performance Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffcccc'},
                {'range': [40, 70], 'color': '#ffffcc'},
                {'range': [70, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_metrics_dataframe(project_name, daily_users, api_calls, ram_gb, cpu_percent, 
                             response_time_ms, monthly_cost, performance_score, 
                             risk_level, system_health):
    """
    Create a dataframe for CSV export
    
    Returns:
        pandas.DataFrame
    """
    data = {
        'Metric': [
            'Project Name',
            'Daily Users',
            'API Calls per Day',
            'RAM Usage (GB)',
            'CPU Usage (%)',
            'Avg Response Time (ms)',
            'Monthly Cloud Cost (USD)',
            'Performance Score',
            'Risk Level',
            'System Health',
            'Report Generated'
        ],
        'Value': [
            project_name,
            daily_users,
            api_calls,
            ram_gb,
            cpu_percent,
            response_time_ms,
            f"${monthly_cost}",
            performance_score,
            risk_level,
            system_health,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
    }
    
    return pd.DataFrame(data)

def main():
    """Main application function"""
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state for theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Header
    st.title("🤖 AI Project Performance & Cost Monitor")
    st.markdown("### Monitor your AI system's health, performance, and cloud costs")
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Dark/Light mode toggle
        theme_col1, theme_col2 = st.columns([3, 1])
        with theme_col1:
            st.markdown("**Theme Mode:**")
        with theme_col2:
            if st.button("🌓"):
                st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
                st.rerun()
        
        st.markdown("---")
        
        # User Inputs
        st.subheader("📊 Project Details")
        
        project_name = st.text_input(
            "Project Name",
            value="AI ChatBot v1.0",
            help="Enter your AI project name"
        )
        
        daily_users = st.number_input(
            "Daily Users",
            min_value=0,
            value=1000,
            step=100,
            help="Number of daily active users"
        )
        
        api_calls = st.number_input(
            "API Calls per Day",
            min_value=0,
            value=50000,
            step=1000,
            help="Total API calls per day"
        )
        
        st.markdown("---")
        st.subheader("💻 Resource Usage")
        
        ram_gb = st.number_input(
            "RAM Usage (GB)",
            min_value=0.0,
            value=8.0,
            step=0.5,
            format="%.1f",
            help="Average RAM usage in GB"
        )
        
        cpu_percent = st.slider(
            "CPU Usage (%)",
            min_value=0,
            max_value=100,
            value=65,
            help="Average CPU usage percentage"
        )
        
        response_time_ms = st.number_input(
            "Avg Response Time (ms)",
            min_value=0,
            value=450,
            step=10,
            help="Average API response time in milliseconds"
        )
        
        st.markdown("---")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            calculate_button = st.button("📈 Calculate", type="primary")
        with col2:
            reset_button = st.button("🔄 Reset")
    
    # Reset functionality
    if reset_button:
        st.rerun()
    
    # Main content area
    if calculate_button or 'calculated' in st.session_state:
        st.session_state.calculated = True
        
        # Calculate metrics
        monthly_cost = calculate_monthly_cost(api_calls, ram_gb, cpu_percent)
        performance_score = calculate_performance_score(response_time_ms, cpu_percent)
        risk_level, risk_class = determine_risk_level(performance_score, response_time_ms, cpu_percent)
        system_health = get_system_health(performance_score)
        optimization_tips = get_optimization_tips(response_time_ms, cpu_percent, ram_gb, api_calls)
        
        # Display key metrics in cards
        st.subheader("📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Monthly Cloud Cost",
                value=f"${monthly_cost:,.2f}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="⚡ Performance Score",
                value=f"{performance_score}/100",
                delta=None
            )
        
        with col3:
            st.markdown(f"**🚦 Risk Level**")
            st.markdown(f'<p class="{risk_class}">{risk_level}</p>', unsafe_allow_html=True)
        
        with col4:
            st.metric(
                label="💚 System Health",
                value=system_health,
                delta=None
            )
        
        st.markdown("---")
        
        # Performance visualization and details
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📈 Performance Gauge")
            fig = create_performance_gauge(performance_score)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📋 System Metrics")
            metrics_data = {
                'Metric': ['Daily Users', 'API Calls/Day', 'RAM Usage', 'CPU Usage', 'Response Time'],
                'Value': [
                    f"{daily_users:,}",
                    f"{api_calls:,}",
                    f"{ram_gb} GB",
                    f"{cpu_percent}%",
                    f"{response_time_ms} ms"
                ]
            }
            st.dataframe(pd.DataFrame(metrics_data), hide_index=True, use_container_width=True)
        
        st.markdown("---")
        
        # Optimization Tips
        st.subheader("💡 Optimization Tips")
        for tip in optimization_tips:
            st.info(tip)
        
        st.markdown("---")
        
        # Cost Breakdown
        st.subheader("💵 Cost Breakdown")
        cost_col1, cost_col2, cost_col3 = st.columns(3)
        
        api_cost = api_calls * 30 * 0.002
        ram_cost = ram_gb * 15
        cpu_cost = cpu_percent * 0.5
        
        with cost_col1:
            st.metric("API Costs", f"${api_cost:,.2f}")
        with cost_col2:
            st.metric("RAM Costs", f"${ram_cost:,.2f}")
        with cost_col3:
            st.metric("CPU Costs", f"${cpu_cost:,.2f}")
        
        # Progress bar for performance
        st.markdown("---")
        st.subheader("📊 Performance Progress")
        st.progress(performance_score / 100)
        st.caption(f"System is operating at {performance_score}% efficiency")
        
        # Download report
        st.markdown("---")
        st.subheader("📥 Export Report")
        
        # Create report dataframe
        report_df = create_metrics_dataframe(
            project_name, daily_users, api_calls, ram_gb, cpu_percent,
            response_time_ms, monthly_cost, performance_score,
            risk_level, system_health
        )
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        report_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Report as CSV",
            data=csv_data,
            file_name=f"ai_monitor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    else:
        # Welcome screen
        st.info("👈 Please configure your project details in the sidebar and click '📈 Calculate' to view the analysis.")
        
        # Feature showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 💰 Cost Monitoring")
            st.write("Track and estimate your monthly cloud costs based on API usage, RAM, and CPU consumption.")
        
        with col2:
            st.markdown("### ⚡ Performance Scoring")
            st.write("Get real-time performance scores based on response times and resource utilization.")
        
        with col3:
            st.markdown("### 🚦 Risk Assessment")
            st.write("Identify potential issues with color-coded risk levels and actionable insights.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "AI Project Performance & Cost Monitor v1.0 | Built with Streamlit 🚀"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
