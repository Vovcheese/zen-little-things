"""Build a local UI fixture from installed Zen markup and the current mod CSS.

This approximates XUL in HTML; it is not native browser validation.
Extracted upstream CSS is kept in an ignored generated file.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def native(archive, path):
    result = subprocess.run(['unzip', '-p', '/Applications/Zen.app/Contents/Resources/' + archive, path], capture_output=True)
    if not result.stdout:
        raise RuntimeError(result.stderr.decode())
    return result.stdout.decode()

def mod(name):
    return (ROOT / 'mods' / name / 'chrome.css').read_text().split('@-moz-document url("chrome://browser/content/browser.xhtml") {', 1)[1].rsplit('}', 1)[0]

source = native('omni.ja', 'chrome/toolkit/content/global/elements/findbar.js')
markup = re.search(r'static get markup\(\)\s*\{\s*return `(.*?)`;', source, re.S).group(1)
markup = markup.replace('html:', '')
markup = re.sub(r'<(toolbarbutton|checkbox|label|image|description)(\s[^<>]*?)/>', r'<\1\2></\1>', markup)
markup = markup.replace('disabled="true"', '')
findcss = native('omni.ja', 'chrome/toolkit/skin/classic/global/findbar.css')
findcss = re.sub(r'@namespace[^;]+;', '', findcss).replace('xul|', '').replace('html|', '')
peekcss = native('browser/omni.ja', 'chrome/browser/skin/classic/browser/tabbrowser/tab-hover-preview.css')
base = '''
:root{color-scheme:light;--arrowpanel-background:#fff;--arrowpanel-color:#333b4c;--toolbar-field-background-color:#f4f5f8;--ctp-accent:#7654ac;--border-width:1px;--border-color-deemphasized:#b3b6c1;--border-radius-medium:10px;--space-small:8px;--space-xsmall:4px;--space-medium:8px;--findbar-container-height:28px}
:root.dark{color-scheme:dark;--arrowpanel-background:#2c3040;--arrowpanel-color:#e0e4f2;--toolbar-field-background-color:#242837;--ctp-accent:#c7aced}
*{box-sizing:border-box}body{margin:0;padding:28px;background:light-dark(#efeee9,#202431);color:var(--arrowpanel-color);font:14px/1.5 system-ui}header{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:20px}button{font:inherit;padding:8px 12px;border:1px solid #8885;border-radius:8px;background:var(--arrowpanel-background);color:inherit;cursor:pointer}main{display:flex;gap:32px;align-items:flex-start;flex-wrap:wrap}h2{font-size:17px;margin:0 0 16px}.browserContainer{display:grid;grid-template-areas:'browserstack';width:580px;height:365px;background:light-dark(#fff,#282c3b);border-radius:16px;box-shadow:inset 0 0 0 1px #8883}.page{padding:32px;grid-area:browserstack;color:#888;align-self:end}body.narrow .browserContainer{width:300px}findbar{display:flex}hbox{display:flex}toolbarbutton{display:inline-flex;align-items:center;justify-content:center;cursor:pointer}toolbarbutton svg{width:16px;height:16px;display:block}checkbox{display:flex;align-items:center;cursor:pointer}checkbox input{margin:0;flex-shrink:0}checkbox .checkbox-label-box{display:flex;flex:1}label.findbar-label,description{display:block}#tab-preview-panel{display:block;width:320px}.tab-preview-content-main{display:flex;flex-direction:column}.tab-preview-text-container{display:block}.tab-preview-content-interactive:empty{display:none}canvas{width:100%;height:auto}[hidden]{display:none!important}.note{max-width:860px;color:light-dark(#626877,#adb5ca)}pre{white-space:pre-wrap;font:12px/1.7 ui-monospace;background:#8881;padding:16px;border-radius:10px}
'''
peek = '''<div id="tab-preview-panel" panelopen="true"><div class="tab-preview-content-interactive"></div><div class="tab-preview-content-main"><div class="tab-preview-thumbnail-container"><canvas width="592" height="330"></canvas></div><div class="tab-preview-text-container"><div class="tab-preview-title">Small ideas, clearer browsing</div><div class="tab-preview-uri">example.com</div><div class="tab-preview-container-indicator" hidden>Personal</div></div></div></div>'''
script = r'''
const root=document.documentElement,bar=document.querySelector('findbar'),field=bar.querySelector('input'),panel=document.getElementById('tab-preview-panel');
const shadow=panel.attachShadow({mode:'open'});shadow.innerHTML='<style>:host{display:block}slot{display:flex;flex-direction:column;width:var(--panel-width);border:1px solid var(--panel-border-color);border-radius:var(--panel-border-radius);padding:var(--panel-padding);background:var(--panel-background-color)}</style><slot part="content"></slot>';
const arrow=(d)=>'<svg class="toolbarbutton-icon" viewBox="0 0 16 16" aria-hidden="true"><path d="'+d+'" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
bar.querySelectorAll('toolbarbutton').forEach((b,i)=>{b.innerHTML=arrow(i===0?'M4 10l4-4 4 4':i===1?'M4 6l4 4 4-4':'M4 4l8 8M12 4l-8 8');b.setAttribute('role','button');b.tabIndex=0;b.title=['Previous','Next','Close'][i]});
const labels=['Highlight all','Match case','Match diacritics','Whole words'];
bar.querySelectorAll('checkbox').forEach((c,i)=>{c.innerHTML='<input type="checkbox" aria-label="'+labels[i]+'"><span class="checkbox-label-box"><span class="checkbox-label">'+labels[i]+'</span></span>';c.onclick=e=>{if(e.target.tagName!=='INPUT')c.querySelector('input').click()}});
field.value='ideas';field.setAttribute('aria-label','Find in page');
const count=bar.querySelector('.found-matches');count.removeAttribute('hidden');count.textContent='2 of 8 matches';
const canvas=panel.querySelector('canvas'),ctx=canvas.getContext('2d');ctx.fillStyle='#e9eee7';ctx.fillRect(0,0,592,330);ctx.fillStyle='#bdd2c4';ctx.fillRect(24,24,250,282);ctx.fillStyle='#608578';ctx.beginPath();ctx.moveTo(24,260);ctx.lineTo(128,126);ctx.lineTo(274,280);ctx.lineTo(274,306);ctx.lineTo(24,306);ctx.fill();ctx.fillStyle='#526c60';ctx.fillRect(304,50,240,10);ctx.fillRect(304,72,176,10);ctx.fillStyle='#c7cfc5';for(let y=118;y<250;y+=22)ctx.fillRect(304,y,y%3?230:160,7);
document.getElementById('theme').onclick=()=>root.classList.toggle('dark');
document.getElementById('alpha').onclick=()=>panel.style.setProperty('--zen-peek-background','rgba(110, 120, 150, 0.25)');
document.getElementById('width').onclick=()=>document.body.classList.toggle('narrow');
document.getElementById('missing').onclick=()=>{const error=field.getAttribute('status')!=='notfound';field.setAttribute('status',error?'notfound':'');count.hidden=error;const status=bar.querySelector('.findbar-find-status');status.setAttribute('status',error?'notfound':'');status.textContent=error?'Phrase not found':''};
document.getElementById('long').onclick=()=>{panel.querySelector('.tab-preview-title').textContent='A long page title that should wrap cleanly across three lines without touching the preview frame or pushing the domain outside the card';bar.querySelectorAll('.checkbox-label').forEach((l,i)=>l.textContent=['Подсветить все совпадения','Учитывать регистр','Учитывать диакритические знаки','Только целые слова'][i])};
document.getElementById('thumb').onclick=()=>panel.querySelector('.tab-preview-thumbnail-container').classList.toggle('hide-thumbnail');
document.getElementById('close').onclick=()=>bar.toggleAttribute('hidden');
document.getElementById('rtl').onclick=()=>root.dir=root.dir==='rtl'?'ltr':'rtl';
bar.querySelector('.findbar-closebutton').onclick=()=>bar.hidden=true;
document.getElementById('check').onclick=()=>{
 const lines=[],rect=el=>el.getBoundingClientRect(),visible=el=>el.getClientRects().length>0;
 const controls=[field,...bar.querySelectorAll('toolbarbutton')].filter(visible),bounds=rect(bar),input=rect(field);
 if(!bar.hidden){
  for(const e of controls){const r=rect(e);lines.push((Math.abs(r.top-input.top)<=1&&r.height===36&&r.left>=bounds.left&&r.right<=bounds.right?'PASS':'FAIL')+' aligned: '+(e.title||'input')+' '+Math.round(r.width)+'×'+r.height)}
  for(let i=0;i<controls.length;i++)for(let j=i+1;j<controls.length;j++){const a=rect(controls[i]),b=rect(controls[j]);if(Math.min(a.right,b.right)>Math.max(a.left,b.left)&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top))lines.push('FAIL overlapping controls')}
  for(const e of bar.querySelectorAll('checkbox,.findbar-label'))if(visible(e)){const r=rect(e);lines.push((r.left>=bounds.left&&r.right<=bounds.right?'PASS':'FAIL')+' contained: '+e.textContent)}
 }
 const frame=shadow.querySelector('slot'),shot=panel.querySelector('canvas');
 const surface=getComputedStyle(frame),mainSurface=getComputedStyle(panel.querySelector('.tab-preview-content-main'));
 lines.push((surface.opacity==='1'&&surface.animationName==='none'&&surface.backgroundColor!=='rgba(0, 0, 0, 0)'&&mainSurface.backgroundColor!=='rgba(0, 0, 0, 0)'?'PASS':'FAIL')+' opaque preview base / no whole-card fade');
 lines.push((getComputedStyle(frame).borderTopWidth==='1px'&&getComputedStyle(shot).borderTopWidth==='0px'?'PASS':'FAIL')+' single preview frame / borderless thumbnail');
 lines.push((rect(frame).width<=320?'PASS':'FAIL')+' preview width');
 document.getElementById('results').textContent=lines.join('\n');
};
'''
html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Zen Find + Peek — UI fixture</title><style>'+base+'</style><style>'+findcss+peekcss+'</style><style>'+mod('zen-find')+mod('zen-peek')+'</style><header><strong>UI fixture · Find + Peek 0.2</strong>'+''.join('<button id="'+i+'">'+label+'</button>' for i,label in [('theme','Light / dark'),('alpha','Translucent theme'),('width','Narrow / wide'),('missing','No matches'),('long','Long text'),('thumb','Thumbnail'),('close','Open / close'),('rtl','RTL'),('check','Check layout')])+'</header><main><section><h2>Native search markup / HTML layout</h2><div id="tabbrowser-tabpanels"><div class="browserContainer"><div class="page">Demo article<br>Search for ideas.</div><findbar>'+markup+'</findbar></div></div></section><section><h2>Preview frame / actual CSS part</h2>'+peek+'</section></main><p class="note">HTML fixture using extracted native markup/styles and current mod CSS. XUL controls are approximated. This is not a native Zen UI test.</p><pre id="results">Click Check layout.</pre><script>'+script+'</script></html>'
(ROOT/'tests/ui-preview.html').write_text(html)
