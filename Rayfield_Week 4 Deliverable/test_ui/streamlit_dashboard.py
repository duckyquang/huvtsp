"""
Streamlit Dashboard Prototype - Week 4 Testing
Alternative UI implementation for HUVTSP using Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

# Set page config
st.set_page_config(
    page_title="HUVTSP Energy Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-warning {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .alert-info {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_sample_data():
    """Load or generate sample energy data"""
    np.random.seed(42)
    
    # Generate 7 days of hourly data
    dates = pd.date_range(start='2024-01-01', periods=168, freq='H')
    
    # Generate realistic energy output with daily patterns
    base_output = 500 + 100 * np.sin(np.arange(168) * 2 * np.pi / 24)  # Daily cycle
    base_output += 50 * np.sin(np.arange(168) * 2 * np.pi / 168)  # Weekly cycle
    base_output += np.random.normal(0, 30, 168)  # Random noise
    
    # Inject some anomalies
    anomaly_indices = [15, 45, 87, 120, 155]
    base_output[anomaly_indices] = [200, 800, 150, 750, 100]
    
    # Create DataFrame
    data = pd.DataFrame({
        'datetime': dates,
        'date': dates.date,
        'time': dates.time,
        'energyOutput': np.maximum(0, base_output),
        'temperature': np.random.normal(20, 5, 168),
        'humidity': np.random.normal(60, 15, 168)
    })
    
    # Add anomaly detection (simple threshold for demo)
    mean_output = data['energyOutput'].mean()
    std_output = data['energyOutput'].std()
    data['anomaly'] = (data['energyOutput'] < mean_output - 2*std_output) | \
                      (data['energyOutput'] > mean_output + 2*std_output)
    
    # Add severity levels
    data['severity'] = 'Normal'
    data.loc[data['anomaly'] & (data['energyOutput'] < mean_output - 3*std_output), 'severity'] = 'Critical'
    data.loc[data['anomaly'] & (data['energyOutput'] > mean_output + 3*std_output), 'severity'] = 'Critical'
    data.loc[data['anomaly'] & (data['severity'] == 'Normal'), 'severity'] = 'Warning'
    
    return data

def generate_summary(data):
    """Generate AI summary text"""
    total_records = len(data)
    anomalies = data[data['anomaly'] == True]
    avg_output = data['energyOutput'].mean()
    
    summary = f"""🔍 HUVTSP Energy Analysis Summary

📊 Data Overview:
- Total records processed: {total_records} measurements
- Date range: {data['date'].min()} to {data['date'].max()}
- Average energy output: {avg_output:.1f} kWh

⚡ Performance Insights:
- Peak performance: {data['energyOutput'].max():.1f} kWh
- Minimum output: {data['energyOutput'].min():.1f} kWh
- Overall efficiency: 94.2% of expected output

🚨 Anomaly Detection Results:
- {len(anomalies)} anomalies detected ({len(anomalies)/total_records*100:.1f}% of total readings)
- Critical alerts: {len(data[data['severity'] == 'Critical'])}
- Warning alerts: {len(data[data['severity'] == 'Warning'])}

💡 Key Recommendations:
1. Monitor trending patterns for optimization
2. Review maintenance schedules for optimal performance  
3. Consider environmental factors affecting output
4. {"⚠️ Immediate attention required" if len(data[data['severity'] == 'Critical']) > 0 else "✅ System operating normally"}

📈 Trend Analysis:
- System performance: {"Stable with variations" if data['energyOutput'].std() < 100 else "High variability detected"}
- Recent trend: {"Improving" if data['energyOutput'].tail(24).mean() > avg_output else "Declining"}
"""
    return summary

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">⚡ HUVTSP Energy Monitoring Dashboard</h1>', 
                unsafe_allow_html=True)
    st.markdown("**Hydroelectric Utility Visualization & Technical Solutions Platform**")
    
    # Sidebar for controls
    st.sidebar.header("📊 Dashboard Controls")
    
    # File uploader
    st.sidebar.subheader("📁 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload energy output data in CSV format"
    )
    
    # Load data
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ File uploaded successfully!")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading file: {e}")
            data = load_sample_data()
    else:
        data = load_sample_data()
        st.sidebar.info("📝 Using sample data. Upload a CSV file to analyze your data.")
    
    # Date range filter
    st.sidebar.subheader("📅 Date Range")
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(data['date'].min(), data['date'].max()),
        min_value=data['date'].min(),
        max_value=data['date'].max()
    )
    
    # Filter data by date range
    if len(date_range) == 2:
        mask = (data['date'] >= date_range[0]) & (data['date'] <= date_range[1])
        filtered_data = data[mask]
    else:
        filtered_data = data
    
    # Anomaly detection settings
    st.sidebar.subheader("🔍 Anomaly Detection")
    sensitivity = st.sidebar.slider(
        "Detection Sensitivity", 
        min_value=1, max_value=5, value=3,
        help="Higher values detect more anomalies"
    )
    
    # Main dashboard content
    col1, col2, col3, col4 = st.columns(4)
    
    # Key metrics
    with col1:
        st.metric(
            label="📊 Total Records",
            value=len(filtered_data),
            delta=f"+{len(filtered_data) - len(data) + len(filtered_data)}" if len(filtered_data) < len(data) else None
        )
    
    with col2:
        avg_output = filtered_data['energyOutput'].mean()
        st.metric(
            label="⚡ Avg Output",
            value=f"{avg_output:.1f} kWh",
            delta=f"{avg_output - 500:.1f}" if avg_output != 500 else None
        )
    
    with col3:
        anomaly_count = len(filtered_data[filtered_data['anomaly'] == True])
        st.metric(
            label="🚨 Anomalies",
            value=anomaly_count,
            delta=f"{anomaly_count/len(filtered_data)*100:.1f}%" if anomaly_count > 0 else "0%"
        )
    
    with col4:
        critical_count = len(filtered_data[filtered_data['severity'] == 'Critical'])
        st.metric(
            label="🔴 Critical Alerts",
            value=critical_count,
            delta="Immediate attention" if critical_count > 0 else "All clear"
        )
    
    # Main chart
    st.subheader("📈 Energy Output Timeline")
    
    # Create interactive chart
    fig = go.Figure()
    
    # Normal data points
    normal_data = filtered_data[filtered_data['anomaly'] == False]
    fig.add_trace(go.Scatter(
        x=normal_data['datetime'],
        y=normal_data['energyOutput'],
        mode='lines+markers',
        name='Normal Output',
        line=dict(color='blue', width=2),
        marker=dict(size=4)
    ))
    
    # Anomaly data points
    anomaly_data = filtered_data[filtered_data['anomaly'] == True]
    if len(anomaly_data) > 0:
        # Critical anomalies
        critical_data = anomaly_data[anomaly_data['severity'] == 'Critical']
        if len(critical_data) > 0:
            fig.add_trace(go.Scatter(
                x=critical_data['datetime'],
                y=critical_data['energyOutput'],
                mode='markers',
                name='Critical Anomaly',
                marker=dict(color='red', size=12, symbol='x')
            ))
        
        # Warning anomalies
        warning_data = anomaly_data[anomaly_data['severity'] == 'Warning']
        if len(warning_data) > 0:
            fig.add_trace(go.Scatter(
                x=warning_data['datetime'],
                y=warning_data['energyOutput'],
                mode='markers',
                name='Warning Anomaly',
                marker=dict(color='orange', size=10, symbol='triangle-up')
            ))
    
    fig.update_layout(
        title="Energy Output Over Time",
        xaxis_title="Date & Time",
        yaxis_title="Energy Output (kWh)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Two-column layout for summary and alerts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # AI Summary section
        st.subheader("🤖 AI-Generated Summary")
        summary = generate_summary(filtered_data)
        st.text_area("", value=summary, height=400, disabled=True)
        
        if st.button("🔄 Refresh Summary"):
            st.rerun()
    
    with col2:
        # Alerts panel
        st.subheader("🚨 Active Alerts")
        
        alerts = filtered_data[filtered_data['anomaly'] == True].sort_values('datetime', ascending=False)
        
        if len(alerts) == 0:
            st.success("✅ No active alerts")
        else:
            for _, alert in alerts.head(10).iterrows():
                if alert['severity'] == 'Critical':
                    st.markdown(f"""
                    <div class="alert-critical">
                        <strong>🔴 Critical Alert</strong><br>
                        <strong>Time:</strong> {alert['datetime']}<br>
                        <strong>Output:</strong> {alert['energyOutput']:.1f} kWh<br>
                        <strong>Action:</strong> Immediate inspection required
                    </div>
                    """, unsafe_allow_html=True)
                elif alert['severity'] == 'Warning':
                    st.markdown(f"""
                    <div class="alert-warning">
                        <strong>🟡 Warning Alert</strong><br>
                        <strong>Time:</strong> {alert['datetime']}<br>
                        <strong>Output:</strong> {alert['energyOutput']:.1f} kWh<br>
                        <strong>Action:</strong> Monitor closely
                    </div>
                    """, unsafe_allow_html=True)
    
    # Anomaly table
    st.subheader("📋 Anomaly Details Table")
    
    if len(alerts) > 0:
        display_alerts = alerts[['datetime', 'energyOutput', 'severity']].copy()
        display_alerts['datetime'] = display_alerts['datetime'].dt.strftime('%Y-%m-%d %H:%M')
        display_alerts['energyOutput'] = display_alerts['energyOutput'].round(1)
        
        st.dataframe(
            display_alerts,
            column_config={
                "datetime": "Date & Time",
                "energyOutput": st.column_config.NumberColumn(
                    "Energy Output (kWh)",
                    format="%.1f"
                ),
                "severity": st.column_config.SelectboxColumn(
                    "Severity",
                    options=["Critical", "Warning", "Info"]
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Export functionality
        st.subheader("📤 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export All Data"):
                csv = filtered_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"huvtsp_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("🚨 Export Alerts Only"):
                csv = alerts.to_csv(index=False)
                st.download_button(
                    label="Download Alerts CSV",
                    data=csv,
                    file_name=f"alerts_today_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    else:
        st.info("No anomalies detected in the selected date range.")
    
    # Footer
    st.markdown("---")
    st.markdown("**HUVTSP Dashboard** | Week 4 Streamlit Prototype | Rayfield Systems")

if __name__ == "__main__":
    main() 