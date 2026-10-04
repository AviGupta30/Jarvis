// The Jarvis "arc reactor": a glowing orb with counter-rotating rings.
// Colours follow the active mode through the --accent / --accent-2 CSS variables.
export default function Orb({ size = 40, busy = false, rings = true, className = '' }) {
  return (
    <div className={`orb shrink-0 ${busy ? 'is-busy' : ''} ${className}`} style={{ width: size, height: size }} aria-hidden>
      <div className="orb-glow" />
      {rings && <div className="orb-ring" />}
      {rings && size >= 64 && <div className="orb-ring r2" />}
      <div className="orb-core" />
    </div>
  );
}
