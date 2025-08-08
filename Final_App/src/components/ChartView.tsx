import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceDot } from 'recharts';

interface ChartData {
  date: string;
  energyOutput: number;
  isAnomaly: boolean;
}

interface ChartViewProps {
  data: ChartData[];
}

export const ChartView = ({ data }: ChartViewProps) => {
  return (
    <div className="w-full h-[400px]">
      <h3 className="text-lg font-medium mb-4">Energy Output Over Time</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
          <XAxis 
            dataKey="date" 
            className="text-muted-foreground"
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            className="text-muted-foreground"
            tick={{ fontSize: 12 }}
            label={{ value: 'Energy Output (kWh)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'hsl(var(--card))',
              border: '1px solid hsl(var(--border))',
              borderRadius: '6px',
              color: 'hsl(var(--card-foreground))'
            }}
          />
          <Line 
            type="monotone" 
            dataKey="energyOutput" 
            stroke="hsl(var(--primary))" 
            strokeWidth={2}
            dot={{ fill: 'hsl(var(--primary))', strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, fill: 'hsl(var(--primary))' }}
          />
          {/* Anomaly dots */}
          {data.map((point, index) => 
            point.isAnomaly ? (
              <ReferenceDot
                key={index}
                x={point.date}
                y={point.energyOutput}
                r={6}
                fill="hsl(var(--destructive))"
                stroke="hsl(var(--destructive))"
                strokeWidth={2}
              />
            ) : null
          )}
        </LineChart>
      </ResponsiveContainer>
      <div className="flex items-center gap-4 mt-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-primary" />
          <span>Normal Output</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-destructive" />
          <span>Anomaly Detected</span>
        </div>
      </div>
    </div>
  );
};