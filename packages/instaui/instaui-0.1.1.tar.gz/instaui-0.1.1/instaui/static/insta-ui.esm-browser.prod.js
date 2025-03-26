var Mn = Object.defineProperty;
var Fn = (e, t, n) => t in e ? Mn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var M = (e, t, n) => Fn(e, typeof t != "symbol" ? t + "" : t, n);
import * as Bn from "vue";
import { unref as B, watch as K, nextTick as Ve, isRef as Ut, shallowRef as Q, ref as J, watchEffect as Gt, computed as W, readonly as Wn, provide as Pe, inject as te, customRef as ct, toValue as H, shallowReactive as Ln, defineComponent as F, reactive as Un, h as A, getCurrentInstance as Kt, toRaw as Gn, normalizeStyle as Kn, normalizeClass as qe, toDisplayString as Ht, onUnmounted as Ce, Fragment as Ae, vModelDynamic as Hn, vShow as qn, resolveDynamicComponent as ut, normalizeProps as zn, withDirectives as Jn, onErrorCaptured as Qn, openBlock as he, createElementBlock as be, createElementVNode as Yn, createVNode as Xn, withCtx as Zn, renderList as er, createBlock as tr, TransitionGroup as qt, KeepAlive as nr } from "vue";
let zt, ze, Je;
function rr(e) {
  zt = e.queryPath, ze = e.pathParams, Je = e.queryParams;
}
function lt() {
  return {
    path: zt,
    ...ze === void 0 ? {} : { params: ze },
    ...Je === void 0 ? {} : { queryParams: Je }
  };
}
var oe;
((e) => {
  function t(i) {
    return i.type === "ref";
  }
  e.isRef = t;
  function n(i) {
    return i.type === "vComputed";
  }
  e.isVueComputed = n;
  function r(i) {
    return i.type === "jsComputed";
  }
  e.isJsComputed = r;
  function o(i) {
    return i.type === "webComputed";
  }
  e.isWebComputed = o;
  function s(i) {
    return i.type === "data";
  }
  e.isConstData = s;
})(oe || (oe = {}));
var N;
((e) => {
  function t(g) {
    return g.type === "ref" || g.type === "computed" || g.type === "webComputed" || g.type === "data";
  }
  e.isVar = t;
  function n(g) {
    return g.type === "ref";
  }
  e.isRef = n;
  function r(g) {
    return g.type === "routePar";
  }
  e.isRouterParams = r;
  function o(g) {
    return g.type === "routeAct";
  }
  e.isRouterAction = o;
  function s(g) {
    return g.type === "data";
  }
  e.isConstData = s;
  function i(g) {
    return g.type === "computed";
  }
  e.isComputed = i;
  function c(g) {
    return g.type === "webComputed";
  }
  e.isWebComputed = c;
  function l(g) {
    return g.type === "js";
  }
  e.isJs = l;
  function h(g) {
    return g.type === "jsOutput";
  }
  e.isJsOutput = h;
  function u(g) {
    return g.type === "vf";
  }
  e.isVForItem = u;
  function a(g) {
    return g.type === "vf-i";
  }
  e.isVForIndex = a;
  function f(g) {
    return g.type === "sp";
  }
  e.isSlotProp = f;
  function d(g) {
    return g.type === "event";
  }
  e.isEventContext = d;
  function p(g) {
    return g.type === "ele_ref";
  }
  e.isElementRef = p;
  function v(g) {
    return g.type !== void 0;
  }
  e.IsBinding = v;
})(N || (N = {}));
var Qe;
((e) => {
  function t(n) {
    return n.url !== void 0;
  }
  e.isWebEventHandler = t;
})(Qe || (Qe = {}));
class or extends Map {
  constructor(t) {
    super(), this.factory = t;
  }
  getOrDefault(t) {
    if (!this.has(t)) {
      const n = this.factory();
      return this.set(t, n), n;
    }
    return super.get(t);
  }
}
function ye(e) {
  return new or(e);
}
function de(e) {
  return typeof e == "function" ? e() : B(e);
}
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const Ye = () => {
};
function Xe(e, t = !1, n = "Timeout") {
  return new Promise((r, o) => {
    setTimeout(t ? () => o(n) : r, e);
  });
}
function Ze(e, t = !1) {
  function n(a, { flush: f = "sync", deep: d = !1, timeout: p, throwOnTimeout: v } = {}) {
    let g = null;
    const _ = [new Promise((O) => {
      g = K(
        e,
        (V) => {
          a(V) !== t && (g ? g() : Ve(() => g == null ? void 0 : g()), O(V));
        },
        {
          flush: f,
          deep: d,
          immediate: !0
        }
      );
    })];
    return p != null && _.push(
      Xe(p, v).then(() => de(e)).finally(() => g == null ? void 0 : g())
    ), Promise.race(_);
  }
  function r(a, f) {
    if (!Ut(a))
      return n((V) => V === a, f);
    const { flush: d = "sync", deep: p = !1, timeout: v, throwOnTimeout: g } = f ?? {};
    let y = null;
    const O = [new Promise((V) => {
      y = K(
        [e, a],
        ([$, x]) => {
          t !== ($ === x) && (y ? y() : Ve(() => y == null ? void 0 : y()), V($));
        },
        {
          flush: d,
          deep: p,
          immediate: !0
        }
      );
    })];
    return v != null && O.push(
      Xe(v, g).then(() => de(e)).finally(() => (y == null || y(), de(e)))
    ), Promise.race(O);
  }
  function o(a) {
    return n((f) => !!f, a);
  }
  function s(a) {
    return r(null, a);
  }
  function i(a) {
    return r(void 0, a);
  }
  function c(a) {
    return n(Number.isNaN, a);
  }
  function l(a, f) {
    return n((d) => {
      const p = Array.from(d);
      return p.includes(a) || p.includes(de(a));
    }, f);
  }
  function h(a) {
    return u(1, a);
  }
  function u(a = 1, f) {
    let d = -1;
    return n(() => (d += 1, d >= a), f);
  }
  return Array.isArray(de(e)) ? {
    toMatch: n,
    toContains: l,
    changed: h,
    changedTimes: u,
    get not() {
      return Ze(e, !t);
    }
  } : {
    toMatch: n,
    toBe: r,
    toBeTruthy: o,
    toBeNull: s,
    toBeNaN: c,
    toBeUndefined: i,
    changed: h,
    changedTimes: u,
    get not() {
      return Ze(e, !t);
    }
  };
}
function sr(e) {
  return Ze(e);
}
function ir(e, t, n) {
  let r;
  Ut(n) ? r = {
    evaluating: n
  } : r = n || {};
  const {
    lazy: o = !1,
    evaluating: s = void 0,
    shallow: i = !0,
    onError: c = Ye
  } = r, l = J(!o), h = i ? Q(t) : J(t);
  let u = 0;
  return Gt(async (a) => {
    if (!l.value)
      return;
    u++;
    const f = u;
    let d = !1;
    s && Promise.resolve().then(() => {
      s.value = !0;
    });
    try {
      const p = await e((v) => {
        a(() => {
          s && (s.value = !1), d || v();
        });
      });
      f === u && (h.value = p);
    } catch (p) {
      c(p);
    } finally {
      s && f === u && (s.value = !1), d = !0;
    }
  }), o ? W(() => (l.value = !0, h.value)) : h;
}
function ar(e, t, n) {
  const {
    immediate: r = !0,
    delay: o = 0,
    onError: s = Ye,
    onSuccess: i = Ye,
    resetOnExecute: c = !0,
    shallow: l = !0,
    throwError: h
  } = {}, u = l ? Q(t) : J(t), a = J(!1), f = J(!1), d = Q(void 0);
  async function p(y = 0, ..._) {
    c && (u.value = t), d.value = void 0, a.value = !1, f.value = !0, y > 0 && await Xe(y);
    const O = typeof e == "function" ? e(..._) : e;
    try {
      const V = await O;
      u.value = V, a.value = !0, i(V);
    } catch (V) {
      if (d.value = V, s(V), h)
        throw V;
    } finally {
      f.value = !1;
    }
    return u.value;
  }
  r && p(o);
  const v = {
    state: u,
    isReady: a,
    isLoading: f,
    error: d,
    execute: p
  };
  function g() {
    return new Promise((y, _) => {
      sr(f).toBe(!1).then(() => y(v)).catch(_);
    });
  }
  return {
    ...v,
    then(y, _) {
      return g().then(y, _);
    }
  };
}
function G(e, t) {
  t = t || {};
  const n = [...Object.keys(t), "__Vue"], r = [...Object.values(t), Bn];
  try {
    return new Function(...n, `return (${e})`)(...r);
  } catch (o) {
    throw new Error(o + " in function code: " + e);
  }
}
function cr(e) {
  if (e.startsWith(":")) {
    e = e.slice(1);
    try {
      return G(e);
    } catch (t) {
      throw new Error(t + " in function code: " + e);
    }
  }
}
function Jt(e) {
  return e.constructor.name === "AsyncFunction";
}
function ur(e, t) {
  return J(e.value);
}
function lr(e, t, n) {
  const { bind: r = {}, code: o, const: s = [] } = e, i = Object.values(r).map((u, a) => s[a] === 1 ? u : t.getVueRefObjectOrValue(u));
  if (Jt(new Function(o)))
    return ir(
      async () => {
        const u = Object.fromEntries(
          Object.keys(r).map((a, f) => [a, i[f]])
        );
        return await G(o, u)();
      },
      null,
      { lazy: !0 }
    );
  const c = Object.fromEntries(
    Object.keys(r).map((u, a) => [u, i[a]])
  ), l = G(o, c);
  return W(l);
}
function fr(e, t, n) {
  const {
    inputs: r = [],
    code: o,
    slient: s,
    data: i,
    asyncInit: c = null
  } = e, l = s || Array(r.length).fill(0), h = i || Array(r.length).fill(0), u = r.filter((v, g) => l[g] === 0 && h[g] === 0).map((v) => t.getVueRefObject(v));
  function a() {
    return r.map(
      (v, g) => h[g] === 1 ? v : t.getObjectToValue(v)
    );
  }
  const f = G(o), d = Q(null), p = { immediate: !0, deep: !0 };
  return Jt(f) ? (d.value = c, K(
    u,
    async () => {
      d.value = await f(...a());
    },
    p
  )) : K(
    u,
    () => {
      d.value = f(...a());
    },
    p
  ), Wn(d);
}
function hr(e, t) {
  const { init: n } = e;
  return Q(n ?? null);
}
function dr() {
  return [];
}
const Ee = ye(dr);
function Qt(e, t) {
  const n = Ee.getOrDefault(e.id), r = /* @__PURE__ */ new Map();
  return n.push(r), t.replaceSnapshot({
    scopeSnapshot: Yt()
  }), (e.vars || []).forEach((o) => {
    r.set(o.id, gr(o, t));
  }), (e.web_computed || []).forEach((o) => {
    const { init: s } = o;
    r.set(o.id, J(s));
  }), n.length - 1;
}
function Yt() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of Ee) {
    const o = r[r.length - 1];
    e.set(n, [o]);
  }
  function t(n) {
    return Xt(n, e);
  }
  return {
    getVueRef: t
  };
}
function pr(e) {
  return Xt(e, Ee);
}
function Xt(e, t) {
  const n = t.get(e.sid);
  if (!n)
    throw new Error(`Scope ${e.sid} not found`);
  const o = n[n.length - 1].get(e.id);
  if (!o)
    throw new Error(`Var ${e.id} not found in scope ${e.sid}`);
  return o;
}
function mr(e) {
  Ee.delete(e);
}
function Zt(e, t) {
  const n = Ee.get(e);
  n && n.splice(t, 1);
}
function gr(e, t, n) {
  if (oe.isRef(e))
    return ur(e);
  if (oe.isVueComputed(e))
    return lr(
      e,
      t
    );
  if (oe.isJsComputed(e))
    return fr(
      e,
      t
    );
  if (oe.isWebComputed(e))
    return hr(e);
  if (oe.isConstData(e))
    return e.value;
  throw new Error(`Invalid var config: ${e}`);
}
const ke = ye(() => []);
function vr(e) {
  const t = Q();
  ke.getOrDefault(e.sid).push(t);
}
function yr(e) {
  ke.has(e) && ke.delete(e);
}
function en() {
  const e = new Map(
    Array.from(ke.entries()).map(([n, r]) => [
      n,
      r[r.length - 1]
    ])
  );
  function t(n) {
    return e.get(n.sid);
  }
  return {
    getRef: t
  };
}
const $e = ye(() => []);
function Er(e) {
  const t = $e.getOrDefault(e);
  return t.push(Q({})), t.length - 1;
}
function wr(e, t, n) {
  $e.get(e)[t].value = n;
}
function _r(e) {
  $e.delete(e);
}
function Rr() {
  const e = /* @__PURE__ */ new Map();
  for (const [n, r] of $e) {
    const o = r[r.length - 1];
    e.set(n, o);
  }
  function t(n) {
    return e.get(n.id).value[n.name];
  }
  return {
    getPropsValue: t
  };
}
function wt(e, t) {
  Object.entries(e).forEach(([n, r]) => t(r, n));
}
function Te(e, t) {
  return tn(e, {
    valueFn: t
  });
}
function tn(e, t) {
  const { valueFn: n, keyFn: r } = t;
  return Object.fromEntries(
    Object.entries(e).map(([o, s]) => [
      r ? r(o, s) : o,
      n(s, o)
    ])
  );
}
function nn(e, t, n) {
  if (Array.isArray(t)) {
    const [o, ...s] = t;
    switch (o) {
      case "!":
        return !e;
      case "+":
        return e + s[0];
      case "~+":
        return s[0] + e;
    }
  }
  const r = rn(t, n);
  return e[r];
}
function rn(e, t) {
  if (typeof e == "string" || typeof e == "number")
    return e;
  if (!Array.isArray(e))
    throw new Error(`Invalid path ${e}`);
  const [n, ...r] = e;
  switch (n) {
    case "bind":
      if (!t)
        throw new Error("No bindable function provided");
      return t(r[0]);
    default:
      throw new Error(`Invalid flag ${n} in array at ${e}`);
  }
}
function we(e, t, n) {
  return t.reduce(
    (r, o) => nn(r, o, n),
    e
  );
}
function et(e, t, n, r) {
  t.reduce((o, s, i) => {
    if (i === t.length - 1)
      o[rn(s, r)] = n;
    else
      return nn(o, s, r);
  }, e);
}
const on = /* @__PURE__ */ new Map(), ft = ye(() => /* @__PURE__ */ new Map()), sn = /* @__PURE__ */ new Set(), an = Symbol("vfor");
function Or(e) {
  const t = cn() ?? {};
  Pe(an, { ...t, [e.fid]: e.key });
}
function cn() {
  return te(an, void 0);
}
function br() {
  const e = cn(), t = /* @__PURE__ */ new Map();
  return e === void 0 || Object.keys(e).forEach((n) => {
    t.set(n, e[n]);
  }), t;
}
function Sr(e, t, n, r) {
  const o = Y();
  if (r) {
    sn.add(e);
    return;
  }
  let s;
  if (n)
    s = new Ar(
      o,
      t
    );
  else {
    const i = Array.isArray(t) ? t : Object.entries(t).map(([c, l], h) => [l, c, h]);
    s = new Cr(i, o);
  }
  on.set(e, s);
}
function Pr(e, t, n) {
  const r = ft.getOrDefault(e);
  r.has(t) || r.set(t, J(n)), r.get(t).value = n;
}
function Vr(e) {
  const t = /* @__PURE__ */ new Set();
  function n(o) {
    t.add(o);
  }
  function r() {
    const o = ft.get(e);
    o !== void 0 && o.forEach((s, i) => {
      t.has(i) || o.delete(i);
    });
  }
  return {
    add: n,
    removeUnusedKeys: r
  };
}
function kr(e) {
  const t = e, n = br();
  function r(o) {
    const s = n.get(o) ?? t;
    return ft.get(o).get(s).value;
  }
  return {
    getVForIndex: r
  };
}
function Nr(e) {
  return on.get(e.binding.fid).createRefObjectWithPaths(e);
}
function Ir(e) {
  return sn.has(e);
}
class Cr {
  constructor(t, n) {
    this.array = t, this.snapshot = n;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { vforSnapshot: r } = t, { path: o = [] } = n, s = [...o], i = r.getVForIndex(n.fid);
    return s.unshift(i), ct(() => ({
      get: () => we(
        this.array,
        s,
        this.snapshot.getObjectToValue
      ),
      set: () => {
        throw new Error("Cannot set value to a constant array");
      }
    }));
  }
}
class Ar {
  constructor(t, n) {
    M(this, "_isDictSource");
    this.snapshot = t, this.binding = n;
  }
  isDictSource(t) {
    if (this._isDictSource === void 0) {
      const n = H(t);
      this._isDictSource = n !== null && !Array.isArray(n);
    }
    return this._isDictSource;
  }
  createRefObjectWithPaths(t) {
    const { binding: n } = t, { path: r = [] } = n, o = [...r], { vforSnapshot: s } = t, i = this.snapshot.getVueRefObject(this.binding), c = this.isDictSource(i), l = s.getVForIndex(n.fid), h = c && o.length === 0 ? [0] : [];
    return o.unshift(l, ...h), ct(() => ({
      get: () => {
        const u = H(i), a = c ? Object.entries(u).map(([f, d], p) => [
          d,
          f,
          p
        ]) : u;
        try {
          return we(
            H(a),
            o,
            this.snapshot.getObjectToValue
          );
        } catch {
          return;
        }
      },
      set: (u) => {
        const a = H(i);
        if (c) {
          const f = Object.keys(a);
          if (l >= f.length)
            throw new Error("Cannot set value to a non-existent key");
          const d = f[l];
          et(
            a,
            [d],
            u,
            this.snapshot.getObjectToValue
          );
          return;
        }
        et(
          a,
          o,
          u,
          this.snapshot.getObjectToValue
        );
      }
    }));
  }
}
function $r(e, t, n = !1) {
  return n && (e = `$computed(${e})`, t = { ...t, $computed: W }), G(e, t);
}
function _t(e, t, n) {
  const { paths: r, getBindableValueFn: o } = t, { paths: s, getBindableValueFn: i } = t;
  return r === void 0 || r.length === 0 ? e : ct(() => ({
    get() {
      try {
        return we(
          H(e),
          r,
          o
        );
      } catch {
        return;
      }
    },
    set(c) {
      et(
        H(e),
        s || r,
        c,
        i
      );
    }
  }));
}
function Rt(e) {
  return e == null;
}
function Tr() {
  return un().__VUE_DEVTOOLS_GLOBAL_HOOK__;
}
function un() {
  return typeof navigator < "u" && typeof window < "u" ? window : typeof globalThis < "u" ? globalThis : {};
}
const jr = typeof Proxy == "function", xr = "devtools-plugin:setup", Dr = "plugin:settings:set";
let ae, tt;
function Mr() {
  var e;
  return ae !== void 0 || (typeof window < "u" && window.performance ? (ae = !0, tt = window.performance) : typeof globalThis < "u" && (!((e = globalThis.perf_hooks) === null || e === void 0) && e.performance) ? (ae = !0, tt = globalThis.perf_hooks.performance) : ae = !1), ae;
}
function Fr() {
  return Mr() ? tt.now() : Date.now();
}
class Br {
  constructor(t, n) {
    this.target = null, this.targetQueue = [], this.onQueue = [], this.plugin = t, this.hook = n;
    const r = {};
    if (t.settings)
      for (const i in t.settings) {
        const c = t.settings[i];
        r[i] = c.defaultValue;
      }
    const o = `__vue-devtools-plugin-settings__${t.id}`;
    let s = Object.assign({}, r);
    try {
      const i = localStorage.getItem(o), c = JSON.parse(i);
      Object.assign(s, c);
    } catch {
    }
    this.fallbacks = {
      getSettings() {
        return s;
      },
      setSettings(i) {
        try {
          localStorage.setItem(o, JSON.stringify(i));
        } catch {
        }
        s = i;
      },
      now() {
        return Fr();
      }
    }, n && n.on(Dr, (i, c) => {
      i === this.plugin.id && this.fallbacks.setSettings(c);
    }), this.proxiedOn = new Proxy({}, {
      get: (i, c) => this.target ? this.target.on[c] : (...l) => {
        this.onQueue.push({
          method: c,
          args: l
        });
      }
    }), this.proxiedTarget = new Proxy({}, {
      get: (i, c) => this.target ? this.target[c] : c === "on" ? this.proxiedOn : Object.keys(this.fallbacks).includes(c) ? (...l) => (this.targetQueue.push({
        method: c,
        args: l,
        resolve: () => {
        }
      }), this.fallbacks[c](...l)) : (...l) => new Promise((h) => {
        this.targetQueue.push({
          method: c,
          args: l,
          resolve: h
        });
      })
    });
  }
  async setRealTarget(t) {
    this.target = t;
    for (const n of this.onQueue)
      this.target.on[n.method](...n.args);
    for (const n of this.targetQueue)
      n.resolve(await this.target[n.method](...n.args));
  }
}
function Wr(e, t) {
  const n = e, r = un(), o = Tr(), s = jr && n.enableEarlyProxy;
  if (o && (r.__VUE_DEVTOOLS_PLUGIN_API_AVAILABLE__ || !s))
    o.emit(xr, e, t);
  else {
    const i = s ? new Br(n, o) : null;
    (r.__VUE_DEVTOOLS_PLUGINS__ = r.__VUE_DEVTOOLS_PLUGINS__ || []).push({
      pluginDescriptor: n,
      setupFn: t,
      proxy: i
    }), i && t(i.proxiedTarget);
  }
}
var b = {};
const z = typeof document < "u";
function ln(e) {
  return typeof e == "object" || "displayName" in e || "props" in e || "__vccOpts" in e;
}
function Lr(e) {
  return e.__esModule || e[Symbol.toStringTag] === "Module" || // support CF with dynamic imports that do not
  // add the Module string tag
  e.default && ln(e.default);
}
const I = Object.assign;
function Ue(e, t) {
  const n = {};
  for (const r in t) {
    const o = t[r];
    n[r] = L(o) ? o.map(e) : e(o);
  }
  return n;
}
const ve = () => {
}, L = Array.isArray;
function S(e) {
  const t = Array.from(arguments).slice(1);
  console.warn.apply(console, ["[Vue Router warn]: " + e].concat(t));
}
const fn = /#/g, Ur = /&/g, Gr = /\//g, Kr = /=/g, Hr = /\?/g, hn = /\+/g, qr = /%5B/g, zr = /%5D/g, dn = /%5E/g, Jr = /%60/g, pn = /%7B/g, Qr = /%7C/g, mn = /%7D/g, Yr = /%20/g;
function ht(e) {
  return encodeURI("" + e).replace(Qr, "|").replace(qr, "[").replace(zr, "]");
}
function Xr(e) {
  return ht(e).replace(pn, "{").replace(mn, "}").replace(dn, "^");
}
function nt(e) {
  return ht(e).replace(hn, "%2B").replace(Yr, "+").replace(fn, "%23").replace(Ur, "%26").replace(Jr, "`").replace(pn, "{").replace(mn, "}").replace(dn, "^");
}
function Zr(e) {
  return nt(e).replace(Kr, "%3D");
}
function eo(e) {
  return ht(e).replace(fn, "%23").replace(Hr, "%3F");
}
function to(e) {
  return e == null ? "" : eo(e).replace(Gr, "%2F");
}
function ce(e) {
  try {
    return decodeURIComponent("" + e);
  } catch {
    b.NODE_ENV !== "production" && S(`Error decoding "${e}". Using original value`);
  }
  return "" + e;
}
const no = /\/$/, ro = (e) => e.replace(no, "");
function Ge(e, t, n = "/") {
  let r, o = {}, s = "", i = "";
  const c = t.indexOf("#");
  let l = t.indexOf("?");
  return c < l && c >= 0 && (l = -1), l > -1 && (r = t.slice(0, l), s = t.slice(l + 1, c > -1 ? c : t.length), o = e(s)), c > -1 && (r = r || t.slice(0, c), i = t.slice(c, t.length)), r = io(r ?? t, n), {
    fullPath: r + (s && "?") + s + i,
    path: r,
    query: o,
    hash: ce(i)
  };
}
function oo(e, t) {
  const n = t.query ? e(t.query) : "";
  return t.path + (n && "?") + n + (t.hash || "");
}
function Ot(e, t) {
  return !t || !e.toLowerCase().startsWith(t.toLowerCase()) ? e : e.slice(t.length) || "/";
}
function bt(e, t, n) {
  const r = t.matched.length - 1, o = n.matched.length - 1;
  return r > -1 && r === o && ne(t.matched[r], n.matched[o]) && gn(t.params, n.params) && e(t.query) === e(n.query) && t.hash === n.hash;
}
function ne(e, t) {
  return (e.aliasOf || e) === (t.aliasOf || t);
}
function gn(e, t) {
  if (Object.keys(e).length !== Object.keys(t).length)
    return !1;
  for (const n in e)
    if (!so(e[n], t[n]))
      return !1;
  return !0;
}
function so(e, t) {
  return L(e) ? St(e, t) : L(t) ? St(t, e) : e === t;
}
function St(e, t) {
  return L(t) ? e.length === t.length && e.every((n, r) => n === t[r]) : e.length === 1 && e[0] === t;
}
function io(e, t) {
  if (e.startsWith("/"))
    return e;
  if (b.NODE_ENV !== "production" && !t.startsWith("/"))
    return S(`Cannot resolve a relative location without an absolute path. Trying to resolve "${e}" from "${t}". It should look like "/${t}".`), e;
  if (!e)
    return t;
  const n = t.split("/"), r = e.split("/"), o = r[r.length - 1];
  (o === ".." || o === ".") && r.push("");
  let s = n.length - 1, i, c;
  for (i = 0; i < r.length; i++)
    if (c = r[i], c !== ".")
      if (c === "..")
        s > 1 && s--;
      else
        break;
  return n.slice(0, s).join("/") + "/" + r.slice(i).join("/");
}
const Z = {
  path: "/",
  // TODO: could we use a symbol in the future?
  name: void 0,
  params: {},
  query: {},
  hash: "",
  fullPath: "/",
  matched: [],
  meta: {},
  redirectedFrom: void 0
};
var ue;
(function(e) {
  e.pop = "pop", e.push = "push";
})(ue || (ue = {}));
var se;
(function(e) {
  e.back = "back", e.forward = "forward", e.unknown = "";
})(se || (se = {}));
const Ke = "";
function vn(e) {
  if (!e)
    if (z) {
      const t = document.querySelector("base");
      e = t && t.getAttribute("href") || "/", e = e.replace(/^\w+:\/\/[^\/]+/, "");
    } else
      e = "/";
  return e[0] !== "/" && e[0] !== "#" && (e = "/" + e), ro(e);
}
const ao = /^[^#]+#/;
function yn(e, t) {
  return e.replace(ao, "#") + t;
}
function co(e, t) {
  const n = document.documentElement.getBoundingClientRect(), r = e.getBoundingClientRect();
  return {
    behavior: t.behavior,
    left: r.left - n.left - (t.left || 0),
    top: r.top - n.top - (t.top || 0)
  };
}
const je = () => ({
  left: window.scrollX,
  top: window.scrollY
});
function uo(e) {
  let t;
  if ("el" in e) {
    const n = e.el, r = typeof n == "string" && n.startsWith("#");
    if (b.NODE_ENV !== "production" && typeof e.el == "string" && (!r || !document.getElementById(e.el.slice(1))))
      try {
        const s = document.querySelector(e.el);
        if (r && s) {
          S(`The selector "${e.el}" should be passed as "el: document.querySelector('${e.el}')" because it starts with "#".`);
          return;
        }
      } catch {
        S(`The selector "${e.el}" is invalid. If you are using an id selector, make sure to escape it. You can find more information about escaping characters in selectors at https://mathiasbynens.be/notes/css-escapes or use CSS.escape (https://developer.mozilla.org/en-US/docs/Web/API/CSS/escape).`);
        return;
      }
    const o = typeof n == "string" ? r ? document.getElementById(n.slice(1)) : document.querySelector(n) : n;
    if (!o) {
      b.NODE_ENV !== "production" && S(`Couldn't find element using selector "${e.el}" returned by scrollBehavior.`);
      return;
    }
    t = co(o, e);
  } else
    t = e;
  "scrollBehavior" in document.documentElement.style ? window.scrollTo(t) : window.scrollTo(t.left != null ? t.left : window.scrollX, t.top != null ? t.top : window.scrollY);
}
function Pt(e, t) {
  return (history.state ? history.state.position - t : -1) + e;
}
const rt = /* @__PURE__ */ new Map();
function lo(e, t) {
  rt.set(e, t);
}
function fo(e) {
  const t = rt.get(e);
  return rt.delete(e), t;
}
let ho = () => location.protocol + "//" + location.host;
function En(e, t) {
  const { pathname: n, search: r, hash: o } = t, s = e.indexOf("#");
  if (s > -1) {
    let c = o.includes(e.slice(s)) ? e.slice(s).length : 1, l = o.slice(c);
    return l[0] !== "/" && (l = "/" + l), Ot(l, "");
  }
  return Ot(n, e) + r + o;
}
function po(e, t, n, r) {
  let o = [], s = [], i = null;
  const c = ({ state: f }) => {
    const d = En(e, location), p = n.value, v = t.value;
    let g = 0;
    if (f) {
      if (n.value = d, t.value = f, i && i === p) {
        i = null;
        return;
      }
      g = v ? f.position - v.position : 0;
    } else
      r(d);
    o.forEach((y) => {
      y(n.value, p, {
        delta: g,
        type: ue.pop,
        direction: g ? g > 0 ? se.forward : se.back : se.unknown
      });
    });
  };
  function l() {
    i = n.value;
  }
  function h(f) {
    o.push(f);
    const d = () => {
      const p = o.indexOf(f);
      p > -1 && o.splice(p, 1);
    };
    return s.push(d), d;
  }
  function u() {
    const { history: f } = window;
    f.state && f.replaceState(I({}, f.state, { scroll: je() }), "");
  }
  function a() {
    for (const f of s)
      f();
    s = [], window.removeEventListener("popstate", c), window.removeEventListener("beforeunload", u);
  }
  return window.addEventListener("popstate", c), window.addEventListener("beforeunload", u, {
    passive: !0
  }), {
    pauseListeners: l,
    listen: h,
    destroy: a
  };
}
function Vt(e, t, n, r = !1, o = !1) {
  return {
    back: e,
    current: t,
    forward: n,
    replaced: r,
    position: window.history.length,
    scroll: o ? je() : null
  };
}
function mo(e) {
  const { history: t, location: n } = window, r = {
    value: En(e, n)
  }, o = { value: t.state };
  o.value || s(r.value, {
    back: null,
    current: r.value,
    forward: null,
    // the length is off by one, we need to decrease it
    position: t.length - 1,
    replaced: !0,
    // don't add a scroll as the user may have an anchor, and we want
    // scrollBehavior to be triggered without a saved position
    scroll: null
  }, !0);
  function s(l, h, u) {
    const a = e.indexOf("#"), f = a > -1 ? (n.host && document.querySelector("base") ? e : e.slice(a)) + l : ho() + e + l;
    try {
      t[u ? "replaceState" : "pushState"](h, "", f), o.value = h;
    } catch (d) {
      b.NODE_ENV !== "production" ? S("Error with push/replace State", d) : console.error(d), n[u ? "replace" : "assign"](f);
    }
  }
  function i(l, h) {
    const u = I({}, t.state, Vt(
      o.value.back,
      // keep back and forward entries but override current position
      l,
      o.value.forward,
      !0
    ), h, { position: o.value.position });
    s(l, u, !0), r.value = l;
  }
  function c(l, h) {
    const u = I(
      {},
      // use current history state to gracefully handle a wrong call to
      // history.replaceState
      // https://github.com/vuejs/router/issues/366
      o.value,
      t.state,
      {
        forward: l,
        scroll: je()
      }
    );
    b.NODE_ENV !== "production" && !t.state && S(`history.state seems to have been manually replaced without preserving the necessary values. Make sure to preserve existing history state if you are manually calling history.replaceState:

history.replaceState(history.state, '', url)

You can find more information at https://router.vuejs.org/guide/migration/#Usage-of-history-state`), s(u.current, u, !0);
    const a = I({}, Vt(r.value, l, null), { position: u.position + 1 }, h);
    s(l, a, !1), r.value = l;
  }
  return {
    location: r,
    state: o,
    push: c,
    replace: i
  };
}
function wn(e) {
  e = vn(e);
  const t = mo(e), n = po(e, t.state, t.location, t.replace);
  function r(s, i = !0) {
    i || n.pauseListeners(), history.go(s);
  }
  const o = I({
    // it's overridden right after
    location: "",
    base: e,
    go: r,
    createHref: yn.bind(null, e)
  }, t, n);
  return Object.defineProperty(o, "location", {
    enumerable: !0,
    get: () => t.location.value
  }), Object.defineProperty(o, "state", {
    enumerable: !0,
    get: () => t.state.value
  }), o;
}
function go(e = "") {
  let t = [], n = [Ke], r = 0;
  e = vn(e);
  function o(c) {
    r++, r !== n.length && n.splice(r), n.push(c);
  }
  function s(c, l, { direction: h, delta: u }) {
    const a = {
      direction: h,
      delta: u,
      type: ue.pop
    };
    for (const f of t)
      f(c, l, a);
  }
  const i = {
    // rewritten by Object.defineProperty
    location: Ke,
    // TODO: should be kept in queue
    state: {},
    base: e,
    createHref: yn.bind(null, e),
    replace(c) {
      n.splice(r--, 1), o(c);
    },
    push(c, l) {
      o(c);
    },
    listen(c) {
      return t.push(c), () => {
        const l = t.indexOf(c);
        l > -1 && t.splice(l, 1);
      };
    },
    destroy() {
      t = [], n = [Ke], r = 0;
    },
    go(c, l = !0) {
      const h = this.location, u = (
        // we are considering delta === 0 going forward, but in abstract mode
        // using 0 for the delta doesn't make sense like it does in html5 where
        // it reloads the page
        c < 0 ? se.back : se.forward
      );
      r = Math.max(0, Math.min(r + c, n.length - 1)), l && s(this.location, h, {
        direction: u,
        delta: c
      });
    }
  };
  return Object.defineProperty(i, "location", {
    enumerable: !0,
    get: () => n[r]
  }), i;
}
function vo(e) {
  return e = location.host ? e || location.pathname + location.search : "", e.includes("#") || (e += "#"), b.NODE_ENV !== "production" && !e.endsWith("#/") && !e.endsWith("#") && S(`A hash base must end with a "#":
"${e}" should be "${e.replace(/#.*$/, "#")}".`), wn(e);
}
function Ne(e) {
  return typeof e == "string" || e && typeof e == "object";
}
function _n(e) {
  return typeof e == "string" || typeof e == "symbol";
}
const ot = Symbol(b.NODE_ENV !== "production" ? "navigation failure" : "");
var kt;
(function(e) {
  e[e.aborted = 4] = "aborted", e[e.cancelled = 8] = "cancelled", e[e.duplicated = 16] = "duplicated";
})(kt || (kt = {}));
const yo = {
  1({ location: e, currentLocation: t }) {
    return `No match for
 ${JSON.stringify(e)}${t ? `
while being at
` + JSON.stringify(t) : ""}`;
  },
  2({ from: e, to: t }) {
    return `Redirected from "${e.fullPath}" to "${wo(t)}" via a navigation guard.`;
  },
  4({ from: e, to: t }) {
    return `Navigation aborted from "${e.fullPath}" to "${t.fullPath}" via a navigation guard.`;
  },
  8({ from: e, to: t }) {
    return `Navigation cancelled from "${e.fullPath}" to "${t.fullPath}" with a new navigation.`;
  },
  16({ from: e, to: t }) {
    return `Avoided redundant navigation to current location: "${e.fullPath}".`;
  }
};
function le(e, t) {
  return b.NODE_ENV !== "production" ? I(new Error(yo[e](t)), {
    type: e,
    [ot]: !0
  }, t) : I(new Error(), {
    type: e,
    [ot]: !0
  }, t);
}
function q(e, t) {
  return e instanceof Error && ot in e && (t == null || !!(e.type & t));
}
const Eo = ["params", "query", "hash"];
function wo(e) {
  if (typeof e == "string")
    return e;
  if (e.path != null)
    return e.path;
  const t = {};
  for (const n of Eo)
    n in e && (t[n] = e[n]);
  return JSON.stringify(t, null, 2);
}
const Nt = "[^/]+?", _o = {
  sensitive: !1,
  strict: !1,
  start: !0,
  end: !0
}, Ro = /[.+*?^${}()[\]/\\]/g;
function Oo(e, t) {
  const n = I({}, _o, t), r = [];
  let o = n.start ? "^" : "";
  const s = [];
  for (const h of e) {
    const u = h.length ? [] : [
      90
      /* PathScore.Root */
    ];
    n.strict && !h.length && (o += "/");
    for (let a = 0; a < h.length; a++) {
      const f = h[a];
      let d = 40 + (n.sensitive ? 0.25 : 0);
      if (f.type === 0)
        a || (o += "/"), o += f.value.replace(Ro, "\\$&"), d += 40;
      else if (f.type === 1) {
        const { value: p, repeatable: v, optional: g, regexp: y } = f;
        s.push({
          name: p,
          repeatable: v,
          optional: g
        });
        const _ = y || Nt;
        if (_ !== Nt) {
          d += 10;
          try {
            new RegExp(`(${_})`);
          } catch (V) {
            throw new Error(`Invalid custom RegExp for param "${p}" (${_}): ` + V.message);
          }
        }
        let O = v ? `((?:${_})(?:/(?:${_}))*)` : `(${_})`;
        a || (O = // avoid an optional / if there are more segments e.g. /:p?-static
        // or /:p?-:p2
        g && h.length < 2 ? `(?:/${O})` : "/" + O), g && (O += "?"), o += O, d += 20, g && (d += -8), v && (d += -20), _ === ".*" && (d += -50);
      }
      u.push(d);
    }
    r.push(u);
  }
  if (n.strict && n.end) {
    const h = r.length - 1;
    r[h][r[h].length - 1] += 0.7000000000000001;
  }
  n.strict || (o += "/?"), n.end ? o += "$" : n.strict && !o.endsWith("/") && (o += "(?:/|$)");
  const i = new RegExp(o, n.sensitive ? "" : "i");
  function c(h) {
    const u = h.match(i), a = {};
    if (!u)
      return null;
    for (let f = 1; f < u.length; f++) {
      const d = u[f] || "", p = s[f - 1];
      a[p.name] = d && p.repeatable ? d.split("/") : d;
    }
    return a;
  }
  function l(h) {
    let u = "", a = !1;
    for (const f of e) {
      (!a || !u.endsWith("/")) && (u += "/"), a = !1;
      for (const d of f)
        if (d.type === 0)
          u += d.value;
        else if (d.type === 1) {
          const { value: p, repeatable: v, optional: g } = d, y = p in h ? h[p] : "";
          if (L(y) && !v)
            throw new Error(`Provided param "${p}" is an array but it is not repeatable (* or + modifiers)`);
          const _ = L(y) ? y.join("/") : y;
          if (!_)
            if (g)
              f.length < 2 && (u.endsWith("/") ? u = u.slice(0, -1) : a = !0);
            else
              throw new Error(`Missing required param "${p}"`);
          u += _;
        }
    }
    return u || "/";
  }
  return {
    re: i,
    score: r,
    keys: s,
    parse: c,
    stringify: l
  };
}
function bo(e, t) {
  let n = 0;
  for (; n < e.length && n < t.length; ) {
    const r = t[n] - e[n];
    if (r)
      return r;
    n++;
  }
  return e.length < t.length ? e.length === 1 && e[0] === 80 ? -1 : 1 : e.length > t.length ? t.length === 1 && t[0] === 80 ? 1 : -1 : 0;
}
function Rn(e, t) {
  let n = 0;
  const r = e.score, o = t.score;
  for (; n < r.length && n < o.length; ) {
    const s = bo(r[n], o[n]);
    if (s)
      return s;
    n++;
  }
  if (Math.abs(o.length - r.length) === 1) {
    if (It(r))
      return 1;
    if (It(o))
      return -1;
  }
  return o.length - r.length;
}
function It(e) {
  const t = e[e.length - 1];
  return e.length > 0 && t[t.length - 1] < 0;
}
const So = {
  type: 0,
  value: ""
}, Po = /[a-zA-Z0-9_]/;
function Vo(e) {
  if (!e)
    return [[]];
  if (e === "/")
    return [[So]];
  if (!e.startsWith("/"))
    throw new Error(b.NODE_ENV !== "production" ? `Route paths should start with a "/": "${e}" should be "/${e}".` : `Invalid path "${e}"`);
  function t(d) {
    throw new Error(`ERR (${n})/"${h}": ${d}`);
  }
  let n = 0, r = n;
  const o = [];
  let s;
  function i() {
    s && o.push(s), s = [];
  }
  let c = 0, l, h = "", u = "";
  function a() {
    h && (n === 0 ? s.push({
      type: 0,
      value: h
    }) : n === 1 || n === 2 || n === 3 ? (s.length > 1 && (l === "*" || l === "+") && t(`A repeatable param (${h}) must be alone in its segment. eg: '/:ids+.`), s.push({
      type: 1,
      value: h,
      regexp: u,
      repeatable: l === "*" || l === "+",
      optional: l === "*" || l === "?"
    })) : t("Invalid state to consume buffer"), h = "");
  }
  function f() {
    h += l;
  }
  for (; c < e.length; ) {
    if (l = e[c++], l === "\\" && n !== 2) {
      r = n, n = 4;
      continue;
    }
    switch (n) {
      case 0:
        l === "/" ? (h && a(), i()) : l === ":" ? (a(), n = 1) : f();
        break;
      case 4:
        f(), n = r;
        break;
      case 1:
        l === "(" ? n = 2 : Po.test(l) ? f() : (a(), n = 0, l !== "*" && l !== "?" && l !== "+" && c--);
        break;
      case 2:
        l === ")" ? u[u.length - 1] == "\\" ? u = u.slice(0, -1) + l : n = 3 : u += l;
        break;
      case 3:
        a(), n = 0, l !== "*" && l !== "?" && l !== "+" && c--, u = "";
        break;
      default:
        t("Unknown state");
        break;
    }
  }
  return n === 2 && t(`Unfinished custom RegExp for param "${h}"`), a(), i(), o;
}
function ko(e, t, n) {
  const r = Oo(Vo(e.path), n);
  if (b.NODE_ENV !== "production") {
    const s = /* @__PURE__ */ new Set();
    for (const i of r.keys)
      s.has(i.name) && S(`Found duplicated params with name "${i.name}" for path "${e.path}". Only the last one will be available on "$route.params".`), s.add(i.name);
  }
  const o = I(r, {
    record: e,
    parent: t,
    // these needs to be populated by the parent
    children: [],
    alias: []
  });
  return t && !o.record.aliasOf == !t.record.aliasOf && t.children.push(o), o;
}
function No(e, t) {
  const n = [], r = /* @__PURE__ */ new Map();
  t = Tt({ strict: !1, end: !0, sensitive: !1 }, t);
  function o(a) {
    return r.get(a);
  }
  function s(a, f, d) {
    const p = !d, v = At(a);
    b.NODE_ENV !== "production" && $o(v, f), v.aliasOf = d && d.record;
    const g = Tt(t, a), y = [v];
    if ("alias" in a) {
      const V = typeof a.alias == "string" ? [a.alias] : a.alias;
      for (const $ of V)
        y.push(
          // we need to normalize again to ensure the `mods` property
          // being non enumerable
          At(I({}, v, {
            // this allows us to hold a copy of the `components` option
            // so that async components cache is hold on the original record
            components: d ? d.record.components : v.components,
            path: $,
            // we might be the child of an alias
            aliasOf: d ? d.record : v
            // the aliases are always of the same kind as the original since they
            // are defined on the same record
          }))
        );
    }
    let _, O;
    for (const V of y) {
      const { path: $ } = V;
      if (f && $[0] !== "/") {
        const x = f.record.path, U = x[x.length - 1] === "/" ? "" : "/";
        V.path = f.record.path + ($ && U + $);
      }
      if (b.NODE_ENV !== "production" && V.path === "*")
        throw new Error(`Catch all routes ("*") must now be defined using a param with a custom regexp.
See more at https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes.`);
      if (_ = ko(V, f, g), b.NODE_ENV !== "production" && f && $[0] === "/" && jo(_, f), d ? (d.alias.push(_), b.NODE_ENV !== "production" && Ao(d, _)) : (O = O || _, O !== _ && O.alias.push(_), p && a.name && !$t(_) && (b.NODE_ENV !== "production" && To(a, f), i(a.name))), On(_) && l(_), v.children) {
        const x = v.children;
        for (let U = 0; U < x.length; U++)
          s(x[U], _, d && d.children[U]);
      }
      d = d || _;
    }
    return O ? () => {
      i(O);
    } : ve;
  }
  function i(a) {
    if (_n(a)) {
      const f = r.get(a);
      f && (r.delete(a), n.splice(n.indexOf(f), 1), f.children.forEach(i), f.alias.forEach(i));
    } else {
      const f = n.indexOf(a);
      f > -1 && (n.splice(f, 1), a.record.name && r.delete(a.record.name), a.children.forEach(i), a.alias.forEach(i));
    }
  }
  function c() {
    return n;
  }
  function l(a) {
    const f = xo(a, n);
    n.splice(f, 0, a), a.record.name && !$t(a) && r.set(a.record.name, a);
  }
  function h(a, f) {
    let d, p = {}, v, g;
    if ("name" in a && a.name) {
      if (d = r.get(a.name), !d)
        throw le(1, {
          location: a
        });
      if (b.NODE_ENV !== "production") {
        const O = Object.keys(a.params || {}).filter((V) => !d.keys.find(($) => $.name === V));
        O.length && S(`Discarded invalid param(s) "${O.join('", "')}" when navigating. See https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22 for more details.`);
      }
      g = d.record.name, p = I(
        // paramsFromLocation is a new object
        Ct(
          f.params,
          // only keep params that exist in the resolved location
          // only keep optional params coming from a parent record
          d.keys.filter((O) => !O.optional).concat(d.parent ? d.parent.keys.filter((O) => O.optional) : []).map((O) => O.name)
        ),
        // discard any existing params in the current location that do not exist here
        // #1497 this ensures better active/exact matching
        a.params && Ct(a.params, d.keys.map((O) => O.name))
      ), v = d.stringify(p);
    } else if (a.path != null)
      v = a.path, b.NODE_ENV !== "production" && !v.startsWith("/") && S(`The Matcher cannot resolve relative paths but received "${v}". Unless you directly called \`matcher.resolve("${v}")\`, this is probably a bug in vue-router. Please open an issue at https://github.com/vuejs/router/issues/new/choose.`), d = n.find((O) => O.re.test(v)), d && (p = d.parse(v), g = d.record.name);
    else {
      if (d = f.name ? r.get(f.name) : n.find((O) => O.re.test(f.path)), !d)
        throw le(1, {
          location: a,
          currentLocation: f
        });
      g = d.record.name, p = I({}, f.params, a.params), v = d.stringify(p);
    }
    const y = [];
    let _ = d;
    for (; _; )
      y.unshift(_.record), _ = _.parent;
    return {
      name: g,
      path: v,
      params: p,
      matched: y,
      meta: Co(y)
    };
  }
  e.forEach((a) => s(a));
  function u() {
    n.length = 0, r.clear();
  }
  return {
    addRoute: s,
    resolve: h,
    removeRoute: i,
    clearRoutes: u,
    getRoutes: c,
    getRecordMatcher: o
  };
}
function Ct(e, t) {
  const n = {};
  for (const r of t)
    r in e && (n[r] = e[r]);
  return n;
}
function At(e) {
  const t = {
    path: e.path,
    redirect: e.redirect,
    name: e.name,
    meta: e.meta || {},
    aliasOf: e.aliasOf,
    beforeEnter: e.beforeEnter,
    props: Io(e),
    children: e.children || [],
    instances: {},
    leaveGuards: /* @__PURE__ */ new Set(),
    updateGuards: /* @__PURE__ */ new Set(),
    enterCallbacks: {},
    // must be declared afterwards
    // mods: {},
    components: "components" in e ? e.components || null : e.component && { default: e.component }
  };
  return Object.defineProperty(t, "mods", {
    value: {}
  }), t;
}
function Io(e) {
  const t = {}, n = e.props || !1;
  if ("component" in e)
    t.default = n;
  else
    for (const r in e.components)
      t[r] = typeof n == "object" ? n[r] : n;
  return t;
}
function $t(e) {
  for (; e; ) {
    if (e.record.aliasOf)
      return !0;
    e = e.parent;
  }
  return !1;
}
function Co(e) {
  return e.reduce((t, n) => I(t, n.meta), {});
}
function Tt(e, t) {
  const n = {};
  for (const r in e)
    n[r] = r in t ? t[r] : e[r];
  return n;
}
function st(e, t) {
  return e.name === t.name && e.optional === t.optional && e.repeatable === t.repeatable;
}
function Ao(e, t) {
  for (const n of e.keys)
    if (!n.optional && !t.keys.find(st.bind(null, n)))
      return S(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
  for (const n of t.keys)
    if (!n.optional && !e.keys.find(st.bind(null, n)))
      return S(`Alias "${t.record.path}" and the original record: "${e.record.path}" must have the exact same param named "${n.name}"`);
}
function $o(e, t) {
  t && t.record.name && !e.name && !e.path && S(`The route named "${String(t.record.name)}" has a child without a name and an empty path. Using that name won't render the empty path child so you probably want to move the name to the child instead. If this is intentional, add a name to the child route to remove the warning.`);
}
function To(e, t) {
  for (let n = t; n; n = n.parent)
    if (n.record.name === e.name)
      throw new Error(`A route named "${String(e.name)}" has been added as a ${t === n ? "child" : "descendant"} of a route with the same name. Route names must be unique and a nested route cannot use the same name as an ancestor.`);
}
function jo(e, t) {
  for (const n of t.keys)
    if (!e.keys.find(st.bind(null, n)))
      return S(`Absolute path "${e.record.path}" must have the exact same param named "${n.name}" as its parent "${t.record.path}".`);
}
function xo(e, t) {
  let n = 0, r = t.length;
  for (; n !== r; ) {
    const s = n + r >> 1;
    Rn(e, t[s]) < 0 ? r = s : n = s + 1;
  }
  const o = Do(e);
  return o && (r = t.lastIndexOf(o, r - 1), b.NODE_ENV !== "production" && r < 0 && S(`Finding ancestor route "${o.record.path}" failed for "${e.record.path}"`)), r;
}
function Do(e) {
  let t = e;
  for (; t = t.parent; )
    if (On(t) && Rn(e, t) === 0)
      return t;
}
function On({ record: e }) {
  return !!(e.name || e.components && Object.keys(e.components).length || e.redirect);
}
function Mo(e) {
  const t = {};
  if (e === "" || e === "?")
    return t;
  const r = (e[0] === "?" ? e.slice(1) : e).split("&");
  for (let o = 0; o < r.length; ++o) {
    const s = r[o].replace(hn, " "), i = s.indexOf("="), c = ce(i < 0 ? s : s.slice(0, i)), l = i < 0 ? null : ce(s.slice(i + 1));
    if (c in t) {
      let h = t[c];
      L(h) || (h = t[c] = [h]), h.push(l);
    } else
      t[c] = l;
  }
  return t;
}
function jt(e) {
  let t = "";
  for (let n in e) {
    const r = e[n];
    if (n = Zr(n), r == null) {
      r !== void 0 && (t += (t.length ? "&" : "") + n);
      continue;
    }
    (L(r) ? r.map((s) => s && nt(s)) : [r && nt(r)]).forEach((s) => {
      s !== void 0 && (t += (t.length ? "&" : "") + n, s != null && (t += "=" + s));
    });
  }
  return t;
}
function Fo(e) {
  const t = {};
  for (const n in e) {
    const r = e[n];
    r !== void 0 && (t[n] = L(r) ? r.map((o) => o == null ? null : "" + o) : r == null ? r : "" + r);
  }
  return t;
}
const Bo = Symbol(b.NODE_ENV !== "production" ? "router view location matched" : ""), xt = Symbol(b.NODE_ENV !== "production" ? "router view depth" : ""), xe = Symbol(b.NODE_ENV !== "production" ? "router" : ""), dt = Symbol(b.NODE_ENV !== "production" ? "route location" : ""), it = Symbol(b.NODE_ENV !== "production" ? "router view location" : "");
function pe() {
  let e = [];
  function t(r) {
    return e.push(r), () => {
      const o = e.indexOf(r);
      o > -1 && e.splice(o, 1);
    };
  }
  function n() {
    e = [];
  }
  return {
    add: t,
    list: () => e.slice(),
    reset: n
  };
}
function ee(e, t, n, r, o, s = (i) => i()) {
  const i = r && // name is defined if record is because of the function overload
  (r.enterCallbacks[o] = r.enterCallbacks[o] || []);
  return () => new Promise((c, l) => {
    const h = (f) => {
      f === !1 ? l(le(4, {
        from: n,
        to: t
      })) : f instanceof Error ? l(f) : Ne(f) ? l(le(2, {
        from: t,
        to: f
      })) : (i && // since enterCallbackArray is truthy, both record and name also are
      r.enterCallbacks[o] === i && typeof f == "function" && i.push(f), c());
    }, u = s(() => e.call(r && r.instances[o], t, n, b.NODE_ENV !== "production" ? Wo(h, t, n) : h));
    let a = Promise.resolve(u);
    if (e.length < 3 && (a = a.then(h)), b.NODE_ENV !== "production" && e.length > 2) {
      const f = `The "next" callback was never called inside of ${e.name ? '"' + e.name + '"' : ""}:
${e.toString()}
. If you are returning a value instead of calling "next", make sure to remove the "next" parameter from your function.`;
      if (typeof u == "object" && "then" in u)
        a = a.then((d) => h._called ? d : (S(f), Promise.reject(new Error("Invalid navigation guard"))));
      else if (u !== void 0 && !h._called) {
        S(f), l(new Error("Invalid navigation guard"));
        return;
      }
    }
    a.catch((f) => l(f));
  });
}
function Wo(e, t, n) {
  let r = 0;
  return function() {
    r++ === 1 && S(`The "next" callback was called more than once in one navigation guard when going from "${n.fullPath}" to "${t.fullPath}". It should be called exactly one time in each navigation guard. This will fail in production.`), e._called = !0, r === 1 && e.apply(null, arguments);
  };
}
function He(e, t, n, r, o = (s) => s()) {
  const s = [];
  for (const i of e) {
    b.NODE_ENV !== "production" && !i.components && !i.children.length && S(`Record with path "${i.path}" is either missing a "component(s)" or "children" property.`);
    for (const c in i.components) {
      let l = i.components[c];
      if (b.NODE_ENV !== "production") {
        if (!l || typeof l != "object" && typeof l != "function")
          throw S(`Component "${c}" in record with path "${i.path}" is not a valid component. Received "${String(l)}".`), new Error("Invalid route component");
        if ("then" in l) {
          S(`Component "${c}" in record with path "${i.path}" is a Promise instead of a function that returns a Promise. Did you write "import('./MyPage.vue')" instead of "() => import('./MyPage.vue')" ? This will break in production if not fixed.`);
          const h = l;
          l = () => h;
        } else l.__asyncLoader && // warn only once per component
        !l.__warnedDefineAsync && (l.__warnedDefineAsync = !0, S(`Component "${c}" in record with path "${i.path}" is defined using "defineAsyncComponent()". Write "() => import('./MyPage.vue')" instead of "defineAsyncComponent(() => import('./MyPage.vue'))".`));
      }
      if (!(t !== "beforeRouteEnter" && !i.instances[c]))
        if (ln(l)) {
          const u = (l.__vccOpts || l)[t];
          u && s.push(ee(u, n, r, i, c, o));
        } else {
          let h = l();
          b.NODE_ENV !== "production" && !("catch" in h) && (S(`Component "${c}" in record with path "${i.path}" is a function that does not return a Promise. If you were passing a functional component, make sure to add a "displayName" to the component. This will break in production if not fixed.`), h = Promise.resolve(h)), s.push(() => h.then((u) => {
            if (!u)
              throw new Error(`Couldn't resolve component "${c}" at "${i.path}"`);
            const a = Lr(u) ? u.default : u;
            i.mods[c] = u, i.components[c] = a;
            const d = (a.__vccOpts || a)[t];
            return d && ee(d, n, r, i, c, o)();
          }));
        }
    }
  }
  return s;
}
function Dt(e) {
  const t = te(xe), n = te(dt);
  let r = !1, o = null;
  const s = W(() => {
    const u = B(e.to);
    return b.NODE_ENV !== "production" && (!r || u !== o) && (Ne(u) || (r ? S(`Invalid value for prop "to" in useLink()
- to:`, u, `
- previous to:`, o, `
- props:`, e) : S(`Invalid value for prop "to" in useLink()
- to:`, u, `
- props:`, e)), o = u, r = !0), t.resolve(u);
  }), i = W(() => {
    const { matched: u } = s.value, { length: a } = u, f = u[a - 1], d = n.matched;
    if (!f || !d.length)
      return -1;
    const p = d.findIndex(ne.bind(null, f));
    if (p > -1)
      return p;
    const v = Mt(u[a - 2]);
    return (
      // we are dealing with nested routes
      a > 1 && // if the parent and matched route have the same path, this link is
      // referring to the empty child. Or we currently are on a different
      // child of the same parent
      Mt(f) === v && // avoid comparing the child with its parent
      d[d.length - 1].path !== v ? d.findIndex(ne.bind(null, u[a - 2])) : p
    );
  }), c = W(() => i.value > -1 && Ho(n.params, s.value.params)), l = W(() => i.value > -1 && i.value === n.matched.length - 1 && gn(n.params, s.value.params));
  function h(u = {}) {
    if (Ko(u)) {
      const a = t[B(e.replace) ? "replace" : "push"](
        B(e.to)
        // avoid uncaught errors are they are logged anyway
      ).catch(ve);
      return e.viewTransition && typeof document < "u" && "startViewTransition" in document && document.startViewTransition(() => a), a;
    }
    return Promise.resolve();
  }
  if (b.NODE_ENV !== "production" && z) {
    const u = Kt();
    if (u) {
      const a = {
        route: s.value,
        isActive: c.value,
        isExactActive: l.value,
        error: null
      };
      u.__vrl_devtools = u.__vrl_devtools || [], u.__vrl_devtools.push(a), Gt(() => {
        a.route = s.value, a.isActive = c.value, a.isExactActive = l.value, a.error = Ne(B(e.to)) ? null : 'Invalid "to" value';
      }, { flush: "post" });
    }
  }
  return {
    route: s,
    href: W(() => s.value.href),
    isActive: c,
    isExactActive: l,
    navigate: h
  };
}
function Lo(e) {
  return e.length === 1 ? e[0] : e;
}
const Uo = /* @__PURE__ */ F({
  name: "RouterLink",
  compatConfig: { MODE: 3 },
  props: {
    to: {
      type: [String, Object],
      required: !0
    },
    replace: Boolean,
    activeClass: String,
    // inactiveClass: String,
    exactActiveClass: String,
    custom: Boolean,
    ariaCurrentValue: {
      type: String,
      default: "page"
    }
  },
  useLink: Dt,
  setup(e, { slots: t }) {
    const n = Un(Dt(e)), { options: r } = te(xe), o = W(() => ({
      [Ft(e.activeClass, r.linkActiveClass, "router-link-active")]: n.isActive,
      // [getLinkClass(
      //   props.inactiveClass,
      //   options.linkInactiveClass,
      //   'router-link-inactive'
      // )]: !link.isExactActive,
      [Ft(e.exactActiveClass, r.linkExactActiveClass, "router-link-exact-active")]: n.isExactActive
    }));
    return () => {
      const s = t.default && Lo(t.default(n));
      return e.custom ? s : A("a", {
        "aria-current": n.isExactActive ? e.ariaCurrentValue : null,
        href: n.href,
        // this would override user added attrs but Vue will still add
        // the listener, so we end up triggering both
        onClick: n.navigate,
        class: o.value
      }, s);
    };
  }
}), Go = Uo;
function Ko(e) {
  if (!(e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) && !e.defaultPrevented && !(e.button !== void 0 && e.button !== 0)) {
    if (e.currentTarget && e.currentTarget.getAttribute) {
      const t = e.currentTarget.getAttribute("target");
      if (/\b_blank\b/i.test(t))
        return;
    }
    return e.preventDefault && e.preventDefault(), !0;
  }
}
function Ho(e, t) {
  for (const n in t) {
    const r = t[n], o = e[n];
    if (typeof r == "string") {
      if (r !== o)
        return !1;
    } else if (!L(o) || o.length !== r.length || r.some((s, i) => s !== o[i]))
      return !1;
  }
  return !0;
}
function Mt(e) {
  return e ? e.aliasOf ? e.aliasOf.path : e.path : "";
}
const Ft = (e, t, n) => e ?? t ?? n, qo = /* @__PURE__ */ F({
  name: "RouterView",
  // #674 we manually inherit them
  inheritAttrs: !1,
  props: {
    name: {
      type: String,
      default: "default"
    },
    route: Object
  },
  // Better compat for @vue/compat users
  // https://github.com/vuejs/router/issues/1315
  compatConfig: { MODE: 3 },
  setup(e, { attrs: t, slots: n }) {
    b.NODE_ENV !== "production" && Jo();
    const r = te(it), o = W(() => e.route || r.value), s = te(xt, 0), i = W(() => {
      let h = B(s);
      const { matched: u } = o.value;
      let a;
      for (; (a = u[h]) && !a.components; )
        h++;
      return h;
    }), c = W(() => o.value.matched[i.value]);
    Pe(xt, W(() => i.value + 1)), Pe(Bo, c), Pe(it, o);
    const l = J();
    return K(() => [l.value, c.value, e.name], ([h, u, a], [f, d, p]) => {
      u && (u.instances[a] = h, d && d !== u && h && h === f && (u.leaveGuards.size || (u.leaveGuards = d.leaveGuards), u.updateGuards.size || (u.updateGuards = d.updateGuards))), h && u && // if there is no instance but to and from are the same this might be
      // the first visit
      (!d || !ne(u, d) || !f) && (u.enterCallbacks[a] || []).forEach((v) => v(h));
    }, { flush: "post" }), () => {
      const h = o.value, u = e.name, a = c.value, f = a && a.components[u];
      if (!f)
        return Bt(n.default, { Component: f, route: h });
      const d = a.props[u], p = d ? d === !0 ? h.params : typeof d == "function" ? d(h) : d : null, g = A(f, I({}, p, t, {
        onVnodeUnmounted: (y) => {
          y.component.isUnmounted && (a.instances[u] = null);
        },
        ref: l
      }));
      if (b.NODE_ENV !== "production" && z && g.ref) {
        const y = {
          depth: i.value,
          name: a.name,
          path: a.path,
          meta: a.meta
        };
        (L(g.ref) ? g.ref.map((O) => O.i) : [g.ref.i]).forEach((O) => {
          O.__vrv_devtools = y;
        });
      }
      return (
        // pass the vnode to the slot as a prop.
        // h and <component :is="..."> both accept vnodes
        Bt(n.default, { Component: g, route: h }) || g
      );
    };
  }
});
function Bt(e, t) {
  if (!e)
    return null;
  const n = e(t);
  return n.length === 1 ? n[0] : n;
}
const zo = qo;
function Jo() {
  const e = Kt(), t = e.parent && e.parent.type.name, n = e.parent && e.parent.subTree && e.parent.subTree.type;
  if (t && (t === "KeepAlive" || t.includes("Transition")) && typeof n == "object" && n.name === "RouterView") {
    const r = t === "KeepAlive" ? "keep-alive" : "transition";
    S(`<router-view> can no longer be used directly inside <transition> or <keep-alive>.
Use slot props instead:

<router-view v-slot="{ Component }">
  <${r}>
    <component :is="Component" />
  </${r}>
</router-view>`);
  }
}
function me(e, t) {
  const n = I({}, e, {
    // remove variables that can contain vue instances
    matched: e.matched.map((r) => is(r, ["instances", "children", "aliasOf"]))
  });
  return {
    _custom: {
      type: null,
      readOnly: !0,
      display: e.fullPath,
      tooltip: t,
      value: n
    }
  };
}
function Se(e) {
  return {
    _custom: {
      display: e
    }
  };
}
let Qo = 0;
function Yo(e, t, n) {
  if (t.__hasDevtools)
    return;
  t.__hasDevtools = !0;
  const r = Qo++;
  Wr({
    id: "org.vuejs.router" + (r ? "." + r : ""),
    label: "Vue Router",
    packageName: "vue-router",
    homepage: "https://router.vuejs.org",
    logo: "https://router.vuejs.org/logo.png",
    componentStateTypes: ["Routing"],
    app: e
  }, (o) => {
    typeof o.now != "function" && console.warn("[Vue Router]: You seem to be using an outdated version of Vue Devtools. Are you still using the Beta release instead of the stable one? You can find the links at https://devtools.vuejs.org/guide/installation.html."), o.on.inspectComponent((u, a) => {
      u.instanceData && u.instanceData.state.push({
        type: "Routing",
        key: "$route",
        editable: !1,
        value: me(t.currentRoute.value, "Current Route")
      });
    }), o.on.visitComponentTree(({ treeNode: u, componentInstance: a }) => {
      if (a.__vrv_devtools) {
        const f = a.__vrv_devtools;
        u.tags.push({
          label: (f.name ? `${f.name.toString()}: ` : "") + f.path,
          textColor: 0,
          tooltip: "This component is rendered by &lt;router-view&gt;",
          backgroundColor: bn
        });
      }
      L(a.__vrl_devtools) && (a.__devtoolsApi = o, a.__vrl_devtools.forEach((f) => {
        let d = f.route.path, p = Vn, v = "", g = 0;
        f.error ? (d = f.error, p = ns, g = rs) : f.isExactActive ? (p = Pn, v = "This is exactly active") : f.isActive && (p = Sn, v = "This link is active"), u.tags.push({
          label: d,
          textColor: g,
          tooltip: v,
          backgroundColor: p
        });
      }));
    }), K(t.currentRoute, () => {
      l(), o.notifyComponentUpdate(), o.sendInspectorTree(c), o.sendInspectorState(c);
    });
    const s = "router:navigations:" + r;
    o.addTimelineLayer({
      id: s,
      label: `Router${r ? " " + r : ""} Navigations`,
      color: 4237508
    }), t.onError((u, a) => {
      o.addTimelineEvent({
        layerId: s,
        event: {
          title: "Error during Navigation",
          subtitle: a.fullPath,
          logType: "error",
          time: o.now(),
          data: { error: u },
          groupId: a.meta.__navigationId
        }
      });
    });
    let i = 0;
    t.beforeEach((u, a) => {
      const f = {
        guard: Se("beforeEach"),
        from: me(a, "Current Location during this navigation"),
        to: me(u, "Target location")
      };
      Object.defineProperty(u.meta, "__navigationId", {
        value: i++
      }), o.addTimelineEvent({
        layerId: s,
        event: {
          time: o.now(),
          title: "Start of navigation",
          subtitle: u.fullPath,
          data: f,
          groupId: u.meta.__navigationId
        }
      });
    }), t.afterEach((u, a, f) => {
      const d = {
        guard: Se("afterEach")
      };
      f ? (d.failure = {
        _custom: {
          type: Error,
          readOnly: !0,
          display: f ? f.message : "",
          tooltip: "Navigation Failure",
          value: f
        }
      }, d.status = Se("❌")) : d.status = Se("✅"), d.from = me(a, "Current Location during this navigation"), d.to = me(u, "Target location"), o.addTimelineEvent({
        layerId: s,
        event: {
          title: "End of navigation",
          subtitle: u.fullPath,
          time: o.now(),
          data: d,
          logType: f ? "warning" : "default",
          groupId: u.meta.__navigationId
        }
      });
    });
    const c = "router-inspector:" + r;
    o.addInspector({
      id: c,
      label: "Routes" + (r ? " " + r : ""),
      icon: "book",
      treeFilterPlaceholder: "Search routes"
    });
    function l() {
      if (!h)
        return;
      const u = h;
      let a = n.getRoutes().filter((f) => !f.parent || // these routes have a parent with no component which will not appear in the view
      // therefore we still need to include them
      !f.parent.record.components);
      a.forEach(In), u.filter && (a = a.filter((f) => (
        // save matches state based on the payload
        at(f, u.filter.toLowerCase())
      ))), a.forEach((f) => Nn(f, t.currentRoute.value)), u.rootNodes = a.map(kn);
    }
    let h;
    o.on.getInspectorTree((u) => {
      h = u, u.app === e && u.inspectorId === c && l();
    }), o.on.getInspectorState((u) => {
      if (u.app === e && u.inspectorId === c) {
        const f = n.getRoutes().find((d) => d.record.__vd_id === u.nodeId);
        f && (u.state = {
          options: Zo(f)
        });
      }
    }), o.sendInspectorTree(c), o.sendInspectorState(c);
  });
}
function Xo(e) {
  return e.optional ? e.repeatable ? "*" : "?" : e.repeatable ? "+" : "";
}
function Zo(e) {
  const { record: t } = e, n = [
    { editable: !1, key: "path", value: t.path }
  ];
  return t.name != null && n.push({
    editable: !1,
    key: "name",
    value: t.name
  }), n.push({ editable: !1, key: "regexp", value: e.re }), e.keys.length && n.push({
    editable: !1,
    key: "keys",
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.keys.map((r) => `${r.name}${Xo(r)}`).join(" "),
        tooltip: "Param keys",
        value: e.keys
      }
    }
  }), t.redirect != null && n.push({
    editable: !1,
    key: "redirect",
    value: t.redirect
  }), e.alias.length && n.push({
    editable: !1,
    key: "aliases",
    value: e.alias.map((r) => r.record.path)
  }), Object.keys(e.record.meta).length && n.push({
    editable: !1,
    key: "meta",
    value: e.record.meta
  }), n.push({
    key: "score",
    editable: !1,
    value: {
      _custom: {
        type: null,
        readOnly: !0,
        display: e.score.map((r) => r.join(", ")).join(" | "),
        tooltip: "Score used to sort routes",
        value: e.score
      }
    }
  }), n;
}
const bn = 15485081, Sn = 2450411, Pn = 8702998, es = 2282478, Vn = 16486972, ts = 6710886, ns = 16704226, rs = 12131356;
function kn(e) {
  const t = [], { record: n } = e;
  n.name != null && t.push({
    label: String(n.name),
    textColor: 0,
    backgroundColor: es
  }), n.aliasOf && t.push({
    label: "alias",
    textColor: 0,
    backgroundColor: Vn
  }), e.__vd_match && t.push({
    label: "matches",
    textColor: 0,
    backgroundColor: bn
  }), e.__vd_exactActive && t.push({
    label: "exact",
    textColor: 0,
    backgroundColor: Pn
  }), e.__vd_active && t.push({
    label: "active",
    textColor: 0,
    backgroundColor: Sn
  }), n.redirect && t.push({
    label: typeof n.redirect == "string" ? `redirect: ${n.redirect}` : "redirects",
    textColor: 16777215,
    backgroundColor: ts
  });
  let r = n.__vd_id;
  return r == null && (r = String(os++), n.__vd_id = r), {
    id: r,
    label: n.path,
    tags: t,
    children: e.children.map(kn)
  };
}
let os = 0;
const ss = /^\/(.*)\/([a-z]*)$/;
function Nn(e, t) {
  const n = t.matched.length && ne(t.matched[t.matched.length - 1], e.record);
  e.__vd_exactActive = e.__vd_active = n, n || (e.__vd_active = t.matched.some((r) => ne(r, e.record))), e.children.forEach((r) => Nn(r, t));
}
function In(e) {
  e.__vd_match = !1, e.children.forEach(In);
}
function at(e, t) {
  const n = String(e.re).match(ss);
  if (e.__vd_match = !1, !n || n.length < 3)
    return !1;
  if (new RegExp(n[1].replace(/\$$/, ""), n[2]).test(t))
    return e.children.forEach((i) => at(i, t)), e.record.path !== "/" || t === "/" ? (e.__vd_match = e.re.test(t), !0) : !1;
  const o = e.record.path.toLowerCase(), s = ce(o);
  return !t.startsWith("/") && (s.includes(t) || o.includes(t)) || s.startsWith(t) || o.startsWith(t) || e.record.name && String(e.record.name).includes(t) ? !0 : e.children.some((i) => at(i, t));
}
function is(e, t) {
  const n = {};
  for (const r in e)
    t.includes(r) || (n[r] = e[r]);
  return n;
}
function as(e) {
  const t = No(e.routes, e), n = e.parseQuery || Mo, r = e.stringifyQuery || jt, o = e.history;
  if (b.NODE_ENV !== "production" && !o)
    throw new Error('Provide the "history" option when calling "createRouter()": https://router.vuejs.org/api/interfaces/RouterOptions.html#history');
  const s = pe(), i = pe(), c = pe(), l = Q(Z);
  let h = Z;
  z && e.scrollBehavior && "scrollRestoration" in history && (history.scrollRestoration = "manual");
  const u = Ue.bind(null, (m) => "" + m), a = Ue.bind(null, to), f = (
    // @ts-expect-error: intentionally avoid the type check
    Ue.bind(null, ce)
  );
  function d(m, w) {
    let E, R;
    return _n(m) ? (E = t.getRecordMatcher(m), b.NODE_ENV !== "production" && !E && S(`Parent route "${String(m)}" not found when adding child route`, w), R = w) : R = m, t.addRoute(R, E);
  }
  function p(m) {
    const w = t.getRecordMatcher(m);
    w ? t.removeRoute(w) : b.NODE_ENV !== "production" && S(`Cannot remove non-existent route "${String(m)}"`);
  }
  function v() {
    return t.getRoutes().map((m) => m.record);
  }
  function g(m) {
    return !!t.getRecordMatcher(m);
  }
  function y(m, w) {
    if (w = I({}, w || l.value), typeof m == "string") {
      const P = Ge(n, m, w.path), T = t.resolve({ path: P.path }, w), re = o.createHref(P.fullPath);
      return b.NODE_ENV !== "production" && (re.startsWith("//") ? S(`Location "${m}" resolved to "${re}". A resolved location cannot start with multiple slashes.`) : T.matched.length || S(`No match found for location with path "${m}"`)), I(P, T, {
        params: f(T.params),
        hash: ce(P.hash),
        redirectedFrom: void 0,
        href: re
      });
    }
    if (b.NODE_ENV !== "production" && !Ne(m))
      return S(`router.resolve() was passed an invalid location. This will fail in production.
- Location:`, m), y({});
    let E;
    if (m.path != null)
      b.NODE_ENV !== "production" && "params" in m && !("name" in m) && // @ts-expect-error: the type is never
      Object.keys(m.params).length && S(`Path "${m.path}" was passed with params but they will be ignored. Use a named route alongside params instead.`), E = I({}, m, {
        path: Ge(n, m.path, w.path).path
      });
    else {
      const P = I({}, m.params);
      for (const T in P)
        P[T] == null && delete P[T];
      E = I({}, m, {
        params: a(P)
      }), w.params = a(w.params);
    }
    const R = t.resolve(E, w), C = m.hash || "";
    b.NODE_ENV !== "production" && C && !C.startsWith("#") && S(`A \`hash\` should always start with the character "#". Replace "${C}" with "#${C}".`), R.params = u(f(R.params));
    const j = oo(r, I({}, m, {
      hash: Xr(C),
      path: R.path
    })), k = o.createHref(j);
    return b.NODE_ENV !== "production" && (k.startsWith("//") ? S(`Location "${m}" resolved to "${k}". A resolved location cannot start with multiple slashes.`) : R.matched.length || S(`No match found for location with path "${m.path != null ? m.path : m}"`)), I({
      fullPath: j,
      // keep the hash encoded so fullPath is effectively path + encodedQuery +
      // hash
      hash: C,
      query: (
        // if the user is using a custom query lib like qs, we might have
        // nested objects, so we keep the query as is, meaning it can contain
        // numbers at `$route.query`, but at the point, the user will have to
        // use their own type anyway.
        // https://github.com/vuejs/router/issues/328#issuecomment-649481567
        r === jt ? Fo(m.query) : m.query || {}
      )
    }, R, {
      redirectedFrom: void 0,
      href: k
    });
  }
  function _(m) {
    return typeof m == "string" ? Ge(n, m, l.value.path) : I({}, m);
  }
  function O(m, w) {
    if (h !== m)
      return le(8, {
        from: w,
        to: m
      });
  }
  function V(m) {
    return U(m);
  }
  function $(m) {
    return V(I(_(m), { replace: !0 }));
  }
  function x(m) {
    const w = m.matched[m.matched.length - 1];
    if (w && w.redirect) {
      const { redirect: E } = w;
      let R = typeof E == "function" ? E(m) : E;
      if (typeof R == "string" && (R = R.includes("?") || R.includes("#") ? R = _(R) : (
        // force empty params
        { path: R }
      ), R.params = {}), b.NODE_ENV !== "production" && R.path == null && !("name" in R))
        throw S(`Invalid redirect found:
${JSON.stringify(R, null, 2)}
 when navigating to "${m.fullPath}". A redirect must contain a name or path. This will break in production.`), new Error("Invalid redirect");
      return I({
        query: m.query,
        hash: m.hash,
        // avoid transferring params if the redirect has a path
        params: R.path != null ? {} : m.params
      }, R);
    }
  }
  function U(m, w) {
    const E = h = y(m), R = l.value, C = m.state, j = m.force, k = m.replace === !0, P = x(E);
    if (P)
      return U(
        I(_(P), {
          state: typeof P == "object" ? I({}, C, P.state) : C,
          force: j,
          replace: k
        }),
        // keep original redirectedFrom if it exists
        w || E
      );
    const T = E;
    T.redirectedFrom = w;
    let re;
    return !j && bt(r, R, E) && (re = le(16, { to: T, from: R }), yt(
      R,
      R,
      // this is a push, the only way for it to be triggered from a
      // history.listen is with a redirect, which makes it become a push
      !0,
      // This cannot be the first navigation because the initial location
      // cannot be manually navigated to
      !1
    )), (re ? Promise.resolve(re) : pt(T, R)).catch((D) => q(D) ? (
      // navigation redirects still mark the router as ready
      q(
        D,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? D : Be(D)
    ) : (
      // reject any unknown error
      Fe(D, T, R)
    )).then((D) => {
      if (D) {
        if (q(
          D,
          2
          /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
        ))
          return b.NODE_ENV !== "production" && // we are redirecting to the same location we were already at
          bt(r, y(D.to), T) && // and we have done it a couple of times
          w && // @ts-expect-error: added only in dev
          (w._count = w._count ? (
            // @ts-expect-error
            w._count + 1
          ) : 1) > 30 ? (S(`Detected a possibly infinite redirection in a navigation guard when going from "${R.fullPath}" to "${T.fullPath}". Aborting to avoid a Stack Overflow.
 Are you always returning a new location within a navigation guard? That would lead to this error. Only return when redirecting or aborting, that should fix this. This might break in production if not fixed.`), Promise.reject(new Error("Infinite redirect in navigation guard"))) : U(
            // keep options
            I({
              // preserve an existing replacement but allow the redirect to override it
              replace: k
            }, _(D.to), {
              state: typeof D.to == "object" ? I({}, C, D.to.state) : C,
              force: j
            }),
            // preserve the original redirectedFrom if any
            w || T
          );
      } else
        D = gt(T, R, !0, k, C);
      return mt(T, R, D), D;
    });
  }
  function jn(m, w) {
    const E = O(m, w);
    return E ? Promise.reject(E) : Promise.resolve();
  }
  function De(m) {
    const w = Oe.values().next().value;
    return w && typeof w.runWithContext == "function" ? w.runWithContext(m) : m();
  }
  function pt(m, w) {
    let E;
    const [R, C, j] = cs(m, w);
    E = He(R.reverse(), "beforeRouteLeave", m, w);
    for (const P of R)
      P.leaveGuards.forEach((T) => {
        E.push(ee(T, m, w));
      });
    const k = jn.bind(null, m, w);
    return E.push(k), ie(E).then(() => {
      E = [];
      for (const P of s.list())
        E.push(ee(P, m, w));
      return E.push(k), ie(E);
    }).then(() => {
      E = He(C, "beforeRouteUpdate", m, w);
      for (const P of C)
        P.updateGuards.forEach((T) => {
          E.push(ee(T, m, w));
        });
      return E.push(k), ie(E);
    }).then(() => {
      E = [];
      for (const P of j)
        if (P.beforeEnter)
          if (L(P.beforeEnter))
            for (const T of P.beforeEnter)
              E.push(ee(T, m, w));
          else
            E.push(ee(P.beforeEnter, m, w));
      return E.push(k), ie(E);
    }).then(() => (m.matched.forEach((P) => P.enterCallbacks = {}), E = He(j, "beforeRouteEnter", m, w, De), E.push(k), ie(E))).then(() => {
      E = [];
      for (const P of i.list())
        E.push(ee(P, m, w));
      return E.push(k), ie(E);
    }).catch((P) => q(
      P,
      8
      /* ErrorTypes.NAVIGATION_CANCELLED */
    ) ? P : Promise.reject(P));
  }
  function mt(m, w, E) {
    c.list().forEach((R) => De(() => R(m, w, E)));
  }
  function gt(m, w, E, R, C) {
    const j = O(m, w);
    if (j)
      return j;
    const k = w === Z, P = z ? history.state : {};
    E && (R || k ? o.replace(m.fullPath, I({
      scroll: k && P && P.scroll
    }, C)) : o.push(m.fullPath, C)), l.value = m, yt(m, w, E, k), Be();
  }
  let fe;
  function xn() {
    fe || (fe = o.listen((m, w, E) => {
      if (!Et.listening)
        return;
      const R = y(m), C = x(R);
      if (C) {
        U(I(C, { replace: !0, force: !0 }), R).catch(ve);
        return;
      }
      h = R;
      const j = l.value;
      z && lo(Pt(j.fullPath, E.delta), je()), pt(R, j).catch((k) => q(
        k,
        12
        /* ErrorTypes.NAVIGATION_CANCELLED */
      ) ? k : q(
        k,
        2
        /* ErrorTypes.NAVIGATION_GUARD_REDIRECT */
      ) ? (U(
        I(_(k.to), {
          force: !0
        }),
        R
        // avoid an uncaught rejection, let push call triggerError
      ).then((P) => {
        q(
          P,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && !E.delta && E.type === ue.pop && o.go(-1, !1);
      }).catch(ve), Promise.reject()) : (E.delta && o.go(-E.delta, !1), Fe(k, R, j))).then((k) => {
        k = k || gt(
          // after navigation, all matched components are resolved
          R,
          j,
          !1
        ), k && (E.delta && // a new navigation has been triggered, so we do not want to revert, that will change the current history
        // entry while a different route is displayed
        !q(
          k,
          8
          /* ErrorTypes.NAVIGATION_CANCELLED */
        ) ? o.go(-E.delta, !1) : E.type === ue.pop && q(
          k,
          20
          /* ErrorTypes.NAVIGATION_DUPLICATED */
        ) && o.go(-1, !1)), mt(R, j, k);
      }).catch(ve);
    }));
  }
  let Me = pe(), vt = pe(), Re;
  function Fe(m, w, E) {
    Be(m);
    const R = vt.list();
    return R.length ? R.forEach((C) => C(m, w, E)) : (b.NODE_ENV !== "production" && S("uncaught error during route navigation:"), console.error(m)), Promise.reject(m);
  }
  function Dn() {
    return Re && l.value !== Z ? Promise.resolve() : new Promise((m, w) => {
      Me.add([m, w]);
    });
  }
  function Be(m) {
    return Re || (Re = !m, xn(), Me.list().forEach(([w, E]) => m ? E(m) : w()), Me.reset()), m;
  }
  function yt(m, w, E, R) {
    const { scrollBehavior: C } = e;
    if (!z || !C)
      return Promise.resolve();
    const j = !E && fo(Pt(m.fullPath, 0)) || (R || !E) && history.state && history.state.scroll || null;
    return Ve().then(() => C(m, w, j)).then((k) => k && uo(k)).catch((k) => Fe(k, m, w));
  }
  const We = (m) => o.go(m);
  let Le;
  const Oe = /* @__PURE__ */ new Set(), Et = {
    currentRoute: l,
    listening: !0,
    addRoute: d,
    removeRoute: p,
    clearRoutes: t.clearRoutes,
    hasRoute: g,
    getRoutes: v,
    resolve: y,
    options: e,
    push: V,
    replace: $,
    go: We,
    back: () => We(-1),
    forward: () => We(1),
    beforeEach: s.add,
    beforeResolve: i.add,
    afterEach: c.add,
    onError: vt.add,
    isReady: Dn,
    install(m) {
      const w = this;
      m.component("RouterLink", Go), m.component("RouterView", zo), m.config.globalProperties.$router = w, Object.defineProperty(m.config.globalProperties, "$route", {
        enumerable: !0,
        get: () => B(l)
      }), z && // used for the initial navigation client side to avoid pushing
      // multiple times when the router is used in multiple apps
      !Le && l.value === Z && (Le = !0, V(o.location).catch((C) => {
        b.NODE_ENV !== "production" && S("Unexpected error when starting the router:", C);
      }));
      const E = {};
      for (const C in Z)
        Object.defineProperty(E, C, {
          get: () => l.value[C],
          enumerable: !0
        });
      m.provide(xe, w), m.provide(dt, Ln(E)), m.provide(it, l);
      const R = m.unmount;
      Oe.add(m), m.unmount = function() {
        Oe.delete(m), Oe.size < 1 && (h = Z, fe && fe(), fe = null, l.value = Z, Le = !1, Re = !1), R();
      }, b.NODE_ENV !== "production" && z && Yo(m, w, t);
    }
  };
  function ie(m) {
    return m.reduce((w, E) => w.then(() => De(E)), Promise.resolve());
  }
  return Et;
}
function cs(e, t) {
  const n = [], r = [], o = [], s = Math.max(t.matched.length, e.matched.length);
  for (let i = 0; i < s; i++) {
    const c = t.matched[i];
    c && (e.matched.find((h) => ne(h, c)) ? r.push(c) : n.push(c));
    const l = e.matched[i];
    l && (t.matched.find((h) => ne(h, l)) || o.push(l));
  }
  return [n, r, o];
}
function us() {
  return te(xe);
}
function ls(e) {
  return te(dt);
}
function Y(e) {
  let t = Yt(), n = Rr(), r = kr(e), o = en(), s = us(), i = ls();
  function c(p) {
    p.scopeSnapshot && (t = p.scopeSnapshot), p.slotSnapshot && (n = p.slotSnapshot), p.vforSnapshot && (r = p.vforSnapshot), p.elementRefSnapshot && (o = p.elementRefSnapshot), p.routerSnapshot && (s = p.routerSnapshot);
  }
  function l(p) {
    if (N.isVar(p))
      return H(h(p));
    if (N.isVForItem(p))
      return Ir(p.fid) ? r.getVForIndex(p.fid) : H(h(p));
    if (N.isVForIndex(p))
      return r.getVForIndex(p.fid);
    if (N.isJs(p)) {
      const { code: v, bind: g } = p, y = Te(g, (_) => u(_));
      return $r(v, y)();
    }
    if (N.isSlotProp(p))
      return n.getPropsValue(p);
    if (N.isRouterParams(p))
      return H(h(p));
    throw new Error(`Invalid binding: ${p}`);
  }
  function h(p) {
    if (N.isVar(p)) {
      const v = t.getVueRef(p) || pr(p);
      return _t(v, {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    if (N.isVForItem(p))
      return Nr({
        binding: p,
        vforSnapshot: r
      });
    if (N.isVForIndex(p))
      return () => l(p);
    if (N.isRouterParams(p)) {
      const { prop: v = "params" } = p;
      return _t(() => i[v], {
        paths: p.path,
        getBindableValueFn: l
      });
    }
    throw new Error(`Invalid binding: ${p}`);
  }
  function u(p) {
    if (N.isVar(p) || N.isVForItem(p))
      return h(p);
    if (N.isVForIndex(p))
      return l(p);
    if (N.isJs(p))
      return null;
    if (N.isRouterParams(p))
      return h(p);
    throw new Error(`Invalid binding: ${p}`);
  }
  function a(p) {
    if (N.isVar(p))
      return {
        sid: p.sid,
        id: p.id
      };
    if (N.isVForItem(p))
      return {
        type: "vf",
        fid: p.fid
      };
    if (N.isVForIndex(p))
      return {
        type: "vf-i",
        fid: p.fid,
        value: null
      };
    if (N.isJs(p))
      return null;
  }
  function f(p) {
    var v, g;
    (v = p.vars) == null || v.forEach((y) => {
      h({ type: "ref", ...y }).value = y.val;
    }), (g = p.ele_refs) == null || g.forEach((y) => {
      o.getRef({
        sid: y.sid,
        id: y.id
      }).value[y.method](...y.args);
    });
  }
  function d(p, v) {
    if (Rt(v) || Rt(p.values))
      return;
    v = v;
    const g = p.values, y = p.skips || new Array(v.length).fill(0);
    v.forEach((_, O) => {
      if (y[O] === 1)
        return;
      if (N.isVar(_)) {
        const $ = h(_);
        $.value = g[O];
        return;
      }
      if (N.isRouterAction(_)) {
        const $ = g[O], x = s[$.fn];
        x(...$.args);
        return;
      }
      if (N.isElementRef(_)) {
        const $ = o.getRef(_).value, x = g[O];
        $[x.method](...x.args);
        return;
      }
      if (N.isJsOutput(_)) {
        const $ = g[O], x = G($);
        typeof x == "function" && x();
        return;
      }
      const V = h(_);
      V.value = g[O];
    });
  }
  return {
    getObjectToValue: l,
    getVueRefObject: h,
    getVueRefObjectOrValue: u,
    getBindingServerInfo: a,
    updateRefFromServer: f,
    updateEventRefFromServer: d,
    replaceSnapshot: c
  };
}
function fs(e, t, n) {
  return new hs(e, t, n);
}
class hs {
  constructor(t, n, r) {
    M(this, "taskQueue", []);
    M(this, "id2TaskMap", /* @__PURE__ */ new Map());
    M(this, "input2TaskIdMap", ye(() => []));
    this.snapshots = r;
    const o = [], s = (i) => {
      var l;
      const c = new ds(i, r);
      return this.id2TaskMap.set(c.id, c), (l = i.inputs) == null || l.forEach((h) => {
        const u = `${h.sid}-${h.id}`;
        this.input2TaskIdMap.getOrDefault(u).push(c.id);
      }), c;
    };
    t == null || t.forEach((i) => {
      const c = s(i);
      o.push(c);
    }), n == null || n.forEach((i) => {
      const c = {
        type: "ref",
        sid: i.sid,
        id: i.id
      }, l = {
        ...i,
        immediate: !0,
        outputs: [c, ...i.outputs || []]
      }, h = s(l);
      o.push(h);
    }), o.forEach((i) => {
      const {
        deep: c = !0,
        once: l,
        flush: h,
        immediate: u = !0
      } = i.watchConfig, a = {
        immediate: u,
        deep: c,
        once: l,
        flush: h
      }, f = this._getWatchTargets(i);
      K(
        f,
        ([d]) => {
          i.modify = !0, this.taskQueue.push(new ps(i)), this._scheduleNextTick();
        },
        a
      );
    });
  }
  _getWatchTargets(t) {
    if (!t.watchConfig.inputs)
      return [];
    const n = t.slientInputs;
    return t.watchConfig.inputs.filter(
      (o, s) => (N.isVar(o) || N.isVForItem(o) || N.isRouterParams(o)) && !n[s]
    ).map((o) => this.snapshots.getVueRefObjectOrValue(o));
  }
  _scheduleNextTick() {
    Ve(() => this._runAllTasks());
  }
  _runAllTasks() {
    const t = this.taskQueue.slice();
    this.taskQueue.length = 0, this._setTaskNodeRelations(t), t.forEach((n) => {
      n.run();
    });
  }
  _setTaskNodeRelations(t) {
    t.forEach((n) => {
      const r = this._findNextNodes(n, t);
      n.appendNextNodes(...r), r.forEach((o) => {
        o.appendPrevNodes(n);
      });
    });
  }
  _findNextNodes(t, n) {
    const r = t.watchTask.watchConfig.outputs;
    if (r && r.length <= 0)
      return [];
    const o = this._getCalculatorTasksByOutput(
      t.watchTask.watchConfig.outputs
    );
    return n.filter(
      (s) => o.has(s.watchTask.id) && s.watchTask.id !== t.watchTask.id
    );
  }
  _getCalculatorTasksByOutput(t) {
    const n = /* @__PURE__ */ new Set();
    return t == null || t.forEach((r) => {
      const o = `${r.sid}-${r.id}`;
      (this.input2TaskIdMap.get(o) || []).forEach((i) => n.add(i));
    }), n;
  }
}
class ds {
  constructor(t, n) {
    M(this, "modify", !0);
    M(this, "_running", !1);
    M(this, "id");
    M(this, "_runningPromise", null);
    M(this, "_runningPromiseResolve", null);
    M(this, "_inputInfos");
    this.watchConfig = t, this.snapshot = n, this.id = Symbol(t.debug), this._inputInfos = this.createInputInfos();
  }
  createInputInfos() {
    const { inputs: t = [] } = this.watchConfig, n = this.watchConfig.data || new Array(t.length).fill(0), r = this.watchConfig.slient || new Array(t.length).fill(0);
    return {
      const_data: n,
      slients: r
    };
  }
  get slientInputs() {
    return this._inputInfos.slients;
  }
  getServerInputs() {
    const { const_data: t } = this._inputInfos;
    return this.watchConfig.inputs ? this.watchConfig.inputs.map((n, r) => t[r] === 0 ? this.snapshot.getObjectToValue(n) : n) : [];
  }
  get running() {
    return this._running;
  }
  get runningPromise() {
    return this._runningPromise;
  }
  /**
   * setRunning
   */
  setRunning() {
    this._running = !0, this._runningPromise = new Promise((t) => {
      this._runningPromiseResolve = t;
    }), this._trySetRunningRef(!0);
  }
  /**
   * taskDone
   */
  taskDone() {
    this._running = !1, this._runningPromiseResolve && (this._runningPromiseResolve(), this._runningPromiseResolve = null), this._trySetRunningRef(!1);
  }
  _trySetRunningRef(t) {
    if (this.watchConfig.running) {
      const n = this.snapshot.getVueRefObject(
        this.watchConfig.running
      );
      n.value = t;
    }
  }
}
class ps {
  /**
   *
   */
  constructor(t) {
    M(this, "prevNodes", []);
    M(this, "nextNodes", []);
    M(this, "_runningPrev", !1);
    this.watchTask = t;
  }
  /**
   * appendPrevNodes
   */
  appendPrevNodes(...t) {
    this.prevNodes.push(...t);
  }
  /**
   *
   */
  appendNextNodes(...t) {
    this.nextNodes.push(...t);
  }
  /**
   * hasNextNodes
   */
  hasNextNodes() {
    return this.nextNodes.length > 0;
  }
  /**
   * run
   */
  async run() {
    if (this.prevNodes.length > 0 && !this._runningPrev)
      try {
        this._runningPrev = !0, await Promise.all(this.prevNodes.map((t) => t.run()));
      } finally {
        this._runningPrev = !1;
      }
    if (this.watchTask.running) {
      await this.watchTask.runningPromise;
      return;
    }
    if (this.watchTask.modify) {
      this.watchTask.modify = !1, this.watchTask.setRunning();
      try {
        await ms(this.watchTask);
      } finally {
        this.watchTask.taskDone();
      }
    }
  }
}
async function ms(e) {
  const { outputs: t, url: n, key: r } = e.watchConfig, o = e.snapshot, s = e.getServerInputs(), i = {
    key: r,
    input: s,
    page: lt()
  }, c = await fetch(n, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(i)
  });
  if (!t)
    return;
  const l = await c.json();
  o.updateEventRefFromServer(l, t);
}
class gs {
  constructor(t) {
    M(this, "varMap", /* @__PURE__ */ new Map());
  }
  /**
   * collectVar
   */
  collectVar(t) {
    this.varMap.set(`${t.sid}-${t.id}`, t);
  }
  /**
   * get
   */
  getRef(t) {
    return this.varMap.get(`${t.sid}-${t.id}`);
  }
  /**
   * get
   */
  getWebComputed(t) {
    return this.varMap.get(`${t.sid}-${t.id}`);
  }
  getJsComputed(t) {
    return this.varMap.get(`${t.sid}-${t.id}`);
  }
}
let Cn;
function vs(e) {
  Cn = new gs(e);
}
function ys() {
  return Cn;
}
function Es(e, t) {
  const { on: n, code: r, immediate: o, deep: s, once: i, flush: c, bind: l = {} } = e, h = Te(
    l,
    (f) => t.getVueRefObject(f)
  ), u = G(r, h), a = Array.isArray(n) ? n.map((f) => t.getVueRefObject(f)) : t.getVueRefObject(n);
  return K(a, u, { immediate: o, deep: s, once: i, flush: c });
}
function ws(e, t) {
  const {
    inputs: n = [],
    outputs: r = [],
    slient: o,
    data: s,
    code: i,
    immediate: c = !0,
    deep: l,
    once: h,
    flush: u
  } = e, a = o || new Array(n.length).fill(0), f = s || new Array(n.length).fill(0), d = G(i), p = n.filter((y, _) => a[_] === 0 && f[_] === 0).map((y) => t.getVueRefObject(y)), v = r.length > 1;
  function g() {
    return n.map((y, _) => f[_] === 0 ? Gn(H(t.getVueRefObject(y))) : y);
  }
  K(
    p,
    () => {
      let y = d(...g());
      r.length !== 0 && (v || (y = [y]), r.forEach((_, O) => {
        const V = y[O];
        t.getVueRefObject(_).value = V;
      }));
    },
    { immediate: c, deep: l, once: h, flush: u }
  );
}
function _s(e, t) {
  return Object.assign(
    {},
    ...Object.entries(e ?? {}).map(([n, r]) => {
      const o = r.map((c) => {
        if (Qe.isWebEventHandler(c)) {
          const l = Rs(c.bind, t);
          return Os(c, l, t);
        } else
          return bs(c, t);
      }), i = G(
        " (...args)=> Promise.all(promises(...args))",
        {
          promises: (...c) => o.map(async (l) => {
            await l(...c);
          })
        }
      );
      return { [n]: i };
    })
  );
}
function Rs(e, t) {
  return (...n) => (e ?? []).map((r) => {
    if (N.isEventContext(r)) {
      if (r.path.startsWith(":")) {
        const o = r.path.slice(1);
        return G(o)(...n);
      }
      return we(n[0], r.path.split("."));
    }
    return N.IsBinding(r) ? t.getObjectToValue(r) : r;
  });
}
function Os(e, t, n) {
  const { url: r, hKey: o, key: s } = e, i = s !== void 0 ? { key: s } : {};
  async function c(...l) {
    let h = {};
    const u = t(...l), a = await fetch(r, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        bind: u,
        hKey: o,
        ...i,
        page: lt(),
        ...h
      })
    });
    if (!a.ok)
      throw new Error(`HTTP error! status: ${a.status}`);
    const f = await a.json();
    n.updateEventRefFromServer(f, e.set);
  }
  return c;
}
function bs(e, t) {
  const { code: n, inputs: r = [], set: o } = e, s = G(n);
  function i(...c) {
    const l = (r ?? []).map((u) => {
      if (N.isEventContext(u)) {
        if (u.path.startsWith(":")) {
          const a = u.path.slice(1);
          return G(a)(...c);
        }
        return we(c[0], u.path.split("."));
      }
      return N.IsBinding(u) ? t.getObjectToValue(u) : u;
    }), h = s(...l);
    if (o !== void 0) {
      const a = o.length === 1 ? [h] : h, f = a.map((d) => d === void 0 ? 1 : 0);
      t.updateEventRefFromServer({ values: a, skips: f }, o);
    }
  }
  return i;
}
function Ss(e, t) {
  const n = [];
  (e.bStyle || []).forEach((s) => {
    Array.isArray(s) ? n.push(
      ...s.map((i) => t.getObjectToValue(i))
    ) : n.push(
      Te(
        s,
        (i) => t.getObjectToValue(i)
      )
    );
  });
  const r = Kn([e.style || {}, n]);
  return {
    hasStyle: r && Object.keys(r).length > 0,
    styles: r
  };
}
function Ps(e, t) {
  const n = e.classes;
  if (!n)
    return null;
  if (typeof n == "string")
    return qe(n);
  const { str: r, map: o, bind: s } = n, i = [];
  return r && i.push(r), o && i.push(
    Te(
      o,
      (c) => t.getObjectToValue(c)
    )
  ), s && i.push(...s.map((c) => t.getObjectToValue(c))), qe(i);
}
function Vs(e, t) {
  var r;
  const n = {};
  return wt(e.bProps || {}, (o, s) => {
    n[s] = ks(t.getObjectToValue(o), s);
  }), (r = e.proxyProps) == null || r.forEach((o) => {
    const s = t.getObjectToValue(o);
    typeof s == "object" && wt(s, (i, c) => {
      n[c] = i;
    });
  }), { ...e.props || {}, ...n };
}
function ks(e, t) {
  return t === "innerText" ? Ht(e) : e;
}
function Ns(e, { slots: t }) {
  const { id: n, use: r } = e.propsInfo, o = Er(n);
  return Ce(() => {
    _r(n);
  }), () => {
    const s = e.propsValue;
    return wr(
      n,
      o,
      Object.fromEntries(
        r.map((i) => [i, s[i]])
      )
    ), A(Ae, null, t.default());
  };
}
const Is = F(Ns, {
  props: ["propsInfo", "propsValue"]
});
function Cs(e, t) {
  if (!e.slots)
    return null;
  const n = e.slots ?? {};
  return Array.isArray(n) ? t ? ge(n) : () => ge(n) : tn(n, { keyFn: (i) => i === ":" ? "default" : i, valueFn: (i) => {
    const { items: c } = i;
    return (l) => {
      if (i.scope) {
        const h = () => i.props ? Wt(i.props, l, c) : ge(c);
        return A(_e, { scope: i.scope }, h);
      }
      return i.props ? Wt(i.props, l, c) : ge(c);
    };
  } });
}
function Wt(e, t, n) {
  return A(
    Is,
    { propsInfo: e, propsValue: t },
    () => ge(n)
  );
}
function ge(e) {
  const t = (e ?? []).map((n) => A(X, {
    component: n
  }));
  return t.length <= 0 ? null : t;
}
function As(e, t) {
  const n = {}, r = [];
  return (e || []).forEach((o) => {
    const { sys: s, name: i, arg: c, value: l, mf: h } = o;
    if (i === "vmodel") {
      const u = t.getVueRefObject(l);
      if (n[`onUpdate:${c}`] = (a) => {
        u.value = a;
      }, s === 1) {
        const a = h ? Object.fromEntries(h.map((f) => [f, !0])) : {};
        r.push([Hn, u.value, void 0, a]);
      } else
        n[c] = u.value;
    } else if (i === "vshow") {
      const u = t.getVueRefObject(l);
      r.push([qn, u.value]);
    } else
      console.warn(`Directive ${i} is not supported yet`);
  }), {
    newProps: n,
    directiveArray: r
  };
}
function $s(e, t) {
  const { eRef: n } = e;
  return n === void 0 ? {} : { ref: t.getRef(n) };
}
function Ts(e) {
  const t = Y(), n = en();
  return () => {
    const { tag: r } = e.component, o = N.IsBinding(r) ? t.getObjectToValue(r) : r, s = ut(o), i = typeof s == "string", c = Ps(e.component, t), { styles: l, hasStyle: h } = Ss(e.component, t), u = _s(e.component.events ?? {}, t), a = Cs(e.component, i), f = Vs(e.component, t), { newProps: d, directiveArray: p } = As(
      e.component.dir,
      t
    ), v = $s(
      e.component,
      n
    ), g = zn({
      ...f,
      ...u,
      ...d,
      ...v
    }) || {};
    h && (g.style = l), c && (g.class = c);
    const y = A(s, { ...g }, a);
    return p.length > 0 ? Jn(
      // @ts-ignore
      y,
      p
    ) : y;
  };
}
const X = F(Ts, {
  props: ["component"]
});
function An(e, t) {
  var n, r;
  if (e) {
    e.vars && e.vars.forEach((i) => {
      ys().collectVar(i);
    });
    const o = Qt(e, Y(t)), s = Y(t);
    fs(e.py_watch, e.web_computed, s), (n = e.vue_watch) == null || n.forEach((i) => Es(i, s)), (r = e.js_watch) == null || r.forEach((i) => ws(i, s)), e.eRefs && e.eRefs.forEach((i) => {
      vr(i);
    }), Ce(() => {
      Zt(e.id, o), yr(e.id);
    });
  }
}
function js(e, { slots: t }) {
  const { scope: n } = e;
  return An(n), () => A(Ae, null, t.default());
}
const _e = F(js, {
  props: ["scope"]
}), xs = F(
  (e) => {
    const { scope: t, items: n, vforInfo: r } = e;
    return Or(r), An(t, r.key), n.length === 1 ? () => A(X, {
      component: n[0]
    }) : () => n.map(
      (s) => A(X, {
        component: s
      })
    );
  },
  {
    props: ["scope", "items", "vforInfo"]
  }
);
function Ds(e, t) {
  const { state: n, isReady: r, isLoading: o } = ar(async () => {
    let s = e;
    const i = t;
    if (!s && !i)
      throw new Error("Either config or configUrl must be provided");
    if (!s && i && (s = await (await fetch(i)).json()), !s)
      throw new Error("Failed to load config");
    return s;
  }, {});
  return { config: n, isReady: r, isLoading: o };
}
function Ms(e, t) {
  let n;
  return t.component ? n = `Error captured from component:tag: ${t.component.tag} ; id: ${t.component.id} ` : n = "Error captured from app init", console.group(n), console.error("Component:", t.component), console.error("Error:", e), console.groupEnd(), !1;
}
const Fs = { class: "app-box" }, Bs = {
  key: 0,
  style: { position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)" }
}, Ws = /* @__PURE__ */ F({
  __name: "App",
  props: {
    config: {},
    configUrl: {}
  },
  setup(e) {
    const t = e, { config: n, isLoading: r } = Ds(
      t.config,
      t.configUrl
    );
    let o = null;
    return K(n, (s) => {
      o = s, s.url && rr({
        version: s.version,
        queryPath: s.url.path,
        pathParams: s.url.params
      }), vs(s);
    }), Qn(Ms), (s, i) => (he(), be("div", Fs, [
      B(r) ? (he(), be("div", Bs, i[0] || (i[0] = [
        Yn("p", { style: { margin: "auto" } }, "Loading ...", -1)
      ]))) : (he(), be("div", {
        key: 1,
        class: qe(["insta-main", B(n).class])
      }, [
        Xn(B(_e), {
          scope: B(o).scope
        }, {
          default: Zn(() => [
            (he(!0), be(Ae, null, er(B(o).items, (c) => (he(), tr(B(X), { component: c }, null, 8, ["component"]))), 256))
          ]),
          _: 1
        }, 8, ["scope"])
      ], 2))
    ]));
  }
}), Ls = (e, t) => {
  const n = e.__vccOpts || e;
  for (const [r, o] of t)
    n[r] = o;
  return n;
}, Us = /* @__PURE__ */ Ls(Ws, [["__scopeId", "data-v-687dcc1a"]]);
function Gs(e) {
  const { on: t, scope: n, items: r } = e, o = Y();
  return () => {
    const s = o.getObjectToValue(t);
    return A(_e, { scope: n }, () => s ? r.map(
      (c) => A(X, { component: c })
    ) : void 0);
  };
}
const Ks = F(Gs, {
  props: ["on", "scope", "items"]
});
function Hs(e) {
  const { start: t = 0, end: n, step: r = 1 } = e;
  let o = [];
  if (r > 0)
    for (let s = t; s < n; s += r)
      o.push(s);
  else
    for (let s = t; s > n; s += r)
      o.push(s);
  return o;
}
function qs(e) {
  const { array: t, bArray: n, items: r, fkey: o, fid: s, scope: i, num: c, tsGroup: l = {} } = e, h = t === void 0, u = c !== void 0, a = h ? n : t, f = Y();
  Sr(s, a, h, u);
  const p = Xs(o ?? "index");
  return Ce(() => {
    mr(i.id);
  }), () => {
    const v = Js(
      u,
      h,
      a,
      f,
      c
    ), g = Vr(s), y = v.map((_, O) => {
      const V = p(_, O);
      return g.add(V), Pr(s, V, O), A(xs, {
        scope: e.scope,
        items: r,
        vforInfo: {
          fid: s,
          key: V
        },
        key: V
      });
    });
    return g.removeUnusedKeys(), l && Object.keys(l).length > 0 ? A(qt, l, {
      default: () => y
    }) : y;
  };
}
const zs = F(qs, {
  props: ["array", "items", "fid", "bArray", "scope", "num", "fkey", "tsGroup"]
});
function Js(e, t, n, r, o) {
  if (e) {
    let i = 0;
    return typeof o == "number" ? i = o : i = r.getObjectToValue(o) ?? 0, Hs({
      end: Math.max(0, i)
    });
  }
  const s = t ? r.getObjectToValue(n) || [] : n;
  return typeof s == "object" ? Object.values(s) : s;
}
const Qs = (e) => e, Ys = (e, t) => t;
function Xs(e) {
  const t = cr(e);
  return typeof t == "function" ? t : e === "item" ? Qs : Ys;
}
function Zs(e) {
  return e.map((n) => {
    if (n.tag)
      return A(X, { component: n });
    const r = ut($n);
    return A(r, {
      scope: n
    });
  });
}
const $n = F(
  (e) => {
    const t = e.scope;
    return () => Zs(t.items ?? []);
  },
  {
    props: ["scope"]
  }
);
function ei(e) {
  return e.map((t) => {
    if (t.tag)
      return A(X, { component: t });
    const n = ut($n);
    return A(n, {
      scope: t
    });
  });
}
const ti = F(
  (e) => {
    const { scope: t, on: n, items: r } = e, o = Q(r), s = Qt(t), i = Y();
    return Ie.createDynamicWatchRefresh(n, i, async () => {
      const { items: c, on: l } = await Ie.fetchRemote(e, i);
      return o.value = c, l;
    }), Ce(() => {
      Zt(t.id, s);
    }), () => ei(o.value);
  },
  {
    props: ["sid", "url", "hKey", "on", "bind", "items", "scope"]
  }
);
var Ie;
((e) => {
  function t(r, o, s) {
    let i = null, c = r, l = c.map((u) => o.getVueRefObject(u));
    function h() {
      i && i(), i = K(
        l,
        async () => {
          c = await s(), l = c.map((u) => o.getVueRefObject(u)), h();
        },
        { deep: !0 }
      );
    }
    return h(), () => {
      i && i();
    };
  }
  e.createDynamicWatchRefresh = t;
  async function n(r, o) {
    const s = Object.values(r.bind).map((u) => ({
      sid: u.sid,
      id: u.id,
      value: o.getObjectToValue(u)
    })), i = {
      sid: r.sid,
      bind: s,
      hKey: r.hKey,
      page: lt()
    }, c = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(i)
    }, l = await fetch(r.url, c);
    if (!l.ok)
      throw new Error("Failed to fetch data");
    return await l.json();
  }
  e.fetchRemote = n;
})(Ie || (Ie = {}));
function ni(e) {
  const { scope: t, items: n } = e;
  return () => {
    const r = n.map((o) => A(X, { component: o }));
    return A(_e, { scope: t }, () => r);
  };
}
const Lt = F(ni, {
  props: ["scope", "items"]
});
function ri(e) {
  const { on: t, case: n, default: r } = e, o = Y();
  return () => {
    const s = o.getObjectToValue(t), i = n.map((c) => {
      const { value: l, items: h, scope: u } = c.props;
      if (s === l)
        return A(Lt, {
          scope: u,
          items: h,
          key: ["case", l].join("-")
        });
    }).filter((c) => c);
    if (r && !i.length) {
      const { items: c, scope: l } = r.props;
      i.push(A(Lt, { scope: l, items: c, key: "default" }));
    }
    return A(Ae, i);
  };
}
const oi = F(ri, {
  props: ["case", "on", "default"]
});
function si(e, { slots: t }) {
  const { name: n = "fade", tag: r } = e;
  return () => A(
    qt,
    { name: n, tag: r },
    {
      default: t.default
    }
  );
}
const ii = F(si, {
  props: ["name", "tag"]
});
function ai(e) {
  const { content: t, r: n = 0 } = e, r = Y(), o = n === 1 ? () => r.getObjectToValue(t) : () => t;
  return () => Ht(o());
}
const ci = F(ai, {
  props: ["content", "r"]
});
function ui(e) {
  if (!e.router)
    throw new Error("Router config is not provided.");
  const { routes: t, kAlive: n = !1 } = e.router;
  return t.map(
    (o) => Tn(o, n)
  );
}
function Tn(e, t) {
  var l;
  const { server: n = !1, vueItem: r, scope: o } = e, s = () => {
    if (n)
      throw new Error("Server-side rendering is not supported yet.");
    return Promise.resolve(li(r, o, t));
  }, i = (l = r.children) == null ? void 0 : l.map(
    (h) => Tn(h, t)
  ), c = {
    ...r,
    children: i,
    component: s
  };
  return r.component.length === 0 && delete c.component, i === void 0 && delete c.children, c;
}
function li(e, t, n) {
  const { path: r, component: o } = e, s = A(
    _e,
    { scope: t, key: r },
    () => o.map((c) => A(X, { component: c }))
  );
  return n ? A(nr, null, () => s) : s;
}
function fi(e, t) {
  const { mode: n = "hash" } = t.router, r = n === "hash" ? vo() : n === "memory" ? go() : wn();
  e.use(
    as({
      history: r,
      routes: ui(t)
    })
  );
}
function pi(e, t) {
  e.component("insta-ui", Us), e.component("vif", Ks), e.component("vfor", zs), e.component("match", oi), e.component("refresh", ti), e.component("ts-group", ii), e.component("content", ci), t.router && fi(e, t);
}
export {
  pi as default
};
//# sourceMappingURL=insta-ui.js.map
