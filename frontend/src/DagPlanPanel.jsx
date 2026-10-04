import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { Workflow, ChevronDown, Loader2, Check, X, Clock, SkipForward } from 'lucide-react';

/**
 * DagPlanPanel — live DAG execution graph shown inside the assistant message.
 *
 * Props:
 *   nodes       — array of node objects from the "plan" SSE event
 *   nodeStates  — map of { [nodeId]: { status, result, error } }
 *   summary     — string (plan_summary from planner)
 *   waveCount   — number of execution waves
 *   isComplete  — boolean, true after "done" event
 */
const STATUS = {
  pending: { icon: Clock, label: 'Pending', color: '#6b7186' },
  running: { icon: Loader2, label: 'Running', color: '#fbbf24', spin: true },
  done: { icon: Check, label: 'Done', color: '#34d399' },
  failed: { icon: X, label: 'Failed', color: '#fb7185' },
  skipped: { icon: SkipForward, label: 'Skipped', color: '#6b7186' },
};

const toolIcon = (tool) => {
  const icons = {
    check_emails: '📧', list_unread: '📧', summarize_inbox: '📧', check_emails_tool: '📧',
    get_upcoming_events: '📅', check_today_schedule: '📅', add_event: '📅',
    set_reminder: '⏰', get_info: '🔍', get_morning_brief: '🌅',
    get_system_time: '🕐', get_system_info: '💻', take_screenshot: '📸',
    read_file: '📄', write_file: '📝', create_word_doc: '📝',
    open_app: '🖥️', open_website: '🌐', DYNAMIC: '⚙️', AGGREGATE: '🧠',
  };
  return icons[tool] || '🔧';
};


function NodeCard({ node, wide, nodeStates }) {
  const status = nodeStates[node.id]?.status || 'pending';
  const s = STATUS[status] || STATUS.pending;
  const Icon = s.icon;
  const st = nodeStates[node.id] || {};
  return (
    <motion.div id={`dag-node-${node.id}`} layout
      className={`relative p-3 rounded-xl border bg-white/[0.025] transition-colors ${wide ? '' : 'min-w-0'}`}
      style={{ borderColor: status === 'pending' ? 'rgba(255,255,255,0.07)' : `${s.color}55`, boxShadow: status === 'running' ? `0 0 24px -8px ${s.color}` : 'none' }}>
      <div className="flex items-center gap-2">
        <span className="text-[15px] leading-none">{toolIcon(node.tool)}</span>
        <span className="flex-1 truncate text-[11px] font-mono text-ink-400">
          {node.tool === 'DYNAMIC' ? 'dynamic' : (node.tool || '').replace(/_/g, ' ')}
        </span>
        <span className="flex items-center gap-1 text-[10.5px] font-medium" style={{ color: s.color }}>
          <Icon size={12} className={s.spin ? 'animate-spin' : ''} /> {s.label}
        </span>
      </div>
      <p className="mt-1.5 text-[12.5px] text-ink-200 leading-snug line-clamp-2">{node.description}</p>
      {status === 'done' && st.result && <p className="mt-1.5 text-[11px] text-emerald-300/80 line-clamp-1">{st.result}</p>}
      {status === 'failed' && st.error && <p className="mt-1.5 text-[11px] text-rose-300/80 line-clamp-1">{st.error}</p>}
    </motion.div>
  );
}

export default function DagPlanPanel({ nodes = [], nodeStates = {}, summary = '', waveCount = 0, isComplete = false }) {
  const panelRef = useRef(null);
  // Folds away once everything finished, unless the user toggled it
  const [collapsedPref, setCollapsed] = useState(null);
  const collapsed = collapsedPref ?? isComplete;

  useEffect(() => {
    // Scroll the panel into view when it first appears
    if (nodes.length > 0 && panelRef.current) {
      panelRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [nodes.length]);

  if (nodes.length === 0) return null;

  const planNodes = nodes.filter(n => n.tool !== 'AGGREGATE');
  const aggregateNode = nodes.find(n => n.tool === 'AGGREGATE');

  // Build execution waves from the depends_on graph (topological grouping for display)
  const getDisplayWaves = () => {
    const waves = [];
    const placed = new Set();
    const wave0 = planNodes.filter(n => (n.depends_on || []).length === 0);
    if (wave0.length > 0) { waves.push(wave0); wave0.forEach(n => placed.add(n.id)); }
    let changed = true;
    while (changed) {
      changed = false;
      const next = planNodes.filter(n => !placed.has(n.id) && (n.depends_on || []).every(dep => placed.has(dep)));
      if (next.length > 0) { waves.push(next); next.forEach(n => placed.add(n.id)); changed = true; }
    }
    const remaining = planNodes.filter(n => !placed.has(n.id));
    if (remaining.length > 0) waves.push(remaining);
    return waves;
  };

  const waves = getDisplayWaves();
  const getNodeStatus = (nodeId) => nodeStates[nodeId]?.status || 'pending';

  const doneCount = planNodes.filter(n => getNodeStatus(n.id) === 'done').length;
  const failedCount = planNodes.filter(n => getNodeStatus(n.id) === 'failed').length;
  const progress = planNodes.length ? (doneCount + failedCount) / planNodes.length : 0;

  return (
    <div id="dag-plan-panel" ref={panelRef} className="mb-4 rounded-2xl border border-white/[0.08] bg-white/[0.02] overflow-hidden">
      <button type="button" onClick={() => setCollapsed(!collapsed)} className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-white/[0.02]">
        <span className="grid place-items-center w-8 h-8 rounded-lg bg-[var(--accent-soft)] text-[var(--accent)]"><Workflow size={15} /></span>
        <div className="flex-1 min-w-0">
          <p className="text-[13px] font-medium text-white flex items-center gap-2">
            {isComplete ? 'Plan executed' : 'Executing plan'}
            <span className="text-[11px] font-normal text-ink-400">
              {planNodes.length} tasks · {waveCount || waves.length} wave{(waveCount || waves.length) !== 1 ? 's' : ''}
              {doneCount > 0 && <span className="text-emerald-300"> · {doneCount} done</span>}
              {failedCount > 0 && <span className="text-rose-300"> · {failedCount} failed</span>}
            </span>
          </p>
          {summary && <p className="text-[12px] text-ink-400 truncate">{summary}</p>}
        </div>
        <ChevronDown size={16} className={`text-ink-400 transition-transform ${collapsed ? '' : 'rotate-180'}`} />
      </button>
      <div className="h-[2px] bg-white/[0.04]">
        <motion.div className="h-full" style={{ background: 'linear-gradient(90deg, var(--accent), var(--accent-2))' }}
          animate={{ width: `${(isComplete ? 1 : progress) * 100}%` }} transition={{ type: 'spring', stiffness: 120, damping: 20 }} />
      </div>

      {!collapsed && (
        <div className="p-3 space-y-3">
          {waves.map((wave, waveIdx) => (
            <div key={waveIdx}>
              <div className="flex items-center gap-2 mb-2 px-1">
                <span className="text-[10.5px] uppercase tracking-[0.14em] text-ink-400">
                  Wave {waveIdx + 1}{wave.length > 1 && <span className="text-[var(--accent)]"> · parallel</span>}
                </span>
                <div className="flex-1 h-px bg-white/[0.05]" />
              </div>
              <div className={`grid gap-2 ${wave.length >= 3 ? 'sm:grid-cols-3' : wave.length === 2 ? 'sm:grid-cols-2' : 'grid-cols-1'}`}>
                {wave.map(node => <NodeCard key={node.id} node={node} nodeStates={nodeStates} />)}
              </div>
            </div>
          ))}
          {aggregateNode && <NodeCard node={aggregateNode} nodeStates={nodeStates} wide />}
        </div>
      )}
    </div>
  );
}
