import { motion, AnimatePresence } from 'framer-motion';
import {
  SquarePen, PanelLeftClose, Hand, FileUser, BrainCircuit, Ear, Loader2, ExternalLink,
} from 'lucide-react';
import Orb from './Orb';
import { MODES } from '../modes';
import { API_BASE } from '../config';

function Section({ title, children }) {
  return (
    <div className="px-3">
      <p className="px-2 mb-1.5 text-[11px] font-medium uppercase tracking-[0.14em] text-ink-400">{title}</p>
      <div className="space-y-0.5">{children}</div>
    </div>
  );
}

function Item({ icon: Icon, label, active, accent, onClick, href, trailing }) {
  const cls = `group relative w-full flex items-center gap-3 px-2.5 py-2 rounded-xl text-[13.5px] transition-all duration-200 ${
    active ? 'text-white bg-white/[0.07]' : 'text-ink-300 hover:text-white hover:bg-white/[0.04]'
  }`;
  const inner = (
    <>
      {active && (
        <motion.span layoutId="side-active" className="absolute left-0 top-2 bottom-2 w-[3px] rounded-full"
          style={{ background: accent || 'var(--accent)', boxShadow: `0 0 12px ${accent || 'var(--accent)'}` }} />
      )}
      <span className="grid place-items-center w-7 h-7 rounded-lg bg-white/[0.04] border border-white/[0.06] group-hover:border-white/10 transition-colors"
        style={active ? { color: accent, borderColor: `${accent}55`, background: `${accent}14` } : undefined}>
        <Icon size={15} />
      </span>
      <span className="flex-1 text-left truncate">{label}</span>
      {trailing}
    </>
  );
  return href
    ? <a href={href} target="_blank" rel="noopener noreferrer" className={cls}>{inner}</a>
    : <button type="button" onClick={onClick} className={cls}>{inner}</button>;
}

export default function Sidebar({
  open, onClose, modeId, onModeChange, onNewChat, onOpenAirDrawing, onOpenMemory,
  backendOnline, isLoading, tripwire, onTripwireToggle, onTripwireCalibrate,
}) {
  return (
    <>
      <AnimatePresence>
        {open && (
          <motion.div className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm lg:hidden" onClick={onClose}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
        )}
      </AnimatePresence>

      <motion.aside
        initial={false}
        animate={{ width: open ? 272 : 0, opacity: open ? 1 : 0 }}
        transition={{ type: 'spring', stiffness: 320, damping: 34 }}
        className="fixed lg:relative z-50 h-full shrink-0 overflow-hidden border-r border-white/[0.06] bg-ink-900/80 backdrop-blur-2xl"
      >
        <div className="w-[272px] h-full flex flex-col">
          {/* Brand */}
          <div className="flex items-center gap-3 px-5 h-16 shrink-0">
            <Orb size={30} busy={isLoading} />
            <div className="flex-1 leading-tight">
              <p className="text-[15px] font-semibold tracking-[0.18em] text-white">JARVIS</p>
              <p className="text-[11px] text-ink-400 flex items-center gap-1.5">
                <span className={`w-1.5 h-1.5 rounded-full ${backendOnline ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]' : 'bg-rose-500'}`} />
                {backendOnline ? 'All systems online' : 'Backend offline'}
              </p>
            </div>
            <button onClick={onClose} className="p-2 rounded-lg text-ink-400 hover:text-white hover:bg-white/5 transition-colors" title="Hide sidebar">
              <PanelLeftClose size={17} />
            </button>
          </div>

          <div className="px-3 pb-3">
            <button onClick={onNewChat}
              className="w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-[13.5px] font-medium text-white bg-white/[0.06] border border-white/[0.08] hover:bg-white/[0.1] hover:border-white/[0.14] transition-all shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]">
              <SquarePen size={16} /> New chat
              <kbd className="ml-auto text-[10px] font-mono text-ink-400 border border-white/10 rounded px-1.5 py-0.5">Ctrl ⇧ O</kbd>
            </button>
          </div>

          <div className="flex-1 overflow-y-auto custom-scrollbar space-y-6 py-2">
            <Section title="Modes">
              {MODES.map(m => (
                <Item key={m.id} icon={m.icon} label={m.label} accent={m.accent}
                  active={modeId === m.id} onClick={() => onModeChange(m.id)} />
              ))}
            </Section>

            <Section title="Studio">
              <Item icon={Hand} label="Air Drawing" onClick={onOpenAirDrawing} />
              <Item icon={BrainCircuit} label="Memory" onClick={onOpenMemory} />
              <Item icon={FileUser} label="Resume editor" href={`${API_BASE}/resume/editor`}
                trailing={<ExternalLink size={13} className="text-ink-400" />} />
            </Section>

            {/* Acoustic tripwire (double clap wake) */}
            <Section title="Acoustic wake">
              <div className="mx-0.5 p-3 rounded-2xl bg-white/[0.03] border border-white/[0.06]">
                <div className="flex items-center gap-3">
                  <span className={`grid place-items-center w-8 h-8 rounded-lg border ${tripwire.enabled ? 'text-emerald-300 border-emerald-400/30 bg-emerald-400/10' : 'text-ink-300 border-white/10 bg-white/[0.04]'}`}>
                    <Ear size={15} />
                  </span>
                  <div className="flex-1 leading-tight">
                    <p className="text-[13px] text-white">Double-clap wake</p>
                    <p className="text-[11px] text-ink-400">
                      {tripwire.running ? (tripwire.enabled ? 'Armed — clap twice' : 'Standby') : 'Offline'}
                      {tripwire.threshold ? ` · thr ${tripwire.threshold}` : ''}
                    </p>
                  </div>
                  <button id="tripwire-toggle-btn" onClick={onTripwireToggle} role="switch" aria-checked={tripwire.enabled}
                    title={tripwire.enabled ? 'Disarm acoustic tripwire' : 'Arm acoustic tripwire'}
                    className={`relative h-6 w-11 rounded-full transition-colors duration-300 border ${tripwire.enabled ? 'bg-emerald-500/80 border-emerald-300/40' : 'bg-white/10 border-white/10'}`}>
                    <motion.span layout transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                      className={`absolute top-0.5 w-[18px] h-[18px] rounded-full bg-white shadow ${tripwire.enabled ? 'right-0.5' : 'left-0.5'}`} />
                  </button>
                </div>
                <button id="tripwire-calibrate-btn" onClick={onTripwireCalibrate}
                  disabled={tripwire.calibrating || !tripwire.running}
                  className="mt-3 w-full flex items-center justify-center gap-2 py-1.5 rounded-lg text-[12px] text-ink-300 border border-white/[0.08] hover:text-white hover:bg-white/5 transition-colors disabled:opacity-35 disabled:cursor-not-allowed">
                  {tripwire.calibrating ? <><Loader2 size={13} className="animate-spin" /> Calibrating…</> : 'Recalibrate noise floor'}
                </button>
              </div>
            </Section>
          </div>

          <div className="px-5 py-4 text-[11px] text-ink-400 border-t border-white/[0.05] flex items-center justify-between">
            <span>Groq · gpt-oss</span>
            <span className="font-mono">v2.0</span>
          </div>
        </div>
      </motion.aside>
    </>
  );
}
