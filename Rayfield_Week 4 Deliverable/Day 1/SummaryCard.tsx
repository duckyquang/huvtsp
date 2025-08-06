import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { Skeleton } from '@/components/ui/skeleton';
import { RefreshCw, FileText, ChevronDown, ChevronUp, AlertCircle } from 'lucide-react';

interface SummaryCardProps {
  data?: any;
  isProcessing?: boolean;
  onRefreshSummary?: () => void;
}

export const SummaryCard = ({ data, isProcessing = false, onRefreshSummary }: SummaryCardProps) => {
  const [summary, setSummary] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  // Mock weekly summary from existing weekly_summary.txt
  const mockWeeklySummary = `
🔍 Weekly Energy Analysis Summary

📊 Data Overview:
- Total records processed: 168 hourly measurements
- Date range: January 15-21, 2024
- Average energy output: 487.3 kWh

⚡ Performance Insights:
- Peak performance: 612.8 kWh (Jan 18, 14:00)
- Minimum output: 298.1 kWh (Jan 17, 06:00)
- Overall efficiency: 94.2% of expected output

🚨 Anomaly Detection Results:
- 12 anomalies detected (7.1% of total readings)
- Most common issue: Output drops during morning hours
- Severity: 3 critical, 9 moderate alerts

💡 Key Recommendations:
1. Investigate morning performance drops
2. Monitor weather correlation patterns
3. Schedule maintenance for underperforming units
4. Consider backup power optimization

📈 Trend Analysis:
- 2.3% improvement over previous week
- Consistent afternoon peak performance
- Weather impact: 15% correlation with cloud cover
  `;

  useEffect(() => {
    if (data) {
      // Simulate API call to generate summary
      generateSummary();
    } else {
      setSummary(mockWeeklySummary);
    }
  }, [data]);

  const generateSummary = async () => {
    setIsGenerating(true);
    try {
      // Simulate GPT API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const dynamicSummary = `
🔍 Real-time Energy Analysis Summary

📊 Current Data Analysis:
- Records processed: ${data?.chartData?.length || 0} measurements
- Anomalies detected: ${data?.anomalies?.filter((a: any) => a.anomalyFlag === 'Yes').length || 0}
- Average output: ${data?.chartData?.reduce((acc: number, item: any) => acc + item.energyOutput, 0) / (data?.chartData?.length || 1) || 0} kWh

⚡ Performance Status:
${data?.anomalies?.filter((a: any) => a.anomalyFlag === 'Yes').length > 2 
  ? '🔴 Multiple anomalies detected - requires attention'
  : '🟢 System operating within normal parameters'}

🚨 Critical Alerts:
${data?.anomalies?.filter((a: any) => a.anomalyFlag === 'Yes' && a.score > 0.8)
  .map((a: any) => `- ${a.date}: ${a.energyOutput} kWh (Score: ${a.score})`)
  .join('\n') || 'No critical alerts'}

💡 AI Recommendations:
- Monitor trending patterns in energy output
- Review maintenance schedules for optimal performance
- Consider environmental factors affecting output
      `;
      
      setSummary(dynamicSummary);
    } catch (error) {
      setSummary('Error generating summary. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleRefresh = () => {
    if (onRefreshSummary) {
      onRefreshSummary();
    } else {
      generateSummary();
    }
  };

  if (isProcessing) {
    return (
      <Card className="w-full">
        <CardHeader>
          <div className="flex items-center space-x-2">
            <Skeleton className="h-4 w-4" />
            <Skeleton className="h-6 w-32" />
          </div>
          <Skeleton className="h-4 w-64" />
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        </CardContent>
      </Card>
    );
  }

  const truncatedSummary = summary.split('\n').slice(0, 8).join('\n');
  const shouldShowExpand = summary.split('\n').length > 8;

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <FileText className="h-5 w-5 text-blue-600" />
            <CardTitle>AI-Generated Summary</CardTitle>
            {isGenerating && (
              <Badge variant="secondary" className="animate-pulse">
                Generating...
              </Badge>
            )}
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={isGenerating}
            className="h-8"
          >
            <RefreshCw className={`h-4 w-4 ${isGenerating ? 'animate-spin' : ''}`} />
          </Button>
        </div>
        <CardDescription>
          Intelligent analysis of energy output patterns and anomalies
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Textarea
            value={isExpanded ? summary : truncatedSummary}
            readOnly
            className="min-h-[200px] font-mono text-sm resize-none"
          />
          
          {shouldShowExpand && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsExpanded(!isExpanded)}
              className="w-full"
            >
              {isExpanded ? (
                <>
                  <ChevronUp className="h-4 w-4 mr-2" />
                  Show Less
                </>
              ) : (
                <>
                  <ChevronDown className="h-4 w-4 mr-2" />
                  Show More
                </>
              )}
            </Button>
          )}

          {data?.anomalies?.filter((a: any) => a.anomalyFlag === 'Yes').length > 0 && (
            <div className="flex items-center space-x-2 p-3 bg-amber-50 border border-amber-200 rounded-lg">
              <AlertCircle className="h-4 w-4 text-amber-600" />
              <span className="text-sm text-amber-800">
                {data.anomalies.filter((a: any) => a.anomalyFlag === 'Yes').length} anomalies detected in current dataset
              </span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}; 