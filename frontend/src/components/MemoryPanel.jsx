import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Search, Loader2, BrainCircuit, Plus, Eraser } from 'lucide-react';
import { API_BASE } from '../config';

const Stat = ({ label, value }) => (
  <div className="p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]">
    <p className="text-[18px] font-semibold text-white tabular-nums">{value ?? '—'}</p>
    <p className="text-[11px] text-ink-400">{label}</p>
  </div>
);

// Long-term memory drawer: stats (/memory/stats), semantic recall (/memory/recall),
// save a fact (/memory/ingest) and forget (/memory/forget).
export default function MemoryPanel({ open, onClose, notify }) {
  const [tab, setTab] = useState('search');
  const [stats, setStats] = useState(null);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [busy, setBusy] = useState(false);
  const [content, setContent] = useState('');

  const loadStats = async () => {
    try {
      const r = await fetch(`${API_BASE}/memory/stats`);
      const d = await r.json();
      setStats(d.status === 'success' ? d : null);
    } catch { setStats(null); }
  };
  useEffect(() => {
    if (!open) return;
    let live = true;
    fetch(`${API_BASE}/memory/stats`).then(r => r.json())
      .then(d => { if (live) setStats(d.status === 'success' ? d : null); })
      .catch(() => { if (live) setStats(null); });
    return () => { live = false; };
  }, [open]);

  const handleRecall = async (e) => {
    e?.preventDefault();
    if (!query.trim() || busy) return;
    setBusy(true);
    try {
      const r = await fetch(`${API_BASE}/memory/recall`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query.trim(), top_k: 8 }),
      });
      const d = await r.json();
      if (d.status !== 'success') throw new Error(d.message || 'Recall failed');
      setResults(d.results || []);
    } catch (err) {
      notify({ type: 'error', title: 'Memory search failed', text: err.message });
      setResults([]);
    } finally { setBusy(false); }
  };

  const handleForget = async () => {
    if (!query.trim() || !window.confirm(`Forget everything related to “${query.trim()}”?`)) return;
    setBusy(true);
    try {
      const r = await fetch(`${API_BASE}/memory/forget`, {
        method: 'DELETE', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query.trim() }),
      });
      const d = await r.json().catch(() => ({}));
      if (!r.ok || d.status === 'error') throw new Error(d.message || 'Forget failed');
      notify({ type: 'success', text: d.message || 'Forgotten.' });
      setResults(null); loadStats();
    } catch (err) {
      notify({ type: 'error', title: 'Could not forget', text: err.message });
    } finally { setBusy(false); }
  };

  const handleIngest = async (e) => {
    e.preventDefault();
    if (!content.trim() || busy) return;
    setBusy(true);
    try {
      const r = await fetch(`${API_BASE}/memory/ingest`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: content.trim() }),
      });
      // The endpoint reports failures as 200 + {status: "error"}, so check the body too
      const d = await r.json().catch(() => ({}));
      if (!r.ok || d.status !== 'success') throw new Error(d.message || 'Failed to save memory');
      setContent('');
      notify({ type: 'success', title: 'Saved to memory', text: 'Jarvis will remember that.' });
      loadStats();
    } catch (err) {
      notify({ type: 'error', title: 'Could not save', text: err.message });
    } finally { setBusy(false); }
  };

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div className="fixed inset-0 z-[90] bg-black/40 backdrop-blur-[2px]" onClick={onClose}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
          <motion.aside
            initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }}
            transition={{ type: 'spring', stiffness: 320, damping: 34 }}
            className="fixed right-0 top-0 bottom-0 z-[100] w-[min(420px,100vw)] glass-strong border-l border-white/10 flex flex-col">
            <div className="flex items-center gap-3 px-5 h-16 border-b border-white/[0.06] shrink-0">
              <span className="grid place-items-center w-8 h-8 rounded-lg bg-[var(--accent-soft)] text-[var(--accent)]"><BrainCircuit size={16} /></span>
              <div className="flex-1">
                <p className="text-[14px] font-medium text-white">Memory</p>
                <p className="text-[11px] text-ink-400">What Jarvis remembers about you</p>
              </div>
              <button onClick={onClose} className="p-2 rounded-lg text-ink-400 hover:text-white hover:bg-white/5"><X size={17} /></button>
            </div>

            <div className="p-5 grid grid-cols-3 gap-2 shrink-0">
              <Stat label="Turns" value={stats?.total_turns} />
              <Stat label="Sessions" value={stats?.total_sessions} />
              <Stat label="Vectors" value={stats?.faiss_vectors} />
            </div>

            <div className="px-5 shrink-0">
              <div className="relative flex p-1 rounded-xl bg-white/[0.04] border border-white/[0.06]">
                {[['search', 'Search'], ['add', 'Add memory']].map(([id, label]) => (
                  <button key={id} onClick={() => setTab(id)}
                    className={`relative flex-1 py-1.5 text-[12.5px] rounded-lg transition-colors ${tab === id ? 'text-white' : 'text-ink-400 hover:text-ink-200'}`}>
                    {tab === id && <motion.span layoutId="mem-tab" className="absolute inset-0 rounded-lg bg-white/[0.08] border border-white/10" />}
                    <span className="relative">{label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="flex-1 overflow-y-auto custom-scrollbar p-5">
              {tab === 'search' ? (
                <>
                  <form onSubmit={handleRecall} className="flex gap-2">
                    <div className="flex-1 flex items-center gap-2 px-3 rounded-xl bg-white/[0.04] border border-white/[0.08] focus-within:border-[var(--accent)] transition-colors">
                      <Search size={15} className="text-ink-400" />
                      <input value={query} onChange={e => setQuery(e.target.value)} placeholder="my exam schedule, favourite food…"
                        className="flex-1 bg-transparent py-2.5 text-[13px] outline-none placeholder:text-ink-400" />
                    </div>
                    <button type="submit" disabled={busy || !query.trim()}
                      className="px-3.5 rounded-xl text-[13px] font-medium text-ink-950 bg-[var(--accent)] hover:brightness-110 disabled:opacity-40 transition">
                      {busy ? <Loader2 size={15} className="animate-spin" /> : 'Recall'}
                    </button>
                  </form>
                  {results !== null && (
                    <div className="mt-4 space-y-2">
                      {results.length === 0 && <p className="text-[12.5px] text-ink-400 text-center py-8">Nothing related found.</p>}
                      {results.map((r, i) => (
                        <motion.div key={i} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.03 }}
                          className="p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                          <div className="flex items-center gap-2 text-[11px] text-ink-400 mb-1">
                            <span className={`px-1.5 py-0.5 rounded-md ${r.role === 'user' ? 'bg-sky-400/10 text-sky-300' : 'bg-violet-400/10 text-violet-300'}`}>{r.role === 'user' ? 'You' : 'Jarvis'}</span>
                            <span>{r.timestamp ? new Date(r.timestamp).toLocaleString() : ''}</span>
                            {typeof r.score === 'number' && <span className="ml-auto font-mono">{Math.round(r.score * 100)}%</span>}
                          </div>
                          <p className="text-[12.5px] text-ink-200 leading-relaxed line-clamp-4">{r.content}</p>
                        </motion.div>
                      ))}
                      {results.length > 0 && (
                        <button onClick={handleForget} disabled={busy}
                          className="w-full mt-2 flex items-center justify-center gap-2 py-2 rounded-xl text-[12px] text-rose-300 border border-rose-400/20 hover:bg-rose-400/10 transition-colors">
                          <Eraser size={13} /> Forget memories about “{query.trim()}”
                        </button>
                      )}
                    </div>
                  )}
                </>
              ) : (
                <form onSubmit={handleIngest} className="space-y-3">
                  <textarea rows={7} value={content} onChange={e => setContent(e.target.value)}
                    placeholder="e.g. My exams start on 12 November. I prefer concise answers."
                    className="w-full p-3.5 rounded-xl bg-white/[0.04] border border-white/[0.08] focus:border-[var(--accent)] outline-none text-[13px] leading-relaxed resize-none custom-scrollbar placeholder:text-ink-400 transition-colors" />
                  <button type="submit" disabled={busy || !content.trim()}
                    className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-[13px] font-medium text-ink-950 bg-[var(--accent)] hover:brightness-110 disabled:opacity-40 transition">
                    {busy ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />} Save to memory
                  </button>
                </form>
              )}
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
