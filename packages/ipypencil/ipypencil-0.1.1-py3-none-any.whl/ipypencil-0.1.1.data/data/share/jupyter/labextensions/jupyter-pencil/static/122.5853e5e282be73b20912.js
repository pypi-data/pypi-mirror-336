"use strict";(self.webpackChunkjupyter_pencil=self.webpackChunkjupyter_pencil||[]).push([[122],{122:function(e,t,r){var i=this&&this.__createBinding||(Object.create?function(e,t,r,i){void 0===i&&(i=r);var n=Object.getOwnPropertyDescriptor(t,r);n&&!("get"in n?!t.__esModule:n.writable||n.configurable)||(n={enumerable:!0,get:function(){return t[r]}}),Object.defineProperty(e,i,n)}:function(e,t,r,i){void 0===i&&(i=r),e[i]=t[r]}),n=this&&this.__setModuleDefault||(Object.create?function(e,t){Object.defineProperty(e,"default",{enumerable:!0,value:t})}:function(e,t){e.default=t}),u=this&&this.__importStar||function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var r in e)"default"!==r&&Object.prototype.hasOwnProperty.call(e,r)&&i(t,e,r);return n(t,e),t};Object.defineProperty(t,"__esModule",{value:!0});const c=r(983),o=u(r(885)),a=r(797),l={id:"jupyter-pencil:plugin",requires:[c.IJupyterWidgetRegistry],activate:function(e,t){t.registerWidget({name:a.MODULE_NAME,version:a.MODULE_VERSION,exports:o})},autoStart:!0};t.default=l}}]);