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
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function TopicSelector() {
  const { startLoop, currentStage, error } = useLoopStore();
  const [studentId, setStudentId] = useState("1"); // Default for easy testing
  const [topics, setTopics] = useState("1.1, 1.2"); // Default for easy testing

  const handleSubmit = () => {
    const studentIdNum = parseInt(studentId, 10);
    const topicsArray = topics.split(",").map((t) => t.trim());
    if (!studentIdNum || topicsArray.length === 0) {
      alert("Please provide a valid Student ID and at least one topic.");
      return;
    }
    startLoop(studentIdNum, topicsArray);
  };

  const isLoading = currentStage === 'assigning';

  return (
    <Card className="w-[450px]">
      <CardHeader>
        <CardTitle>Start a New Learning Loop</CardTitle>
        <CardDescription>Select a student and the topics you want to focus on.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid w-full items-center gap-4">
          <div className="flex flex-col space-y-1.5">
            <Label htmlFor="studentId">Student ID</Label>
            <Input
              id="studentId"
              placeholder="Enter student ID"
              value={studentId}
              onChange={(e) => setStudentId(e.target.value)}
              disabled={isLoading}
            />
          </div>
          <div className="flex flex-col space-y-1.5">
            <Label htmlFor="topics">Syllabus Topics (comma-separated)</Label>
            <Input
              id="topics"
              placeholder="e.g., 1.1, 1.2, 2.3"
              value={topics}
              onChange={(e) => setTopics(e.target.value)}
              disabled={isLoading}
            />
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex flex-col items-start gap-4">
        <Button onClick={handleSubmit} disabled={isLoading} className="w-full">
          {isLoading ? "Generating Learning Pack..." : "Assign Learning Pack"}
        </Button>
        {error && <p className="text-sm text-red-500">{error}</p>}
      </CardFooter>
    </Card>
  );
}
