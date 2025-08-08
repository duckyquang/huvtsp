import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

interface AnomalyData {
  date: string;
  energyOutput: number;
  anomalyFlag: string;
  score: number;
}

interface AnomalyTableProps {
  data: AnomalyData[];
}

export const AnomalyTable = ({ data }: AnomalyTableProps) => {
  return (
    <div className="w-full">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Date</TableHead>
            <TableHead>Energy Output (kWh)</TableHead>
            <TableHead>Anomaly Flag</TableHead>
            <TableHead>Anomaly Score</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index}>
              <TableCell className="font-medium">{row.date}</TableCell>
              <TableCell>{row.energyOutput.toFixed(1)}</TableCell>
              <TableCell>
                <Badge 
                  variant={row.anomalyFlag === 'Yes' ? 'destructive' : 'secondary'}
                  className="text-xs"
                >
                  {row.anomalyFlag}
                </Badge>
              </TableCell>
              <TableCell>
                <span className={`font-medium ${
                  row.score > 0.7 ? 'text-destructive' : 
                  row.score > 0.4 ? 'text-warning' : 
                  'text-success'
                }`}>
                  {row.score.toFixed(2)}
                </span>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};