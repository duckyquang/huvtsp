# Rayfield Systems Technical Training Guide – Team Version (Week 1–4)

This document includes complete, specific steps, filenames, data structure, and task logic for executing the team deliverables from Week 1 to Week 4 of the Rayfield Systems internship.

## 📁 Folder Conventions
- `Week 1/` to `Week 4/`: Holds daily task outputs
- `Final App/`: Holds full pipeline integration, app code, and final deliverables

---

## 🧭 Week 1 – Research & UI Design

### **Day 1 – Research**
- Output: `Week 1/research_notes.md`
- Tasks:
  - Read onboarding doc and Rayfield website.
  - Research tools and roles in energy firms.
  - Document pain points and technologies.

### **Day 2 – Personas & Problems**
- Output: `Week 1/personas.md`
- Format:
```markdown
### Persona: Sarah, Grid Analyst
- Goals: Ensure daily kWh output meets target
- Pain Points: No alerts, manual Excel sheets
- Opportunity: Auto-anomaly detection + dashboard
```

### **Day 3 – User Flow**
- Output: `Week 1/user_flow.png` + `Week 1/flow_notes.md`

### **Day 4 – Hi-Fidelity Design**
- Output: `figma_link.txt` or UI screenshots

---

## 🧪 Week 2 – Feature Engineering & Pipeline

### **Day 1 – Dataset Cleaning**
- Input: `raw_data.csv`
- Output: `Week 2/cleaned_dataset.csv`

### **Day 2 – Feature Engineering**
- Output: `Week 2/features.csv`, `feature_notes.md`

### **Day 3 – Pipeline Diagram**
- Output: `pipeline_v1.png` (ML workflow diagram)

### **Day 4 – GPT Summary Function**
- Output: `gpt_summary.py`, `weekly_summary.txt`
- Function:
```python
def generate_summary(df):
    return f"Summary based on {len(df)} rows"
```

### **Day 5 – Final Pipeline Output**
- Output: `pipeline_with_ml.png`, `README.md`

---

## 🧠 Week 3 – Model Training

### **Day 1 – Baseline Model**
- Output: `ai_model_dev.ipynb`

### **Day 2 – Model Tuning**
- Output: `tuned_predictions.csv`

### **Day 3 – Anomaly Visualization**
- Output: `anomaly_plot.png`

### **Day 4 – GPT Summary Reuse**
- Output: integrated in notebook or `main_pipeline.py`

### **Day 5 – Full Pipeline Integration**
- Output: `ai_module.py`, `main_pipeline.py`

---

## 🖥 Week 4 – App Integration & Alert Logic

### **Day 1 – UI with Summary**
- Output: `Final App/app.py`
- Components:
  - Upload box, Chart, Summary, Alert section

### **Day 2 – Anomaly Chart + Table**
- Output: `alerts_today.csv`, UI update

### **Day 3 – Full UI Flow**
- Output: updated `app.py` handling full logic

### **Day 4 – Zapier Flow Documentation**
- Output: `zapier_flow.md`

### **Day 5 – Testing & Weekly Summary**
- Output: `week4_notes.md`

---

## ✅ Final Checklist

| Criteria              | File(s)                       |
|----------------------|-------------------------------|
| Cleaned Data         | `cleaned_dataset.csv`         |
| Engineered Features  | `features.csv`                |
| ML Diagrams          | `pipeline_v1.png`             |
| Summary Function     | `gpt_summary.py`              |
| Final Pipeline       | `main_pipeline.py`            |
| AI Module Logic      | `ai_module.py`                |
| UI Dashboard         | `Final App/app.py`            |
| Alerts File          | `alerts_today.csv`            |
| Zapier Flow          | `zapier_flow.md`              |
| Completion Notes     | `week4_notes.md`              |