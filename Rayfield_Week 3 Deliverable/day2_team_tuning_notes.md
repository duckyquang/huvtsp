
# Team Feature Tuning Notes

## New Features Added:
- `percent_change`: Change in energy output from the previous day
- `day_of_week`: Number from 0 (Monday) to 6 (Sunday)
- `is_weekend`: Boolean flag for weekends

## Model Tuning
We tested different `contamination` values for the Isolation Forest model:

- Values tested: 0.05, 0.1, 0.15
- Best value chosen: **0.1**
- Number of anomalies detected: 3

## Notes
We selected contamination=0.1 to give a balance of anomaly sensitivity and visual interpretability.
