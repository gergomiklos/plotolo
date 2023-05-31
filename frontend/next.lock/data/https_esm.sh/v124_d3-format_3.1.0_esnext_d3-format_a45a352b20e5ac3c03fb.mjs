/* esm.sh - esbuild bundle(d3-format@3.1.0) esnext production */
function Z(t){return Math.abs(t=Math.round(t))>=1e21?t.toLocaleString("en").replace(/,/g,""):t.toString(10)}function g(t,r){if((e=(t=r?t.toExponential(r-1):t.toExponential()).indexOf("e"))<0)return null;var e,o=t.slice(0,e);return[o.length>1?o[0]+o.slice(2):o,+t.slice(e+1)]}function h(t){return t=g(Math.abs(t)),t?t[1]:NaN}function q(t,r){return function(e,o){for(var i=e.length,f=[],c=0,s=t[0],w=0;i>0&&s>0&&(w+s+1>o&&(s=Math.max(1,o-w)),f.push(e.substring(i-=s,i+s)),!((w+=s+1)>o));)s=t[c=(c+1)%t.length];return f.reverse().join(r)}}function B(t){return function(r){return r.replace(/[0-9]/g,function(e){return t[+e]})}}var nt=/^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$/i;function b(t){if(!(r=nt.exec(t)))throw new Error("invalid format: "+t);var r;return new D({fill:r[1],align:r[2],sign:r[3],symbol:r[4],zero:r[5],width:r[6],comma:r[7],precision:r[8]&&r[8].slice(1),trim:r[9],type:r[10]})}b.prototype=D.prototype;function D(t){this.fill=t.fill===void 0?" ":t.fill+"",this.align=t.align===void 0?">":t.align+"",this.sign=t.sign===void 0?"-":t.sign+"",this.symbol=t.symbol===void 0?"":t.symbol+"",this.zero=!!t.zero,this.width=t.width===void 0?void 0:+t.width,this.comma=!!t.comma,this.precision=t.precision===void 0?void 0:+t.precision,this.trim=!!t.trim,this.type=t.type===void 0?"":t.type+""}D.prototype.toString=function(){return this.fill+this.align+this.sign+this.symbol+(this.zero?"0":"")+(this.width===void 0?"":Math.max(1,this.width|0))+(this.comma?",":"")+(this.precision===void 0?"":"."+Math.max(0,this.precision|0))+(this.trim?"~":"")+this.type};function H(t){t:for(var r=t.length,e=1,o=-1,i;e<r;++e)switch(t[e]){case".":o=i=e;break;case"0":o===0&&(o=e),i=e;break;default:if(!+t[e])break t;o>0&&(o=0);break}return o>0?t.slice(0,o)+t.slice(i+1):t}var N;function J(t,r){var e=g(t,r);if(!e)return t+"";var o=e[0],i=e[1],f=i-(N=Math.max(-8,Math.min(8,Math.floor(i/3)))*3)+1,c=o.length;return f===c?o:f>c?o+new Array(f-c+1).join("0"):f>0?o.slice(0,f)+"."+o.slice(f):"0."+new Array(1-f).join("0")+g(t,Math.max(0,r+f-1))[0]}function $(t,r){var e=g(t,r);if(!e)return t+"";var o=e[0],i=e[1];return i<0?"0."+new Array(-i).join("0")+o:o.length>i+1?o.slice(0,i+1)+"."+o.slice(i+1):o+new Array(i-o.length+2).join("0")}var T={"%":(t,r)=>(t*100).toFixed(r),b:t=>Math.round(t).toString(2),c:t=>t+"",d:Z,e:(t,r)=>t.toExponential(r),f:(t,r)=>t.toFixed(r),g:(t,r)=>t.toPrecision(r),o:t=>Math.round(t).toString(8),p:(t,r)=>$(t*100,r),r:$,s:J,X:t=>Math.round(t).toString(16).toUpperCase(),x:t=>Math.round(t).toString(16)};function C(t){return t}var K=Array.prototype.map,Q=["y","z","a","f","p","n","\xB5","m","","k","M","G","T","P","E","Z","Y"];function G(t){var r=t.grouping===void 0||t.thousands===void 0?C:q(K.call(t.grouping,Number),t.thousands+""),e=t.currency===void 0?"":t.currency[0]+"",o=t.currency===void 0?"":t.currency[1]+"",i=t.decimal===void 0?".":t.decimal+"",f=t.numerals===void 0?C:B(K.call(t.numerals,String)),c=t.percent===void 0?"%":t.percent+"",s=t.minus===void 0?"\u2212":t.minus+"",w=t.nan===void 0?"NaN":t.nan+"";function R(a){a=b(a);var S=a.fill,P=a.align,d=a.sign,k=a.symbol,y=a.zero,z=a.width,L=a.comma,x=a.precision,X=a.trim,m=a.type;m==="n"?(L=!0,m="g"):T[m]||(x===void 0&&(x=12),X=!0,m="g"),(y||S==="0"&&P==="=")&&(y=!0,S="0",P="=");var v=k==="$"?e:k==="#"&&/[boxX]/.test(m)?"0"+m.toLowerCase():"",tt=k==="$"?o:/[%p]/.test(m)?c:"",O=T[m],rt=/[defgprs%]/.test(m);x=x===void 0?6:/[gprs]/.test(m)?Math.max(1,Math.min(21,x)):Math.max(0,Math.min(20,x));function U(n){var l=v,u=tt,M,Y,A;if(m==="c")u=O(n)+u,n="";else{n=+n;var j=n<0||1/n<0;if(n=isNaN(n)?w:O(Math.abs(n),x),X&&(n=H(n)),j&&+n==0&&d!=="+"&&(j=!1),l=(j?d==="("?d:s:d==="-"||d==="("?"":d)+l,u=(m==="s"?Q[8+N/3]:"")+u+(j&&d==="("?")":""),rt){for(M=-1,Y=n.length;++M<Y;)if(A=n.charCodeAt(M),48>A||A>57){u=(A===46?i+n.slice(M+1):n.slice(M))+u,n=n.slice(0,M);break}}}L&&!y&&(n=r(n,1/0));var E=l.length+n.length+u.length,p=E<z?new Array(z-E+1).join(S):"";switch(L&&y&&(n=r(p+n,p.length?z-u.length:1/0),p=""),P){case"<":n=l+n+u+p;break;case"=":n=l+p+n+u;break;case"^":n=p.slice(0,E=p.length>>1)+l+n+u+p.slice(E);break;default:n=p+l+n+u;break}return f(n)}return U.toString=function(){return a+""},U}function _(a,S){var P=R((a=b(a),a.type="f",a)),d=Math.max(-8,Math.min(8,Math.floor(h(S)/3)))*3,k=Math.pow(10,-d),y=Q[8+d/3];return function(z){return P(k*z)+y}}return{format:R,formatPrefix:_}}var F,V,W;I({thousands:",",grouping:[3],currency:["$",""]});function I(t){return F=G(t),V=F.format,W=F.formatPrefix,F}function ot(t){return Math.max(0,-h(Math.abs(t)))}function et(t,r){return Math.max(0,Math.max(-8,Math.min(8,Math.floor(h(r)/3)))*3-h(Math.abs(t)))}function it(t,r){return t=Math.abs(t),r=Math.abs(r)-t,Math.max(0,h(r)-h(t))+1}export{D as FormatSpecifier,V as format,I as formatDefaultLocale,G as formatLocale,W as formatPrefix,b as formatSpecifier,ot as precisionFixed,et as precisionPrefix,it as precisionRound};
//# sourceMappingURL=d3-format.mjs.map