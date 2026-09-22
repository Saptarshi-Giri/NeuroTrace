import { useEffect, useState } from 'react';
import { fetchTraceList, fetchTraceDetail, type TraceDetail, type TraceSummary } from './api/traces';
import { DAGViewer } from './features/DAGViewer/DAGViewer';

export default function App() {
  const [traces, setTraces] = useState<TraceSummary[]>([]);
  const [selectedTrace, setSelectedTrace] = useState<TraceDetail | null>(null);

  useEffect(() => {
    fetchTraceList().then(setTraces);
  }, []);

  const handleSelectTrace = async (traceId: string) => {
    const detail = await fetchTraceDetail(traceId);
    setSelectedTrace(detail);
  };

  return (
    <div style={{ padding: '24px', fontFamily: 'sans-serif', backgroundColor: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '24px', color: '#0f172a' }}>Agent Trace Cost & Failure Profiler</h1>
        <p style={{ color: '#64748b', margin: '4px 0 0 0' }}>Inspect multi-step LLM chains and highlight redundant loops</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '24px' }}>
        {/* Trace List Sidebar */}
        <div style={{ background: '#fff', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <h3 style={{ marginTop: 0, fontSize: '16px' }}>Ingested Traces</h3>
          {traces.length === 0 ? (
            <p style={{ color: '#94a3b8', fontSize: '14px' }}>No traces found. Run generate_sample_trace.py.</p>
          ) : (
            traces.map((t) => (
              <div
                key={t.trace_id}
                onClick={() => handleSelectTrace(t.trace_id)}
                style={{
                  padding: '12px',
                  marginBottom: '8px',
                  borderRadius: '6px',
                  border: '1px solid #e2e8f0',
                  cursor: 'pointer',
                  backgroundColor: selectedTrace?.trace_id === t.trace_id ? '#eff6ff' : '#fff',
                }}
              >
                <div style={{ fontWeight: 'bold', fontSize: '14px' }}>{t.trace_id}</div>
                <div style={{ fontSize: '12px', color: '#64748b' }}>
                  Spans: {t.span_count} | Cost: ${t.total_cost.toFixed(4)}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Main DAG Graph Area */}
        <div>
          {selectedTrace ? (
            <div>
              <div style={{ marginBottom: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2 style={{ margin: 0, fontSize: '18px' }}>Trace: {selectedTrace.trace_id}</h2>
                <span style={{ fontSize: '14px', color: '#64748b' }}>Session: {selectedTrace.session_id}</span>
              </div>
              <DAGViewer spans={selectedTrace.spans} />
            </div>
          ) : (
            <div
              style={{
                height: '600px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: '2px dashed #cbd5e1',
                borderRadius: '8px',
                color: '#94a3b8',
              }}
            >
              Select a trace from the left panel to inspect the DAG tree
            </div>
          )}
        </div>
      </div>
    </div>
  );
}