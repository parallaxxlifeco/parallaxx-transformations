/* PARALLAXX TRANSFORMATIONS - Wheel of Reconnect. Wix Custom Element.
   Tag: parallaxx-wheel-of-reconnect
   Self-contained shadow-DOM element (same pattern as parallaxx-home-page.js).
   In the Wix editor: add a Custom Element, Source = this file's URL,
   Tag name = parallaxx-wheel-of-reconnect, and turn the site Header + Footer
   ON (this is a section, not a full-bleed page) or OFF to taste.

   EDITING THE CONTENT: everything a coach needs to change (segment names,
   descriptions, colours, intro copy) lives in the CONFIG block below.
   Nothing else needs touching. */
(function(){
  if (customElements.get('parallaxx-wheel-of-reconnect')) return;

  /* ============================================================
     CONFIG - EDIT THIS BLOCK ONLY
     ============================================================ */
  var CONFIG = {
    title: "The Wheel of Reconnect",
    eyebrow: "Time to check back in with yourself",
    intro: "You're here because you backed yourself enough to look at your life honestly, and that takes guts. Respect. This is where we get a real read on where you're at, across the areas that make up a full life. The ones you love, and the ones that have gone a bit quiet. Rate each one from 1 to 7. 1 is running on empty, 7 is exactly how you'd want it. No performing, no impressing anyone, just be honest with yourself. Rate all ten and your wheel will show you what's true right now.",
    introFoot: "Takes about 5 minutes. Nothing is saved or sent, this stays between you and the screen.",
    maxScore: 7,

    // Palette - Parallaxx Transformations brand colours.
    //  navy #061938 · gold #E8C65F · cream #F1ECE1 · coral #FF501F · slate #7C89A3 · mist #B1BFD7
    colors: {
      bg:        "#F1ECE1",  // px-cream
      ink:       "#061938",  // px-navy
      muted:     "#5E6B85",  // deepened slate (readable on cream)
      brand:     "#061938",  // px-navy - buttons, progress, wheel outline
      brandSoft: "#7C89A3",  // px-slate
      accent:    "#E8C65F",  // px-gold
      line:      "#DED6C4",  // soft cream border
      card:      "#ffffff"
    },

    // The 10 dimensions, grouped into 3 pillars. Each pillar is a brand colour
    // family, shaded dark to light so the three pillars read as groups.
    //  Inner Self        -> GOLD family
    //  Connected Self    -> CORAL family
    //  Professional Self -> NAVY / SLATE family
    segments: [
      { name: "Mindset",                pillar: "Inner Self",        color: "#8A6A18",
        desc: "The thoughts and beliefs running underneath your habits, and how you talk to yourself when things get hard." },
      { name: "Emotions",               pillar: "Inner Self",        color: "#B08A2C",
        desc: "How you feel your feelings and sit with them, instead of numbing out or pushing them down." },
      { name: "Passion & Inspiration",  pillar: "Inner Self",        color: "#D2AE48",
        desc: "The stuff that lights you up and pulls you in, where you lose track of time and it feels like play." },
      { name: "Physical Health",        pillar: "Inner Self",        color: "#ECCB66",
        desc: "How you're looking after your body. Food, movement, sleep, energy, the whole engine." },
      { name: "Friends & Family",       pillar: "Connected Self",    color: "#C23A18",
        desc: "The people close to you and how supported you feel. The quality of your relationships shapes the quality of your life." },
      { name: "Intimate Relationship",  pillar: "Connected Self",    color: "#FF501F",
        desc: "Real closeness with one person. Being fully yourself with them, open, seen and connected." },
      { name: "Recreational Activities",pillar: "Connected Self",    color: "#FF8A5F",
        desc: "The play and downtime you actually make room for, the things you do purely because you love them." },
      { name: "Intellectual & Learning",pillar: "Professional Self", color: "#061938",
        desc: "Feeding your mind and building skills, and that feeling of growth when you're getting better at something that matters." },
      { name: "Business or Career",     pillar: "Professional Self", color: "#4A5A7C",
        desc: "Work that means something. Waking up curious about the day instead of counting down to the weekend." },
      { name: "Wealth & Contribution",  pillar: "Professional Self", color: "#7C89A3",
        desc: "Real abundance and the freedom it buys you, plus what you get to give back. Bigger than money." }
    ]
  };
  /* ============================================================
     END CONFIG - no need to edit below this line
     ============================================================ */

  var CSS = `
  *{box-sizing:border-box;margin:0;padding:0;}
  :host{
    display:block;
    --bg:#F1ECE1; --ink:#061938; --muted:#5E6B85;
    --brand:#061938; --brand-soft:#7C89A3; --accent:#E8C65F;
    --line:#DED6C4; --card:#ffffff;
    --shadow:0 14px 46px rgba(6,25,56,.12);
    --radius:22px;
    font-family:'Montserrat',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  }
  #wor-root{
    background:var(--bg);
    color:var(--ink);
    line-height:1.5;
    -webkit-font-smoothing:antialiased;
    display:flex; align-items:center; justify-content:center;
    padding:clamp(28px,5vw,64px) 16px;
  }
  .app{ width:100%; max-width:560px; margin:0 auto; }
  .card{
    background:var(--card); border-radius:var(--radius);
    box-shadow:var(--shadow); padding:34px 30px 30px;
    position:relative; overflow:hidden;
  }

  /* Screens */
  .screen{display:none; animation:worfade .5s ease both;}
  .screen.active{display:block;}
  @keyframes worfade{from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:translateY(0);}}

  /* Intro */
  .eyebrow{text-transform:uppercase; letter-spacing:.18em; font-size:12px; font-weight:700; color:var(--brand-soft); margin:0 0 12px;}
  h1{font-family:'Cormorant Garamond',Georgia,serif; font-size:clamp(30px,7vw,40px); line-height:1.08; margin:0 0 16px; font-weight:600; letter-spacing:-.005em; color:var(--ink);}
  .lead{color:var(--muted); font-size:16px; margin:0 0 26px;}

  .btn{appearance:none; border:none; cursor:pointer; font-family:inherit; font-weight:700; font-size:16px; padding:15px 26px; border-radius:999px; background:var(--brand); color:#fff; transition:transform .12s ease, filter .12s ease, opacity .2s; box-shadow:0 8px 22px rgba(6,25,56,.28);}
  .btn:hover{filter:brightness(1.12); transform:translateY(-1px);}
  .btn:active{transform:translateY(0);}
  .btn:disabled{opacity:.4; cursor:not-allowed; box-shadow:none;}
  .btn.secondary{background:transparent; color:var(--brand); box-shadow:none; border:1.5px solid var(--line);}
  .btn.ghost{background:transparent; color:var(--muted); box-shadow:none;}
  .btn-row{display:flex; gap:12px; align-items:center; flex-wrap:wrap;}

  /* Progress */
  .progress-wrap{margin:0 0 22px;}
  .progress-meta{display:flex; justify-content:space-between; font-size:13px; color:var(--muted); margin-bottom:8px; font-weight:600;}
  .progress-track{height:6px; background:var(--line); border-radius:999px; overflow:hidden;}
  .progress-bar{height:100%; width:0; background:var(--brand); border-radius:999px; transition:width .4s ease;}

  /* Segment rating */
  .seg-dot{width:44px; height:44px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:18px; margin-bottom:16px;}
  .seg-pillar{text-transform:uppercase; letter-spacing:.16em; font-size:11px; font-weight:700; color:var(--brand-soft); margin:0 0 4px;}
  .seg-title{font-size:24px; font-weight:800; margin:0 0 4px; letter-spacing:-.01em;}
  .seg-desc{color:var(--muted); font-size:15px; margin:0 0 24px;}

  .levels{display:flex; gap:8px; align-items:flex-end; height:150px; margin:0 0 10px; justify-content:center;}
  .level{flex:1; max-width:46px; height:100%; border-radius:12px; border:2px solid var(--line); background:#faf8f4; cursor:pointer; position:relative; transition:transform .1s ease, border-color .15s; display:flex; align-items:flex-end; justify-content:center; padding-bottom:6px; color:var(--muted); font-weight:700; font-size:13px; overflow:hidden;}
  .level:hover{transform:translateY(-3px); border-color:var(--brand-soft);}
  .level .fill{position:absolute; left:0; right:0; bottom:0; top:0; background:var(--seg-color, var(--brand)); transform:scaleY(0); transform-origin:bottom; transition:transform .25s cubic-bezier(.34,1.3,.5,1); border-radius:9px;}
  .level.filled .fill{transform:scaleY(1);}
  .level .num{position:relative; z-index:2; transition:color .2s;}
  .level.filled .num{color:#fff; text-shadow:0 1px 2px rgba(0,0,0,.32);}
  .scale-labels{display:flex; justify-content:space-between; font-size:12px; color:var(--muted); margin:0 0 22px; font-weight:600;}

  .note-field{width:100%; border:1.5px solid var(--line); border-radius:14px; padding:12px 14px; font-family:inherit; font-size:15px; color:var(--ink); resize:none; background:#faf8f4; margin:0 0 24px;}
  .note-field:focus{outline:none; border-color:var(--brand-soft);}
  .note-label{font-size:13px; font-weight:700; color:var(--muted); margin:0 0 8px; display:block;}

  .nav-row{display:flex; justify-content:space-between; align-items:center; gap:12px;}

  /* Reveal */
  .reveal-head{text-align:center; margin-bottom:18px;}
  .reveal-head h2{font-family:'Cormorant Garamond',Georgia,serif; font-size:clamp(26px,6vw,34px); margin:0 0 6px; font-weight:600; letter-spacing:-.005em;}
  .reveal-head p{color:var(--muted); margin:0; font-size:15px;}
  .canvas-wrap{display:flex; justify-content:center; align-items:center; margin:2px 0 14px;}
  #wheel{width:100%; max-width:430px; height:auto; display:block;}

  .summary{border-top:1px solid var(--line); margin-top:6px; padding-top:16px; display:grid; grid-template-columns:1fr 1fr; gap:8px 18px;}
  .summary-item{display:flex; align-items:center; gap:10px; font-size:14px;}
  .summary-swatch{width:12px; height:12px; border-radius:3px; flex:none;}
  .summary-name{flex:1; color:var(--ink);}
  .summary-score{font-weight:800; color:var(--brand);}
  .avg-pill{display:inline-flex; align-items:center; gap:8px; background:#efe9dd; color:var(--ink); font-weight:700; padding:8px 16px; border-radius:999px; font-size:14px; margin-top:4px;}

  .footer-note{text-align:center; color:var(--muted); font-size:12px; margin-top:20px;}
  @media (max-width:420px){
    .card{padding:26px 20px 24px;}
    .levels{height:130px;}
    .summary{grid-template-columns:1fr;}
  }`;

  var HTML = `
  <div id="wor-root">
    <div class="app">
      <div class="card">

        <section class="screen active" id="screen-intro">
          <p class="eyebrow" id="introEyebrow"></p>
          <h1 id="introTitle">The Wheel of Reconnect</h1>
          <p class="lead" id="introLead"></p>
          <div class="btn-row"><button class="btn" id="startBtn">Begin</button></div>
          <p class="footer-note" id="introFoot"></p>
        </section>

        <section class="screen" id="screen-rate">
          <div class="progress-wrap">
            <div class="progress-meta">
              <span id="progLabel"></span>
              <span id="progPct">0%</span>
            </div>
            <div class="progress-track"><div class="progress-bar" id="progBar"></div></div>
          </div>

          <div class="seg-dot" id="segDot">1</div>
          <p class="seg-pillar" id="segPillar"></p>
          <h2 class="seg-title" id="segTitle">Segment</h2>
          <p class="seg-desc" id="segDesc"></p>

          <div class="levels" id="levels"></div>
          <div class="scale-labels"><span>1 · Running on empty</span><span>7 · Exactly how I want it</span></div>

          <label class="note-label" for="noteField">One honest line, if you want to</label>
          <textarea class="note-field" id="noteField" rows="2" placeholder="Whatever's true for you right now"></textarea>

          <div class="nav-row">
            <button class="btn ghost" id="backBtn">&larr; Back</button>
            <button class="btn" id="nextBtn" disabled>Next &rarr;</button>
          </div>
        </section>

        <section class="screen" id="screen-reveal">
          <div class="reveal-head">
            <h2 id="revealTitle">Here's your wheel.</h2>
            <p id="revealSub">So how smooth is your ride right now, and where's it pulling?</p>
          </div>
          <div class="canvas-wrap"><canvas id="wheel" width="860" height="740"></canvas></div>
          <div style="text-align:center;"><span class="avg-pill" id="avgPill"></span></div>
          <div class="summary" id="summary"></div>
          <div class="btn-row" style="justify-content:center; margin-top:24px;">
            <button class="btn" id="downloadBtn">Download my wheel</button>
            <button class="btn secondary" id="restartBtn">Start over</button>
          </div>
          <p class="footer-note" id="revealFoot"></p>
        </section>

      </div>
    </div>
  </div>`;

  /* ---------- Shared helpers (same as other Parallaxx pages) ---------- */
  function addFonts(){
    if (document.getElementById('px-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
    var l=document.createElement('link'); l.id='px-fonts'; l.rel='stylesheet';
    l.href='https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap';
    document.head.appendChild(l);
  }
  function collapseAncestors(host){
    try{ var h=host.getBoundingClientRect().height; if(h<50) return;
      var n=host.parentElement,guard=0;
      while(n && n!==document.body && guard++<14){ if(n.getBoundingClientRect().height>h+600){ n.style.height='auto'; n.style.minHeight='0px'; } n=n.parentElement; }
    }catch(e){}
  }

  /* ---------- The tool ---------- */
  function boot(root){
    var host = root.host;
    var segs = CONFIG.segments;
    var MAX  = CONFIG.maxScore;
    var scores = new Array(segs.length).fill(0);
    var notes  = new Array(segs.length).fill("");
    var current = 0;

    var $ = function(id){ return root.getElementById(id); };

    // Theme -> CSS vars on the root wrapper (cascades to all children)
    (function applyTheme(){
      var c = CONFIG.colors, s = $('wor-root').style;
      s.setProperty('--bg', c.bg);
      s.setProperty('--ink', c.ink);
      s.setProperty('--muted', c.muted);
      s.setProperty('--brand', c.brand);
      s.setProperty('--brand-soft', c.brandSoft);
      s.setProperty('--accent', c.accent);
      s.setProperty('--line', c.line);
      if(c.card) s.setProperty('--card', c.card);
      $('introTitle').textContent = CONFIG.title;
      $('introEyebrow').textContent = CONFIG.eyebrow;
      $('introLead').textContent = CONFIG.intro;
      $('introFoot').textContent = CONFIG.introFoot;
    })();

    function show(screen){
      var all = root.querySelectorAll('.screen');
      for(var i=0;i<all.length;i++) all[i].classList.remove('active');
      $(screen).classList.add('active');
      // Bring the tool to the top of the viewport if it has scrolled off-screen
      var top = host.getBoundingClientRect().top;
      if(top < -20 || top > 140){ try{ host.scrollIntoView({behavior:'smooth', block:'start'}); }catch(e){} }
    }

    function renderLevels(){
      var wrap = $('levels'); wrap.innerHTML = '';
      var seg = segs[current];
      for(var i=1;i<=MAX;i++){
        var b = document.createElement('div');
        b.className = 'level';
        b.style.setProperty('--seg-color', seg.color);
        b.innerHTML = '<span class="fill"></span><span class="num">'+i+'</span>';
        (function(val){ b.addEventListener('click', function(){ setScore(val); }); })(i);
        wrap.appendChild(b);
      }
      paintLevels();
    }
    function paintLevels(){
      var blocks = root.querySelectorAll('#levels .level');
      var val = scores[current];
      blocks.forEach(function(b,idx){
        if(idx < val) b.classList.add('filled'); else b.classList.remove('filled');
      });
      $('nextBtn').disabled = val === 0;
    }
    function setScore(v){ scores[current] = v; paintLevels(); }

    function renderSegment(){
      var seg = segs[current];
      $('segDot').textContent = current+1;
      $('segDot').style.background = seg.color;
      $('segPillar').textContent = seg.pillar || '';
      $('segPillar').style.color = seg.color;
      $('segTitle').textContent = seg.name;
      $('segDesc').textContent = seg.desc;
      $('noteField').value = notes[current] || '';
      $('progLabel').textContent = 'Area '+(current+1)+' of '+segs.length;
      var pct = Math.round((current)/segs.length*100);
      $('progPct').textContent = pct + '%';
      $('progBar').style.width = pct + '%';
      $('backBtn').style.visibility = current === 0 ? 'hidden' : 'visible';
      $('nextBtn').innerHTML = current === segs.length-1 ? 'Reveal my wheel &#10022;' : 'Next &rarr;';
      renderLevels();
    }

    // Navigation
    $('startBtn').addEventListener('click', function(){ current=0; renderSegment(); show('screen-rate'); });
    $('backBtn').addEventListener('click', function(){
      notes[current] = $('noteField').value;
      if(current>0){ current--; renderSegment(); }
    });
    $('nextBtn').addEventListener('click', function(){
      if(scores[current]===0) return;
      notes[current] = $('noteField').value;
      if(current < segs.length-1){ current++; renderSegment(); }
      else { $('progBar').style.width='100%'; $('progPct').textContent='100%'; goReveal(); }
    });
    $('restartBtn').addEventListener('click', function(){
      for(var i=0;i<scores.length;i++){ scores[i]=0; notes[i]=''; }
      current=0; show('screen-intro');
    });

    function goReveal(){ buildSummary(); show('screen-reveal'); setTimeout(animateWheel, 350); }

    function buildSummary(){
      var sum = $('summary'); sum.innerHTML = '';
      segs.forEach(function(s,i){
        var row = document.createElement('div');
        row.className = 'summary-item';
        row.innerHTML =
          '<span class="summary-swatch" style="background:'+s.color+'"></span>'+
          '<span class="summary-name">'+s.name+'</span>'+
          '<span class="summary-score">'+scores[i]+'</span>';
        sum.appendChild(row);
      });
      var avg = (scores.reduce(function(a,b){return a+b;},0)/segs.length).toFixed(1);
      $('avgPill').textContent = 'Overall balance: '+avg+' / '+MAX;
    }

    // Canvas wheel
    var canvas = $('wheel');
    var ctx = canvas.getContext('2d');
    var DPR = Math.min(window.devicePixelRatio||1, 2);
    var W = 860, H = 740;
    canvas.width = W*DPR; canvas.height = H*DPR;
    ctx.scale(DPR,DPR);
    var CX = W/2, CY = H/2, R = 262, N = segs.length, START = -Math.PI/2;
    var LABEL_FONT = "600 15px 'Montserrat',-apple-system,Segoe UI,Roboto,sans-serif";

    function hexToRgba(hex, a){
      var h = hex.replace('#','');
      var n = parseInt(h.length===3 ? h.split('').map(function(x){return x+x;}).join('') : h, 16);
      return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')';
    }
    function wrapLabel(text, x, y){
      var words = text.split(' ');
      if(words.length<=1 || text.length<=12){ ctx.fillText(text,x,y); return; }
      var mid = Math.ceil(words.length/2);
      ctx.fillText(words.slice(0,mid).join(' '), x, y-8);
      ctx.fillText(words.slice(mid).join(' '), x, y+8);
    }
    function drawGrid(){
      ctx.lineWidth = 1;
      for(var ring=1; ring<=MAX; ring++){
        ctx.beginPath();
        ctx.strokeStyle = ring===MAX ? CONFIG.colors.muted : CONFIG.colors.line;
        ctx.arc(CX,CY, R*ring/MAX, 0, Math.PI*2); ctx.stroke();
      }
      ctx.font = LABEL_FONT;
      for(var i=0;i<N;i++){
        var a = START + i*2*Math.PI/N;
        ctx.beginPath(); ctx.strokeStyle = CONFIG.colors.line;
        ctx.moveTo(CX,CY); ctx.lineTo(CX+Math.cos(a)*R, CY+Math.sin(a)*R); ctx.stroke();
        var la = START + (i+0.5)*2*Math.PI/N;
        var lx = CX+Math.cos(la)*(R+24);
        var ly = CY+Math.sin(la)*(R+24);
        lx = Math.max(90, Math.min(W-90, lx));
        ctx.fillStyle = CONFIG.colors.ink;
        ctx.textAlign = Math.abs(Math.cos(la))<0.25 ? 'center' : (Math.cos(la)>0?'left':'right');
        ctx.textBaseline = 'middle';
        wrapLabel(segs[i].name, lx, ly);
      }
    }
    function drawWheel(t){
      ctx.clearRect(0,0,W,H);
      drawGrid();
      var sliceA = 2*Math.PI/N, i, ac, rad, px, py;
      for(i=0;i<N;i++){
        var a0 = START + i*sliceA, a1 = a0 + sliceA;
        rad = R * (scores[i]/MAX) * t;
        ctx.beginPath(); ctx.moveTo(CX,CY); ctx.arc(CX,CY, rad, a0, a1); ctx.closePath();
        ctx.fillStyle = hexToRgba(segs[i].color, 0.62); ctx.fill();
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.stroke();
      }
      ctx.beginPath();
      for(i=0;i<N;i++){
        ac = START + (i+0.5)*sliceA; rad = R*(scores[i]/MAX)*t;
        px = CX+Math.cos(ac)*rad; py = CY+Math.sin(ac)*rad;
        if(i===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
      }
      ctx.closePath(); ctx.lineWidth = 3; ctx.strokeStyle = CONFIG.colors.brand; ctx.stroke();
      ctx.fillStyle = hexToRgba(CONFIG.colors.brand, 0.08); ctx.fill();
      for(i=0;i<N;i++){
        ac = START + (i+0.5)*sliceA; rad = R*(scores[i]/MAX)*t;
        px = CX+Math.cos(ac)*rad; py = CY+Math.sin(ac)*rad;
        ctx.beginPath(); ctx.arc(px,py,6,0,Math.PI*2);
        ctx.fillStyle = segs[i].color; ctx.fill();
        ctx.lineWidth = 2.5; ctx.strokeStyle = '#fff'; ctx.stroke();
      }
      ctx.beginPath(); ctx.arc(CX,CY,5,0,Math.PI*2); ctx.fillStyle = CONFIG.colors.muted; ctx.fill();
    }
    function animateWheel(){
      var dur = 1200, startTs = null;
      function frame(ts){
        if(!startTs) startTs = ts;
        var p = Math.min((ts-startTs)/dur, 1);
        drawWheel(1 - Math.pow(1-p, 3));
        if(p<1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    }

    // Download PNG
    $('downloadBtn').addEventListener('click', function(){
      var pad = 50, headH = 96;
      var out = document.createElement('canvas');
      out.width = W + pad*2; out.height = H + pad*2 + headH;
      var o = out.getContext('2d');
      o.fillStyle = CONFIG.colors.bg; o.fillRect(0,0,out.width,out.height);
      o.fillStyle = CONFIG.colors.ink; o.textAlign = 'center';
      o.font = "600 40px 'Cormorant Garamond',Georgia,serif";
      o.fillText(CONFIG.title, out.width/2, 60);
      var avg = (scores.reduce(function(a,b){return a+b;},0)/segs.length).toFixed(1);
      o.font = "600 19px 'Montserrat',-apple-system,Segoe UI,Roboto,sans-serif";
      o.fillStyle = CONFIG.colors.muted;
      o.fillText('Overall balance: '+avg+' / '+MAX, out.width/2, 88);
      o.drawImage(canvas, pad, headH+pad, W, H);
      var link = document.createElement('a');
      link.download = 'my-wheel-of-reconnect.png';
      link.href = out.toDataURL('image/png');
      link.click();
    });
  }

  class ParallaxxWheelOfReconnect extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      try{ boot(shadow); }catch(e){ console.error('[px-wheel] boot failed:', e); }
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      window.addEventListener('resize', function(){ collapseAncestors(host); }, {passive:true});
    }
  }
  customElements.define('parallaxx-wheel-of-reconnect', ParallaxxWheelOfReconnect);
})();
