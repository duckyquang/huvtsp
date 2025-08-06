import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { FileUpload } from './FileUpload';
import { AnomalyTable } from './AnomalyTable';
import { ChartView } from './ChartView';
import { ExportSection } from './ExportSection';
import { SummarySection } from './SummarySection';
import { Upload, Database, Brain, FileText } from 'lucide-react';

interface ProcessingStatus {
  step: string;
  status: 'pending' | 'processing' | 'complete' | 'error';
  message: string;
}

export const Dashboard = () => {
  const [file, setFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState<ProcessingStatus[]>([]);
  const [results, setResults] = useState<any>(null);
  const [summary, setSummary] = useState('');

  // Mock data for demonstration
  const mockResults = {
    anomalies: [
      { date: '2024-01-15', energyOutput: 485.2, anomalyFlag: 'Yes', score: 0.85 },
      { date: '2024-01-16', energyOutput: 512.8, anomalyFlag: 'No', score: 0.12 },
      { date: '2024-01-17', energyOutput: 398.1, anomalyFlag: 'Yes', score: 0.92 },
      { date: '2024-01-18', energyOutput: 475.6, anomalyFlag: 'No', score: 0.28 },
      { date: '2024-01-19', energyOutput: 501.3, anomalyFlag: 'No', score: 0.15 },
    ],
    chartData: [
      { date: '2024-01-15', energyOutput: 485.2, isAnomaly: true },
      { date: '2024-01-16', energyOutput: 512.8, isAnomaly: false },
      { date: '2024-01-17', energyOutput: 398.1, isAnomaly: true },
      { date: '2024-01-18', energyOutput: 475.6, isAnomaly: false },
      { date: '2024-01-19', energyOutput: 501.3, isAnomaly: false },
    ]
  };

  const handleRunPipeline = async () => {
    if (!file) return;
    
    setProcessing(true);
    setProcessingStatus([
      { step: 'upload', status: 'processing', message: 'Uploading file...' },
      { step: 'validate', status: 'pending', message: 'Validating data format...' },
      { step: 'analyze', status: 'pending', message: 'Running ML analysis...' },
      { step: 'generate', status: 'pending', message: 'Generating summary...' }
    ]);

    // Simulate processing steps
    const steps = ['upload', 'validate', 'analyze', 'generate'];
    
    for (let i = 0; i < steps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setProcessingStatus(prev => prev.map(status => 
        status.step === steps[i] 
          ? { ...status, status: 'complete', message: `${status.message} Complete!` }
          : status.step === steps[i + 1]
          ? { ...status, status: 'processing' }
          : status
      ));
    }

    // Set mock results
    setResults(mockResults);
    setSummary('Analysis complete. 2 anomalies detected in the energy output data spanning January 15-19, 2024. Peak anomaly occurred on January 17th with significantly lower output (398.1 kWh). System recommends immediate inspection of equipment for potential maintenance needs.');
    setProcessing(false);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-foreground">Rayfield Systems</h1>
              <p className="text-muted-foreground mt-1">Energy Pipeline Dashboard</p>
            </div>
            <Badge variant="secondary" className="text-sm">
              Upload, Analyze, and Review AI Results
            </Badge>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        <div className="grid gap-8">
          {/* Upload Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5" />
                Data Upload
              </CardTitle>
              <CardDescription>
                Upload your CSV energy data file to begin analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FileUpload 
                file={file} 
                onFileSelect={setFile}
                disabled={processing}
              />
              
              <div className="flex items-center gap-4">
                <Button 
                  onClick={handleRunPipeline}
                  disabled={!file || processing}
                  className="flex items-center gap-2"
                >
                  <Brain className="h-4 w-4" />
                  {processing ? 'Running Pipeline...' : 'Run Pipeline'}
                </Button>
                
                {file && (
                  <span className="text-sm text-muted-foreground">
                    File ready: {file.name}
                  </span>
                )}
              </div>

              {/* Processing Status */}
              {processingStatus.length > 0 && (
                <div className="space-y-2 p-4 bg-muted rounded-lg">
                  <h4 className="font-medium text-sm">Processing Status:</h4>
                  {processingStatus.map((status) => (
                    <div key={status.step} className="flex items-center gap-2 text-sm">
                      <div className={`w-2 h-2 rounded-full ${
                        status.status === 'complete' ? 'bg-success' :
                        status.status === 'processing' ? 'bg-warning' :
                        status.status === 'error' ? 'bg-destructive' :
                        'bg-muted-foreground'
                      }`} />
                      <span className={status.status === 'complete' ? 'text-success' : ''}>
                        {status.message}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results Section */}
          {results && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="h-5 w-5" />
                  Analysis Results
                </CardTitle>
                <CardDescription>
                  Machine learning analysis and anomaly detection results
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="table" className="w-full">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="table">Anomaly Report</TabsTrigger>
                    <TabsTrigger value="chart">Chart View</TabsTrigger>
                    <TabsTrigger value="summary">AI Summary</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="table" className="mt-6">
                    <AnomalyTable data={results.anomalies} />
                  </TabsContent>
                  
                  <TabsContent value="chart" className="mt-6">
                    <ChartView data={results.chartData} />
                  </TabsContent>
                  
                  <TabsContent value="summary" className="mt-6">
                    <SummarySection 
                      data={results}
                      isProcessing={processing}
                      onRefreshSummary={() => {
                        setSummary('Refreshing AI summary...');
                        // This would call the actual GPT API in production
                        setTimeout(() => {
                          setSummary('Updated analysis complete. 2 anomalies detected in the energy output data spanning January 15-19, 2024. Peak anomaly occurred on January 17th with significantly lower output (398.1 kWh). System recommends immediate inspection of equipment for potential maintenance needs.');
                        }, 2000);
                      }}
                    />
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          )}

          {/* Export Section */}
          {results && (
            <ExportSection 
              anomalyData={results.anomalies}
              summary={summary}
            />
          )}
        </div>
      </div>
    </div>
  );
};