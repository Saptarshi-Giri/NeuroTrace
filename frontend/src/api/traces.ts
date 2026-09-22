import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/v1/traces';

// 1. ADDED THIS INTERFACE
export interface TraceSummary {
  trace_id: string;
  session_id: string;
  total_cost: number;
  span_count: number;
}

export interface Span {
  span_id: string;
  parent_id: string | null;
  name: string;
  span_type: 'agent' | 'llm' | 'tool';
  inputs: Record<string, unknown>;
  outputs: Record<string, unknown>;
  tokens?: { total_tokens: number; cost_usd: number };
  flags: Array<{ flag_type: string; severity: string; message: string }>;
}

export interface TraceDetail {
  trace_id: string;
  session_id: string;
  total_cost: number;
  spans: Span[];
}

// 2. UPDATED THIS FUNCTION with the return type
export const fetchTraceList = async (): Promise<TraceSummary[]> => {
  const res = await axios.get(API_BASE);
  return res.data;
};

export const fetchTraceDetail = async (traceId: string): Promise<TraceDetail> => {
  const res = await axios.get(`${API_BASE}/${traceId}`);
  return res.data;
};