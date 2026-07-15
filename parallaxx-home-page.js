/* PARALLAXX TRANSFORMATIONS — Home page Wix Custom Element. Tag: parallaxx-home-page.
   Converted from the dc design to a self-contained shadow-DOM element (same pattern as gia-home-page.js).
   In the Wix editor: turn the site Header + Footer OFF for this page. */
(function(){
  if (customElements.get('parallaxx-home-page')) return;

  var CSS = `/* ═══════════════════════════════════════════════════════════════════
   PARALLAXX - HOME - v4  "EVERYTHING IS GLASS"
   -------------------------------------------------------------------
   v3 had a bespoke hero and then fell back on layout defaults --
   centred headings, three white cards, a quote grid. That is the house
   style of every coach site on the internet, and it is what happens
   when the IDEA stops at the fold.

   So: the whole page is made of glass. Every section is another pane
   in another state. The visitor keeps meeting the same material.

     01 HERO      dirty pane. he wipes it. Daniel is behind it.
     02 MIRROR    his confessions arrive FOGGED, and wipe clear on scroll
     03 REFRAME   draggable divider: his side vs her side of the same pane
     04 MASKS     five men, five different kinds of dirt
     05 SYSTEM    three panes of glass. pull one out, see what stays dirty.
     06 DANIEL    the ONLY image on the site with no glass on it at all
     07 PROOF     one face, one quote
     08 CREDS     demoted. proof closes, it does not open.

   TOKENS shared with GIVE IT ALL:  navy #061938 gold #E8C65F Montserrat
   TOKENS Parallaxx only:  coral #FF501F  Cormorant  Caveat  cream #F1ECE1

   ===================================================================
   THE ACCENT RULE.  GOLD IS DANIEL. CORAL IS YOU.
   -------------------------------------------------------------------
   GOLD  #E8C65F -- Daniel's VOICE. Everything he says.
                    His handwriting (Caveat). His emphasis inside prose.
                    His pull-quotes. Section labels. Hairlines.
                    Shared with GIVE IT ALL -- it is the family colour.

   CORAL #FF501F -- THE READER. His words, his actions, his moves.
                    Buttons. Links. Controls. The divider handle. Active
                    states. The confession cards -- because those are HIS
                    sentences, not Daniel's. And the microcopy that tells
                    him to do something.

   Coral never appears as decorative emphasis in prose. Reason is
   commercial, not aesthetic: colour is a scarcity currency, and every
   coral word on the page devalues the coral BUTTON. Keep coral rare and
   the eye finds the CTA without being asked.

   Structural emphasis inside body copy is ink (#1E2A3D on cream,
   #F1ECE1 on navy) -- never an accent.
   =================================================================== 
   ═══════════════════════════════════════════════════════════════════ */
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  ::selection{background:#FF501F;color:#fff}
  img{display:block;max-width:100%}

  #px-root{background:#04122A;color:#B1BFD7;font-family:'Montserrat',system-ui,sans-serif;font-size:16px;line-height:1.7;overflow-x:clip;position:relative}
  .px-serif{font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;letter-spacing:-.005em}
  .px-hand{font-family:'Caveat',cursive}
  .px-wrap{max-width:1240px;margin:0 auto}
  .px-sec{padding:clamp(52px,6.5vw,92px) clamp(20px,4vw,52px);position:relative}
  .px-label{font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:#5E6B85}

  .px-btn{display:inline-flex;align-items:center;gap:.55em;background:#FF501F;color:#fff;font-weight:700;font-size:.98rem;padding:1.05em 2.2em;border-radius:999px;text-decoration:none;transition:background .3s,transform .3s,box-shadow .3s;box-shadow:0 10px 30px -12px rgba(255,80,31,.5)}
  .px-btn:hover{background:#FF6A3D;transform:translateY(-2px)}
  .px-ghost{display:inline-flex;align-items:center;gap:.55em;color:#E8C65F;border:1px solid rgba(232,198,95,.4);font-weight:600;font-size:.94rem;padding:1em 2em;border-radius:999px;text-decoration:none;transition:background .3s,border-color .3s}
  .px-ghost:hover{background:rgba(232,198,95,.1);border-color:#E8C65F}

  /* KINETIC TYPE.
     Each .px-line is ONE line, masked and slid up. Which means each one must
     actually FIT on one line -- if it wraps, the mask breaks and you get
     orphaned single-word rows.

     The bug: these headlines were sitting in a max-width:68ch box. 'ch' is
     measured against the BODY font size (~9px per char), so that box is only
     ~630px wide -- while a 54px display headline needs ~1000px. It wrapped
     four times and orphaned a word.

     So: headline containers get their own width, in px, sized for DISPLAY
     type -- never the body measure. And each line refuses to wrap. */
  .px-line{display:block;overflow:hidden}
  .px-line > span{display:block;transform:translateY(110%);will-change:transform;white-space:nowrap}
  @media(max-width:820px){
    .px-line > span{white-space:normal}   /* let it wrap on small screens rather than overflow */
  }
  .px-head{max-width:min(1020px,92vw);margin-left:auto;margin-right:auto}
  .px-fade{opacity:0;transform:translateY(22px);will-change:transform,opacity}

  .px-ph{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:11px;padding:30px;
    background:repeating-linear-gradient(45deg,rgba(255,80,31,.05) 0 12px,rgba(255,80,31,.10) 12px 24px);
    border:2px dashed #FF501F;border-radius:18px;min-height:280px}
  .px-ph b{font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;color:#FF501F;font-weight:800}
  .px-ph span{font-size:.87rem;line-height:1.7;max-width:36ch;color:#E6BCAC}
  .px-ph em{font-style:normal;font-size:.73rem;line-height:1.6;color:#8E9BB2;max-width:38ch}
  .px-ph.on-cream span{color:#8A5A47}.px-ph.on-cream em{color:#A6968A}

  /* ── 01 HERO ─────────────────────────────────────────────── */
  #px-hero{position:relative;height:100svh;min-height:640px;overflow:hidden;background:#04122A}
  #px-glass{position:absolute;inset:0;width:100%;height:100%;display:block}
  /* THE FALLBACK — mobile, reduced-motion, and low-power machines.
     This is not a second-class path. There is no cursor on a phone, so
     there is no wipe -- which means without this the biggest half of the
     audience would sit behind permanently dirty glass and NEVER see the
     face. The face is the entire payoff. So on the fallback the glass
     clears on SCROLL instead, driven by --px-clear (0 -> 1) below.

     background-position anchors on the face, not the centre: on a tall
     phone a centre-crop of a 16:10 frame throws his head off the right. */
  #px-fallback{position:absolute;inset:0;background:#04122A;display:none;--px-clear:0}
  #px-fallback .fb-img{position:absolute;inset:0;background-size:cover;background-position:70% 18%;
    filter:saturate(calc(.55 + .45*var(--px-clear)))
           contrast(calc(1.05 - .05*var(--px-clear)))
           brightness(calc(.5 + .5*var(--px-clear)))
           blur(calc(9px*(1 - var(--px-clear))))}
  #px-fallback .fb-glass{position:absolute;inset:0;
    background:rgba(180,160,120,calc(.30*(1 - var(--px-clear))))}
  #px-hero-veil{position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(90deg,rgba(4,18,42,.90) 0%,rgba(4,18,42,.58) 44%,rgba(4,18,42,.04) 78%),
               linear-gradient(0deg,rgba(4,18,42,.86) 0%,rgba(4,18,42,0) 52%)}
  #px-hero-copy{position:absolute;inset:0;display:flex;align-items:center;padding:0 clamp(20px,5vw,90px);pointer-events:none}
  #px-hero-copy .inner{max-width:min(640px,54vw);pointer-events:auto}
  @media(max-width:900px){#px-hero-copy .inner{max-width:100%}}

  /* -- 02 MIRROR : the confessions ------------------------------
     They used to sit in a 6-up grid -- all on screen at once, so the eye
     SCANNED them and they blurred into "a list of sad things". Not one
     landed.

     Now they're staggered down an offset column: only one or two are ever
     in view, so the SCROLL is what delivers them one at a time. Each wipes
     clear as it individually arrives -- guaranteed, on every device, with
     no interaction required.

     Hover only ACCELERATES it. A reward for the curious, never a toll.
     We do not gate the best copy on the page behind a mechanic.  ----- */
  /* -- 02 THE MIRROR : a message thread with yourself -----------
     The six confessions were cards, then a mosaic, and both read as a
     COMPONENT -- a set of items presented to him.

     They're a conversation. The honest self messages him at 2am; the
     polished self has an answer for every one of them.

     LEFT  = incoming. The man behind the glass. Unbidden.
     RIGHT = him. His own excuses. Marked 'delivered'. He sent those.
     The last message gets NO REPLY -- an empty dashed box where his
     answer should be. That silence is the whole section.

     Layout: thread left, sticky column right. A 720px thread centred in
     a 1240px page wastes both flanks and reads as endless. Now the man
     who's sending the messages sits beside them and never leaves. ---- */
  /* THE PHONE.
     v9 made the thread shorter but left it 640px wide -- a letterbox, not a
     phone. It has to hold the DEVICE ratio: narrow and tall (~9:19).
     So the left column shrinks to hold a phone, and the right column takes
     the width it gives back. */
  /* The phone is a fixed 9:19.4 slab -- about 730px tall. The text beside it
     is shorter. align-items:start left a dead 200px hole under the copy.
     CENTRE the text against the phone: the leftover height splits into two
     even margins instead of pooling at the bottom as a gap. */
  #px-mirror-grid{display:grid;grid-template-columns:.82fr 1.18fr;gap:clamp(30px,4.5vw,72px);
    align-items:center;max-width:1180px;margin:0 auto}
  #px-sticky{position:relative}

  .px-phone{width:min(340px,100%);margin:0 auto;aspect-ratio:9/19.4;position:relative;
    background:#1A1A1E;border-radius:42px;padding:11px;
    box-shadow:0 40px 90px -40px rgba(30,42,61,.55), 0 0 0 1px rgba(160,138,94,.22)}
  .px-screen{position:relative;height:100%;background:#FBF8F2;border-radius:32px;overflow:hidden;
    display:flex;flex-direction:column}
  .px-notch{position:absolute;top:9px;left:50%;transform:translateX(-50%);
    width:82px;height:6px;border-radius:99px;background:#2B2B31;z-index:4}

  .px-thread-hd{display:flex;align-items:center;gap:9px;padding:22px 16px 11px;
    border-bottom:1px solid rgba(160,138,94,.2);background:#FBF8F2;position:relative;z-index:3;flex:0 0 auto}
  .px-av{width:29px;height:29px;border-radius:50%;background:#12233F;color:#E8C65F;
    display:flex;align-items:center;justify-content:center;font-weight:800;font-size:10px;flex:0 0 auto}

  /* NO INTERNAL SCROLL. The whole conversation fits on one screen.
     v10 translated a tape inside a masked window and you had to chase the
     top message. Nobody should have to work to read the thing that's meant
     to describe their life. Smaller type, one screen, done. */
  #px-window{position:relative;flex:1;padding:10px 13px 0;display:flex;flex-direction:column;justify-content:center}
  #px-tape{padding:0}

  /* INCOMING -- the honest self. fogged until it climbs the screen. */
  .px-in{display:flex;justify-content:flex-start;margin-bottom:5px}
  .px-in > div{max-width:90%;position:relative;overflow:hidden;border-radius:15px 15px 15px 4px}
  .px-bub{background:#1E2A3D;color:#F1ECE1;padding:9px 13px;font-size:11.5px;line-height:1.42}
  .px-in.last > div{border:1px solid rgba(232,198,95,.6);box-shadow:0 0 0 3px rgba(232,198,95,.1)}
  .px-fog{position:absolute;top:-2px;bottom:-2px;left:-4%;width:112%;pointer-events:none;
    transform:translateX(0);transition:transform 1.7s cubic-bezier(.5,0,.15,1);
    background:linear-gradient(96deg,rgba(198,175,132,0) 0%,rgba(206,186,148,.6) 6%,
      rgba(198,175,132,.97) 14%,rgba(212,195,163,.97) 60%,rgba(198,175,132,.98) 100%)}
  .px-in.wiped .px-fog{transform:translateX(104%)}

  /* OUTGOING -- his excuse. a brush-off. */
  .px-out{display:flex;justify-content:flex-end;margin-bottom:12px}
  .px-out > div{max-width:80%}
  .px-out .b{background:#EDE7DC;color:#8A8073;padding:7px 12px;border-radius:15px 15px 4px 15px;
    font-size:10.5px;line-height:1.38}
  .px-meta{text-align:right;font-size:8px;letter-spacing:.1em;text-transform:uppercase;
    font-weight:700;color:#C6BBAA;margin:3px 3px 0 0}

  /* THE SILENCE. */
  .px-none{margin-bottom:0}
  .px-none > div{width:142px}
  .px-none .b{border:1px dashed rgba(255,80,31,.45);border-radius:15px 15px 4px 15px;height:32px;
    display:flex;align-items:center;justify-content:center;background:rgba(255,80,31,.03);
    font-size:8.5px;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:#FF501F}

  @media(max-width:860px){
    #px-mirror-grid{grid-template-columns:1fr}
    #px-sticky{order:-1;margin-bottom:30px}
    .px-phone{width:min(320px,90%)}
  }

  /* -- 03 REFRAME : the divider IS the section ------------------
     v4 made it a card in a box -- a demo sitting in its own module.
     Now the glass is the section background and the copy lives INSIDE
     the two sides. Drag the handle and the argument moves with it. -- */
  #px-reframe{position:relative;min-height:58svh;display:flex;align-items:center;overflow:hidden;background:#0A1D3C;cursor:ew-resize;user-select:none}
  #px-split{position:absolute;inset:0;width:100%;height:100%;display:block}
  #px-rf-veil{position:absolute;inset:0;pointer-events:none;background:linear-gradient(0deg,rgba(6,25,56,.94) 0%,rgba(6,25,56,.62) 45%,rgba(6,25,56,.72) 100%)}
  #px-handle{position:absolute;top:0;bottom:0;width:2px;background:#FF501F;box-shadow:0 0 30px rgba(255,80,31,.8);pointer-events:none;z-index:3}
  #px-handle::after{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:54px;height:54px;border-radius:50%;background:#FF501F;box-shadow:0 8px 30px rgba(255,80,31,.55)}
  #px-handle::before{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:20px;height:10px;z-index:1;
    background:linear-gradient(90deg,#fff 0 4px,transparent 4px 8px,#fff 8px 12px,transparent 12px 16px,#fff 16px 20px);opacity:.9}
  #px-rf-copy{position:relative;z-index:2;width:100%;padding:0 clamp(20px,4vw,52px);pointer-events:none}
  .px-rf-side{max-width:34ch}
  .px-rf-tag{display:inline-block;padding:7px 14px;border-radius:999px;font-size:.64rem;letter-spacing:.16em;text-transform:uppercase;font-weight:800;margin-bottom:16px}

  /* -- 04 THE FIVE PANES ----------------------------------------
     v7 gave each archetype its own bespoke CSS "film" -- frost for the
     Fortress, rain-runs for the Defender, glare for the Idealist. Clever,
     and nobody could read it. Texture cannot carry a personality. It was
     decoration wearing the costume of meaning, and the cards ended up 80%
     empty gradient and 20% words -- when the WORDS were the section.

     So: one consistent film on all five. They are all glass; "five kinds
     of glass" is a distinction the reader has no key for. And behind each
     pane, a FACE -- the first ten seconds of that archetype's video.

     Hover clears ONE pane. Five dirty windows in a row, and as he moves
     across, one at a time comes alive and looks back at him. That is the
     whole page compressed into a card.

     It does not spend the quiz. The clip gives him APPETITE; the quiz
     tells him WHICH ONE IS HIS. Different products.
     ------------------------------------------------------------------ */
  #px-panes{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;max-width:1240px;margin:0 auto}
  .px-pane{position:relative;display:flex;flex-direction:column;justify-content:flex-end;
    aspect-ratio:4/5;                       /* a FACE wants portrait. square crops the shoulders off. */
    padding:20px 18px;border-radius:14px;cursor:pointer;overflow:hidden;
    background:#0A1D3C;border:1px solid rgba(232,198,95,.14);
    transition:border-color .35s ease,transform .35s ease}

  /* THE VIDEO. preload=none -- nothing loads until he reaches for it.
     Five autoplaying clips on a page with four WebGL canvases would be
     brutal, and 90% of visitors never touch a single one. */
  .px-pane video, .px-pane .poster{position:absolute;inset:0;width:100%;height:100%;
    object-fit:cover;pointer-events:none}
  .px-pane video{opacity:0;transition:opacity .9s ease}
  .px-pane.on video{opacity:1}
  .px-pane .poster{background-size:cover;background-position:center 22%;
    filter:saturate(.5) brightness(.62);transition:filter .9s ease}
  .px-pane.on .poster{filter:saturate(1) brightness(1)}

  /* ═══ THE FILMS ═══════════════════════════════════════════════════
     Each archetype is a DIFFERENT PHYSICAL THING covering the glass, and
     each one comes OFF in the way that thing would come off. The film is
     no longer being asked to communicate the archetype on its own -- the
     face and the words do that -- so it's free to be flavour, and
     flavour can be as literal as it likes.

       01 FORTRESS  bricks     ->  they fall away, bottom row first
       02 DEFENDER  graph grid ->  it retracts and burns off
       03 IDEALIST  golden bloom -> the fantasy collapses to a point
       04 PERFORMER stage curtain -> it parts, and the show is over
       05 ROMANTIC  dust sheet ->  it slides off, like uncovering furniture

     Every one of them is CSS transforms on a handful of divs. No GPU,
     no images, no libraries. ═══════════════════════════════════════ */
  /* ═══ PALETTE DISCIPLINE FOR THE FILMS ════════════════════════════
     The films are THE DIRT. They are neither Daniel nor the reader, so
     they have NO claim on gold or coral.

     v8 broke this twice: a brick-red stage curtain (a SECOND red on a
     page where coral is the one red and it means "press me" -- a full
     height red curtain quietly devalues the CTA sitting under it), and a
     muddy brown in the bloom that isn't in the system at all. Meanwhile
     three of the five were the same blue-grey, which is the "row of blue
     boxes" problem all over again.

     So the five are told apart by MATERIAL and VALUE, not by hue. Every
     one lives in navy / slate / mist / cream, with gold used only where
     it is literally LIGHT.

       01  deep navy masonry      DARK    heavy
       02  mist rules on slate    MID     precise
       03  cream-gold glare       BRIGHT  blown out
       04  navy velvet + gold     DARK    theatrical
       05  pale cream sheet       PALE    silent

     dark -> mid -> bright -> dark -> pale. A real rhythm across the row,
     and coral is left alone to mean exactly one thing. ═══════════════ */
  .px-film{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden}

  /* 01 — BRICKS. A fortress is a wall, so give him a wall. The heaviest,
     darkest thing in the row: this one should feel like WEIGHT.
     Falls bottom-up -- the base goes first and the rest comes down after it. */
  .px-brick{position:absolute;border-radius:1px;
    background:linear-gradient(150deg,rgba(52,74,108,.97),rgba(22,42,74,.96));
    box-shadow:inset 0 1px 0 rgba(177,191,215,.20), inset 0 -2px 0 rgba(3,10,24,.55);
    transition:transform 1.05s cubic-bezier(.45,0,.7,.2), opacity .85s ease}
  .px-pane.on .px-brick{transform:translateY(150%) rotate(var(--r)) ;opacity:0}

  /* 02 — GRAPH PAPER. Everything filed, ruled, catalogued. You get the
     schema of how he feels. Cold, exact, clinical. Retracts and burns off. */
  .px-grid{position:absolute;inset:-8%;
    background:
      repeating-linear-gradient(0deg,rgba(177,191,215,.40) 0 1px,transparent 1px 13px),
      repeating-linear-gradient(90deg,rgba(177,191,215,.40) 0 1px,transparent 1px 13px),
      linear-gradient(160deg,rgba(86,112,152,.80),rgba(46,72,112,.86));
    transition:transform 1.1s cubic-bezier(.2,.8,.2,1), opacity .9s ease}
  .px-pane.on .px-grid{transform:scale(1.35);opacity:0}

  /* 03 — THE GLARE. Blown out by an idealised light -- and gold IS this
     site's light, so this is the one film that gets to be warm. Cream at
     the core, gold falling off, and it lands on NAVY at the edge. No brown.
     On hover the fantasy collapses to a point. */
  .px-bloom{position:absolute;inset:0;
    background:radial-gradient(circle at 56% 34%,rgba(248,242,228,.97),rgba(232,198,95,.72) 38%,rgba(20,44,80,.80) 82%);
    transition:transform 1.15s cubic-bezier(.5,0,.2,1), opacity .95s ease;transform-origin:56% 34%}
  .px-pane.on .px-bloom{transform:scale(.06);opacity:0}

  /* 04 — THE CURTAIN. He's been on stage his whole life.
     NAVY VELVET, not red. A stage curtain doesn't have to be scarlet, and a
     dark velvet one looks more expensive anyway. The gold does the SPOTLIGHT
     work on the ribs -- which is what gold is for -- and coral is left alone
     to mean "press me". */
  .px-curtain{position:absolute;top:0;bottom:0;width:50.6%;
    transition:transform 1.2s cubic-bezier(.55,0,.2,1)}
  .px-curtain.l{left:0;background:linear-gradient(90deg,rgba(10,26,54,.98),rgba(34,60,100,.94) 58%,rgba(8,22,48,.98));
    box-shadow:inset -12px 0 26px -8px rgba(2,8,20,.9)}
  .px-curtain.r{right:0;background:linear-gradient(270deg,rgba(10,26,54,.98),rgba(34,60,100,.94) 58%,rgba(8,22,48,.98));
    box-shadow:inset 12px 0 26px -8px rgba(2,8,20,.9)}
  .px-curtain::after{content:'';position:absolute;inset:0;      /* velvet ribs, catching a gold light */
    background:repeating-linear-gradient(90deg,rgba(2,8,20,.34) 0 2px,transparent 2px 10px,rgba(232,198,95,.14) 10px 13px)}
  .px-pane.on .px-curtain.l{transform:translateX(-101%)}
  .px-pane.on .px-curtain.r{transform:translateX(101%)}

  /* 05 — THE DUST SHEET. A life under wraps. The palest thing in the row,
     and the quietest -- cream going to mist. Nothing happening at all. */
  .px-sheet{position:absolute;inset:0;
    background:linear-gradient(178deg,rgba(241,236,225,.94),rgba(207,209,214,.90) 52%,rgba(177,191,215,.92));
    box-shadow:inset 0 12px 26px -12px rgba(255,255,255,.6), inset 0 -20px 30px -22px rgba(30,42,61,.35);
    transition:transform 1.25s cubic-bezier(.35,0,.2,1)}
  .px-sheet::after{content:'';position:absolute;inset:0;        /* the weave */
    background:repeating-linear-gradient(96deg,rgba(255,255,255,.16) 0 3px,transparent 3px 9px)}
  .px-pane.on .px-sheet{transform:translateY(101%)}

  /* the smear of glass that sits over every film, and the scrim that keeps
     the words readable. */
  .px-pane::after{content:'';position:absolute;inset:0;pointer-events:none;z-index:2;
    background:repeating-linear-gradient(101deg,rgba(255,255,255,.05) 0 1px,transparent 1px 6px),
               linear-gradient(0deg,rgba(4,18,42,.94) 0%,rgba(4,18,42,.52) 32%,transparent 60%);
    transition:opacity .9s ease}
  /* SCRIM OFF WHEN IT PLAYS. The clip has its own burnt-in captions along
     the bottom -- a navy gradient sitting on top of them is just dirt on a
     subtitle. */
  .px-pane.on::after{opacity:.14}
  .px-pane.on{border-color:rgba(255,80,31,.55);transform:translateY(-3px)}

  /* THE WORDS.
     Number + NAME live at the TOP. They stay put, always, so he never loses
     track of which pane he's looking at.
     The DESCRIPTION lives at the bottom -- and gets out of the way the
     instant the clip runs, because that's where the captions are. */
  /* DO NOT put a blanket \`.px-pane > *{position:relative}\` here.
     It has the same specificity as \`.px-film\` (one class each) and sits
     later in the sheet, so it WINS -- and quietly turns the film container
     into a zero-height static div. Every brick, curtain and dust sheet then
     lays itself out inside nothing and renders as nothing. No error, no
     warning, just five empty cards. Target the text directly instead. */
  .px-pane > .n{position:absolute;top:18px;left:18px;z-index:3;
    font-family:'Cormorant Garamond',serif;font-size:1.9rem;
    color:rgba(232,198,95,.6);line-height:1}
  .px-pane > h3, .px-pane > p{position:relative;z-index:3}
  /* THE WHOLE BOTTOM BLOCK CLEARS OUT WHEN THE CLIP RUNS.
     Title and description both. The clip has its own captions, and the
     captions say who is talking -- so the title is redundant the moment
     his face is on screen, and redundant text over a video is just dirt
     on a subtitle.

     opacity ONLY -- no display, no height change, no transform. The block
     keeps its box, so nothing under it reflows and the card doesn't twitch.
     The number stays in the corner as the one persistent marker of which
     pane he's on. */
  .px-pane h3{font-size:.95rem;font-weight:800;color:#F1ECE1;line-height:1.3;margin:0 0 7px;
    text-shadow:0 1px 12px rgba(4,18,42,.9);transition:opacity .45s ease}
  .px-pane p{font-size:.84rem;line-height:1.5;color:#C4CEE0;margin:0;
    transition:opacity .45s ease}
  .px-pane.on h3, .px-pane.on p{opacity:0;pointer-events:none}

  /* the cue. only on the panes that actually have a clip. */
  .px-pane .cue{position:absolute;top:20px;right:16px;z-index:4;font-size:.6rem;letter-spacing:.14em;
    text-transform:uppercase;font-weight:800;color:rgba(232,198,95,.55);transition:opacity .35s ease}
  .px-pane.on .cue{opacity:0}
  @media(prefers-reduced-motion:reduce){
    .px-brick,.px-grid,.px-bloom,.px-curtain,.px-sheet{transition:opacity .3s ease !important}
    .px-pane.on .px-brick,.px-pane.on .px-grid,.px-pane.on .px-bloom,
    .px-pane.on .px-curtain,.px-pane.on .px-sheet{transform:none !important;opacity:0 !important}
  }

  @media(max-width:980px){#px-panes{grid-template-columns:repeat(2,1fr)}}
  /* 360px cap is load-bearing: it puts the 720px-wide clip at exactly 2x. */
  @media(max-width:560px){#px-panes{grid-template-columns:1fr;justify-items:center}
    .px-pane{width:100%;max-width:360px}}

  /* ── 05 SYSTEM : three panes ──────────────────────────────── */
  /* SQUARE, not 4:3. The reveal behind this glass is a vertical photograph of
     two people, and forcing a portrait frame into a landscape stage is the
     exact mistake that gave the divider a band of teeth. Square holds the
     POSTURE -- her leaning her weight on him, her arm round his neck, her
     hand on his chest -- which is the whole argument. A landscape crop keeps
     the faces and throws the reaching away.

     BUT SQUARE IS TALL, and a square stage in a 1.12fr column on a wide
     screen becomes an enormous box -- the section stopped fitting on a 14"
     laptop, which is what most people are actually reading this on. So the
     stage is CAPPED and centred in its column. It stays square; it just
     stops trying to be 600px tall. The whole section has to be takeable in
     one screen, or the three clicks never happen. */
  #px-vv-stage{position:relative;aspect-ratio:1/1;border-radius:18px;overflow:hidden;background:#04122A;
    width:100%}
  #px-vv-c{position:absolute;inset:0;width:100%;height:100%;display:block}
  /* THE SCRIM RUNS TO THE EDGE. It has to -- it's a gradient, and a gradient
     that stops short of the frame leaves a hard seam with a strip of photo
     below it.

     The previous version lifted the whole overlay to bottom:6% and tried to
     patch the gap with an ::after. That failed for a dull reason: a
     percentage height on the pseudo-element resolves against the OVERLAY's
     height, not the stage's, so the patch came out the wrong size and you
     got the strip anyway.

     Lift the TEXT, not the BOX. Bottom padding does it, and the gradient
     still reaches the corner. */
  #px-vv-overlay{position:absolute;left:0;right:0;bottom:0;padding:30px 26px 44px;pointer-events:none;
    background:linear-gradient(0deg,rgba(4,18,42,.95) 30%,rgba(4,18,42,.72) 62%,rgba(4,18,42,0))}
  .px-pill{flex:1;padding:11px 8px;border-radius:12px;font-weight:800;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;transition:all .25s ease;border-width:2px;border-style:solid}
  .px-card{background:#fff;border-radius:20px;padding:28px 30px;border-top:3px solid #E8C65F;transition:border-color .3s ease}

  /* Row 1 = stage | card.  Row 2 = pills+caption | (nothing).
     So row 1's height IS the image's height, and the card centres against the
     PICTURE rather than against picture-plus-buttons. And it hugs its own
     content -- no cathedral of white space around three lines of text. */
  #px-vv-grid{display:grid;grid-template-columns:minmax(0,470px) minmax(0,1fr);
    grid-template-rows:auto auto;column-gap:clamp(24px,3vw,48px);row-gap:14px;
    max-width:1080px;margin:0 auto}
  #px-vv-card{grid-column:2;grid-row:1;align-self:center}
  #px-vv-controls{grid-column:1;grid-row:2}
  @media(max-width:820px){
    #px-vv-grid{grid-template-columns:1fr}
    #px-vv-stage{grid-column:1;grid-row:1}
    #px-vv-controls{grid-column:1;grid-row:2}
    #px-vv-card{grid-column:1;grid-row:3;align-self:auto;margin-top:8px}
  }
  /* THE FORK. Home carries the shared truth. The brutal, gendered pain
     lives behind these two doors, where it can hit as hard as it likes. */
  .px-doors{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:760px;margin:26px auto 0}
  @media(max-width:680px){.px-doors{grid-template-columns:1fr}}
  .px-door{display:block;text-align:left;background:rgba(241,236,225,.04);border:1px solid rgba(241,236,225,.12);
    border-radius:18px;padding:26px 28px;text-decoration:none;transition:border-color .3s ease,background .3s ease,transform .3s ease}
  .px-door:hover{border-color:rgba(255,80,31,.55);background:rgba(255,80,31,.07);transform:translateY(-3px)}
  .px-door .eyebrow{font-size:.64rem;letter-spacing:.2em;text-transform:uppercase;font-weight:800;color:#E8C65F;margin-bottom:10px}
  .px-door h4{font-family:'Cormorant Garamond',Georgia,serif;font-weight:300;font-size:clamp(21px,2.2vw,29px);color:#F1ECE1;margin-bottom:10px;line-height:1.2}
  .px-door p{font-size:.9rem;line-height:1.7;color:#8E9BB2;margin-bottom:14px}
  .px-door span.go{font-size:.82rem;font-weight:700;color:#FF6A3D}

  /* THE DOORS MOVED TO CREAM, so they need a cream skin. The navy versions
     above (translucent white on dark, gold eyebrow, cream heading) go
     invisible on #F1ECE1 -- 4% white on cream is nothing, and #F1ECE1 text
     on #F1ECE1 is literally nothing.
     Gold also has to go: it has no contrast on cream. Bronze #A08A5E is the
     cream-side equivalent, same voice, legible. */
  .px-door.on-cream{background:#FBF8F2;border:1px solid #E2DACB;
    box-shadow:0 18px 40px -30px rgba(30,42,61,.45)}
  .px-door.on-cream:hover{border-color:rgba(255,80,31,.5);background:#fff;
    box-shadow:0 24px 50px -28px rgba(30,42,61,.5)}
  .px-door.on-cream .eyebrow{color:#A08A5E}
  .px-door.on-cream h4{color:#1E2A3D}
  .px-door.on-cream p{color:#5E5850}
  .px-door.on-cream span.go{color:#FF501F}
  /* ── 07 PROOF : real faces, real names ────────────────────────────
     These were flattened into PNGs on the live Testimonials page -- photo,
     quote and name baked into one image. Which means Google reads NONE of it,
     a screen reader gets nothing, and it cannot reflow on a phone. Every one
     of these quotes was invisible to search. Now it's text, and the faces are
     cropped out of the source files with Wix's own crop transform -- so no
     re-upload, no reshoot, and the words are indexable. */
  /* SMALL FACES. This is the whole design rule for the section:
     THE WORDS ARE THE PROOF. THE FACE IS ONLY THE VERIFICATION.

     v1 ran these as 380px squares and it backfired -- Tobias's is a corporate
     headshot on a grey studio backdrop, Gena's is a moody photoshoot profile
     where she isn't even looking at the lens. Fine photographs; blown up they
     stop reading as CLIENTS and start reading as IMAGERY. And imagery invites
     the one question you never want asked here: are these people real?

     A face needs to be big enough to say "a human being said this" and not one
     pixel bigger. The moment it's large enough to admire as a photograph it is
     competing with the sentence it exists to authenticate. */
  .px-face{width:64px;height:64px;flex:0 0 auto;object-fit:cover;border-radius:999px;display:block;
    filter:saturate(.9) contrast(1.02);
    box-shadow:0 0 0 1px rgba(232,198,95,.30), 0 8px 18px -10px rgba(3,12,28,.9)}
  .px-face.lg{width:78px;height:78px}
  .px-byline{display:flex;align-items:center;gap:14px}
  .px-byline .who{font-size:.9rem;font-weight:700;color:#E8C65F;line-height:1.45}
  .px-byline .who span{display:block;font-size:.76rem;font-weight:500;color:#7C89A3;margin-top:2px}

  /* ── VIDEO FACADE ─────────────────────────────────────────────────
     A YouTube <iframe> drags in ~1MB of JS and several third-party requests
     BEFORE anybody presses anything. Five of them on a page that already runs
     four WebGL canvases would be indefensible -- and most visitors play none.

     So these are just thumbnails. The real iframe is created on CLICK, with
     autoplay, and it replaces the button in place. Zero cost until asked. */
  .px-vid{position:relative;display:block;width:100%;padding:0;border:0;cursor:pointer;
    background:#04122A;border-radius:16px;overflow:hidden;aspect-ratio:16/9;
    box-shadow:0 26px 60px -34px rgba(3,12,28,.95), 0 0 0 1px rgba(232,198,95,.14);
    transition:transform .3s ease, box-shadow .3s ease}
  .px-vid:hover{transform:translateY(-3px);box-shadow:0 30px 70px -32px rgba(3,12,28,1), 0 0 0 1px rgba(232,198,95,.34)}
  .px-vid > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    filter:saturate(.92) brightness(.86);transition:filter .3s ease}
  .px-vid:hover > img{filter:saturate(1) brightness(1)}
  /* THE PLAY BUTTON IS NOT IN THE MIDDLE.
     It's a talking head, filmed on a webcam, and he is dead centre in frame.
     A 62px centred button lands squarely on his MOUTH -- the one part of a
     testimonial that has to look like it's speaking. Bottom-left instead:
     out of his face, into the quiet corner, and it reads as a control rather
     than a sticker. */
  .px-vid .play{position:absolute;left:20px;bottom:20px;
    width:58px;height:58px;border-radius:999px;background:rgba(255,80,31,.94);
    box-shadow:0 10px 30px -8px rgba(255,80,31,.6);transition:transform .3s ease}
  .px-vid .play::after{content:'';position:absolute;top:50%;left:53%;transform:translate(-50%,-50%);
    border-style:solid;border-width:10px 0 10px 16px;border-color:transparent transparent transparent #fff}
  .px-vid:hover .play{transform:scale(1.09)}
  /* SAY THE RUNTIME. This is a 13-minute interview and pretending otherwise
     just ambushes him. Naming it up front costs a few clicks and improves
     every one that's left -- nobody presses play by accident and bounces. */
  .px-vid .len{position:absolute;right:12px;bottom:12px;padding:5px 10px;border-radius:8px;
    background:rgba(4,18,42,.82);backdrop-filter:blur(6px);
    font-size:.68rem;font-weight:700;letter-spacing:.06em;color:#B1BFD7}
  .px-vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0}

  #px-voices{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(20px,2.8vw,38px);
    padding-top:32px;border-top:1px solid rgba(241,236,225,.1)}
  .px-voice{margin:0;display:flex;flex-direction:column}
  .px-voice blockquote{margin:0 0 18px;font-family:'Cormorant Garamond',Georgia,serif;
    font-style:italic;font-size:clamp(18px,1.6vw,22px);line-height:1.4;color:#F1ECE1;flex:1}
  @media(max-width:820px){#px-voices{grid-template-columns:1fr;gap:28px}
    .px-voice blockquote{flex:none}}

  /* fires only when all three panes are in. he ends on the promise. */
  #px-vv-cta{max-height:0;opacity:0;overflow:hidden;transition:max-height .7s ease,opacity .6s ease,margin .6s ease;margin-top:0}
  #px-vv-cta.show{max-height:240px;opacity:1;margin-top:22px}

  @media(prefers-reduced-motion:reduce){
    .px-line > span{transform:none!important}
    .px-fade{opacity:1!important;transform:none!important}
    .px-in .px-fog{transform:translateX(104%)!important}
  }`;

  var HTML = `<div id="px-root">

<!-- ══════════════ 01 · THE HERO ══════════════
     NO CAPTION CARD. It was competing with the hook (third-heaviest thing
     on screen, right next to the CTA) -- and it spoiled the best moment on
     the page.

     The hero image is a MIRROR. A man behind glass, unreachable. That's HIM.
     The second you caption it "Daniel Lawson", it stops being a mirror and
     becomes a portrait of the coach.

     And section 06 is built to land like a trapdoor:
       "I was the man behind the glass. I sat in there seven years."
     If he's already read that in the hero, it arrives as a reminder instead
     of a reveal. Hold it. -->
<section id="px-hero">
  <canvas id="px-glass"></canvas>
  <div id="px-fallback"><div class="fb-img" id="px-fb-img"></div><div class="fb-glass"></div></div>
  <div id="px-hero-veil"></div>

  <div id="px-hero-copy">
    <div class="inner">
      <p class="px-hand px-fade" style="font-size:1.7rem;color:#E8C65F;margin-bottom:14px">it takes courage to admit you want love</p>

      <!-- THE HOOK.
           v6 said "No one gets close to you. And you can't work out why."
           That is a DIAGNOSIS. He nods and scrolls.

           Daniel's actual hook form, from every post that has ever worked
           for him, is a provocative flat statement that sounds wrong until
           it doesn't:
             "Fixing her feelings is selfish."
             "Productivity is my favourite place to hide."
             "Your checklist is keeping you alone."
             "The loudest guy is the most insecure."

           So the hero is the whole thesis, weaponised. He can't argue with
           it and he can't ignore it, because it flatters him and cuts him
           in the same breath. -->
      <h1 class="px-serif" style="font-size:clamp(34px,5.4vw,72px);line-height:1.1;color:#F1ECE1;margin-bottom:26px">
        <span class="px-line"><span>What made you successful</span></span>
        <span class="px-line"><span style="font-style:italic;color:#E8C65F">is what's keeping you</span></span>
        <span class="px-line"><span style="font-style:italic;color:#E8C65F">alone.</span></span>
      </h1>
      <!-- 63 words was too heavy for a hero. But this line stays, tightened:
           the headline makes a CLAIM (your strengths are the problem), and an
           unsupported claim from a stranger gets dismissed. This is the proof,
           and it lands in a second because it's a list.

           The single/married line is a QUALIFIER, not a hook. It exists only
           so a married man doesn't bounce at the word "alone". Nine words. -->
      <p class="px-fade" style="font-size:clamp(16px,1.35vw,20px);line-height:1.8;max-width:48ch;margin-bottom:12px;color:#C4CEE0">
        The discipline. The standards. The self&#8209;sufficiency. They built the life. Now everybody's looking at you through it.
      </p>
      <!-- THE SOLUTION. One line, and it does three jobs at once.

           1. It answers the headline. The hook makes a brutal claim about
              him ("your strengths are the problem") and then leaves him
              holding it. Nobody stays on a page that only accuses.
           2. It carries the WHOLE promise: keep every bit of it, we're just
              making you reachable. That is the offer, in nine words.
           3. It makes the CURSOR WIPE legible without a single line of UI.
              No prompt, no ring, no "drag to clean" tutorial -- the copy
              says "we clean the glass," the hero IS glass, and anyone who
              moves the mouse discovers what that sentence means. The
              mechanic explains itself, and nothing is gated behind it for
              the people who never touch it.

           GOLD on "clean the glass" -- gold is Daniel's voice. This is him
           making the promise. Coral would be wrong here: coral is the
           reader's colour, reserved for controls, and every coral word in
           prose devalues the coral BUTTON sitting right underneath. -->
      <p class="px-fade" style="font-size:clamp(16px,1.35vw,20px);line-height:1.75;max-width:48ch;margin-bottom:32px;color:#F1ECE1;font-weight:500">
        We <strong style="color:#E8C65F;font-weight:600">clean the glass</strong>. You keep every bit of what you built.
      </p>

      <div class="px-fade" style="display:flex;gap:14px;flex-wrap:wrap">
        <a class="px-btn" href="https://www.parallaxxtransformations.com/reconnect">Find your pattern <span>→</span></a>
        <a class="px-ghost" href="#px-mirror">Is this me? <span>↓</span></a>
      </div>

      <!-- The single/married qualifier is NOT a beat -- it's a footnote. It
           exists for one reason: so a married man doesn't bounce off the word
           "alone" in the headline. Sitting in the main stack it read like a
           third argument and cost the hero a whole line of weight. Under the
           buttons it does the same job at a fraction of the price. -->
      <p class="px-fade" style="font-size:.8rem;line-height:1.6;color:#7C89A3;margin-top:18px;max-width:48ch">
        Single or married. Makes less difference than you'd think.
      </p>
    </div>
  </div>

</section>

<!-- ══════════════ 02 · THE MIRROR — fogged confessions ══════════════ -->
<section id="px-mirror" class="px-sec" style="background:#F1ECE1;color:#3A3630">
  <div class="px-wrap">
    <div id="px-mirror-grid">

      <!-- LEFT: the thread -->
      <div class="px-fade">
        <div class="px-phone">
          <div class="px-notch"></div>
          <div class="px-screen">
          <div class="px-thread-hd">
            <div class="px-av">YOU</div>
            <div>
              <div style="font-size:12px;font-weight:700;color:#1E2A3D">You</div>
              <div style="font-size:9.5px;color:#A79C8C">2:14 am · same as every night</div>
            </div>
          </div>

          <div id="px-window">
          <div id="px-tape">
          <div class="px-in"><div><div class="px-bub">I don't know how to let anyone all the way in.</div><div class="px-fog"></div></div></div>
          <div class="px-out"><div><div class="b">You're just selective.</div></div></div>

          <div class="px-in"><div><div class="px-bub">Everyone gets the curated version of me.</div><div class="px-fog"></div></div></div>
          <div class="px-out"><div><div class="b">That's called being professional.</div></div></div>

          <div class="px-in"><div><div class="px-bub">I pull away right when it starts to matter.</div><div class="px-fog"></div></div></div>
          <div class="px-out"><div><div class="b">You have standards.</div></div></div>

          <div class="px-in"><div><div class="px-bub">I'm lying next to someone and I still feel alone in it.</div><div class="px-fog"></div></div></div>
          <div class="px-out"><div><div class="b">Everyone feels like that sometimes.</div></div></div>

          <div class="px-in"><div><div class="px-bub">I can be alone and fine. But it's lonely.</div><div class="px-fog"></div></div></div>
          <div class="px-out"><div><div class="b">You're fine. You're busy.</div></div></div>

          <div class="px-in last"><div><div class="px-bub">Maybe this just isn't for people like me.</div><div class="px-fog"></div></div></div>
          <!-- THE SILENCE. There is no answer to this one, so he never gave one. -->
          <div class="px-out px-none"><div><div class="b">no reply</div><div class="px-meta" style="color:#C6BBAA">you never had one</div></div></div>
          </div>
          </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: the explanation.
           The portrait that lived here was doing nothing -- same man, same
           glass as the hero, so it just repeated a picture he'd already sat
           with, and competed with the phone.

           The explanation belongs here instead. It lands while he's still
           reading the thread, and it saves the section a full-width block
           of ~500px underneath. -->
      <div id="px-sticky">
        <p class="px-label px-fade" style="color:#A08A5E;margin-bottom:14px">01 — The mirror</p>
        <h2 class="px-serif" style="font-size:clamp(25px,3vw,40px);line-height:1.15;color:#1E2A3D;margin-bottom:16px">
          The conversation you keep <span style="font-style:italic">having with yourself.</span>
        </h2>
        <p class="px-fade" style="font-size:1.06rem;line-height:1.7;color:#5E5850;margin-bottom:10px">
          He messages you at 2am. You've got an answer for everything he says.
        </p>
        <p class="px-fade" style="font-size:1.06rem;line-height:1.7;color:#8A8073;margin-bottom:26px">
          Every one of them, you talked him out of.
        </p>

        <div class="px-fade" style="display:flex;align-items:center;gap:16px;margin-bottom:20px">
          <span style="height:1px;flex:1;background:linear-gradient(90deg,rgba(160,138,94,.5),transparent)"></span>
          <span class="px-hand" style="font-size:1.4rem;color:#A08A5E;white-space:nowrap">so where did they come from?</span>
          <span style="height:1px;flex:1;background:linear-gradient(90deg,transparent,rgba(160,138,94,.5))"></span>
        </div>

        <p class="px-fade" style="font-size:1.02rem;line-height:1.72;color:#5E5850;margin-bottom:14px">
          <strong style="color:#1E2A3D">Every one of them came from somewhere.</strong> A younger version of you worked out that opening up cost something, and found a way to stay safe. Smart kid.
        </p>
        <p class="px-fade" style="font-size:1.02rem;line-height:1.72;color:#5E5850;margin-bottom:14px">
          And it worked. That's what gets us — it worked so well we built whole lives on it.
        </p>
        <p class="px-fade" style="font-size:1.02rem;line-height:1.72;color:#5E5850">
          Now the same film that kept the pain out is keeping <strong style="color:#1E2A3D">them</strong> out too. Whether they're still out there, or right beside you. <strong style="color:#1E2A3D">No judgment.</strong> Most of us do this until we know better.
        </p>
      </div>
    </div>

    <!-- THE BRIDGE: from his head into his body.
         He is analytical and probably numb. Go straight at feeling and he
         calls it woo. Stay analytical and nothing moves.
         So: something he can OBSERVE (the pause), located in the BODY
         (the chest), and only then NAMED (loneliness). Every rung is
         verifiable. He can check the first one right now. -->
    <div class="px-fade" style="max-width:68ch;margin:62px auto 0;padding:34px 36px;background:#12233F;border-radius:20px">
      <p class="px-serif" style="font-size:clamp(20px,2.2vw,29px);line-height:1.45;color:#F1ECE1;font-style:italic;margin-bottom:18px">
        You know the half&#8209;second before you answer "how are you"?
      </p>
      <p style="font-size:1.02rem;line-height:1.75;color:#B1BFD7;margin-bottom:16px">
        That tiny gap where you decide how much to give. It's so quick now you don't notice it. But it's there, and it's in your body — a small tightening, up behind the breastbone, and then it's gone and you've said "yeah, good."
      </p>
      <p style="font-size:1.02rem;line-height:1.75;color:#B1BFD7;margin-bottom:16px">
        That gap is a muscle. You've been holding it for twenty years, and the holding stopped feeling like anything at all.
      </p>
      <p style="font-size:1.02rem;line-height:1.75;color:#E8C65F">
        And if reading this left you flat — <strong>that's the muscle. You're feeling it right now.</strong>
      </p>
    </div>
  </div>
</section>

<!-- ══════════════ 03 · THE REFRAME - the divider IS the section ══════════════
     "You can't see the dirt from in there" used to be a sentence, then a
     demo in a box. Now it's the ground he's standing on: the copy for each
     side lives ON that side of the glass. Drag it and the argument moves.
     ═══════════════════════════════════════════════════════════════ -->
<section id="px-reframe">
  <canvas id="px-split"></canvas>
  <div id="px-rf-veil"></div>
  <div id="px-handle" style="left:50%"></div>

  <div id="px-rf-copy">
    <div class="px-wrap" style="display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,6vw,90px);align-items:center" id="px-rf-grid">

      <!-- HER SIDE -->
      <div class="px-rf-side px-fade">
        <span class="px-rf-tag" style="background:#E8C65F;color:#061938">From where they stand</span>
        <h3 class="px-serif" style="font-size:clamp(24px,3vw,40px);line-height:1.2;color:#F1ECE1;margin-bottom:16px">Flawless.</h3>
        <p style="font-size:1rem;line-height:1.72;color:#C4CEE0;pointer-events:auto">
          Capable. Composed. The one everyone counts on. This is what they get, every time, for years. <strong style="color:#E8C65F">It's a beautiful picture. It's also the only thing they've ever been allowed to see.</strong>
        </p>
      </div>

      <!-- HIS SIDE -->
      <div class="px-rf-side px-fade" style="margin-left:auto;text-align:right">
        <span class="px-rf-tag" style="background:#FF501F;color:#fff">From where you stand</span>
        <h3 class="px-serif" style="font-size:clamp(24px,3vw,40px);line-height:1.2;color:#F1ECE1;margin-bottom:16px">And this is what it feels like.</h3>
        <p style="font-size:1rem;line-height:1.72;color:#C4CEE0;pointer-events:auto">
          Everyone at arm's length. Someone's face right in front of you and you're somewhere behind your own eyes, watching it happen. Everything works. You just can't get out, and nobody can get in.
        </p>
      </div>
    </div>

    <div class="px-wrap" style="text-align:center;margin-top:clamp(18px,2.5vw,32px)">
      <p class="px-hand" style="font-size:1.6rem;color:#FF501F">same man. drag it across.</p>
    </div>
  </div>
</section>

<!-- The reframe argument, in normal prose, straight after he's felt it. -->
<section class="px-sec" style="background:#0A1D3C;padding-top:clamp(34px,4vw,52px)">
  <div class="px-wrap">
    <div class="px-head" style="margin:0 auto 40px;text-align:center">
      <p class="px-label px-fade" style="margin-bottom:20px">02 — Why it keeps happening</p>
      <h2 class="px-serif" style="font-size:clamp(26px,3.6vw,46px);line-height:1.22;color:#F1ECE1">
        <span class="px-line"><span>You don't get the relationship you want.</span></span>
        <span class="px-line"><span style="font-style:italic;color:#E8C65F">You get the one that matches who you are.</span></span>
      </h2>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,56px)" id="px-reframe-cols">
      <div>
        <p class="px-fade" style="font-size:1.05rem;line-height:1.75;color:#C4CEE0;margin-bottom:18px">
          So it was never the apps, right? Never the city, never the timing. And if you're already with someone — it was never them either. We keep changing what's out there and walking the same person into it.
        </p>
        <p class="px-fade" style="font-size:1.05rem;line-height:1.75;color:#C4CEE0">
          Look at that left-hand side again. It's immaculate. That's the trap. <strong style="color:#E8C65F">The polish is the film.</strong> The discipline, the standards, the self-sufficiency, the composure — every good thing about you. Flawless, and completely opaque.
        </p>
      </div>
      <div>
        <p class="px-fade" style="font-size:1.05rem;line-height:1.75;color:#C4CEE0;margin-bottom:18px">
          They keep meeting the impressive version, and it's standing in the doorway. <strong style="color:#E8C65F">You can't fix what you can't see. And you can't see it from in there.</strong> That's why ten years of books and podcasts changed nothing. It takes somebody standing on the outside.
        </p>
        <blockquote class="px-fade" style="border-left:2px solid #E8C65F;padding-left:24px;margin-top:18px">
          <p class="px-serif" style="font-size:1.45rem;line-height:1.45;color:#E8C65F;font-style:italic">Keep every bit of it. The discipline, the standards, the drive. We're just making you reachable — and you'll know the day it lands, because someone asks how you are and the answer comes out unedited.</p>
          <cite class="px-hand" style="display:block;font-size:1.3rem;color:#7C89A3;margin-top:12px;font-style:normal">— Daniel</cite>
        </blockquote>
      </div>
    </div>
  </div>
</section>

<!-- ══════════════ 04 · THE FIVE PANES - the lock, not the reveal ══════════════ -->
<section class="px-sec" style="background:#04122A">
  <div class="px-wrap">
    <div class="px-head" style="text-align:center;margin:0 auto 30px">
      <p class="px-hand px-fade" style="font-size:1.75rem;color:#E8C65F;margin-bottom:14px">we all keep people out differently</p>
      <h2 class="px-serif" style="font-size:clamp(30px,4.4vw,56px);line-height:1.15;color:#F1ECE1;margin-bottom:22px">
        <span class="px-line"><span>Five kinds of film.</span></span>
        <span class="px-line"><span style="font-style:italic;color:#E8C65F">One of them is yours.</span></span>
      </h2>
      <p class="px-fade" style="font-size:1.05rem;line-height:1.75;color:#C4CEE0;margin-bottom:14px">
        Each of us does it differently. <strong style="color:#E8C65F">And it's hard to scrub off something you're still proud of.</strong>
      </p>
    </div>

    <!-- Add a clip to a pane by giving it data-clip (and, ideally, data-poster).
         Panes with no data-clip simply stay as glass -- no broken video, no
         empty box, no "watch" cue. The section degrades to exactly what it
         was. So the four un-shot ones can sit here safely until the footage
         lands. -->
    <div class="px-fade" id="px-panes">
      <div class="px-pane" data-film="fortress"
           data-clip="https://video.wixstatic.com/video/111174_495d92c709a74ae199756df31216a61e/480p/mp4/file.mp4">
        <div class="n">01</div>
        <h3>The Freedom Fortress</h3>
        <p>Closeness starts to feel like being trapped.</p>
      </div>

      <div class="px-pane" data-film="defender"
           data-clip="https://video.wixstatic.com/video/111174_863af1d4805a4c24ad33cb35ff088881/480p/mp4/file.mp4">
        <div class="n">02</div>
        <h3>The Intellectual Defender</h3>
        <p>You know the story of how you feel. Not the feeling.</p>
      </div>

      <div class="px-pane" data-film="idealist"
           data-clip="https://video.wixstatic.com/video/111174_0c316e5ec9a44931a1f94fe8f9bac6a6/480p/mp4/file.mp4">
        <div class="n">03</div>
        <h3>The Idealist</h3>
        <p>You only fully show up when it feels perfect.</p>
      </div>
      <div class="px-pane" data-film="performer"
           data-clip="https://video.wixstatic.com/video/111174_2dd20e0c35d3467e8957b2e57cd6d9d9/480p/mp4/file.mp4">
        <div class="n">04</div>
        <h3>The Performer</h3>
        <p>They love the energy. Nobody has ever met the truth.</p>
      </div>
      <div class="px-pane" data-film="romantic"
           data-clip="https://video.wixstatic.com/video/111174_469a5c83d5ae49ddb30780eb2ca3a85d/480p/mp4/file.mp4">
        <div class="n">05</div>
        <h3>The Over-Controlled Romantic</h3>
        <p>You live half a step behind your own impulse.</p>
      </div>
    </div>

    <!-- THE GATE. He can rub at it from out here. He can't get through it. -->
    <div style="max-width:68ch;margin:28px auto 0;text-align:center">
      <p class="px-fade" style="font-size:1.08rem;line-height:1.75;color:#C4CEE0;margin-bottom:14px">
        One of those made you shift in your seat.
      </p>
      <p class="px-fade" style="font-size:1.08rem;line-height:1.75;color:#C4CEE0;margin-bottom:30px">
        That's as far as I can take you from out here. Two minutes and I'll tell you which one is yours — where it came from, what it's protecting, and what it's cost you.
      </p>
      <a class="px-btn px-fade" href="https://www.parallaxxtransformations.com/reconnect">Find out which one is yours <span>→</span></a>
      <p class="px-fade" style="font-size:.84rem;color:#5E6B85;margin-top:14px">2 minutes. No email wall on the result.</p>
    </div>

  </div>
</section>

<!-- ══════════════ THE FORK — same glass, different room ══════════════
     Pulled out of section 04 and given its own room, on CREAM.

     Two reasons, and the second one is the real one:
       1. It was a THIRD idea stapled to the end of a section that already
          had two (the five films, and the quiz gate). It reads as an
          afterthought down there. It's the audience split -- it deserves air.
       2. It buys the CONTRAST. The section below it has to hold a piece of
          glass going from filthy to clear on a photograph. That needs to sit
          on NAVY -- dark room, lit window. On cream the dirty state has
          nothing to be dark against and the reveal barely registers.

     So the page now alternates properly: navy panes -> cream fork ->
     navy system -> cream Daniel. ══════════════════════════════════ -->
<section class="px-sec" style="background:#F1ECE1;color:#3A3630">
  <div class="px-wrap">
    <p class="px-hand px-fade" style="text-align:center;font-size:1.6rem;color:#A08A5E;margin-bottom:26px">same glass. different room.</p>
    <div class="px-doors">
      <a class="px-door on-cream px-fade" href="https://www.parallaxxtransformations.com/the-reconnected-man">
        <div class="eyebrow">For men</div>
        <h4>The Reconnected Man</h4>
        <p>You learned that needing someone was a risk. So you built a life that doesn't require anyone — and now nobody can get in.</p>
        <span class="go">Step into the brotherhood →</span>
      </a>
      <a class="px-door on-cream px-fade" href="https://www.parallaxxtransformations.com/the-reconnected-woman">
        <div class="eyebrow">For women</div>
        <h4>The Reconnected Woman</h4>
        <p>You've competed with men, led men, carried men. You've held it together for everyone. And nobody has ever held you.</p>
        <span class="go">Put it down →</span>
      </a>
    </div>
  </div>
</section>

<!-- ══════════════ 05 · THE SYSTEM — three panes of glass ══════════════
     Tightened to fit a 14" laptop in one screen. Three clicks only happen
     if the stage, the pills and the card are all visible at once.
     ON NAVY NOW, not cream. This section's whole job is a pane of glass
     going from filthy to clear over a photograph of two people. That needs
     a DARK ROOM and a LIT WINDOW. On cream the dirty state had nothing to
     be dark against, and the clean state had nowhere to arrive.
     ═══════════════════════════════════════════════════════════════ -->
<section class="px-sec" style="background:#04122A;padding-top:clamp(38px,4.4vw,58px);padding-bottom:clamp(38px,4.4vw,58px)">
  <div class="px-wrap">
    <div class="px-head" style="text-align:center;margin:0 auto 22px">
      <p class="px-label px-fade" style="margin-bottom:12px">03 — How the work actually works</p>
      <h2 class="px-serif" style="font-size:clamp(27px,3.4vw,42px);line-height:1.18;color:#F1ECE1;margin-bottom:14px">
        <span class="px-line"><span>The Relational Connection System™</span></span>
      </h2>
      <p class="px-fade" style="font-size:1rem;line-height:1.65;color:#C4CEE0;margin-bottom:0;max-width:60ch;margin-left:auto;margin-right:auto">
        Three panes between you and the people you love. Fit all three and they can reach you. <strong style="color:#E8C65F">Miss one and the glass stays dirty in a specific, predictable way</strong> — which is why the same thing keeps happening.
      </p>
    </div>

    <!-- TWO ROWS, not one column-of-stuff beside a card.

         The card has to hug its content AND sit centred against the IMAGE.
         Those two things fight each other if the pills live in the same grid
         cell as the stage: the left column becomes stage + pills + caption
         (~545px), the row grows to match, and a centred card is then centred
         against THAT -- which drops it ~35px below the middle of the picture.
         Stretch the card to fill instead and you get a huge white box with
         the words marooned in the middle of it.

         So: the STAGE and the CARD share row 1. The pills and the caption
         drop to row 2, under the stage. Row 1's height is now exactly the
         height of the image, the card centres against it, and the card is
         only ever as tall as its own words. -->
    <div id="px-vv-grid">
      <div id="px-vv-stage" class="px-fade">
        <canvas id="px-vv-c"></canvas>
        <div id="px-vv-overlay">
          <div id="px-vv-title" class="px-serif" style="font-style:italic;font-size:clamp(17px,1.8vw,25px);color:#F1ECE1;line-height:1.35"></div>
        </div>
      </div>

      <div class="px-card px-fade" id="px-vv-card">
        <div id="px-vv-label" style="font-size:.66rem;letter-spacing:.2em;text-transform:uppercase;font-weight:800;color:#A08A5E;margin-bottom:14px"></div>
        <div id="px-vv-head" class="px-serif" style="font-size:1.6rem;line-height:1.3;color:#1E2A3D;margin-bottom:16px"></div>
        <div id="px-vv-body" style="font-size:.94rem;line-height:1.72;color:#5E5850"></div>

        <div id="px-vv-cta">
          <div style="border-top:1px solid #E5DFD3;padding-top:20px">
            <p class="px-hand" style="font-size:1.5rem;color:#A08A5E;margin-bottom:10px">that's the whole model</p>
            <p style="font-size:.92rem;line-height:1.8;color:#5E5850;margin-bottom:18px">
              Three clicks. It takes a bit longer in a life. Let's find out which one you're missing.
            </p>
            <a class="px-btn" style="font-size:.9rem;padding:.9em 1.7em" href="https://www.parallaxxtransformations.com/contact-daniel-lawson">Start with a conversation <span>&#8594;</span></a>
          </div>
        </div>
      </div>

      <!-- ROW 2, under the stage. Out of the card's way. -->
      <div id="px-vv-controls">
        <div style="display:flex;gap:9px" class="px-fade">
          <button class="px-pill" data-k="vision">Vision</button>
          <button class="px-pill" data-k="values">Values</button>
          <button class="px-pill" data-k="velocity">Velocity</button>
        </div>
        <p class="px-fade" style="font-size:.8rem;color:#8E9BB2;margin-top:10px">Click a pillar to fit that pane. Three, and they can see you.</p>
      </div>
    </div>

    <p class="px-hand px-fade" style="text-align:center;font-size:1.5rem;color:#E8C65F;margin-top:20px">so it was never about finding "the one" - it's about connecting back with yourself</p>
  </div>
</section>

<!-- ══════════════ 06 · DANIEL — the only clear glass on the site ══════════════ -->
<section class="px-sec" style="background:#F7F3EA;color:#3A3630">
  <div class="px-wrap" id="px-daniel" style="display:grid;grid-template-columns:.82fr 1.18fr;gap:clamp(36px,5vw,76px);align-items:center">

    <div>
      <!-- Seated. A table. A cup. Looking straight at the person reading.
           The picture and the button under it say the same thing: start with
           a conversation.

           It is NOT "the only clear image on the site" any more -- section 05
           took that when its glass came off two people laughing. That's fine.
           This one stopped being the REVEAL and became the INVITATION, which
           is a better job for it.

           Barely graded on purpose: blacks floored, 8% saturation off so the
           turquoise doesn't shout at the cream. Nothing else. It is captioned
           "no film, no filter, no glass" and grading it into a mood would be
           the exact hypocrisy this page spends 2000 words attacking. -->
      <img class="px-fade" alt="Daniel Lawson" loading="lazy"
           style="width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:20px;display:block;
                  box-shadow:0 40px 80px -50px rgba(30,42,61,.6), 0 0 0 1px rgba(160,138,94,.18)"
           src="https://static.wixstatic.com/media/111174_5104ff2da2e0456a80264bc62d635fa4~mv2.jpg/v1/fill/w_1200,h_1500,al_c,q_90,enc_auto/daniel-conversation.jpg">
      <p class="px-fade" style="font-size:.76rem;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:#C0AE92;margin-top:14px;text-align:center">No film. No filter. No glass.</p>
    </div>

    <div>
      <p class="px-hand px-fade" style="font-size:1.75rem;color:#A08A5E;margin-bottom:16px">now — me</p>
      <h2 class="px-serif" style="font-size:clamp(28px,3.7vw,48px);line-height:1.22;color:#1E2A3D;margin-bottom:30px">
        <span class="px-line"><span>I was the man behind the glass.</span></span>
        <span class="px-line"><span style="font-style:italic;color:#8A5A47">I sat in there seven years.</span></span>
      </h2>
      <p class="px-fade" style="font-size:1.03rem;line-height:1.78;color:#5E5850;margin-bottom:18px;max-width:66ch">
        A woman I loved told me the way I held back the truth — never lying, just never quite telling her — was still dishonesty. She was right. And it showed me something I couldn't outrun: I wasn't the man I needed to be for the relationship I wanted, and I had no idea how to become him.
      </p>
      <p class="px-fade" style="font-size:1.03rem;line-height:1.78;color:#5E5850;margin-bottom:18px;max-width:66ch">
        So I waited. Seven years. Told myself someone would show up and it'd all click. Nobody was coming. The problem was never out there.
      </p>
      <p class="px-fade" style="font-size:1.03rem;line-height:1.78;color:#5E5850;margin-bottom:22px;max-width:66ch">
        What shifted it was admitting the thing underneath: <strong style="color:#1E2A3D">I was lonely, and it was mine to deal with.</strong> Most of us don't wreck intimacy by cheating or lying. We do it by hiding, and hoping it sorts itself out. It doesn't.
      </p>
      <p class="px-fade" style="font-size:1.03rem;line-height:1.78;color:#5E5850;margin-bottom:34px;max-width:66ch">
        The people I sit with now — some are single, some are lying next to someone they love and can't reach. Men and women. It's the same glass every time.
      </p>
      <p class="px-fade" style="font-size:1.03rem;line-height:1.78;color:#5E5850;margin-bottom:34px;max-width:66ch">
        I'll walk you out the way I came out. I know every wrong turn on that road — I took all of them.
      </p>
      <div class="px-fade" style="display:flex;gap:14px;flex-wrap:wrap;align-items:center">
        <a class="px-btn" href="https://www.parallaxxtransformations.com/contact-daniel-lawson">Start with a conversation <span>→</span></a>
        <a class="px-ghost" style="color:#8A5A47;border-color:rgba(255,80,31,.4)" href="https://www.parallaxxtransformations.com/about-daniel-lawson">The full story <span>→</span></a>
      </div>
      <p class="px-hand px-fade" style="font-size:2.1rem;color:#C0AE92;margin-top:34px">Daniel</p>
      <!-- ▸ Replace with a scan of Daniel's ACTUAL signature. Not a font. -->
    </div>
  </div>
</section>

<!-- ══════════════ 07 · PROOF ══════════════
     Rebuilt around what was already sitting on the Testimonials page, flattened
     into PNGs where Google cannot read a word of it and a phone cannot reflow it.
     Four real clients, real names, real countries, real faces.

     THE FIND: they describe it in the language of NOT BEING ABLE TO SEE.
       "Daniel helped me see what I couldn't see myself."   -- Tobias
       "I couldn't see where the actual problem was coming from." -- Gena
       "The emotional burden blinded me."                    -- Silja
     Nobody coached them into that. The glass is not a metaphor Daniel invented
     to sell with -- it is how the people he has actually helped describe the
     thing. So the section leads with THAT, and the strip of fragments underneath
     proves the whole page in three lines that aren't his.

     TOBIAS CARRIES IT, not the old "chameleon / buttons to push" quote. That one
     complimented the COACH. This one validates the MECHANISM -- it is section
     03's argument ("you can't see it from in there") in a client's own mouth.

     BRANDON is the second, because he is the highest-stakes story on the site --
     addiction, PTSD, "a path to death" -- he is a MAN, and he is in dress
     uniform, which makes him instantly, verifiably real. Nobody looks at that
     and thinks stock photo.

     Faces are cropped out of the source PNGs with Wix's own crop transform, so
     there is no re-upload and no shoot. ══════════════════════════════════ -->
<section class="px-sec" style="background:#0A1D3C">
  <div class="px-wrap" style="max-width:1080px">
    <p class="px-label px-fade" style="text-align:center;margin-bottom:14px">04 — People who did it</p>
    <h2 class="px-serif px-fade" style="text-align:center;font-size:clamp(25px,3.2vw,40px);line-height:1.2;color:#F1ECE1;margin:0 auto 34px;max-width:20ch">
      They all say the <span style="font-style:italic;color:#E8C65F">same thing.</span>
    </h2>

    <!-- ▸▸ THE LEAD IS A VIDEO, and it is the best asset on the entire site.
         "MY WIFE COULDN'T REACH ME." A client, on camera, saying the exact
         sentence this page is built on. The hero says people are looking at
         you through it; section 05 says fit all three and THEY CAN REACH YOU;
         the footer says the people who love you just stop trying. And here is
         a man who has never read any of that using the same word.

         A written quote can be written by anyone. A face saying it cannot. -->
    <!-- ONE VIDEO. NOT FIVE.

         v1 put all five long-form interviews here and that was wrong twice.

         1. THEY ARE 12-15 MINUTES. Nobody three sections above a CTA commits
            to thirteen minutes. And the ones who click LEAVE FOR YOUTUBE and
            do not come back. That isn't proof, it's a leak with a play button
            on it.
         2. It spent the entire library. "1 of 5 client stories" is only a
            promise if the other four are somewhere else. Showing all five
            underneath it made the line a lie and left the Testimonials page
            with nothing to be for.

         So the home page takes the sharpest one and says the number out loud.
         The other four are the reason to click through.

         ▸ NEXT: cut a 45-60 second highlight from this interview and host it
           on Wix like the archetype clips. THAT is the right home-page asset:
           a taste, in the page, that costs nobody thirteen minutes. Swap the
           facade's data-yt for a local <video> when it exists. -->
    <div class="px-fade" style="max-width:760px;margin:0 auto 6px">
      <button class="px-vid"
              data-mp4="https://video.wixstatic.com/video/111174_96f86443b9e244999b01cd1e8172bd81/720p/mp4/file.mp4"
              aria-label="Play: a client on why he kept it all internally">
        <img alt="" loading="lazy"
             src="https://static.wixstatic.com/media/111174_e25884f8c6bb492c9dea0f85b614c441~mv2.jpg/v1/fill/w_1280,h_720,al_c,q_90,enc_auto/proof-poster.jpg">
        <span class="play" aria-hidden="true"></span>
        <span class="len">49 sec</span>
      </button>
      <!-- THE QUOTE HAS TO BE WORDS HE ACTUALLY SAYS.
           v1 ran "My wife couldn't reach me" -- which is the YouTube thumbnail,
           i.e. Daniel's editorial framing. It is nowhere in the transcript. In
           quotation marks, attributed as speech, on the one section of the page
           whose entire job is being verifiably true, that is a small lie.
           This is verbatim, and it's stronger anyway: it's the HEADLINE, said
           back to the page by a stranger who has never read it. -->
      <p class="px-serif" style="text-align:center;font-size:clamp(23px,2.8vw,38px);line-height:1.35;color:#F1ECE1;font-style:italic;margin:26px auto 12px;max-width:26ch">
        “I kept it all internally. <span style="color:#E8C65F;font-style:normal;font-weight:600">I didn't realise that was what was causing the problems.</span>”
      </p>
      <!-- The clip is 49 seconds of the PROBLEM. It does not contain the turn,
           because this interview's turn is quiet and internal and takes ten more
           minutes to arrive. Rather than splice a Frankenstein arc, name the gap
           and let it BE the click. Nothing is implied that he doesn't claim. -->
      <p style="text-align:center;font-size:.92rem;color:#B1BFD7;margin:0 0 8px">
        That's the problem. <a href="https://www.parallaxxtransformations.com/testimonials-daniel-lawson" style="color:#E8C65F;font-weight:600;text-decoration:none;border-bottom:1px solid rgba(232,198,95,.4)">What changed is in the full conversation →</a>
      </p>
      <p style="text-align:center;font-size:.8rem;color:#5E6B85;margin:0">One of five. All of them are on the testimonials page.</p>
    </div>

    <p class="px-hand px-fade" style="text-align:center;font-size:1.45rem;color:#E8C65F;margin:26px 0 8px">and the ones who wrote it down said the same thing</p>

    <!-- THE OTHER THREE. Same sentence, three more mouths.
         Brandon's UNIFORM was doing his credibility work when the photo was
         large. At 64px it can't -- so the WORDS do it instead: "US Navy". That
         is more honest anyway. The credential is the fact, not the picture. -->
    <div class="px-fade" id="px-voices">
      <figure class="px-voice">
        <blockquote>“Daniel helped me see what I couldn't see myself.”</blockquote>
        <div class="px-byline">
          <img class="px-face" alt="Tobias M, Sweden" style="object-position:center 18%"
               src="https://static.wixstatic.com/media/111174_392b733e816548dcbfadab2fe214e05c~mv2.png/v1/crop/x_84,y_490,w_664,h_442,q_90,enc_auto/file.png">
          <span class="who">Tobias M · Sweden<span>Founder · hit a plateau</span></span>
        </div>
      </figure>
      <figure class="px-voice">
        <blockquote>“I couldn't see where the actual problem was coming from.”</blockquote>
        <div class="px-byline">
          <img class="px-face" alt="Gena K, Bulgaria" style="object-position:72% 26%"
               src="https://static.wixstatic.com/media/111174_40fcf9f37e654196b42fac9dc18e2761~mv2.png/v1/crop/x_72,y_46,w_666,h_474,q_90,enc_auto/file.png">
          <span class="who">Gena K · Bulgaria<span>Self-sabotage · emotional overload</span></span>
        </div>
      </figure>
      <figure class="px-voice">
        <blockquote>“I was down a path to death. I didn't love myself. Now I feel reborn.”</blockquote>
        <div class="px-byline">
          <img class="px-face" alt="Brandon L, USA" style="object-position:center 22%"
               src="https://static.wixstatic.com/media/111174_3db56c0e87c84875a9f6d059a2a768eb~mv2.png/v1/crop/x_60,y_0,w_692,h_470,q_90,enc_auto/file.png">
          <span class="who">Brandon L · USA<span>US Navy · addiction, PTSD</span></span>
        </div>
      </figure>
    </div>

    <!-- THE POINT OF THE WHOLE SECTION, and it isn't Daniel's line -- it's
         theirs. Couldn't reach. Couldn't see. Blinded. Nobody fed them that
         vocabulary. The glass isn't a metaphor he invented to sell with; it's
         how the people he's actually helped describe the thing. -->
    <p class="px-hand px-fade" style="text-align:center;font-size:1.5rem;color:#E8C65F;margin-top:30px">couldn't reach me. couldn't see it. blinded. — nobody gave them those words.</p>

    <p class="px-fade" style="text-align:center;margin-top:22px">
      <a href="https://www.parallaxxtransformations.com/testimonials-daniel-lawson" style="font-size:.92rem;font-weight:600;color:#E8C65F;text-decoration:none;border-bottom:1px solid rgba(232,198,95,.4);padding-bottom:2px">Read them in full →</a>
    </p>
  </div>
</section>

<!-- ══════════════ 08 · CREDENTIALS — demoted ══════════════ -->
<section style="background:#061938;border-top:1px solid rgba(241,236,225,.07);padding:54px clamp(20px,4vw,52px)">
  <div class="px-wrap">
    <p style="text-align:center;font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;color:#46536E;font-weight:700;margin-bottom:26px">Seen in · Credentialled by</p>
    <div style="display:flex;align-items:center;justify-content:center;gap:clamp(14px,3vw,38px);flex-wrap:wrap;font-size:.85rem;color:#5E6B85;font-weight:600">
      <span>ABC News</span><span style="color:#2A3550">·</span>
      <span>Wanderlust Magazine</span><span style="color:#2A3550">·</span>
      <span>Brainz Magazine</span><span style="color:#2A3550">·</span>
      <span>Solarcon</span><span style="color:#2A3550">·</span>
      <span>Meta Dynamics L3</span><span style="color:#2A3550">·</span>
      <span>Int'l Coach Guild</span>
    </div>
    <!-- "1000+ lives already changed" is the number he actually runs on his own
         banner. Use his number, not a vaguer one I invented. And the countries
         are now NAMED by the testimonials above -- Sweden, Bulgaria, USA -- so
         "7 countries" stops being a claim and starts being a receipt. -->
    <div style="display:flex;align-items:center;justify-content:center;gap:clamp(18px,3vw,40px);flex-wrap:wrap;margin-top:22px;font-size:.85rem;color:#5E6B85">
      <span><strong style="color:#B1BFD7">1000+</strong> lives changed</span>
      <span><strong style="color:#B1BFD7">7</strong> countries</span>
      <span><strong style="color:#B1BFD7">5+</strong> years facilitating</span>
    </div>
  </div>
</section>

</div>`;

  function addFonts(){
    if (document.getElementById('px-fonts')) return;
    var p1=document.createElement('link'); p1.rel='preconnect'; p1.href='https://fonts.googleapis.com'; document.head.appendChild(p1);
    var p2=document.createElement('link'); p2.rel='preconnect'; p2.href='https://fonts.gstatic.com'; p2.crossOrigin=''; document.head.appendChild(p2);
    var l=document.createElement('link'); l.id='px-fonts'; l.rel='stylesheet'; l.href='https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Caveat:wght@500;600;700&display=swap'; document.head.appendChild(l);
  }

  function loadScript(src){
    return new Promise(function(res,rej){
      var ex=document.querySelector('script[data-px="'+src+'"]');
      if(ex){ if(ex.getAttribute('data-loaded')){res();} else { ex.addEventListener('load',function(){res();}); ex.addEventListener('error',rej);} return; }
      var s=document.createElement('script'); s.src=src; s.async=false; s.setAttribute('data-px',src);
      s.addEventListener('load',function(){ s.setAttribute('data-loaded','1'); res(); });
      s.addEventListener('error',rej);
      document.head.appendChild(s);
    });
  }

  function loadLibs(){
    var g=loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js')
      .then(function(){ return loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js'); });
    var l=loadScript('https://unpkg.com/lenis@1.1.13/dist/lenis.min.js');
    return Promise.all([ g.catch(function(){}), l.catch(function(){}) ]);
  }

  function collapseAncestors(host){
    try{ var h=host.getBoundingClientRect().height; if(h<50) return;
      var n=host.parentElement,guard=0;
      while(n && n!==document.body && guard++<14){ if(n.getBoundingClientRect().height>h+600){ n.style.height='auto'; n.style.minHeight='0px'; } n=n.parentElement; }
    }catch(e){}
  }

  function boot(root){

    if(!root || !root.getElementById('px-root')) return;
    root.querySelectorAll('a[href^="#"]').forEach(function(a){ a.addEventListener('click',function(e){ var id=a.getAttribute('href'); if(id && id.length>1){ var t=root.querySelector(id); if(t){ e.preventDefault(); t.scrollIntoView({behavior:'smooth'}); } } }); });

    /* ══ HERO IMAGE — DANIEL, BEHIND THE GLASS ══════════════════════════
       Shot from outside at blue hour. Him inside, close to the pane,
       looking straight out at you. Level gaze. Warm lamp behind him.

       THE RULE THIS IMAGE LIVES BY: it is NEVER captioned, named or
       labelled anywhere in the hero. To a cold visitor it is just "a man
       who can't be reached" -- the mirror. To a warm visitor it's Daniel,
       and they clock it the moment they wipe. Then section 06 says
       "I was the man behind the glass. I sat in there seven years." and
       it fires backwards up the whole page. Put a name on it up here and
       it becomes a coach's portrait and the trapdoor never opens.

       PREPARED FOR THE SHADER, not for looking at:
       black point lifted (near-black went 5.95% -> 0.16%). Dirt SCATTERS
       light -- anything near black turns to flat grey mud under the film
       and there is nothing left to reveal when he wipes it.

       enc_auto, never enc_avif (AVIF can silently fail as a WebGL texture
       and you get the fallback with no error in the console). */
    const PX_HERO_SRC = 'https://static.wixstatic.com/media/111174_05c7360ab71a442ca1d13ffc8340bb18~mv2.jpg/v1/fill/w_1800,h_1100,al_c,q_90,enc_auto/hero-daniel-behind-glass.jpg';

    /* ══ THE DIVIDER — THE DREAM, AND THE DISTANCE ══════════════════════
       Golden hour. Infinity pool, ocean, closed laptop. The life he was
       told to want, and he built it. She's leaning on his shoulder with
       her whole attention on him. He's staring at the horizon like it's
       a wall.

       THE SETTING IS THE ARGUMENT. The first pass at this was a dark
       candlelit dining room, and the polished half had nothing to be loud
       ABOUT -- two shades of beige, no gap between the sides. Give the
       shader a sunlit villa and the same drag becomes: a travel advert on
       the left, grey concrete and grey water on the right. Identical
       frame. All the colour gone. "It's a beautiful picture" stops being
       a metaphor and becomes literally true.

       BUILT FOR THE BAND, NOT CROPPED INTO IT. This section is ~3:1 at
       every desktop size (3.07:1 at 1920x1080). Almost no photograph is
       that shape, which is why the old portrait stand-in rendered as a
       band of teeth -- a 3:1 slice through the middle of a head-shot IS
       a mouth. So this frame is ENVIRONMENTAL: the people are small in
       it, with air above and around them, and it survives the crop.

       HIS FACE IS ON 50%, deliberately. The drag handle sits at 50%, so
       if he were off-centre the handle would land in the GAP between them
       -- left half him, right half her, reading as two different people.
       The caption says SAME MAN. The handle has to bisect HIS FACE so the
       polish drags across HIM.

       SHE IS ON THE LEFT, deliberately. Left is "from where they stand" --
       HER view. She belongs in the polished half, looking at a flawless
       man. Put her in the murk and she's standing inside his interior,
       which is the one place she has never been able to get to.

       Black point floored, saturation eased 6% at source -- the shader
       adds +62% on the left and the source has to leave it room. */
    const PX_SPLIT_SRC = 'https://static.wixstatic.com/media/111174_c6bbbb5291ee46d09a35f835643b5569~mv2.jpg/v1/fill/w_2600,h_867,al_c,q_90,enc_auto/divider-villa-pool.jpg';

    /* ══ SECTION 05 — WHAT'S BEHIND THE THREE PANES ═════════════════════
       Was PX_HERO_SRC. Which meant the reward for fitting all three panes
       was... looking at his own face again. The section says "fit all three
       and THEY CAN REACH YOU" -- so the payoff has to be a PERSON, reaching.

       It's Daniel and Luiza. Her arm round his neck, her hand on his chest,
       her whole weight leaning in, and he's letting it land and laughing.
       That is what "reachable" looks like, and it's the one thing on this
       page that is not an argument -- it's evidence. Demonstrated outcome,
       not theory.

       SQUARE, and the stage is square to match. It's a vertical photo of two
       people; a landscape crop keeps the faces and throws the POSTURE away,
       and the posture is the entire point.

       NOTE FOR THE COPY PASS: this now front-loads section 06. The visitor
       clears this glass, sees the man from the hero, alive -- and works out
       who it is before Daniel says so. Section 06 stops being the REVEAL and
       becomes the EXPLANATION. Feeling first, story second. Its copy needs
       to be re-cut for that. */
    const PX_SYSTEM_SRC = 'https://static.wixstatic.com/media/111174_02c371279b93485ebbae695ecd18686d~mv2.jpg/v1/fill/w_1400,h_1400,al_c,q_90,enc_auto/system-reachable.jpg';

    const reduce   = window.matchMedia('(prefers-reduced-motion:reduce)').matches;
    const coarse   = window.matchMedia('(hover:none)').matches;
    const lowPower = coarse || window.innerWidth < 900 || (navigator.hardwareConcurrency||8) <= 4;

    /* ══════════ SHARED GLASS TOOLKIT ══════════
       One noise/grime prelude, three shaders. No backticks inside any
       GLSL string -- they are template literals and one stray backtick
       kills the whole script. Learned that the hard way. */
    const VERT = 'attribute vec2 p;varying vec2 v;void main(){v=p*0.5+0.5;gl_Position=vec4(p,0.,1.);}';

    const NOISE = [
      'precision highp float;',
      'varying vec2 v;',
      'float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
      'float noise(vec2 p){vec2 i=floor(p),f=fract(p);vec2 w=f*f*(3.0-2.0*f);',
      ' return mix(mix(hash(i),hash(i+vec2(1.0,0.0)),w.x),mix(hash(i+vec2(0.0,1.0)),hash(i+vec2(1.0,1.0)),w.x),w.y);}',
      'float fbm(vec2 p){float s=0.0,a=0.5;for(int i=0;i<5;i++){s+=a*noise(p);p*=2.03;a*=0.5;}return s;}',
      'float grimeAt(vec2 p){',
      ' float haze=fbm(p*vec2(5.5,3.8));',      // broad cloudiness
      ' float smear=fbm(vec2(p.x*3.2,p.y*44.0));', // cloth / rain streaks
      ' float dust=fbm(p*34.0);',                  // fine speckle
      ' return clamp(haze*0.58+smear*0.27+dust*0.15,0.0,1.0);}',
      // transmission + scatter. dirt SCATTERS light, it does not absorb it.
      // it lifts the blacks and goes pale. never dark, never blue.
      'vec3 filmify(vec3 col, vec3 scat, float dens, vec3 tint){',
      ' float T=exp(-dens*3.4);',
      ' float bloom=dot(scat,vec3(0.299,0.587,0.114));',
      ' vec3 scatCol=mix(scat, vec3(bloom)*tint, 0.80);',   // strip the navy OUT of the dirt
      ' vec3 veil=(scatCol*0.34 + tint*(0.34+0.62*bloom))*(1.0-T);',
      ' vec3 o=col*T+veil;',
      ' return mix(o, vec3(dot(o,vec3(0.299,0.587,0.114)))*tint*1.10, dens*0.50);}',
      'const vec3 FILM = vec3(0.78,0.69,0.52);'   // city film. amber nicotine. years of it.
    ].join('\n');

    function makeGL(canvas, fragBody){
      const gl = canvas.getContext('webgl',{antialias:false,alpha:false,powerPreference:'high-performance'});
      if(!gl) return null;
      const sh=(t,src)=>{const s=gl.createShader(t);gl.shaderSource(s,src);gl.compileShader(s);
        if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s;};
      let prog;
      try{
        prog=gl.createProgram();
        gl.attachShader(prog, sh(gl.VERTEX_SHADER, VERT));
        gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, NOISE + '\n' + fragBody));
        gl.linkProgram(prog);
        if(!gl.getProgramParameter(prog,gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
      }catch(e){ console.warn('[px] shader failed:', e.message); return null; }
      gl.useProgram(prog);
      const b=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,b);
      gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
      const loc=gl.getAttribLocation(prog,'p');
      gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
      const resize=()=>{const d=Math.min(window.devicePixelRatio||1,1.25);const r=canvas.getBoundingClientRect();
        canvas.width=Math.max(1,r.width*d); canvas.height=Math.max(1,r.height*d); gl.viewport(0,0,canvas.width,canvas.height);};
      resize(); window.addEventListener('resize',resize,{passive:true});
      return { gl, prog, U:(n)=>gl.getUniformLocation(prog,n), draw:()=>gl.drawArrays(gl.TRIANGLES,0,3) };
    }

    function makeTex(gl, unit){
      const t=gl.createTexture();
      gl.activeTexture(gl.TEXTURE0+unit); gl.bindTexture(gl.TEXTURE_2D,t);
      gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,1,1,0,gl.RGBA,gl.UNSIGNED_BYTE,new Uint8Array([10,29,60,255]));
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
      return t;
    }
    function loadImg(gl, tex, unit, src, cb){
      const im=new Image(); im.crossOrigin='anonymous';
      im.onload=()=>{ gl.activeTexture(gl.TEXTURE0+unit); gl.bindTexture(gl.TEXTURE_2D,tex);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,true);
        gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,im);
        cb(im.naturalWidth, im.naturalHeight); };
      im.onerror=()=>console.warn('[px] image missing:', src);
      im.src=src;
    }

    /* COVER, with a FOCAL POINT.
       The old version cropped from the centre. That was fine for a stand-in
       and fatal for the real hero: Daniel's face sits at roughly x=0.70 of
       a 16:10 frame, and a centre-crop on a tall viewport slices the right
       edge off -- taking his face with it and leaving a photo of a wall.
       So we anchor the crop on the FACE and let the empty left side of the
       frame be the thing that gets sacrificed. It's empty on purpose; the
       headline is sitting on it. */
    /* MIND THE FLIP. loadImg() uploads with UNPACK_FLIP_Y_WEBGL=true, so in
       TEXTURE space y=1 is the TOP of the photo and y=0 is the bottom. A
       focal y of 0.63 therefore anchors the crop NEAR THE TOP -- which is
       where his head is. Setting it to 0.42 (which reads like "a bit above
       centre") anchors LOW and guillotines him. It is backwards from CSS
       background-position, where 0% is the top. Don't trust your instinct
       here, just look at the render. */
    const COVER =
      'vec2 cover(vec2 uv, vec2 res, vec2 img, vec2 f){float ra=res.x/res.y, ia=img.x/img.y; vec2 s=uv;' +
      ' if(ra>ia){ float k=ia/ra; s.y=(uv.y-0.5)*k+clamp(f.y,0.5*k,1.0-0.5*k); }' +
      ' else { float k=ra/ia; s.x=(uv.x-0.5)*k+clamp(f.x,0.5*k,1.0-0.5*k); } return s;}';

    /* ══ VISIBILITY-GATED RENDERING ══
       There are FOUR full-screen WebGL canvases on this page. v5 drew all
       four of them every single frame, whether they were on screen or not --
       two of them viewport-sized, each with a 16-tap blur loop per pixel.
       The GPU saturated and the scroll starved. It stalled hardest at the
       divider, because that's where the second full-bleed canvas joins in.

       Now a canvas only draws when it's in (or near) the viewport, and
       nothing draws at all when the tab is hidden. */
    const renderers = [];
    const addRenderer = (el, fn) => renderers.push({ el, fn, on:false });

    const vis = ('IntersectionObserver' in window)
      ? new IntersectionObserver((entries)=>{
          entries.forEach(e=>{
            const r = renderers.find(x=>x.el===e.target);
            if(r) r.on = e.isIntersecting;
          });
        },{ rootMargin:'220px 0px' })   // spin up just before it arrives
      : null;

    let pageVisible = true;
    document.addEventListener('visibilitychange',()=>{ pageVisible = !document.hidden; });

    /* ══════════════ 01 · HERO ══════════════ */
    (function hero(){
      const canvas=root.getElementById('px-glass');
      const fb=root.getElementById('px-fallback');

      const useFallback=()=>{
        if(canvas) canvas.style.display='none';
        if(!fb) return;
        fb.style.display='block';
        root.getElementById('px-fb-img').style.backgroundImage='url('+PX_HERO_SRC+')';

        /* THE GLASS STILL HAS TO CLEAR HERE.
           No cursor on a phone means no wipe, so scroll does the wiping:
           --px-clear runs 0 -> 1 across the hero and the CSS filters follow.
           Same beat as the WebGL path (uProg), same payoff -- he scrolls,
           the fog lifts, a face is looking back at him.
           Reduced-motion users get it too; it's a scrub, not an animation. */
        if(window.gsap && window.ScrollTrigger){
          gsap.registerPlugin(ScrollTrigger);
          gsap.to(fb,{ '--px-clear':1, ease:'none',
            scrollTrigger:{ trigger:root.getElementById('px-hero'), start:'top top', end:'bottom top', scrub:.6 } });
        } else {
          fb.style.setProperty('--px-clear','1');   // no GSAP: just show him
        }
      };

      if(reduce || lowPower || !canvas){ useFallback(); return; }

      const R = makeGL(canvas, COVER + [
        'uniform sampler2D uTex; uniform sampler2D uClean;',
        'uniform vec2 uRes,uImg,uMouse; uniform float uProg,uHas;',
        'void main(){ vec2 uv=v; vec2 s=cover(uv,uRes,uImg,vec2(0.70,0.63));',
        ' float cleaned=pow(clamp(texture2D(uClean,uv).r,0.0,1.0),2.2);',   // 3 honest passes
        ' float ra=uRes.x/uRes.y; vec2 m=uMouse; m.x*=ra; vec2 pa=uv; pa.x*=ra;',
        ' float wet=(1.0-smoothstep(0.012,0.072,distance(pa,m)))*0.22;',
        ' float open=clamp(max(cleaned,uProg*1.15),0.0,1.0); float armour=1.0-open;',
        ' float g=clamp(0.70+grimeAt(uv)*0.58,0.0,1.0)*armour;',
        ' vec2 e=vec2(0.0022,0.0);',
        ' vec2 gr=vec2(grimeAt(uv+e.xy)-grimeAt(uv-e.xy), grimeAt(uv+e.yx)-grimeAt(uv-e.yx));',
        ' vec2 duv=s+gr*0.055*armour;',
        ' vec3 col,scat;',
        ' if(uHas>0.5){ float ab=0.0016*armour;',
        '  col=vec3(texture2D(uTex,duv+vec2(ab,0.0)).r, texture2D(uTex,duv).g, texture2D(uTex,duv-vec2(ab,0.0)).b);',
        '  float r=0.030*g; scat=vec3(0.0);',
        '  for(int i=0;i<8;i++){float a=float(i)*0.7854; vec2 d=vec2(cos(a),sin(a));',
        '   scat+=texture2D(uTex,duv+d*r*(0.55+0.45*hash(uv+float(i)))).rgb; scat+=texture2D(uTex,duv+d*r*0.45).rgb;}',
        '  scat/=16.0;',
        ' } else { float gw=1.0-distance(s,vec2(0.66,0.42));',
        '  col=mix(vec3(0.012,0.055,0.13),vec3(0.16,0.24,0.40),pow(max(gw,0.0),2.2)); scat=col; }',
        ' col=filmify(col,scat,g,FILM);',
        ' col+=vec3(0.86,0.88,0.92)*wet*armour*1.8;',
        ' float lum=dot(col,vec3(0.299,0.587,0.114));',
        ' vec3 cold=mix(vec3(lum),col,0.55)*vec3(0.80,0.90,1.10);',
        ' vec3 warm=mix(vec3(lum),col,1.15)*vec3(1.12,0.98,0.88);',
        ' warm+=vec3(1.0,0.31,0.12)*pow(lum,3.0)*0.10*uProg;',
        ' col=mix(mix(cold,warm,open), col, g*0.95);',   // the grade is the SCENE, not the pane
        ' col*=1.0-0.42*pow(distance(uv,vec2(0.5)),2.0);',
        ' col+=(fract(sin(dot(uv*uRes,vec2(12.99,78.23)))*43758.55)-0.5)*0.022;',
        ' gl_FragColor=vec4(col,1.0); }'
      ].join('\n'));
      if(!R){ useFallback(); return; }

      const gl=R.gl;
      const u={tex:R.U('uTex'),clean:R.U('uClean'),res:R.U('uRes'),img:R.U('uImg'),mouse:R.U('uMouse'),prog:R.U('uProg'),has:R.U('uHas')};
      const tex=makeTex(gl,0), cleanTex=makeTex(gl,1);
      const st={prog:0,mx:.72,my:.42,tmx:.72,tmy:.42,has:0,iw:16,ih:9};
      loadImg(gl,tex,0,PX_HERO_SRC,(w,h)=>{st.has=1;st.iw=w;st.ih=h;});

      /* THREE PASSES TO CLEAN, and it cannot be cheated by moving slowly.
         PASS  = current stroke, painted with 'lighten' (per-pixel MAX), so
                 one sweep can deposit at most PASS_STRENGTH however long
                 you linger. CLEAN = banked passes. COMBO = what we upload. */
      const CM=220, WIPE_RADIUS=0.058, PASS_STRENGTH=0.30, PASS_END_MS=130;
      const mk=()=>{const c=document.createElement('canvas');c.width=c.height=CM;return c;};
      const cm=mk(), passC=mk(), comboC=mk();
      const cx=cm.getContext('2d'), pxx=passC.getContext('2d'), cox=comboC.getContext('2d',{willReadFrequently:true});
      const black=(c)=>{c.globalCompositeOperation='source-over';c.fillStyle='#000';c.fillRect(0,0,CM,CM);};
      black(cx); black(pxx);
      let dirty=true, timer=null, ppx=null, ppy=null, frames=0;
      const commit=()=>{ cx.globalCompositeOperation='lighter'; cx.drawImage(passC,0,0);
        cx.globalCompositeOperation='source-over'; black(pxx); dirty=true; };
      const compose=()=>{ cox.globalCompositeOperation='source-over'; cox.drawImage(cm,0,0);
        cox.globalCompositeOperation='lighter'; cox.drawImage(passC,0,0); return comboC; };
      const measure=()=>{ const d=cox.getImageData(0,0,CM,CM).data; let lit=0,n=0;
        for(let i=0;i<d.length;i+=64){n++; if(d[i]>150)lit++;} return lit/n; };
      const wipe=(x,y)=>{
        const steps=(ppx==null)?1:Math.min(28,Math.ceil(Math.hypot(x-ppx,y-ppy)*CM/4)+1);
        pxx.globalCompositeOperation='lighten';   // MAX -- lingering cannot cheat
        const A=PASS_STRENGTH;
        for(let i=0;i<steps;i++){
          const t=steps===1?1:i/(steps-1);
          const ix=(ppx==null?x:ppx+(x-ppx)*t)*CM, iy=(ppy==null?y:ppy+(y-ppy)*t)*CM, r=CM*WIPE_RADIUS;
          const g=pxx.createRadialGradient(ix,iy,0,ix,iy,r);
          g.addColorStop(0,'rgba(255,255,255,'+A+')');
          g.addColorStop(0.45,'rgba(255,255,255,'+(A*0.80)+')');
          g.addColorStop(0.75,'rgba(255,255,255,'+(A*0.38)+')');
          g.addColorStop(1,'rgba(255,255,255,0)');
          pxx.fillStyle=g; pxx.beginPath(); pxx.arc(ix,iy,r,0,6.2832); pxx.fill();
        }
        ppx=x; ppy=y; dirty=true;
        if(timer) clearTimeout(timer);
        timer=setTimeout(commit, PASS_END_MS);
      };

      const heroEl=root.getElementById('px-hero');
      window.addEventListener('pointermove', e=>{
        const r=heroEl.getBoundingClientRect();
        const x=(e.clientX-r.left)/r.width, y=(e.clientY-r.top)/r.height;
        const inside = e.clientY>r.top && e.clientY<r.bottom && x>=0 && x<=1;
        if(!inside){ ppx=ppy=null; return; }
        st.tmx=x; st.tmy=y;
        wipe(x,y);   // still works. no prompt, no ring, no meter. a secret.
      },{passive:true});
      window.addEventListener('pointerleave',()=>{ ppx=ppy=null; });

      addRenderer(canvas, ()=>{
        st.mx+=(st.tmx-st.mx)*0.18; st.my+=(st.tmy-st.my)*0.18;
        gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D,tex);
        gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D,cleanTex);
        if(dirty){ gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,compose()); dirty=false; }
        gl.useProgram(R.prog);
        gl.uniform1i(u.tex,0); gl.uniform1i(u.clean,1);
        gl.uniform2f(u.res,canvas.width,canvas.height); gl.uniform2f(u.img,st.iw,st.ih);
        gl.uniform2f(u.mouse,st.mx,1.0-st.my); gl.uniform1f(u.prog,st.prog); gl.uniform1f(u.has,st.has);
        R.draw();
      });
      window.__pxHeroState = st;   // the scroll spine drives st.prog
    })();

    /* ══════════════ 03 · THE SPLIT — their side / your side ══════════════
       Left of the handle  = FLAWLESS. What they get. Over-polished, glossy,
                             a brochure photo. The polish IS the film.
       Right of the handle = MURK. What it feels like from in there.
       The handle bisects HIS FACE. Same man. Drag it across. */
    (function split(){
      const canvas=root.getElementById('px-split');
      const wrap=root.getElementById('px-reframe');
      const handle=root.getElementById('px-handle');
      if(!canvas||!wrap) return;

      if(reduce || !window.WebGLRenderingContext){
        if(canvas) canvas.style.display='none';
        const h=root.getElementById('px-handle'); if(h) h.style.display='none';
        wrap.style.cursor='default';
        return;
      }

      const R=makeGL(canvas, COVER + [
        'uniform sampler2D uTex; uniform vec2 uRes,uImg; uniform float uSplit,uHas;',
        'void main(){ vec2 uv=v; vec2 s=cover(uv,uRes,uImg,vec2(0.50,0.50));',
        /* The 0.62 zoom-out that used to live here is GONE. It existed to
           rescue a portrait stand-in from a 3:1 band by shrinking it until
           the teeth stopped being teeth. The real frame is shot 3:1, built
           for this band, with his face on 50% -- so it wants a straight
           cover and nothing else. Zooming out now would just smear it. */
        /* INVERTED -- and this is the whole point.

           LEFT  (their side)  = FLAWLESS. Sharp, bright, saturated, glossy.
                                 A little TOO perfect. A brochure photo.
                                 Because that is exactly what they get: the
                                 capable one, the composed one, the one who
                                 is fine. The clean image IS the film. That
                                 is the horror -- it looks great, and nobody
                                 has ever got past it.

           RIGHT (your side)   = MURK. Veiled, distant, the colour drained
                                 out of it. Because that is what it actually
                                 feels like from in there.

           v5 had these the wrong way round: "you look fine to yourself and
           grubby to them." Backwards, and it made the MAN look like the
           mess. He is not the mess. The polish is. */
        /* THE AXIS OF THE SPLIT IS COLOUR, NOT VISIBILITY.
           v6 hid his side behind grime, so the section read as "clear vs
           obscured" -- and it made the polished half look merely normal by
           comparison. Nothing was bold. Nothing was dead. It was just two
           kinds of beige.

           The real contrast is LIFE vs NO LIFE:
             LEFT  = bold, vibrant, glossy. Advert-grade. Too much.
             RIGHT = draining to black-and-white. Soft. Flat. Still fully
                     legible -- he can see everything, he just can't feel it.
                     That is precisely the complaint. Hiding it would be
                     the wrong metaphor entirely. */
        ' float mine = step(uSplit, uv.x);',              // 1 on HIS side of the pane
        ' float g = mine * clamp(0.20 + grimeAt(uv)*0.14, 0.0, 1.0);',   // barely a veil
        ' vec2 e=vec2(0.0022,0.0);',
        ' vec2 gr=vec2(grimeAt(uv+e.xy)-grimeAt(uv-e.xy), grimeAt(uv+e.yx)-grimeAt(uv-e.yx));',
        ' vec2 duv=s+gr*0.005*mine;',                    // a hair of warp. not a smear.
        ' vec3 col,scat;',
        ' if(uHas>0.5){ col=texture2D(uTex,duv).rgb;',
        /* BLUR IS THE WRONG INSTRUMENT AND I KEEP REACHING FOR IT.
           Blur says "he can't see it." He can. He sees the pool, the ocean,
           her face, all of it, in perfect focus. It just doesn't land. The
           deadness is in the COLOUR and the CONTRAST -- the picture is
           sharp and it is a corpse. So: almost no defocus at all. Enough to
           take the sparkle off the water, nothing more. */
        '  float r=0.0028*mine; scat=vec3(0.0);',
        '  for(int i=0;i<6;i++){float a=float(i)*1.0472; vec2 d=vec2(cos(a),sin(a));',
        '   scat+=texture2D(uTex,duv+d*r).rgb;}',
        '  scat/=6.0;',
        ' } else { col=vec3(0.05,0.12,0.24); scat=col; }',

        /* THEIR SIDE — the brochure. Loud, warm, glossy, a touch too much.
           It should look like it's selling something. That IS the joke. */
        ' float lum0=dot(col,vec3(0.299,0.587,0.114));',
        ' vec3 polished = mix(vec3(lum0), col, 1.62);',                      // saturation, hard
        ' polished = (polished-0.5)*1.30 + 0.5;',                            // contrast, hard
        ' polished *= vec3(1.09,1.05,0.99);',                                // golden, magazine-warm
        ' polished += vec3(1.0,0.97,0.90)*pow(max(lum0-0.58,0.0),1.7)*0.95;', // a real sheen on the highlights
        ' polished = clamp(polished,0.0,1.0);',

        /* HIS SIDE — the colour going out of it. Near monochrome, softly out
           of focus, flat. Nothing hidden. He can see it all. It just doesn't
           reach him. */
        ' vec3 murk = mix(col, scat, 0.25);',                                // sharp. he sees everything.
        ' float lm = dot(murk,vec3(0.299,0.587,0.114));',
        ' murk = mix(vec3(lm), murk, 0.16);',                                // 84% of the colour gone
        ' murk = (murk-0.5)*0.88 + 0.5;',                                    // flat. no bite left.
        ' murk *= vec3(0.96,0.98,1.04);',                                    // the last of it turning cold
        ' murk = mix(murk, vec3(0.36,0.38,0.42), g*0.13);',                  // a breath of haze, that's all
        ' col = mix(polished, murk, mine);',
        // a hairline of light down the divider itself
        ' float edge=1.0-smoothstep(0.0,0.0035,abs(uv.x-uSplit));',
        ' col+=vec3(1.0,0.35,0.14)*edge*0.55;',
        ' col*=1.0-0.34*pow(distance(uv,vec2(0.5)),2.0);',
        ' gl_FragColor=vec4(col,1.0); }'
      ].join('\n'));
      if(!R){ return; }

      const gl=R.gl;
      const u={tex:R.U('uTex'),res:R.U('uRes'),img:R.U('uImg'),split:R.U('uSplit'),has:R.U('uHas')};
      const tex=makeTex(gl,0);
      const st={split:0.5, target:0.5, has:0, iw:16, ih:9};
      loadImg(gl,tex,0,PX_SPLIT_SRC,(w,h)=>{st.has=1;st.iw=w;st.ih=h;});

      let drag=false;
      const setFrom=(clientX)=>{ const r=wrap.getBoundingClientRect();
        st.target=Math.min(0.97,Math.max(0.03,(clientX-r.left)/r.width)); };
      wrap.addEventListener('pointerdown',e=>{drag=true; setFrom(e.clientX); wrap.setPointerCapture(e.pointerId);});
      wrap.addEventListener('pointermove',e=>{ if(drag||e.buttons===1) setFrom(e.clientX);
        else { const r=wrap.getBoundingClientRect(); // gentle follow on hover too
               st.target = Math.min(0.97,Math.max(0.03,(e.clientX-r.left)/r.width)); } });
      wrap.addEventListener('pointerup',()=>{drag=false;});
      wrap.addEventListener('pointerleave',()=>{drag=false; st.target=0.5;});

      addRenderer(canvas, ()=>{
        st.split += (st.target-st.split)*0.12;
        if(handle) handle.style.left=(st.split*100)+'%';
        gl.useProgram(R.prog);
        gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D,tex);
        gl.uniform1i(u.tex,0);
        gl.uniform2f(u.res,canvas.width,canvas.height); gl.uniform2f(u.img,st.iw,st.ih);
        gl.uniform1f(u.split,st.split); gl.uniform1f(u.has,st.has);
        R.draw();
      });
    })();

    /* ══════════════ 05 · THREE PANES ══════════════
       Straight out of the Connection System doc. Each MISSING pillar
       leaves its own kind of dirt, and names its own failure. */
    (function panes(){
      const canvas=root.getElementById('px-vv-c');
      if(!canvas) return;
      /* STARTS DIRTY. All three panes OUT.
         v4 started CLEAN, which meant the man who never clicked walked away
         with "She can see you" -- i.e. everything's fine. The worst possible
         message for the man we're actually trying to reach. Now the default
         state is where he genuinely is, and every pane he adds clears the
         view a little more. The LAST click lands on the promise, which is
         where the CTA catches him. */
      const on={vision:false,values:false,velocity:false};
      /* VELOCITY WAS #1E2A3D -- navy ink. Which was fine when this section sat
         on cream and is invisible now that it sits on navy: a navy pill on a
         navy field. Mist is the third structural colour in the system and it
         reads on dark, which is the whole reason it exists. */
      const COLOUR={vision:'#E8C65F',values:'#FF501F',velocity:'#B1BFD7'};
      const INK={vision:'#1E2A3D',values:'#fff',velocity:'#0A1D3C'};   // text ON the filled pill
      const S={
        'vision,values,velocity':{l:'All three clear',b:'#E8C65F',
          h:'They can reach you.',
          t:"Clear on what you want. Grounded in who you are. Taking action that matches both. Connection stops being a guessing game. You stop chasing. You stop sabotaging. You start leading with clarity, and with love.",
          o:'All three panes clear. A healthy, functional, romantic relationship.'},
        'vision,values':{l:'Missing Velocity',b:'#1E2A3D',
          h:'You know exactly who you need to be. You never became him.',
          t:"A lot of journalling. A lot of reflecting. Not a lot different. You're stood on the shore knowing precisely where you want to swim, and you never get in the water. Ten years of podcasts, same relationship waiting at the end of it.",
          o:'Standing on the shore. Never getting in.'},
        'values,velocity':{l:'Missing Vision',b:'#E8C65F',
          h:"You're moving. You've no idea where.",
          t:"Out there, active, meeting people, and mostly the wrong ones. Situationships that don't match anything you actually want. Plenty of effort with nothing behind it. Chasing chemistry and reacting to whoever shows up.",
          o:'Moving fast. Pointed nowhere.'},
        'vision,velocity':{l:'Missing Values',b:'#FF501F',
          h:'It starts strong. Then it comes apart.',
          t:"You know what you want and you're going after it, and you haven't done the work on who you'd have to be to hold it. So you compromise without noticing. Go soft on what you need. Pretzel yourself to be liked. This one's worse than being alone. It erodes you.",
          o:'Looks good early. Shaky underneath.'},
        'vision':{l:'Vision only',b:'#E8C65F',
          h:'A beautiful picture of a life you never walk into.',
          t:"You can describe them. You can describe the life. And nothing in how you actually live is pointed at it.",
          o:'A picture you never walk into.'},
        'values':{l:'Values only',b:'#FF501F',
          h:'Good man. Going nowhere.',
          t:"Solid, decent, self-aware, and no direction and no momentum. Waiting to be found.",
          o:'Waiting to be found.'},
        'velocity':{l:'Velocity only',b:'#1E2A3D',
          h:'Busy. Very busy.',
          t:"Dates, apps, gym, work. Motion mistaken for progress. None of it lands anywhere.",
          o:'Motion mistaken for progress.'},
        '':{l:'Nothing',b:'#7C89A3',
          h:'This is where most of us start.',
          t:"No judgment. I was here for seven years. Everything's fine, nothing connects, and you can't put your finger on why.",
          o:"Everything's fine. Nothing connects."}
      };

      const R = makeGL(canvas, COVER + [
        'uniform sampler2D uTex; uniform vec2 uRes,uImg; uniform float uHas,uV,uA,uL;',
        'void main(){ vec2 uv=v; vec2 s=cover(uv,uRes,uImg,vec2(0.50,0.50));',
        /* THE SUM-AND-CLAMP BUG.
           This was: g = clamp(dV+dA+dL, 0.0, 1.0).
           Each dirt term runs to about 0.85 when its pillar is missing. So
           three missing summed to ~2.5 and TWO missing summed to ~1.7 --
           and both clamped flat to 1.0. Pixel-for-pixel identical. The first
           click cleared nothing because the maths had already saturated
           before the reader ever touched it.

           AVERAGE, don't sum. Now each pillar owns exactly a third of the
           glass, and fitting one visibly takes a third of the dirt off.
           The 0.72 curve then pushes the dirty end back down so the opening
           state is still properly filthy:

             3 missing  g .90     4 missing? no. this is the ladder:
             2 missing  g .68
             1 missing  g .41
             0 missing  g  0      -- and she can see him.

           Each term keeps its own noise, so the CHARACTER of each missing
           pillar survives: haze, streaks, dust. */
        ' float dV=(1.0-uV)*clamp(0.62+fbm(uv*vec2(5.0,3.6))*0.5,0.0,1.0);',        // vision  : broad haze, no direction
        ' float dA=(1.0-uA)*clamp(0.62+fbm(vec2(uv.x*3.0,uv.y*40.0))*0.5,0.0,1.0);',// values  : streaks, self-abandonment
        ' float dL=(1.0-uL)*clamp(0.62+fbm(uv*26.0)*0.5,0.0,1.0);',                 // velocity: dust that never gets shifted

        /* AN S-CURVE, NOT A STRAIGHT LINE.
           A linear ladder (.90 / .67 / .41 / 0) made the last click do all
           the work -- two pillars in and the glass was still half filthy, so
           the jump from 2 to 3 was a cliff. That's the wrong story. Fit two
           of the three and you should be NEARLY THERE. The last one is the
           hardest, not the biggest.

           smoothstep does exactly that -- it hangs at the dirty end and
           falls away fast once he's most of the way:

             0 fitted   g .94    barely a shape
             1 fitted   g .63    something's in there
             2 fitted   g .22    almost him
             3 fitted   g  0     and she can see him */
        ' float a3=clamp((dV+dA+dL)/3.0,0.0,1.0);',
        ' float g=a3*a3*(3.0-2.0*a3);',
        ' vec3 col,scat;',
        ' if(uHas>0.5){ col=texture2D(uTex,s).rgb;',
        '  float r=0.030*g; scat=vec3(0.0);',
        '  for(int i=0;i<6;i++){float a=float(i)*1.0472; vec2 d=vec2(cos(a),sin(a));',
        '   scat+=texture2D(uTex,s+d*r).rgb;}',
        '  scat/=6.0;',
        ' } else { col=vec3(0.05,0.12,0.24); scat=col; }',
        ' col=filmify(col,scat,g,FILM);',
        /* AND THE COLOUR COMES BACK.
           Blur alone is a technical change; the reader clocks it and moves
           on. COLOUR RETURNING is felt. Dirty glass is grey and dead --
           and as the panes fit, the warmth bleeds back into it. By two
           pillars there's real colour in there; by three it's a warm
           photograph of two people laughing. That's the payoff, and it is
           the same argument the divider makes: the deadness was never in
           his eyes, it was in the colour. */
        ' float lum=dot(col,vec3(0.299,0.587,0.114));',
        ' col=mix(col, vec3(lum), g*0.86);',
        ' col*=1.0-0.35*pow(distance(uv,vec2(0.5)),2.0);',
        ' gl_FragColor=vec4(col,1.0); }'
      ].join('\n'));
      if(!R) return;

      const gl=R.gl;
      const u={tex:R.U('uTex'),res:R.U('uRes'),img:R.U('uImg'),has:R.U('uHas'),V:R.U('uV'),A:R.U('uA'),L:R.U('uL')};
      const tex=makeTex(gl,0);
      const st={has:0,iw:16,ih:9,V:1,A:1,L:1,tV:1,tA:1,tL:1};
      loadImg(gl,tex,0,PX_SYSTEM_SRC,(w,h)=>{st.has=1;st.iw=w;st.ih=h;});

      const key=()=>['vision','values','velocity'].filter(k=>on[k]).join(',');
      const cta=root.getElementById('px-vv-cta');
      const paint=()=>{
        const s=S[key()];
        const done = on.vision && on.values && on.velocity;
        if(cta) cta.classList.toggle('show', done);   // he ends on the promise
        root.getElementById('px-vv-label').textContent=s.l;
        root.getElementById('px-vv-head').textContent=s.h;
        root.getElementById('px-vv-body').textContent=s.t;
        root.getElementById('px-vv-title').textContent=s.o;
        root.getElementById('px-vv-card').style.borderTopColor=s.b;
        st.tV=on.vision?1:0; st.tA=on.values?1:0; st.tL=on.velocity?1:0;
        root.querySelectorAll('.px-pill').forEach(p=>{
          const k=p.dataset.k, c=COLOUR[k], act=on[k];
          p.style.borderColor=c;
          p.style.background=act?c:'transparent';
          p.style.color=act?INK[k]:c;
          p.style.textDecoration=act?'none':'line-through';
          p.style.opacity=act?'1':'.72';
        });
      };
      root.querySelectorAll('.px-pill').forEach(p=>{
        p.addEventListener('click',()=>{ on[p.dataset.k]=!on[p.dataset.k]; paint(); });
      });
      paint();

      addRenderer(canvas, ()=>{
        st.V+=(st.tV-st.V)*0.08; st.A+=(st.tA-st.A)*0.08; st.L+=(st.tL-st.L)*0.08;
        gl.useProgram(R.prog);
        gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D,tex);
        gl.uniform1i(u.tex,0);
        gl.uniform2f(u.res,canvas.width,canvas.height); gl.uniform2f(u.img,st.iw,st.ih);
        gl.uniform1f(u.has,st.has); gl.uniform1f(u.V,st.V); gl.uniform1f(u.A,st.A); gl.uniform1f(u.L,st.L);
        R.draw();
      });
    })();

    /* ══════════════ 07 · VIDEO FACADE ══════════════
       Nothing from youtube.com is requested until he presses play. Then the
       button becomes the iframe, in place, already playing. */
    (function proofVideos(){
      root.querySelectorAll('.px-vid').forEach(btn=>{
        btn.addEventListener('click',()=>{
          if(btn.dataset.live) return;
          const mp4 = btn.getAttribute('data-mp4');
          const yt  = btn.getAttribute('data-yt');
          if(!mp4 && !yt) return;
          btn.dataset.live = '1';
          let el;
          if(mp4){
            /* SELF-HOSTED, AND IT HAS SOUND.
               This is the opposite of the archetype clips: those are silent
               atmosphere and autoplay muted on hover. This is a man TALKING --
               muting it would leave a stranger moving his mouth at you. So:
               native controls, real audio, and it only ever loads on click.
               playsinline keeps iOS from hijacking it into fullscreen. */
            el = document.createElement('video');
            el.src = mp4;
            el.controls = true;
            el.autoplay = true;
            el.playsInline = true;
            el.setAttribute('playsinline','');
            el.preload = 'auto';
            el.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;background:#04122A';
          } else {
            el = document.createElement('iframe');
            el.src = 'https://www.youtube-nocookie.com/embed/'+yt+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';
            el.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture';
            el.setAttribute('allowfullscreen','');
            el.title = btn.getAttribute('aria-label') || 'Client story';
          }
          btn.innerHTML = '';
          btn.appendChild(el);
          btn.style.cursor = 'default';
          if(mp4){ const p = el.play(); if(p && p.catch) p.catch(()=>{}); }
        });
      });
    })();

    /* ══════════════ 04 · THE FIVE PANES ══════════════
       Films are CSS. Behind each pane (once its clip exists) is the first
       ten seconds of that archetype's video -- a face, fogged over, that
       comes alive when he clears the glass.

       ONE AT A TIME. Five dirty windows in a row; he moves across and each
       one wakes up and looks back at him, then goes under again. That is
       the whole page in a row of cards.

       LAZY TO THE BONE. preload='none' and the <video> element isn't even
       created until first hover. Five autoplaying clips on a page already
       running four WebGL canvases would be brutal, and most visitors will
       never touch one. Nothing is paid for until it's asked for. */
    (function fivePanes(){
      const panes=[...root.querySelectorAll('.px-pane')];
      if(!panes.length) return;
      const touch = window.matchMedia('(hover:none)').matches;

      /* ── BUILD THE FILM ────────────────────────────────────────────
         Each archetype is a different physical thing on the glass, and it
         comes off the way that thing would. All CSS transforms -- the JS
         only lays out the pieces. */
      const COLS=6, ROWS=9;                       // 54 bricks. enough to read as a wall.
      const makeFilm = (el) => {
        const kind = el.getAttribute('data-film');
        const f = document.createElement('div'); f.className='px-film';

        if(kind==='fortress'){
          /* A FORTRESS IS A WALL. So: a wall. Running bond -- every other
             course offset by half a brick, or it reads as a grid, not
             masonry. They fall BOTTOM-UP: knock out the base and the rest
             comes down after it. */
          for(let r=0;r<ROWS;r++){
            const off = (r%2) ? -0.5 : 0;         // the running bond
            for(let c=-1;c<=COLS;c++){
              const b=document.createElement('div'); b.className='px-brick';
              b.style.left   = ((c+off)*(100/COLS)) + '%';
              b.style.width  = (100/COLS - 0.9) + '%';
              b.style.top    = (r*(100/ROWS)) + '%';
              b.style.height = (100/ROWS - 1.1) + '%';
              b.style.setProperty('--r', ((Math.random()*22)-11).toFixed(1)+'deg');
              /* 62ms per course (was 34). The wall now takes ~500ms to come
                 down from base to top instead of 270 -- long enough to read
                 as masonry collapsing rather than a single flicker. The
                 random jitter stops the courses landing in lockstep. */
              b.style.transitionDelay = ((ROWS-1-r)*62 + Math.random()*70|0) + 'ms';
              f.appendChild(b);
            }
          }
        }
        else if(kind==='defender'){ const g=document.createElement('div'); g.className='px-grid'; f.appendChild(g); }
        else if(kind==='idealist'){ const b=document.createElement('div'); b.className='px-bloom'; f.appendChild(b); }
        else if(kind==='performer'){
          const l=document.createElement('div'); l.className='px-curtain l';
          const r=document.createElement('div'); r.className='px-curtain r';
          f.appendChild(l); f.appendChild(r);
        }
        else if(kind==='romantic'){ const s=document.createElement('div'); s.className='px-sheet'; f.appendChild(s); }
        else return;

        el.insertBefore(f, el.firstChild);
      };
      panes.forEach(makeFilm);

      const build = (el) => {
        const src = el.getAttribute('data-clip');
        if(!src || el.__v) return el.__v || null;
        const v = document.createElement('video');
        v.src = src;
        v.muted = true; v.defaultMuted = true;   // BOTH. Safari ignores the property alone.
        v.loop = true;
        v.playsInline = true;                    // without this iOS goes fullscreen. every time.
        v.setAttribute('playsinline','');
        v.setAttribute('muted','');
        v.preload = 'none';
        el.insertBefore(v, el.firstChild);
        el.__v = v;
        return v;
      };

      const open = (el) => {
        panes.forEach(o=>{ if(o!==el){ o.classList.remove('on'); if(o.__v){ o.__v.pause(); } } });
        el.classList.add('on');
        const v = build(el);
        if(v){ const p = v.play(); if(p && p.catch) p.catch(()=>{}); }
      };
      const close = (el) => {
        el.classList.remove('on');
        if(el.__v) el.__v.pause();
      };

      panes.forEach(el=>{
        if(el.getAttribute('data-clip')){
          const c=document.createElement('span'); c.className='cue'; c.textContent='watch';
          el.appendChild(c);
          const poster = el.getAttribute('data-poster');
          if(poster){ const p=document.createElement('div'); p.className='poster';
            p.style.backgroundImage='url('+poster+')'; el.insertBefore(p, el.firstChild); }
          /* Warm the connection on approach, not on page load. By the time the
             cursor lands the file is already coming down the wire. */
          el.addEventListener('pointerenter',()=>{ const v=build(el); if(v && v.preload==='none') v.preload='auto'; },{once:true});
        }

        if(!touch){
          el.addEventListener('pointerenter',()=>open(el));
          el.addEventListener('pointerleave',()=>close(el));
        }
        /* Touch: no hover, so tap opens it. Tap again (or tap another) closes.
           NOT autoplay-on-scroll -- five clips firing as he scrolls past is
           chaos, and it burns his data for something he didn't ask for. */
        el.addEventListener('click',()=>{
          if(el.classList.contains('on')) close(el); else open(el);
        });
      });
    })();

    /* ══════════════ THE FRAME LOOP + SCROLL SPINE ══════════════ */
    const G=window.gsap, ST=window.ScrollTrigger;
    const hasGSAP=!!(G&&ST);
    if(hasGSAP) G.registerPlugin(ST);

    if(vis) renderers.forEach(r=>vis.observe(r.el));

    const tick=()=>{
      if(!pageVisible) return;
      for(let i=0;i<renderers.length;i++){
        const r=renderers[i];
        if(r.on || !vis) r.fn();     // only what's on screen
      }
    };

    if(window.Lenis && !reduce){
      const lenis=new window.Lenis({duration:1.15,smoothWheel:true,touchMultiplier:1.4});
      const raf=(t)=>{ lenis.raf(t); tick(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
      if(hasGSAP) lenis.on('scroll', ST.update);
    } else {
      const raf=()=>{ tick(); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }

    if(hasGSAP && !reduce){
      // the armour comes down as he descends
      if(window.__pxHeroState){
        G.to(window.__pxHeroState,{prog:1,ease:'none',
          scrollTrigger:{trigger:root.getElementById('px-hero'),start:'top top',end:'bottom top',scrub:0.7}});
      }

      // kinetic type
      root.querySelectorAll('.px-line > span').forEach(l=>{
        G.to(l,{y:'0%',duration:1.05,ease:'expo.out',scrollTrigger:{trigger:l,start:'top 88%',once:true}});
      });
      root.querySelectorAll('.px-fade').forEach(el=>{
        G.to(el,{opacity:1,y:0,duration:.95,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 90%',once:true}});
      });

      /* 02 - THE THREAD.
         The whole conversation sits on one phone screen. No inner scroll,
         no tape, nothing to chase.

         As the phone enters view the messages wipe clear IN SEQUENCE --
         each incoming line, then the excuse he gave it. It plays like a
         conversation arriving, and he can't miss the last one, because
         there's nothing to scroll past. */
      const msgs=[...root.querySelectorAll('.px-in')];
      const outs=[...root.querySelectorAll('.px-out')];
      outs.forEach(o=>{ o.style.opacity='0'; o.style.transform='translateY(6px)';
        o.style.transition='opacity .5s ease, transform .5s ease'; });

      ST.create({
        trigger:root.querySelector('.px-phone'), start:'top 72%', once:true,
        onEnter:()=>{
          msgs.forEach((m,i)=>{
            setTimeout(()=>m.classList.add('wiped'), i*420);            // his honest thought clears
            const o=outs[i];
            if(o) setTimeout(()=>{ o.style.opacity='1'; o.style.transform='none'; }, i*420 + 700); // then his excuse
          });
        }
      });

      // fast scrollers / anyone who jumps past: nothing left fogged.
      ST.create({ trigger:root.getElementById('px-mirror'), start:'bottom 88%', once:true,
        onEnter:()=>{ msgs.forEach(m=>m.classList.add('wiped'));
                      outs.forEach(o=>{ o.style.opacity='1'; o.style.transform='none'; }); } });

    } else {
      root.querySelectorAll('.px-line > span').forEach(l=>l.style.transform='none');
      root.querySelectorAll('.px-fade').forEach(e=>{e.style.opacity='1';e.style.transform='none';});
      root.querySelectorAll('.px-in').forEach(c=>c.classList.add('wiped'));
      root.querySelectorAll('.px-out').forEach(o=>{o.style.opacity='1';o.style.transform='none';});
    }

    /* ══════════════ RESPONSIVE COLLAPSE ══════════════ */
    /* px-vv-grid is NOT in here any more. It's a two-row grid with explicit
       row/column placement, and this helper only knows how to rewrite
       grid-template-columns -- it would have collapsed the columns and left
       the card sitting in row 1 next to nothing. Its stacking is a media
       query now, where it can move the rows too. */
    const stacks=[['px-reframe-cols',900],['px-daniel',900],['px-proof',820]];
    stacks.forEach(([id])=>{const g=root.getElementById(id); if(g) g.dataset.cols=g.style.gridTemplateColumns;});
    const layout=()=>stacks.forEach(([id,bp])=>{
      const g=root.getElementById(id); if(!g) return;
      g.style.gridTemplateColumns = window.innerWidth<bp ? '1fr' : g.dataset.cols;
    });
    window.addEventListener('resize',layout,{passive:true});
    layout();
  }

  class ParallaxxHomePage extends HTMLElement {
    connectedCallback(){
      if (this._mounted) return; this._mounted = true;
      addFonts();
      var shadow = this.attachShadow({mode:'open'});
      shadow.innerHTML = '<style>'+CSS+'</style>'+HTML;
      var host = this;
      loadLibs().then(function(){ try{ boot(shadow); }catch(e){ console.error('[px] boot failed:', e); } })
        .catch(function(){ try{ boot(shadow); }catch(e){} });
      requestAnimationFrame(function(){ collapseAncestors(host); });
      [400,1200,2500].forEach(function(t){ setTimeout(function(){ collapseAncestors(host); }, t); });
      window.addEventListener('resize', function(){ collapseAncestors(host); }, {passive:true});
    }
  }
  customElements.define('parallaxx-home-page', ParallaxxHomePage);
})();
