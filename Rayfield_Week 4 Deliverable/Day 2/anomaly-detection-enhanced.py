"""
Enhanced Anomaly Detection for HUVTSP Energy Data
Integrates with existing ai_module.py and adds advanced features
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class EnhancedAnomalyDetector:
    def __init__(self, contamination=0.1, random_state=42):
        """
        Enhanced anomaly detection with multiple algorithms
        
        Args:
            contamination (float): Expected proportion of anomalies
            random_state (int): Random seed for reproducibility
        """
        self.contamination = contamination
        self.random_state = random_state
        self.isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.fitted = False
        self.thresholds = {
            'critical': 0.8,
            'warning': 0.5,
            'info': 0.3
        }
        
    def fit(self, data):
        """
        Fit the anomaly detection models
        
        Args:
            data (pd.DataFrame): Training data with energy output values
        """
        # Prepare features for anomaly detection
        features = self._extract_features(data)
        scaled_features = self.scaler.fit_transform(features)
        
        # Fit Isolation Forest
        self.isolation_forest.fit(scaled_features)
        self.fitted = True
        
        return self
    
    def detect_anomalies(self, data):
        """
        Detect anomalies using ensemble of methods
        
        Args:
            data (pd.DataFrame): Data to analyze for anomalies
            
        Returns:
            pd.DataFrame: Original data with anomaly flags and scores
        """
        if not self.fitted:
            raise ValueError("Model must be fitted before detecting anomalies")
            
        # Extract features
        features = self._extract_features(data)
        scaled_features = self.scaler.transform(features)
        
        # Isolation Forest anomaly detection
        isolation_scores = self.isolation_forest.decision_function(scaled_features)
        isolation_anomalies = self.isolation_forest.predict(scaled_features)
        
        # Z-score based anomaly detection
        z_scores = np.abs(stats.zscore(data['energyOutput']))
        z_anomalies = z_scores > 2.5
        
        # Statistical process control
        spc_scores = self._spc_analysis(data['energyOutput'])
        
        # Combine anomaly scores
        combined_scores = self._combine_scores(isolation_scores, z_scores, spc_scores)
        
        # Create result dataframe
        result = data.copy()
        result['anomaly_score'] = combined_scores
        result['isolation_score'] = isolation_scores
        result['z_score'] = z_scores
        result['spc_score'] = spc_scores
        result['anomaly_flag'] = combined_scores > self.thresholds['info']
        result['severity'] = self._classify_severity(combined_scores)
        result['recommended_action'] = self._get_recommendations(result)
        
        return result
    
    def _extract_features(self, data):
        """
        Extract features for anomaly detection
        
        Args:
            data (pd.DataFrame): Input data
            
        Returns:
            np.ndarray: Feature matrix
        """
        features = []
        
        # Basic energy output
        features.append(data['energyOutput'].values)
        
        # Rolling statistics (if enough data points)
        if len(data) >= 7:
            rolling_mean = data['energyOutput'].rolling(window=3, min_periods=1).mean()
            rolling_std = data['energyOutput'].rolling(window=3, min_periods=1).std().fillna(0)
            features.extend([rolling_mean.values, rolling_std.values])
        
        # Time-based features (if datetime column exists)
        if 'date' in data.columns:
            try:
                dates = pd.to_datetime(data['date'])
                hour_of_day = dates.dt.hour
                day_of_week = dates.dt.dayofweek
                features.extend([hour_of_day.values, day_of_week.values])
            except:
                pass
        
        # Rate of change
        if len(data) > 1:
            rate_of_change = data['energyOutput'].diff().fillna(0)
            features.append(rate_of_change.values)
        
        return np.column_stack(features)
    
    def _spc_analysis(self, values):
        """
        Statistical Process Control analysis
        
        Args:
            values (pd.Series): Energy output values
            
        Returns:
            np.ndarray: SPC-based anomaly scores
        """
        mean_val = values.mean()
        std_val = values.std()
        
        # Calculate control limits (3-sigma)
        ucl = mean_val + 3 * std_val
        lcl = mean_val - 3 * std_val
        
        # Calculate deviation from control limits
        upper_deviation = np.maximum(0, values - ucl) / std_val
        lower_deviation = np.maximum(0, lcl - values) / std_val
        
        return upper_deviation + lower_deviation
    
    def _combine_scores(self, isolation_scores, z_scores, spc_scores):
        """
        Combine different anomaly scores into a unified score
        
        Args:
            isolation_scores (np.ndarray): Isolation forest scores
            z_scores (np.ndarray): Z-score based scores
            spc_scores (np.ndarray): SPC-based scores
            
        Returns:
            np.ndarray: Combined anomaly scores (0-1 scale)
        """
        # Normalize isolation forest scores to 0-1
        iso_normalized = (isolation_scores - isolation_scores.min()) / (isolation_scores.max() - isolation_scores.min() + 1e-8)
        iso_normalized = 1 - iso_normalized  # Invert so higher = more anomalous
        
        # Normalize z-scores to 0-1
        z_normalized = np.clip(z_scores / 4.0, 0, 1)  # 4-sigma max
        
        # Normalize SPC scores to 0-1
        spc_normalized = np.clip(spc_scores / 3.0, 0, 1)  # 3-sigma max
        
        # Weighted combination
        weights = [0.5, 0.3, 0.2]  # Isolation Forest, Z-score, SPC
        combined = (weights[0] * iso_normalized + 
                   weights[1] * z_normalized + 
                   weights[2] * spc_normalized)
        
        return combined
    
    def _classify_severity(self, scores):
        """
        Classify anomaly severity based on scores
        
        Args:
            scores (np.ndarray): Anomaly scores
            
        Returns:
            list: Severity classifications
        """
        severity = []
        for score in scores:
            if score >= self.thresholds['critical']:
                severity.append('Critical')
            elif score >= self.thresholds['warning']:
                severity.append('Warning')
            elif score >= self.thresholds['info']:
                severity.append('Info')
            else:
                severity.append('Normal')
        return severity
    
    def _get_recommendations(self, data):
        """
        Generate recommendations based on anomaly analysis
        
        Args:
            data (pd.DataFrame): Data with anomaly information
            
        Returns:
            list: Recommended actions
        """
        recommendations = []
        
        for _, row in data.iterrows():
            if row['severity'] == 'Critical':
                if row['energyOutput'] < data['energyOutput'].mean() * 0.5:
                    recommendations.append('Immediate equipment inspection required')
                else:
                    recommendations.append('Check for external factors affecting output')
            elif row['severity'] == 'Warning':
                recommendations.append('Monitor closely and schedule maintenance check')
            elif row['severity'] == 'Info':
                recommendations.append('Note for pattern analysis')
            else:
                recommendations.append('No action required')
                
        return recommendations
    
    def get_anomaly_summary(self, results):
        """
        Generate summary statistics for anomaly detection results
        
        Args:
            results (pd.DataFrame): Results from detect_anomalies()
            
        Returns:
            dict: Summary statistics
        """
        total_points = len(results)
        anomalies = results[results['anomaly_flag']]
        
        summary = {
            'total_data_points': total_points,
            'total_anomalies': len(anomalies),
            'anomaly_rate': len(anomalies) / total_points * 100,
            'critical_anomalies': len(anomalies[anomalies['severity'] == 'Critical']),
            'warning_anomalies': len(anomalies[anomalies['severity'] == 'Warning']),
            'info_anomalies': len(anomalies[anomalies['severity'] == 'Info']),
            'avg_anomaly_score': anomalies['anomaly_score'].mean() if len(anomalies) > 0 else 0,
            'max_anomaly_score': anomalies['anomaly_score'].max() if len(anomalies) > 0 else 0,
            'most_severe_date': anomalies.loc[anomalies['anomaly_score'].idxmax(), 'date'] if len(anomalies) > 0 else None
        }
        
        return summary

def process_energy_data(file_path_or_data, contamination=0.1):
    """
    Process energy data for anomaly detection
    
    Args:
        file_path_or_data: Path to CSV file or pandas DataFrame
        contamination (float): Expected anomaly rate
        
    Returns:
        tuple: (processed_data, summary_stats)
    """
    # Load data
    if isinstance(file_path_or_data, str):
        data = pd.read_csv(file_path_or_data)
    else:
        data = file_path_or_data.copy()
    
    # Initialize detector
    detector = EnhancedAnomalyDetector(contamination=contamination)
    
    # Fit and detect
    detector.fit(data)
    results = detector.detect_anomalies(data)
    
    # Generate summary
    summary = detector.get_anomaly_summary(results)
    
    return results, summary

# Example usage and testing
if __name__ == "__main__":
    # Create sample data for testing
    np.random.seed(42)
    dates = pd.date_range('2024-01-15', periods=50, freq='H')
    
    # Generate synthetic energy data with anomalies
    base_output = 500 + 50 * np.sin(np.arange(50) * 0.3) + np.random.normal(0, 20, 50)
    
    # Inject anomalies
    anomaly_indices = [10, 25, 40]
    base_output[anomaly_indices] = [200, 800, 150]  # Obvious anomalies
    
    test_data = pd.DataFrame({
        'date': dates,
        'energyOutput': base_output
    })
    
    # Run anomaly detection
    results, summary = process_energy_data(test_data, contamination=0.1)
    
    print("Anomaly Detection Results:")
    print(f"Total anomalies detected: {summary['total_anomalies']}")
    print(f"Anomaly rate: {summary['anomaly_rate']:.2f}%")
    print(f"Critical anomalies: {summary['critical_anomalies']}")
    
    print("\nDetected Anomalies:")
    anomalies = results[results['anomaly_flag']]
    for _, row in anomalies.iterrows():
        print(f"Date: {row['date']}, Output: {row['energyOutput']:.1f} kWh, "
              f"Score: {row['anomaly_score']:.3f}, Severity: {row['severity']}") 