import { useState, useRef, useEffect } from 'react';
import { Send, Bot, Loader2, Mic, Paperclip } from 'lucide-react';
import ChatMessage from './ChatMessage';
import DagPlanPanel from './DagPlanPanel';
import AirDrawingApp from './AirDrawing/AirDrawingApp';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isUploadMenuOpen, setIsUploadMenuOpen] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [pptThemeImage, setPptThemeImage] = useState(null); // { name, path, url }
  const [isAirDrawingOpen, setIsAirDrawingOpen] = useState(false);

  // ── Acoustic Tripwire state ────────────────────────────────────────
  const [tripwireEnabled, setTripwireEnabled] = useState(false);
  const [tripwireRunning, setTripwireRunning] = useState(false);
  const [tripwireCalibrating, setTripwireCalibrating] = useState(false);
  const [tripwireThreshold, setTripwireThreshold] = useState(null);

  // ── Acoustic Tripwire: poll backend status every 5 seconds ───────────────
  useEffect(() => {
    const fetchTripwireStatus = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/tripwire/status');
        if (res.ok) {
          const data = await res.json();
          setTripwireEnabled(data.enabled ?? false);
          setTripwireRunning(data.running ?? false);
          if (data.volume_threshold) setTripwireThreshold(data.volume_threshold);
        }
      } catch (_) { /* backend not running yet — silent */ }
    };
    fetchTripwireStatus();
    const id = setInterval(fetchTripwireStatus, 5000);
    return () => clearInterval(id);
  }, []);

  const handleTripwireToggle = async () => {
    const endpoint = tripwireEnabled ? '/tripwire/disable' : '/tripwire/enable';
    try {
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        if (data.status === 'ok') setTripwireEnabled(!tripwireEnabled);
      }
    } catch (err) { console.error('[Tripwire] toggle error:', err); }
  };

  const handleTripwireCalibrate = async () => {
    setTripwireCalibrating(true);
    try {
      await fetch('http://127.0.0.1:8000/tripwire/calibrate', { method: 'POST' });
      // Wait 2.5s for calibration to complete, then refresh threshold
      setTimeout(async () => {
        try {
          const res = await fetch('http://127.0.0.1:8000/tripwire/status');
          if (res.ok) {
            const d = await res.json();
            if (d.volume_threshold) setTripwireThreshold(d.volume_threshold);
          }
        } catch (_) {}
        setTripwireCalibrating(false);
      }, 2500);
    } catch (err) {
      console.error('[Tripwire] calibrate error:', err);
      setTripwireCalibrating(false);
    }
  };

  useEffect(() => {
    if (messages.length > 0) {
      const lastMsg = messages[messages.length - 1];
      if (lastMsg.role === 'assistant' && lastMsg.content.includes('[OPEN_AIR_DRAWING]')) {
        setIsAirDrawingOpen(true);
        setMessages(prev => {
          const copy = [...prev];
          const last = { ...copy[copy.length - 1] };
          last.content = last.content.replace('[OPEN_AIR_DRAWING]', '').trim();
          copy[copy.length - 1] = last;
          return copy;
        });
      }
    }
  }, [messages]);

  // ── DAG state ────────────────────────────────────────────────────────────
  // dagPlan: { nodes, summary, waveCount } | null
  // dagNodeStates: { [nodeId]: { status, result, error } }
  // dagComplete: boolean
  const [dagPlan, setDagPlan] = useState(null);
  const [dagNodeStates, setDagNodeStates] = useState({});
  const [dagComplete, setDagComplete] = useState(false);

  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const themeInputRef = useRef(null);
  const textareaRef = useRef(null);

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (!files || files.length === 0) return;

    setIsUploading(true);
    const uploadType = e.target.dataset.uploadType;

    for (const file of files) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const res = await fetch('http://127.0.0.1:8000/upload', {
          method: 'POST',
          body: formData,
        });
        const data = await res.json();
        if (data.status === 'success') {
          if (uploadType === 'ppt_theme') {
            setPptThemeImage({ name: file.name, path: data.path, url: URL.createObjectURL(file) });
          } else {
            if (uploadType === 'assignment') {
              setInputValue(prev => prev ? `${prev} | do my assignment from ${data.filename}` : `do my assignment from ${data.filename}`);
            }
            setUploadedFiles(prev => [...prev, {
              name: file.name,
              path: data.path,
              url: URL.createObjectURL(file)
            }]);
          }
        } else {
          alert("Upload failed: " + data.error);
        }
      } catch (err) {
        console.error(err);
        alert(`Failed to upload file ${file.name}`);
      }
    }

    setIsUploading(false);
    e.target.value = '';
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const PPT_KW = [
    'create a presentation', 'make a presentation', 'build a presentation',
    'generate a presentation', 'design a presentation', 'prepare a presentation',
    'create slides', 'make slides', 'build slides',
    'make a ppt', 'create a ppt', 'build a ppt', 'generate a ppt',
    'create a deck', 'make a deck', 'create a powerpoint', 'make a powerpoint',
    'create presentation', 'make presentation',
    'ppt on ', 'ppt about ', 'presentation on ', 'presentation about ', 'slide deck on ',
  ];
  const isPPTRequest = (text) => {
    const lower = text.toLowerCase();
    const exactMatch = PPT_KW.some(kw => lower.includes(kw));
    const regexMatch = /(?:create|make|build|generate|design|prepare|give|need|want|use|change|update|modify|edit|convert|theme).*(?:ppt|presentation|slide|deck|powerpoint|theme|color)/i.test(lower);
    return exactMatch || regexMatch;
  };

  const appendMsg = (chunk) => {
    setMessages((prev) => {
      const copy = prev.map((m) => ({ ...m }));
      const last = copy[copy.length - 1];
      if (last && last.role === 'assistant') last.content += chunk;
      return copy;
    });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    const prompt = inputValue.trim();
    if (!prompt && uploadedFiles.length === 0 && !isLoading) return;

    setInputValue('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
    setIsLoading(true);

    const attachedTags = uploadedFiles.map(f => {
      const p = f.path.replace(/\\/g, '/');
      return f.description ? `[ATTACHED_FILE: ${p} | DESCRIPTION: ${f.description}]` : `[ATTACHED_FILE: ${p}]`;
    }).join("\n");
    const promptToSend = attachedTags ? `${prompt}\n\n${attachedTags}`.trim() : prompt;
    const uiDisplayMessage = prompt;
    const attachedFiles = [...uploadedFiles];

    setMessages((prev) => [
      ...prev,
      { role: 'user', content: uiDisplayMessage, attachedFiles: attachedFiles },
      { role: 'assistant', content: '' },
    ]);

    setUploadedFiles([]);

    try {
      if (isPPTRequest(prompt)) {
        appendMsg('🚀 Initializing Deep Chunked PPT Generation...\n');

        const body = { prompt: promptToSend };

        if (pptThemeImage) {
          body.theme_image_path = pptThemeImage.path.replace(/\\/g, '/');
          appendMsg(`🎨 Using your reference theme: ${pptThemeImage.name}\n`);
          setPptThemeImage(null);
        } else if (uploadedFiles.length > 0) {
          const imgFile = uploadedFiles.find(f => f.name.match(/\.(png|jpg|jpeg|webp)$/i));
          if (imgFile) {
            body.theme_image_path = imgFile.path.replace(/\\/g, '/');
            appendMsg(`🎨 Auto-detected theme reference from uploaded image: ${imgFile.name}\n`);
          }
        }

        const res = await fetch('http://127.0.0.1:8000/ppt/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });

        if (!res.ok) throw new Error("Backend PPT creation failed");

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let done = false;
        while (!done) {
          const { value, done: doneReading } = await reader.read();
          done = doneReading;
          if (value) {
            const chunk = decoder.decode(value);
            setMessages((prev) => {
              const copy = [...prev];
              const last = copy[copy.length - 1];
              if (last && last.role === 'assistant') last.content += chunk;
              return copy;
            });
          }
        }
        return;
      }

      // Reset DAG state for a fresh request
      setDagPlan(null);
      setDagNodeStates({});
      setDagComplete(false);

      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: promptToSend }),
      });

      if (!response.ok) throw new Error(`Server returned ${response.status}`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      // Detect response type from the first meaningful chunk:
      //   DAG responses  → start with  'data: {'  (structured SSE events)
      //   LLM responses  → plain text tokens with no 'data:' prefix
      let isDagStream = null;   // null = not yet determined
      let dagBuffer = '';     // accumulates partial DAG SSE events

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        if (!chunk) continue;

        // ── Determine stream type on first non-empty chunk ──────────────────
        if (isDagStream === null) {
          isDagStream = chunk.trimStart().startsWith('data: {');
        }

        // ── DAG stream: buffer on \n\n and parse JSON events ─────────────────
        if (isDagStream) {
          dagBuffer += chunk;
          // SSE events are delimited by double-newline
          const parts = dagBuffer.split('\n\n');
          dagBuffer = parts.pop();           // keep last incomplete fragment

          for (const part of parts) {
            const line = part.replace(/^data:\s*/, '').trim();
            if (!line || line === '[DONE]') continue;
            try {
              const evt = JSON.parse(line);
              if (evt && typeof evt.type === 'string') {
                handleDagEvent(evt);
              }
            } catch (_) {
              // Malformed JSON in a DAG event — ignore
            }
          }
        } else {
          // ── Plain LLM stream: append raw chunk directly (original behaviour) ──
          const text = chunk
            .replace(/^data:\s*/gm, '')   // strip any stray data: prefixes
            .replace(/\[DONE\]/g, '');    // strip SSE done marker
          if (text) {
            setMessages((prev) => {
              const copy = prev.map((m) => ({ ...m }));
              const last = copy[copy.length - 1];
              if (last && last.role === 'assistant') last.content += text;
              return copy;
            });
          }
        }
      }

      // Flush any remaining DAG buffer content
      if (dagBuffer.trim()) {
        const line = dagBuffer.replace(/^data:\s*/, '').trim();
        if (line && line !== '[DONE]') {
          try {
            const evt = JSON.parse(line);
            if (evt && typeof evt.type === 'string') handleDagEvent(evt);
          } catch (_) { }
        }
      }
    } catch (err) {
      console.error('[Jarvis] fetch error:', err);
      setMessages((prev) => {
        const copy = prev.map((m) => ({ ...m }));
        const last = copy[copy.length - 1];
        if (last && last.role === 'assistant') {
          last.content += `\n\n⚠️ Could not complete request: ${err.message}. Make sure the backend is running on port 8000.`;
        }
        return copy;
      });
    } finally {
      setIsLoading(false);
    }
  };

  // ── DAG Event Handler ──────────────────────────────────────────────────────
  const handleDagEvent = (evt) => {
    switch (evt.type) {
      case 'plan':
        setDagPlan({
          nodes: evt.nodes || [],
          summary: evt.summary || '',
          waveCount: evt.wave_count || 0,
        });
        setDagNodeStates(
          Object.fromEntries((evt.nodes || []).map(n => [n.id, { status: 'pending', result: '', error: '' }]))
        );
        break;

      case 'node_start':
        setDagNodeStates(prev => ({
          ...prev,
          [evt.id]: { ...(prev[evt.id] || {}), status: 'running' },
        }));
        break;

      case 'node_done':
        setDagNodeStates(prev => ({
          ...prev,
          [evt.id]: { ...(prev[evt.id] || {}), status: 'done', result: evt.result || '' },
        }));
        break;

      case 'node_failed':
        setDagNodeStates(prev => ({
          ...prev,
          [evt.id]: { ...(prev[evt.id] || {}), status: 'failed', error: evt.error || '' },
        }));
        break;

      case 'aggregate':
        setMessages(prev => {
          const copy = prev.map(m => ({ ...m }));
          const last = copy[copy.length - 1];
          if (last && last.role === 'assistant') last.content = evt.text || last.content;
          return copy;
        });
        break;

      case 'narration':
      case 'fallback':
        setMessages(prev => {
          const copy = prev.map(m => ({ ...m }));
          const last = copy[copy.length - 1];
          if (last && last.role === 'assistant' && evt.text) {
            last.content += (last.content ? ' ' : '') + evt.text;
          }
          return copy;
        });
        break;

      case 'done':
        setDagComplete(true);
        break;

      default:
        break;
    }
  };

  return (
    <div className="flex flex-col h-screen sci-fi-bg text-white font-sans overflow-hidden relative">
      {isAirDrawingOpen && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          zIndex: 99999,
          backgroundColor: '#0f172a',
          overflow: 'hidden'
        }}>
          <AirDrawingApp />
          <button
            onClick={() => setIsAirDrawingOpen(false)}
            style={{
              position: 'absolute',
              top: '20px',
              left: '20px',
              zIndex: 999999,
              background: 'rgba(255, 50, 50, 0.8)',
              color: 'white',
              border: '1px solid rgba(255, 100, 100, 0.5)',
              borderRadius: '8px',
              padding: '10px 20px',
              cursor: 'pointer',
              fontFamily: 'monospace',
              fontWeight: 'bold',
              boxShadow: '0 4px 15px rgba(0,0,0,0.5)'
            }}
          >
            EXIT AIR DRAWING
          </button>
        </div>
      )}

      {/* Arc Reactor Background */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] pointer-events-none opacity-40 z-0 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-[1px] border-cyan-500/30 animate-spin-slow"></div>
        <div className="absolute inset-8 rounded-full border-2 border-dashed border-cyan-400/50 animate-spin-reverse-slow"></div>
        <div className="absolute inset-16 rounded-full border-[6px] border-cyan-500/20 shadow-[0_0_50px_rgba(0,243,255,0.2)]" style={{ animation: 'pulse-glow 4s infinite' }}></div>
        <div className="absolute inset-28 rounded-full border border-cyan-400/40 animate-spin-slow" style={{ animationDuration: '15s' }}></div>
        <div className="absolute inset-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-cyan-500/20 rounded-full blur-[60px]"></div>
        <Bot size={80} className="absolute text-cyan-300/60 animate-pulse drop-shadow-[0_0_15px_rgba(0,243,255,0.8)]" />
      </div>

      {/* Top Header */}
      <header className="h-16 bg-[#020713]/80 backdrop-blur-md border-b border-cyan-900/80 flex items-center justify-between px-8 z-20 shrink-0 shadow-[0_0_20px_rgba(0,243,255,0.05)]">
        <div className="flex items-center space-x-6 text-xs font-mono text-cyan-500 hidden md:flex">
          <div className="flex items-center space-x-2">
            <span className="animate-pulse text-cyan-400">📡</span>
            <span className="tracking-widest">SATELLITE STRENGTH</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-cyan-400">⚡</span>
            <span className="tracking-widest">QUANTUM LINK STABILITY</span>
          </div>
          <button onClick={() => setIsAirDrawingOpen(true)} className="px-3 py-1 bg-cyan-900/40 border border-cyan-500/50 rounded text-cyan-300 hover:bg-cyan-500/30 transition-colors flex items-center shadow-[0_0_10px_rgba(0,243,255,0.1)]">
            <span>✨ AIR DRAWING</span>
          </button>
        </div>

        <div className="flex items-center space-x-4 absolute left-1/2 -translate-x-1/2">
          <span className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_8px_#00f3ff]"></span>
          <span className="text-xl font-mono text-cyan-300 tracking-[0.3em] uppercase font-bold" style={{ textShadow: '0 0 15px #00f3ff' }}>System Uplink</span>
          <span className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_8px_#00f3ff]" style={{ animationDelay: '500ms' }}></span>
        </div>

        <div className="flex items-center space-x-4 text-xs font-mono text-cyan-500 hidden md:flex">
          <div className="flex items-center space-x-2">
            <span className="tracking-widest">🔒 DUPLEX-7 | SECURE: LEVEL-10</span>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex-1 flex w-full relative z-10 min-h-0">
        {/* Jarvis Core Left Panel */}
        <div className="hidden lg:flex flex-col w-[340px] p-6 space-y-6 shrink-0 h-full overflow-y-auto custom-scrollbar">
          <div className="hud-panel p-6 flex flex-col">
            <div className="flex items-center justify-between mb-6 border-b border-cyan-800/50 pb-3">
              <h2 className="hud-header-text text-xl">Jarvis Core</h2>
              <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_8px_#00f3ff]"></div>
            </div>

            <div className="w-full space-y-6">
              <div>
                <div className="flex justify-between text-[11px] font-mono text-cyan-300 mb-2 uppercase tracking-widest">
                  <span>CPU Load</span>
                  <span className="text-cyan-100">42%</span>
                </div>
                <div className="w-full h-1.5 bg-cyan-950/60 rounded-full overflow-hidden border border-cyan-900/50">
                  <div className="h-full bg-cyan-400 w-[42%] shadow-[0_0_10px_#00f3ff]"></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-[11px] font-mono text-cyan-300 mb-2 uppercase tracking-widest">
                  <span>NET Mbps</span>
                  <span className="text-cyan-100">94 bps</span>
                </div>
                <div className="w-full h-1.5 bg-cyan-950/60 rounded-full overflow-hidden border border-cyan-900/50">
                  <div className="h-full bg-cyan-400 w-[75%] shadow-[0_0_10px_#00f3ff]"></div>
                </div>
              </div>

              <div className="pt-4">
                <span className="text-[11px] font-mono text-cyan-500 uppercase tracking-widest mb-2 block">Voice Activity</span>
                <div className="flex items-end h-16 gap-1 w-full bg-cyan-950/20 border border-cyan-900/30 p-2 rounded">
                  {[...Array(24)].map((_, i) => (
                    <div key={i} className="flex-1 bg-cyan-500/70 rounded-t-sm" style={{ height: `${Math.max(10, Math.random() * 100)}%`, animation: `wave ${1 + Math.random()}s infinite` }}></div>
                  ))}
                </div>
              </div>

              <div className="pt-4 flex justify-between items-center text-[11px] font-mono text-cyan-500 uppercase border-t border-cyan-800/50 pt-4">
                <span className="tracking-widest">Neural Stability</span>
                <span className="text-emerald-400 border border-emerald-500/30 bg-emerald-900/20 px-2 py-0.5 rounded">Stable</span>
              </div>

              <div className="pt-2 flex justify-between items-center text-[11px] font-mono text-cyan-500 uppercase">
                <span className="tracking-widest">Core Temperature</span>
                <span className="text-orange-400 border border-orange-500/30 bg-orange-900/20 px-2 py-0.5 rounded">Optimal</span>
              </div>

              {/* ── Acoustic Tripwire Toggle ── */}
              <div className="pt-4 border-t border-cyan-800/50">
                <div className="flex justify-between items-center text-[11px] font-mono uppercase mb-3">
                  <div className="flex items-center gap-2 text-cyan-500 tracking-widest">
                    {tripwireEnabled && tripwireRunning && (
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_6px_#34d399] animate-pulse" />
                    )}
                    <span>Acoustic Wake</span>
                  </div>
                  <button
                    id="tripwire-toggle-btn"
                    onClick={handleTripwireToggle}
                    title={tripwireEnabled ? 'Disarm acoustic tripwire' : 'Arm acoustic tripwire'}
                    className={`relative inline-flex items-center h-5 w-9 rounded-full transition-colors duration-300 focus:outline-none border ${
                      tripwireEnabled
                        ? 'bg-emerald-600/70 border-emerald-500/60 shadow-[0_0_8px_rgba(52,211,153,0.4)]'
                        : 'bg-cyan-950/60 border-cyan-800/60'
                    }`}
                  >
                    <span className={`inline-block w-3.5 h-3.5 rounded-full transition-transform duration-300 ${
                      tripwireEnabled
                        ? 'translate-x-[18px] bg-emerald-300 shadow-[0_0_6px_#34d399]'
                        : 'translate-x-[2px] bg-cyan-600'
                    }`} />
                  </button>
                </div>

                {/* Status / threshold line */}
                <div className="flex justify-between items-center text-[10px] font-mono text-cyan-700 mb-2">
                  <span>{tripwireRunning ? (tripwireEnabled ? 'ARMED — clap twice' : 'STANDBY') : 'OFFLINE'}</span>
                  {tripwireThreshold && (
                    <span className="text-cyan-600">thr: {tripwireThreshold}</span>
                  )}
                </div>

                {/* Calibrate button */}
                <button
                  id="tripwire-calibrate-btn"
                  onClick={handleTripwireCalibrate}
                  disabled={tripwireCalibrating || !tripwireRunning}
                  className="w-full py-1.5 text-[10px] font-mono tracking-widest uppercase border border-cyan-800/60 rounded bg-cyan-950/40 text-cyan-600 hover:text-cyan-300 hover:border-cyan-600/60 hover:bg-cyan-900/40 transition-all disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {tripwireCalibrating ? (
                    <><span className="animate-spin">&#9696;</span> Calibrating...</>
                  ) : (
                    <>⦿ Recalibrate Noise Floor</>
                  )}
                </button>
              </div>
            </div>
          </div>

          <div className="hud-panel p-6 flex flex-col mt-auto border border-cyan-500/30 relative overflow-hidden group">
            <div className="absolute inset-0 bg-cyan-500/5 group-hover:bg-cyan-500/10 transition-colors"></div>
            <h3 className="hud-header-text text-sm mb-3">System Logs</h3>
            <div className="space-y-2 text-[10px] font-mono text-cyan-600 tracking-widest leading-relaxed">
              <p className="animate-pulse text-cyan-400">&gt; Initializing neural subsystems...</p>
              <p>&gt; Data ingestion protocol bypassed.</p>
              <p>&gt; Quantum link established.</p>
              <p className="text-emerald-400">&gt; ALL SYSTEMS OPERATIONAL.</p>
            </div>
          </div>
        </div>

        {/* Center Chat Area */}
        <div className="flex-1 flex flex-col relative px-4 lg:pl-0 lg:pr-12 pb-40 w-full max-w-[1600px] mr-auto min-h-0" style={{ perspective: '1200px' }}>

          {/* Holographic Container for Chat */}
          <div className="flex-1 flex flex-col relative z-10 w-full rounded-[2rem] border border-cyan-400/50 shadow-[20px_20px_50px_rgba(0,243,255,0.15)] overflow-hidden transition-transform duration-500 bg-cyan-950/20 backdrop-blur-[4px] min-h-0"
            style={{ transform: 'rotateY(8deg) rotateX(2deg) translateZ(0)', transformOrigin: 'left center', transformStyle: 'preserve-3d' }}>

            <div className="absolute inset-0 bg-gradient-to-br from-cyan-300/10 via-transparent to-transparent pointer-events-none"></div>

            {/* Messages */}
            <main className="flex-1 overflow-y-auto pt-8 px-6 lg:px-12 space-y-8 custom-scrollbar relative z-10 w-full pb-10">
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-cyan-700 space-y-8 opacity-90 mt-10">
                  <div className="hud-panel p-6 border border-cyan-500/30 bg-[#020713]/80 w-full max-w-2xl text-center shadow-[0_0_30px_rgba(0,243,255,0.1)] rounded-2xl relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-cyan-400 to-transparent opacity-70" />
                    <p className="text-3xl font-bold text-cyan-300 tracking-[0.2em] uppercase font-mono mb-6" style={{ textShadow: '0 0 15px #00f3ff' }}>System Ready</p>

                    <div className="grid grid-cols-2 gap-4 text-left">
                      <div className="border border-cyan-900/50 p-4 rounded bg-cyan-950/20">
                        <p className="text-cyan-400 mb-2 text-xs font-mono tracking-widest border-b border-cyan-800/50 pb-2">COMMANDS</p>
                        <ul className="text-[11px] font-mono text-cyan-500 space-y-2">
                          <li>&gt; open [app name]</li>
                          <li>&gt; search [query]</li>
                          <li>&gt; send whatsapp to [name]</li>
                          <li>&gt; check emails</li>
                        </ul>
                      </div>
                      <div className="border border-cyan-900/50 p-4 rounded bg-cyan-950/20">
                        <p className="text-cyan-400 mb-2 text-xs font-mono tracking-widest border-b border-cyan-800/50 pb-2">MODULES</p>
                        <ul className="text-[11px] font-mono text-cyan-500 space-y-2">
                          <li>&gt; PPT Generator</li>
                          <li>&gt; Vision Stack</li>
                          <li>&gt; Desktop Automation</li>
                          <li>&gt; Voice Synthesis</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div className="w-full mx-auto space-y-6 relative">
                {messages.map((msg, idx) => (
                  <div key={idx}>
                    {/* Show DAG panel above the last assistant message when a plan exists */}
                    {msg.role === 'assistant' && idx === messages.length - 1 && dagPlan && (
                      <DagPlanPanel
                        nodes={dagPlan.nodes}
                        nodeStates={dagNodeStates}
                        summary={dagPlan.summary}
                        waveCount={dagPlan.waveCount}
                        isComplete={dagComplete}
                      />
                    )}
                    <ChatMessage msg={msg} />
                  </div>
                ))}

                {isLoading && messages[messages.length - 1]?.content === '' && (
                  <div className="flex items-start">
                    <div className="hud-panel text-gray-200 rounded-2xl rounded-tl-none border-l-4 border-l-cyan-400 px-6 py-4 flex items-center space-x-3 w-[100px] shadow-[0_0_15px_rgba(0,243,255,0.15)]">
                      <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce shadow-[0_0_5px_#00f3ff]" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce shadow-[0_0_5px_#00f3ff]" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce shadow-[0_0_5px_#00f3ff]" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} className="h-8" />
              </div>
            </main>
          </div>
        </div>
      </div>

      {/* Input Pedestal (Bottom Fixed) */}
      <div className="absolute bottom-6 left-0 right-0 flex flex-col items-center z-30 pointer-events-none">

        {/* Status Bar */}
        <div className="mb-4 relative flex items-center justify-center bg-[#010409]/90 backdrop-blur-md border border-cyan-900/80 rounded-full px-8 py-2 shadow-[0_0_20px_rgba(0,243,255,0.1)] gap-6 pointer-events-auto">
          <div className="absolute left-0 top-0 h-full w-12 bg-gradient-to-r from-cyan-500/20 to-transparent rounded-l-full" />
          <div className="absolute right-0 top-0 h-full w-12 bg-gradient-to-l from-cyan-500/20 to-transparent rounded-r-full" />

          <span className={`text-[10px] font-mono tracking-[0.2em] uppercase ${isLoading ? 'text-cyan-300 animate-pulse' : 'text-cyan-500'}`}>
            {isLoading ? 'Processing command...' : 'Awaiting operator command...'}
          </span>

          <div className="flex items-center h-5 gap-1">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className={`waveform-bar ${isLoading ? 'opacity-100' : 'opacity-40'}`} />
            ))}
            <div className="w-8 h-8 rounded-full border border-cyan-500/50 flex items-center justify-center bg-cyan-900/30 mx-2 z-10 shadow-[0_0_15px_rgba(0,243,255,0.2)]">
              <Mic size={14} className={isLoading ? 'text-cyan-300' : 'text-cyan-400'} />
            </div>
            {[4, 5, 6, 7].map((i) => (
              <div key={i} className={`waveform-bar ${isLoading ? 'opacity-100' : 'opacity-40'}`} />
            ))}
          </div>
        </div>

        <div className="w-full max-w-4xl relative flex flex-col items-center pointer-events-auto px-4">
          <form onSubmit={handleSendMessage} className="w-full relative flex flex-col gap-2 group">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 via-cyan-400/20 to-cyan-500/10 rounded-[28px] blur-md group-focus-within:opacity-100 opacity-60 transition-opacity" />

            {uploadedFiles.length > 0 && (
              <div className="relative flex gap-3 px-4 py-3 overflow-x-auto w-full hud-panel border border-cyan-500/40 rounded-[20px] shadow-[0_0_15px_rgba(0,243,255,0.1)] z-10">
                {uploadedFiles.map((f, i) => (
                  <div key={i} className="relative group/img shrink-0 rounded-lg overflow-visible h-16 border border-cyan-700 bg-cyan-950/60 flex items-center p-1 gap-2">
                    {f.name.match(/\.(png|jpg|jpeg|webp)$/i) ? (
                      <img src={f.url} alt={f.name} className="h-full w-14 object-cover rounded-md border border-cyan-500/30" />
                    ) : (
                      <div className="text-[10px] text-cyan-200 text-center break-words p-1 leading-tight font-mono w-14">
                        {f.name.length > 15 ? f.name.substring(0, 13) + '...' : f.name}
                      </div>
                    )}
                    <input
                      type="text"
                      placeholder="Describe image..."
                      className="bg-transparent border-none text-xs text-cyan-100 outline-none w-36 placeholder-cyan-800/70 mr-2"
                      value={f.description || ''}
                      onChange={(e) => {
                        const newFiles = [...uploadedFiles];
                        newFiles[i].description = e.target.value;
                        setUploadedFiles(newFiles);
                      }}
                    />
                    <button
                      type="button"
                      onClick={() => setUploadedFiles(prev => prev.filter((_, idx) => idx !== i))}
                      className="absolute -top-2 -right-2 bg-red-500/80 text-white rounded-full p-1 w-5 h-5 flex items-center justify-center text-[10px] shadow-lg hover:bg-red-500 transition-colors z-20 border border-red-400/50"
                    >✕</button>
                  </div>
                ))}
              </div>
            )}

            {pptThemeImage && (
              <div className="relative flex items-center gap-3 px-4 py-2 mb-2 w-full bg-purple-950/60 border border-purple-500/50 rounded-2xl z-10 shadow-[0_0_12px_rgba(168,85,247,0.2)]">
                <span className="text-purple-300 text-xs font-mono tracking-wide">🎨 PPT Theme Reference:</span>
                <img src={pptThemeImage.url} alt="theme" className="h-10 w-16 object-cover rounded-md border border-purple-400/40" />
                <span className="text-purple-200 text-xs font-mono truncate max-w-[160px]">{pptThemeImage.name}</span>
                <button
                  type="button"
                  onClick={() => setPptThemeImage(null)}
                  className="ml-auto text-purple-400 hover:text-white text-xs font-mono bg-purple-900/40 px-2 py-1 rounded-full hover:bg-purple-700/60 transition-colors"
                >✕ Remove</button>
              </div>
            )}

            <div className="relative flex w-full bg-[#020611]/90 backdrop-blur-xl border border-cyan-500/50 rounded-[28px] shadow-[0_0_25px_rgba(0,243,255,0.15)] focus-within:border-cyan-400 focus-within:shadow-[0_0_30px_rgba(0,243,255,0.3)] transition-all items-end pl-6 pr-2 py-2 z-10">
              <div className="w-2 h-2 bg-cyan-500 rounded-full shadow-[0_0_8px_#00f3ff] animate-pulse shrink-0 ml-2 mb-3" />

              <div className="relative ml-2 flex items-center justify-center shrink-0 mb-0.5">
                <button
                  type="button"
                  disabled={isLoading || isUploading}
                  onClick={() => setIsUploadMenuOpen(!isUploadMenuOpen)}
                  className="p-2.5 rounded-full text-cyan-400 hover:text-white hover:bg-cyan-900/50 transition-all disabled:opacity-40"
                  title="Upload Options"
                >
                  {isUploading ? <Loader2 size={20} className="animate-spin text-cyan-400" /> : <Paperclip size={20} />}
                </button>

                {isUploadMenuOpen && (
                  <>
                    <div className="fixed inset-0 z-40" onClick={() => setIsUploadMenuOpen(false)}></div>
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-4 w-56 transition-all duration-200 z-50 hud-panel border border-cyan-500/50 shadow-[0_0_20px_rgba(0,243,255,0.3)] overflow-hidden">
                      <div className="px-4 py-2 bg-cyan-950/40 border-b border-cyan-900/50 text-[10px] text-cyan-500 font-mono tracking-widest uppercase">Select Input</div>
                      <button
                        type="button"
                        onClick={() => {
                          setIsUploadMenuOpen(false);
                          fileInputRef.current.dataset.uploadType = 'assignment';
                          fileInputRef.current?.click();
                        }}
                        className="w-full text-left px-4 py-3 text-xs text-cyan-100 hover:bg-cyan-900/50 hover:text-white transition-colors border-b border-cyan-900/30 font-mono tracking-wide"
                      >
                        Assignment PDF
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setIsUploadMenuOpen(false);
                          fileInputRef.current.dataset.uploadType = 'general';
                          fileInputRef.current?.click();
                        }}
                        className="w-full text-left px-4 py-3 text-xs text-cyan-100 hover:bg-cyan-900/50 hover:text-white transition-colors border-b border-cyan-900/30 font-mono tracking-wide"
                      >
                        General File
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setIsUploadMenuOpen(false);
                          fileInputRef.current.dataset.uploadType = 'ppt_theme';
                          fileInputRef.current?.click();
                        }}
                        className="w-full text-left px-4 py-3 text-xs text-purple-300 hover:bg-purple-900/40 hover:text-white transition-colors font-mono flex items-center gap-2 tracking-wide"
                      >
                        <span>🎨</span> PPT Theme Image
                      </button>
                    </div>
                  </>
                )}
              </div>

              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                data-upload-type="assignment"
                onChange={handleFileUpload}
                accept=".pdf,.txt,.docx,.png,.jpg,.jpeg,.webp,.mp4,.avi,.mov,.mkv"
                multiple
              />

              <textarea
                id="jarvis-command-input"
                ref={textareaRef}
                rows={1}
                className="flex-1 bg-transparent text-cyan-100 px-4 py-2 outline-none text-[15px] font-mono placeholder-cyan-800/70 resize-none max-h-40 overflow-y-auto custom-scrollbar leading-relaxed"
                placeholder={isLoading ? 'Processing...' : 'Enter operator command...'}
                value={inputValue}
                onChange={(e) => {
                  setInputValue(e.target.value);
                  e.target.style.height = 'auto';
                  e.target.style.height = e.target.scrollHeight + 'px';
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    if ((inputValue.trim() || uploadedFiles.length > 0) && !isLoading) {
                      handleSendMessage(e);
                    }
                  }
                }}
                disabled={isLoading}
                autoFocus
              />

              <button
                id="jarvis-send-btn"
                type="submit"
                disabled={(!inputValue.trim() && uploadedFiles.length === 0) || isLoading}
                className="p-2.5 rounded-full text-cyan-300 hover:text-white hover:bg-cyan-600/80 transition-all disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center bg-cyan-900/40 shrink-0 mb-1 mr-1 border border-cyan-500/30 shadow-[0_0_10px_rgba(0,243,255,0.1)]"
              >
                {isLoading
                  ? <Loader2 size={20} className="animate-spin text-cyan-200" />
                  : <Send size={20} className="ml-0.5" />
                }
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
