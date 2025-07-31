
# Energy Anomaly Detection with Isolation Forest

## Overview
This ML module detects anomalies in daily energy output using the Isolation Forest algorithm. It helps analysts identify unusual drops or spikes in production that may require manual investigation.

## Workflow Summary
1. Load daily energy data (simulated in this version)
2. Clean and engineer features (7-day rolling average)
3. Train Isolation Forest model on energy output
4. Predict anomalies and visualize them
5. Generate a human-readable summary
6. Save results to CSV, TXT, and PNG

## Model
- **Type**: Isolation Forest
- **Library**: scikit-learn
- **Features Used**:
  - output_kwh
  - 7-day rolling average (engineered)
- **Output**:
  - Anomaly flag for each record
  - Anomaly score used internally

## Output Files
- `predictions.csv`: Raw predictions with anomaly flags
- `weekly_summary.txt`: Natural language summary of anomalies
- `anomaly_plot.png`: Visualization of detected anomalies
- `ai_module.py`: Reusable model functions
- `main_pipeline.py`: End-to-end pipeline script
- `ai_model_dev.ipynb`: Interactive notebook with full logic

## Known Limitations
- Data is simulated, not real energy production
- Model is not tuned with GridSearch
- Summary is mock (non-GPT version)

## Next Steps
- Replace with real cleaned dataset
- Add time-of-day or weather-based features
- Integrate GPT summary API for enhanced reporting
