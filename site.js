(function(){
var page=document.body.dataset.page||'';
var links=[['products.html','Products','products'],['how-it-works.html','How it works','how'],['developers.html','Developers','dev'],['about.html','About','about'],['contact.html','Contact','contact']];
var nav='<nav class="nav" aria-label="Main"><div class="nav-bar"><a class="logo" href="index.html"><img class="mark" src="logo-dark.svg" width="30" height="30" alt="">Relavoi</a><div class="nav-links">'+links.map(function(l){return '<a href="'+l[0]+'" class="'+(l[2]===page?'on':'')+'"'+(l[2]===page?' aria-current="page"':'')+'>'+l[1]+'</a>'}).join('')+'</div><div class="nav-cta"><a href="https://app.relavoi.com/login" class="nav-signin">Sign in</a><a href="https://app.relavoi.com/signup" class="btn btn-p btn-sm">Request pilot access<span class="arr" aria-hidden="true"></span></a></div><button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-sheet" aria-label="Open menu"><i></i><i></i></button><div class="nav-sheet" id="nav-sheet">'+links.map(function(l){return '<a href="'+l[0]+'" class="l'+(l[2]===page?' on':'')+'">'+l[1]+'</a>'}).join('')+'<div class="sheet-cta"><a href="https://app.relavoi.com/login" class="btn btn-s">Sign in</a><a href="https://app.relavoi.com/signup" class="btn btn-p">Request pilot access<span class="arr" aria-hidden="true"></span></a></div></div></div></nav>';
var foot='<footer class="foot"><div class="wrap"><div class="foot-panel"><div class="cols"><div><a class="logo" href="index.html"><img class="mark" src="logo.svg" width="30" height="30" alt="">Relavoi</a><p class="blurb">Privacy-first calling and messaging infrastructure for Nigeria\'s marketplaces.</p><p class="mono loc">Lagos · Nigeria</p></div><div><h4>Products</h4><a href="products.html#voice">Voice masking</a><a href="products.html#sms">SMS masking</a><a href="products.html#sdk">Mobile SDKs</a><a href="products.html#analytics">Analytics</a></div><div><h4>Developers</h4><a href="developers.html">API docs</a><a href="developers.html#sdks">SDKs</a><a href="developers.html#webhooks">Webhooks</a></div><div><h4>Company</h4><a href="about.html">About</a><a href="how-it-works.html">How it works</a><a href="contact.html">Contact</a></div><div><h4>Legal</h4><a href="contact.html">Privacy</a><a href="contact.html">Terms</a><a href="contact.html">NDPR DPA</a><a href="https://docs.relavoi.com/guides/security" target="_blank" rel="noopener">Security</a></div></div><div class="bot"><span>© 2026 Relavoi · <a href=\"https://cicanda.com\" target=\"_blank\" rel=\"noopener\">CICANDA Ltd</a></span><span>NDPR-aligned · Numbers via NCC-licensed carriers</span></div></div></div></footer>';
document.body.insertAdjacentHTML('afterbegin',nav);
document.body.insertAdjacentHTML('beforeend',foot);

var navEl=document.querySelector('.nav'),toggle=navEl.querySelector('.nav-toggle');
function setOpen(open){
  navEl.classList.toggle('open',open);
  toggle.setAttribute('aria-expanded',open);
  toggle.setAttribute('aria-label',open?'Close menu':'Open menu');
  document.documentElement.style.overflow=open?'hidden':'';
}
toggle.addEventListener('click',function(){setOpen(!navEl.classList.contains('open'))});
document.addEventListener('click',function(e){if(navEl.classList.contains('open')&&!navEl.contains(e.target))setOpen(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&navEl.classList.contains('open')){setOpen(false);toggle.focus()}});
Array.prototype.forEach.call(navEl.querySelectorAll('.nav-sheet a'),function(a){a.addEventListener('click',function(){setOpen(false)})});
window.addEventListener('resize',function(){if(window.innerWidth>1024&&navEl.classList.contains('open'))setOpen(false)});

Array.prototype.forEach.call(document.querySelectorAll('[data-tabs]'),function(root,ti){
  var panels=root.querySelectorAll('.tab-panel');
  if(!panels.length)return;
  var bar=document.createElement('div'),tabs=[];
  bar.className='tabs-bar';
  bar.setAttribute('role','tablist');
  bar.setAttribute('aria-label',root.getAttribute('data-tabs'));
  Array.prototype.forEach.call(panels,function(p,i){
    var t=document.createElement('button');
    p.id=p.id||'tp'+ti+'-'+i;
    t.type='button';t.className='tab';t.id=p.id+'-tab';
    t.setAttribute('role','tab');t.setAttribute('aria-controls',p.id);
    t.textContent=p.querySelector('h3').textContent;
    p.setAttribute('role','tabpanel');p.setAttribute('aria-labelledby',t.id);p.tabIndex=0;
    bar.appendChild(t);tabs.push(t);
  });
  function select(i,focus){
    tabs.forEach(function(t,j){var on=i===j;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;panels[j].hidden=!on});
    if(focus)tabs[i].focus();
    var t=tabs[i];
    bar.scrollTo({left:t.offsetLeft-(bar.clientWidth-t.offsetWidth)/2,behavior:'smooth'});
  }
  bar.addEventListener('click',function(e){var t=e.target.closest('.tab');if(t)select(tabs.indexOf(t))});
  bar.addEventListener('keydown',function(e){
    var i=tabs.indexOf(document.activeElement),n=tabs.length,k=e.key;
    var j=k==='ArrowRight'?(i+1)%n:k==='ArrowLeft'?(i-1+n)%n:k==='Home'?0:k==='End'?n-1:-1;
    if(i>=0&&j>=0){e.preventDefault();select(j,true)}
  });
  root.insertBefore(bar,root.firstChild);
  root.classList.add('tabs-ready');
  select(0);
});
})();
