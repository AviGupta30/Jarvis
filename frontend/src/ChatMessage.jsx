import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function ChatMessage({ msg }) {
  const isUser = msg.role === 'user';

  return (
    <div className={`flex items-start w-full ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
      <div
        className={`max-w-[85%] sm:max-w-[75%] px-6 py-4 relative shadow-lg ${
          isUser
            ? 'bg-[#00f3ff]/10 text-cyan-100 rounded-2xl rounded-br-none border border-[#00f3ff]/50 shadow-[0_0_15px_rgba(0,243,255,0.2)]'
            : 'glass-panel text-gray-200 rounded-2xl rounded-tl-none border-l-4 border-l-cyan-400'
        }`}
      >
        {/* Decorative corner accents for assistant */}
        {!isUser && (
          <>
            <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-cyan-400"></div>
            <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-cyan-400"></div>
          </>
        )}
        
        {/* decorative glowing dot for user */}
        {isUser && (
          <div className="absolute -right-2 -bottom-2 w-4 h-4 bg-cyan-400 rounded-full blur-[4px]"></div>
        )}

        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || '');
              return !inline && match ? (
                <div className="my-4 rounded-xl overflow-hidden border border-cyan-900/60 shadow-[0_4px_15px_rgba(0,0,0,0.5)]">
                  <div className="bg-[#050b14] text-cyan-400 px-4 py-2 text-xs font-mono uppercase border-b border-cyan-900/60 flex justify-between tracking-widest">
                    {match[1]}
                  </div>
                  <SyntaxHighlighter
                    {...props}
                    style={vscDarkPlus}
                    language={match[1]}
                    PreTag="div"
                    customStyle={{ margin: 0, borderRadius: 0, background: '#0a101d' }}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                </div>
              ) : (
                <code className="bg-cyan-900/30 text-cyan-300 px-1.5 py-0.5 rounded text-[13px] font-mono border border-cyan-800/50" {...props}>
                  {children}
                </code>
              );
            },
            img: ({ node, ...props }) => {
              const isVideo = props.src && props.src.match(/\.(mp4|webm|ogg|avi|mov|mkv)$/i);
              return (
                <div className="my-4 flex flex-col items-center border border-cyan-500/40 bg-[#061022]/80 rounded-xl overflow-hidden shadow-[0_0_15px_rgba(0,243,255,0.1)]">
                  {isVideo ? (
                    <video controls src={props.src} className="max-w-full max-h-[400px]" />
                  ) : (
                    <img src={props.src} alt={props.alt} className="max-w-full max-h-[400px] object-contain" />
                  )}
                  <div className="w-full bg-[#050b14] p-3 border-t border-cyan-900/60 flex justify-between items-center">
                    <span className="text-xs font-mono text-cyan-500">{isVideo ? 'VIDEO RENDERED' : 'IMAGE RENDERED'}</span>
                    <a
                      href={props.src}
                      download
                      className="px-4 py-1.5 text-xs font-mono bg-cyan-900/40 hover:bg-cyan-600 hover:text-white text-cyan-300 border border-cyan-700/50 rounded transition-colors"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Download
                    </a>
                  </div>
                </div>
              );
            },
            p: ({ node, ...props }) => <p className="mb-3 last:mb-0 leading-relaxed text-[15px]" {...props} />,
            ul: ({ node, ...props }) => <ul className="list-disc ml-5 mb-3 space-y-1 text-gray-300" {...props} />,
            ol: ({ node, ...props }) => <ol className="list-decimal ml-5 mb-3 space-y-1 text-gray-300" {...props} />,
            li: ({ node, ...props }) => <li className="leading-relaxed" {...props} />,
            a: ({ node, ...props }) => <a className="text-cyan-400 hover:text-cyan-300 hover:shadow-[0_0_5px_rgba(0,243,255,0.5)] transition-all underline decoration-cyan-500/50" target="_blank" rel="noopener noreferrer" {...props} />,
            
            // Custom Table styling for sci-fi look
            table: ({ node, ...props }) => (
              <div className="my-4 rounded-xl overflow-hidden border border-cyan-500/40 bg-[#061022]/80 shadow-[0_0_15px_rgba(0,243,255,0.1)]">
                <table className="min-w-full divide-y divide-cyan-800/50 text-sm font-mono" {...props} />
              </div>
            ),
            thead: ({ node, ...props }) => <thead className="bg-[#00f3ff]/10" {...props} />,
            th: ({ node, ...props }) => <th className="px-4 py-3 text-left font-semibold text-cyan-300 uppercase tracking-widest border-b border-cyan-500/40" {...props} />,
            tbody: ({ node, ...props }) => <tbody className="divide-y divide-cyan-900/30" {...props} />,
            tr: ({ node, ...props }) => <tr className="hover:bg-cyan-900/20 transition-colors" {...props} />,
            td: ({ node, ...props }) => <td className="px-4 py-3 whitespace-nowrap text-cyan-100/80 border-r border-cyan-900/30 last:border-r-0" {...props} />,
          }}
        >
          {msg.content}
        </ReactMarkdown>
      </div>
    </div>
  );
}
