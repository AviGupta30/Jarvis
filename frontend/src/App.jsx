import { useState, useRef, useEffect } from 'react';
import { Send, Bot, Loader2, Mic, Paperclip } from 'lucide-react';
import MemorySidebar from './MemorySidebar';
import ChatMessage from './ChatMessage';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (!files || files.length === 0) return;
    
    setIsUploading(true);
    
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
          const type = fileInputRef.current.dataset.uploadType;
          if (type === 'assignment') {
            setInputValue(prev => prev ? `${prev} | do my assignment from ${data.filename}` : `do my assignment from ${data.filename}`);
          }
          
          setUploadedFiles(prev => [...prev, {
            name: file.name,
            path: data.path,
            url: URL.createObjectURL(file)
          }]);
        } else {
          alert("Upload failed: " + data.error);
        }
      } catch (err) {
        console.error(err);
        alert(`Failed to upload file ${file.name}`);
      }
    }
    
    setIsUploading(false);
    e.target.value = ''; // Reset input
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
  const isPPTRequest = (text) => {
    const lower = text.toLowerCase();
    const exactMatch = PPT_KW.some(kw => lower.includes(kw));
    // Powerful regex to catch variations like "make me a 10 slide presentation", "give me a cool ppt", "use light color theme on this ppt", "change the presentation"
    const regexMatch = /(?:create|make|build|generate|design|prepare|give|need|want|use|change|update|modify|edit|convert|theme).*(?:ppt|presentation|slide|deck|powerpoint|theme|color)/i.test(lower);
    return exactMatch || regexMatch;
  };

  const STYLE_MAP = {
    'cyber dark':'cyber_dark','cyber_dark':'cyber_dark',
    'midnight executive':'midnight_exec','midnight_exec':'midnight_exec',
    'solar flare':'solar_flare','solar_flare':'solar_flare',
    'arctic clean':'arctic_clean','arctic_clean':'arctic_clean',
    'forest calm':'forest_calm','forest_calm':'forest_calm',
    'ocean gradient':'ocean_gradient','ocean_gradient':'ocean_gradient',
    'velvet noir':'velvet_noir','velvet_noir':'velvet_noir',
    'charcoal minimal':'charcoal_minimal','charcoal_minimal':'charcoal_minimal',
    'synthwave':'synthwave',
    'aurora':'aurora',
    'hacker terminal':'hacker_terminal','hacker_terminal':'hacker_terminal',
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
    synthwave:'Neon pink + purple. Retro cyber, 80s aesthetic.',
    aurora:'Deep teal + bright green. Nature tech, biological systems.',
    hacker_terminal:'Pitch black + lime green. Matrix style, raw code.'
  };

  const autoPersonality = (text) => {
    const t = text.toLowerCase();
    if (/synthwave|retro|neon|80s/.test(t)) return 'synthwave';
    if (/aurora|bio|clean energy|nature tech/.test(t)) return 'aurora';
    if (/hacker|matrix|terminal|cybersecurity/.test(t)) return 'hacker_terminal';
    if (/cyber|dark|hacker|neon|matrix|tech/.test(t)) return 'cyber_dark';
    if (/light|white|clean|minimal|snow|arctic/.test(t)) return 'arctic_clean';
    if (/midnight|exec|corporate|professional|business/.test(t)) return 'midnight_exec';
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

  // Puter.js disabled due to quota limits and hallucination issues.
  // Generation is now perfectly chunked and handled by the robust Python backend.

  const handleSendMessage = async (e) => {
    e.preventDefault();
    const prompt = inputValue.trim();
    if (!prompt && uploadedFiles.length === 0 && !isLoading) return;

    setInputValue('');
    setIsLoading(true);

    const recentUserMessages = messages.filter(m => m.role === 'user').map(m => m.content);
    const recentPrompts = recentUserMessages.slice(-3).join(" | ");

    const attachedTags = uploadedFiles.map(f => {
      const p = f.path.replace(/\\/g, '/');
      return f.description ? `[ATTACHED_FILE: ${p} | DESCRIPTION: ${f.description}]` : `[ATTACHED_FILE: ${p}]`;
    }).join("\n");
    const promptToSend = attachedTags ? `${prompt}\n\n${attachedTags}`.trim() : prompt;
    const uiDisplayMessage = prompt || (uploadedFiles.length > 0 ? "Uploaded files" : "");
    const attachedFiles = [...uploadedFiles];

    setMessages((prev) => [
      ...prev,
      { role: 'user', content: uiDisplayMessage },
      { role: 'assistant', content: '' },
    ]);
    
    setUploadedFiles([]);

    try {
      if (isPPTRequest(prompt)) {
        appendMsg('🚀 Initializing Deep Chunked PPT Generation...\n');
        
        const res = await fetch('http://127.0.0.1:8000/ppt/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: promptToSend }),
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
        return; // success or backend finished
      }

      // ── Standard /chat path (Groq) ──────────────────────────────────────
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: promptToSend }),
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
          // Append the error instead of overwriting, so we don't lose Puter.js logs
          last.content += `\n\n⚠️ Could not complete request: ${err.message}. Make sure the backend is running on port 8000.`;
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

          <form onSubmit={handleSendMessage} className="w-full max-w-4xl relative flex flex-col gap-2 mb-4 group">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 via-blue-500/20 to-cyan-500/20 rounded-[32px] blur group-focus-within:opacity-100 opacity-50 transition-opacity" />

            {uploadedFiles.length > 0 && (
              <div className="relative flex gap-3 px-4 py-3 overflow-x-auto w-full bg-[#030a16] border border-cyan-500/40 rounded-[24px] shadow-[0_0_15px_rgba(0,243,255,0.1)] z-10">
                {uploadedFiles.map((f, i) => (
                  <div key={i} className="relative group/img shrink-0 rounded-lg overflow-visible h-16 border border-cyan-700 bg-cyan-950/40 flex items-center p-1 gap-2">
                    {f.name.match(/\.(png|jpg|jpeg|webp)$/i) ? (
                      <img src={f.url} alt={f.name} className="h-full w-14 object-cover rounded-md" />
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
                      className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 w-5 h-5 flex items-center justify-center text-[10px] shadow-lg hover:bg-red-600 transition-colors z-20"
                    >✕</button>
                  </div>
                ))}
              </div>
            )}

            <div className="relative flex w-full bg-[#030a16] border border-cyan-500/40 rounded-full shadow-[0_0_15px_rgba(0,243,255,0.1)] focus-within:border-cyan-400 focus-within:shadow-[0_0_20px_rgba(0,243,255,0.3)] transition-all overflow-hidden items-center pl-6 pr-2 py-2 z-10">
              {/* Accent dot */}
              <div className="w-2 h-2 bg-cyan-500 rounded-full shadow-[0_0_5px_#00f3ff] animate-pulse shrink-0 ml-2" />

              {/* Upload Dropdown */}
              <div className="relative ml-2 flex items-center justify-center shrink-0 group">
                <button
                  type="button"
                  disabled={isLoading || isUploading}
                  onClick={() => {
                    fileInputRef.current.dataset.uploadType = 'general';
                    fileInputRef.current?.click();
                  }}
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
                accept=".pdf,.txt,.docx,.png,.jpg,.jpeg,.webp"
                multiple
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
