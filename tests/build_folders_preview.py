from pathlib import Path
import re
import subprocess

# Extract native styles/icons from the installed Zen; never write its profile.
def native_file(name):
    archive = "/Applications/Zen.app/Contents/Resources/browser/omni.ja"
    result = subprocess.run(["unzip", "-p", archive, name], capture_output=True)
    if not result.stdout:
        raise RuntimeError(result.stderr.decode())
    return result.stdout.decode()

root=Path(__file__).resolve().parents[1]
source=native_file('chrome/browser/content/browser/zen-components/ZenFolder.mjs')
svg=re.search(r'<svg.*?</svg>',source,re.S).group()
native=native_file('chrome/browser/content/browser/zen-styles/zen-folders.css')
css=(root/'mods/zen-folders/chrome.css').read_text().split('@-moz-document url("chrome://browser/content/browser.xhtml") {',1)[1].rsplit('}',1)[0]
def tab(name,letter,color):
 return f'<tab class="tabbrowser-tab" tabindex="0" title="{name}"><div class="tab-stack"><div class="tab-background"></div><div class="tab-content"><span class="favicon" style="background:{color}">{letter}</span><span class="tab-label">{name}</span></div></div></tab>'
def folder(name,children,closed=False):
 return '<zen-folder '+('collapsed' if closed else '')+'><hbox class="tab-group-label-container" tabindex="0" role="button" title="'+name+'"><div class="tab-group-folder-icon">'+svg+'</div><label class="tab-group-label">'+name+'</label></hbox><div class="tab-group-container">'+children+'</div></zen-folder>'
body=folder('Projects',tab('Documentation','D','#3975c8')+folder('Team',tab('Notes','N','#6e6b9b')+tab('Planning','P','#de9b42'))+folder('Archive',tab('2025','A','#649785'),True))+folder('Design',tab('Mockups','F','#926acd')+folder('Research',tab('Interviews','I','#4888a6')+folder('Sources',tab('Links','L','#649785'),True)),True)+folder('Personal',tab('Reading','R','#da8b64'),True)
base='''
:root {color-scheme:light;--ctp-accent:#8839ef;--zen-primary-color:#8839ef;--zen-colors-primary:#ccd0da;--toolbar-color:#4c4f69;--arrowpanel-color:#4c4f69;--tab-min-width:48px;--tab-min-height:36px;--tab-margin-block:2px;--tab-group-label-padding:4px;--border-radius-medium:8px;--tab-background-color-hover:#ccd0da;--zen-folder-indent:0px}
* {box-sizing:border-box} body {margin:0;background:#eff1f5;color:#4c4f69;font:14px/1.5 system-ui} body.dark{background:#303446;color:#c6d0f5} body.dark #rail{background:#292c3c} header{padding:24px;display:flex;gap:12px;align-items:center} button{font:inherit;padding:8px 14px;border:1px solid #9995;border-radius:8px;background:transparent;color:inherit;cursor:pointer} main{display:flex;gap:28px;margin:0 24px} #rail{width:60px;padding:6px;background:#e6e9ef;flex-shrink:0;border-radius:12px} :root[zen-sidebar-expanded="true"] #rail{width:260px} #tabbrowser-tabs{width:100%} hbox{display:flex;align-items:center} .tab-group-label-container{justify-content:center;position:relative} .tab-group-label{display:block} zen-folder[collapsed]>.tab-group-container{display:none} .tabbrowser-tab{display:block;width:48px;height:40px;position:relative;cursor:pointer;outline-offset:-3px}.tab-stack{position:relative;width:100%;height:100%}.tab-background{position:absolute;inset:4px 0;width:100%;border-radius:8px}.tabbrowser-tab:hover .tab-background{background:#ccd0da}.tabbrowser-tab[selected] .tab-background{background:#fff;box-shadow:0 1px 4px #0002}.tab-content{height:100%;display:flex;align-items:center;justify-content:center;gap:8px;position:relative;pointer-events:none}.favicon{display:grid;place-items:center;width:16px;height:16px;border-radius:4px;font:bold 10px system-ui;color:white}.tab-label{display:none}:root[zen-sidebar-expanded="true"] .tabbrowser-tab{width:auto}:root[zen-sidebar-expanded="true"] .tab-content{justify-content:flex-start;padding:0 12px}:root[zen-sidebar-expanded="true"] .tab-label{display:inline}aside{max-width:650px}#results{white-space:pre-wrap;font:12px/1.6 ui-monospace,monospace;padding:16px;background:#8881;border-radius:8px}
'''
script='''
const root=document.documentElement;
document.querySelectorAll('.tab-group-label-container').forEach(h=>{function toggle(){h.parentElement.toggleAttribute('collapsed');h.setAttribute('aria-expanded',!h.parentElement.hasAttribute('collapsed'));}h.onclick=toggle;h.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle()}}});
document.querySelectorAll('.tabbrowser-tab').forEach(t=>t.onclick=()=>{document.querySelectorAll('tab[selected]').forEach(x=>x.removeAttribute('selected'));t.setAttribute('selected','true')});
document.getElementById('wide').onclick=()=>{root.toggleAttribute('zen-sidebar-expanded');if(root.hasAttribute('zen-sidebar-expanded'))root.setAttribute('zen-sidebar-expanded','true')};
document.getElementById('dark').onclick=()=>{const dark=document.body.classList.toggle('dark');root.style.colorScheme=dark?'dark':'light';root.style.setProperty('--ctp-accent',dark?'#ca9ee6':'#8839ef');root.style.setProperty('--toolbar-color',dark?'#c6d0f5':'#4c4f69');root.style.setProperty('--arrowpanel-color',dark?'#c6d0f5':'#4c4f69')};
document.getElementById('expand').onclick=()=>document.querySelectorAll('zen-folder').forEach(f=>f.removeAttribute('collapsed'));
document.getElementById('check').onclick=()=>{let results=[];const rail=document.getElementById('rail').getBoundingClientRect();for(const h of document.querySelectorAll('.tab-group-label-container')){if(!h.getClientRects().length)continue;const r=h.getBoundingClientRect(),icon=h.querySelector('svg').getBoundingClientRect(),arrow=getComputedStyle(h,'::after'),aLeft=r.right-parseFloat(arrow.right)-8;results.push((r.left>=rail.left&&r.right<=rail.right&&icon.right<aLeft?'PASS':'FAIL')+' '+h.title+': row '+Math.round(r.width)+'×'+Math.round(r.height)+', icon→arrow gap '+Math.round(aLeft-icon.right)+'px');}results.push('Visible folder headings: '+results.length);document.getElementById('results').textContent=results.join('\\n')};
'''
html='<!doctype html><html lang="en"><meta charset="utf-8"><title>Zen Folders — visual fixture</title><style>'+base+'</style><style>'+native+'</style><style>'+css+'</style><header><strong>Zen Folders 0.2 · geometry fixture</strong><button id="wide">Wide sidebar</button><button id="dark">Dark theme</button><button id="expand">Expand all</button><button id="check">Check geometry</button></header><main><div id="rail"><div id="tabbrowser-tabs">'+body+'</div></div><aside><h1>Folders without nested boxes</h1><p>Local fixture: native Zen folder markup, icons, and styles plus the mod CSS. Rows and tabs are approximated in HTML. This does not replace validation of the real Zen sidebar.</p><p>Click folders and tabs to inspect hover, collapse, and selection. Switch between light/dark themes and narrow/wide layouts.</p><pre id="results">Click “Check geometry”.</pre></aside></main><script>'+script+'</script></html>'
(root/'tests/folders-preview.html').write_text(html)
