"use client";

import { useLoopStore } from "@/store/loop-store";
import { ProgressStepper } from "@/components/ProgressStepper";
import { TopicSelector } from "@/components/TopicSelector";
import { LearningPackDisplay } from "@/components/LearningPackDisplay";
import { ExamInterface } from "@/components/ExamInterface";
import { ResultsDashboard } from "@/components/ResultsDashboard";

export default function Home() {
  const currentStage = useLoopStore((state) => state.currentStage);

  const renderCurrentStage = () => {
    switch (currentStage) {
      case 'idle':
      case 'assigning':
        return <TopicSelector />;
      case 'assigned':
        return <LearningPackDisplay />;
      case 'testing':
      case 'diagnosing':
        return <ExamInterface />;
      case 'finished':
        return <ResultsDashboard />;
      default:
        return <p>Loading...</p>;
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-6 sm:p-12 md:p-24 bg-gray-50">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-12">
            <h1 className="text-4xl font-bold tracking-tight">Cambridge AI Professor</h1>
            <p className="text-lg text-muted-foreground mt-2">
                Your personal A-Level tutor, powered by the A*-Workflow.
            </p>
        </div>
        
        {currentStage !== 'idle' && <ProgressStepper />}
        
        <div className="mt-8 flex justify-center">
            {renderCurrentStage()}
        </div>
      </div>
    </main>
  );
}
