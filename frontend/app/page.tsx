"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Activity, AlertTriangle, CheckCircle2, RadioTower, ShieldCheck, Undo2, Zap } from "lucide-react";
import { post, WS_URL } from "../lib/api";
import { StatCard } from "../components/StatCard";

type State = {
  telemetry: {
    timestamp: string;
    zone: string;
    crowd_density: number;
    wait_time_minutes: number;
    throughput_per_minute: number;
    transport_delay_minutes: number;
    sentiment_score: number;
    weather: string;
    vendor_stock_percent: number;
    severity: string;
  };
  active_incident?: any;
  timeline: string[];
};

export default function Page() {
  const [state, setState] = useState<State | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    ws.onmessage = (event) => setState(JSON.parse(event.data));
    return () => ws.close();
  }, []);

  async function run(action: () => Promise<any>) {
    setBusy(true);
    try { await action(); } finally { setBusy(false); }
  }

  const t = state?.telemetry;
  const incident = state?.active_incident;
  const plan = incident?.plan;
  const density = t ? Math.round(t.crowd_density * 100) : 0;
  const sentiment = t ? t.sentiment_score.toFixed(2) : "0.00";

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,#183766,#050816_45%)] p-6 text-slate-100">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="flex flex-col gap-4 rounded-3xl border border-white/10 bg-black/30 p-6 shadow-glow md:flex-row md:items-center md:justify-between">
          <div>
            <div className="flex items-center gap-2 text-sm text-blue-300"><RadioTower size={16}/> Gemini + Elastic MCP Demo</div>
            <h1 className="mt-2 text-4xl font-bold tracking-tight">WorldCupOps Agent</h1>
            <p className="mt-2 max-w-2xl text-slate-300">AI incident commander for World Cup-scale stadium operations. Detect, investigate, approve, execute, and monitor recovery.</p>
          </div>
          <div className="flex flex-wrap gap-3">
            <button disabled={busy} onClick={() => run(() => post('/api/simulator/inject/gate-b-surge'))} className="rounded-2xl bg-amber-500 px-4 py-3 font-semibold text-black shadow-lg hover:bg-amber-400 disabled:opacity-60"><AlertTriangle className="mr-2 inline" size={18}/>Inject Incident</button>
            <button disabled={busy} onClick={() => run(() => post('/api/agent/analyze'))} className="rounded-2xl bg-blue-500 px-4 py-3 font-semibold text-white shadow-lg hover:bg-blue-400 disabled:opacity-60"><Zap className="mr-2 inline" size={18}/>Run Agent</button>
            {incident?.status === 'awaiting_approval' && <button disabled={busy} onClick={() => run(() => post(`/api/incidents/${incident.id}/approve`))} className="rounded-2xl bg-emerald-500 px-4 py-3 font-semibold text-black shadow-lg hover:bg-emerald-400"><ShieldCheck className="mr-2 inline" size={18}/>Approve Actions</button>}
            {incident && <button disabled={busy} onClick={() => run(() => post(`/api/incidents/${incident.id}/rollback`))} className="rounded-2xl bg-slate-700 px-4 py-3 font-semibold text-white hover:bg-slate-600"><Undo2 className="mr-2 inline" size={18}/>Rollback</button>}
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-5">
          <StatCard label="Crowd density" value={`${density}%`} hint={density > 80 ? "High-risk congestion" : "Safe operating range"} />
          <StatCard label="Wait time" value={`${t?.wait_time_minutes ?? 0}m`} hint="Gate B entry queue" />
          <StatCard label="Throughput" value={`${t?.throughput_per_minute ?? 0}/m`} hint="Fans processed per minute" />
          <StatCard label="Transport delay" value={`${t?.transport_delay_minutes ?? 0}m`} hint="Stadium Express route" />
          <StatCard label="Sentiment" value={sentiment} hint="Fan experience signal" />
        </section>

        <section className="grid gap-6 lg:grid-cols-3">
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="rounded-3xl border border-white/10 bg-white/5 p-6 lg:col-span-2">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold">Live Operations Map</h2>
              <span className={`rounded-full px-3 py-1 text-xs font-semibold ${t?.severity === 'high' ? 'bg-amber-500 text-black' : 'bg-emerald-500 text-black'}`}>{t?.severity ?? 'loading'}</span>
            </div>
            <div className="grid min-h-[340px] grid-cols-3 gap-4 rounded-2xl bg-black/30 p-5">
              {['Gate A','Gate B','Gate C','Gate D','Transit Hub','Vendor Zone'].map((zone) => {
                const active = zone === 'Gate B';
                return <div key={zone} className={`flex items-center justify-center rounded-2xl border p-4 text-center ${active && density > 80 ? 'border-amber-400 bg-amber-500/20 text-amber-100' : active ? 'border-blue-400 bg-blue-500/10 text-blue-100' : 'border-white/10 bg-white/5 text-slate-300'}`}>
                  <div><div className="font-semibold">{zone}</div><div className="mt-2 text-xs">{active ? `${density}% density` : 'normal'}</div></div>
                </div>;
              })}
            </div>
          </motion.div>

          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <h2 className="mb-4 text-xl font-semibold">Incident Status</h2>
            {incident ? <div className="space-y-3">
              <div className="rounded-2xl bg-black/30 p-4"><div className="text-sm text-slate-400">Incident</div><div className="font-semibold">{incident.title}</div></div>
              <div className="rounded-2xl bg-black/30 p-4"><div className="text-sm text-slate-400">Status</div><div className="font-semibold">{incident.status}</div></div>
              <div className="rounded-2xl bg-black/30 p-4"><div className="text-sm text-slate-400">Zone</div><div className="font-semibold">{incident.zone}</div></div>
            </div> : <div className="rounded-2xl bg-emerald-500/10 p-4 text-emerald-200"><CheckCircle2 className="mb-2"/>No active incident. Operations stable.</div>}
          </div>
        </section>

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <h2 className="text-xl font-semibold">AI Reasoning and Mitigation Plan</h2>
            {plan ? <div className="mt-4 space-y-4 text-sm">
              <div><b>Root causes</b><ul className="mt-2 list-disc space-y-1 pl-5 text-slate-300">{plan.root_causes.map((x: string) => <li key={x}>{x}</li>)}</ul></div>
              <div><b>Recommended actions</b><ul className="mt-2 list-disc space-y-1 pl-5 text-slate-300">{plan.recommended_actions.map((x: string) => <li key={x}>{x}</li>)}</ul></div>
              <div className="rounded-2xl bg-blue-500/10 p-4 text-blue-100"><b>Estimated impact:</b> {plan.estimated_impact}</div>
            </div> : <p className="mt-4 text-slate-400">Click “Run Agent” after injecting the incident to show Gemini planning.</p>}
          </div>
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <h2 className="text-xl font-semibold">Elastic MCP Tool Calls</h2>
            {plan?.elastic_mcp_calls?.length ? <ul className="mt-4 space-y-3 text-sm">{plan.elastic_mcp_calls.map((x: string) => <li className="rounded-2xl bg-black/30 p-3 font-mono text-blue-200" key={x}>{x}</li>)}</ul> : <p className="mt-4 text-slate-400">MCP call trace will appear here.</p>}
          </div>
        </section>

        <section className="rounded-3xl border border-white/10 bg-white/5 p-6">
          <h2 className="mb-4 text-xl font-semibold">Timeline and Audit Trail</h2>
          <div className="grid gap-3 md:grid-cols-2">
            {(state?.timeline ?? []).slice().reverse().map((x) => <div className="rounded-2xl bg-black/30 p-3 text-sm text-slate-300" key={x}><Activity className="mr-2 inline text-blue-300" size={14}/>{x}</div>)}
            {incident?.audit_log?.map((x: string) => <div className="rounded-2xl bg-black/30 p-3 text-sm text-slate-300" key={x}><ShieldCheck className="mr-2 inline text-emerald-300" size={14}/>{x}</div>)}
          </div>
        </section>
      </div>
    </main>
  );
}
