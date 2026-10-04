import { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PanelLeftOpen, BrainCircuit, Hand, SquarePen, ArrowDown, Upload, X } from 'lucide-react';
import ChatMessage from './ChatMessage';
import AirDrawingApp from './AirDrawing/AirDrawingApp';
import Sidebar from './components/Sidebar';
import Composer from './components/Composer';
import EmptyState from './components/EmptyState';
import MemoryPanel from './components/MemoryPanel';
import Toasts from './components/Toasts';
import Orb from './components/Orb';
import { MODE_BY_ID, KIND_LABEL, buildRequest, kindForFile, suggestMode } from './modes';
import { API_BASE } from './config';

// ── localStorage helpers (UI convenience only; the backend keeps its own history) ──
const LS = 'jarvis.ui.v2';
const load = () => { try { return JSON.parse(localStorage.getItem(LS)) || {}; } catch { return {}; } };
const save = (patch) => { try { localStorage.setItem(LS, JSON.stringify({ ...load(), ...patch })); } catch { /* storage blocked */ } };
const uid = () => Math.random().toString(36).slice(2, 10);

// Browser dictation (Chrome / Edge Web Speech API)
function useSpeech(onText) {
  const [listening, setListening] = useState(false);
  const recRef = useRef(null);
  const SR = typeof window !== 'undefined' ? (window.SpeechRecognition || window.webkitSpeechRecognition) : null;
  const toggle = () => {
    if (listening) { recRef.current?.stop(); return; }
    try {
      const rec = new SR();
      rec.continuous = true;
      rec.interimResults = true;
      rec.lang = navigator.language || 'en-US';
      rec.onresult = (e) => {
        let t = '';
        for (let i = 0; i < e.results.length; i++) t += e.results[i][0].transcript;
        onText(t, false);
      };
      rec.onend = () => { setListening(false); onText(null, true); };
      rec.onerror = () => setListening(false);
      onText(null, false, true);
      rec.start();
      recRef.current = rec;
      setListening(true);
    } catch { setListening(false); }
  };
  return { supported: !!SR, listening, toggle };
}

function App() {
  const stored = useRef(load()).current;
  const [messages, setMessages] = useState(stored.messages || []);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [modeId, setModeId] = useState(MODE_BY_ID[stored.modeId] ? stored.modeId : 'chat');
  const [modeOptions, setModeOptions] = useState(stored.modeOptions || {});
  const [attachments, setAttachments] = useState([]);
  const [hasDeck, setHasDeck] = useState(!!stored.hasDeck);
  const [sidebarOpen, setSidebarOpen] = useState(() => (typeof window !== 'undefined' ? window.innerWidth >= 1024 : true));
  const [memoryOpen, setMemoryOpen] = useState(false);
  const [isAirDrawingOpen, setIsAirDrawingOpen] = useState(false);
  const [backendOnline, setBackendOnline] = useState(true);
  const [toasts, setToasts] = useState([]);
  const [dragging, setDragging] = useState(false);
  const [atBottom, setAtBottom] = useState(true);

  const mode = MODE_BY_ID[modeId];
  const options = modeOptions[modeId] || {};

  const textareaRef = useRef(null);
  const scrollRef = useRef(null);
  const abortRef = useRef(null);
  const dictationBase = useRef('');

  // ── Toasts ──────────────────────────────────────────────────────────────
  const notify = useCallback((t) => {
    const id = uid();
    setToasts(prev => [...prev.slice(-3), { id, ...t }]);
    setTimeout(() => setToasts(prev => prev.filter(x => x.id !== id)), t.type === 'alert' ? 12000 : 4500);
  }, []);
  const dismissToast = (id) => setToasts(prev => prev.filter(x => x.id !== id));

  // ── Mode accent colours drive the whole theme (CSS variables) ──────────
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty('--accent', mode.accent);
    root.style.setProperty('--accent-2', mode.accent2);
    root.style.setProperty('--accent-soft', `${mode.accent}24`);
  }, [mode]);

  // ── Persist UI state ────────────────────────────────────────────────────
  useEffect(() => { save({ modeId, modeOptions, hasDeck }); }, [modeId, modeOptions, hasDeck]);
  useEffect(() => {
    if (isLoading) return;
    save({
      messages: messages.slice(-60).map(m => ({
        ...m,
        attachedFiles: m.attachedFiles?.map(f => ({ name: f.name, label: f.label, description: f.description })),
      })),
    });
  }, [messages, isLoading]);

  // ── Acoustic Tripwire state (+ backend heartbeat) ──────────────────────
  const [tripwireEnabled, setTripwireEnabled] = useState(false);
  const [tripwireRunning, setTripwireRunning] = useState(false);
  const [tripwireCalibrating, setTripwireCalibrating] = useState(false);
  const [tripwireThreshold, setTripwireThreshold] = useState(null);

  useEffect(() => {
    const fetchTripwireStatus = async () => {
      try {
        const res = await fetch(`${API_BASE}/tripwire/status`);
        setBackendOnline(res.ok);
        if (res.ok) {
          const data = await res.json();
          setTripwireEnabled(data.enabled ?? false);
          setTripwireRunning(data.running ?? false);
          if (data.volume_threshold) setTripwireThreshold(data.volume_threshold);
        }
      } catch { setBackendOnline(false); }
    };
    fetchTripwireStatus();
    const id = setInterval(fetchTripwireStatus, 5000);
    return () => clearInterval(id);
  }, []);

  const handleTripwireToggle = async () => {
    const endpoint = tripwireEnabled ? '/tripwire/disable' : '/tripwire/enable';
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        if (data.status === 'ok') {
          setTripwireEnabled(!tripwireEnabled);
          notify({ type: 'success', text: tripwireEnabled ? 'Acoustic wake disarmed.' : 'Acoustic wake armed — clap twice to wake Jarvis.' });
        } else notify({ type: 'error', text: data.message || 'Tripwire is not available.' });
      }
    } catch (err) { notify({ type: 'error', title: 'Tripwire', text: err.message }); }
  };

  const handleTripwireCalibrate = async () => {
    setTripwireCalibrating(true);
    try {
      await fetch(`${API_BASE}/tripwire/calibrate`, { method: 'POST' });
      // Calibration takes ~2.5 s, then refresh the threshold
      setTimeout(async () => {
        try {
          const res = await fetch(`${API_BASE}/tripwire/status`);
          if (res.ok) {
            const d = await res.json();
            if (d.volume_threshold) setTripwireThreshold(d.volume_threshold);
          }
        } catch { /* ignore */ }
        setTripwireCalibrating(false);
        notify({ type: 'success', text: 'Noise floor recalibrated.' });
      }, 2500);
    } catch (err) {
      console.error('[Tripwire] calibrate error:', err);
      setTripwireCalibrating(false);
    }
  };

  // ── Proactive screen-watcher alerts (/alerts) → toasts ─────────────────
  useEffect(() => {
    const id = setInterval(async () => {
      try {
        const res = await fetch(`${API_BASE}/alerts?clear=true`);
        if (!res.ok) return;
        const { alerts = [] } = await res.json();
        alerts.forEach(a => notify({ type: 'alert', title: 'Jarvis noticed', text: typeof a === 'string' ? a : JSON.stringify(a) }));
      } catch { /* offline */ }
    }, 6000);
    return () => clearInterval(id);
  }, [notify]);

  // ── [OPEN_AIR_DRAWING] marker in a reply opens the overlay ─────────────
  useEffect(() => {
    const last = messages[messages.length - 1];
    if (last?.role === 'assistant' && last.content.includes('[OPEN_AIR_DRAWING]')) {
      setIsAirDrawingOpen(true);
      setMessages(prev => prev.map((m, i) => i === prev.length - 1 ? { ...m, content: m.content.replace('[OPEN_AIR_DRAWING]', '').trim() } : m));
    }
  }, [messages]);

  // ── Scrolling: stick to the bottom while the user is there ─────────────
  const onScroll = () => {
    const el = scrollRef.current;
    if (el) setAtBottom(el.scrollHeight - el.scrollTop - el.clientHeight < 80);
  };
  const scrollToBottom = (smooth = true) => {
    const el = scrollRef.current;
    if (el) el.scrollTo({ top: el.scrollHeight, behavior: smooth ? 'smooth' : 'auto' });
  };
  useEffect(() => { if (atBottom) scrollToBottom(false); }, [messages]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Message helpers ────────────────────────────────────────────────────
  const patchLast = (fn) => setMessages(prev => {
    const i = prev.length - 1;
    if (i < 0 || prev[i].role !== 'assistant') return prev;
    const copy = prev.slice();
    copy[i] = fn({ ...prev[i] });
    return copy;
  });
  const appendMsg = (chunk) => patchLast(m => ({ ...m, content: m.content + chunk }));

  // ── DAG Event Handler (state lives on the assistant message) ───────────
  const handleDagEvent = (evt) => {
    const dag = (m) => m.dag || { plan: null, nodeStates: {}, complete: false };
    const setNode = (id, patch) => patchLast(m => {
      const d = dag(m);
      return { ...m, dag: { ...d, nodeStates: { ...d.nodeStates, [id]: { ...(d.nodeStates[id] || {}), ...patch } } } };
    });
    switch (evt.type) {
      case 'plan':
        patchLast(m => ({
          ...m,
          dag: {
            plan: { nodes: evt.nodes || [], summary: evt.summary || '', waveCount: evt.wave_count || 0 },
            nodeStates: Object.fromEntries((evt.nodes || []).map(n => [n.id, { status: 'pending', result: '', error: '' }])),
            complete: false,
          },
        }));
        break;
      case 'node_start': setNode(evt.id, { status: 'running' }); break;
      case 'node_done': setNode(evt.id, { status: 'done', result: evt.result || '' }); break;
      case 'node_failed': setNode(evt.id, { status: 'failed', error: evt.error || '' }); break;
      case 'aggregate': patchLast(m => ({ ...m, content: evt.text || m.content })); break;
      case 'narration':
      case 'fallback':
        if (evt.text) patchLast(m => ({ ...m, content: m.content + (m.content ? ' ' : '') + evt.text }));
        break;
      case 'done': patchLast(m => ({ ...m, dag: { ...dag(m), complete: true } })); break;
      default: break;
    }
  };

  // ── Streaming request runner (/chat or /ppt/create) ────────────────────
  const runRequest = async ({ route, body }) => {
    setIsLoading(true);
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    try {
      const url = route === 'ppt' ? `${API_BASE}/ppt/create` : `${API_BASE}/chat`;
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: ctrl.signal,
      });
      if (!response.ok) throw new Error(`Server returned ${response.status}`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      // DAG responses start with 'data: {' (structured SSE events); everything else is plain text
      let isDagStream = route === 'ppt' ? false : null;
      let dagBuffer = '';
      let streamed = '';
      const flushDag = (part) => {
        const line = part.replace(/^data:\s*/, '').trim();
        if (!line || line === '[DONE]') return;
        try {
          const evt = JSON.parse(line);
          if (evt && typeof evt.type === 'string') handleDagEvent(evt);
        } catch { /* malformed DAG event */ }
      };

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        if (!chunk) continue;
        if (isDagStream === null) isDagStream = chunk.trimStart().startsWith('data: {');

        if (isDagStream) {
          dagBuffer += chunk;
          const parts = dagBuffer.split('\n\n');
          dagBuffer = parts.pop();
          parts.forEach(flushDag);
        } else {
          const text = chunk.replace(/^data:\s*/gm, '').replace(/\[DONE\]/g, '');
          if (text) { streamed += text; appendMsg(text); }
        }
      }
      if (dagBuffer.trim()) flushDag(dagBuffer);
      // A finished deck enables follow-up edits ("change slide 2 title") via /chat → ppt_edit
      if (route === 'ppt' || /\.pptx\b/i.test(streamed)) setHasDeck(true);
    } catch (err) {
      if (err.name === 'AbortError') {
        patchLast(m => ({ ...m, content: m.content + (m.content ? '\n\n' : '') + '_Stopped._' }));
      } else {
        console.error('[Jarvis] fetch error:', err);
        patchLast(m => ({ ...m, content: m.content + `\n\n⚠️ Could not complete request: ${err.message}. Make sure the backend is running at ${API_BASE}.` }));
      }
    } finally {
      abortRef.current = null;
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (overrideText) => {
    const prompt = (typeof overrideText === 'string' ? overrideText : inputValue).trim();
    if ((!prompt && attachments.length === 0) || isLoading || attachments.some(a => a.uploading)) return;

    const req = buildRequest({ modeId, prompt, attachments, options, hasDeck });
    const attachedFiles = attachments.map(a => ({ name: a.name, url: a.url, description: a.description, label: KIND_LABEL[a.kind] }));
    const head = req.route === 'ppt' && req.themeName ? `🎨 Using your reference theme: ${req.themeName}\n\n` : '';

    setMessages(prev => [
      ...prev,
      { id: uid(), role: 'user', content: req.display, attachedFiles, mode: modeId },
      { id: uid(), role: 'assistant', content: head, mode: modeId, note: req.note, request: { route: req.route, body: req.body } },
    ]);
    setInputValue('');
    setAttachments([]);
    setAtBottom(true);
    await runRequest(req);
  };

  const handleRegenerate = () => {
    const last = messages[messages.length - 1];
    if (isLoading || last?.role !== 'assistant' || !last.request) return;
    patchLast(m => ({ ...m, content: '', dag: undefined }));
    runRequest(last.request);
  };

  const handleStop = () => abortRef.current?.abort();

  const handleNewChat = async () => {
    abortRef.current?.abort();
    setMessages([]);
    setAttachments([]);
    setInputValue('');
    save({ messages: [] });
    try { await fetch(`${API_BASE}/chat/history`, { method: 'DELETE' }); } catch { /* offline */ }
    textareaRef.current?.focus();
  };

  // ── Modes ──────────────────────────────────────────────────────────────
  const handleModeChange = (id) => {
    const next = MODE_BY_ID[id];
    const allowed = new Set([...next.uploads.map(u => u.kind), 'general']);
    setAttachments(prev => prev.filter(a => allowed.has(a.kind)));
    setModeId(id);
    if (window.innerWidth < 1024) setSidebarOpen(false);
    setTimeout(() => textareaRef.current?.focus(), 50);
  };
  const setOption = (key, value) => setModeOptions(prev => ({ ...prev, [modeId]: { ...(prev[modeId] || {}), [key]: value } }));

  // ── Uploads (+ menu, drag & drop, paste) ───────────────────────────────
  const handleFileUpload = async (files, kind) => {
    const def = mode.uploads.find(u => u.kind === kind);
    const list = def?.single ? files.slice(0, 1) : files;
    for (const file of list) {
      const id = uid();
      const att = { id, kind, name: file.name, url: URL.createObjectURL(file), uploading: true, description: '' };
      setAttachments(prev => [...(def?.single ? prev.filter(a => a.kind !== kind) : prev), att]);
      const formData = new FormData();
      formData.append('file', file);
      try {
        const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
        const data = await res.json();
        if (data.status !== 'success') throw new Error(data.error || 'upload failed');
        setAttachments(prev => prev.map(a => a.id === id ? { ...a, path: data.path, filename: data.filename, uploading: false } : a));
      } catch (err) {
        setAttachments(prev => prev.filter(a => a.id !== id));
        notify({ type: 'error', title: `Couldn't upload ${file.name}`, text: err.message });
      }
    }
  };
  const addFilesAuto = (files) => {
    let current = attachments;
    files.forEach(f => {
      const kind = kindForFile(modeId, f.name, current);
      current = [...current, { kind }];
      handleFileUpload([f], kind);
    });
  };

  useEffect(() => {
    let depth = 0;
    const hasFiles = (e) => Array.from(e.dataTransfer?.types || []).includes('Files');
    const enter = (e) => { if (!hasFiles(e)) return; e.preventDefault(); depth++; setDragging(true); };
    const over = (e) => { if (hasFiles(e)) e.preventDefault(); };
    const leave = (e) => { if (!hasFiles(e)) return; depth = Math.max(0, depth - 1); if (!depth) setDragging(false); };
    const drop = (e) => {
      if (!hasFiles(e)) return;
      e.preventDefault(); depth = 0; setDragging(false);
      if (!isAirDrawingOpen) addFilesAuto(Array.from(e.dataTransfer.files || []));
    };
    window.addEventListener('dragenter', enter);
    window.addEventListener('dragover', over);
    window.addEventListener('dragleave', leave);
    window.addEventListener('drop', drop);
    return () => {
      window.removeEventListener('dragenter', enter);
      window.removeEventListener('dragover', over);
      window.removeEventListener('dragleave', leave);
      window.removeEventListener('drop', drop);
    };
  });

  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    const onPaste = (e) => {
      const files = Array.from(e.clipboardData?.files || []);
      if (files.length) { e.preventDefault(); addFilesAuto(files); }
    };
    el.addEventListener('paste', onPaste);
    return () => el.removeEventListener('paste', onPaste);
  });

  // ── Keyboard shortcuts ─────────────────────────────────────────────────
  useEffect(() => {
    const onKey = (e) => {
      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'o') { e.preventDefault(); handleNewChat(); }
      else if (e.ctrlKey && e.key.toLowerCase() === 'b' && !e.shiftKey) { e.preventDefault(); setSidebarOpen(o => !o); }
      else if (e.key === '/' && document.activeElement?.tagName !== 'TEXTAREA' && document.activeElement?.tagName !== 'INPUT') {
        e.preventDefault(); textareaRef.current?.focus();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  // ── Dictation ──────────────────────────────────────────────────────────
  const speech = useSpeech((text, ended, starting) => {
    if (starting) { dictationBase.current = inputValue; return; }
    if (ended || text == null) return;
    const base = dictationBase.current;
    setInputValue(base ? `${base} ${text}` : text);
  });

  const suggestion = isLoading ? null : suggestMode(modeId, inputValue);
  const lastIdx = messages.length - 1;

  return (
    <div className="h-screen flex overflow-hidden text-ink-100 font-sans">
      <div className="app-bg">
        <div className="blob b1" /><div className="blob b2" /><div className="blob b3" />
        <div className="grid" /><div className="grain" />
      </div>

      <Sidebar
        open={sidebarOpen} onClose={() => setSidebarOpen(false)}
        modeId={modeId} onModeChange={handleModeChange} onNewChat={handleNewChat}
        onOpenAirDrawing={() => setIsAirDrawingOpen(true)} onOpenMemory={() => setMemoryOpen(true)}
        backendOnline={backendOnline} isLoading={isLoading}
        tripwire={{ enabled: tripwireEnabled, running: tripwireRunning, calibrating: tripwireCalibrating, threshold: tripwireThreshold }}
        onTripwireToggle={handleTripwireToggle} onTripwireCalibrate={handleTripwireCalibrate}
      />

      <main className="relative z-10 flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="h-14 shrink-0 flex items-center gap-2 px-3 sm:px-5">
          {!sidebarOpen && (
            <>
              <button onClick={() => setSidebarOpen(true)} title="Show sidebar (Ctrl+B)" className="p-2 rounded-lg text-ink-300 hover:text-white hover:bg-white/5">
                <PanelLeftOpen size={18} />
              </button>
              <div className="flex items-center gap-2.5 mr-2">
                <Orb size={22} busy={isLoading} rings={false} />
                <span className="text-[14px] font-semibold tracking-[0.18em] text-white">JARVIS</span>
              </div>
            </>
          )}
          <AnimatePresence mode="wait">
            <motion.div key={modeId} initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 4 }}
              className="hidden sm:flex items-center gap-2 text-[13px] text-ink-300">
              <mode.icon size={15} style={{ color: mode.accent }} />
              <span className="text-white font-medium">{mode.label}</span>
              {!backendOnline && <span className="ml-2 px-2 py-0.5 rounded-full text-[11px] text-rose-300 bg-rose-500/10 border border-rose-400/20">backend offline</span>}
            </motion.div>
          </AnimatePresence>
          <div className="flex-1" />
          {[
            { icon: BrainCircuit, title: 'Memory', onClick: () => setMemoryOpen(true) },
            { icon: Hand, title: 'Air Drawing', onClick: () => setIsAirDrawingOpen(true) },
            { icon: SquarePen, title: 'New chat (Ctrl+Shift+O)', onClick: handleNewChat },
          ].map(b => (
            <button key={b.title} onClick={b.onClick} title={b.title}
              className="p-2 rounded-xl text-ink-300 hover:text-white hover:bg-white/[0.06] transition-colors">
              <b.icon size={18} />
            </button>
          ))}
        </header>

        {/* Conversation */}
        <div ref={scrollRef} onScroll={onScroll} className="flex-1 overflow-y-auto custom-scrollbar">
          {messages.length === 0 ? (
            <EmptyState mode={mode} onPick={(s) => {
              if (s.fill !== false && s.text) setInputValue(s.text);
              setTimeout(() => {
                const el = textareaRef.current;
                if (el) { el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
              }, 30);
            }} />
          ) : (
            <div className="max-w-3xl mx-auto px-4 sm:px-6 pt-6 pb-10 space-y-8">
              {messages.map((msg, idx) => (
                <ChatMessage key={msg.id || idx} msg={msg}
                  isStreaming={isLoading && idx === lastIdx && msg.role === 'assistant'}
                  canRegenerate={idx === lastIdx && !isLoading && !!msg.request}
                  onRegenerate={handleRegenerate} />
              ))}
            </div>
          )}
        </div>

        {/* Composer */}
        <div className="relative shrink-0 px-3 sm:px-6 pb-3 pt-2">
          <div className="pointer-events-none absolute inset-x-0 -top-10 h-10 bg-gradient-to-t from-ink-950/90 to-transparent" />
          <AnimatePresence>
            {!atBottom && messages.length > 0 && (
              <motion.button initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 8 }}
                onClick={() => scrollToBottom()} title="Scroll to bottom"
                className="absolute left-1/2 -translate-x-1/2 -top-12 z-10 grid place-items-center w-9 h-9 rounded-full glass-strong text-ink-200 hover:text-white">
                <ArrowDown size={16} />
              </motion.button>
            )}
          </AnimatePresence>
          <div className="max-w-3xl mx-auto">
            <Composer
              mode={mode} onModeChange={handleModeChange}
              value={inputValue} onChange={setInputValue}
              onSubmit={() => handleSendMessage()} onStop={handleStop} isLoading={isLoading}
              attachments={attachments} onFiles={handleFileUpload}
              onRemoveAttachment={(id) => setAttachments(prev => prev.filter(a => a.id !== id))}
              onDescribe={(id, d) => setAttachments(prev => prev.map(a => a.id === id ? { ...a, description: d } : a))}
              options={options} onOptionChange={setOption}
              speech={speech} suggestedMode={suggestion} textareaRef={textareaRef}
            />
          </div>
        </div>
      </main>

      <MemoryPanel open={memoryOpen} onClose={() => setMemoryOpen(false)} notify={notify} />
      <Toasts toasts={toasts} onDismiss={dismissToast} />

      {/* Drag & drop overlay */}
      <AnimatePresence>
        {dragging && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-[150] grid place-items-center bg-ink-950/70 backdrop-blur-md pointer-events-none">
            <motion.div initial={{ scale: 0.95 }} animate={{ scale: 1 }}
              className="flex flex-col items-center gap-3 px-14 py-12 rounded-[28px] border-2 border-dashed"
              style={{ borderColor: `${mode.accent}80`, background: `${mode.accent}0d` }}>
              <Upload size={30} style={{ color: mode.accent }} />
              <p className="text-[16px] font-medium text-white">Drop files to attach</p>
              <p className="text-[12.5px] text-ink-300">
                {mode.uploads.length ? `They'll be added as ${mode.label} inputs` : 'Attached to your next message'}
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Air Drawing overlay */}
      {isAirDrawingOpen && (
        <div className="fixed inset-0 z-[99999] bg-[#0f172a] overflow-hidden">
          <AirDrawingApp />
          <button onClick={() => setIsAirDrawingOpen(false)}
            className="absolute top-5 left-5 z-[999999] flex items-center gap-2 px-4 py-2 rounded-full glass-strong text-[13px] font-medium text-white hover:bg-white/10 transition-colors">
            <X size={15} /> Exit Air Drawing
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
