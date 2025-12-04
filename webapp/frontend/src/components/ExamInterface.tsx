"use client";

import { useState } from "react";
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
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

export function ExamInterface() {
  const { examDetails, submitTest, currentStage } = useLoopStore();
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const isLoading = currentStage === 'diagnosing';

  const handleAnswerChange = (questionId: number, value: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = () => {
    const formattedAnswers = Object.entries(answers).map(([qid, atext]) => ({
      question_id: parseInt(qid, 10),
      answer_text: atext,
    }));
    submitTest(formattedAnswers);
  };

  if (!examDetails) {
    return <p>Loading exam...</p>;
  }

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle>Stage 2: Mock Exam</CardTitle>
        <CardDescription>
          Answer the following questions to the best of your ability.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {examDetails.questions.map((q) => (
          <div key={q.id} className="space-y-2">
            <Label>
              Question {q.question_number} ({q.max_marks} marks)
            </Label>
            <p className="text-sm text-muted-foreground">
              (In a full implementation, the full question text would be displayed here.)
            </p>
            <Input
              placeholder="Your answer..."
              onChange={(e) => handleAnswerChange(q.id, e.target.value)}
              disabled={isLoading}
            />
          </div>
        ))}
      </CardContent>
      <CardFooter>
        <Button onClick={handleSubmit} disabled={isLoading} className="w-full">
          {isLoading ? "Submitting and Diagnosing..." : "Submit Exam"}
        </Button>
      </CardFooter>
    </Card>
  );
}
