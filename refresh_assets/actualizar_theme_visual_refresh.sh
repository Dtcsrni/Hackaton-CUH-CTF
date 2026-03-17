#!/usr/bin/env bash
set -euo pipefail

CTFD_CONTAINER=${CTFD_CONTAINER:-ctfd-ctfd-1}
WORKDIR=/tmp/cuh_ctfd_visual_refresh
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

cat > "$WORKDIR/apply_visual_refresh.py" <<'PY'
import re
from CTFd import create_app
from CTFd.models import Configs, db

STYLE = r'''<!-- CTFCU_VISUAL_REFRESH_START --><style id="ctfcu-visual-refresh">
:root{
  --cuhv-bg:#24313e;
  --cuhv-bg-deep:#18212b;
  --cuhv-panel-top:rgba(74,88,104,.92);
  --cuhv-panel-bottom:rgba(31,38,46,.98);
  --cuhv-panel-soft:rgba(255,255,255,.04);
  --cuhv-text:#eef1f3;
  --cuhv-soft:rgba(222,229,235,.78);
  --cuhv-muted:rgba(205,216,226,.62);
  --cuhv-line:rgba(172,185,198,.16);
  --cuhv-line-strong:rgba(198,209,220,.26);
  --cuhv-accent:#46627f;
  --cuhv-accent-soft:#7b92ac;
  --cuhv-highlight:#b4c2cf;
  --cuhv-shadow:0 18px 50px rgba(0,0,0,.28);
  --cuhv-radius-xl:30px;
  --cuhv-radius-lg:24px;
  --cuhv-radius-md:18px;
}
html,body{
  background:
    radial-gradient(circle at 12% 18%,rgba(70,98,127,.15) 0%,transparent 24%),
    radial-gradient(circle at 86% 12%,rgba(123,146,172,.12) 0%,transparent 20%),
    linear-gradient(180deg,var(--cuhv-bg) 0%,var(--cuhv-bg-deep) 100%)!important;
  color:var(--cuhv-text)!important;
}
body::before{
  background-image:
    linear-gradient(rgba(180,194,207,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(180,194,207,.04) 1px,transparent 1px)!important;
  opacity:.18!important;
}
body,button,input,select,textarea{
  color:var(--cuhv-text);
}
a{
  color:#d8e4ef;
}
a:hover,a:focus{
  color:#f3f7fb;
}
.challenge-button,.card,.cuhv-card,.cuh-item{
  border:1px solid var(--cuhv-line)!important;
  background:linear-gradient(180deg,rgba(72,86,101,.92),rgba(35,43,52,.97))!important;
  box-shadow:var(--cuhv-shadow)!important;
}
.challenge-button:hover,.card:hover{
  border-color:var(--cuhv-line-strong)!important;
  box-shadow:0 20px 55px rgba(0,0,0,.34)!important;
}
.btn-primary,.btn-info{
  background:linear-gradient(135deg,var(--cuhv-accent),var(--cuhv-accent-soft))!important;
  border:0!important;
  color:#eef1f3!important;
  box-shadow:0 10px 30px rgba(70,98,127,.22)!important;
}
.btn-outline-secondary,.btn-outline-info{
  border-color:rgba(198,209,220,.22)!important;
  color:var(--cuhv-text)!important;
}
.modal-content,.challenge-window .modal-content{
  background:linear-gradient(180deg,rgba(67,78,91,.98),rgba(28,34,41,.99))!important;
  border:1px solid rgba(172,185,198,.18)!important;
}
.form-control,.custom-select,textarea{
  background:rgba(248,250,252,.05)!important;
  color:var(--cuhv-text)!important;
  border-color:rgba(172,185,198,.16)!important;
}
.form-control:focus,textarea:focus{
  border-color:rgba(70,98,127,.42)!important;
  box-shadow:0 0 0 .2rem rgba(70,98,127,.12)!important;
}
.cuhv-page{
  position:relative;
  width:min(100%,1680px);
  margin:0 auto;
  padding:36px 22px 88px;
  color:var(--cuhv-text);
}
.cuhv-page > *{
  position:relative;
  z-index:1;
}
.cuhv-page > * + *{
  margin-top:24px;
}
.cuhv-page code,
.cuhv-page pre{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
.cuhv-hero,
.cuhv-section{
  position:relative;
  overflow:hidden;
  padding:clamp(20px,3vw,30px);
  border:1px solid var(--cuhv-line);
  border-radius:var(--cuhv-radius-xl);
  background:
    radial-gradient(circle at top right,rgba(127,147,168,.10),transparent 30%),
    linear-gradient(180deg,var(--cuhv-panel-top),var(--cuhv-panel-bottom));
  box-shadow:var(--cuhv-shadow);
}
.cuhv-hero::before,
.cuhv-section::before{
  content:"";
  position:absolute;
  inset:0;
  pointer-events:none;
  background:
    linear-gradient(90deg,rgba(255,255,255,.04),rgba(255,255,255,0) 26%),
    repeating-linear-gradient(90deg,rgba(183,197,211,.04) 0,rgba(183,197,211,.04) 1px,transparent 1px,transparent 58px);
  opacity:.45;
}
.cuhv-hero > *,
.cuhv-section > *{
  position:relative;
  z-index:1;
}
.cuhv-hero{
  display:grid;
  grid-template-columns:minmax(0,1.15fr) minmax(320px,.85fr);
  gap:clamp(18px,2vw,26px);
  align-items:stretch;
}
.cuhv-hero-compact{
  grid-template-columns:minmax(0,1fr);
}
.cuhv-hero-copy{
  min-width:0;
}
.cuhv-kicker,.cuhv-button,.cuhv-button:visited{
  background:linear-gradient(135deg,var(--cuhv-accent),var(--cuhv-accent-soft))!important;
  color:#eef1f3!important;
}
.cuhv-kicker{
  display:inline-flex;
  align-items:center;
  gap:8px;
  min-height:34px;
  padding:0 14px;
  border-radius:999px;
  font-size:.8rem;
  font-weight:900;
  letter-spacing:.11em;
  text-transform:uppercase;
  box-shadow:0 12px 26px rgba(70,98,127,.2);
}
.cuhv-hero h1,
.cuhv-section-head h2{
  margin:14px 0 0;
  color:#fff;
  letter-spacing:-.04em;
}
.cuhv-hero h1{
  font-size:clamp(2.6rem,4.8vw,5rem);
  line-height:.96;
}
.cuhv-hero-compact h1{
  max-width:14ch;
}
.cuhv-hero p,
.cuhv-section-head p,
.cuhv-card p,
.cuhv-card li,
.cuhv-step p,
.cuhv-note,
.cuhv-note p,
.cuhv-photo-card figcaption{
  color:var(--cuhv-soft);
  line-height:1.72;
}
.cuhv-actions{
  display:flex;
  flex-wrap:wrap;
  gap:12px;
  margin-top:20px;
}
.cuhv-button{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-height:50px;
  padding:0 18px;
  border-radius:16px;
  border:1px solid rgba(172,185,198,.12);
  text-decoration:none;
  font-weight:900;
  box-shadow:0 14px 28px rgba(70,98,127,.22);
}
.cuhv-button-alt{
  background:linear-gradient(180deg,rgba(76,90,105,.88),rgba(34,42,50,.96))!important;
}
.cuhv-section-head{
  display:flex;
  flex-direction:column;
  gap:10px;
  margin-bottom:18px;
}
.cuhv-grid{
  display:grid;
  gap:16px;
}
.cuhv-grid-2{grid-template-columns:repeat(2,minmax(0,1fr))}
.cuhv-grid-3{grid-template-columns:repeat(3,minmax(0,1fr))}
.cuhv-grid-4{grid-template-columns:repeat(4,minmax(0,1fr))}
.cuhv-card,
.cuhv-note,
.cuhv-step,
.cuhv-photo-card{
  position:relative;
  overflow:hidden;
  min-width:0;
  padding:20px;
  border:1px solid rgba(172,185,198,.14);
  border-radius:var(--cuhv-radius-lg);
  background:linear-gradient(180deg,rgba(79,92,108,.88),rgba(34,42,50,.96));
  box-shadow:0 16px 36px rgba(0,0,0,.22);
}
.cuhv-card h3,
.cuhv-step strong,
.cuhv-note strong{
  display:block;
  margin:0 0 10px;
  color:#fff;
  font-size:1.08rem;
  line-height:1.3;
}
.cuhv-card > :last-child,
.cuhv-note > :last-child,
.cuhv-step > :last-child{
  margin-bottom:0;
}
.cuhv-list{
  margin:0;
  padding-left:18px;
}
.cuhv-list li + li{
  margin-top:8px;
}
.cuhv-codeblock{
  margin:0;
  padding:16px 18px;
  border:1px solid rgba(172,185,198,.14);
  border-radius:18px;
  background:linear-gradient(180deg,rgba(16,27,44,.88),rgba(8,14,24,.96));
  color:#edf4fb;
  font-size:.9rem;
  line-height:1.65;
  overflow:auto;
  white-space:pre-wrap;
  word-break:break-word;
}
.cuhv-note{
  margin-top:18px;
  background:linear-gradient(135deg,rgba(74,88,104,.96),rgba(33,41,50,.98));
}
.cuhv-timeline{
  display:grid;
  gap:14px;
}
.cuhv-step{
  padding-left:24px;
}
.cuhv-step::before{
  content:"";
  position:absolute;
  left:0;
  top:18px;
  bottom:18px;
  width:4px;
  border-radius:999px;
  background:linear-gradient(180deg,var(--cuhv-accent-soft),rgba(180,194,207,.26));
}
.cuhv-photo-card{
  display:grid;
  gap:12px;
  align-content:start;
}
.cuhv-photo-card img{
  width:100%;
  border-radius:18px;
  object-fit:cover;
  border:1px solid rgba(172,185,198,.14);
}
.cuhv-reader-reward{
  border:1px solid rgba(172,185,198,.14);
  border-radius:var(--cuhv-radius-xl);
}
.cuhv-reveal{
  opacity:0;
  transform:translateY(18px);
  transition:opacity .45s ease,transform .45s ease;
}
.cuhv-reveal.is-visible{
  opacity:1;
  transform:none;
}
@media (max-width:1200px){
  .cuhv-grid-4{grid-template-columns:repeat(2,minmax(0,1fr))}
  .cuhv-grid-3{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:980px){
  .cuhv-page{
    padding:24px 16px 72px;
  }
  .cuhv-hero{
    grid-template-columns:1fr;
  }
}
@media (max-width:680px){
  .cuhv-page{
    padding:18px 12px 56px;
  }
  .cuhv-hero,
  .cuhv-section{
    padding:18px;
    border-radius:24px;
  }
  .cuhv-grid-2,
  .cuhv-grid-3,
  .cuhv-grid-4{
    grid-template-columns:1fr;
  }
  .cuhv-card,
  .cuhv-note,
  .cuhv-step,
  .cuhv-photo-card{
    padding:16px;
    border-radius:20px;
  }
}
@media (prefers-reduced-motion:reduce){
  .cuhv-reveal{
    opacity:1;
    transform:none;
    transition:none;
  }
}
</style><!-- CTFCU_VISUAL_REFRESH_END -->'''

SCRIPT = r'''<!-- CTFCU_VISUAL_REFRESH_SCRIPT_START --><script id="ctfcu-visual-refresh-script">(()=>{const nodes=()=>Array.from(document.querySelectorAll('.cuhv-reveal,.challenge-button,.card'));const boot=()=>{const list=nodes();list.forEach((n,i)=>{if(!n.dataset.ctfcuDelay){n.style.transitionDelay=`${Math.min(i*50,260)}ms`;n.dataset.ctfcuDelay='1';}});if(!('IntersectionObserver'in window)){list.forEach(n=>n.classList.add('is-visible'));return;}const io=new IntersectionObserver((entries)=>{entries.forEach((e)=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target);}})},{threshold:.12});list.forEach(n=>io.observe(n));};document.addEventListener('DOMContentLoaded',boot);})();</script><!-- CTFCU_VISUAL_REFRESH_SCRIPT_END -->'''

def upsert(value, start, end, block):
    value = re.sub(re.escape(start) + r'.*?' + re.escape(end), '', str(value), flags=re.S).strip()
    return (value + '\n' if value else '') + block + '\n'

app = create_app()
with app.app_context():
    header = Configs.query.filter_by(key='theme_header').first()
    footer = Configs.query.filter_by(key='theme_footer').first()
    header.value = upsert(header.value, '<!-- CTFCU_VISUAL_REFRESH_START -->', '<!-- CTFCU_VISUAL_REFRESH_END -->', STYLE)
    footer.value = upsert(footer.value, '<!-- CTFCU_VISUAL_REFRESH_SCRIPT_START -->', '<!-- CTFCU_VISUAL_REFRESH_SCRIPT_END -->', SCRIPT)
    db.session.commit()
    print('visual refresh synced')
PY

docker cp "$WORKDIR/apply_visual_refresh.py" "$CTFD_CONTAINER:/tmp/apply_visual_refresh.py"
docker exec -e PYTHONPATH=/opt/CTFd "$CTFD_CONTAINER" python3 /tmp/apply_visual_refresh.py
