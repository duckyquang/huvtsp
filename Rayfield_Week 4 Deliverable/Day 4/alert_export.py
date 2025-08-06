"""
Alert Export System for HUVTSP
Exports daily anomaly alerts to CSV for Zapier integration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
import json
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('alert_export.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AlertExporter:
    def __init__(self, output_dir="./exports"):
        """
        Initialize Alert Exporter
        
        Args:
            output_dir (str): Directory to save exported CSV files
        """
        self.output_dir = output_dir
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")
    
    def filter_anomalies_by_date(self, data, target_date=None):
        """
        Filter anomalies for a specific date
        
        Args:
            data (pd.DataFrame): Anomaly data with date column
            target_date (str): Target date in 'YYYY-MM-DD' format
            
        Returns:
            pd.DataFrame: Filtered anomalies for the target date
        """
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        # Ensure date column is datetime
        if 'date' in data.columns:
            data['date'] = pd.to_datetime(data['date'])
            
            # Filter for target date
            target_datetime = pd.to_datetime(target_date)
            filtered_data = data[data['date'].dt.date == target_datetime.date()]
            
            logger.info(f"Filtered {len(filtered_data)} anomalies for date {target_date}")
            return filtered_data
        else:
            logger.warning("No 'date' column found in data")
            return pd.DataFrame()
    
    def format_alert_data(self, anomaly_data):
        """
        Format anomaly data for export
        
        Args:
            anomaly_data (pd.DataFrame): Raw anomaly data
            
        Returns:
            pd.DataFrame: Formatted data ready for export
        """
        if anomaly_data.empty:
            return pd.DataFrame()
        
        # Standard columns for alert export
        export_columns = {
            'alert_id': range(1, len(anomaly_data) + 1),
            'timestamp': anomaly_data.get('date', ''),
            'energy_kwh': anomaly_data.get('energyOutput', 0),
            'severity': anomaly_data.get('severity', 'Unknown'),
            'anomaly_score': anomaly_data.get('anomaly_score', 0),
            'deviation_percentage': '',
            'expected_min': '',
            'expected_max': '',
            'system_status': '',
            'recommended_action': anomaly_data.get('recommended_action', 'Review and investigate'),
            'units_affected': 'Primary System',
            'trend_direction': '',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Create formatted DataFrame
        formatted_data = pd.DataFrame(export_columns)
        
        # Calculate additional fields
        if 'energyOutput' in anomaly_data.columns:
            mean_output = anomaly_data['energyOutput'].mean()
            std_output = anomaly_data['energyOutput'].std()
            
            formatted_data['expected_min'] = max(0, mean_output - 2 * std_output)
            formatted_data['expected_max'] = mean_output + 2 * std_output
            
            # Calculate deviation percentage
            formatted_data['deviation_percentage'] = abs(
                (formatted_data['energy_kwh'] - mean_output) / mean_output * 100
            ).round(2)
        
        # Determine system status based on severity
        formatted_data['system_status'] = formatted_data['severity'].map({
            'Critical': 'Requires Immediate Attention',
            'Warning': 'Monitoring Required',
            'Info': 'Normal Operation',
            'Normal': 'Operating Normally'
        }).fillna('Under Review')
        
        # Determine trend direction based on energy output
        if len(formatted_data) > 1:
            formatted_data['trend_direction'] = 'Declining' if formatted_data['energy_kwh'].is_monotonic_decreasing else 'Variable'
        else:
            formatted_data['trend_direction'] = 'Single Point'
        
        return formatted_data
    
    def export_daily_alerts(self, anomaly_data, export_date=None, filename_prefix="alerts"):
        """
        Export daily alerts to CSV
        
        Args:
            anomaly_data (pd.DataFrame): Complete anomaly dataset
            export_date (str): Date to export (YYYY-MM-DD format)
            filename_prefix (str): Prefix for output filename
            
        Returns:
            tuple: (export_path, alert_count, summary_stats)
        """
        if export_date is None:
            export_date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"Starting export for date: {export_date}")
        
        # Filter anomalies for the target date
        daily_anomalies = self.filter_anomalies_by_date(anomaly_data, export_date)
        
        # Format data for export
        formatted_data = self.format_alert_data(daily_anomalies)
        
        # Generate filename
        filename = f"{filename_prefix}_{export_date.replace('-', '')}.csv"
        export_path = os.path.join(self.output_dir, filename)
        
        # Export to CSV
        if not formatted_data.empty:
            formatted_data.to_csv(export_path, index=False)
            logger.info(f"Exported {len(formatted_data)} alerts to {export_path}")
        else:
            # Create empty file with headers for consistency
            headers = ['alert_id', 'timestamp', 'energy_kwh', 'severity', 'anomaly_score',
                      'deviation_percentage', 'expected_min', 'expected_max', 'system_status',
                      'recommended_action', 'units_affected', 'trend_direction', 'created_at']
            pd.DataFrame(columns=headers).to_csv(export_path, index=False)
            logger.info(f"No alerts found for {export_date}. Created empty file: {export_path}")
        
        # Generate summary statistics
        summary_stats = self.generate_summary_stats(formatted_data, export_date)
        
        # Save summary as JSON
        summary_path = export_path.replace('.csv', '_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary_stats, f, indent=2, default=str)
        
        return export_path, len(formatted_data), summary_stats
    
    def generate_summary_stats(self, alert_data, export_date):
        """
        Generate summary statistics for exported alerts
        
        Args:
            alert_data (pd.DataFrame): Formatted alert data
            export_date (str): Export date
            
        Returns:
            dict: Summary statistics
        """
        if alert_data.empty:
            return {
                'export_date': export_date,
                'total_alerts': 0,
                'severity_breakdown': {},
                'avg_energy_output': 0,
                'avg_deviation': 0,
                'status': 'No alerts',
                'export_timestamp': datetime.now().isoformat()
            }
        
        severity_counts = alert_data['severity'].value_counts().to_dict()
        
        summary = {
            'export_date': export_date,
            'total_alerts': len(alert_data),
            'severity_breakdown': severity_counts,
            'critical_alerts': severity_counts.get('Critical', 0),
            'warning_alerts': severity_counts.get('Warning', 0),
            'info_alerts': severity_counts.get('Info', 0),
            'avg_energy_output': float(alert_data['energy_kwh'].mean()),
            'min_energy_output': float(alert_data['energy_kwh'].min()),
            'max_energy_output': float(alert_data['energy_kwh'].max()),
            'avg_deviation': float(alert_data['deviation_percentage'].mean()),
            'max_deviation': float(alert_data['deviation_percentage'].max()),
            'primary_trend': alert_data['trend_direction'].mode().iloc[0] if not alert_data.empty else 'N/A',
            'systems_affected': alert_data['units_affected'].nunique(),
            'status': 'Critical' if severity_counts.get('Critical', 0) > 0 else 'Normal',
            'export_timestamp': datetime.now().isoformat(),
            'recommendations': self.get_recommendations(alert_data)
        }
        
        return summary
    
    def get_recommendations(self, alert_data):
        """
        Generate recommendations based on alert data
        
        Args:
            alert_data (pd.DataFrame): Alert data
            
        Returns:
            list: List of recommendations
        """
        if alert_data.empty:
            return ["No immediate action required - no anomalies detected"]
        
        recommendations = []
        
        critical_count = len(alert_data[alert_data['severity'] == 'Critical'])
        warning_count = len(alert_data[alert_data['severity'] == 'Warning'])
        
        if critical_count > 0:
            recommendations.append(f"Immediate attention required: {critical_count} critical anomalies detected")
            recommendations.append("Contact on-call engineer for immediate investigation")
        
        if warning_count > 2:
            recommendations.append(f"Monitor closely: {warning_count} warning-level anomalies detected")
            recommendations.append("Schedule maintenance check within 24 hours")
        
        if alert_data['deviation_percentage'].max() > 50:
            recommendations.append("High deviation detected - investigate potential equipment issues")
        
        if len(recommendations) == 0:
            recommendations.append("Continue normal monitoring procedures")
        
        return recommendations
    
    def batch_export(self, anomaly_data, date_range_days=7):
        """
        Export alerts for multiple days
        
        Args:
            anomaly_data (pd.DataFrame): Complete anomaly dataset
            date_range_days (int): Number of days to export (from today backwards)
            
        Returns:
            list: List of export results
        """
        results = []
        
        for i in range(date_range_days):
            export_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            try:
                export_path, count, stats = self.export_daily_alerts(anomaly_data, export_date)
                results.append({
                    'date': export_date,
                    'file_path': export_path,
                    'alert_count': count,
                    'status': 'success'
                })
            except Exception as e:
                logger.error(f"Failed to export for {export_date}: {str(e)}")
                results.append({
                    'date': export_date,
                    'file_path': None,
                    'alert_count': 0,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results

def create_sample_anomaly_data():
    """Create sample anomaly data for testing"""
    np.random.seed(42)
    
    # Generate dates for the last 7 days
    dates = []
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        # Generate multiple entries per day
        for hour in [6, 10, 14, 18, 22]:
            dates.append(date.replace(hour=hour, minute=0, second=0))
    
    # Generate sample data
    data = []
    for i, date in enumerate(dates):
        # Most entries are normal
        if np.random.random() > 0.8:  # 20% chance of anomaly
            severity = np.random.choice(['Critical', 'Warning', 'Info'], p=[0.3, 0.5, 0.2])
            energy_output = np.random.normal(300 if severity == 'Critical' else 450, 50)
            anomaly_score = np.random.uniform(0.6, 0.95)
            recommended_action = {
                'Critical': 'Immediate equipment inspection required',
                'Warning': 'Monitor closely and schedule maintenance check',
                'Info': 'Note for pattern analysis'
            }[severity]
        else:
            severity = 'Normal'
            energy_output = np.random.normal(500, 30)
            anomaly_score = np.random.uniform(0.1, 0.4)
            recommended_action = 'No action required'
        
        data.append({
            'date': date,
            'energyOutput': max(0, energy_output),
            'severity': severity,
            'anomaly_score': anomaly_score,
            'recommended_action': recommended_action
        })
    
    return pd.DataFrame(data)

def main():
    """Main function for testing alert export"""
    logger.info("Starting Alert Export System")
    
    # Create exporter
    exporter = AlertExporter("./Final App")
    
    # Load or create sample data
    try:
        # Try to load existing anomaly data
        anomaly_data = pd.read_csv("./Rayfield_Week 3 Deliverable/predictions.csv")
        logger.info("Loaded existing anomaly data")
    except FileNotFoundError:
        # Create sample data if file doesn't exist
        anomaly_data = create_sample_anomaly_data()
        logger.info("Created sample anomaly data for testing")
    
    # Export today's alerts
    today = datetime.now().strftime('%Y-%m-%d')
    export_path, alert_count, summary = exporter.export_daily_alerts(anomaly_data, today)
    
    logger.info(f"Export completed:")
    logger.info(f"- File: {export_path}")
    logger.info(f"- Alert count: {alert_count}")
    logger.info(f"- Status: {summary['status']}")
    
    print(f"\n✅ Alert export completed successfully!")
    print(f"📁 Export file: {export_path}")
    print(f"🚨 Alerts exported: {alert_count}")
    print(f"📊 Summary: {summary['status']}")
    
    if alert_count > 0:
        print(f"\n📈 Summary Statistics:")
        print(f"- Critical alerts: {summary['critical_alerts']}")
        print(f"- Warning alerts: {summary['warning_alerts']}")
        print(f"- Average energy output: {summary['avg_energy_output']:.1f} kWh")
        print(f"- Maximum deviation: {summary['max_deviation']:.1f}%")

if __name__ == "__main__":
    main() 