var Ne = (e) => {
  throw TypeError(e);
};
var Ve = (e, t, n) => t.has(e) || Ne("Cannot " + n);
var W = (e, t, n) => (Ve(e, t, "read from private field"), n ? n.call(e) : t.get(e)), We = (e, t, n) => t.has(e) ? Ne("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), Ue = (e, t, n, o) => (Ve(e, t, "write to private field"), o ? o.call(e, n) : t.set(e, n), n);
import { i as Xt, a as Pe, r as Ft, w as te, g as Nt, c as G } from "./Index-CAJ-by8V.js";
const b = window.ms_globals.React, At = window.ms_globals.React.forwardRef, $t = window.ms_globals.React.useRef, Bt = window.ms_globals.React.useState, Dt = window.ms_globals.React.useEffect, Me = window.ms_globals.ReactDOM.createPortal, Vt = window.ms_globals.internalContext.useContextPropsContext, Wt = window.ms_globals.antd.ConfigProvider, Ee = window.ms_globals.antd.theme, Ge = window.ms_globals.antd.Typography, xe = window.ms_globals.antd.Flex, qe = window.ms_globals.antdCssinjs.unit, Se = window.ms_globals.antdCssinjs.token2CSSVar, Ke = window.ms_globals.antdCssinjs.useStyleRegister, Ut = window.ms_globals.antdCssinjs.useCSSVarRegister, Gt = window.ms_globals.antdCssinjs.createTheme, qt = window.ms_globals.antdCssinjs.useCacheToken;
var Kt = /\s/;
function Qt(e) {
  for (var t = e.length; t-- && Kt.test(e.charAt(t)); )
    ;
  return t;
}
var Jt = /^\s+/;
function Zt(e) {
  return e && e.slice(0, Qt(e) + 1).replace(Jt, "");
}
var Qe = NaN, Yt = /^[-+]0x[0-9a-f]+$/i, er = /^0b[01]+$/i, tr = /^0o[0-7]+$/i, rr = parseInt;
function Je(e) {
  if (typeof e == "number")
    return e;
  if (Xt(e))
    return Qe;
  if (Pe(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Pe(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Zt(e);
  var n = er.test(e);
  return n || tr.test(e) ? rr(e.slice(2), n ? 2 : 8) : Yt.test(e) ? Qe : +e;
}
var _e = function() {
  return Ft.Date.now();
}, nr = "Expected a function", or = Math.max, ir = Math.min;
function sr(e, t, n) {
  var o, r, i, s, a, l, c = 0, f = !1, u = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(nr);
  t = Je(t) || 0, Pe(n) && (f = !!n.leading, u = "maxWait" in n, i = u ? or(Je(n.maxWait) || 0, t) : i, d = "trailing" in n ? !!n.trailing : d);
  function v(m) {
    var w = o, T = r;
    return o = r = void 0, c = m, s = e.apply(T, w), s;
  }
  function S(m) {
    return c = m, a = setTimeout(x, t), f ? v(m) : s;
  }
  function p(m) {
    var w = m - l, T = m - c, M = t - w;
    return u ? ir(M, i - T) : M;
  }
  function h(m) {
    var w = m - l, T = m - c;
    return l === void 0 || w >= t || w < 0 || u && T >= i;
  }
  function x() {
    var m = _e();
    if (h(m))
      return _(m);
    a = setTimeout(x, p(m));
  }
  function _(m) {
    return a = void 0, d && o ? v(m) : (o = r = void 0, s);
  }
  function P() {
    a !== void 0 && clearTimeout(a), c = 0, o = l = r = a = void 0;
  }
  function g() {
    return a === void 0 ? s : _(_e());
  }
  function C() {
    var m = _e(), w = h(m);
    if (o = arguments, r = this, l = m, w) {
      if (a === void 0)
        return S(l);
      if (u)
        return clearTimeout(a), a = setTimeout(x, t), v(l);
    }
    return a === void 0 && (a = setTimeout(x, t)), s;
  }
  return C.cancel = P, C.flush = g, C;
}
var gt = {
  exports: {}
}, se = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ar = b, lr = Symbol.for("react.element"), cr = Symbol.for("react.fragment"), ur = Object.prototype.hasOwnProperty, fr = ar.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, dr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function pt(e, t, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) ur.call(t, o) && !dr.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: lr,
    type: e,
    key: i,
    ref: s,
    props: r,
    _owner: fr.current
  };
}
se.Fragment = cr;
se.jsx = pt;
se.jsxs = pt;
gt.exports = se;
var D = gt.exports;
const {
  SvelteComponent: hr,
  assign: Ze,
  binding_callbacks: Ye,
  check_outros: gr,
  children: mt,
  claim_element: bt,
  claim_space: pr,
  component_subscribe: et,
  compute_slots: mr,
  create_slot: br,
  detach: U,
  element: yt,
  empty: tt,
  exclude_internal_props: rt,
  get_all_dirty_from_scope: yr,
  get_slot_changes: vr,
  group_outros: xr,
  init: Sr,
  insert_hydration: re,
  safe_not_equal: _r,
  set_custom_element_data: vt,
  space: Cr,
  transition_in: ne,
  transition_out: je,
  update_slot_base: wr
} = window.__gradio__svelte__internal, {
  beforeUpdate: Tr,
  getContext: Or,
  onDestroy: Mr,
  setContext: Pr
} = window.__gradio__svelte__internal;
function nt(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = br(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = yt("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      t = bt(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = mt(t);
      r && r.l(s), s.forEach(U), this.h();
    },
    h() {
      vt(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      re(i, t, s), r && r.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && wr(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? vr(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : yr(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (ne(r, i), n = !0);
    },
    o(i) {
      je(r, i), n = !1;
    },
    d(i) {
      i && U(t), r && r.d(i), e[9](null);
    }
  };
}
function Er(e) {
  let t, n, o, r, i = (
    /*$$slots*/
    e[4].default && nt(e)
  );
  return {
    c() {
      t = yt("react-portal-target"), n = Cr(), i && i.c(), o = tt(), this.h();
    },
    l(s) {
      t = bt(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), mt(t).forEach(U), n = pr(s), i && i.l(s), o = tt(), this.h();
    },
    h() {
      vt(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      re(s, t, a), e[8](t), re(s, n, a), i && i.m(s, a), re(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && ne(i, 1)) : (i = nt(s), i.c(), ne(i, 1), i.m(o.parentNode, o)) : i && (xr(), je(i, 1, 1, () => {
        i = null;
      }), gr());
    },
    i(s) {
      r || (ne(i), r = !0);
    },
    o(s) {
      je(i), r = !1;
    },
    d(s) {
      s && (U(t), U(n), U(o)), e[8](null), i && i.d(s);
    }
  };
}
function ot(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function jr(e, t, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = mr(i);
  let {
    svelteInit: l
  } = t;
  const c = te(ot(t)), f = te();
  et(e, f, (g) => n(0, o = g));
  const u = te();
  et(e, u, (g) => n(1, r = g));
  const d = [], v = Or("$$ms-gr-react-wrapper"), {
    slotKey: S,
    slotIndex: p,
    subSlotIndex: h
  } = Nt() || {}, x = l({
    parent: v,
    props: c,
    target: f,
    slot: u,
    slotKey: S,
    slotIndex: p,
    subSlotIndex: h,
    onDestroy(g) {
      d.push(g);
    }
  });
  Pr("$$ms-gr-react-wrapper", x), Tr(() => {
    c.set(ot(t));
  }), Mr(() => {
    d.forEach((g) => g());
  });
  function _(g) {
    Ye[g ? "unshift" : "push"](() => {
      o = g, f.set(o);
    });
  }
  function P(g) {
    Ye[g ? "unshift" : "push"](() => {
      r = g, u.set(r);
    });
  }
  return e.$$set = (g) => {
    n(17, t = Ze(Ze({}, t), rt(g))), "svelteInit" in g && n(5, l = g.svelteInit), "$$scope" in g && n(6, s = g.$$scope);
  }, t = rt(t), [o, r, f, u, a, l, s, i, _, P];
}
class Ir extends hr {
  constructor(t) {
    super(), Sr(this, t, jr, Er, _r, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: Hn
} = window.__gradio__svelte__internal, it = window.ms_globals.rerender, Ce = window.ms_globals.tree;
function kr(e, t = {}) {
  function n(o) {
    const r = te(), i = new Ir({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, l = s.parent ?? Ce;
          return l.nodes = [...l.nodes, a], it({
            createPortal: Me,
            node: Ce
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== r), it({
              createPortal: Me,
              node: Ce
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(i), i;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Rr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Lr(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = Hr(n, o), t;
  }, {}) : {};
}
function Hr(e, t) {
  return typeof t == "number" && !Rr.includes(e) ? t + "px" : t;
}
function Ie(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = b.Children.toArray(e._reactElement.props.children).map((i) => {
      if (b.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Ie(i.props.el);
        return b.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...b.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(Me(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, s, l);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const i = o[r];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Ie(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function zr(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Y = At(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = $t(), [a, l] = Bt([]), {
    forceClone: c
  } = Vt(), f = c ? !0 : t;
  return Dt(() => {
    var p;
    if (!s.current || !e)
      return;
    let u = e;
    function d() {
      let h = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (h = u.children[0], h.tagName.toLowerCase() === "react-portal-target" && h.children[0] && (h = h.children[0])), zr(i, h), n && h.classList.add(...n.split(" ")), o) {
        const x = Lr(o);
        Object.keys(x).forEach((_) => {
          h.style[_] = x[_];
        });
      }
    }
    let v = null, S = null;
    if (f && window.MutationObserver) {
      let h = function() {
        var g, C, m;
        (g = s.current) != null && g.contains(u) && ((C = s.current) == null || C.removeChild(u));
        const {
          portals: _,
          clonedElement: P
        } = Ie(e);
        u = P, l(_), u.style.display = "contents", S && clearTimeout(S), S = setTimeout(() => {
          d();
        }, 50), (m = s.current) == null || m.appendChild(u);
      };
      h();
      const x = sr(() => {
        h(), v == null || v.disconnect(), v == null || v.observe(e, {
          childList: !0,
          subtree: !0
          // attributes: observeAttributes ?? (forceClone ? true : false),
        });
      }, 50);
      v = new window.MutationObserver(x), v.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (p = s.current) == null || p.appendChild(u);
    return () => {
      var h, x;
      u.style.display = "", (h = s.current) != null && h.contains(u) && ((x = s.current) == null || x.removeChild(u)), v == null || v.disconnect();
    };
  }, [e, f, n, o, i, r, c]), b.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Ar = "1.0.5", $r = /* @__PURE__ */ b.createContext({}), Br = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Dr = (e) => {
  const t = b.useContext($r);
  return b.useMemo(() => ({
    ...Br,
    ...t[e]
  }), [t[e]]);
};
function ke() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = b.useContext(Wt.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function Xr(e) {
  if (Array.isArray(e)) return e;
}
function Fr(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], l = !0, c = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = i.call(n)).done) && (a.push(o.value), a.length !== t); l = !0) ;
    } catch (f) {
      c = !0, r = f;
    } finally {
      try {
        if (!l && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (c) throw r;
      }
    }
    return a;
  }
}
function st(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function Nr(e, t) {
  if (e) {
    if (typeof e == "string") return st(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? st(e, t) : void 0;
  }
}
function Vr() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function oe(e, t) {
  return Xr(e) || Fr(e, t) || Nr(e, t) || Vr();
}
function z(e) {
  "@babel/helpers - typeof";
  return z = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, z(e);
}
var y = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var He = Symbol.for("react.element"), ze = Symbol.for("react.portal"), ae = Symbol.for("react.fragment"), le = Symbol.for("react.strict_mode"), ce = Symbol.for("react.profiler"), ue = Symbol.for("react.provider"), fe = Symbol.for("react.context"), Wr = Symbol.for("react.server_context"), de = Symbol.for("react.forward_ref"), he = Symbol.for("react.suspense"), ge = Symbol.for("react.suspense_list"), pe = Symbol.for("react.memo"), me = Symbol.for("react.lazy"), Ur = Symbol.for("react.offscreen"), xt;
xt = Symbol.for("react.module.reference");
function R(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case He:
        switch (e = e.type, e) {
          case ae:
          case ce:
          case le:
          case he:
          case ge:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Wr:
              case fe:
              case de:
              case me:
              case pe:
              case ue:
                return e;
              default:
                return t;
            }
        }
      case ze:
        return t;
    }
  }
}
y.ContextConsumer = fe;
y.ContextProvider = ue;
y.Element = He;
y.ForwardRef = de;
y.Fragment = ae;
y.Lazy = me;
y.Memo = pe;
y.Portal = ze;
y.Profiler = ce;
y.StrictMode = le;
y.Suspense = he;
y.SuspenseList = ge;
y.isAsyncMode = function() {
  return !1;
};
y.isConcurrentMode = function() {
  return !1;
};
y.isContextConsumer = function(e) {
  return R(e) === fe;
};
y.isContextProvider = function(e) {
  return R(e) === ue;
};
y.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === He;
};
y.isForwardRef = function(e) {
  return R(e) === de;
};
y.isFragment = function(e) {
  return R(e) === ae;
};
y.isLazy = function(e) {
  return R(e) === me;
};
y.isMemo = function(e) {
  return R(e) === pe;
};
y.isPortal = function(e) {
  return R(e) === ze;
};
y.isProfiler = function(e) {
  return R(e) === ce;
};
y.isStrictMode = function(e) {
  return R(e) === le;
};
y.isSuspense = function(e) {
  return R(e) === he;
};
y.isSuspenseList = function(e) {
  return R(e) === ge;
};
y.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === ae || e === ce || e === le || e === he || e === ge || e === Ur || typeof e == "object" && e !== null && (e.$$typeof === me || e.$$typeof === pe || e.$$typeof === ue || e.$$typeof === fe || e.$$typeof === de || e.$$typeof === xt || e.getModuleId !== void 0);
};
y.typeOf = R;
function Gr(e, t) {
  if (z(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (z(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function St(e) {
  var t = Gr(e, "string");
  return z(t) == "symbol" ? t : t + "";
}
function H(e, t, n) {
  return (t = St(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function at(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function j(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? at(Object(n), !0).forEach(function(o) {
      H(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : at(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function be(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function qr(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, St(o.key), o);
  }
}
function ye(e, t, n) {
  return t && qr(e.prototype, t), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Re(e, t) {
  return Re = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, Re(e, t);
}
function _t(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Re(e, t);
}
function ie(e) {
  return ie = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, ie(e);
}
function Ct() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Ct = function() {
    return !!e;
  })();
}
function K(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function Kr(e, t) {
  if (t && (z(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return K(e);
}
function wt(e) {
  var t = Ct();
  return function() {
    var n, o = ie(e);
    if (t) {
      var r = ie(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return Kr(this, n);
  };
}
var Tt = /* @__PURE__ */ ye(function e() {
  be(this, e);
}), Ot = "CALC_UNIT", Qr = new RegExp(Ot, "g");
function we(e) {
  return typeof e == "number" ? "".concat(e).concat(Ot) : e;
}
var Jr = /* @__PURE__ */ function(e) {
  _t(n, e);
  var t = wt(n);
  function n(o, r) {
    var i;
    be(this, n), i = t.call(this), H(K(i), "result", ""), H(K(i), "unitlessCssVar", void 0), H(K(i), "lowPriority", void 0);
    var s = z(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = we(o) : s === "string" && (i.result = o), i;
  }
  return ye(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(we(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(we(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " * ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " * ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " / ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " / ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(r) {
      return this.lowPriority || r ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(r) {
      var i = this, s = r || {}, a = s.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(c) {
        return i.result.includes(c);
      }) && (l = !1), this.result = this.result.replace(Qr, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Tt), Zr = /* @__PURE__ */ function(e) {
  _t(n, e);
  var t = wt(n);
  function n(o) {
    var r;
    return be(this, n), r = t.call(this), H(K(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return ye(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result += r.result : typeof r == "number" && (this.result += r), this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result -= r.result : typeof r == "number" && (this.result -= r), this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return r instanceof n ? this.result *= r.result : typeof r == "number" && (this.result *= r), this;
    }
  }, {
    key: "div",
    value: function(r) {
      return r instanceof n ? this.result /= r.result : typeof r == "number" && (this.result /= r), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(Tt), Yr = function(t, n) {
  var o = t === "css" ? Jr : Zr;
  return function(r) {
    return new o(r, n);
  };
}, lt = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ct(e, t, n, o) {
  var r = j({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var l = oe(a, 2), c = l[0], f = l[1];
      if (r != null && r[c] || r != null && r[f]) {
        var u;
        (u = r[f]) !== null && u !== void 0 || (r[f] = r == null ? void 0 : r[c]);
      }
    });
  }
  var s = j(j({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var Mt = typeof CSSINJS_STATISTIC < "u", Le = !0;
function Ae() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!Mt)
    return Object.assign.apply(Object, [{}].concat(t));
  Le = !1;
  var o = {};
  return t.forEach(function(r) {
    if (z(r) === "object") {
      var i = Object.keys(r);
      i.forEach(function(s) {
        Object.defineProperty(o, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[s];
          }
        });
      });
    }
  }), Le = !0, o;
}
var ut = {};
function en() {
}
var tn = function(t) {
  var n, o = t, r = en;
  return Mt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(s, a) {
      if (Le) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var l;
    ut[s] = {
      global: Array.from(n),
      component: j(j({}, (l = ut[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function ft(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Ae(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function rn(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(i) {
        return qe(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(i) {
        return qe(i);
      }).join(","), ")");
    }
  };
}
var nn = 1e3 * 60 * 10, on = /* @__PURE__ */ function() {
  function e() {
    be(this, e), H(this, "map", /* @__PURE__ */ new Map()), H(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), H(this, "nextID", 0), H(this, "lastAccessBeat", /* @__PURE__ */ new Map()), H(this, "accessBeat", 0);
  }
  return ye(e, [{
    key: "set",
    value: function(n, o) {
      this.clear();
      var r = this.getCompositeKey(n);
      this.map.set(r, o), this.lastAccessBeat.set(r, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var o = this.getCompositeKey(n), r = this.map.get(o);
      return this.lastAccessBeat.set(o, Date.now()), this.accessBeat += 1, r;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var o = this, r = n.map(function(i) {
        return i && z(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(z(i), "_").concat(i);
      });
      return r.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var o = this.nextID;
      return this.objectIDMap.set(n, o), this.nextID += 1, o;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var o = Date.now();
        this.lastAccessBeat.forEach(function(r, i) {
          o - r > nn && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), dt = new on();
function sn(e, t) {
  return b.useMemo(function() {
    var n = dt.get(t);
    if (n)
      return n;
    var o = e();
    return dt.set(t, o), o;
  }, t);
}
var an = function() {
  return {};
};
function ln(e) {
  var t = e.useCSP, n = t === void 0 ? an : t, o = e.useToken, r = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, v, S, p) {
    var h = Array.isArray(d) ? d[0] : d;
    function x(T) {
      return "".concat(String(h)).concat(T.slice(0, 1).toUpperCase()).concat(T.slice(1));
    }
    var _ = (p == null ? void 0 : p.unitless) || {}, P = typeof a == "function" ? a(d) : {}, g = j(j({}, P), {}, H({}, x("zIndexPopup"), !0));
    Object.keys(_).forEach(function(T) {
      g[x(T)] = _[T];
    });
    var C = j(j({}, p), {}, {
      unitless: g,
      prefixToken: x
    }), m = f(d, v, S, C), w = c(h, S, C);
    return function(T) {
      var M = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : T, L = m(T, M), X = oe(L, 2), E = X[1], F = w(M), I = oe(F, 2), A = I[0], J = I[1];
      return [A, E, J];
    };
  }
  function c(d, v, S) {
    var p = S.unitless, h = S.injectStyle, x = h === void 0 ? !0 : h, _ = S.prefixToken, P = S.ignore, g = function(w) {
      var T = w.rootCls, M = w.cssVar, L = M === void 0 ? {} : M, X = o(), E = X.realToken;
      return Ut({
        path: [d],
        prefix: L.prefix,
        key: L.key,
        unitless: p,
        ignore: P,
        token: E,
        scope: T
      }, function() {
        var F = ft(d, E, v), I = ct(d, E, F, {
          deprecatedTokens: S == null ? void 0 : S.deprecatedTokens
        });
        return Object.keys(F).forEach(function(A) {
          I[_(A)] = I[A], delete I[A];
        }), I;
      }), null;
    }, C = function(w) {
      var T = o(), M = T.cssVar;
      return [function(L) {
        return x && M ? /* @__PURE__ */ b.createElement(b.Fragment, null, /* @__PURE__ */ b.createElement(g, {
          rootCls: w,
          cssVar: M,
          component: d
        }), L) : L;
      }, M == null ? void 0 : M.key];
    };
    return C;
  }
  function f(d, v, S) {
    var p = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = Array.isArray(d) ? d : [d, d], x = oe(h, 1), _ = x[0], P = h.join("-"), g = e.layer || {
      name: "antd"
    };
    return function(C) {
      var m = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, w = o(), T = w.theme, M = w.realToken, L = w.hashId, X = w.token, E = w.cssVar, F = r(), I = F.rootPrefixCls, A = F.iconPrefixCls, J = n(), ve = E ? "css" : "js", Et = sn(function() {
        var N = /* @__PURE__ */ new Set();
        return E && Object.keys(p.unitless || {}).forEach(function(Z) {
          N.add(Se(Z, E.prefix)), N.add(Se(Z, lt(_, E.prefix)));
        }), Yr(ve, N);
      }, [ve, _, E == null ? void 0 : E.prefix]), $e = rn(ve), jt = $e.max, It = $e.min, Be = {
        theme: T,
        token: X,
        hashId: L,
        nonce: function() {
          return J.nonce;
        },
        clientOnly: p.clientOnly,
        layer: g,
        // antd is always at top of styles
        order: p.order || -999
      };
      typeof i == "function" && Ke(j(j({}, Be), {}, {
        clientOnly: !1,
        path: ["Shared", I]
      }), function() {
        return i(X, {
          prefix: {
            rootPrefixCls: I,
            iconPrefixCls: A
          },
          csp: J
        });
      });
      var kt = Ke(j(j({}, Be), {}, {
        path: [P, C, A]
      }), function() {
        if (p.injectStyle === !1)
          return [];
        var N = tn(X), Z = N.token, Rt = N.flush, V = ft(_, M, S), Lt = ".".concat(C), De = ct(_, M, V, {
          deprecatedTokens: p.deprecatedTokens
        });
        E && V && z(V) === "object" && Object.keys(V).forEach(function(Fe) {
          V[Fe] = "var(".concat(Se(Fe, lt(_, E.prefix)), ")");
        });
        var Xe = Ae(Z, {
          componentCls: Lt,
          prefixCls: C,
          iconCls: ".".concat(A),
          antCls: ".".concat(I),
          calc: Et,
          // @ts-ignore
          max: jt,
          // @ts-ignore
          min: It
        }, E ? V : De), Ht = v(Xe, {
          hashId: L,
          prefixCls: C,
          rootPrefixCls: I,
          iconPrefixCls: A
        });
        Rt(_, De);
        var zt = typeof s == "function" ? s(Xe, C, m, p.resetFont) : null;
        return [p.resetStyle === !1 ? null : zt, Ht];
      });
      return [kt, L];
    };
  }
  function u(d, v, S) {
    var p = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = f(d, v, S, j({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, p)), x = function(P) {
      var g = P.prefixCls, C = P.rootCls, m = C === void 0 ? g : C;
      return h(g, m), null;
    };
    return x;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: u,
    genComponentStyleHook: f
  };
}
function Q(e) {
  "@babel/helpers - typeof";
  return Q = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Q(e);
}
function cn(e, t) {
  if (Q(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (Q(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function un(e) {
  var t = cn(e, "string");
  return Q(t) == "symbol" ? t : t + "";
}
function k(e, t, n) {
  return (t = un(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
const O = Math.round;
function Te(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const ht = (e, t, n) => n === 0 ? e : e / 100;
function q(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class B {
  constructor(t) {
    k(this, "isValid", !0), k(this, "r", 0), k(this, "g", 0), k(this, "b", 0), k(this, "a", 1), k(this, "_h", void 0), k(this, "_s", void 0), k(this, "_l", void 0), k(this, "_v", void 0), k(this, "_max", void 0), k(this, "_min", void 0), k(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof B)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = q(t.r), this.g = q(t.g), this.b = q(t.b), this.a = typeof t.a == "number" ? q(t.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(t);
    else if (n("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const n = this.toHsv();
    return n.h = t, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), o = t(this.g), r = t(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = O(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - t / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + t / 100;
    return r > 1 && (r = 1), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const o = this._c(t), r = n / 100, i = (a) => (o[a] - this[a]) * r + this[a], s = {
      r: O(i("r")),
      g: O(i("g")),
      b: O(i("b")),
      a: O(i("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (i) => O((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
    return this._c({
      r: r("r"),
      g: r("g"),
      b: r("b"),
      a: o
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.g || 0).toString(16);
    t += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (t += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = O(this.a * 255).toString(16);
      t += i.length === 2 ? i : "0" + i;
    }
    return t;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const t = this.getHue(), n = O(this.getSaturation() * 100), o = O(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${o}%,${this.a})` : `hsl(${t},${n}%,${o}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(t, n, o) {
    const r = this.clone();
    return r[t] = q(n, o), r;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const n = t.replace("#", "");
    function o(r, i) {
      return parseInt(n[r] + n[i || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = t % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const d = O(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const l = t / 60, c = (1 - Math.abs(2 * o - 1)) * n, f = c * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = c, s = f) : l >= 1 && l < 2 ? (i = f, s = c) : l >= 2 && l < 3 ? (s = c, a = f) : l >= 3 && l < 4 ? (s = f, a = c) : l >= 4 && l < 5 ? (i = f, a = c) : l >= 5 && l < 6 && (i = c, a = f);
    const u = o - c / 2;
    this.r = O((i + u) * 255), this.g = O((s + u) * 255), this.b = O((a + u) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = O(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), l = s - a, c = O(o * (1 - n) * 255), f = O(o * (1 - n * l) * 255), u = O(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = c;
        break;
      case 1:
        this.r = f, this.b = c;
        break;
      case 2:
        this.r = c, this.b = u;
        break;
      case 3:
        this.r = c, this.g = f;
        break;
      case 4:
        this.r = u, this.g = c;
        break;
      case 5:
      default:
        this.g = c, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const n = Te(t, ht);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = Te(t, ht);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = Te(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? O(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const fn = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, dn = Object.assign(Object.assign({}, fn), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function Oe(e) {
  return e >= 0 && e <= 255;
}
function ee(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new B(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: l
  } = new B(t).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const f = Math.round((n - s * (1 - c)) / c), u = Math.round((o - a * (1 - c)) / c), d = Math.round((r - l * (1 - c)) / c);
    if (Oe(f) && Oe(u) && Oe(d))
      return new B({
        r: f,
        g: u,
        b: d,
        a: Math.round(c * 100) / 100
      }).toRgbString();
  }
  return new B({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var hn = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function gn(e) {
  const {
    override: t
  } = e, n = hn(e, ["override"]), o = Object.assign({}, t);
  Object.keys(dn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, l = 992, c = 1200, f = 1600;
  if (r.motion === !1) {
    const d = "0s";
    r.motionDurationFast = d, r.motionDurationMid = d, r.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: ee(r.colorBorderSecondary, r.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: r.colorTextQuaternary,
    colorTextDisabled: r.colorTextQuaternary,
    colorTextHeading: r.colorText,
    colorTextLabel: r.colorTextSecondary,
    colorTextDescription: r.colorTextTertiary,
    colorTextLightSolid: r.colorWhite,
    colorHighlight: r.colorError,
    colorBgTextHover: r.colorFillSecondary,
    colorBgTextActive: r.colorFill,
    colorIcon: r.colorTextTertiary,
    colorIconHover: r.colorText,
    colorErrorOutline: ee(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: ee(r.colorWarningBg, r.colorBgContainer),
    // Font
    fontSizeIcon: r.fontSizeSM,
    // Line
    lineWidthFocus: r.lineWidth * 3,
    // Control
    lineWidth: r.lineWidth,
    controlOutlineWidth: r.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: r.controlHeight / 2,
    controlItemBgHover: r.colorFillTertiary,
    controlItemBgActive: r.colorPrimaryBg,
    controlItemBgActiveHover: r.colorPrimaryBgHover,
    controlItemBgActiveDisabled: r.colorFill,
    controlTmpOutline: r.colorFillQuaternary,
    controlOutline: ee(r.colorPrimaryBg, r.colorBgContainer),
    lineType: r.lineType,
    borderRadius: r.borderRadius,
    borderRadiusXS: r.borderRadiusXS,
    borderRadiusSM: r.borderRadiusSM,
    borderRadiusLG: r.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: r.sizeXXS,
    paddingXS: r.sizeXS,
    paddingSM: r.sizeSM,
    padding: r.size,
    paddingMD: r.sizeMD,
    paddingLG: r.sizeLG,
    paddingXL: r.sizeXL,
    paddingContentHorizontalLG: r.sizeLG,
    paddingContentVerticalLG: r.sizeMS,
    paddingContentHorizontal: r.sizeMS,
    paddingContentVertical: r.sizeSM,
    paddingContentHorizontalSM: r.size,
    paddingContentVerticalSM: r.sizeXS,
    marginXXS: r.sizeXXS,
    marginXS: r.sizeXS,
    marginSM: r.sizeSM,
    margin: r.size,
    marginMD: r.sizeMD,
    marginLG: r.sizeLG,
    marginXL: r.sizeXL,
    marginXXL: r.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: c - 1,
    screenXL: c,
    screenXLMin: c,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new B("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new B("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new B("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), o);
}
const pn = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, mn = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, bn = Gt(Ee.defaultAlgorithm), yn = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, Pt = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...i
  } = t;
  let s = {
    ...o,
    override: r
  };
  return s = gn(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: c,
      ...f
    } = l;
    let u = f;
    c && (u = Pt({
      ...s,
      ...f
    }, {
      override: f
    }, c)), s[a] = u;
  }), s;
};
function vn() {
  const {
    token: e,
    hashed: t,
    theme: n = bn,
    override: o,
    cssVar: r
  } = b.useContext(Ee._internalContext), [i, s, a] = qt(n, [Ee.defaultSeed, e], {
    salt: `${Ar}-${t || ""}`,
    override: o,
    getComputedToken: Pt,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: pn,
      ignore: mn,
      preserve: yn
    }
  });
  return [n, a, t ? s : "", i, r];
}
const {
  genStyleHooks: xn
} = ln({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = ke();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = vn();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = ke();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Sn = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, o = n(e.fontSizeHeading3).mul(e.lineHeightHeading3).equal(), r = n(e.fontSize).mul(e.lineHeight).equal();
  return {
    [t]: {
      gap: e.padding,
      // ======================== Icon ========================
      [`${t}-icon`]: {
        height: n(o).add(r).add(e.paddingXXS).equal(),
        display: "flex",
        img: {
          height: "100%"
        }
      },
      // ==================== Content Wrap ====================
      [`${t}-content-wrapper`]: {
        gap: e.paddingXS,
        flex: "auto",
        minWidth: 0,
        [`${t}-title-wrapper`]: {
          gap: e.paddingXS
        },
        [`${t}-title`]: {
          margin: 0
        },
        [`${t}-extra`]: {
          marginInlineStart: "auto"
        }
      }
    }
  };
}, _n = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Filled ========================
      "&-filled": {
        paddingInline: e.padding,
        paddingBlock: e.paddingSM,
        background: e.colorFillContent,
        borderRadius: e.borderRadiusLG
      },
      // ====================== Borderless ======================
      "&-borderless": {
        [`${t}-title`]: {
          fontSize: e.fontSizeHeading3,
          lineHeight: e.lineHeightHeading3
        }
      }
    }
  };
}, Cn = () => ({}), wn = xn("Welcome", (e) => {
  const t = Ae(e, {});
  return [Sn(t), _n(t)];
}, Cn);
function Tn(e, t) {
  const {
    prefixCls: n,
    rootClassName: o,
    className: r,
    style: i,
    variant: s = "filled",
    // Semantic
    classNames: a = {},
    styles: l = {},
    // Layout
    icon: c,
    title: f,
    description: u,
    extra: d
  } = e, {
    direction: v,
    getPrefixCls: S
  } = ke(), p = S("welcome", n), h = Dr("welcome"), [x, _, P] = wn(p), g = b.useMemo(() => {
    if (!c)
      return null;
    let w = c;
    return typeof c == "string" && c.startsWith("http") && (w = /* @__PURE__ */ b.createElement("img", {
      src: c,
      alt: "icon"
    })), /* @__PURE__ */ b.createElement("div", {
      className: G(`${p}-icon`, h.classNames.icon, a.icon),
      style: l.icon
    }, w);
  }, [c]), C = b.useMemo(() => f ? /* @__PURE__ */ b.createElement(Ge.Title, {
    level: 4,
    className: G(`${p}-title`, h.classNames.title, a.title),
    style: l.title
  }, f) : null, [f]), m = b.useMemo(() => d ? /* @__PURE__ */ b.createElement("div", {
    className: G(`${p}-extra`, h.classNames.extra, a.extra),
    style: l.extra
  }, d) : null, [d]);
  return x(/* @__PURE__ */ b.createElement(xe, {
    ref: t,
    className: G(p, h.className, r, o, _, P, `${p}-${s}`, {
      [`${p}-rtl`]: v === "rtl"
    }),
    style: i
  }, g, /* @__PURE__ */ b.createElement(xe, {
    vertical: !0,
    className: `${p}-content-wrapper`
  }, d ? /* @__PURE__ */ b.createElement(xe, {
    align: "flex-start",
    className: `${p}-title-wrapper`
  }, C, m) : C, u && /* @__PURE__ */ b.createElement(Ge.Text, {
    className: G(`${p}-description`, h.classNames.description, a.description),
    style: l.description
  }, u))));
}
const On = /* @__PURE__ */ b.forwardRef(Tn);
new Intl.Collator(0, {
  numeric: 1
}).compare;
typeof process < "u" && process.versions && process.versions.node;
var $;
class zn extends TransformStream {
  /** Constructs a new instance. */
  constructor(n = {
    allowCR: !1
  }) {
    super({
      transform: (o, r) => {
        for (o = W(this, $) + o; ; ) {
          const i = o.indexOf(`
`), s = n.allowCR ? o.indexOf("\r") : -1;
          if (s !== -1 && s !== o.length - 1 && (i === -1 || i - 1 > s)) {
            r.enqueue(o.slice(0, s)), o = o.slice(s + 1);
            continue;
          }
          if (i === -1) break;
          const a = o[i - 1] === "\r" ? i - 1 : i;
          r.enqueue(o.slice(0, a)), o = o.slice(i + 1);
        }
        Ue(this, $, o);
      },
      flush: (o) => {
        if (W(this, $) === "") return;
        const r = n.allowCR && W(this, $).endsWith("\r") ? W(this, $).slice(0, -1) : W(this, $);
        o.enqueue(r);
      }
    });
    We(this, $, "");
  }
}
$ = new WeakMap();
function Mn(e) {
  try {
    const t = new URL(e);
    return t.protocol === "http:" || t.protocol === "https:";
  } catch {
    return !1;
  }
}
function Pn() {
  const e = document.querySelector(".gradio-container");
  if (!e)
    return "";
  const t = e.className.match(/gradio-container-(.+)/);
  return t ? t[1] : "";
}
const En = +Pn()[0];
function jn(e, t, n) {
  const o = En >= 5 ? "gradio_api/" : "";
  return e == null ? n ? `/proxy=${n}${o}file=` : `${t}${o}file=` : Mn(e) ? e : n ? `/proxy=${n}${o}file=${e}` : `${t}/${o}file=${e}`;
}
const In = (e) => !!e.url;
function kn(e, t, n) {
  if (e)
    return In(e) ? e.url : typeof e == "string" ? e.startsWith("http") ? e : jn(e, t, n) : e;
}
const An = kr(({
  slots: e,
  children: t,
  urlProxyUrl: n,
  urlRoot: o,
  ...r
}) => /* @__PURE__ */ D.jsxs(D.Fragment, {
  children: [/* @__PURE__ */ D.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ D.jsx(On, {
    ...r,
    extra: e.extra ? /* @__PURE__ */ D.jsx(Y, {
      slot: e.extra
    }) : r.extra,
    icon: e.icon ? /* @__PURE__ */ D.jsx(Y, {
      slot: e.icon
    }) : kn(r.icon, o, n),
    title: e.title ? /* @__PURE__ */ D.jsx(Y, {
      slot: e.title
    }) : r.title,
    description: e.description ? /* @__PURE__ */ D.jsx(Y, {
      slot: e.description
    }) : r.description
  })]
}));
export {
  An as Welcome,
  An as default
};
