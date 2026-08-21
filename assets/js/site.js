(function(){
  'use strict';
  var d=document;

  /* sticky header gölgesi + "Uzmana Danış" rozetinin görünürlüğü */
  var hdr=d.querySelector('.ye-hdr'), ask=d.querySelector('.ye-ask');
  var onScroll=function(){
    var y=window.scrollY;
    if(hdr) hdr.classList.toggle('is-stuck', y>8);
    if(ask) ask.classList.toggle('is-on', y>240);
  };
  onScroll(); window.addEventListener('scroll',onScroll,{passive:true});

  /* mobil menü */
  var burger=d.querySelector('.ye-burger'), nav=d.querySelector('.ye-nav'), ovl=d.querySelector('.ye-ovl');
  function closeNav(){ if(!nav)return; nav.classList.remove('is-open'); if(ovl)ovl.classList.remove('is-on');
    if(burger)burger.setAttribute('aria-expanded','false'); d.body.style.overflow='';
    d.body.classList.remove('ye-menu'); }
  if(burger&&nav){
    burger.addEventListener('click',function(){
      var open=nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded',open?'true':'false');
      if(ovl)ovl.classList.toggle('is-on',open);
      d.body.style.overflow=open?'hidden':'';
      d.body.classList.toggle('ye-menu',open);
    });
  }
  if(ovl)ovl.addEventListener('click',closeNav);
  if(nav){
    nav.addEventListener('click',function(e){
      var a=e.target.closest && e.target.closest('a[href]');
      if(a && !a.parentElement.querySelector(':scope > .ye-sub')) closeNav();
    });
  }
  d.addEventListener('keydown',function(e){ if(e.key==='Escape')closeNav(); });

  /* mobilde alt menü aç/kapa */
  Array.prototype.forEach.call(d.querySelectorAll('.ye-nav > li'),function(li){
    var a=li.querySelector(':scope > a'), sub=li.querySelector(':scope > .ye-sub');
    if(!sub||!a)return;
    a.addEventListener('click',function(e){
      if(window.matchMedia('(max-width:1024px)').matches){ e.preventDefault(); li.classList.toggle('is-open'); }
    });
  });

  /* scroll reveal — transform SINIFTA, inline stil verilmiyor */
  var rv=d.querySelectorAll('.ye-rv');
  if(rv.length){
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(en){
        en.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add('is-in'); io.unobserve(x.target); } });
      },{rootMargin:'0px 0px -8% 0px',threshold:.06});
      Array.prototype.forEach.call(rv,function(el){ io.observe(el); });
    } else {
      Array.prototype.forEach.call(rv,function(el){ el.classList.add('is-in'); });
    }
  }

  /* haritalar: görünür olunca yükle (LCP korunur) */
  var maps=d.querySelectorAll('[data-map]');
  if(maps.length){
    var load=function(box){
      if(box.dataset.done)return; box.dataset.done='1';
      var f=d.createElement('iframe');
      f.src=box.getAttribute('data-map');
      f.title=box.getAttribute('data-title')||'Konum haritası';
      f.loading='lazy'; f.referrerPolicy='strict-origin-when-cross-origin';
      f.setAttribute('allowfullscreen',''); f.style.border='0';
      box.appendChild(f);
    };
    if('IntersectionObserver' in window){
      var mio=new IntersectionObserver(function(en){
        en.forEach(function(x){ if(x.isIntersecting){ load(x.target); mio.unobserve(x.target); } });
      },{rootMargin:'320px'});
      Array.prototype.forEach.call(maps,function(m){ mio.observe(m); });
    } else { Array.prototype.forEach.call(maps,load); }
  }

  /* aynı anda tek SSS açık kalsın (isteğe bağlı, gruplu) */
  Array.prototype.forEach.call(d.querySelectorAll('.ye-faq'),function(g){
    var ds=g.querySelectorAll('details');
    Array.prototype.forEach.call(ds,function(x){
      x.addEventListener('toggle',function(){
        if(x.open) Array.prototype.forEach.call(ds,function(y){ if(y!==x)y.open=false; });
      });
    });
  });
})();
