import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Plus, ArrowUp, Square, Mic, X, Check, ChevronDown, SlidersHorizontal, Loader2, FileText, ExternalLink, ChevronRight,
} from 'lucide-react';
import { MODES, MODE_BY_ID, KIND_LABEL, isImage } from '../modes';
import { API_BASE } from '../config';

// Small popover with click-outside / Escape to close
function Popover({ open, onClose, children, align = 'left', width = 300 }) {
  const ref = useRef(null);
  useEffect(() => {
    if (!open) return;
    // The parent wrapper also holds the trigger button, so clicking the trigger toggles instead of close+reopen
    const onDown = (e) => { const box = ref.current?.parentElement; if (box && !box.contains(e.target)) onClose(); };
    const onKey = (e) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => { document.removeEventListener('mousedown', onDown); document.removeEventListener('keydown', onKey); };
  }, [open, onClose]);
  return (
    <AnimatePresence>
      {open && (
        <motion.div ref={ref}
          initial={{ opacity: 0, y: 8, scale: 0.97 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 6, scale: 0.98 }}
          transition={{ duration: 0.16, ease: 'easeOut' }}
          style={{ width }}
          className={`absolute bottom-full mb-3 z-50 menu-surface rounded-2xl p-1.5 origin-bottom ${align === 'right' ? 'right-0' : 'left-0'}`}>
          {children}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function MenuItem({ icon: Icon, label, hint, onClick, accent, right, href }) {
  const cls = 'w-full flex items-start gap-3 px-3 py-2.5 rounded-xl text-left hover:bg-white/[0.06] transition-colors group';
  const body = (
    <>
      <span className="mt-0.5 grid place-items-center w-8 h-8 shrink-0 rounded-lg border border-white/[0.08] bg-white/[0.04] text-ink-200 group-hover:text-white"
        style={accent ? { color: accent, borderColor: `${accent}40`, background: `${accent}12` } : undefined}>
        <Icon size={15} />
      </span>
      <span className="flex-1 min-w-0">
        <span className="block text-[13px] text-white">{label}</span>
        {hint && <span className="block text-[11.5px] text-ink-400 leading-snug">{hint}</span>}
      </span>
      {right}
    </>
  );
  return href
    ? <a href={href} target="_blank" rel="noopener noreferrer" className={cls}>{body}</a>
    : <button type="button" onClick={onClick} className={cls}>{body}</button>;
}

function OptionPill({ option, value, onChange }) {
  const [open, setOpen] = useState(false);
  const current = option.choices.find(c => c[0] === (value || '')) || option.choices[0];
  const Icon = option.icon;
  const active = !!value;
  return (
    <div className="relative">
      <button type="button" onClick={() => setOpen(o => !o)}
        className={`flex items-center gap-1.5 h-8 px-2.5 rounded-full text-[12.5px] border transition-colors ${
          active ? 'text-white border-[var(--accent)]/40 bg-[var(--accent-soft)]' : 'text-ink-300 border-white/[0.08] hover:text-white hover:bg-white/[0.05]'}`}>
        <Icon size={13} className={active ? 'text-[var(--accent)]' : ''} />
        <span className="max-w-[120px] truncate">{current[1]}</span>
        <ChevronDown size={13} className={`transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      <Popover open={open} onClose={() => setOpen(false)} width={220}>
        <p className="px-3 pt-2 pb-1 text-[11px] uppercase tracking-[0.12em] text-ink-400">{option.label}</p>
        <div className="max-h-72 overflow-y-auto custom-scrollbar">
          {option.choices.map(([v, label]) => (
            <button key={v || 'auto'} type="button" onClick={() => { onChange(v); setOpen(false); }}
              className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-[13px] text-ink-200 hover:text-white hover:bg-white/[0.06]">
              {label}
              {(value || '') === v && <Check size={14} className="text-[var(--accent)]" />}
            </button>
          ))}
        </div>
      </Popover>
    </div>
  );
}

function AttachmentChip({ a, describable, onRemove, onDescribe }) {
  const img = isImage(a.name) && a.url;
  return (
    <motion.div layout initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }}
      className="relative group shrink-0 flex items-center gap-2.5 p-1.5 pr-3 rounded-2xl bg-white/[0.04] border border-white/[0.08]">
      <div className="relative w-12 h-12 rounded-xl overflow-hidden bg-white/[0.04] grid place-items-center">
        {img ? <img src={a.url} alt={a.name} className="w-full h-full object-cover" /> : <FileText size={18} className="text-ink-300" />}
        {a.uploading && <div className="absolute inset-0 grid place-items-center bg-black/60"><Loader2 size={16} className="animate-spin text-white" /></div>}
      </div>
      <div className="min-w-0 max-w-[180px]">
        <p className="text-[12.5px] text-white truncate">{a.name}</p>
        {describable && img && !a.uploading ? (
          <input value={a.description || ''} onChange={e => onDescribe(a.id, e.target.value)} placeholder="Add a caption…"
            className="w-full bg-transparent text-[11.5px] text-ink-200 outline-none placeholder:text-ink-400" />
        ) : (
          <p className="text-[11px] text-ink-400 truncate">
            {a.uploading ? 'Uploading…' : (KIND_LABEL[a.kind] || (a.name.split('.').pop() || '').toUpperCase())}
          </p>
        )}
      </div>
      {KIND_LABEL[a.kind] && !a.uploading && (
        <span className="absolute -top-2 left-2 px-1.5 py-[1px] rounded-md text-[9.5px] font-medium uppercase tracking-wider bg-[var(--accent)] text-ink-950">
          {KIND_LABEL[a.kind]}
        </span>
      )}
      <button type="button" onClick={() => onRemove(a.id)}
        className="absolute -top-2 -right-2 w-5 h-5 grid place-items-center rounded-full bg-ink-700 border border-white/15 text-ink-200 hover:bg-rose-500 hover:text-white transition-colors opacity-0 group-hover:opacity-100">
        <X size={11} />
      </button>
    </motion.div>
  );
}

export default function Composer({
  mode, onModeChange, value, onChange, onSubmit, onStop, isLoading,
  attachments, onFiles, onRemoveAttachment, onDescribe,
  options, onOptionChange, speech, suggestedMode, textareaRef,
}) {
  const [menu, setMenu] = useState(null); // 'upload' | 'modes' | null
  const fileRef = useRef(null);
  const pendingKind = useRef('general');

  const uploading = attachments.some(a => a.uploading);
  const canSend = !isLoading && !uploading && (value.trim() || attachments.length > 0);
  const ModeIcon = mode.icon;
  const describeKinds = new Set(mode.uploads.filter(u => u.describe).map(u => u.kind));

  // Auto-grow the textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 220) + 'px';
  }, [value, textareaRef]);

  const pickUpload = (u) => {
    setMenu(null);
    pendingKind.current = u.kind;
    const input = fileRef.current;
    input.accept = u.accept;
    input.multiple = !!u.multiple;
    input.click();
  };

  const submit = (e) => { e.preventDefault(); if (canSend) onSubmit(); };

  return (
    <div className="w-full">
      <AnimatePresence>
        {suggestedMode && (
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 8 }}
            className="mb-2 mx-auto w-fit flex items-center gap-2 pl-3 pr-1.5 py-1.5 rounded-full glass-strong text-[12.5px] text-ink-200">
            {(() => { const S = MODE_BY_ID[suggestedMode]; const I = S.icon; return (<>
              <I size={14} style={{ color: S.accent }} />
              <span>Looks like a job for <b className="text-white font-medium">{S.label}</b></span>
              <button type="button" onClick={() => onModeChange(S.id)}
                className="ml-1 px-2.5 py-1 rounded-full text-[12px] font-medium text-ink-950 hover:brightness-110" style={{ background: S.accent }}>
                Switch
              </button>
            </>); })()}
          </motion.div>
        )}
      </AnimatePresence>

      <form onSubmit={submit}
        className="ring-gradient relative rounded-[26px] glass-strong transition-shadow focus-within:shadow-[0_0_0_4px_var(--accent-soft),0_24px_60px_-20px_rgba(0,0,0,0.7)]">
        {/* Attachments */}
        <AnimatePresence initial={false}>
          {attachments.length > 0 && (
            <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden">
              <div className="flex gap-3 px-3 pt-4 pb-1 overflow-x-auto custom-scrollbar">
                <AnimatePresence initial={false}>
                  {attachments.map(a => (
                    <AttachmentChip key={a.id} a={a} describable={describeKinds.has(a.kind)} onRemove={onRemoveAttachment} onDescribe={onDescribe} />
                  ))}
                </AnimatePresence>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <textarea
          id="jarvis-command-input"
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={e => onChange(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); if (canSend) onSubmit(); }
          }}
          placeholder={speech.listening ? 'Listening…' : mode.placeholder}
          className="block w-full bg-transparent resize-none outline-none px-5 pt-4 pb-2 text-[15px] leading-relaxed text-white placeholder:text-ink-400 custom-scrollbar max-h-[220px]"
          autoFocus
        />

        <div className="flex items-center gap-1.5 px-2.5 pb-2.5 pt-1">
          {/* + uploads */}
          {mode.uploads.length > 0 && (
            <div className="relative">
              <button type="button" onClick={() => setMenu(m => m === 'upload' ? null : 'upload')} title="Add files"
                className={`grid place-items-center w-9 h-9 rounded-full border transition-all ${menu === 'upload' ? 'bg-white/10 border-white/15 text-white rotate-45' : 'border-white/[0.08] text-ink-200 hover:text-white hover:bg-white/[0.06]'}`}>
                <Plus size={18} />
              </button>
              <Popover open={menu === 'upload'} onClose={() => setMenu(null)} width={320}>
                <p className="px-3 pt-2 pb-1 text-[11px] uppercase tracking-[0.12em] text-ink-400">
                  {mode.id === 'chat' ? 'Attach' : `${mode.label} inputs`}
                </p>
                {mode.uploads.map(u => {
                  const added = u.single && attachments.some(a => a.kind === u.kind);
                  return (
                    <MenuItem key={u.kind} icon={u.icon} label={u.label} hint={u.hint} accent={mode.id === 'chat' ? undefined : mode.accent}
                      onClick={() => pickUpload(u)}
                      right={added ? <span className="mt-1 text-[10.5px] text-emerald-300 flex items-center gap-1"><Check size={12} /> Added</span> : null} />
                  );
                })}
                {(mode.links || []).map(l => (
                  <MenuItem key={l.path} icon={ExternalLink} label={l.label} hint="Opens in a new tab" href={`${API_BASE}${l.path}`} onClick={() => setMenu(null)} />
                ))}
                {mode.id === 'chat' && (
                  <>
                    <div className="my-1.5 mx-3 h-px bg-white/[0.06]" />
                    <p className="px-3 pt-1 pb-1 text-[11px] uppercase tracking-[0.12em] text-ink-400">Need resume or slide inputs?</p>
                    {MODES.filter(m => m.uploads.length && m.id !== 'chat').map(m => (
                      <MenuItem key={m.id} icon={m.icon} label={m.label} hint={m.uploads.map(u => u.label).join(' · ')} accent={m.accent}
                        onClick={() => { setMenu(null); onModeChange(m.id); }} right={<ChevronRight size={14} className="mt-2 text-ink-400" />} />
                    ))}
                  </>
                )}
              </Popover>
            </div>
          )}

          {/* Mode: "Tools" button in chat, removable chip otherwise */}
          <div className="relative">
            {mode.id === 'chat' ? (
              <button type="button" onClick={() => setMenu(m => m === 'modes' ? null : 'modes')}
                className={`flex items-center gap-2 h-9 px-3 rounded-full text-[13px] border transition-colors ${menu === 'modes' ? 'bg-white/10 border-white/15 text-white' : 'border-white/[0.08] text-ink-200 hover:text-white hover:bg-white/[0.06]'}`}>
                <SlidersHorizontal size={15} /> Tools
              </button>
            ) : (
              <motion.div layout initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
                className="flex items-center h-9 rounded-full border text-[13px] font-medium overflow-hidden"
                style={{ color: mode.accent, borderColor: `${mode.accent}45`, background: `${mode.accent}14` }}>
                <button type="button" onClick={() => setMenu(m => m === 'modes' ? null : 'modes')} className="flex items-center gap-2 pl-3 pr-1.5 h-full hover:brightness-125">
                  <ModeIcon size={15} /> <span className="hidden sm:inline">{mode.label}</span>
                </button>
                <button type="button" title="Exit mode" onClick={() => onModeChange('chat')} className="grid place-items-center w-7 h-full pr-1 hover:brightness-150">
                  <X size={14} />
                </button>
              </motion.div>
            )}
            <Popover open={menu === 'modes'} onClose={() => setMenu(null)} width={330}>
              <p className="px-3 pt-2 pb-1 text-[11px] uppercase tracking-[0.12em] text-ink-400">Modes</p>
              {MODES.map(m => (
                <MenuItem key={m.id} icon={m.icon} label={m.label} hint={m.tagline} accent={m.accent}
                  onClick={() => { setMenu(null); onModeChange(m.id); }}
                  right={m.id === mode.id ? <Check size={15} className="mt-2" style={{ color: m.accent }} /> : null} />
              ))}
            </Popover>
          </div>

          {/* Mode options */}
          <div className="hidden md:flex items-center gap-1.5 min-w-0">
            {mode.options.map(o => (
              <OptionPill key={o.key} option={o} value={options[o.key]} onChange={v => onOptionChange(o.key, v)} />
            ))}
          </div>

          <div className="flex-1" />

          {speech.supported && (
            <button type="button" onClick={speech.toggle} title={speech.listening ? 'Stop dictation' : 'Dictate'}
              className={`relative grid place-items-center w-9 h-9 rounded-full transition-colors ${speech.listening ? 'text-rose-300 bg-rose-500/15' : 'text-ink-300 hover:text-white hover:bg-white/[0.06]'}`}>
              {speech.listening
                ? <span className="voice-bars flex items-center gap-[2px] h-4"><span /><span /><span /><span /></span>
                : <Mic size={17} />}
              {speech.listening && <span className="absolute inset-0 rounded-full border border-rose-400/40 animate-ping" />}
            </button>
          )}

          {isLoading ? (
            <button type="button" onClick={onStop} title="Stop"
              className="grid place-items-center w-9 h-9 rounded-full bg-white text-ink-950 hover:bg-ink-200 transition-colors">
              <Square size={13} fill="currentColor" />
            </button>
          ) : (
            <motion.button id="jarvis-send-btn" type="submit" disabled={!canSend} whileTap={{ scale: 0.92 }} title="Send (Enter)"
              className="grid place-items-center w-9 h-9 rounded-full transition-all disabled:opacity-30 disabled:cursor-not-allowed text-ink-950"
              style={{ background: canSend ? 'linear-gradient(135deg, var(--accent), var(--accent-2))' : 'rgba(255,255,255,0.15)', boxShadow: canSend ? '0 6px 20px -6px var(--accent)' : 'none' }}>
              {uploading ? <Loader2 size={16} className="animate-spin" /> : <ArrowUp size={18} strokeWidth={2.4} />}
            </motion.button>
          )}
        </div>

        {/* Mode options on small screens */}
        {mode.options.length > 0 && (
          <div className="md:hidden flex flex-wrap gap-1.5 px-3 pb-3">
            {mode.options.map(o => (
              <OptionPill key={o.key} option={o} value={options[o.key]} onChange={v => onOptionChange(o.key, v)} />
            ))}
          </div>
        )}

        <input ref={fileRef} type="file" className="hidden"
          onChange={e => { onFiles(Array.from(e.target.files || []), pendingKind.current); e.target.value = ''; }} />
      </form>

      <p className="mt-2.5 text-center text-[11px] text-ink-400">
        <kbd className="font-mono">Enter</kbd> to send · <kbd className="font-mono">Shift + Enter</kbd> new line · drop or paste files anywhere
      </p>
    </div>
  );
}
