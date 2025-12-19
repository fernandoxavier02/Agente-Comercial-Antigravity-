async function fetchLead(id) {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
  const res = await fetch(`${base}/leads/${id}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

async function fetchDraft(id) {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
  const res = await fetch(`${base}/leads/${id}/drafts`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export default async function LeadPage({ params }) {
  const id = params.id;
  const lead = await fetchLead(id);
  const draft = await fetchDraft(id);

  if (!lead) return <div>Lead não encontrado.</div>;

  return (
    <div style={{ display: "grid", gap: 12 }}>
      <a href="/" style={{ color: "#555" }}>← voltar</a>

      <div style={{ padding: 12, border: "1px solid #eee", borderRadius: 12 }}>
        <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
          <div>
            <div style={{ fontWeight: 700, fontSize: 18 }}>{lead.pain_point?.label}</div>
            <div style={{ color: "#666" }}>{lead.author_handle} • {lead.source}</div>
            <div style={{ marginTop: 8, color: "#333" }}>{lead.text_excerpt}</div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 12, color: "#777" }}>lead_score</div>
            <div style={{ fontWeight: 800, fontSize: 22 }}>{lead.scores?.lead_score ?? "-"}</div>
            <div style={{ fontSize: 12, color: "#777", marginTop: 6 }}>intent</div>
            <div style={{ fontWeight: 600 }}>{lead.intent_stage?.label}</div>
          </div>
        </div>

        <div style={{ marginTop: 10 }}>
          <a href={lead.source_url} target="_blank" rel="noreferrer">ver fonte</a>
        </div>
      </div>

      <div style={{ padding: 12, border: "1px solid #eee", borderRadius: 12 }}>
        <div style={{ fontWeight: 700 }}>Evidências</div>
        <ul>
          {(lead.evidence || []).map((e, idx) => (
            <li key={idx} style={{ color: "#444" }}>{e.text}</li>
          ))}
        </ul>
      </div>

      <div style={{ padding: 12, border: "1px solid #eee", borderRadius: 12 }}>
        <div style={{ fontWeight: 700 }}>Rascunhos</div>
        {!draft && <div style={{ color: "#666" }}>Sem rascunho ainda.</div>}
        {draft && (
          <div style={{ display: "grid", gap: 10 }}>
            {(draft.drafts || []).map((d, idx) => (
              <div key={idx} style={{ padding: 10, border: "1px dashed #ddd", borderRadius: 10 }}>
                <div style={{ whiteSpace: "pre-wrap" }}>{d}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
