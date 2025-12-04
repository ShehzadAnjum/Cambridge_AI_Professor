import { create } from 'zustand';

// Define the types for the state
interface Question {
  id: number;
  question_number: string;
  max_marks: number | null;
}

interface ExamDetails {
  mock_exam_id: number;
  questions: Question[];
}

interface DiagnosedWeakness {
  question_number: string;
  weakness: string;
  suggestion: string;
}

interface ExamResult {
  total_score: number;
  max_score: number;
  weaknesses: DiagnosedWeakness[];
}

// Define the state structure and actions
interface LoopState {
  loopId: number | null;
  studentId: number | null;
  currentStage: 'idle' | 'assigning' | 'assigned' | 'testing' | 'diagnosing' | 'finished';
  learningPackId: number | null;
  examDetails: ExamDetails | null;
  examResult: ExamResult | null;
  error: string | null;

  startLoop: (studentId: number, topics: string[]) => Promise<void>;
  generateTest: () => Promise<void>;
  submitTest: (answers: { question_id: number; answer_text: string }[]) => Promise<void>;
  reset: () => void;
}

export const useLoopStore = create<LoopState>((set, get) => ({
  // Initial State
  loopId: null,
  studentId: null,
  currentStage: 'idle',
  learningPackId: null,
  examDetails: null,
  examResult: null,
  error: null,

  // Actions
  startLoop: async (studentId, topics) => {
    set({ currentStage: 'assigning', error: null });
    try {
      const response = await fetch('http://127.0.0.1:8000/api/loop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_id: studentId, topics }),
      });
      if (!response.ok) throw new Error('Failed to start loop.');
      const data = await response.json();
      set({
        loopId: data.loop_id,
        studentId: data.student_id,
        learningPackId: data.learning_pack_id,
        currentStage: 'assigned',
      });
    } catch (error: any) {
      set({ error: error.message, currentStage: 'idle' });
    }
  },

  generateTest: async () => {
    const { loopId } = get();
    if (!loopId) return;
    set({ currentStage: 'testing', error: null });
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/loop/${loopId}/generate-test`, {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to generate test.');
      const data = await response.json();
      set({ examDetails: data, currentStage: 'testing' });
    } catch (error: any) {
      set({ error: error.message, currentStage: 'assigned' });
    }
  },

  submitTest: async (answers) => {
    const { loopId } = get();
    if (!loopId) return;
    set({ currentStage: 'diagnosing', error: null });
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/loop/${loopId}/submit-test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers }),
      });
      if (!response.ok) throw new Error('Failed to submit test.');
      const data = await response.json();
      set({ examResult: data, currentStage: 'finished' });
    } catch (error: any) {
      set({ error: error.message, currentStage: 'testing' });
    }
  },

  reset: () => {
    set({
      loopId: null,
      studentId: null,
      currentStage: 'idle',
      learningPackId: null,
      examDetails: null,
      examResult: null,
      error: null,
    });
  },
}));
