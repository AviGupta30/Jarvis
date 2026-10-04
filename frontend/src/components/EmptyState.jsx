import { motion } from 'framer-motion';
import { ArrowUpRight } from 'lucide-react';
import Orb from './Orb';

const greeting = () => {
  const h = new Date().getHours();
  if (h < 5) return 'Working late';
  if (h < 12) return 'Good morning';
  if (h < 17) return 'Good afternoon';
  return 'Good evening';
};

const container = { hidden: {}, show: { transition: { staggerChildren: 0.06, delayChildren: 0.15 } } };
const item = { hidden: { opacity: 0, y: 12 }, show: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 260, damping: 24 } } };

export default function EmptyState({ mode, onPick }) {
  const Icon = mode.icon;
  return (
    <div className="min-h-full flex flex-col items-center justify-center px-4 pt-10 pb-6">
      <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ type: 'spring', stiffness: 160, damping: 18 }}
        className="mb-9 animate-float">
        <Orb size={96} />
      </motion.div>

      <motion.h1 initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}
        className="text-center text-[34px] sm:text-[44px] leading-[1.1] font-medium tracking-[-0.03em] text-white">
        {greeting()}, <span className="font-serif italic font-normal text-gradient pr-1">Sir.</span>
      </motion.h1>

      <motion.div key={mode.id} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
        className="mt-3 flex items-center gap-2 text-[15px] text-ink-300">
        {mode.id === 'chat'
          ? <span>How can I help you today?</span>
          : <>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[12.5px] font-medium border"
                style={{ color: mode.accent, borderColor: `${mode.accent}40`, background: `${mode.accent}12` }}>
                <Icon size={13} /> {mode.label}
              </span>
              <span className="hidden sm:inline">{mode.tagline}</span>
            </>}
      </motion.div>

      <motion.div key={`s-${mode.id}`} variants={container} initial="hidden" animate="show"
        className="mt-10 w-full max-w-3xl grid grid-cols-1 sm:grid-cols-2 gap-3">
        {mode.suggestions.map((s, i) => (
          <motion.button key={i} variants={item} whileHover={{ y: -2 }} whileTap={{ scale: 0.98 }}
            onClick={() => onPick(s)}
            className="group text-left p-4 rounded-2xl glass hover:bg-white/[0.06] hover:border-white/[0.14] transition-colors">
            <div className="flex items-center justify-between">
              <p className="text-[13.5px] font-medium text-white">{s.title}</p>
              <ArrowUpRight size={15} className="text-ink-400 opacity-0 -translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all" style={{ color: mode.accent }} />
            </div>
            <p className="mt-1 text-[12.5px] text-ink-400 line-clamp-2">{s.text || mode.placeholder}</p>
          </motion.button>
        ))}
      </motion.div>
    </div>
  );
}
