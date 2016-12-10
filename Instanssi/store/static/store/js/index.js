!function(t){function e(o){if(n[o])return n[o].exports;var r=n[o]={i:o,l:!1,exports:{}};return t[o].call(r.exports,r,r.exports,e),r.l=!0,r.exports}var n={};return e.m=t,e.c=n,e.i=function(t){return t},e.d=function(t,e,n){Object.defineProperty(t,e,{configurable:!1,enumerable:!0,get:n})},e.n=function(t){var n=t&&t.__esModule?function(){return t.default}:function(){return t};return e.d(n,"a",n),n},e.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},e.p="",e(e.s=9)}([function(t,e){t.exports=Vue},function(t,e,n){"use strict";(function(t,o){function r(t,e){this._id=t,this._clearFn=e}var a=n(6).nextTick,i=Function.prototype.apply,s=Array.prototype.slice,u={},c=0;e.setTimeout=function(){return new r(i.call(setTimeout,window,arguments),clearTimeout)},e.setInterval=function(){return new r(i.call(setInterval,window,arguments),clearInterval)},e.clearTimeout=e.clearInterval=function(t){t.close()},r.prototype.unref=r.prototype.ref=function(){},r.prototype.close=function(){this._clearFn.call(window,this._id)},e.enroll=function(t,e){clearTimeout(t._idleTimeoutId),t._idleTimeout=e},e.unenroll=function(t){clearTimeout(t._idleTimeoutId),t._idleTimeout=-1},e._unrefActive=e.active=function(t){clearTimeout(t._idleTimeoutId);var e=t._idleTimeout;e>=0&&(t._idleTimeoutId=setTimeout(function(){t._onTimeout&&t._onTimeout()},e))},e.setImmediate="function"==typeof t?t:function(t){var n=c++,o=!(arguments.length<2)&&s.call(arguments,1);return u[n]=!0,a(function(){u[n]&&(o?t.apply(null,o):t.call(null),e.clearImmediate(n))}),n},e.clearImmediate="function"==typeof o?o:function(t){delete u[t]}}).call(e,n(1).setImmediate,n(1).clearImmediate)},function(t,e,n){"use strict";function o(t){return t&&t.__esModule?t:{default:t}}function r(t){return t.toLocaleString("fi",{style:"currency",currency:"EUR"})}function a(t){return t.toFixed(2)+" €"}function i(t,e,n){return new d.default(function(o,r){var a=new XMLHttpRequest;a.onload=function(){a.status>=200&&a.status<300?o(JSON.parse(a.responseText)):a.onerror()},a.onerror=function(){r(a.responseText?JSON.parse(a.responseText):null)},a.open(t,e),a.setRequestHeader("Accept","application/json"),a.setRequestHeader("Content-Type","application/json;charset=UTF-8"),a.send(n?JSON.stringify(n):null)})}Object.defineProperty(e,"__esModule",{value:!0}),e.storeMessages=e.storeFormGroup=e.storeXHR=e.formatPrice=void 0;var s="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},u=n(0),c=o(u),l=n(7),d=o(l),f=!("object"!==("undefined"==typeof Intl?"undefined":s(Intl))||!Intl||"function"!=typeof Intl.NumberFormat),p=void 0;f?e.formatPrice=p=r:e.formatPrice=p=a;var m=c.default.component("store-form-group",{props:{title:String,field:String,messages:Object,update:Function,data:Object},methods:{onInput:function(t){this.$emit("update",this.field,t)}},computed:{clazz:function(){var t=this.messages,e=this.field;return t&&t[e]&&t[e].length>0?"form-group has-error":"form-group"}},template:'<div v-bind:class="clazz">\n        <label class="col-sm-4 control-label">{{ title }}</label>\n        <div class="col-sm-8">\n            <input class="form-control" @input="onInput" v-bind:value="data[field]" />\n            <store-messages :field="field" :messages="messages" />\n        </div>\n    </div>'}),v=c.default.component("store-messages",{props:{field:String,messages:Object},computed:{localMessages:function(){var t=this.messages,e=this.field;return t&&t[e]&&t[e].length>0?t[e]:null}},template:'<div><p v-if="localMessages">\n        <div class="alert alert-danger" role="alert" v-for="message in localMessages">\n            <span class="fa fa-times"></span> {{ message }}\n        </div>\n    </p></div>'});e.formatPrice=p,e.storeXHR=i,e.storeFormGroup=m,e.storeMessages=v},function(t,e,n){"use strict";function o(t){return t&&t.__esModule?t:{default:t}}var r=n(0),a=o(r);a.default.component("store-information-form",{props:{messages:Object,data:Object},methods:{update:function(t,e){this.data[t]=e.target.value}},template:n(8)})},,function(t,e){t.exports='<div class="product">\n    <span class="pull-right">\n        <span class="product-cart-count" v-if="cartCount > 0">\n            <span class="fa fa-shopping-cart"></span> {{ cartCount }}\n        </span>\n        <select class="product-variants" v-if="product.variants && product.variants.length > 0" v-model="variant">\n            <option v-for="variant in product.variants" v-bind:value="variant">\n                {{ variant.name }}\n            </option>\n        </select>\n        <button class="btn btn-success" v-on:click="addItem()">\n            <span class="fa fa-plus" /> Lisää\n        </button>\n    </span>\n    <div>\n        <img :src="product.imagefile_thumbnail_url" width="48" height="48" />\n        {{ product.name }} ({{ product.price | formatPrice }})\n        <p class="small" v-if="product.description" v-html="product.description"></p>\n        <p v-if="product.discount_amount > 0">\n            <span class="fa fa-info"/>\n            {{ product.discount_percentage }} % alennus, jos ostat ainakin {{ product.discount_amount }} kappaletta!\n        </p>\n    </div>\n    <span class="clearfix"></span>\n</div>'},function(t,e){"use strict";function n(){throw new Error("setTimeout has not been defined")}function o(){throw new Error("clearTimeout has not been defined")}function r(t){if(l===setTimeout)return setTimeout(t,0);if((l===n||!l)&&setTimeout)return l=setTimeout,setTimeout(t,0);try{return l(t,0)}catch(e){try{return l.call(null,t,0)}catch(e){return l.call(this,t,0)}}}function a(t){if(d===clearTimeout)return clearTimeout(t);if((d===o||!d)&&clearTimeout)return d=clearTimeout,clearTimeout(t);try{return d(t)}catch(e){try{return d.call(null,t)}catch(e){return d.call(this,t)}}}function i(){v&&p&&(v=!1,p.length?m=p.concat(m):h=-1,m.length&&s())}function s(){if(!v){var t=r(i);v=!0;for(var e=m.length;e;){for(p=m,m=[];++h<e;)p&&p[h].run();h=-1,e=m.length}p=null,v=!1,a(t)}}function u(t,e){this.fun=t,this.array=e}function c(){}var l,d,f=t.exports={};!function(){try{l="function"==typeof setTimeout?setTimeout:n}catch(t){l=n}try{d="function"==typeof clearTimeout?clearTimeout:o}catch(t){d=o}}();var p,m=[],v=!1,h=-1;f.nextTick=function(t){var e=new Array(arguments.length-1);if(arguments.length>1)for(var n=1;n<arguments.length;n++)e[n-1]=arguments[n];m.push(new u(t,e)),1!==m.length||v||r(s)},u.prototype.run=function(){this.fun.apply(null,this.array)},f.title="browser",f.browser=!0,f.env={},f.argv=[],f.version="",f.versions={},f.on=c,f.addListener=c,f.once=c,f.off=c,f.removeListener=c,f.removeAllListeners=c,f.emit=c,f.binding=function(t){throw new Error("process.binding is not supported")},f.cwd=function(){return"/"},f.chdir=function(t){throw new Error("process.chdir is not supported")},f.umask=function(){return 0}},function(t,e,n){(function(e){!function(n){function o(){}function r(t,e){return function(){t.apply(e,arguments)}}function a(t){if("object"!=typeof this)throw new TypeError("Promises must be constructed via new");if("function"!=typeof t)throw new TypeError("not a function");this._state=0,this._handled=!1,this._value=void 0,this._deferreds=[],d(t,this)}function i(t,e){for(;3===t._state;)t=t._value;return 0===t._state?void t._deferreds.push(e):(t._handled=!0,void a._immediateFn(function(){var n=1===t._state?e.onFulfilled:e.onRejected;if(null===n)return void(1===t._state?s:u)(e.promise,t._value);var o;try{o=n(t._value)}catch(t){return void u(e.promise,t)}s(e.promise,o)}))}function s(t,e){try{if(e===t)throw new TypeError("A promise cannot be resolved with itself.");if(e&&("object"==typeof e||"function"==typeof e)){var n=e.then;if(e instanceof a)return t._state=3,t._value=e,void c(t);if("function"==typeof n)return void d(r(n,e),t)}t._state=1,t._value=e,c(t)}catch(e){u(t,e)}}function u(t,e){t._state=2,t._value=e,c(t)}function c(t){2===t._state&&0===t._deferreds.length&&a._immediateFn(function(){t._handled||a._unhandledRejectionFn(t._value)});for(var e=0,n=t._deferreds.length;e<n;e++)i(t,t._deferreds[e]);t._deferreds=null}function l(t,e,n){this.onFulfilled="function"==typeof t?t:null,this.onRejected="function"==typeof e?e:null,this.promise=n}function d(t,e){var n=!1;try{t(function(t){n||(n=!0,s(e,t))},function(t){n||(n=!0,u(e,t))})}catch(t){if(n)return;n=!0,u(e,t)}}var f=setTimeout;a.prototype.catch=function(t){return this.then(null,t)},a.prototype.then=function(t,e){var n=new this.constructor(o);return i(this,new l(t,e,n)),n},a.all=function(t){var e=Array.prototype.slice.call(t);return new a(function(t,n){function o(a,i){try{if(i&&("object"==typeof i||"function"==typeof i)){var s=i.then;if("function"==typeof s)return void s.call(i,function(t){o(a,t)},n)}e[a]=i,0===--r&&t(e)}catch(t){n(t)}}if(0===e.length)return t([]);for(var r=e.length,a=0;a<e.length;a++)o(a,e[a])})},a.resolve=function(t){return t&&"object"==typeof t&&t.constructor===a?t:new a(function(e){e(t)})},a.reject=function(t){return new a(function(e,n){n(t)})},a.race=function(t){return new a(function(e,n){for(var o=0,r=t.length;o<r;o++)t[o].then(e,n)})},a._immediateFn="function"==typeof e&&function(t){e(t)}||function(t){f(t,0)},a._unhandledRejectionFn=function(t){"undefined"!=typeof console&&console&&console.warn("Possible Unhandled Promise Rejection:",t)},a._setImmediateFn=function(t){a._immediateFn=t},a._setUnhandledRejectionFn=function(t){a._unhandledRejectionFn=t},"undefined"!=typeof t&&t.exports?t.exports=a:n.Promise||(n.Promise=a)}(this)}).call(e,n(1).setImmediate)},function(t,e){t.exports='<form class="form-horizontal" @submit.prevent>\n    <p>Huomaathan, että lippukoodit lähetetään annettuun sähköpostiosoitteeseen.</p>\n    <div class="row"><div class="col-lg-6">\n        <store-form-group title="Etunimi" field="first_name" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Sukunimi" field="last_name" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Sähköposti" field="email" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Vahvista sähköposti" field="email2" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Matkapuhelin" field="mobile" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Muu puhelinnumero" field="telephone" @update="update" :messages="messages" :data="data" />\n    </div>\n    <div class="col-lg-6">\n        <store-form-group title="Katuosoite" field="street" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Postinumero" field="postal_code" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Kaupunki" field="city" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Maa" field="country" @update="update" :messages="messages" :data="data" />\n        <store-form-group title="Yritys" field="company" @update="update" :messages="messages" :data="data" />\n    </div></div>\n    <div class="form-group">\n        <label class="col-lg-2 control-label">Lisätietoja</label>\n        <div class="col-lg-10">\n            <textarea class="form-control" @input="update(\'information\', $event)" v-bind:value="data.information"></textarea>\n            <store-messages field="information" :messages="messages" />\n        </div>\n    </div>\n    <div class="form-group">\n        <div class="col-sm-12">\n            <label class="control-label">\n                <input type="checkbox" v-model="data.read_terms" />\n                <span>\n                    Olen lukenut <a target="_blank" href="/store/terms">toimitusehdot</a> ja hyväksyn ne.\n                </span>\n            </label>\n            <store-messages field="read_terms" :messages="messages" />\n        </div>\n    </div>\n    <div class="clearfix"></div>\n</form>\n'},function(t,e,n){"use strict";function o(t){return t&&t.__esModule?t:{default:t}}function r(t,e,n){return t.product.id===e.id&&(!n||t.variant&&n.id===t.variant.id)}var a=n(0),i=o(a),s=n(2);n(3),i.default.filter("formatPrice",s.formatPrice),i.default.component("store-product",{props:{product:Object,cart:Array,messages:Object},data:function(){return{variant:null}},created:function(){var t=this.product;t.variants&&t.variants.length&&(this.variant=t.variants[0])},methods:{addItem:function(){this.$emit("addItem",this.product,this.variant)}},computed:{cartCount:function(){var t=this.product,e=this.variant;if(!this.cart)return 0;var n=this.cart.findIndex(function(n){return r(n,t,e)});return n<0?0:this.cart[n].count}},template:n(5)});new i.default({el:"#store",data:{products:[],cart:[],messages:{},info:{first_name:"",last_name:"",email:"",street:"",postal_code:"",city:"",country:"",mobile:"",telephone:"",company:"",information:"",read_terms:!1},totalPrice:0},template:n(10),created:function(){var t=this;(0,s.storeXHR)("GET","/api/store_items/?format=json").then(function(e){e.forEach(function(t){t.price=parseFloat(t.price)}),t.products=e}).catch(function(t){console.error("error fetching store items:",t)})},methods:{updateInfo:function(t){this.info=t},getSubtotal:function(t){var e=1,n=t.product.discount_amount,o=(100-t.product.discount_percentage)/100;return n&&t.count>=n&&(e*=o),t.product.price*t.count*e},updateCart:function(){var t=this,e=0;this.cart.forEach(function(n){e+=t.getSubtotal(n)}),this.totalPrice=e},addItem:function(t,e){var n=this.cart.findIndex(function(n){return r(n,t,e)});if(n>=0){var o=Object.assign({},this.cart[n]);o.count++,this.cart.splice(n,1,o)}else this.cart.push({count:1,product:t,variant:e});this.updateCart()},removeItemFromCart:function(t){var e=this.cart.indexOf(t);this.cart.splice(e,1),this.updateCart()},changeItemCount:function(t,e){var n=this.cart.indexOf(t),o=this.cart[n];return o.count+e<=0?void this.removeItemFromCart(o):(o.count+=e,this.cart.splice(n,1,o),void this.updateCart())},getTransactionObject:function(){var t=Object.assign({},this.info);return t.items=this.cart.map(function(t){return{item_id:t.product.id,variant_id:t.variant?t.variant.id:null,amount:t.count}}),t},submit:function(){var t=this,e=this.info;if(e.email!==e.email2)return void(this.messages={email:["Kirjoita sama sähköpostiosoite kahdesti."],email2:["Kirjoita sama sähköpostiosoite kahdesti."]});var n=this.getTransactionObject();return(0,s.storeXHR)("POST","/api/store_transaction/?format=json",n).then(function(t){console.info(t)},function(e){t.messages=e,e&&(e.email2=e.email)}).catch(function(t){console.error(t)})}}})},function(t,e){t.exports='<div>\n    <h3>Tuotteet</h3>\n    <div class="list-unstyled store-items">\n        <store-product v-for="product in products" :product="product" :cart="cart" :messages="messages" v-on:addItem="addItem" />\n    </div>\n    <h3>Ostoskori</h3>\n    <store-messages field="items" :messages="messages" />\n    <div class="list-unstyled store-items">\n        <div v-for="item in cart">\n            <div class="pull-left">\n                <span>{{ item.product.name }}</span>\n                <span v-if="item.variant">({{ item.variant.name }})</span>\n            </div>\n            <span class="pull-right">\n            x {{ item.count }} = {{ getSubtotal(item) | formatPrice }}\n            <button class="btn btn-secondary" v-on:click="changeItemCount(item, 1)">+</button>\n            <button class="btn btn-secondary" v-on:click="changeItemCount(item, -1)">-</button>\n            <button class="btn btn-danger" v-on:click="removeItemFromCart(item)">\n                <span class="fa fa-fw fa-trash"></span>\n            </button>\n            </span>\n            <span class="clearfix"></span>\n        </div>\n        <div>Yhteensä: {{ totalPrice | formatPrice }}</div>\n    </div>\n    <h3>Tiedot</h3>\n    <store-information-form @infoUpdate="updateInfo" :data="info" :messages="messages" />\n    <span class="pull-right">\n    <button class="btn btn-primary" @click="submit">Jatka &gt;</button>\n</span>\n</div>'}]);