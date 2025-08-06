# Day 2 Integration Notes - Anomaly Detection & Alerts

## Integration Strategy

### 1. Backend Integration
- **Primary**: Enhance existing `ai_module.py` with `EnhancedAnomalyDetector`
- **Secondary**: Update `main_pipeline.py` to use new anomaly classification
- **API**: Modify endpoints to return severity levels and recommendations

### 2. Frontend Integration
- **Chart Enhancement**: Update `ChartView.tsx` with severity-based markers
- **Alert System**: Integrate `AnomalyAlertsList` component
- **Real-time**: WebSocket connection for live anomaly alerts

### 3. Data Flow Updates

```
CSV Upload → Enhanced Detection → Severity Classification → UI Updates
     ↓              ↓                    ↓                    ↓
File Processing → Multi-Algorithm → Critical/Warning/Info → Visual Markers
     ↓              ↓                    ↓                    ↓
Validation → Isolation Forest + → Recommended Actions → Alert Notifications
             Z-Score + SPC
```

## Technical Implementation Steps

### Step 1: Backend Enhancement
```python
# In ai_module.py - Add enhanced detection
from enhanced_anomaly_detector import EnhancedAnomalyDetector

def analyze_with_enhanced_detection(data):
    detector = EnhancedAnomalyDetector(contamination=0.1)
    detector.fit(data)
    results = detector.detect_anomalies(data)
    return results.to_dict('records')
```

### Step 2: API Updates
```python
# In main_pipeline.py - Update response format
@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    # ... existing code ...
    
    enhanced_results = analyze_with_enhanced_detection(df)
    
    return jsonify({
        'anomalies': enhanced_results,
        'summary': generate_summary(enhanced_results),
        'alerts': filter_critical_alerts(enhanced_results)
    })
```

### Step 3: Frontend Integration
```typescript
// In Dashboard.tsx - Update data processing
interface EnhancedAnomalyData {
  date: string;
  energyOutput: number;
  anomalyFlag: boolean;
  anomalyScore: number;
  severity: 'Critical' | 'Warning' | 'Info' | 'Normal';
  recommendedAction: string;
}

const processApiResponse = (response: any) => {
  return response.anomalies.map(item => ({
    date: item.date,
    energyOutput: item.energyOutput,
    isAnomaly: item.anomaly_flag,
    anomalyScore: item.anomaly_score,
    severity: item.severity
  }));
};
```

### Step 4: Chart Component Updates
```typescript
// In ChartView.tsx - Add severity-based rendering
const getAnomalyColor = (severity: string) => {
  switch (severity) {
    case 'Critical': return '#dc2626';
    case 'Warning': return '#ea580c'; 
    case 'Info': return '#ca8a04';
    default: return '#6b7280';
  }
};

// Update ReferenceDot rendering
{data.map((point, index) => 
  point.isAnomaly ? (
    <ReferenceDot
      key={index}
      x={point.date}
      y={point.energyOutput}
      r={point.severity === 'Critical' ? 8 : 6}
      fill={getAnomalyColor(point.severity)}
      stroke="#ffffff"
      strokeWidth={2}
    />
  ) : null
)}
```

## Testing Checklist

### Backend Testing
- [ ] Unit tests for EnhancedAnomalyDetector
- [ ] Integration tests with existing pipeline
- [ ] Performance benchmarks for large datasets
- [ ] Validation against known anomaly datasets

### Frontend Testing
- [ ] Chart rendering with severity markers
- [ ] Alert list functionality
- [ ] Tooltip information accuracy
- [ ] Responsive design across devices

### End-to-End Testing
- [ ] Full pipeline: Upload → Process → Display
- [ ] Real-time alert notifications
- [ ] Export functionality with enhanced data
- [ ] Error handling and edge cases

## Performance Considerations

### Backend Optimization
- **Caching**: Cache trained models for repeated analysis
- **Batch Processing**: Process multiple files efficiently
- **Memory Management**: Handle large datasets without memory issues

### Frontend Optimization
- **Chart Performance**: Optimize rendering for 1000+ data points
- **State Management**: Efficient updates for real-time data
- **Memory Leaks**: Proper cleanup of chart components

## Security & Reliability

### Data Validation
- Input sanitization for anomaly thresholds
- Validation of anomaly score ranges (0-1)
- Error handling for malformed data

### System Reliability
- Fallback to basic anomaly detection if enhanced fails
- Graceful degradation for unsupported data formats
- Logging and monitoring for anomaly detection pipeline

## Deployment Notes

### Environment Variables
```
ANOMALY_CONTAMINATION_RATE=0.1
CRITICAL_THRESHOLD=0.8
WARNING_THRESHOLD=0.5
INFO_THRESHOLD=0.3
```

### Dependencies
```
# Backend requirements
scikit-learn>=1.0.0
scipy>=1.7.0
pandas>=1.3.0

# Frontend dependencies
recharts>=2.5.0
lucide-react>=0.263.0
```

### Database Schema Updates (if applicable)
```sql
ALTER TABLE anomaly_results ADD COLUMN severity VARCHAR(20);
ALTER TABLE anomaly_results ADD COLUMN anomaly_score DECIMAL(5,3);
ALTER TABLE anomaly_results ADD COLUMN recommended_action TEXT;
```

## Next Steps for Day 3

1. **API Integration**: Connect frontend to enhanced backend
2. **Real-time Updates**: Implement WebSocket for live alerts
3. **User Configuration**: Allow users to adjust thresholds
4. **Export Enhancement**: Include severity data in exports
5. **Dashboard Integration**: Combine all components seamlessly 