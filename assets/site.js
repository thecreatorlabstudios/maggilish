// Her / His switch. Remembers the last choice; /men/ always opens on His.
(function(){
  var root=document.documentElement;
  var forced=root.getAttribute('data-force');
  function set(side,save){
    root.setAttribute('data-side',side);
    document.querySelectorAll('.toggle button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.side===side));});
    // Only the visible theme owns #services, so category links scroll correctly.
    document.querySelectorAll('.sec-h[id^="services"]').forEach(function(h){
      var owner=h.closest('.for-her')?'her':'his';
      h.id=owner===side?'services':'services-'+owner;
    });
    var meta=document.querySelector('meta[name="theme-color"]'); if(meta) meta.content=side==='his'?'#151311':'#F5EEE6';
    if(save){try{localStorage.setItem('maggilish-side',side);}catch(e){}}
  }
  var saved=null; try{saved=localStorage.getItem('maggilish-side');}catch(e){}
  set(forced||saved||root.getAttribute('data-side')||'her',false);
  document.addEventListener('click',function(e){
    var b=e.target.closest('.toggle button'); if(!b) return;
    set(b.dataset.side,true);
  });
})();
