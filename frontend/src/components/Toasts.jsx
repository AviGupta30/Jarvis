import { motion, AnimatePresence } from 'framer-motion';
import { Bell, CircleCheck, CircleAlert, Info, X } from 'lucide-react';

const STYLE = {
  alert: { icon: Bell, color: '#fbbf24' },
  success: { icon: CircleCheck, color: '#34d399' },
  error: { icon: CircleAlert, color: '#fb7185' },
  info: { icon: Info, color: '#22d3ee' },
};

// Stacked notifications (top-right). Screen-watcher alerts from /alerts land here too.
export default function Toasts({ toasts, onDismiss }) {
  return (
    <div className="fixed top-4 right-4 z-[200] flex flex-col gap-2 w-[min(380px,calc(100vw-2rem))] pointer-events-none">
      <AnimatePresence initial={false}>
        {toasts.map(t => {
          const s = STYLE[t.type] || STYLE.info;
          const Icon = s.icon;
          return (
            <motion.div key={t.id} layout
              initial={{ opacity: 0, x: 40, scale: 0.96 }} animate={{ opacity: 1, x: 0, scale: 1 }} exit={{ opacity: 0, x: 40, scale: 0.96 }}
              transition={{ type: 'spring', stiffness: 380, damping: 30 }}
              className="pointer-events-auto glass-strong rounded-2xl p-3.5 flex gap-3 items-start">
              <span className="grid place-items-center w-8 h-8 rounded-xl shrink-0" style={{ color: s.color, background: `${s.color}1a` }}>
                <Icon size={16} />
              </span>
              <div className="flex-1 min-w-0">
                {t.title && <p className="text-[13px] font-medium text-white">{t.title}</p>}
                <p className="text-[12.5px] text-ink-200 leading-snug break-words">{t.text}</p>
              </div>
              <button onClick={() => onDismiss(t.id)} className="p-1 rounded-md text-ink-400 hover:text-white hover:bg-white/5">
                <X size={14} />
              </button>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
