interface Props {
  sessionId: string;
  attempts: number;
  lastError: string;
  onChoice: (choice: "replan" | "simplify" | "pause") => void;
}

export default function EscalationPanel({ sessionId, attempts, lastError, onChoice }: Props) {
  return (
    <div style={{
      background: "linear-gradient(135deg, #1c1917 0%, #292524 100%)",
      border: "1px solid #b45309",
      borderRadius: "12px",
      padding: "20px",
      margin: "12px 0",
      fontFamily: "'Inter', sans-serif",
      animation: "pulse-border 2s ease-in-out infinite, slideIn 0.3s ease-out",
    }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "12px" }}>
        <span style={{ fontSize: "22px" }}>⚠️</span>
        <div>
          <div style={{ color: "#fcd34d", fontWeight: 700, fontSize: "14px" }}>
            Agent is stuck after {attempts} attempt{attempts !== 1 ? "s" : ""}
          </div>
          <div style={{ color: "#78716c", fontSize: "11px", marginTop: "2px" }}>
            The agent needs your guidance to proceed
          </div>
        </div>
      </div>

      {/* Error summary */}
      <div style={{
        background: "rgba(127, 29, 29, 0.3)",
        border: "1px solid #7f1d1d",
        borderRadius: "8px",
        padding: "10px 12px",
        marginBottom: "16px",
      }}>
        <div style={{ color: "#fca5a5", fontSize: "11px", fontWeight: 500, marginBottom: "4px" }}>
          Last error:
        </div>
        <div style={{ color: "#f87171", fontSize: "12px", fontFamily: "monospace", wordBreak: "break-all" }}>
          {lastError.substring(0, 200)}{lastError.length > 200 ? "..." : ""}
        </div>
      </div>

      {/* Choice buttons */}
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <ActionButton
          emoji="🔄"
          label="Try a different approach"
          description="Replan from scratch using a different strategy"
          color="#d97706"
          onClick={() => onChoice("replan")}
        />
        <ActionButton
          emoji="🎯"
          label="Simplify the task"
          description="Strip down to the simplest working version"
          color="#7c3aed"
          onClick={() => onChoice("simplify")}
        />
        <ActionButton
          emoji="💬"
          label="Pause and let me guide"
          description="Stop execution — I'll update the task or provide more info"
          color="#374151"
          onClick={() => onChoice("pause")}
        />
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

function ActionButton({ emoji, label, description, color, onClick }: {
  emoji: string; label: string; description: string; color: string; onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        display: "flex",
        alignItems: "center",
        gap: "12px",
        padding: "10px 14px",
        background: `${color}22`,
        border: `1px solid ${color}66`,
        borderRadius: "8px",
        cursor: "pointer",
        textAlign: "left",
        width: "100%",
        transition: "all 0.15s ease",
      }}
      onMouseEnter={e => (e.currentTarget.style.background = `${color}44`)}
      onMouseLeave={e => (e.currentTarget.style.background = `${color}22`)}
    >
      <span style={{ fontSize: "18px" }}>{emoji}</span>
      <div>
        <div style={{ color: "#e5e7eb", fontSize: "13px", fontWeight: 600 }}>{label}</div>
        <div style={{ color: "#6b7280", fontSize: "11px", marginTop: "2px" }}>{description}</div>
      </div>
    </button>
  );
}
