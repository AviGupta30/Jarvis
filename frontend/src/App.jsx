import { useState, useRef, useEffect } from 'react';
import { Send, Bot, Loader2, Mic } from 'lucide-react';
import MemorySidebar from './MemorySidebar';
import ChatMessage from './ChatMessage';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll whenever messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    const prompt = inputValue.trim();
    if (!prompt || isLoading) return;

    setInputValue('');
    setIsLoading(true);

    // Add user message + empty assistant placeholder in a single update
    // to prevent React batching from creating index race conditions
    setMessages((prev) => [
      ...prev,
      { role: 'user', content: prompt },
      { role: 'assistant', content: '' },
    ]);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const raw = decoder.decode(value, { stream: true });

        // Strip SSE "data: " prefix that FastAPI StreamingResponse may add
        const cleanChunk = raw
          .split('\n')
          .map((line) => line.replace(/^data:\s*/, ''))
          .filter((line) => line !== '[DONE]')
          .join('\n');

        if (!cleanChunk) continue;

        // Always update the LAST message (which is always the assistant placeholder)
        setMessages((prev) => {
          const copy = prev.map((m) => ({ ...m })); // shallow-clone each item
          const last = copy[copy.length - 1];
          if (last && last.role === 'assistant') {
            last.content += cleanChunk;
          }
          return copy;
        });
      }
    } catch (err) {
      console.error('[Jarvis] fetch error:', err);
      setMessages((prev) => {
        const copy = prev.map((m) => ({ ...m }));
        const last = copy[copy.length - 1];
        if (last && last.role === 'assistant') {
          last.content =
            '⚠️ Could not reach Jarvis. Make sure the backend server is running on port 8000.';
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
              <div className="w-2 h-2 bg-cyan-500 rounded-full shadow-[0_0_5px_#00f3ff] animate-pulse shrink-0" />

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
