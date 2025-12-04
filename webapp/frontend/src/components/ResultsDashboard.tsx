"use client";

import { useLoopStore } from "@/store/loop-store";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function ResultsDashboard() {
  const { examResult, reset } = useLoopStore();

  if (!examResult) {
    return <p>Loading results...</p>;
  }

  const { total_score, max_score, weaknesses } = examResult;
  const percentage = max_score > 0 ? (total_score / max_score) * 100 : 0;

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle>Stage 3: Results & Diagnosis</CardTitle>
        <CardDescription>
          Here is the breakdown of your performance.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="text-center">
          <p className="text-lg font-semibold">Your Score</p>
          <p className="text-4xl font-bold">
            {total_score.toFixed(1)} / {max_score.toFixed(1)}
          </p>
          <p className="text-2xl text-blue-600">{percentage.toFixed(1)}%</p>
        </div>

        {weaknesses.length > 0 && (
          <div>
            <h3 className="font-semibold mb-2">Areas for Improvement</h3>
            <ul className="list-disc pl-5 space-y-2">
              {weaknesses.map((weakness, index) => (
                <li key={index}>
                  <span className="font-semibold">Question {weakness.question_number}:</span>{" "}
                  {weakness.suggestion}
                </li>
              ))}
            </ul>
          </div>
        )}

        {weaknesses.length === 0 && (
            <p className="text-center text-green-600 font-semibold">
                Excellent work! No significant weaknesses were diagnosed.
            </p>
        )}

      </CardContent>
      <CardFooter>
        <Button onClick={reset} className="w-full">
          Start a New Loop
        </Button>
      </CardFooter>
    </Card>
  );
}
