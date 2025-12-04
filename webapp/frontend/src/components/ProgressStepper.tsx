"use client";

import { useLoopStore } from "@/store/loop-store";

const stages = ["Assign", "Test", "Diagnose", "Finished"];
const stageMap = {
  idle: -1,
  assigning: 0,
  assigned: 0,
  testing: 1,
  diagnosing: 2,
  finished: 3,
};

export function ProgressStepper() {
  const currentStage = useLoopStore((state) => state.currentStage);
  const activeIndex = stageMap[currentStage] ?? -1;

  return (
    <div className="w-full max-w-2xl mx-auto py-8">
      <div className="flex items-center justify-between">
        {stages.map((stage, index) => (
          <div key={stage} className="flex flex-col items-center">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center text-white ${
                index <= activeIndex ? "bg-blue-600" : "bg-gray-300"
              }`}
            >
              {index < activeIndex ? "✓" : index + 1}
            </div>
            <p className="mt-2 text-sm text-center">{stage}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
