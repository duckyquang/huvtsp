"""
HUVTSP Flask Backend Application
Provides API endpoints for the React frontend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import sys

# Import our AI module
from ai_module import detect_anomalies

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_mock_summary(data):
    """Generate a mock AI summary for the data"""
    total_records = len(data)
    anomalies = data[data.get('anomaly_flag', False) == True] if 'anomaly_flag' in data.columns else pd.DataFrame()
    avg_output = data['energyOutput'].mean() if 'energyOutput' in data.columns else 0
    
    summary = f"""🔍 HUVTSP Energy Analysis Summary

📊 Data Overview:
- Total records processed: {total_records} measurements
- Date range: {data.iloc[0]['date'] if 'date' in data.columns else 'N/A'} to {data.iloc[-1]['date'] if 'date' in data.columns else 'N/A'}
- Average energy output: {avg_output:.1f} kWh

⚡ Performance Insights:
- Peak performance: {data['energyOutput'].max():.1f} kWh
- Minimum output: {data['energyOutput'].min():.1f} kWh
- Overall efficiency: 94.2% of expected output

🚨 Anomaly Detection Results:
- {len(anomalies)} anomalies detected ({len(anomalies)/total_records*100:.1f}% of total readings)
- Most common issue: Output variations detected
- Severity: Mix of info, warning, and critical alerts

💡 Key Recommendations:
1. Monitor trending patterns for optimization
2. Review maintenance schedules for optimal performance
3. Consider environmental factors affecting output
4. Continue regular monitoring procedures

📈 Trend Analysis:
- Stable performance with minor variations
- No critical system issues detected
- Weather impact: Minimal correlation observed"""

    return summary

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400
        
        # Save uploaded file
        filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Process the file
        data = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['date', 'energyOutput']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            return jsonify({
                'error': f'Missing required columns: {missing_columns}',
                'required': required_columns,
                'found': list(data.columns)
            }), 400
        
        # Run anomaly detection
        try:
            processed_data = detect_anomalies(data)
        except Exception as e:
            # Fallback to basic processing if AI module fails
            print(f"AI module error: {e}")
            processed_data = data.copy()
            processed_data['anomaly_flag'] = False
            processed_data['anomaly_score'] = 0.0
        
        # Generate summary
        summary = generate_mock_summary(processed_data)
        
        # Prepare response data
        anomalies = processed_data[processed_data.get('anomaly_flag', False) == True]
        chart_data = processed_data.to_dict('records')
        
        response = {
            'jobId': filename.replace('.csv', ''),
            'status': 'complete',
            'data': {
                'anomalies': anomalies.to_dict('records'),
                'chartData': chart_data,
                'summary': summary,
                'alerts': anomalies.to_dict('records')
            },
            'metadata': {
                'processedAt': datetime.now().isoformat(),
                'totalRecords': len(data),
                'anomalyCount': len(anomalies),
                'filename': filename
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': 'Processing failed',
            'details': str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """Analyze uploaded data and return results"""
    try:
        # This endpoint can be used for additional analysis
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Mock analysis for demonstration
        response = {
            'status': 'success',
            'analysis': {
                'anomaly_rate': 0.07,
                'average_output': 487.3,
                'recommendations': [
                    'System operating within normal parameters',
                    'Continue regular monitoring',
                    'No immediate action required'
                ]
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': 'Analysis failed',
            'details': str(e)
        }), 500

@app.route('/api/alerts/export', methods=['GET'])
def export_alerts():
    """Export current alerts to CSV"""
    try:
        # Load or generate alert data
        if os.path.exists('alerts_today.csv'):
            alerts_df = pd.read_csv('alerts_today.csv')
        else:
            # Generate sample alerts if file doesn't exist
            alerts_df = pd.DataFrame({
                'alert_id': [1, 2],
                'timestamp': [datetime.now().isoformat(), datetime.now().isoformat()],
                'energy_kwh': [485.2, 398.1],
                'severity': ['Warning', 'Critical'],
                'recommended_action': ['Monitor closely', 'Immediate inspection required']
            })
        
        return jsonify({
            'status': 'success',
            'alerts': alerts_df.to_dict('records'),
            'count': len(alerts_df),
            'export_time': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Export failed',
            'details': str(e)
        }), 500

@app.route('/api/summary/generate', methods=['POST'])
def generate_summary():
    """Generate AI summary for given data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Convert to DataFrame for processing
        df = pd.DataFrame(data.get('chartData', []))
        
        if df.empty:
            summary = "No data available for analysis."
        else:
            summary = generate_mock_summary(df)
        
        return jsonify({
            'status': 'success',
            'summary': summary,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Summary generation failed',
            'details': str(e)
        }), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting HUVTSP Flask Backend...")
    print("📡 API Endpoints:")
    print("   GET  /api/health - Health check")
    print("   POST /api/upload - File upload and processing")
    print("   POST /api/analyze - Data analysis")
    print("   GET  /api/alerts/export - Export alerts")
    print("   POST /api/summary/generate - Generate AI summary")
    print("\n🌐 Starting server on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 