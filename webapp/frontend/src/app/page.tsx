"use client";

import { useState } from "react";
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

export default function Home() {
  const [studentId, setStudentId] = useState("");
  const [topics, setTopics] = useState("");
  const [status, setStatus] = useState("Idle");
  const [error, setError] = useState("");

  const handleStartLoop = async () => {
    setStatus("Starting loop...");
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/start-loop", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: parseInt(studentId, 10),
          topics: topics.split(",").map((t) => t.trim()),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to start learning loop");
      }

      const data = await response.json();
      if (data.error) {
        throw new Error(data.error);
      }
      
      setStatus("Learning loop started successfully!");
    } catch (err: any) {
      setError(err.message);
      setStatus("Error");
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-background">
      <Card className="w-[450px]">
        <CardHeader>
          <CardTitle>Cambridge AI Professor</CardTitle>
          <CardDescription>Start a new A*-Workflow learning loop.</CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="studentId">Student ID</Label>
                <Input
                  id="studentId"
                  placeholder="Enter your student ID"
                  value={studentId}
                  onChange={(e) => setStudentId(e.target.value)}
                />
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="topics">Syllabus Topics</Label>
                <Input
                  id="topics"
                  placeholder="e.g., 1.1, 1.2, 2.3"
                  value={topics}
                  onChange={(e) => setTopics(e.target.value)}
                />
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex flex-col items-start">
          <Button onClick={handleStartLoop} className="w-full">
            Start Learning Loop
          </Button>
          <div className="mt-4 text-sm">
            <p>Status: {status}</p>
            {error && <p className="text-red-500">Error: {error}</p>}
          </div>
        </CardFooter>
      </Card>
    </main>
  );
}