(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[811],{95822:function(e,t,n){Promise.resolve().then(n.bind(n,54224))},54224:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return m}});var r=n(57437),a=n(88797),i=n(2265);let o=(0,n(87565).A)(function(e){return i.createElement("svg",Object.assign({viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",width:"1em",height:"1em",focusable:!1,"aria-hidden":!0},e),i.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M3 4a2 2 0 0 0-2 2v12c0 1.1.9 2 2 2h11a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2H3Zm4.98 4h-3v3h3V8Z",fill:"currentColor"}),i.createElement("path",{d:"M21.55 6.72a1 1 0 0 1 1.45.9v8.76a1 1 0 0 1-1.45.9l-4-2a1 1 0 0 1-.55-.9V9.62a1 1 0 0 1 .56-.9l4-2Z",fill:"currentColor"}))},"user_card_video");var l=n(67050),d=n(85323),s=n(97500),c=n(55775),u=n.n(c),f=n(36699);let h=u()(()=>Promise.all([n.e(714),n.e(739),n.e(543)]).then(n.bind(n,59543)),{loadableGenerated:{webpack:()=>[59543]},ssr:!1});function m(){let{Header:e,Footer:t,Sider:n,Content:c}=a.Layout,{data:u,error:m,isLoading:g}=(0,d.ZP)("/v1/videos",s._i),{Text:p}=a.Typography,[v,x]=(0,i.useState)(),w=[{title:"标题",dataIndex:"name",render:(e,t,n)=>(0,r.jsx)(p,{strong:!0,children:e})},{title:"大小",dataIndex:"size",render:e=>"".concat((e/1024/1024).toFixed(2)," MB")},{title:"更新日期",dataIndex:"updateTime",defaultSortOrder:"descend",sorter:(e,t)=>e.updateTime-t.updateTime>0?1:-1,render:e=>(0,f.cE)(e)},{title:"",dataIndex:"operate",render:(e,t,n)=>(0,r.jsx)(o,{style:{cursor:"pointer"},onClick:()=>j(t.name)})}],[b,y]=(0,i.useState)(!1),j=e=>{y(!0),x(e)};return(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)(e,{style:{backgroundColor:"var(--semi-color-bg-1)"},children:(0,r.jsx)(a.JL,{style:{border:"none"},header:(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)("div",{style:{backgroundColor:"rgba(var(--semi-green-4), 1)",borderRadius:"var(--semi-border-radius-large)",color:"var(--semi-color-bg-0)",display:"flex",padding:"6px"},children:(0,r.jsx)(l.Z,{size:"large"})}),(0,r.jsx)("h4",{style:{marginLeft:"12px"},children:"历史记录"})]}),mode:"horizontal"})}),(0,r.jsxs)(c,{style:{paddingLeft:12,paddingRight:12,backgroundColor:"var(--semi-color-bg-0)"},children:[(0,r.jsx)("main",{children:(0,r.jsx)(a.iA,{size:"small",columns:w,dataSource:u})}),(0,r.jsxs)(a.u_,{visible:b,onCancel:()=>{y(!1),console.log("Cancel button clicked")},closeOnEsc:!0,size:"large",bodyStyle:{height:500},footer:null,children:[(0,r.jsx)(h,{url:"/static/"+v}),(0,r.jsx)("div",{id:"mse"})]})]})]})}},97500:function(e,t,n){"use strict";async function r(e,t){let{arg:n}=t,r=await fetch(""+e,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)});if(!(r.status>=200&&r.status<300))throw Error(await r.text());let a=await r.json();if(!r.ok)throw Error(a.message);return a}n.d(t,{_i:function(){return a},gz:function(){return l},hw:function(){return o},sj:function(){return i},wG:function(){return r}});let a=async function(){for(var e=arguments.length,t=Array(e),n=0;n<e;n++)t[n]=arguments[n];let r=await fetch(""+t[0],t[1]);if(!r.ok)throw Error(await r.text());return r.json()},i=async(e,t)=>{let n=await fetch(""+e,t);if(!n.ok)throw Error(await n.text());return n};async function o(e,t){let{arg:n}=t,r=await fetch("".concat("").concat(e,"/").concat(n),{method:"DELETE"});if(!r.ok)throw Error(await r.text());return r}async function l(e,t){let{arg:n}=t,r=await fetch("".concat("").concat(e),{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)});if(!r.ok)throw Error(await r.text());return r}},36699:function(e,t,n){"use strict";n.d(t,{Fg:function(){return d},K4:function(){return l},cE:function(){return o},f:function(){return a},ql:function(){return i}});var r=n(2265);let a={xs:"(max-width: 575px)",sm:"(min-width: 576px)",md:"(min-width: 768px)",lg:"(min-width: 992px)",xl:"(min-width: 1200px)",xxl:"(min-width: 1600px)"},i=(e,t)=>{let{match:n,unmatch:r,callInInit:a=!0}=t;{let t=window.matchMedia(e),i=function(e){e.matches?n&&n(e):r&&r(e)};return(a&&i(t),Object.prototype.hasOwnProperty.call(t,"addEventListener"))?(t.addEventListener("change",i),()=>t.removeEventListener("change",i)):(t.addListener(i),()=>t.removeListener(i))}},o=e=>new Date(1e3*e).toLocaleString("zh-CN",{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",hour12:!1}).replaceAll("/","-"),l=()=>{let[e,t]=(0,r.useState)("light");return(0,r.useEffect)(()=>{let e=()=>window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";t(e);let n=window.matchMedia("(prefers-color-scheme: dark)"),r=()=>t(e);return n.addEventListener("change",r),()=>n.removeEventListener("change",r)},[]),e},d=(e,t)=>{(0,r.useEffect)(()=>{switch(localStorage.setItem("mode",e),e){case"light":document.body.setAttribute("theme-mode","light");break;case"dark":document.body.setAttribute("theme-mode","dark");break;default:document.body.setAttribute("theme-mode",t)}},[e,t])}},67050:function(e,t,n){"use strict";var r=n(2265);let a=(0,n(87565).A)(function(e){return r.createElement("svg",Object.assign({viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",width:"1em",height:"1em",focusable:!1,"aria-hidden":!0},e),r.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M4 2a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h7a1 1 0 1 0 0-2H4V4h16v10a1 1 0 1 0 2 0V4a2 2 0 0 0-2-2H4Zm5.5 5.13A1 1 0 0 0 8 8v8a1 1 0 0 0 1.5.87l7-4a1 1 0 0 0 0-1.74l-7-4ZM13.98 12 10 14.28V9.72L13.98 12Zm.52 5a.5.5 0 0 0-.5.5v1c0 .28.22.5.5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1Zm0 3a.5.5 0 0 0-.5.5v1c0 .28.22.5.5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1Zm2.5-2.5c0-.28.22-.5.5-.5h4c.28 0 .5.22.5.5v1a.5.5 0 0 1-.5.5h-4a.5.5 0 0 1-.5-.5v-1Zm.5 2.5a.5.5 0 0 0-.5.5v1c0 .28.22.5.5.5h4a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-4Z",fill:"currentColor"}))},"video_list_stroked");t.Z=a},55775:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"default",{enumerable:!0,get:function(){return i}});let r=n(47043);n(57437),n(2265);let a=r._(n(15602));function i(e,t){var n;let r={loading:e=>{let{error:t,isLoading:n,pastDelay:r}=e;return null}};"function"==typeof e&&(r.loader=e);let i={...r,...t};return(0,a.default)({...i,modules:null==(n=i.loadableGenerated)?void 0:n.modules})}("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},81523:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"BailoutToCSR",{enumerable:!0,get:function(){return a}});let r=n(18993);function a(e){let{reason:t,children:n}=e;if("undefined"==typeof window)throw new r.BailoutToCSRError(t);return n}},15602:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"default",{enumerable:!0,get:function(){return s}});let r=n(57437),a=n(2265),i=n(81523),o=n(70049);function l(e){return{default:e&&"default"in e?e.default:e}}let d={loader:()=>Promise.resolve(l(()=>null)),loading:null,ssr:!0},s=function(e){let t={...d,...e},n=(0,a.lazy)(()=>t.loader().then(l)),s=t.loading;function c(e){let l=s?(0,r.jsx)(s,{isLoading:!0,pastDelay:!0,error:null}):null,d=t.ssr?(0,r.jsxs)(r.Fragment,{children:["undefined"==typeof window?(0,r.jsx)(o.PreloadCss,{moduleIds:t.modules}):null,(0,r.jsx)(n,{...e})]}):(0,r.jsx)(i.BailoutToCSR,{reason:"next/dynamic",children:(0,r.jsx)(n,{...e})});return(0,r.jsx)(a.Suspense,{fallback:l,children:d})}return c.displayName="LoadableComponent",c}},70049:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"PreloadCss",{enumerable:!0,get:function(){return i}});let r=n(57437),a=n(20544);function i(e){let{moduleIds:t}=e;if("undefined"!=typeof window)return null;let n=(0,a.getExpectedRequestStore)("next/dynamic css"),i=[];if(n.reactLoadableManifest&&t){let e=n.reactLoadableManifest;for(let n of t){if(!e[n])continue;let t=e[n].files.filter(e=>e.endsWith(".css"));i.push(...t)}}return 0===i.length?null:(0,r.jsx)(r.Fragment,{children:i.map(e=>(0,r.jsx)("link",{precedence:"dynamic",rel:"stylesheet",href:n.assetPrefix+"/_next/"+encodeURI(e),as:"style"},e))})}}},function(e){e.O(0,[308,385,251,157,440,326,152,797,323,971,117,744],function(){return e(e.s=95822)}),_N_E=e.O()}]);