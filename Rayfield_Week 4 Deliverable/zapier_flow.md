# Zapier Integration Flow for HUVTSP Anomaly Alerts

## Overview
This document outlines the complete Zapier integration workflow for automated anomaly alert notifications in the HUVTSP energy monitoring system.

## 🔄 Zapier Workflow Design

### **Trigger: Google Drive File Update**
- **App**: Google Drive
- **Trigger Event**: "New File in Folder" or "Updated File in Folder"
- **Folder**: `/HUVTSP/Daily_Exports/`
- **File Pattern**: `alerts_*.csv`
- **Frequency**: Real-time (webhook-based)

### **Filter: Check for Anomalies**
- **Condition**: File size > 0 bytes (contains data)
- **Pattern Matching**: Filename contains today's date
- **Data Validation**: CSV contains anomaly records

### **Parser: Extract Alert Data**
- **Action**: Read CSV content
- **Fields Extracted**:
  - Date/Time of anomaly
  - Energy output value (kWh)
  - Anomaly severity level
  - Recommended action
  - Location/unit identifier

### **Action 1: Send Email Alert**
- **App**: Gmail/Outlook
- **Trigger Condition**: Severity = "Critical" OR count > 3 anomalies
- **Recipients**: 
  - Operations Team: `ops@rayfieldysystems.com`
  - Management: `alerts@rayfieldsystems.com`
  - On-call Engineer: `oncall@rayfieldsystems.com`

### **Action 2: Send Slack Notification**
- **App**: Slack
- **Channel**: `#energy-alerts`
- **Trigger Condition**: All anomalies (immediate notification)
- **Message Format**: Structured with severity indicators

### **Action 3: Update Google Sheets Dashboard**
- **App**: Google Sheets
- **Sheet**: "HUVTSP Alert Dashboard"
- **Action**: Add new row with alert details
- **Trigger Condition**: All anomalies (logging)

## 📧 Sample Alert Messages

### Email Alert Template

**Subject**: `🚨 HUVTSP Energy Anomaly Alert - {{severity}} - {{date}}`

**Body**:
```
HUVTSP Energy Monitoring System Alert

⚠️ ANOMALY DETECTED
------------------
Date & Time: {{timestamp}}
Energy Output: {{energy_kwh}} kWh
Severity Level: {{severity}}
Expected Range: {{expected_min}} - {{expected_max}} kWh
Deviation: {{deviation_percentage}}%

📊 IMPACT ASSESSMENT
-------------------
System Status: {{system_status}}
Units Affected: {{affected_units}}
Estimated Duration: {{estimated_duration}}

🔧 RECOMMENDED ACTIONS
---------------------
{{recommended_action}}

📈 ADDITIONAL DATA
-----------------
- Recent Trend: {{trend_analysis}}
- Weather Conditions: {{weather_impact}}
- Previous Similar Events: {{historical_context}}

🔗 DASHBOARD LINK
----------------
View full details: https://huvtsp-dashboard.rayfieldsystems.com/alerts/{{alert_id}}

This is an automated alert from the HUVTSP monitoring system.
For immediate assistance, contact the on-call engineer at +1-XXX-XXX-XXXX.

---
Rayfield Systems Energy Monitoring
Generated: {{generation_timestamp}}
```

### Slack Alert Template

```
🚨 **ENERGY ANOMALY DETECTED** 🚨

**{{severity_emoji}} Severity**: {{severity}}
**📅 Date**: {{date}} {{time}}
**⚡ Output**: {{energy_kwh}} kWh (Expected: {{expected_range}})
**📊 Deviation**: {{deviation_percentage}}%

**🔧 Action Required**: {{recommended_action}}

**📈 Quick Stats**:
• System Status: {{system_status}}
• Trend: {{trend_direction}}
• Units: {{affected_units}}

<https://huvtsp-dashboard.rayfieldsystems.com/alerts/{{alert_id}}|View Dashboard> | <https://docs.rayfieldsystems.com/troubleshooting|Troubleshooting Guide>

cc: @ops-team @energy-engineers
```

### SMS Alert Template (Critical Only)

```
🚨 HUVTSP CRITICAL ALERT
{{date}} {{time}}
Energy: {{energy_kwh}} kWh
Expected: {{expected_range}}
Action: {{short_action}}
Dashboard: {{short_url}}
```

## ⚙️ Zapier Configuration Steps

### Step 1: Set Up Google Drive Trigger
1. **Create Zap**: "New File in Folder"
2. **Connect Account**: Google Drive with appropriate permissions
3. **Configure Folder**: Select `/HUVTSP/Daily_Exports/`
4. **File Filter**: `*.csv` files only
5. **Test**: Upload sample CSV to verify trigger

### Step 2: Add Filter Logic
1. **Add Filter Step**: "Only continue if..."
2. **Condition 1**: File size > 0 bytes
3. **Condition 2**: Filename contains current date pattern
4. **Condition 3**: File extension equals "csv"

### Step 3: Parse CSV Data
1. **Add Code Step**: Python or JavaScript
2. **Function**: Parse CSV and extract anomaly records
3. **Output**: Structured data for subsequent actions
4. **Error Handling**: Validate data format and content

### Step 4: Configure Email Action
1. **Add Gmail Action**: "Send Email"
2. **Dynamic Recipients**: Based on severity level
3. **Template Variables**: Map CSV fields to email template
4. **Formatting**: HTML email with proper styling

### Step 5: Configure Slack Action
1. **Add Slack Action**: "Send Channel Message"
2. **Channel Selection**: #energy-alerts
3. **Message Format**: Markdown with emojis and mentions
4. **Conditional Logic**: Different formats for different severities

### Step 6: Configure Google Sheets Logging
1. **Add Google Sheets Action**: "Create Spreadsheet Row"
2. **Sheet Selection**: HUVTSP Alert Dashboard
3. **Field Mapping**: All CSV columns to sheet columns
4. **Timestamp**: Add current timestamp for logging

## 🧪 Testing Procedures

### Unit Testing
- Upload test CSV with known anomalies
- Verify trigger activation
- Check data parsing accuracy
- Validate filter conditions

### Integration Testing
- Test complete workflow end-to-end
- Verify all notification channels
- Check message formatting
- Validate recipient targeting

### Performance Testing
- Test with large CSV files
- Verify processing speed
- Check error handling
- Monitor resource usage

## 📊 Monitoring & Analytics

### Zapier Dashboard Metrics
- **Success Rate**: Percentage of successful executions
- **Processing Time**: Average workflow completion time
- **Error Rate**: Failed executions and error types
- **Volume**: Number of alerts processed daily/weekly

### Alert Effectiveness Metrics
- **Response Time**: Time from detection to notification
- **Delivery Rate**: Successful notification delivery percentage
- **Engagement**: Email opens, Slack reactions, dashboard views
- **Resolution Time**: Time from alert to issue resolution

## 🔧 Maintenance & Updates

### Regular Maintenance
- **Weekly**: Review error logs and failed executions
- **Monthly**: Update recipient lists and notification preferences
- **Quarterly**: Review and optimize workflow performance
- **Annually**: Audit security and permissions

### Version Control
- **Template Updates**: Version control for email/Slack templates
- **Workflow Changes**: Document all Zapier workflow modifications
- **Testing**: Regression testing after any changes
- **Rollback**: Procedures for reverting problematic updates

## 💰 Cost Optimization

### Zapier Pricing Considerations
- **Task Usage**: Monitor monthly task consumption
- **Premium Features**: Evaluate need for advanced actions
- **Multi-Step Zaps**: Optimize workflow efficiency
- **Alternative Solutions**: Consider direct API integrations for high volume

### Efficiency Improvements
- **Batch Processing**: Group similar alerts where possible
- **Smart Filtering**: Reduce unnecessary executions
- **Conditional Logic**: Optimize notification frequency
- **Data Compression**: Minimize file sizes and processing time

## 🔐 Security & Compliance

### Data Protection
- **Access Controls**: Limit folder and sheet permissions
- **Encryption**: Ensure data encryption in transit
- **Audit Logging**: Track all workflow executions
- **Compliance**: Meet industry data protection standards

### Error Handling
- **Graceful Failures**: Handle API failures gracefully
- **Retry Logic**: Implement appropriate retry mechanisms
- **Fallback Notifications**: Backup notification methods
- **Alert Escalation**: Escalate critical failures to administrators

---

**Implementation Timeline**: 2-3 days
**Testing Period**: 1 week
**Go-Live**: After successful testing and approval
**Review Date**: 30 days after implementation 