import { useEffect, useRef } from 'react';

/**
 * DagPlanPanel — Live DAG Execution Graph
 * ----------------------------------------
 * Renders a real-time visual of the DAG plan as nodes execute.
 * Styled to match the existing Jarvis sci-fi HUD aesthetic.
 *
 * Props:
 *   nodes       — array of node objects from the "plan" SSE event
 *   nodeStates  — map of { [nodeId]: { status, result, error } }
 *   summary     — string (plan_summary from planner)
 *   waveCount   — number of execution waves
 *   isComplete  — boolean, true after "done" event
 */
export default function DagPlanPanel({ nodes = [], nodeStates = {}, summary = '', waveCount = 0, isComplete = false }) {
  const panelRef = useRef(null);

  useEffect(() => {
    // Scroll the panel into view when it first appears
    if (nodes.length > 0 && panelRef.current) {
      panelRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [nodes.length]);

  if (nodes.length === 0) return null;

  // Group non-aggregate nodes vs aggregate node
  const planNodes = nodes.filter(n => n.tool !== 'AGGREGATE');
  const aggregateNode = nodes.find(n => n.tool === 'AGGREGATE');

  // Build execution waves from depends_on graph (topological grouping for display)
  const getDisplayWaves = () => {
    const waves = [];
    const placed = new Set();

    // Wave 0: nodes with no dependencies
    const wave0 = planNodes.filter(n => n.depends_on.length === 0);
    if (wave0.length > 0) {
      waves.push(wave0);
      wave0.forEach(n => placed.add(n.id));
    }

    // Subsequent waves: nodes whose all deps are placed
    let changed = true;
    while (changed) {
      changed = false;
      const next = planNodes.filter(n =>
        !placed.has(n.id) && n.depends_on.every(dep => placed.has(dep))
      );
      if (next.length > 0) {
        waves.push(next);
        next.forEach(n => placed.add(n.id));
        changed = true;
      }
    }

    // Any remaining (shouldn't happen after cycle detection, but safety net)
    const remaining = planNodes.filter(n => !placed.has(n.id));
    if (remaining.length > 0) waves.push(remaining);

    return waves;
  };

  const waves = getDisplayWaves();

  const getNodeStatus = (nodeId) => nodeStates[nodeId]?.status || 'pending';

  const statusConfig = {
    pending: {
      badge: '⏳ Pending',
      badgeClass: 'text-cyan-500 border-cyan-800 bg-cyan-950/40',
      cardBorder: 'border-cyan-900/50',
      glow: '',
    },
    running: {
      badge: '⚡ Running',
      badgeClass: 'text-yellow-300 border-yellow-600/50 bg-yellow-900/30 animate-pulse',
      cardBorder: 'border-yellow-500/60',
      glow: 'shadow-[0_0_12px_rgba(234,179,8,0.3)]',
    },
    done: {
      badge: '✅ Done',
      badgeClass: 'text-emerald-400 border-emerald-600/50 bg-emerald-900/30',
      cardBorder: 'border-emerald-600/50',
      glow: 'shadow-[0_0_8px_rgba(52,211,153,0.2)]',
    },
    failed: {
      badge: '❌ Failed',
      badgeClass: 'text-red-400 border-red-600/50 bg-red-900/30',
      cardBorder: 'border-red-600/40',
      glow: 'shadow-[0_0_8px_rgba(239,68,68,0.2)]',
    },
    skipped: {
      badge: '⏭ Skipped',
      badgeClass: 'text-gray-500 border-gray-700 bg-gray-900/30',
      cardBorder: 'border-gray-800',
      glow: '',
    },
  };

  const toolIcon = (tool) => {
    const icons = {
      check_emails: '📧', list_unread: '📧', summarize_inbox: '📧', check_emails_tool: '📧',
      get_upcoming_events: '📅', check_today_schedule: '📅', add_event: '📅',
      set_reminder: '⏰',
      get_info: '🔍', get_morning_brief: '🌅',
      get_system_time: '🕐', get_system_info: '💻',
      take_screenshot: '📸',
      read_file: '📄', write_file: '📝', create_word_doc: '📝',
      open_app: '🖥️', open_website: '🌐',
      DYNAMIC: '⚙️',
      AGGREGATE: '🧠',
    };
    return icons[tool] || '🔧';
  };

  const doneCount = planNodes.filter(n => getNodeStatus(n.id) === 'done').length;
  const failedCount = planNodes.filter(n => getNodeStatus(n.id) === 'failed').length;
  const aggStatus = aggregateNode ? getNodeStatus(aggregateNode.id) : 'pending';

  return (
    <div
      id="dag-plan-panel"
      ref={panelRef}
      className="w-full mb-3 rounded-xl border border-cyan-700/60 bg-[#010c18]/90 backdrop-blur-md overflow-hidden shadow-[0_0_30px_rgba(0,243,255,0.08)]"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2.5 border-b border-cyan-900/60 bg-cyan-950/30">
        <div className="flex items-center gap-2">
          <span className="text-cyan-400 text-xs font-mono tracking-widest uppercase">⬡ DAG Executor</span>
          <span className="text-[10px] font-mono text-cyan-600 px-2 py-0.5 border border-cyan-800/50 rounded bg-cyan-950/40">
            {planNodes.length} tasks · {waveCount || waves.length} wave{(waveCount || waves.length) !== 1 ? 's' : ''}
          </span>
        </div>
        <div className="flex items-center gap-2 text-[10px] font-mono">
          {doneCount > 0 && (
            <span className="text-emerald-400">{doneCount} done</span>
          )}
          {failedCount > 0 && (
            <span className="text-red-400">{failedCount} failed</span>
          )}
          {isComplete && (
            <span className="text-cyan-400 animate-pulse">● Complete</span>
          )}
        </div>
      </div>

      {/* Plan Summary */}
      {summary && (
        <div className="px-4 py-2 text-[11px] font-mono text-cyan-400/80 border-b border-cyan-900/40 bg-cyan-950/10 truncate">
          {summary}
        </div>
      )}

      {/* Execution Waves */}
      <div className="p-3 space-y-2">
        {waves.map((wave, waveIdx) => (
          <div key={waveIdx}>
            {/* Wave Label */}
            <div className="flex items-center gap-2 mb-1.5">
              <span className="text-[9px] font-mono text-cyan-700 uppercase tracking-widest">
                Wave {waveIdx + 1}
                {wave.length > 1 && <span className="text-cyan-600 ml-1">· parallel</span>}
              </span>
              <div className="flex-1 h-px bg-cyan-900/40" />
            </div>

            {/* Node Cards */}
            <div className={`grid gap-1.5 ${wave.length >= 3 ? 'grid-cols-3' : wave.length === 2 ? 'grid-cols-2' : 'grid-cols-1'}`}>
              {wave.map((node) => {
                const status = getNodeStatus(node.id);
                const cfg = statusConfig[status] || statusConfig.pending;
                const nodeState = nodeStates[node.id] || {};

                return (
                  <div
                    key={node.id}
                    id={`dag-node-${node.id}`}
                    className={`relative rounded-lg border ${cfg.cardBorder} ${cfg.glow} bg-[#010d1a]/80 p-2.5 transition-all duration-300`}
                  >
                    {/* Running pulse ring */}
                    {status === 'running' && (
                      <div className="absolute inset-0 rounded-lg border border-yellow-500/40 animate-ping pointer-events-none" />
                    )}

                    {/* Top row: icon + tool name + status badge */}
                    <div className="flex items-center justify-between gap-1 mb-1">
                      <div className="flex items-center gap-1.5 min-w-0">
                        <span className="text-base leading-none shrink-0">{toolIcon(node.tool)}</span>
                        <span className="text-[9px] font-mono text-cyan-600 uppercase tracking-wide truncate">
                          {node.tool === 'DYNAMIC' ? 'dynamic' : node.tool.replace(/_/g, ' ')}
                        </span>
                      </div>
                      <span className={`text-[8px] font-mono px-1.5 py-0.5 rounded border shrink-0 ${cfg.badgeClass}`}>
                        {cfg.badge}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-[10px] text-cyan-200/80 font-mono leading-tight line-clamp-2">
                      {node.description}
                    </p>

                    {/* Result preview */}
                    {status === 'done' && nodeState.result && (
                      <div className="mt-1.5 px-2 py-1 bg-emerald-950/30 border border-emerald-800/30 rounded text-[9px] text-emerald-300/70 font-mono line-clamp-1">
                        {nodeState.result}
                      </div>
                    )}

                    {/* Error preview */}
                    {status === 'failed' && nodeState.error && (
                      <div className="mt-1.5 px-2 py-1 bg-red-950/30 border border-red-800/30 rounded text-[9px] text-red-300/70 font-mono line-clamp-1">
                        {nodeState.error}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Arrow between waves */}
            {waveIdx < waves.length - 1 && (
              <div className="flex justify-center mt-1.5">
                <span className="text-cyan-800 text-xs font-mono">↓</span>
              </div>
            )}
          </div>
        ))}

        {/* Aggregate node */}
        {aggregateNode && (
          <>
            <div className="flex justify-center">
              <span className="text-cyan-800 text-xs font-mono">↓</span>
            </div>
            <div
              id={`dag-node-${aggregateNode.id}`}
              className={`rounded-lg border ${(statusConfig[getNodeStatus(aggregateNode.id)] || statusConfig.pending).cardBorder} ${(statusConfig[getNodeStatus(aggregateNode.id)] || statusConfig.pending).glow} bg-[#010d1a]/80 p-2.5 transition-all duration-300`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-base">🧠</span>
                  <span className="text-[10px] font-mono text-cyan-300">
                    {aggregateNode.description || 'Final Summary'}
                  </span>
                </div>
                <span className={`text-[8px] font-mono px-1.5 py-0.5 rounded border ${(statusConfig[aggStatus] || statusConfig.pending).badgeClass}`}>
                  {(statusConfig[aggStatus] || statusConfig.pending).badge}
                </span>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
