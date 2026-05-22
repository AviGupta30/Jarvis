import { useState } from 'react';
import { Database, Loader2, CheckCircle2, Cpu, Wifi, Mic } from 'lucide-react';

export default function MemorySidebar() {
  const [content, setContent] = useState('');
  const [isIngesting, setIsIngesting] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);

  const handleIngest = async (e) => {
    e.preventDefault();
    if (!content.trim() || isIngesting) return;

    setIsIngesting(true);
    setStatusMessage(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/ingest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: content.trim() }),
      });

      if (!response.ok) {
        throw new Error("Failed to ingest memory");
      }

      setContent('');
      setStatusMessage({ type: 'success', text: 'Memory saved successfully!' });
      
      setTimeout(() => {
        setStatusMessage(null);
      }, 3000);
    } catch (error) {
      console.error("Ingestion error:", error);
      setStatusMessage({ type: 'error', text: 'Failed to save memory.' });
    } finally {
      setIsIngesting(false);
    }
  };

  return (
    <div className="flex flex-col h-full glass-panel p-5 text-gray-200 rounded-2xl m-4 overflow-hidden relative">
      {/* Background glow for the panel itself */}
      <div className="absolute top-0 left-0 w-full h-full bg-cyan-900/10 pointer-events-none"></div>
      
      <h2 className="text-2xl font-bold mb-6 text-center neon-text tracking-wider">
        Jarvis Core
      </h2>
      
      {/* 3D Sphere Representation */}
      <div className="flex justify-center mb-8 relative">
        <div className="w-48 h-48 rounded-full flex items-center justify-center relative">
           <div className="absolute inset-0 rounded-full bg-cyan-500/20 blur-xl animate-pulse"></div>
           <img src="/core-sphere.png" alt="Jarvis Core" className="w-full h-full object-cover rounded-full z-10" />
           
           {/* Futuristic rings */}
           <div className="absolute inset-[-10px] border border-cyan-500/30 rounded-full animate-[spin_10s_linear_infinite]"></div>
           <div className="absolute inset-[-20px] border border-cyan-500/10 rounded-full animate-[spin_15s_linear_reverse_infinite]"></div>
        </div>
      </div>

      {/* System Stats */}
      <div className="flex justify-between items-end mb-8 px-2 space-x-2">
         <div className="flex flex-col w-1/3">
            <div className="flex justify-between text-[10px] font-mono text-cyan-400 mb-1 tracking-widest">
               <span>CPU:</span>
               <span>42%</span>
            </div>
            <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
               <div className="h-full bg-cyan-400 w-[42%] shadow-[0_0_5px_#00f3ff]"></div>
            </div>
            {/* tick marks below */}
            <div className="flex justify-between mt-0.5">
               {[...Array(8)].map((_, i) => <div key={i} className="w-[1px] h-1 bg-cyan-900"></div>)}
            </div>
         </div>
         
         <div className="flex flex-col w-1/3">
            <div className="flex justify-between text-[10px] font-mono text-cyan-400 mb-1 tracking-widest">
               <span>NET:</span>
               <span>890 Mbps</span>
            </div>
            <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
               <div className="h-full bg-cyan-400 w-[80%] shadow-[0_0_5px_#00f3ff]"></div>
            </div>
            <div className="flex justify-between mt-0.5">
               {[...Array(8)].map((_, i) => <div key={i} className="w-[1px] h-1 bg-cyan-900"></div>)}
            </div>
         </div>

         <div className="flex flex-col w-1/3">
            <div className="flex justify-between text-[10px] font-mono text-cyan-400 mb-1 tracking-widest">
               <span>VOICE:</span>
               <span className="text-emerald-400">ACTIVE</span>
            </div>
            <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
               <div className="h-full bg-emerald-400 w-[100%] shadow-[0_0_5px_#34d399]"></div>
            </div>
            <div className="flex justify-between mt-0.5">
               {[...Array(8)].map((_, i) => <div key={i} className="w-[1px] h-1 bg-cyan-900"></div>)}
            </div>
         </div>
      </div>
      
      <div className="flex-1 flex flex-col z-10">
        <h3 className="text-[13px] font-semibold text-cyan-300 uppercase tracking-widest mb-3">
          Memory Ingestion
        </h3>
        
        <form onSubmit={handleIngest} className="flex flex-col gap-4">
          <div className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl opacity-20 group-hover:opacity-40 blur transition duration-200"></div>
            <textarea
              className="relative w-full bg-[#051024] border border-cyan-800/50 rounded-xl p-3 text-sm text-cyan-100 focus:outline-none focus:border-cyan-400 focus:shadow-[0_0_10px_rgba(0,243,255,0.3)] transition-all resize-none custom-scrollbar font-mono placeholder-cyan-700/50"
              rows={4}
              placeholder="Analyze dataset_alpha_7..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
          </div>
          
          <button
            type="submit"
            disabled={!content.trim() || isIngesting}
            className="relative flex items-center justify-center gap-2 w-full bg-transparent border border-cyan-500 text-cyan-300 font-bold py-3 px-4 transition-all disabled:opacity-50 hover:bg-cyan-900/40 hover:shadow-[0_0_15px_rgba(0,243,255,0.4)] disabled:hover:bg-transparent overflow-hidden clip-path-hexagon"
            style={{ clipPath: 'polygon(5% 0, 95% 0, 100% 50%, 95% 100%, 5% 100%, 0 50%)' }}
          >
            {/* Hexagon shape effect using clip-path */}
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-600/20 to-blue-600/20"></div>
            {isIngesting ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                PROCESSING...
              </>
            ) : (
              'SAVE TO MEMORY'
            )}
          </button>
        </form>

        {statusMessage && (
          <div className={`mt-4 p-3 rounded flex items-start gap-2 text-xs font-mono ${
            statusMessage.type === 'success' ? 'bg-emerald-900/30 text-emerald-400 border border-emerald-800' : 'bg-red-900/30 text-red-400 border border-red-800'
          }`}>
            {statusMessage.type === 'success' && <CheckCircle2 size={14} className="mt-0.5 flex-shrink-0" />}
            <p>{statusMessage.text}</p>
          </div>
        )}
      </div>
    </div>
  );
}
