// Jarvis "modes" — like Gemini's Deep Research / Image modes.
// Each mode decides: which uploads the + menu offers, which option pills show,
// the starter suggestions, and how the typed text is turned into a backend request.
// Everything still ends up at POST /chat (or /ppt/create for plain decks), so the
// backend needs no changes.
import {
  MessageSquare, FileUser, Presentation, Telescope, GraduationCap, WandSparkles,
  Paperclip, LayoutTemplate, User, Building2, FileText, Palette, ImagePlus, FileUp,
} from 'lucide-react';

const IMG = '.png,.jpg,.jpeg,.webp';
const DOCS = '.pdf,.docx,.txt,.md';
const ANY = '.pdf,.txt,.docx,.md,.csv,.json,.pptx,.potx,.png,.jpg,.jpeg,.webp,.gif,.mp4,.avi,.mov,.mkv';

const RESUME_TEMPLATES = ['elegant', 'modern', 'minimal', 'creative', 'executive', 'tech', 'wave', 'corporate', 'campus'];
const PPT_THEMES = [
  ['minimal_light', 'Minimal Light'], ['editorial', 'Editorial'], ['slate_corporate', 'Slate Corporate'],
  ['ocean_light', 'Ocean Light'], ['forest', 'Forest'], ['medical', 'Medical'], ['lavender', 'Lavender'],
  ['mono_bold', 'Mono Bold'], ['midnight', 'Midnight'], ['neon_pitch', 'Neon Pitch'], ['cosmic', 'Cosmic'],
  ['ember', 'Ember'], ['emerald_dark', 'Emerald Dark'],
];
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);

export const MODES = [
  {
    id: 'chat', label: 'Chat', icon: MessageSquare, accent: '#22d3ee', accent2: '#818cf8',
    tagline: 'Ask anything, control your PC, run any tool',
    placeholder: 'Ask Jarvis anything…',
    uploads: [
      { kind: 'general', label: 'Upload files', hint: 'Images, documents, videos', icon: Paperclip, accept: ANY, multiple: true, describe: true },
    ],
    options: [],
    suggestions: [
      { title: 'Morning brief', text: 'Good morning Jarvis, give me my brief' },
      { title: 'Check my inbox', text: 'Check my emails and summarise the important ones' },
      { title: "What's on my screen?", text: "What's on my screen right now?" },
      { title: 'Play some music', text: 'Play lofi beats on Spotify' },
    ],
  },
  {
    id: 'resume', label: 'Resume Creator', icon: FileUser, accent: '#fbbf24', accent2: '#fb7185',
    tagline: 'Copy any resume design, or pick a template — PDF, PNG and an editable copy',
    placeholder: 'Paste your details, or describe a change ("make it single page", "colour navy")…',
    uploads: [
      { kind: 'resume_design', label: 'Design reference', hint: 'Picture or PDF of a resume to copy exactly', icon: LayoutTemplate, accept: `${IMG},.pdf`, single: true },
      { kind: 'resume_photo', label: 'Your photo', hint: 'Headshot placed on the resume', icon: User, accept: IMG, single: true },
      { kind: 'resume_logo', label: 'Logo', hint: 'College or company logo', icon: Building2, accept: IMG, single: true },
      { kind: 'resume_details', label: 'Details document', hint: 'Old CV, LinkedIn PDF or DOCX', icon: FileText, accept: DOCS, multiple: true },
    ],
    options: [
      { key: 'template', label: 'Template', icon: Palette, choices: [['', 'Auto'], ...RESUME_TEMPLATES.map(t => [t, cap(t)])] },
      { key: 'pages', label: 'Pages', icon: FileText, choices: [['', 'Auto length'], ['1', '1 page'], ['2', '2 pages']] },
    ],
    links: [{ label: 'Open resume editor', path: '/resume/editor' }],
    suggestions: [
      { title: 'Copy a design', text: 'Upload a resume picture with the + button, then paste your details here.' , fill: false },
      { title: 'Modern one-pager', text: 'Create my resume in the modern template, single page, using these details: ' },
      { title: 'Add a certification', text: 'Update my resume: add AWS Certified Cloud Practitioner (2025) to certifications' },
      { title: 'See all templates', text: 'list resume templates' },
    ],
  },
  {
    id: 'ppt', label: 'PPT Generator', icon: Presentation, accent: '#c084fc', accent2: '#f472b6',
    tagline: 'Research-backed decks with themes, charts and your own images',
    placeholder: 'What should the presentation be about?',
    uploads: [
      { kind: 'ppt_theme', label: 'Theme reference', hint: 'Screenshot of a slide whose look to copy', icon: Palette, accept: IMG, single: true },
      { kind: 'ppt_image', label: 'Slide images', hint: 'Pictures to place on slides (add a caption)', icon: ImagePlus, accept: IMG, multiple: true, describe: true },
      { kind: 'ppt_template', label: 'PowerPoint template', hint: '.pptx / .potx to fill in', icon: LayoutTemplate, accept: '.pptx,.potx', single: true },
      { kind: 'ppt_source', label: 'Source document', hint: 'PDF / DOCX / TXT with the content', icon: FileUp, accept: DOCS, multiple: true },
    ],
    options: [
      { key: 'theme', label: 'Theme', icon: Palette, choices: [['', 'Auto theme'], ...PPT_THEMES] },
      { key: 'purpose', label: 'Purpose', icon: Presentation, choices: [['', 'Auto purpose'], ['general', 'General'], ['academic', 'Academic'], ['business', 'Business'], ['hackathon', 'Hackathon / pitch']] },
      { key: 'slides', label: 'Slides', icon: FileText, choices: [['', 'Auto slides'], ...[5, 8, 10, 12, 15, 20].map(n => [String(n), `${n} slides`])] },
    ],
    suggestions: [
      { title: 'Hackathon pitch', text: 'AI-powered crop disease detection for farmers — hackathon pitch' },
      { title: 'Academic seminar', text: 'Quantum computing basics for a college seminar' },
      { title: 'Business review', text: 'Q3 sales performance review with charts and next steps' },
      { title: 'Edit the last deck', text: 'Change the title of slide 2 to "Our Approach"' },
    ],
  },
  {
    id: 'research', label: 'Deep Research', icon: Telescope, accent: '#38bdf8', accent2: '#34d399',
    tagline: 'Jarvis browses the live web and brings back what it finds',
    placeholder: 'What should Jarvis research on the web?',
    uploads: [],
    options: [],
    suggestions: [
      { title: 'Hackathons', text: 'Upcoming hackathons in India this month' },
      { title: 'Internships', text: 'Remote AI/ML internships open for students' },
      { title: 'Tech news', text: 'Latest news on open-source AI models' },
      { title: 'Compare', text: 'Best laptops under 80000 rupees for programming' },
    ],
  },
  {
    id: 'assignment', label: 'Assignment', icon: GraduationCap, accent: '#34d399', accent2: '#22d3ee',
    tagline: 'Upload an assignment — Jarvis extracts the questions and writes the answers',
    placeholder: 'Attach the assignment with +, then send (or ask a single question)…',
    uploads: [
      { kind: 'assignment', label: 'Assignment file', hint: 'PDF, DOCX or TXT', icon: FileText, accept: DOCS, single: true },
    ],
    // No "PPT output" option: chat.py's is_complex_task() sends "do my assignment … ppt" (or any extra
    // text) to the planner instead of the direct do_assignment route, so only the bare command is reliable.
    options: [],
    suggestions: [
      { title: 'Upload & solve', text: 'Upload your assignment with the + button, then press send.', fill: false },
      { title: 'One question', text: 'Answer this question: explain the CAP theorem with an example' },
      { title: 'My assignments', text: 'list my assignments' },
      { title: 'Humanize answers', text: 'humanize answers' },
    ],
  },
  {
    id: 'humanize', label: 'Humanizer', icon: WandSparkles, accent: '#fb7185', accent2: '#fbbf24',
    tagline: 'Rewrite AI-sounding text so it reads like a person wrote it',
    placeholder: 'Paste the text to humanize…',
    uploads: [],
    options: [],
    suggestions: [
      { title: 'Paste text', text: '', fill: false },
      { title: 'LinkedIn post', text: 'Write a linkedin post about finishing my first hackathon' },
    ],
  },
];

export const MODE_BY_ID = Object.fromEntries(MODES.map(m => [m.id, m]));

// Kind labels shown on attachment chips
export const KIND_LABEL = {
  general: '', assignment: 'Assignment',
  resume_design: 'Design', resume_photo: 'Photo', resume_logo: 'Logo', resume_details: 'Details',
  ppt_theme: 'Theme', ppt_image: 'Slide image', ppt_template: 'Template', ppt_source: 'Source',
};

export const isImage = (name = '') => /\.(png|jpe?g|webp|gif|bmp)$/i.test(name);

// Which kind a dropped / pasted file becomes in each mode
export function kindForFile(modeId, name, attachments) {
  const img = isImage(name);
  const has = (k) => attachments.some(a => a.kind === k);
  switch (modeId) {
    case 'resume':
      if (img) return has('resume_design') ? (has('resume_photo') ? 'resume_logo' : 'resume_photo') : 'resume_design';
      return /\.pdf$/i.test(name) && !has('resume_design') && !has('resume_details') ? 'resume_design' : 'resume_details';
    case 'ppt':
      if (img) return 'ppt_image';
      if (/\.(pptx|potx)$/i.test(name)) return 'ppt_template';
      return 'ppt_source';
    case 'assignment':
      return 'assignment';
    default:
      return 'general';
  }
}

// ── Intent detection (Chat mode keeps the old auto-routing) ─────────────────
const PPT_KW = [
  'create a presentation', 'make a presentation', 'build a presentation',
  'generate a presentation', 'design a presentation', 'prepare a presentation',
  'create slides', 'make slides', 'build slides',
  'make a ppt', 'create a ppt', 'build a ppt', 'generate a ppt',
  'create a deck', 'make a deck', 'create a powerpoint', 'make a powerpoint',
  'create presentation', 'make presentation',
  'ppt on ', 'ppt about ', 'presentation on ', 'presentation about ', 'slide deck on ',
];
// Whichever artifact is named FIRST wins, so resume details that mention
// "presentation skills" don't get hijacked by the PPT path.
export const isResumeRequest = (text) => {
  const lower = text.toLowerCase();
  const r = lower.search(/\b(r[eé]sum[eé]s?|cv|curriculum vitae|bio-?data)\b/i);
  if (r < 0) return false;
  const p = lower.search(/\b(ppt|presentation|slides?|deck|powerpoint)\b/i);
  return p < 0 || r < p;
};
export const isPPTRequest = (text) => {
  const lower = text.toLowerCase();
  if (isResumeRequest(lower)) return false;
  const exactMatch = PPT_KW.some(kw => lower.includes(kw));
  const regexMatch = /(?:create|make|build|generate|design|prepare|give|need|want|use|change|update|modify|edit|convert|theme).*(?:ppt|presentation|slide|deck|powerpoint|theme|color)/i.test(lower);
  return exactMatch || regexMatch;
};
// A follow-up edit of the deck Jarvis already made (goes to /chat → ppt_edit)
const isPPTEdit = (text) =>
  /^(change|edit|update|modify|replace|remove|delete|add|insert|move|rename|fix|swap|shorten|expand|translate|make (the|slide|it|this|them))\b/i.test(text.trim())
  && !/\b(create|make|generate|build)\s+(a |an |me a |new )*(ppt|presentation|deck|slides)\b/i.test(text);

// Suggest a better mode while typing in Chat mode
export function suggestMode(modeId, text) {
  if (modeId !== 'chat' || text.trim().length < 8) return null;
  if (isResumeRequest(text)) return 'resume';
  if (isPPTRequest(text) && /\b(ppt|presentation|slides?|deck|powerpoint)\b/i.test(text)) return 'ppt';
  if (/\b(do|solve|complete) my assignment\b/i.test(text)) return 'assignment';
  if (/\b(humani[sz]e|paraphrase)\b/i.test(text)) return 'humanize';
  return null;
}

const fwd = (p) => p.replace(/\\/g, '/');
const tag = (path, desc) => desc ? `[ATTACHED_FILE: ${fwd(path)} | DESCRIPTION: ${desc}]` : `[ATTACHED_FILE: ${fwd(path)}]`;
const withTags = (text, tags) => (tags.length ? `${text}\n\n${tags.join('\n')}` : text).trim();
const pick = (atts, kind) => atts.filter(a => a.kind === kind);

/**
 * Turn what the user typed + attachments + mode options into a backend request.
 * Returns { route: 'chat' | 'ppt', body, display, note? }.
 */
export function buildRequest({ modeId, prompt, attachments, options = {}, hasDeck = false }) {
  const text = prompt.trim();
  const generic = attachments.filter(a => a.kind === 'general');
  const genericTags = generic.map(a => tag(a.path, a.description));

  if (modeId === 'resume') {
    const design = pick(attachments, 'resume_design')[0];
    const photo = pick(attachments, 'resume_photo')[0];
    const logo = pick(attachments, 'resume_logo')[0];
    const docs = pick(attachments, 'resume_details');
    const tags = [];
    if (design) tags.push(tag(design.path, 'resume design reference'));
    if (photo) tags.push(tag(photo.path, 'my photo for the resume'));
    if (logo) tags.push(tag(logo.path, 'logo for the resume'));
    docs.forEach(d => tags.push(tag(d.path)));   // plain tag → /chat reads the document's text

    const tpl = !design && options.template ? ` in the ${options.template} template` : '';
    const pages = options.pages === '1' ? ', single page' : options.pages === '2' ? ', 2 pages' : '';
    const looksLikeDetails = !!(design || photo || docs.length) || text.length > 160
      || /@|\n|\+?\d[\d\s-]{8,}/.test(text) || !text;
    let out;
    if (/^list resume templates?$/i.test(text)) out = text;
    else if (isResumeRequest(text)) out = `${text}${tpl}${pages}`;
    else if (looksLikeDetails) out = `Create my resume${design ? ' exactly like this design' : ''}${tpl}${pages}, using these details: ${text}`;
    else out = `Update my resume: ${text}${tpl}${pages}`;
    return {
      route: 'chat',
      body: { prompt: withTags(out, [...tags, ...genericTags]) },
      display: text || (design ? 'Create my resume in this design' : 'Create my resume'),
    };
  }

  if (modeId === 'ppt') {
    const theme = pick(attachments, 'ppt_theme')[0];
    const images = pick(attachments, 'ppt_image');
    const template = pick(attachments, 'ppt_template')[0];
    const sources = pick(attachments, 'ppt_source');
    const themeName = options.theme ? options.theme.replace(/_/g, ' ') : '';
    const slides = options.slides ? `, ${options.slides} slides` : '';
    const display = text || 'Create a presentation';

    // Edits to the deck made earlier → /chat (ppt_edit needs the active deck)
    if (hasDeck && text && isPPTEdit(text) && !template && !sources.length) {
      return { route: 'chat', body: { prompt: withTags(text, genericTags) }, display };
    }
    const base = /\b(ppt|presentation|slides?|deck|powerpoint)\b/i.test(text)
      ? text : `Create a presentation on ${text || 'the attached document'}`;
    const topic = `${base}${slides}`;

    // A .pptx template or a source document is only understood by /chat
    if (template || sources.length) {
      const tags = [];
      if (template) tags.push(tag(template.path));
      sources.forEach(s => tags.push(tag(s.path)));
      images.forEach(i => tags.push(tag(i.path, i.description)));
      const extra = [themeName && `${themeName} theme`, options.purpose && `for a ${options.purpose} audience`].filter(Boolean).join(', ');
      return {
        route: 'chat',
        body: { prompt: withTags(extra ? `${topic} (${extra})` : topic, [...tags, ...genericTags]) },
        display,
        note: theme ? 'The theme reference is skipped when a template or source document is attached.' : undefined,
      };
    }
    const body = { prompt: withTags(topic, genericTags) };
    if (options.theme) body.style = options.theme;
    if (options.purpose) body.purpose = options.purpose;
    if (theme) body.theme_image_path = fwd(theme.path);
    if (images.length) {
      body.image_paths = images.map(i => fwd(i.path));
      body.image_descriptions = images.map(i => (i.description || '').trim());
    }
    return { route: 'ppt', body, display, themeName: theme?.name };
  }

  if (modeId === 'assignment') {
    // The bare filename is enough (assignment_tool resolves it in data/uploads). No [ATTACHED_FILE] tag:
    // /chat would paste the PDF's text into the prompt and the keyword router would skip do_assignment.
    const file = pick(attachments, 'assignment')[0];
    let out = text;
    if (file) out = `do my assignment from ${file.filename || file.name}${text ? `. ${text}` : ''}`;
    return { route: 'chat', body: { prompt: withTags(out, genericTags) }, display: text || `Solve ${file?.name || 'my assignment'}` };
  }

  if (modeId === 'research') {
    const out = /^(search|find|look up|browse)\b/i.test(text) ? text : `search the web: ${text}`;
    return { route: 'chat', body: { prompt: withTags(out, genericTags) }, display: text };
  }

  if (modeId === 'humanize') {
    const out = /^(humani[sz]e|paraphrase|rewrite|write a)\b/i.test(text) ? text : `humanize this text: ${text}`;
    return { route: 'chat', body: { prompt: withTags(out, genericTags) }, display: text };
  }

  // Chat mode — keep the original auto-routing of "make a ppt on …" to /ppt/create
  if (!isResumeRequest(text) && isPPTRequest(text) && !(hasDeck && isPPTEdit(text))) {
    const images = generic.filter(a => isImage(a.name));
    const body = { prompt: withTags(text, genericTags) };
    if (images.length) {
      body.image_paths = images.map(i => fwd(i.path));
      body.image_descriptions = images.map(i => (i.description || '').trim());
      body.theme_image_path = body.image_paths[0];
    }
    return { route: 'ppt', body, display: text };
  }
  return { route: 'chat', body: { prompt: withTags(text, genericTags) }, display: text };
}
