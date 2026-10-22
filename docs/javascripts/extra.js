/* 말풍선, Colab 버튼, 완료 체크를 붙인다 (페이지마다 실행) */
(function(){
  var CREW = {doc:["박사","박","doc_explain"], asst:["세라","세","asst_why"], fly:["초파리","초","fly_doubt"], robo:["Money-Robo","R","robo_idle"]};
  var ALIASES = {doc_explain:"doc_smile",doc_judge:"doc_smile",doc_think:"doc_smile",doc_spark:"doc_smile",
    asst_why:"asst_smile",asst_ledger:"asst_smile",asst_sweat:"asst_smile",asst_spark:"asst_smile",
    fly_doubt:"fly_point",fly_magnify:"fly_point",fly_arms:"fly_point",fly_coffee:"fly_point",
    robo_thinking:"robo_idle",robo_confused:"robo_thinking",robo_wrong:"robo_idle",robo_success:"robo_idle"};
  var KEY = "lpbd-done";

  function base(){ var a=document.querySelector('link[rel="icon"]'); /* site 루트 찾기 */
    var s=document.querySelector('script[src*="javascripts/extra.js"]'); return s? s.src.replace(/javascripts\/extra\.js.*$/,"") : "/"; }
  function charImg(av, key){
    var im=document.createElement("img"); im.alt=""; im.setAttribute("aria-hidden","true"); var tried=[key];
    im.onerror=function(){ var nx=ALIASES[tried[tried.length-1]]; if(nx && tried.indexOf(nx)<0){ tried.push(nx); im.src=base()+"assets/chars/"+nx+".png"; } else im.remove(); };
    im.src=base()+"assets/chars/"+key+".png"; av.appendChild(im);
  }
  function says(){
    document.querySelectorAll(".say:not(.ready)").forEach(function(d){
      var who=CREW[d.dataset.who]||CREW.asst, st=d.dataset.state;
      var key=d.dataset.face || (d.dataset.who==="robo" ? "robo_"+(st||"idle") : who[2]);
      var av=document.createElement("span"); av.className="av"; av.textContent=who[1]; charImg(av,key);
      if(d.classList.contains("only")){ d.innerHTML=""; d.appendChild(av); d.classList.add("ready"); return; }
      var b=document.createElement("div"); b.className="bubble"; b.innerHTML='<span class="who">'+who[0]+"</span>"+d.innerHTML;
      d.innerHTML=""; d.appendChild(av); d.appendChild(b); d.classList.add("ready");
    });
  }
  function colab(){
    var src=document.querySelector("a.md-source"), m=src && src.href.match(/github\.com\/([^\/]+)\/([^\/?#]+)/);
    document.querySelectorAll("a.colab[data-nb]").forEach(function(a){
      if(m && m[1]!=="USER") a.href="https://colab.research.google.com/github/"+m[1]+"/"+m[2]+"/blob/main/docs/notebooks/"+a.dataset.nb;
      else a.href=base()+"notebooks/"+a.dataset.nb;   /* repo 주소를 아직 안 바꿨으면 파일 내려받기 */
      a.target="_blank"; a.rel="noopener";
    });
  }
  function load(){ try{ return JSON.parse(localStorage.getItem(KEY)||"{}")||{}; }catch(e){ return {}; } }
  function save(d){ try{ localStorage.setItem(KEY, JSON.stringify(d)); }catch(e){} }
  function done(){
    var d=load();
    document.querySelectorAll("label.done input[data-step]").forEach(function(b){
      b.checked=!!d[b.dataset.step]; b.parentNode.classList.toggle("on",b.checked);
      b.onchange=function(){ var x=load(); x[b.dataset.step]=b.checked; save(x); b.parentNode.classList.toggle("on",b.checked); marknav(); };
    });
    marknav();
  }
  function marknav(){
    var d=load();
    document.querySelectorAll(".md-nav__link").forEach(function(a){
      var m=(a.textContent||"").trim().match(/^(\d-\d+)\s/); if(m) a.classList.toggle("is-done", !!d[m[1]]);
    });
  }
  function run(){ says(); colab(); done(); }
  if (window.document$ && document$.subscribe) document$.subscribe(run);
  else document.addEventListener("DOMContentLoaded", run);
})();
