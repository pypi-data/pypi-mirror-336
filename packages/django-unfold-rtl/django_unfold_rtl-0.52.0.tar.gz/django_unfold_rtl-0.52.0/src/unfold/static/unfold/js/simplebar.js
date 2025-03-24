/**
 * simplebar - v6.2.6
 * Scrollbars, simpler.
 * https://grsmto.github.io/simplebar/
 *
 * Made by Adrien Denat from a fork by Jonathan Nicol
 * Under MIT License
 */

var SimpleBar=function(){"use strict";var t=function(e,i){return t=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var i in e)Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i])},t(e,i)};var e=!("undefined"==typeof window||!window.document||!window.document.createElement),i="object"==typeof global&&global&&global.Object===Object&&global,s="object"==typeof self&&self&&self.Object===Object&&self,r=i||s||Function("return this")(),l=r.Symbol,o=Object.prototype,n=o.hasOwnProperty,a=o.toString,c=l?l.toStringTag:void 0;var h=Object.prototype.toString;var u=l?l.toStringTag:void 0;function d(t){return null==t?void 0===t?"[object Undefined]":"[object Null]":u&&u in Object(t)?function(t){var e=n.call(t,c),i=t[c];try{t[c]=void 0;var s=!0}catch(t){}var r=a.call(t);return s&&(e?t[c]=i:delete t[c]),r}(t):function(t){return h.call(t)}(t)}var p=/\s/;var v=/^\s+/;function f(t){return t?t.slice(0,function(t){for(var e=t.length;e--&&p.test(t.charAt(e)););return e}(t)+1).replace(v,""):t}function m(t){var e=typeof t;return null!=t&&("object"==e||"function"==e)}var b=/^[-+]0x[0-9a-f]+$/i,g=/^0b[01]+$/i,x=/^0o[0-7]+$/i,y=parseInt;function E(t){if("number"==typeof t)return t;if(function(t){return"symbol"==typeof t||function(t){return null!=t&&"object"==typeof t}(t)&&"[object Symbol]"==d(t)}(t))return NaN;if(m(t)){var e="function"==typeof t.valueOf?t.valueOf():t;t=m(e)?e+"":e}if("string"!=typeof t)return 0===t?t:+t;t=f(t);var i=g.test(t);return i||x.test(t)?y(t.slice(2),i?2:8):b.test(t)?NaN:+t}var O=function(){return r.Date.now()},w=Math.max,S=Math.min;function A(t,e,i){var s,r,l,o,n,a,c=0,h=!1,u=!1,d=!0;if("function"!=typeof t)throw new TypeError("Expected a function");function p(e){var i=s,l=r;return s=r=void 0,c=e,o=t.apply(l,i)}function v(t){return c=t,n=setTimeout(b,e),h?p(t):o}function f(t){var i=t-a;return void 0===a||i>=e||i<0||u&&t-c>=l}function b(){var t=O();if(f(t))return g(t);n=setTimeout(b,function(t){var i=e-(t-a);return u?S(i,l-(t-c)):i}(t))}function g(t){return n=void 0,d&&s?p(t):(s=r=void 0,o)}function x(){var t=O(),i=f(t);if(s=arguments,r=this,a=t,i){if(void 0===n)return v(a);if(u)return clearTimeout(n),n=setTimeout(b,e),p(a)}return void 0===n&&(n=setTimeout(b,e)),o}return e=E(e)||0,m(i)&&(h=!!i.leading,l=(u="maxWait"in i)?w(E(i.maxWait)||0,e):l,d="trailing"in i?!!i.trailing:d),x.cancel=function(){void 0!==n&&clearTimeout(n),c=0,s=a=r=n=void 0},x.flush=function(){return void 0===n?o:g(O())},x}var k=function(){return k=Object.assign||function(t){for(var e,i=1,s=arguments.length;i<s;i++)for(var r in e=arguments[i])Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t},k.apply(this,arguments)},W=null,M=null;function N(){if(null===W){if("undefined"==typeof document)return W=0;var t=document.body,e=document.createElement("div");e.classList.add("simplebar-hide-scrollbar"),t.appendChild(e);var i=e.getBoundingClientRect().right;t.removeChild(e),W=i}return W}function L(t){return t&&t.ownerDocument&&t.ownerDocument.defaultView?t.ownerDocument.defaultView:window}function z(t){return t&&t.ownerDocument?t.ownerDocument:document}e&&window.addEventListener("resize",(function(){M!==window.devicePixelRatio&&(M=window.devicePixelRatio,W=null)}));var C=function(t){return Array.prototype.reduce.call(t,(function(t,e){var i=e.name.match(/data-simplebar-(.+)/);if(i){var s=i[1].replace(/\W+(.)/g,(function(t,e){return e.toUpperCase()}));switch(e.value){case"true":t[s]=!0;break;case"false":t[s]=!1;break;case void 0:t[s]=!0;break;default:t[s]=e.value}}return t}),{})};function T(t,e){var i;t&&(i=t.classList).add.apply(i,e.split(" "))}function D(t,e){t&&e.split(" ").forEach((function(e){t.classList.remove(e)}))}function R(t){return".".concat(t.split(" ").join("."))}var V=Object.freeze({__proto__:null,addClasses:T,classNamesToQuery:R,getElementDocument:z,getElementWindow:L,getOptions:C,removeClasses:D}),H=L,j=z,B=C,_=T,q=D,P=R,X=function(){function t(e,i){void 0===i&&(i={});var s=this;if(this.removePreventClickId=null,this.minScrollbarWidth=20,this.stopScrollDelay=175,this.isScrolling=!1,this.isMouseEntering=!1,this.isDragging=!1,this.scrollXTicking=!1,this.scrollYTicking=!1,this.wrapperEl=null,this.contentWrapperEl=null,this.contentEl=null,this.offsetEl=null,this.maskEl=null,this.placeholderEl=null,this.heightAutoObserverWrapperEl=null,this.heightAutoObserverEl=null,this.rtlHelpers=null,this.scrollbarWidth=0,this.resizeObserver=null,this.mutationObserver=null,this.elStyles=null,this.isRtl=null,this.mouseX=0,this.mouseY=0,this.onMouseMove=function(){},this.onWindowResize=function(){},this.onStopScrolling=function(){},this.onMouseEntered=function(){},this.onScroll=function(){var t=H(s.el);s.scrollXTicking||(t.requestAnimationFrame(s.scrollX),s.scrollXTicking=!0),s.scrollYTicking||(t.requestAnimationFrame(s.scrollY),s.scrollYTicking=!0),s.isScrolling||(s.isScrolling=!0,_(s.el,s.classNames.scrolling)),s.showScrollbar("x"),s.showScrollbar("y"),s.onStopScrolling()},this.scrollX=function(){s.axis.x.isOverflowing&&s.positionScrollbar("x"),s.scrollXTicking=!1},this.scrollY=function(){s.axis.y.isOverflowing&&s.positionScrollbar("y"),s.scrollYTicking=!1},this._onStopScrolling=function(){q(s.el,s.classNames.scrolling),s.options.autoHide&&(s.hideScrollbar("x"),s.hideScrollbar("y")),s.isScrolling=!1},this.onMouseEnter=function(){s.isMouseEntering||(_(s.el,s.classNames.mouseEntered),s.showScrollbar("x"),s.showScrollbar("y"),s.isMouseEntering=!0),s.onMouseEntered()},this._onMouseEntered=function(){q(s.el,s.classNames.mouseEntered),s.options.autoHide&&(s.hideScrollbar("x"),s.hideScrollbar("y")),s.isMouseEntering=!1},this._onMouseMove=function(t){s.mouseX=t.clientX,s.mouseY=t.clientY,(s.axis.x.isOverflowing||s.axis.x.forceVisible)&&s.onMouseMoveForAxis("x"),(s.axis.y.isOverflowing||s.axis.y.forceVisible)&&s.onMouseMoveForAxis("y")},this.onMouseLeave=function(){s.onMouseMove.cancel(),(s.axis.x.isOverflowing||s.axis.x.forceVisible)&&s.onMouseLeaveForAxis("x"),(s.axis.y.isOverflowing||s.axis.y.forceVisible)&&s.onMouseLeaveForAxis("y"),s.mouseX=-1,s.mouseY=-1},this._onWindowResize=function(){s.scrollbarWidth=s.getScrollbarWidth(),s.hideNativeScrollbar()},this.onPointerEvent=function(t){var e,i;s.axis.x.track.el&&s.axis.y.track.el&&s.axis.x.scrollbar.el&&s.axis.y.scrollbar.el&&(s.axis.x.track.rect=s.axis.x.track.el.getBoundingClientRect(),s.axis.y.track.rect=s.axis.y.track.el.getBoundingClientRect(),(s.axis.x.isOverflowing||s.axis.x.forceVisible)&&(e=s.isWithinBounds(s.axis.x.track.rect)),(s.axis.y.isOverflowing||s.axis.y.forceVisible)&&(i=s.isWithinBounds(s.axis.y.track.rect)),(e||i)&&(t.stopPropagation(),"pointerdown"===t.type&&"touch"!==t.pointerType&&(e&&(s.axis.x.scrollbar.rect=s.axis.x.scrollbar.el.getBoundingClientRect(),s.isWithinBounds(s.axis.x.scrollbar.rect)?s.onDragStart(t,"x"):s.onTrackClick(t,"x")),i&&(s.axis.y.scrollbar.rect=s.axis.y.scrollbar.el.getBoundingClientRect(),s.isWithinBounds(s.axis.y.scrollbar.rect)?s.onDragStart(t,"y"):s.onTrackClick(t,"y")))))},this.drag=function(e){var i,r,l,o,n,a,c,h,u,d,p;if(s.draggedAxis&&s.contentWrapperEl){var v=s.axis[s.draggedAxis].track,f=null!==(r=null===(i=v.rect)||void 0===i?void 0:i[s.axis[s.draggedAxis].sizeAttr])&&void 0!==r?r:0,m=s.axis[s.draggedAxis].scrollbar,b=null!==(o=null===(l=s.contentWrapperEl)||void 0===l?void 0:l[s.axis[s.draggedAxis].scrollSizeAttr])&&void 0!==o?o:0,g=parseInt(null!==(a=null===(n=s.elStyles)||void 0===n?void 0:n[s.axis[s.draggedAxis].sizeAttr])&&void 0!==a?a:"0px",10);e.preventDefault(),e.stopPropagation();var x=("y"===s.draggedAxis?e.pageY:e.pageX)-(null!==(h=null===(c=v.rect)||void 0===c?void 0:c[s.axis[s.draggedAxis].offsetAttr])&&void 0!==h?h:0)-s.axis[s.draggedAxis].dragOffset,y=(x="x"===s.draggedAxis&&s.isRtl?(null!==(d=null===(u=v.rect)||void 0===u?void 0:u[s.axis[s.draggedAxis].sizeAttr])&&void 0!==d?d:0)-m.size-x:x)/(f-m.size)*(b-g);"x"===s.draggedAxis&&s.isRtl&&(y=(null===(p=t.getRtlHelpers())||void 0===p?void 0:p.isScrollingToNegative)?-y:y),s.contentWrapperEl[s.axis[s.draggedAxis].scrollOffsetAttr]=y}},this.onEndDrag=function(t){s.isDragging=!1;var e=j(s.el),i=H(s.el);t.preventDefault(),t.stopPropagation(),q(s.el,s.classNames.dragging),s.onStopScrolling(),e.removeEventListener("mousemove",s.drag,!0),e.removeEventListener("mouseup",s.onEndDrag,!0),s.removePreventClickId=i.setTimeout((function(){e.removeEventListener("click",s.preventClick,!0),e.removeEventListener("dblclick",s.preventClick,!0),s.removePreventClickId=null}))},this.preventClick=function(t){t.preventDefault(),t.stopPropagation()},this.el=e,this.options=k(k({},t.defaultOptions),i),this.classNames=k(k({},t.defaultOptions.classNames),i.classNames),this.axis={x:{scrollOffsetAttr:"scrollLeft",sizeAttr:"width",scrollSizeAttr:"scrollWidth",offsetSizeAttr:"offsetWidth",offsetAttr:"left",overflowAttr:"overflowX",dragOffset:0,isOverflowing:!0,forceVisible:!1,track:{size:null,el:null,rect:null,isVisible:!1},scrollbar:{size:null,el:null,rect:null,isVisible:!1}},y:{scrollOffsetAttr:"scrollTop",sizeAttr:"height",scrollSizeAttr:"scrollHeight",offsetSizeAttr:"offsetHeight",offsetAttr:"top",overflowAttr:"overflowY",dragOffset:0,isOverflowing:!0,forceVisible:!1,track:{size:null,el:null,rect:null,isVisible:!1},scrollbar:{size:null,el:null,rect:null,isVisible:!1}}},"object"!=typeof this.el||!this.el.nodeName)throw new Error("Argument passed to SimpleBar must be an HTML element instead of ".concat(this.el));this.onMouseMove=function(t,e,i){var s=!0,r=!0;if("function"!=typeof t)throw new TypeError("Expected a function");return m(i)&&(s="leading"in i?!!i.leading:s,r="trailing"in i?!!i.trailing:r),A(t,e,{leading:s,maxWait:e,trailing:r})}(this._onMouseMove,64),this.onWindowResize=A(this._onWindowResize,64,{leading:!0}),this.onStopScrolling=A(this._onStopScrolling,this.stopScrollDelay),this.onMouseEntered=A(this._onMouseEntered,this.stopScrollDelay),this.init()}return t.getRtlHelpers=function(){if(t.rtlHelpers)return t.rtlHelpers;var e=document.createElement("div");e.innerHTML='<div class="simplebar-dummy-scrollbar-size"><div></div></div>';var i=e.firstElementChild,s=null==i?void 0:i.firstElementChild;if(!s)return null;document.body.appendChild(i),i.scrollLeft=0;var r=t.getOffset(i),l=t.getOffset(s);i.scrollLeft=-999;var o=t.getOffset(s);return document.body.removeChild(i),t.rtlHelpers={isScrollOriginAtZero:r.left!==l.left,isScrollingToNegative:l.left!==o.left},t.rtlHelpers},t.prototype.getScrollbarWidth=function(){try{return this.contentWrapperEl&&"none"===getComputedStyle(this.contentWrapperEl,"::-webkit-scrollbar").display||"scrollbarWidth"in document.documentElement.style||"-ms-overflow-style"in document.documentElement.style?0:N()}catch(t){return N()}},t.getOffset=function(t){var e=t.getBoundingClientRect(),i=j(t),s=H(t);return{top:e.top+(s.pageYOffset||i.documentElement.scrollTop),left:e.left+(s.pageXOffset||i.documentElement.scrollLeft)}},t.prototype.init=function(){e&&(this.initDOM(),this.rtlHelpers=t.getRtlHelpers(),this.scrollbarWidth=this.getScrollbarWidth(),this.recalculate(),this.initListeners())},t.prototype.initDOM=function(){var t,e;this.wrapperEl=this.el.querySelector(P(this.classNames.wrapper)),this.contentWrapperEl=this.options.scrollableNode||this.el.querySelector(P(this.classNames.contentWrapper)),this.contentEl=this.options.contentNode||this.el.querySelector(P(this.classNames.contentEl)),this.offsetEl=this.el.querySelector(P(this.classNames.offset)),this.maskEl=this.el.querySelector(P(this.classNames.mask)),this.placeholderEl=this.findChild(this.wrapperEl,P(this.classNames.placeholder)),this.heightAutoObserverWrapperEl=this.el.querySelector(P(this.classNames.heightAutoObserverWrapperEl)),this.heightAutoObserverEl=this.el.querySelector(P(this.classNames.heightAutoObserverEl)),this.axis.x.track.el=this.findChild(this.el,"".concat(P(this.classNames.track)).concat(P(this.classNames.horizontal))),this.axis.y.track.el=this.findChild(this.el,"".concat(P(this.classNames.track)).concat(P(this.classNames.vertical))),this.axis.x.scrollbar.el=(null===(t=this.axis.x.track.el)||void 0===t?void 0:t.querySelector(P(this.classNames.scrollbar)))||null,this.axis.y.scrollbar.el=(null===(e=this.axis.y.track.el)||void 0===e?void 0:e.querySelector(P(this.classNames.scrollbar)))||null,this.options.autoHide||(_(this.axis.x.scrollbar.el,this.classNames.visible),_(this.axis.y.scrollbar.el,this.classNames.visible))},t.prototype.initListeners=function(){var t,e=this,i=H(this.el);if(this.el.addEventListener("mouseenter",this.onMouseEnter),this.el.addEventListener("pointerdown",this.onPointerEvent,!0),this.el.addEventListener("mousemove",this.onMouseMove),this.el.addEventListener("mouseleave",this.onMouseLeave),null===(t=this.contentWrapperEl)||void 0===t||t.addEventListener("scroll",this.onScroll),i.addEventListener("resize",this.onWindowResize),this.contentEl){if(window.ResizeObserver){var s=!1,r=i.ResizeObserver||ResizeObserver;this.resizeObserver=new r((function(){s&&i.requestAnimationFrame((function(){e.recalculate()}))})),this.resizeObserver.observe(this.el),this.resizeObserver.observe(this.contentEl),i.requestAnimationFrame((function(){s=!0}))}this.mutationObserver=new i.MutationObserver((function(){i.requestAnimationFrame((function(){e.recalculate()}))})),this.mutationObserver.observe(this.contentEl,{childList:!0,subtree:!0,characterData:!0})}},t.prototype.recalculate=function(){if(this.heightAutoObserverEl&&this.contentEl&&this.contentWrapperEl&&this.wrapperEl&&this.placeholderEl){var t=H(this.el);this.elStyles=t.getComputedStyle(this.el),this.isRtl="rtl"===this.elStyles.direction;var e=this.contentEl.offsetWidth,i=this.heightAutoObserverEl.offsetHeight<=1,s=this.heightAutoObserverEl.offsetWidth<=1||e>0,r=this.contentWrapperEl.offsetWidth,l=this.elStyles.overflowX,o=this.elStyles.overflowY;this.contentEl.style.padding="".concat(this.elStyles.paddingTop," ").concat(this.elStyles.paddingRight," ").concat(this.elStyles.paddingBottom," ").concat(this.elStyles.paddingLeft),this.wrapperEl.style.margin="-".concat(this.elStyles.paddingTop," -").concat(this.elStyles.paddingRight," -").concat(this.elStyles.paddingBottom," -").concat(this.elStyles.paddingLeft);var n=this.contentEl.scrollHeight,a=this.contentEl.scrollWidth;this.contentWrapperEl.style.height=i?"auto":"100%",this.placeholderEl.style.width=s?"".concat(e||a,"px"):"auto",this.placeholderEl.style.height="".concat(n,"px");var c=this.contentWrapperEl.offsetHeight;this.axis.x.isOverflowing=0!==e&&a>e,this.axis.y.isOverflowing=n>c,this.axis.x.isOverflowing="hidden"!==l&&this.axis.x.isOverflowing,this.axis.y.isOverflowing="hidden"!==o&&this.axis.y.isOverflowing,this.axis.x.forceVisible="x"===this.options.forceVisible||!0===this.options.forceVisible,this.axis.y.forceVisible="y"===this.options.forceVisible||!0===this.options.forceVisible,this.hideNativeScrollbar();var h=this.axis.x.isOverflowing?this.scrollbarWidth:0,u=this.axis.y.isOverflowing?this.scrollbarWidth:0;this.axis.x.isOverflowing=this.axis.x.isOverflowing&&a>r-u,this.axis.y.isOverflowing=this.axis.y.isOverflowing&&n>c-h,this.axis.x.scrollbar.size=this.getScrollbarSize("x"),this.axis.y.scrollbar.size=this.getScrollbarSize("y"),this.axis.x.scrollbar.el&&(this.axis.x.scrollbar.el.style.width="".concat(this.axis.x.scrollbar.size,"px")),this.axis.y.scrollbar.el&&(this.axis.y.scrollbar.el.style.height="".concat(this.axis.y.scrollbar.size,"px")),this.positionScrollbar("x"),this.positionScrollbar("y"),this.toggleTrackVisibility("x"),this.toggleTrackVisibility("y")}},t.prototype.getScrollbarSize=function(t){var e,i;if(void 0===t&&(t="y"),!this.axis[t].isOverflowing||!this.contentEl)return 0;var s,r=this.contentEl[this.axis[t].scrollSizeAttr],l=null!==(i=null===(e=this.axis[t].track.el)||void 0===e?void 0:e[this.axis[t].offsetSizeAttr])&&void 0!==i?i:0,o=l/r;return s=Math.max(~~(o*l),this.options.scrollbarMinSize),this.options.scrollbarMaxSize&&(s=Math.min(s,this.options.scrollbarMaxSize)),s},t.prototype.positionScrollbar=function(e){var i,s,r;void 0===e&&(e="y");var l=this.axis[e].scrollbar;if(this.axis[e].isOverflowing&&this.contentWrapperEl&&l.el&&this.elStyles){var o=this.contentWrapperEl[this.axis[e].scrollSizeAttr],n=(null===(i=this.axis[e].track.el)||void 0===i?void 0:i[this.axis[e].offsetSizeAttr])||0,a=parseInt(this.elStyles[this.axis[e].sizeAttr],10),c=this.contentWrapperEl[this.axis[e].scrollOffsetAttr];c="x"===e&&this.isRtl&&(null===(s=t.getRtlHelpers())||void 0===s?void 0:s.isScrollOriginAtZero)?-c:c,"x"===e&&this.isRtl&&(c=(null===(r=t.getRtlHelpers())||void 0===r?void 0:r.isScrollingToNegative)?c:-c);var h=c/(o-a),u=~~((n-l.size)*h);u="x"===e&&this.isRtl?-u+(n-l.size):u,l.el.style.transform="x"===e?"translate3d(".concat(u,"px, 0, 0)"):"translate3d(0, ".concat(u,"px, 0)")}},t.prototype.toggleTrackVisibility=function(t){void 0===t&&(t="y");var e=this.axis[t].track.el,i=this.axis[t].scrollbar.el;e&&i&&this.contentWrapperEl&&(this.axis[t].isOverflowing||this.axis[t].forceVisible?(e.style.visibility="visible",this.contentWrapperEl.style[this.axis[t].overflowAttr]="scroll",this.el.classList.add("".concat(this.classNames.scrollable,"-").concat(t))):(e.style.visibility="hidden",this.contentWrapperEl.style[this.axis[t].overflowAttr]="hidden",this.el.classList.remove("".concat(this.classNames.scrollable,"-").concat(t))),this.axis[t].isOverflowing?i.style.display="block":i.style.display="none")},t.prototype.showScrollbar=function(t){void 0===t&&(t="y"),this.axis[t].isOverflowing&&!this.axis[t].scrollbar.isVisible&&(_(this.axis[t].scrollbar.el,this.classNames.visible),this.axis[t].scrollbar.isVisible=!0)},t.prototype.hideScrollbar=function(t){void 0===t&&(t="y"),this.isDragging||this.axis[t].isOverflowing&&this.axis[t].scrollbar.isVisible&&(q(this.axis[t].scrollbar.el,this.classNames.visible),this.axis[t].scrollbar.isVisible=!1)},t.prototype.hideNativeScrollbar=function(){this.offsetEl&&(this.offsetEl.style[this.isRtl?"left":"right"]=this.axis.y.isOverflowing||this.axis.y.forceVisible?"-".concat(this.scrollbarWidth,"px"):"0px",this.offsetEl.style.bottom=this.axis.x.isOverflowing||this.axis.x.forceVisible?"-".concat(this.scrollbarWidth,"px"):"0px")},t.prototype.onMouseMoveForAxis=function(t){void 0===t&&(t="y");var e=this.axis[t];e.track.el&&e.scrollbar.el&&(e.track.rect=e.track.el.getBoundingClientRect(),e.scrollbar.rect=e.scrollbar.el.getBoundingClientRect(),this.isWithinBounds(e.track.rect)?(this.showScrollbar(t),_(e.track.el,this.classNames.hover),this.isWithinBounds(e.scrollbar.rect)?_(e.scrollbar.el,this.classNames.hover):q(e.scrollbar.el,this.classNames.hover)):(q(e.track.el,this.classNames.hover),this.options.autoHide&&this.hideScrollbar(t)))},t.prototype.onMouseLeaveForAxis=function(t){void 0===t&&(t="y"),q(this.axis[t].track.el,this.classNames.hover),q(this.axis[t].scrollbar.el,this.classNames.hover),this.options.autoHide&&this.hideScrollbar(t)},t.prototype.onDragStart=function(t,e){var i;void 0===e&&(e="y"),this.isDragging=!0;var s=j(this.el),r=H(this.el),l=this.axis[e].scrollbar,o="y"===e?t.pageY:t.pageX;this.axis[e].dragOffset=o-((null===(i=l.rect)||void 0===i?void 0:i[this.axis[e].offsetAttr])||0),this.draggedAxis=e,_(this.el,this.classNames.dragging),s.addEventListener("mousemove",this.drag,!0),s.addEventListener("mouseup",this.onEndDrag,!0),null===this.removePreventClickId?(s.addEventListener("click",this.preventClick,!0),s.addEventListener("dblclick",this.preventClick,!0)):(r.clearTimeout(this.removePreventClickId),this.removePreventClickId=null)},t.prototype.onTrackClick=function(t,e){var i,s,r,l,o=this;void 0===e&&(e="y");var n=this.axis[e];if(this.options.clickOnTrack&&n.scrollbar.el&&this.contentWrapperEl){t.preventDefault();var a=H(this.el);this.axis[e].scrollbar.rect=n.scrollbar.el.getBoundingClientRect();var c=null!==(s=null===(i=this.axis[e].scrollbar.rect)||void 0===i?void 0:i[this.axis[e].offsetAttr])&&void 0!==s?s:0,h=parseInt(null!==(l=null===(r=this.elStyles)||void 0===r?void 0:r[this.axis[e].sizeAttr])&&void 0!==l?l:"0px",10),u=this.contentWrapperEl[this.axis[e].scrollOffsetAttr],d=("y"===e?this.mouseY-c:this.mouseX-c)<0?-1:1,p=-1===d?u-h:u+h,v=function(){o.contentWrapperEl&&(-1===d?u>p&&(u-=40,o.contentWrapperEl[o.axis[e].scrollOffsetAttr]=u,a.requestAnimationFrame(v)):u<p&&(u+=40,o.contentWrapperEl[o.axis[e].scrollOffsetAttr]=u,a.requestAnimationFrame(v)))};v()}},t.prototype.getContentElement=function(){return this.contentEl},t.prototype.getScrollElement=function(){return this.contentWrapperEl},t.prototype.removeListeners=function(){var t=H(this.el);this.el.removeEventListener("mouseenter",this.onMouseEnter),this.el.removeEventListener("pointerdown",this.onPointerEvent,!0),this.el.removeEventListener("mousemove",this.onMouseMove),this.el.removeEventListener("mouseleave",this.onMouseLeave),this.contentWrapperEl&&this.contentWrapperEl.removeEventListener("scroll",this.onScroll),t.removeEventListener("resize",this.onWindowResize),this.mutationObserver&&this.mutationObserver.disconnect(),this.resizeObserver&&this.resizeObserver.disconnect(),this.onMouseMove.cancel(),this.onWindowResize.cancel(),this.onStopScrolling.cancel(),this.onMouseEntered.cancel()},t.prototype.unMount=function(){this.removeListeners()},t.prototype.isWithinBounds=function(t){return this.mouseX>=t.left&&this.mouseX<=t.left+t.width&&this.mouseY>=t.top&&this.mouseY<=t.top+t.height},t.prototype.findChild=function(t,e){var i=t.matches||t.webkitMatchesSelector||t.mozMatchesSelector||t.msMatchesSelector;return Array.prototype.filter.call(t.children,(function(t){return i.call(t,e)}))[0]},t.rtlHelpers=null,t.defaultOptions={forceVisible:!1,clickOnTrack:!0,scrollbarMinSize:25,scrollbarMaxSize:0,ariaLabel:"scrollable content",classNames:{contentEl:"simplebar-content",contentWrapper:"simplebar-content-wrapper",offset:"simplebar-offset",mask:"simplebar-mask",wrapper:"simplebar-wrapper",placeholder:"simplebar-placeholder",scrollbar:"simplebar-scrollbar",track:"simplebar-track",heightAutoObserverWrapperEl:"simplebar-height-auto-observer-wrapper",heightAutoObserverEl:"simplebar-height-auto-observer",visible:"simplebar-visible",horizontal:"simplebar-horizontal",vertical:"simplebar-vertical",hover:"simplebar-hover",dragging:"simplebar-dragging",scrolling:"simplebar-scrolling",scrollable:"simplebar-scrollable",mouseEntered:"simplebar-mouse-entered"},scrollableNode:null,contentNode:null,autoHide:!0},t.getOptions=B,t.helpers=V,t}(),Y=X.helpers,F=Y.getOptions,I=Y.addClasses,$=function(e){function i(){for(var t=[],s=0;s<arguments.length;s++)t[s]=arguments[s];var r=e.apply(this,t)||this;return i.instances.set(t[0],r),r}return function(e,i){if("function"!=typeof i&&null!==i)throw new TypeError("Class extends value "+String(i)+" is not a constructor or null");function s(){this.constructor=e}t(e,i),e.prototype=null===i?Object.create(i):(s.prototype=i.prototype,new s)}(i,e),i.initDOMLoadedElements=function(){document.removeEventListener("DOMContentLoaded",this.initDOMLoadedElements),window.removeEventListener("load",this.initDOMLoadedElements),Array.prototype.forEach.call(document.querySelectorAll("[data-simplebar]"),(function(t){"init"===t.getAttribute("data-simplebar")||i.instances.has(t)||new i(t,F(t.attributes))}))},i.removeObserver=function(){var t;null===(t=i.globalObserver)||void 0===t||t.disconnect()},i.prototype.initDOM=function(){var t,e,i,s=this;if(!Array.prototype.filter.call(this.el.children,(function(t){return t.classList.contains(s.classNames.wrapper)})).length){for(this.wrapperEl=document.createElement("div"),this.contentWrapperEl=document.createElement("div"),this.offsetEl=document.createElement("div"),this.maskEl=document.createElement("div"),this.contentEl=document.createElement("div"),this.placeholderEl=document.createElement("div"),this.heightAutoObserverWrapperEl=document.createElement("div"),this.heightAutoObserverEl=document.createElement("div"),I(this.wrapperEl,this.classNames.wrapper),I(this.contentWrapperEl,this.classNames.contentWrapper),I(this.offsetEl,this.classNames.offset),I(this.maskEl,this.classNames.mask),I(this.contentEl,this.classNames.contentEl),I(this.placeholderEl,this.classNames.placeholder),I(this.heightAutoObserverWrapperEl,this.classNames.heightAutoObserverWrapperEl),I(this.heightAutoObserverEl,this.classNames.heightAutoObserverEl);this.el.firstChild;)this.contentEl.appendChild(this.el.firstChild);this.contentWrapperEl.appendChild(this.contentEl),this.offsetEl.appendChild(this.contentWrapperEl),this.maskEl.appendChild(this.offsetEl),this.heightAutoObserverWrapperEl.appendChild(this.heightAutoObserverEl),this.wrapperEl.appendChild(this.heightAutoObserverWrapperEl),this.wrapperEl.appendChild(this.maskEl),this.wrapperEl.appendChild(this.placeholderEl),this.el.appendChild(this.wrapperEl),null===(t=this.contentWrapperEl)||void 0===t||t.setAttribute("tabindex","0"),null===(e=this.contentWrapperEl)||void 0===e||e.setAttribute("role","region"),null===(i=this.contentWrapperEl)||void 0===i||i.setAttribute("aria-label",this.options.ariaLabel)}if(!this.axis.x.track.el||!this.axis.y.track.el){var r=document.createElement("div"),l=document.createElement("div");I(r,this.classNames.track),I(l,this.classNames.scrollbar),r.appendChild(l),this.axis.x.track.el=r.cloneNode(!0),I(this.axis.x.track.el,this.classNames.horizontal),this.axis.y.track.el=r.cloneNode(!0),I(this.axis.y.track.el,this.classNames.vertical),this.el.appendChild(this.axis.x.track.el),this.el.appendChild(this.axis.y.track.el)}X.prototype.initDOM.call(this),this.el.setAttribute("data-simplebar","init")},i.prototype.unMount=function(){X.prototype.unMount.call(this),i.instances.delete(this.el)},i.initHtmlApi=function(){this.initDOMLoadedElements=this.initDOMLoadedElements.bind(this),"undefined"!=typeof MutationObserver&&(this.globalObserver=new MutationObserver(i.handleMutations),this.globalObserver.observe(document,{childList:!0,subtree:!0})),"complete"===document.readyState||"loading"!==document.readyState&&!document.documentElement.doScroll?window.setTimeout(this.initDOMLoadedElements):(document.addEventListener("DOMContentLoaded",this.initDOMLoadedElements),window.addEventListener("load",this.initDOMLoadedElements))},i.handleMutations=function(t){t.forEach((function(t){t.addedNodes.forEach((function(t){1===t.nodeType&&(t.hasAttribute("data-simplebar")?!i.instances.has(t)&&document.documentElement.contains(t)&&new i(t,F(t.attributes)):t.querySelectorAll("[data-simplebar]").forEach((function(t){"init"!==t.getAttribute("data-simplebar")&&!i.instances.has(t)&&document.documentElement.contains(t)&&new i(t,F(t.attributes))})))})),t.removedNodes.forEach((function(t){var e;1===t.nodeType&&("init"===t.getAttribute("data-simplebar")?!document.documentElement.contains(t)&&(null===(e=i.instances.get(t))||void 0===e||e.unMount()):Array.prototype.forEach.call(t.querySelectorAll('[data-simplebar="init"]'),(function(t){var e;!document.documentElement.contains(t)&&(null===(e=i.instances.get(t))||void 0===e||e.unMount())})))}))}))},i.instances=new WeakMap,i}(X);return e&&$.initHtmlApi(),$}();
