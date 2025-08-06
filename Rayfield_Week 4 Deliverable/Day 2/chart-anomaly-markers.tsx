import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceDot, Legend } from 'recharts';
import { AlertTriangle, AlertCircle, Info } from 'lucide-react';

interface EnhancedChartData {
  date: string;
  energyOutput: number;
  isAnomaly: boolean;
  anomalyScore?: number;
  severity?: 'Critical' | 'Warning' | 'Info' | 'Normal';
}

interface EnhancedChartViewProps {
  data: EnhancedChartData[];
  showAnomalyScores?: boolean;
  highlightThreshold?: number;
}

export const EnhancedChartView = ({ 
  data, 
  showAnomalyScores = true, 
  highlightThreshold = 0.5 
}: EnhancedChartViewProps) => {
  
  // Custom tooltip with anomaly information
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-gray-300 rounded-lg shadow-lg p-3 text-sm">
          <p className="font-medium">{`Date: ${label}`}</p>
          <p className="text-blue-600">{`Output: ${data.energyOutput.toFixed(1)} kWh`}</p>
          {data.isAnomaly && (
            <>
              <p className={`font-medium ${getSeverityColor(data.severity)}`}>
                {`Anomaly: ${data.severity}`}
              </p>
              {data.anomalyScore && (
                <p className="text-gray-600">{`Score: ${data.anomalyScore.toFixed(3)}`}</p>
              )}
            </>
          )}
        </div>
      );
    }
    return null;
  };

  // Get color based on severity
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'Critical': return 'text-red-600';
      case 'Warning': return 'text-orange-600';
      case 'Info': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  const getSeverityFill = (severity: string) => {
    switch (severity) {
      case 'Critical': return '#dc2626';
      case 'Warning': return '#ea580c';
      case 'Info': return '#ca8a04';
      default: return '#6b7280';
    }
  };

  // Calculate control limits for reference lines
  const outputs = data.map(d => d.energyOutput);
  const mean = outputs.reduce((a, b) => a + b, 0) / outputs.length;
  const stdDev = Math.sqrt(outputs.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / outputs.length);
  const upperControlLimit = mean + 3 * stdDev;
  const lowerControlLimit = mean - 3 * stdDev;

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium">Enhanced Energy Output Analysis</h3>
        <div className="flex items-center space-x-4 text-xs">
          <span className="text-gray-500">
            UCL: {upperControlLimit.toFixed(1)} kWh
          </span>
          <span className="text-gray-500">
            Mean: {mean.toFixed(1)} kWh
          </span>
          <span className="text-gray-500">
            LCL: {lowerControlLimit.toFixed(1)} kWh
          </span>
        </div>
      </div>
      
      <div className="h-[450px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 80 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200" />
            <XAxis 
              dataKey="date" 
              className="text-gray-600"
              tick={{ fontSize: 11 }}
              angle={-45}
              textAnchor="end"
              height={60}
            />
            <YAxis 
              className="text-gray-600"
              tick={{ fontSize: 11 }}
              label={{ 
                value: 'Energy Output (kWh)', 
                angle: -90, 
                position: 'insideLeft',
                style: { textAnchor: 'middle' }
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            
            {/* Control limit reference lines */}
            <ReferenceDot
              x={data[0]?.date}
              y={upperControlLimit}
              fill="transparent"
              stroke="transparent"
            />
            <ReferenceDot
              x={data[data.length - 1]?.date}
              y={upperControlLimit}
              fill="transparent"
              stroke="transparent"
            />
            
            {/* Main energy output line */}
            <Line 
              type="monotone" 
              dataKey="energyOutput" 
              stroke="#2563eb" 
              strokeWidth={2}
              dot={{ fill: '#2563eb', strokeWidth: 1, r: 3 }}
              activeDot={{ r: 5, fill: '#2563eb' }}
            />
            
            {/* Enhanced anomaly markers with severity-based colors */}
            {data.map((point, index) => {
              if (!point.isAnomaly) return null;
              
              const severity = point.severity || 'Info';
              const size = severity === 'Critical' ? 8 : severity === 'Warning' ? 6 : 5;
              
              return (
                <ReferenceDot
                  key={`anomaly-${index}`}
                  x={point.date}
                  y={point.energyOutput}
                  r={size}
                  fill={getSeverityFill(severity)}
                  stroke="#ffffff"
                  strokeWidth={2}
                  opacity={0.9}
                />
              );
            })}
            
            {/* Anomaly score overlay (optional) */}
            {showAnomalyScores && data.some(d => d.anomalyScore) && (
              <Line 
                type="monotone" 
                dataKey="anomalyScore" 
                stroke="#f97316" 
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={false}
                yAxisId="score"
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
      
      {/* Enhanced legend with severity indicators */}
      <div className="mt-4 space-y-3">
        <div className="flex items-center gap-6 text-sm flex-wrap">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-600" />
            <span>Normal Output</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-600" />
            <AlertCircle className="h-3 w-3 text-red-600" />
            <span>Critical Anomaly</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-orange-600" />
            <AlertTriangle className="h-3 w-3 text-orange-600" />
            <span>Warning</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-600" />
            <Info className="h-3 w-3 text-yellow-600" />
            <span>Info</span>
          </div>
          {showAnomalyScores && (
            <div className="flex items-center gap-2">
              <div className="w-3 h-0.5 bg-orange-500" style={{ borderTop: '1px dashed' }} />
              <span>Anomaly Score</span>
            </div>
          )}
        </div>
        
        {/* Anomaly summary */}
        <div className="bg-gray-50 rounded-lg p-3">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Total Points:</span>
              <span className="ml-2 font-medium">{data.length}</span>
            </div>
            <div>
              <span className="text-gray-600">Anomalies:</span>
              <span className="ml-2 font-medium text-red-600">
                {data.filter(d => d.isAnomaly).length}
              </span>
            </div>
            <div>
              <span className="text-gray-600">Critical:</span>
              <span className="ml-2 font-medium text-red-600">
                {data.filter(d => d.severity === 'Critical').length}
              </span>
            </div>
            <div>
              <span className="text-gray-600">Rate:</span>
              <span className="ml-2 font-medium">
                {((data.filter(d => d.isAnomaly).length / data.length) * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Companion component for anomaly alerts list
export const AnomalyAlertsList = ({ data }: { data: EnhancedChartData[] }) => {
  const anomalies = data.filter(d => d.isAnomaly);
  
  if (anomalies.length === 0) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
        <div className="text-green-600 mb-2">✓</div>
        <p className="text-green-800 font-medium">No anomalies detected</p>
        <p className="text-green-600 text-sm">System operating within normal parameters</p>
      </div>
    );
  }
  
  return (
    <div className="space-y-2">
      <h4 className="font-medium text-gray-900">Active Anomaly Alerts</h4>
      <div className="max-h-60 overflow-y-auto space-y-2">
        {anomalies
          .sort((a, b) => (b.anomalyScore || 0) - (a.anomalyScore || 0))
          .map((anomaly, index) => (
            <div 
              key={index}
              className={`p-3 rounded-lg border-l-4 ${
                anomaly.severity === 'Critical' 
                  ? 'bg-red-50 border-red-500' 
                  : anomaly.severity === 'Warning'
                  ? 'bg-orange-50 border-orange-500'
                  : 'bg-yellow-50 border-yellow-500'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    {anomaly.severity === 'Critical' && <AlertCircle className="h-4 w-4 text-red-600" />}
                    {anomaly.severity === 'Warning' && <AlertTriangle className="h-4 w-4 text-orange-600" />}
                    {anomaly.severity === 'Info' && <Info className="h-4 w-4 text-yellow-600" />}
                    <span className="font-medium text-sm">{anomaly.severity} Anomaly</span>
                  </div>
                  <p className="text-sm text-gray-700">
                    {anomaly.date} - {anomaly.energyOutput.toFixed(1)} kWh
                  </p>
                  {anomaly.anomalyScore && (
                    <p className="text-xs text-gray-500 mt-1">
                      Anomaly Score: {anomaly.anomalyScore.toFixed(3)}
                    </p>
                  )}
                </div>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                  anomaly.severity === 'Critical' 
                    ? 'bg-red-100 text-red-800' 
                    : anomaly.severity === 'Warning'
                    ? 'bg-orange-100 text-orange-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {anomaly.severity}
                </span>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}; 