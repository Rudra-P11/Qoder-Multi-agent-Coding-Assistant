import { useState } from "react";

interface Question {
  id: string;
  question: string;
  options: string[];
}

interface Props {
  sessionId: string;
  ambiguityScore: number;
  questions: Question[];
  onSubmit: (answers: Record<string, string>) => void;
  onSkip: () => void;
}

export default function ClarificationPanel({ sessionId, ambiguityScore, questions, onSubmit, onSkip }: Props) {
  const [answers, setAnswers] = useState<Record<string, string>>({});

  const handleSelect = (qId: string, option: string) => {
    setAnswers(prev => ({ ...prev, [qId]: option }));
  };

  const handleSubmit = () => {
    // Fill any unanswered questions with "Agent decides"
    const filled: Record<string, string> = {};
    questions.forEach(q => {
      filled[q.id] = answers[q.id] || "Agent decides";
    });
    onSubmit(filled);
  };

  const scorePercent = Math.round(ambiguityScore * 100);
  const scoreColor = ambiguityScore > 0.7 ? "#f87171" : ambiguityScore > 0.55 ? "#fbbf24" : "#34d399";

  return (
    <div style={{
      background: "linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)",
      border: "1px solid #4f46e5",
      borderRadius: "12px",
      padding: "20px",
      margin: "12px 0",
      fontFamily: "'Inter', sans-serif",
      animation: "slideIn 0.3s ease-out"
    }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
        <span style={{ fontSize: "20px" }}>🤔</span>
        <div>
          <div style={{ color: "#c7d2fe", fontWeight: 600, fontSize: "14px" }}>
            Task needs clarification
          </div>
          <div style={{ color: "#818cf8", fontSize: "11px", marginTop: "2px" }}>
            Ambiguity score:&nbsp;
            <span style={{ color: scoreColor, fontWeight: 700 }}>{scorePercent}%</span>
            &nbsp;— answering prevents wrong assumptions
          </div>
        </div>
      </div>

      {/* Questions */}
      <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
        {questions.map((q, i) => (
          <div key={q.id}>
            <div style={{ color: "#e0e7ff", fontSize: "13px", fontWeight: 500, marginBottom: "8px" }}>
              {i + 1}. {q.question}
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
              {q.options.map(option => {
                const selected = answers[q.id] === option;
                return (
                  <button
                    key={option}
                    onClick={() => handleSelect(q.id, option)}
                    style={{
                      padding: "6px 14px",
                      borderRadius: "20px",
                      border: selected ? "2px solid #818cf8" : "1px solid #3730a3",
                      background: selected ? "#3730a3" : "rgba(55, 48, 163, 0.3)",
                      color: selected ? "#e0e7ff" : "#a5b4fc",
                      fontSize: "12px",
                      cursor: "pointer",
                      fontWeight: selected ? 600 : 400,
                      transition: "all 0.15s ease",
                    }}
                  >
                    {selected && "✓ "}{option}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Actions */}
      <div style={{ display: "flex", gap: "10px", marginTop: "20px" }}>
        <button
          onClick={handleSubmit}
          style={{
            padding: "8px 20px",
            background: "linear-gradient(90deg, #4f46e5, #7c3aed)",
            color: "white",
            border: "none",
            borderRadius: "8px",
            fontSize: "13px",
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          ▶ Start with these constraints
        </button>
        <button
          onClick={onSkip}
          style={{
            padding: "8px 16px",
            background: "transparent",
            color: "#6b7280",
            border: "1px solid #374151",
            borderRadius: "8px",
            fontSize: "13px",
            cursor: "pointer",
          }}
        >
          Skip — let agent decide
        </button>
      </div>

      <style>{`
        @keyframes slideIn {
          from { opacity: 0; transform: translateY(-8px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}
