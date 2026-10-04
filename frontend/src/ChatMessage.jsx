import { memo, useState } from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check, RefreshCw, Download, FileText, ExternalLink, FilePen, Info } from 'lucide-react';
import Orb from './components/Orb';
import DagPlanPanel from './DagPlanPanel';
import { MODE_BY_ID, isImage } from './modes';

function useCopy() {
  const [copied, setCopied] = useState(false);
  const copy = async (text) => {
    try { await navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 1500); } catch { /* clipboard blocked */ }
  };
  return [copied, copy];
}

function CodeBlock({ lang, code }) {
  const [copied, copy] = useCopy();
  return (
    <div className="my-4 rounded-2xl overflow-hidden border border-white/[0.08] bg-[#0b0d14]">
      <div className="flex items-center justify-between px-4 h-9 border-b border-white/[0.06] bg-white/[0.02]">
        <span className="text-[11.5px] font-mono text-ink-400">{lang}</span>
        <button onClick={() => copy(code)} className="flex items-center gap-1.5 text-[11.5px] text-ink-400 hover:text-white transition-colors">
          {copied ? <><Check size={13} className="text-emerald-400" /> Copied</> : <><Copy size={13} /> Copy</>}
        </button>
      </div>
      <SyntaxHighlighter style={vscDarkPlus} language={lang} PreTag="div"
        customStyle={{ margin: 0, padding: '14px 16px', background: 'transparent', fontSize: '13px', lineHeight: 1.65 }}
        codeTagProps={{ style: { fontFamily: 'var(--font-mono)' } }}>
        {code}
      </SyntaxHighlighter>
    </div>
  );
}

const FILE_RX = /\.(pptx|potx|pdf|docx|xlsx|csv|zip|html|png|jpe?g|webp|mp4|mov|webm)(\?|#|$)/i;

const mdComponents = {
  pre: ({ children }) => <>{children}</>,
  code({ className, children }) {
    const match = /language-([\w+-]+)/.exec(className || '');
    const text = String(children ?? '');
    if (match || text.includes('\n')) return <CodeBlock lang={match?.[1] || 'text'} code={text.replace(/\n$/, '')} />;
    return <code className="inline-code">{children}</code>;
  },
  img: ({ src, alt }) => {
    const props = { src, alt };
    const isVideo = /\.(mp4|webm|ogg|avi|mov|mkv)$/i.test(props.src || '');
    return (
      <span className="block my-4 rounded-2xl overflow-hidden border border-white/[0.08] bg-black/30 w-fit max-w-full">
        {isVideo
          ? <video controls src={props.src} className="max-w-full max-h-[420px]" />
          : <a href={props.src} target="_blank" rel="noopener noreferrer"><img src={props.src} alt={props.alt} className="max-w-full max-h-[420px] object-contain" /></a>}
        <span className="flex items-center justify-between gap-6 px-3.5 py-2 border-t border-white/[0.06] bg-white/[0.02]">
          <span className="text-[11.5px] text-ink-400 truncate">{props.alt || (isVideo ? 'Video' : 'Image')}</span>
          <a href={props.src} download target="_blank" rel="noopener noreferrer" className="!no-underline flex items-center gap-1.5 text-[12px] !text-ink-200 hover:!text-white">
            <Download size={13} /> Download
          </a>
        </span>
      </span>
    );
  },
  a: ({ href = '', title, children }) => {
    const props = { title };
    if (href.includes('/resume/editor')) {
      return (
        <a href={href} target="_blank" rel="noopener noreferrer" {...props}
          className="!no-underline inline-flex items-center gap-2 my-1 px-3.5 py-2 rounded-xl text-[13px] font-medium !text-ink-950 bg-amber-300 hover:bg-amber-200 transition-colors">
          <FilePen size={14} /> {children}
        </a>
      );
    }
    if (FILE_RX.test(href)) {
      const ext = (href.match(FILE_RX)?.[1] || '').toUpperCase();
      return (
        <a href={href} target="_blank" rel="noopener noreferrer" {...props}
          className="!no-underline inline-flex items-center gap-2.5 my-1 pl-1.5 pr-3 py-1.5 rounded-xl border border-white/10 bg-white/[0.04] hover:bg-white/[0.08] hover:border-white/20 transition-colors align-middle">
          <span className="grid place-items-center w-7 h-7 rounded-lg bg-[var(--accent-soft)] text-[var(--accent)]"><FileText size={14} /></span>
          <span className="text-[13px] !text-white">{children}</span>
          <span className="text-[10px] font-mono text-ink-400">{ext}</span>
          <ExternalLink size={12} className="text-ink-400" />
        </a>
      );
    }
    return <a href={href} target="_blank" rel="noopener noreferrer" {...props}>{children}</a>;
  },
  table: ({ children }) => (
    <div className="my-4 overflow-x-auto custom-scrollbar rounded-2xl border border-white/[0.08] bg-white/[0.015]">
      <table>{children}</table>
    </div>
  ),
};

function Attachments({ files, align }) {
  if (!files?.length) return null;
  return (
    <div className={`flex flex-wrap gap-2 mb-2 ${align === 'right' ? 'justify-end' : ''}`}>
      {files.map((f, i) => (
        f.url && isImage(f.name) ? (
          <div key={i} className="relative rounded-2xl overflow-hidden border border-white/10 bg-black/30">
            <img src={f.url} alt={f.name} className="h-32 w-auto min-w-24 max-w-[220px] object-cover" />
            {(f.description || f.label) && (
              <p className="absolute bottom-0 inset-x-0 px-2.5 py-1.5 text-[11px] text-white bg-gradient-to-t from-black/80 to-transparent truncate">
                {f.label ? <b className="font-medium">{f.label}</b> : null}{f.label && f.description ? ' · ' : ''}{f.description}
              </p>
            )}
          </div>
        ) : (
          <div key={i} className="flex items-center gap-2.5 pl-1.5 pr-3 py-1.5 rounded-2xl border border-white/10 bg-white/[0.04] max-w-[260px]">
            <span className="grid place-items-center w-8 h-8 rounded-xl bg-white/[0.06] text-ink-200"><FileText size={15} /></span>
            <div className="min-w-0">
              <p className="text-[12.5px] text-white truncate">{f.name}</p>
              <p className="text-[10.5px] text-ink-400">{f.label || (f.name.split('.').pop() || '').toUpperCase()}</p>
            </div>
          </div>
        )
      ))}
    </div>
  );
}

function ChatMessage({ msg, isStreaming, canRegenerate, onRegenerate }) {
  const [copied, copy] = useCopy();
  const mode = msg.mode && msg.mode !== 'chat' ? MODE_BY_ID[msg.mode] : null;

  if (msg.role === 'user') {
    return (
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ type: 'spring', stiffness: 300, damping: 28 }}
        className="flex flex-col items-end">
        <Attachments files={msg.attachedFiles} align="right" />
        {msg.content && (
          <div className="max-w-[85%] sm:max-w-[75%] px-4 py-2.5 rounded-3xl rounded-br-lg bg-white/[0.07] border border-white/[0.08] text-[15px] leading-relaxed text-ink-100 whitespace-pre-wrap break-words">
            {msg.content}
          </div>
        )}
        {mode && (
          <span className="mt-1.5 inline-flex items-center gap-1 text-[11px]" style={{ color: mode.accent }}>
            <mode.icon size={11} /> {mode.label}
          </span>
        )}
      </motion.div>
    );
  }

  const empty = !msg.content;
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ type: 'spring', stiffness: 300, damping: 28 }}
      className="group flex gap-3.5 sm:gap-4">
      <div className="pt-0.5"><Orb size={28} busy={isStreaming} rings={false} /></div>
      <div className="flex-1 min-w-0">
        <p className="text-[13px] font-medium text-ink-200 mb-1.5 h-[22px] flex items-center">Jarvis</p>

        {msg.dag?.plan && (
          <DagPlanPanel nodes={msg.dag.plan.nodes} nodeStates={msg.dag.nodeStates} summary={msg.dag.plan.summary}
            waveCount={msg.dag.plan.waveCount} isComplete={msg.dag.complete} />
        )}

        {empty && isStreaming ? (
          <div className="flex items-center gap-3 h-7">
            <span className="dot-pulse flex gap-1"><span /><span /><span /></span>
            <span className="text-[13.5px] text-shimmer">{mode ? `${mode.label} is working…` : 'Thinking…'}</span>
          </div>
        ) : (
          <div className={`prose-jarvis ${isStreaming ? 'caret' : ''}`}>
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{msg.content}</ReactMarkdown>
          </div>
        )}

        {msg.note && (
          <p className="mt-3 flex items-start gap-2 text-[12px] text-ink-400"><Info size={13} className="mt-0.5 shrink-0" /> {msg.note}</p>
        )}

        {!isStreaming && !empty && (
          <div className="mt-2 -ml-1.5 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 focus-within:opacity-100 transition-opacity">
            <button onClick={() => copy(msg.content)} title="Copy" className="p-1.5 rounded-lg text-ink-400 hover:text-white hover:bg-white/[0.06]">
              {copied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
            </button>
            {canRegenerate && (
              <button onClick={onRegenerate} title="Regenerate" className="p-1.5 rounded-lg text-ink-400 hover:text-white hover:bg-white/[0.06]">
                <RefreshCw size={14} />
              </button>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default memo(ChatMessage);
