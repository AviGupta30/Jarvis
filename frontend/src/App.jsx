import { useState, useRef, useEffect } from 'react';
import { Send, Bot, Loader2, Mic, Paperclip } from 'lucide-react';
import MemorySidebar from './MemorySidebar';
import ChatMessage from './ChatMessage';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const res = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (data.status === 'success') {
        const type = fileInputRef.current.dataset.uploadType;
        if (type === 'general') {
          setInputValue(`read this file: ${data.filename}`);
        } else {
          setInputValue(`do my assignment from ${data.filename}`);
        }
      } else {
        alert("Upload failed: " + data.error);
      }
    } catch (err) {
      console.error(err);
      alert("Failed to upload file");
    } finally {
      setIsUploading(false);
      e.target.value = null; // reset
    }
  };

  // Auto-scroll whenever messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // ── PPT intent detector ──────────────────────────────────────────────────
  const PPT_KW = [
    'create a presentation','make a presentation','build a presentation',
    'generate a presentation','design a presentation','prepare a presentation',
    'create slides','make slides','build slides',
    'make a ppt','create a ppt','build a ppt','generate a ppt',
    'create a deck','make a deck','create a powerpoint','make a powerpoint',
    'create presentation','make presentation',
    'ppt on ','ppt about ','presentation on ','presentation about ','slide deck on ',
  ];
  const isPPTRequest = (text) => PPT_KW.some(kw => text.toLowerCase().includes(kw));

  const STYLE_MAP = {
    'cyber dark':'cyber_dark','cyber_dark':'cyber_dark',
    'midnight executive':'midnight_exec','midnight_exec':'midnight_exec',
    'solar flare':'solar_flare','solar_flare':'solar_flare',
    'arctic clean':'arctic_clean','arctic_clean':'arctic_clean',
    'forest calm':'forest_calm','forest_calm':'forest_calm',
    'ocean gradient':'ocean_gradient','ocean_gradient':'ocean_gradient',
    'velvet noir':'velvet_noir','velvet_noir':'velvet_noir',
    'charcoal minimal':'charcoal_minimal','charcoal_minimal':'charcoal_minimal',
  };
  const detectStyle = (text) => {
    const lower = text.toLowerCase();
    for (const [name, key] of Object.entries(STYLE_MAP)) {
      if (lower.includes(name)) return key;
    }
    return null;
  };

  const PERSONALITY_DESCS = {
    cyber_dark:'Dark navy + electric teal. Hackathons, SIH, blockchain, security.',
    midnight_exec:'Deep indigo + platinum. Consulting, boardroom, enterprise strategy.',
    solar_flare:'Charcoal + amber + coral. Startups, product launches, VC pitches.',
    arctic_clean:'Ice white + deep teal. SaaS, fintech, medical, professional services.',
    forest_calm:'Forest green + sage + cream. Education, health, sustainability.',
    ocean_gradient:'Deep ocean + cerulean + white. AI, data science, ML, research.',
    velvet_noir:'Deep plum + rose gold + cream. Luxury, fashion, design portfolios.',
    charcoal_minimal:'True black + off-white + gold. Architecture, design, premium brands.',
  };

  const autoPersonality = (text) => {
    const t = text.toLowerCase();
    if (/hack|cyber|security|blockchain|ctf|sih/.test(t)) return 'cyber_dark';
    if (/luxury|fashion|portfolio|brand|premium|aesthetic/.test(t)) return 'velvet_noir';
    if (/startup|pitch|investor|funding|vc|seed|product launch/.test(t)) return 'solar_flare';
    if (/corporate|consulting|enterprise|quarterly|board|strategy/.test(t)) return 'midnight_exec';
    if (/health|nature|education|environment|green|sustainability/.test(t)) return 'forest_calm';
    if (/machine learning|deep learning|\bai\b|data science|neural/.test(t)) return 'ocean_gradient';
    if (/saas|fintech|finance|app|software|platform|cloud/.test(t)) return 'arctic_clean';
    if (/design|minimal|architecture|typography/.test(t)) return 'charcoal_minimal';
    return 'cyber_dark';
  };

  const appendMsg = (chunk) => {
    setMessages((prev) => {
      const copy = prev.map((m) => ({ ...m }));
      const last = copy[copy.length - 1];
      if (last && last.role === 'assistant') last.content += chunk;
      return copy;
    });
  };

  const handlePPTWithPuter = async (prompt) => {
    const personality = detectStyle(prompt) || autoPersonality(prompt);
    const desc = PERSONALITY_DESCS[personality] || '';

    appendMsg(`🎨 Style: **${personality.replace(/_/g,' ')}** — ${desc}\n`);
    appendMsg('🤖 Calling Gemini via Puter.js (free, no API key required)...\n');

    let plan;
    try {
      if (typeof puter === 'undefined') throw new Error('Puter.js not loaded');

      const userMsg = `You are an elite aesthetic presentation generator. Create a highly technical, content-dense, aesthetic presentation for:
TOPIC: ${prompt}

RULES:
- Exactly 10 slides.
- First slide MUST use "aesthetic_title".
- Use a mix of "aesthetic_split", "aesthetic_grid", and "aesthetic_flow" for the rest.
- TEXT MUST BE EXTREMELY DENSE. Every bullet array must have 3-4 items, and each text property MUST be 25-30 words of deep technical/strategic detail. No short bullets.
- Every layout requires a "visual_suggestion" detailing exactly what flowchart/diagram goes in the massive placeholder.
- Output ONLY valid JSON, no markdown fences or explanations.

JSON SCHEMA:
{
  "presentation_title": "...",
  "personality": "${personality}",
  "slides": [
    {
      "slide_number": 1,
      "layout": "aesthetic_title",
      "title": "Project/Topic Name",
      "subtitle": "A robust 3-sentence technical abstract explaining the core innovation, stack, and impact."
    },
    {
      "slide_number": 2,
      "layout": "aesthetic_split",
      "title": "Problem Statement",
      "bullets": [
        {"bold": "Key Point 1", "text": "25-30 words of extremely detailed context ensuring vertical space is filled completely."},
        {"bold": "Key Point 2", "text": "25-30 words explaining consequences, metrics, or current system failures in depth."},
        {"bold": "Key Point 3", "text": "25-30 words on why previous approaches fall short and what needs to change."}
      ],
      "visual_suggestion": "[ Diagram: User pain-point flowchart ]"
    },
    {
      "slide_number": 3,
      "layout": "aesthetic_grid",
      "title": "Technical Approach",
      "cards": [
        {
          "header": "Data Ingestion",
          "bullets": ["20 words detailing the pipeline", "20 words on scaling", "20 words on security"]
        },
        {"header":"...","bullets":["...","...","..."]},
        {"header":"...","bullets":["...","...","..."]},
        {"header":"...","bullets":["...","...","..."]}
      ]
    },
    {
      "slide_number": 4,
      "layout": "aesthetic_flow",
      "title": "System Architecture",
      "description": "A dense 50-word paragraph explaining the exact end-to-end data flow and logical architecture before displaying the huge diagram below.",
      "visual_suggestion": "[ Massive Flowchart: User -> API -> DB -> LLM ]"
    }
  ]
}`;

      const puterResp = await puter.ai.chat(userMsg);
      let rawText = typeof puterResp === 'string' ? puterResp : (puterResp?.text || puterResp?.message?.content || puterResp?.content || JSON.stringify(puterResp));
      if (typeof rawText !== 'string') rawText = String(rawText);

      const jsonMatch = rawText.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
          appendMsg(`⚠️ Puter.js returned invalid JSON. Falling back to backend...\n`);
          return false;
      }
      plan = JSON.parse(jsonMatch[0]);
      plan.personality = personality;

      const n = plan.total_slides || plan.slides?.length || '?';
      appendMsg(`📋 Plan ready! **"${plan.presentation_title}"** — ${n} slides\n`);
      appendMsg('─'.repeat(44) + '\n');
    } catch (puterErr) {
      appendMsg(`⚠️ Puter.js unavailable (${puterErr.message}) — switching to Groq...\n`);
      return false;
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/ppt/build', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ plan }),
      });
      if (!res.ok) throw new Error(`/ppt/build returned ${res.status}`);
      const reader  = res.body.getReader();
      const decoder = new TextDecoder('utf-8');
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        if (chunk.trim()) appendMsg(chunk);
      }
      return true;
    } catch (buildErr) {
      appendMsg(`❌ Build error: ${buildErr.message}\n`);
      return true;
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    const prompt = inputValue.trim();
    if (!prompt || isLoading) return;

    setInputValue('');
    setIsLoading(true);

    setMessages((prev) => [
      ...prev,
      { role: 'user', content: prompt },
      { role: 'assistant', content: '' },
    ]);

    try {
      if (isPPTRequest(prompt)) {
        let handled = await handlePPTWithPuter(prompt);
        if (!handled) {
          // Fallback to backend PPT generation
          const res = await fetch('http://127.0.0.1:8000/ppt/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt }),
          });
          if (!res.ok) throw new Error(`Backend PPT fallback returned ${res.status}`);
          const reader  = res.body.getReader();
          const decoder = new TextDecoder('utf-8');
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            if (chunk.trim()) appendMsg(chunk);
          }
        }
        return; // success or backend fallback finished — don't call /chat
      }

      // ── Standard /chat path (Groq) ──────────────────────────────────────
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) throw new Error(`Server returned ${response.status}`);

      const reader  = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const raw   = decoder.decode(value, { stream: true });
        const lines = raw.split('\n');
        const cleanLines = lines
          .map((line) => line.replace(/^data:\s*/, ''))
          .filter((line) => line !== '[DONE]');
        const cleanChunk = cleanLines.join('\n');
        if (!cleanChunk.trim()) continue;
        setMessages((prev) => {
          const copy = prev.map((m) => ({ ...m }));
          const last = copy[copy.length - 1];
          if (last && last.role === 'assistant') last.content += cleanChunk;
          return copy;
        });
      }
    } catch (err) {
      console.error('[Jarvis] fetch error:', err);
      setMessages((prev) => {
        const copy = prev.map((m) => ({ ...m }));
        const last = copy[copy.length - 1];
        if (last && last.role === 'assistant') {
          last.content = '⚠️ Could not reach Jarvis. Make sure the backend is running on port 8000.';
        }
        return copy;
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen sci-fi-bg text-white font-sans overflow-hidden">
      {/* Sidebar */}
      <div className="w-80 hidden md:block z-10 shrink-0">
        <MemorySidebar />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative z-0 p-4 pl-0">

        {/* Glass Panel */}
        <div className="flex-1 flex flex-col glass-panel rounded-2xl overflow-hidden relative shadow-[0_0_30px_rgba(0,243,255,0.05)] border-t border-b border-cyan-500/20">

          {/* Header */}
          <header className="p-4 bg-[#020611]/80 backdrop-blur-md border-b border-cyan-900/50 flex items-center justify-between z-10 w-full relative">
            <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-cyan-400 to-transparent opacity-50" />

            <h1 className="text-lg font-semibold md:hidden neon-text tracking-widest uppercase">Jarvis</h1>

            <div className="hidden md:flex items-center space-x-3">
              <span className="text-sm font-mono text-cyan-500 tracking-widest uppercase">System Uplink</span>
              <div className="flex items-center space-x-1">
                <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_5px_#00f3ff]" />
                <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_5px_#00f3ff]" style={{ animationDelay: '150ms' }} />
                <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_5px_#00f3ff]" style={{ animationDelay: '300ms' }} />
              </div>
            </div>

            <div className="flex items-center space-x-2 bg-cyan-900/20 px-3 py-1 rounded-full border border-cyan-800/50">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500 shadow-[0_0_5px_#34d399]" />
              </span>
              <span className="text-xs font-mono text-emerald-400">SECURE</span>
            </div>
          </header>

          {/* Messages */}
          <main className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar relative z-0">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-cyan-700 space-y-6">
                <div className="w-24 h-24 rounded-full border-2 border-cyan-500/30 flex items-center justify-center shadow-[0_0_30px_rgba(0,243,255,0.1)] relative">
                  <div className="absolute inset-0 rounded-full bg-cyan-500/5 blur-xl animate-pulse" />
                  <Bot size={48} className="text-cyan-400 opacity-80" />
                  <div className="absolute inset-[-10px] border border-cyan-500/20 rounded-full animate-[spin_8s_linear_infinite] border-t-transparent" />
                </div>
                <p className="text-xl font-medium text-cyan-300 tracking-widest uppercase font-mono">System Ready</p>
                <p className="text-sm font-mono text-cyan-600 text-center max-w-sm leading-relaxed">
                  Type any command — open apps, search the web, send WhatsApp messages,
                  check emails, control your PC, and more.
                </p>
              </div>
            )}

            <div className="w-full mx-auto space-y-6 relative">
              {messages.map((msg, idx) => (
                <ChatMessage key={idx} msg={msg} />
              ))}

              {/* Typing indicator — only show when response hasn't started yet */}
              {isLoading && messages[messages.length - 1]?.content === '' && (
                <div className="flex items-start">
                  <div className="glass-panel text-gray-200 rounded-2xl rounded-tl-none border-l-4 border-l-cyan-400 px-6 py-4 flex items-center space-x-3 w-[100px]">
                    <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce shadow-[0_0_5px_#00f3ff]" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce shadow-[0_0_5px_#00f3ff]" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce shadow-[0_0_5px_#00f3ff]" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} className="h-4" />
            </div>
          </main>
        </div>

        {/* Input + Status Bar */}
        <div className="mt-4 flex flex-col items-center w-full relative z-20 pb-4">

          <form onSubmit={handleSendMessage} className="w-full max-w-4xl relative flex items-center mb-4 group">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 via-blue-500/20 to-cyan-500/20 rounded-full blur group-focus-within:opacity-100 opacity-50 transition-opacity" />

            <div className="relative flex w-full bg-[#030a16] border border-cyan-500/40 rounded-full shadow-[0_0_15px_rgba(0,243,255,0.1)] focus-within:border-cyan-400 focus-within:shadow-[0_0_20px_rgba(0,243,255,0.3)] transition-all overflow-hidden items-center pl-6 pr-2 py-2">
              {/* Accent dot */}
              <div className="w-2 h-2 bg-cyan-500 rounded-full shadow-[0_0_5px_#00f3ff] animate-pulse shrink-0 ml-2" />

              {/* Upload Dropdown */}
              <div className="relative ml-2 flex items-center justify-center shrink-0 group">
                <button
                  type="button"
                  disabled={isLoading || isUploading}
                  className="p-2 rounded-full text-cyan-500 hover:text-white hover:bg-cyan-600 transition-all disabled:opacity-40"
                  title="Upload Document"
                >
                  {isUploading ? <Loader2 size={18} className="animate-spin text-cyan-400" /> : <Paperclip size={18} />}
                </button>
                
                {/* Hover Menu */}
                <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-40 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 bg-[#020611] border border-cyan-800/80 rounded-lg shadow-[0_0_15px_rgba(0,243,255,0.2)] overflow-hidden">
                  <button 
                    type="button"
                    onClick={() => {
                      fileInputRef.current.dataset.uploadType = 'assignment';
                      fileInputRef.current?.click();
                    }}
                    className="w-full text-left px-4 py-2 text-sm text-cyan-100 hover:bg-cyan-900/50 hover:text-white transition-colors border-b border-cyan-900/30 font-mono"
                  >
                    Assignment PDF
                  </button>
                  <button 
                    type="button"
                    onClick={() => {
                      fileInputRef.current.dataset.uploadType = 'general';
                      fileInputRef.current?.click();
                    }}
                    className="w-full text-left px-4 py-2 text-sm text-cyan-100 hover:bg-cyan-900/50 hover:text-white transition-colors font-mono"
                  >
                    General File
                  </button>
                </div>
              </div>

              <input 
                type="file" 
                ref={fileInputRef} 
                style={{ display: 'none' }} 
                data-upload-type="assignment"
                onChange={handleFileUpload} 
                accept=".pdf,.txt,.docx"
              />

              <input
                id="jarvis-command-input"
                type="text"
                className="flex-1 bg-transparent text-cyan-100 px-4 py-2 outline-none text-[15px] font-mono placeholder-cyan-800/70"
                placeholder={isLoading ? 'Processing...' : 'Enter operator command...'}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                disabled={isLoading}
                autoComplete="off"
                autoFocus
              />

              <button
                id="jarvis-send-btn"
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="p-2 rounded-full text-cyan-500 hover:text-white hover:bg-cyan-600 transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center bg-cyan-900/30 shrink-0"
              >
                {isLoading
                  ? <Loader2 size={18} className="animate-spin text-cyan-400" />
                  : <Send size={18} />
                }
              </button>
            </div>
          </form>

          {/* Status Bar */}
          <div className="relative flex items-center justify-center bg-[#020611]/80 backdrop-blur-md border border-cyan-900/60 rounded-full px-6 py-2 shadow-[0_0_15px_rgba(0,243,255,0.1)] gap-4 overflow-hidden">
            <div className="absolute left-0 top-0 h-full w-8 bg-gradient-to-r from-cyan-500/20 to-transparent" />
            <div className="absolute right-0 top-0 h-full w-8 bg-gradient-to-l from-cyan-500/20 to-transparent" />

            <span className={`text-xs font-mono tracking-widest opacity-70 ${isLoading ? 'text-cyan-300' : 'text-cyan-500'}`}>
              {isLoading ? 'Processing command...' : 'Awaiting operator command...'}
            </span>

            <div className="flex items-center h-4 gap-0.5">
              {[0, 1, 2].map((i) => (
                <div key={i} className={`waveform-bar ${isLoading ? 'opacity-100' : 'opacity-50'}`} />
              ))}
              <div className="w-6 h-6 rounded-full border border-cyan-500/50 flex items-center justify-center bg-cyan-900/30 mx-1 z-10 shadow-[0_0_10px_rgba(0,243,255,0.2)]">
                <Mic size={12} className={isLoading ? 'text-cyan-300' : 'text-cyan-400'} />
              </div>
              {[3, 4, 5].map((i) => (
                <div key={i} className={`waveform-bar ${isLoading ? 'opacity-100' : 'opacity-50'}`} />
              ))}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
