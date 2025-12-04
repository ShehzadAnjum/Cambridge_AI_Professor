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

export function LearningPackDisplay() {
  const { learningPackId, generateTest, currentStage } = useLoopStore();
  const isLoading = currentStage === 'testing';

  return (
    <Card className="w-[450px]">
      <CardHeader>
        <CardTitle>Stage 1: Learning Pack Assigned</CardTitle>
        <CardDescription>
          Your personalized learning pack is ready. Review the materials before starting the test.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p>Learning Pack ID: {learningPackId}</p>
        <p className="mt-4 text-sm text-muted-foreground">
          (In a full implementation, this section would display the resources, notes, and videos included in the learning pack.)
        </p>
      </CardContent>
      <CardFooter>
        <Button onClick={generateTest} disabled={isLoading} className="w-full">
          {isLoading ? "Generating Test..." : "I'm Ready, Start Test"}
        </Button>
      </CardFooter>
    </Card>
  );
}
