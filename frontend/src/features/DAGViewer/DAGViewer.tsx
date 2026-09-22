import React, { useMemo, useState } from 'react';
import { ReactFlow, Background, Controls, type Node, type Edge } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import type { Span } from '../../api/traces';

interface DAGViewerProps {
  spans: Span[];
}

export const DAGViewer: React.FC<DAGViewerProps> = ({ spans }) => {
  const [selectedSpan, setSelectedSpan] = useState<Span | null>(null);

  const { nodes, edges } = useMemo(() => {
    const nodesList: Node[] = [];
    const edgesList: Edge[] = [];
    const levelMap: Record<string, number> = {};
    
    spans.forEach((span) => {
      levelMap[span.span_id] = span.parent_id ? (levelMap[span.parent_id] || 0) + 1 : 0;
    });

    const levelCounts: Record<number, number> = {};

    spans.forEach((span) => {
      const level = levelMap[span.span_id] || 0;
      const indexInLevel = levelCounts[level] || 0;
      levelCounts[level] = indexInLevel + 1;

      const hasFlags = span.flags && span.flags.length > 0;

      nodesList.push({
        id: span.span_id,
        position: { x: indexInLevel * 250 + 50, y: level * 120 + 50 },
        style: {
          padding: '12px 16px',
          borderRadius: '8px',
          background: hasFlags ? '#fef2f2' : '#ffffff',
          border: hasFlags ? '2px solid #ef4444' : '1px solid #cbd5e1',
          color: '#1e293b',
          boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
          width: 220,
          cursor: 'pointer',
        },
        data: {
          label: (
            <div style={{ fontSize: '12px' }}>
              <div style={{ fontWeight: 'bold', color: span.span_type === 'tool' ? '#2563eb' : '#0f172a' }}>
                [{span.span_type.toUpperCase()}] {span.name}
              </div>
              {hasFlags && (
                <div style={{ color: '#dc2626', fontSize: '10px', marginTop: '4px', fontWeight: 'bold' }}>
                  ⚠️ {span.flags[0].flag_type}
                </div>
              )}
            </div>
          ),
        },
      });

      if (span.parent_id) {
        edgesList.push({
          id: `e-${span.parent_id}-${span.span_id}`,
          source: span.parent_id,
          target: span.span_id,
          animated: hasFlags,
          style: { stroke: hasFlags ? '#ef4444' : '#94a3b8', strokeWidth: 2 },
        });
      }
    });

    return { nodes: nodesList, edges: edgesList };
  }, [spans]);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: selectedSpan ? '1fr 320px' : '1fr', gap: '16px' }}>
      <div style={{ width: '100%', height: '600px', border: '1px solid #e2e8f0', borderRadius: '8px' }}>
        <ReactFlow 
          nodes={nodes} 
          edges={edges} 
          fitView
          onNodeClick={(_, node) => {
            const span = spans.find((s) => s.span_id === node.id);
            if (span) setSelectedSpan(span);
          }}
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>

      {/* Span Inspector Sidebar */}
      {selectedSpan && (
        <div style={{ background: '#fff', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0', overflowY: 'auto', maxHeight: '600px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ margin: 0, fontSize: '16px' }}>{selectedSpan.name}</h3>
            <button onClick={() => setSelectedSpan(null)} style={{ border: 'none', background: 'none', cursor: 'pointer', fontWeight: 'bold' }}>✕</button>
          </div>
          <p style={{ color: '#64748b', fontSize: '12px' }}>Type: {selectedSpan.span_type} | ID: {selectedSpan.span_id}</p>
          
          {selectedSpan.flags.length > 0 && (
            <div style={{ background: '#fef2f2', border: '1px solid #fca5a5', padding: '8px', borderRadius: '6px', marginBottom: '12px' }}>
              <strong style={{ color: '#dc2626', fontSize: '12px' }}>Flags Detected:</strong>
              {selectedSpan.flags.map((f, i) => (
                <div key={i} style={{ fontSize: '11px', color: '#991b1b', marginTop: '4px' }}>
                  • <strong>{f.flag_type}</strong>: {f.message}
                </div>
              ))}
            </div>
          )}

          <h4 style={{ fontSize: '13px', marginBottom: '4px' }}>Inputs</h4>
          <pre style={{ background: '#f8fafc', padding: '8px', borderRadius: '4px', fontSize: '11px', overflowX: 'auto' }}>
            {JSON.stringify(selectedSpan.inputs, null, 2)}
          </pre>

          <h4 style={{ fontSize: '13px', marginBottom: '4px' }}>Outputs</h4>
          <pre style={{ background: '#f8fafc', padding: '8px', borderRadius: '4px', fontSize: '11px', overflowX: 'auto' }}>
            {JSON.stringify(selectedSpan.outputs, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};