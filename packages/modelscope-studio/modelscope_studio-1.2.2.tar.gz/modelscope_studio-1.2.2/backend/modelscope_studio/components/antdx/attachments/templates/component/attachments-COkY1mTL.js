import { i as fn, a as _t, r as dn, w as Ue, g as pn, d as mn, b as Ie, c as ne, e as hn } from "./Index-BjvUZ7fL.js";
const M = window.ms_globals.React, l = window.ms_globals.React, qe = window.ms_globals.React.useMemo, jt = window.ms_globals.React.useState, be = window.ms_globals.React.useEffect, ln = window.ms_globals.React.isValidElement, me = window.ms_globals.React.useRef, cn = window.ms_globals.React.useLayoutEffect, un = window.ms_globals.React.forwardRef, Xt = window.ms_globals.ReactDOM, Ve = window.ms_globals.ReactDOM.createPortal, gn = window.ms_globals.internalContext.useContextPropsContext, vn = window.ms_globals.internalContext.ContextPropsProvider, bn = window.ms_globals.antd.ConfigProvider, Rr = window.ms_globals.antd.Upload, We = window.ms_globals.antd.theme, yn = window.ms_globals.antd.Progress, pt = window.ms_globals.antd.Button, Sn = window.ms_globals.antd.Flex, mt = window.ms_globals.antd.Typography, wn = window.ms_globals.antdIcons.FileTextFilled, xn = window.ms_globals.antdIcons.CloseCircleFilled, En = window.ms_globals.antdIcons.FileExcelFilled, Cn = window.ms_globals.antdIcons.FileImageFilled, _n = window.ms_globals.antdIcons.FileMarkdownFilled, Ln = window.ms_globals.antdIcons.FilePdfFilled, Tn = window.ms_globals.antdIcons.FilePptFilled, Rn = window.ms_globals.antdIcons.FileWordFilled, In = window.ms_globals.antdIcons.FileZipFilled, Pn = window.ms_globals.antdIcons.PlusOutlined, Mn = window.ms_globals.antdIcons.LeftOutlined, On = window.ms_globals.antdIcons.RightOutlined, Vt = window.ms_globals.antdCssinjs.unit, ht = window.ms_globals.antdCssinjs.token2CSSVar, Wt = window.ms_globals.antdCssinjs.useStyleRegister, Fn = window.ms_globals.antdCssinjs.useCSSVarRegister, An = window.ms_globals.antdCssinjs.createTheme, $n = window.ms_globals.antdCssinjs.useCacheToken;
var kn = /\s/;
function jn(e) {
  for (var t = e.length; t-- && kn.test(e.charAt(t)); )
    ;
  return t;
}
var Dn = /^\s+/;
function Nn(e) {
  return e && e.slice(0, jn(e) + 1).replace(Dn, "");
}
var Gt = NaN, zn = /^[-+]0x[0-9a-f]+$/i, Hn = /^0b[01]+$/i, Un = /^0o[0-7]+$/i, Bn = parseInt;
function Kt(e) {
  if (typeof e == "number")
    return e;
  if (fn(e))
    return Gt;
  if (_t(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = _t(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Nn(e);
  var r = Hn.test(e);
  return r || Un.test(e) ? Bn(e.slice(2), r ? 2 : 8) : zn.test(e) ? Gt : +e;
}
function Xn() {
}
var gt = function() {
  return dn.Date.now();
}, Vn = "Expected a function", Wn = Math.max, Gn = Math.min;
function Kn(e, t, r) {
  var n, o, i, s, a, c, u = 0, d = !1, f = !1, p = !0;
  if (typeof e != "function")
    throw new TypeError(Vn);
  t = Kt(t) || 0, _t(r) && (d = !!r.leading, f = "maxWait" in r, i = f ? Wn(Kt(r.maxWait) || 0, t) : i, p = "trailing" in r ? !!r.trailing : p);
  function h(g) {
    var b = n, x = o;
    return n = o = void 0, u = g, s = e.apply(x, b), s;
  }
  function v(g) {
    return u = g, a = setTimeout(_, t), d ? h(g) : s;
  }
  function y(g) {
    var b = g - c, x = g - u, P = t - b;
    return f ? Gn(P, i - x) : P;
  }
  function m(g) {
    var b = g - c, x = g - u;
    return c === void 0 || b >= t || b < 0 || f && x >= i;
  }
  function _() {
    var g = gt();
    if (m(g))
      return E(g);
    a = setTimeout(_, y(g));
  }
  function E(g) {
    return a = void 0, p && n ? h(g) : (n = o = void 0, s);
  }
  function w() {
    a !== void 0 && clearTimeout(a), u = 0, n = c = o = a = void 0;
  }
  function S() {
    return a === void 0 ? s : E(gt());
  }
  function C() {
    var g = gt(), b = m(g);
    if (n = arguments, o = this, c = g, b) {
      if (a === void 0)
        return v(c);
      if (f)
        return clearTimeout(a), a = setTimeout(_, t), h(c);
    }
    return a === void 0 && (a = setTimeout(_, t)), s;
  }
  return C.cancel = w, C.flush = S, C;
}
var Ir = {
  exports: {}
}, Ze = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var qn = l, Zn = Symbol.for("react.element"), Qn = Symbol.for("react.fragment"), Yn = Object.prototype.hasOwnProperty, Jn = qn.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, eo = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Pr(e, t, r) {
  var n, o = {}, i = null, s = null;
  r !== void 0 && (i = "" + r), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) Yn.call(t, n) && !eo.hasOwnProperty(n) && (o[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: Zn,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: Jn.current
  };
}
Ze.Fragment = Qn;
Ze.jsx = Pr;
Ze.jsxs = Pr;
Ir.exports = Ze;
var oe = Ir.exports;
const {
  SvelteComponent: to,
  assign: qt,
  binding_callbacks: Zt,
  check_outros: ro,
  children: Mr,
  claim_element: Or,
  claim_space: no,
  component_subscribe: Qt,
  compute_slots: oo,
  create_slot: io,
  detach: Se,
  element: Fr,
  empty: Yt,
  exclude_internal_props: Jt,
  get_all_dirty_from_scope: so,
  get_slot_changes: ao,
  group_outros: lo,
  init: co,
  insert_hydration: Be,
  safe_not_equal: uo,
  set_custom_element_data: Ar,
  space: fo,
  transition_in: Xe,
  transition_out: Lt,
  update_slot_base: po
} = window.__gradio__svelte__internal, {
  beforeUpdate: mo,
  getContext: ho,
  onDestroy: go,
  setContext: vo
} = window.__gradio__svelte__internal;
function er(e) {
  let t, r;
  const n = (
    /*#slots*/
    e[7].default
  ), o = io(
    n,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Fr("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = Or(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Mr(t);
      o && o.l(s), s.forEach(Se), this.h();
    },
    h() {
      Ar(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Be(i, t, s), o && o.m(t, null), e[9](t), r = !0;
    },
    p(i, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && po(
        o,
        n,
        i,
        /*$$scope*/
        i[6],
        r ? ao(
          n,
          /*$$scope*/
          i[6],
          s,
          null
        ) : so(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      r || (Xe(o, i), r = !0);
    },
    o(i) {
      Lt(o, i), r = !1;
    },
    d(i) {
      i && Se(t), o && o.d(i), e[9](null);
    }
  };
}
function bo(e) {
  let t, r, n, o, i = (
    /*$$slots*/
    e[4].default && er(e)
  );
  return {
    c() {
      t = Fr("react-portal-target"), r = fo(), i && i.c(), n = Yt(), this.h();
    },
    l(s) {
      t = Or(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Mr(t).forEach(Se), r = no(s), i && i.l(s), n = Yt(), this.h();
    },
    h() {
      Ar(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Be(s, t, a), e[8](t), Be(s, r, a), i && i.m(s, a), Be(s, n, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && Xe(i, 1)) : (i = er(s), i.c(), Xe(i, 1), i.m(n.parentNode, n)) : i && (lo(), Lt(i, 1, 1, () => {
        i = null;
      }), ro());
    },
    i(s) {
      o || (Xe(i), o = !0);
    },
    o(s) {
      Lt(i), o = !1;
    },
    d(s) {
      s && (Se(t), Se(r), Se(n)), e[8](null), i && i.d(s);
    }
  };
}
function tr(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function yo(e, t, r) {
  let n, o, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = oo(i);
  let {
    svelteInit: c
  } = t;
  const u = Ue(tr(t)), d = Ue();
  Qt(e, d, (S) => r(0, n = S));
  const f = Ue();
  Qt(e, f, (S) => r(1, o = S));
  const p = [], h = ho("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: y,
    subSlotIndex: m
  } = pn() || {}, _ = c({
    parent: h,
    props: u,
    target: d,
    slot: f,
    slotKey: v,
    slotIndex: y,
    subSlotIndex: m,
    onDestroy(S) {
      p.push(S);
    }
  });
  vo("$$ms-gr-react-wrapper", _), mo(() => {
    u.set(tr(t));
  }), go(() => {
    p.forEach((S) => S());
  });
  function E(S) {
    Zt[S ? "unshift" : "push"](() => {
      n = S, d.set(n);
    });
  }
  function w(S) {
    Zt[S ? "unshift" : "push"](() => {
      o = S, f.set(o);
    });
  }
  return e.$$set = (S) => {
    r(17, t = qt(qt({}, t), Jt(S))), "svelteInit" in S && r(5, c = S.svelteInit), "$$scope" in S && r(6, s = S.$$scope);
  }, t = Jt(t), [n, o, d, f, a, c, s, i, E, w];
}
class So extends to {
  constructor(t) {
    super(), co(this, t, yo, bo, uo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ms
} = window.__gradio__svelte__internal, rr = window.ms_globals.rerender, vt = window.ms_globals.tree;
function wo(e, t = {}) {
  function r(n) {
    const o = Ue(), i = new So({
      ...n,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? vt;
          return c.nodes = [...c.nodes, a], rr({
            createPortal: Ve,
            node: vt
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), rr({
              createPortal: Ve,
              node: vt
            });
          }), a;
        },
        ...n.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(r);
    });
  });
}
function xo(e) {
  const [t, r] = jt(() => Ie(e));
  return be(() => {
    let n = !0;
    return e.subscribe((i) => {
      n && (n = !1, i === t) || r(i);
    });
  }, [e]), t;
}
function Eo(e) {
  const t = qe(() => mn(e, (r) => r), [e]);
  return xo(t);
}
const Co = "1.0.5", _o = /* @__PURE__ */ l.createContext({}), Lo = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, To = (e) => {
  const t = l.useContext(_o);
  return l.useMemo(() => ({
    ...Lo,
    ...t[e]
  }), [t[e]]);
};
function Pe() {
  return Pe = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var r = arguments[t];
      for (var n in r) ({}).hasOwnProperty.call(r, n) && (e[n] = r[n]);
    }
    return e;
  }, Pe.apply(null, arguments);
}
function Ge() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: n,
    theme: o
  } = l.useContext(bn.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: r,
    iconPrefixCls: n
  };
}
function Ee(e) {
  var t = M.useRef();
  t.current = e;
  var r = M.useCallback(function() {
    for (var n, o = arguments.length, i = new Array(o), s = 0; s < o; s++)
      i[s] = arguments[s];
    return (n = t.current) === null || n === void 0 ? void 0 : n.call.apply(n, [t].concat(i));
  }, []);
  return r;
}
function Ro(e) {
  if (Array.isArray(e)) return e;
}
function Io(e, t) {
  var r = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (r != null) {
    var n, o, i, s, a = [], c = !0, u = !1;
    try {
      if (i = (r = r.call(e)).next, t === 0) {
        if (Object(r) !== r) return;
        c = !1;
      } else for (; !(c = (n = i.call(r)).done) && (a.push(n.value), a.length !== t); c = !0) ;
    } catch (d) {
      u = !0, o = d;
    } finally {
      try {
        if (!c && r.return != null && (s = r.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function nr(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var r = 0, n = Array(t); r < t; r++) n[r] = e[r];
  return n;
}
function Po(e, t) {
  if (e) {
    if (typeof e == "string") return nr(e, t);
    var r = {}.toString.call(e).slice(8, -1);
    return r === "Object" && e.constructor && (r = e.constructor.name), r === "Map" || r === "Set" ? Array.from(e) : r === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? nr(e, t) : void 0;
  }
}
function Mo() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function Q(e, t) {
  return Ro(e) || Io(e, t) || Po(e, t) || Mo();
}
function Qe() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var or = Qe() ? M.useLayoutEffect : M.useEffect, Oo = function(t, r) {
  var n = M.useRef(!0);
  or(function() {
    return t(n.current);
  }, r), or(function() {
    return n.current = !1, function() {
      n.current = !0;
    };
  }, []);
}, ir = function(t, r) {
  Oo(function(n) {
    if (!n)
      return t();
  }, r);
};
function Me(e) {
  var t = M.useRef(!1), r = M.useState(e), n = Q(r, 2), o = n[0], i = n[1];
  M.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, c) {
    c && t.current || i(a);
  }
  return [o, s];
}
function bt(e) {
  return e !== void 0;
}
function Fo(e, t) {
  var r = t || {}, n = r.defaultValue, o = r.value, i = r.onChange, s = r.postState, a = Me(function() {
    return bt(o) ? o : bt(n) ? typeof n == "function" ? n() : n : typeof e == "function" ? e() : e;
  }), c = Q(a, 2), u = c[0], d = c[1], f = o !== void 0 ? o : u, p = s ? s(f) : f, h = Ee(i), v = Me([f]), y = Q(v, 2), m = y[0], _ = y[1];
  ir(function() {
    var w = m[0];
    u !== w && h(u, w);
  }, [m]), ir(function() {
    bt(o) || d(o);
  }, [o]);
  var E = Ee(function(w, S) {
    d(w, S), _([f], S);
  });
  return [p, E];
}
function G(e) {
  "@babel/helpers - typeof";
  return G = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, G(e);
}
var $r = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Dt = Symbol.for("react.element"), Nt = Symbol.for("react.portal"), Ye = Symbol.for("react.fragment"), Je = Symbol.for("react.strict_mode"), et = Symbol.for("react.profiler"), tt = Symbol.for("react.provider"), rt = Symbol.for("react.context"), Ao = Symbol.for("react.server_context"), nt = Symbol.for("react.forward_ref"), ot = Symbol.for("react.suspense"), it = Symbol.for("react.suspense_list"), st = Symbol.for("react.memo"), at = Symbol.for("react.lazy"), $o = Symbol.for("react.offscreen"), kr;
kr = Symbol.for("react.module.reference");
function ie(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Dt:
        switch (e = e.type, e) {
          case Ye:
          case et:
          case Je:
          case ot:
          case it:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Ao:
              case rt:
              case nt:
              case at:
              case st:
              case tt:
                return e;
              default:
                return t;
            }
        }
      case Nt:
        return t;
    }
  }
}
O.ContextConsumer = rt;
O.ContextProvider = tt;
O.Element = Dt;
O.ForwardRef = nt;
O.Fragment = Ye;
O.Lazy = at;
O.Memo = st;
O.Portal = Nt;
O.Profiler = et;
O.StrictMode = Je;
O.Suspense = ot;
O.SuspenseList = it;
O.isAsyncMode = function() {
  return !1;
};
O.isConcurrentMode = function() {
  return !1;
};
O.isContextConsumer = function(e) {
  return ie(e) === rt;
};
O.isContextProvider = function(e) {
  return ie(e) === tt;
};
O.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Dt;
};
O.isForwardRef = function(e) {
  return ie(e) === nt;
};
O.isFragment = function(e) {
  return ie(e) === Ye;
};
O.isLazy = function(e) {
  return ie(e) === at;
};
O.isMemo = function(e) {
  return ie(e) === st;
};
O.isPortal = function(e) {
  return ie(e) === Nt;
};
O.isProfiler = function(e) {
  return ie(e) === et;
};
O.isStrictMode = function(e) {
  return ie(e) === Je;
};
O.isSuspense = function(e) {
  return ie(e) === ot;
};
O.isSuspenseList = function(e) {
  return ie(e) === it;
};
O.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Ye || e === et || e === Je || e === ot || e === it || e === $o || typeof e == "object" && e !== null && (e.$$typeof === at || e.$$typeof === st || e.$$typeof === tt || e.$$typeof === rt || e.$$typeof === nt || e.$$typeof === kr || e.getModuleId !== void 0);
};
O.typeOf = ie;
$r.exports = O;
var yt = $r.exports, ko = Symbol.for("react.element"), jo = Symbol.for("react.transitional.element"), Do = Symbol.for("react.fragment");
function No(e) {
  return (
    // Base object type
    e && G(e) === "object" && // React Element type
    (e.$$typeof === ko || e.$$typeof === jo) && // React Fragment type
    e.type === Do
  );
}
var zo = function(t, r) {
  typeof t == "function" ? t(r) : G(t) === "object" && t && "current" in t && (t.current = r);
}, Ho = function(t) {
  var r, n;
  if (!t)
    return !1;
  if (jr(t) && t.props.propertyIsEnumerable("ref"))
    return !0;
  var o = yt.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((r = o.prototype) !== null && r !== void 0 && r.render) && o.$$typeof !== yt.ForwardRef || typeof t == "function" && !((n = t.prototype) !== null && n !== void 0 && n.render) && t.$$typeof !== yt.ForwardRef);
};
function jr(e) {
  return /* @__PURE__ */ ln(e) && !No(e);
}
var Uo = function(t) {
  if (t && jr(t)) {
    var r = t;
    return r.props.propertyIsEnumerable("ref") ? r.props.ref : r.ref;
  }
  return null;
};
function Bo(e, t) {
  if (G(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var n = r.call(e, t);
    if (G(n) != "object") return n;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Dr(e) {
  var t = Bo(e, "string");
  return G(t) == "symbol" ? t : t + "";
}
function D(e, t, r) {
  return (t = Dr(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
function sr(e, t) {
  var r = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var n = Object.getOwnPropertySymbols(e);
    t && (n = n.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), r.push.apply(r, n);
  }
  return r;
}
function L(e) {
  for (var t = 1; t < arguments.length; t++) {
    var r = arguments[t] != null ? arguments[t] : {};
    t % 2 ? sr(Object(r), !0).forEach(function(n) {
      D(e, n, r[n]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(r)) : sr(Object(r)).forEach(function(n) {
      Object.defineProperty(e, n, Object.getOwnPropertyDescriptor(r, n));
    });
  }
  return e;
}
const Fe = /* @__PURE__ */ l.createContext(null);
function ar(e) {
  const {
    getDropContainer: t,
    className: r,
    prefixCls: n,
    children: o
  } = e, {
    disabled: i
  } = l.useContext(Fe), [s, a] = l.useState(), [c, u] = l.useState(null);
  if (l.useEffect(() => {
    const p = t == null ? void 0 : t();
    s !== p && a(p);
  }, [t]), l.useEffect(() => {
    if (s) {
      const p = () => {
        u(!0);
      }, h = (m) => {
        m.preventDefault();
      }, v = (m) => {
        m.relatedTarget || u(!1);
      }, y = (m) => {
        u(!1), m.preventDefault();
      };
      return document.addEventListener("dragenter", p), document.addEventListener("dragover", h), document.addEventListener("dragleave", v), document.addEventListener("drop", y), () => {
        document.removeEventListener("dragenter", p), document.removeEventListener("dragover", h), document.removeEventListener("dragleave", v), document.removeEventListener("drop", y);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const f = `${n}-drop-area`;
  return /* @__PURE__ */ Ve(/* @__PURE__ */ l.createElement("div", {
    className: ne(f, r, {
      [`${f}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, o), s);
}
function lr(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function Xo(e) {
  return e && G(e) === "object" && lr(e.nativeElement) ? e.nativeElement : lr(e) ? e : null;
}
function Vo(e) {
  var t = Xo(e);
  if (t)
    return t;
  if (e instanceof l.Component) {
    var r;
    return (r = Xt.findDOMNode) === null || r === void 0 ? void 0 : r.call(Xt, e);
  }
  return null;
}
function Wo(e, t) {
  if (e == null) return {};
  var r = {};
  for (var n in e) if ({}.hasOwnProperty.call(e, n)) {
    if (t.includes(n)) continue;
    r[n] = e[n];
  }
  return r;
}
function cr(e, t) {
  if (e == null) return {};
  var r, n, o = Wo(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (n = 0; n < i.length; n++) r = i[n], t.includes(r) || {}.propertyIsEnumerable.call(e, r) && (o[r] = e[r]);
  }
  return o;
}
var Go = /* @__PURE__ */ M.createContext({});
function Ce(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function ur(e, t) {
  for (var r = 0; r < t.length; r++) {
    var n = t[r];
    n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(e, Dr(n.key), n);
  }
}
function _e(e, t, r) {
  return t && ur(e.prototype, t), r && ur(e, r), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Tt(e, t) {
  return Tt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(r, n) {
    return r.__proto__ = n, r;
  }, Tt(e, t);
}
function lt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Tt(e, t);
}
function Ke(e) {
  return Ke = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Ke(e);
}
function Nr() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Nr = function() {
    return !!e;
  })();
}
function ye(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function Ko(e, t) {
  if (t && (G(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ye(e);
}
function ct(e) {
  var t = Nr();
  return function() {
    var r, n = Ke(e);
    if (t) {
      var o = Ke(this).constructor;
      r = Reflect.construct(n, arguments, o);
    } else r = n.apply(this, arguments);
    return Ko(this, r);
  };
}
var qo = /* @__PURE__ */ function(e) {
  lt(r, e);
  var t = ct(r);
  function r() {
    return Ce(this, r), t.apply(this, arguments);
  }
  return _e(r, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), r;
}(M.Component);
function Zo(e) {
  var t = M.useReducer(function(a) {
    return a + 1;
  }, 0), r = Q(t, 2), n = r[1], o = M.useRef(e), i = Ee(function() {
    return o.current;
  }), s = Ee(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, n();
  });
  return [i, s];
}
var he = "none", ke = "appear", je = "enter", De = "leave", fr = "none", ae = "prepare", we = "start", xe = "active", zt = "end", zr = "prepared";
function dr(e, t) {
  var r = {};
  return r[e.toLowerCase()] = t.toLowerCase(), r["Webkit".concat(e)] = "webkit".concat(t), r["Moz".concat(e)] = "moz".concat(t), r["ms".concat(e)] = "MS".concat(t), r["O".concat(e)] = "o".concat(t.toLowerCase()), r;
}
function Qo(e, t) {
  var r = {
    animationend: dr("Animation", "AnimationEnd"),
    transitionend: dr("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete r.animationend.animation, "TransitionEvent" in t || delete r.transitionend.transition), r;
}
var Yo = Qo(Qe(), typeof window < "u" ? window : {}), Hr = {};
if (Qe()) {
  var Jo = document.createElement("div");
  Hr = Jo.style;
}
var Ne = {};
function Ur(e) {
  if (Ne[e])
    return Ne[e];
  var t = Yo[e];
  if (t)
    for (var r = Object.keys(t), n = r.length, o = 0; o < n; o += 1) {
      var i = r[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Hr)
        return Ne[e] = t[i], Ne[e];
    }
  return "";
}
var Br = Ur("animationend"), Xr = Ur("transitionend"), Vr = !!(Br && Xr), pr = Br || "animationend", mr = Xr || "transitionend";
function hr(e, t) {
  if (!e) return null;
  if (G(e) === "object") {
    var r = t.replace(/-\w/g, function(n) {
      return n[1].toUpperCase();
    });
    return e[r];
  }
  return "".concat(e, "-").concat(t);
}
const ei = function(e) {
  var t = me();
  function r(o) {
    o && (o.removeEventListener(mr, e), o.removeEventListener(pr, e));
  }
  function n(o) {
    t.current && t.current !== o && r(t.current), o && o !== t.current && (o.addEventListener(mr, e), o.addEventListener(pr, e), t.current = o);
  }
  return M.useEffect(function() {
    return function() {
      r(t.current);
    };
  }, []), [n, r];
};
var Wr = Qe() ? cn : be, Gr = function(t) {
  return +setTimeout(t, 16);
}, Kr = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Gr = function(t) {
  return window.requestAnimationFrame(t);
}, Kr = function(t) {
  return window.cancelAnimationFrame(t);
});
var gr = 0, Ht = /* @__PURE__ */ new Map();
function qr(e) {
  Ht.delete(e);
}
var Rt = function(t) {
  var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  gr += 1;
  var n = gr;
  function o(i) {
    if (i === 0)
      qr(n), t();
    else {
      var s = Gr(function() {
        o(i - 1);
      });
      Ht.set(n, s);
    }
  }
  return o(r), n;
};
Rt.cancel = function(e) {
  var t = Ht.get(e);
  return qr(e), Kr(t);
};
const ti = function() {
  var e = M.useRef(null);
  function t() {
    Rt.cancel(e.current);
  }
  function r(n) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = Rt(function() {
      o <= 1 ? n({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : r(n, o - 1);
    });
    e.current = i;
  }
  return M.useEffect(function() {
    return function() {
      t();
    };
  }, []), [r, t];
};
var ri = [ae, we, xe, zt], ni = [ae, zr], Zr = !1, oi = !0;
function Qr(e) {
  return e === xe || e === zt;
}
const ii = function(e, t, r) {
  var n = Me(fr), o = Q(n, 2), i = o[0], s = o[1], a = ti(), c = Q(a, 2), u = c[0], d = c[1];
  function f() {
    s(ae, !0);
  }
  var p = t ? ni : ri;
  return Wr(function() {
    if (i !== fr && i !== zt) {
      var h = p.indexOf(i), v = p[h + 1], y = r(i);
      y === Zr ? s(v, !0) : v && u(function(m) {
        function _() {
          m.isCanceled() || s(v, !0);
        }
        y === !0 ? _() : Promise.resolve(y).then(_);
      });
    }
  }, [e, i]), M.useEffect(function() {
    return function() {
      d();
    };
  }, []), [f, i];
};
function si(e, t, r, n) {
  var o = n.motionEnter, i = o === void 0 ? !0 : o, s = n.motionAppear, a = s === void 0 ? !0 : s, c = n.motionLeave, u = c === void 0 ? !0 : c, d = n.motionDeadline, f = n.motionLeaveImmediately, p = n.onAppearPrepare, h = n.onEnterPrepare, v = n.onLeavePrepare, y = n.onAppearStart, m = n.onEnterStart, _ = n.onLeaveStart, E = n.onAppearActive, w = n.onEnterActive, S = n.onLeaveActive, C = n.onAppearEnd, g = n.onEnterEnd, b = n.onLeaveEnd, x = n.onVisibleChanged, P = Me(), A = Q(P, 2), $ = A[0], T = A[1], I = Zo(he), F = Q(I, 2), R = F[0], k = F[1], ee = Me(null), Y = Q(ee, 2), le = Y[0], B = Y[1], N = R(), H = me(!1), K = me(null);
  function X() {
    return r();
  }
  var ce = me(!1);
  function ge() {
    k(he), B(null, !0);
  }
  var z = Ee(function(J) {
    var Z = R();
    if (Z !== he) {
      var fe = X();
      if (!(J && !J.deadline && J.target !== fe)) {
        var Ae = ce.current, $e;
        Z === ke && Ae ? $e = C == null ? void 0 : C(fe, J) : Z === je && Ae ? $e = g == null ? void 0 : g(fe, J) : Z === De && Ae && ($e = b == null ? void 0 : b(fe, J)), Ae && $e !== !1 && ge();
      }
    }
  }), U = ei(z), q = Q(U, 1), ue = q[0], V = function(Z) {
    switch (Z) {
      case ke:
        return D(D(D({}, ae, p), we, y), xe, E);
      case je:
        return D(D(D({}, ae, h), we, m), xe, w);
      case De:
        return D(D(D({}, ae, v), we, _), xe, S);
      default:
        return {};
    }
  }, se = M.useMemo(function() {
    return V(N);
  }, [N]), ve = ii(N, !e, function(J) {
    if (J === ae) {
      var Z = se[ae];
      return Z ? Z(X()) : Zr;
    }
    if (j in se) {
      var fe;
      B(((fe = se[j]) === null || fe === void 0 ? void 0 : fe.call(se, X(), null)) || null);
    }
    return j === xe && N !== he && (ue(X()), d > 0 && (clearTimeout(K.current), K.current = setTimeout(function() {
      z({
        deadline: !0
      });
    }, d))), j === zr && ge(), oi;
  }), Le = Q(ve, 2), Te = Le[0], j = Le[1], ut = Qr(j);
  ce.current = ut;
  var Bt = me(null);
  Wr(function() {
    if (!(H.current && Bt.current === t)) {
      T(t);
      var J = H.current;
      H.current = !0;
      var Z;
      !J && t && a && (Z = ke), J && t && i && (Z = je), (J && !t && u || !J && f && !t && u) && (Z = De);
      var fe = V(Z);
      Z && (e || fe[ae]) ? (k(Z), Te()) : k(he), Bt.current = t;
    }
  }, [t]), be(function() {
    // Cancel appear
    (N === ke && !a || // Cancel enter
    N === je && !i || // Cancel leave
    N === De && !u) && k(he);
  }, [a, i, u]), be(function() {
    return function() {
      H.current = !1, clearTimeout(K.current);
    };
  }, []);
  var ft = M.useRef(!1);
  be(function() {
    $ && (ft.current = !0), $ !== void 0 && N === he && ((ft.current || $) && (x == null || x($)), ft.current = !0);
  }, [$, N]);
  var dt = le;
  return se[ae] && j === we && (dt = L({
    transition: "none"
  }, dt)), [N, j, dt, $ ?? t];
}
function ai(e) {
  var t = e;
  G(e) === "object" && (t = e.transitionSupport);
  function r(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var n = /* @__PURE__ */ M.forwardRef(function(o, i) {
    var s = o.visible, a = s === void 0 ? !0 : s, c = o.removeOnLeave, u = c === void 0 ? !0 : c, d = o.forceRender, f = o.children, p = o.motionName, h = o.leavedClassName, v = o.eventProps, y = M.useContext(Go), m = y.motion, _ = r(o, m), E = me(), w = me();
    function S() {
      try {
        return E.current instanceof HTMLElement ? E.current : Vo(w.current);
      } catch {
        return null;
      }
    }
    var C = si(_, a, S, o), g = Q(C, 4), b = g[0], x = g[1], P = g[2], A = g[3], $ = M.useRef(A);
    A && ($.current = !0);
    var T = M.useCallback(function(Y) {
      E.current = Y, zo(i, Y);
    }, [i]), I, F = L(L({}, v), {}, {
      visible: a
    });
    if (!f)
      I = null;
    else if (b === he)
      A ? I = f(L({}, F), T) : !u && $.current && h ? I = f(L(L({}, F), {}, {
        className: h
      }), T) : d || !u && !h ? I = f(L(L({}, F), {}, {
        style: {
          display: "none"
        }
      }), T) : I = null;
    else {
      var R;
      x === ae ? R = "prepare" : Qr(x) ? R = "active" : x === we && (R = "start");
      var k = hr(p, "".concat(b, "-").concat(R));
      I = f(L(L({}, F), {}, {
        className: ne(hr(p, b), D(D({}, k, k && R), p, typeof p == "string")),
        style: P
      }), T);
    }
    if (/* @__PURE__ */ M.isValidElement(I) && Ho(I)) {
      var ee = Uo(I);
      ee || (I = /* @__PURE__ */ M.cloneElement(I, {
        ref: T
      }));
    }
    return /* @__PURE__ */ M.createElement(qo, {
      ref: w
    }, I);
  });
  return n.displayName = "CSSMotion", n;
}
const li = ai(Vr);
var It = "add", Pt = "keep", Mt = "remove", St = "removed";
function ci(e) {
  var t;
  return e && G(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, L(L({}, t), {}, {
    key: String(t.key)
  });
}
function Ot() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(ci);
}
function ui() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], r = [], n = 0, o = t.length, i = Ot(e), s = Ot(t);
  i.forEach(function(u) {
    for (var d = !1, f = n; f < o; f += 1) {
      var p = s[f];
      if (p.key === u.key) {
        n < f && (r = r.concat(s.slice(n, f).map(function(h) {
          return L(L({}, h), {}, {
            status: It
          });
        })), n = f), r.push(L(L({}, p), {}, {
          status: Pt
        })), n += 1, d = !0;
        break;
      }
    }
    d || r.push(L(L({}, u), {}, {
      status: Mt
    }));
  }), n < o && (r = r.concat(s.slice(n).map(function(u) {
    return L(L({}, u), {}, {
      status: It
    });
  })));
  var a = {};
  r.forEach(function(u) {
    var d = u.key;
    a[d] = (a[d] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return c.forEach(function(u) {
    r = r.filter(function(d) {
      var f = d.key, p = d.status;
      return f !== u || p !== Mt;
    }), r.forEach(function(d) {
      d.key === u && (d.status = Pt);
    });
  }), r;
}
var fi = ["component", "children", "onVisibleChanged", "onAllRemoved"], di = ["status"], pi = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function mi(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : li, r = /* @__PURE__ */ function(n) {
    lt(i, n);
    var o = ct(i);
    function i() {
      var s;
      Ce(this, i);
      for (var a = arguments.length, c = new Array(a), u = 0; u < a; u++)
        c[u] = arguments[u];
      return s = o.call.apply(o, [this].concat(c)), D(ye(s), "state", {
        keyEntities: []
      }), D(ye(s), "removeKey", function(d) {
        s.setState(function(f) {
          var p = f.keyEntities.map(function(h) {
            return h.key !== d ? h : L(L({}, h), {}, {
              status: St
            });
          });
          return {
            keyEntities: p
          };
        }, function() {
          var f = s.state.keyEntities, p = f.filter(function(h) {
            var v = h.status;
            return v !== St;
          }).length;
          p === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return _e(i, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, u = this.props, d = u.component, f = u.children, p = u.onVisibleChanged;
        u.onAllRemoved;
        var h = cr(u, fi), v = d || M.Fragment, y = {};
        return pi.forEach(function(m) {
          y[m] = h[m], delete h[m];
        }), delete h.keys, /* @__PURE__ */ M.createElement(v, h, c.map(function(m, _) {
          var E = m.status, w = cr(m, di), S = E === It || E === Pt;
          return /* @__PURE__ */ M.createElement(t, Pe({}, y, {
            key: w.key,
            visible: S,
            eventProps: w,
            onVisibleChanged: function(g) {
              p == null || p(g, {
                key: w.key
              }), g || a.removeKey(w.key);
            }
          }), function(C, g) {
            return f(L(L({}, C), {}, {
              index: _
            }), g);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var u = a.keys, d = c.keyEntities, f = Ot(u), p = ui(d, f);
        return {
          keyEntities: p.filter(function(h) {
            var v = d.find(function(y) {
              var m = y.key;
              return h.key === m;
            });
            return !(v && v.status === St && h.status === Mt);
          })
        };
      }
    }]), i;
  }(M.Component);
  return D(r, "defaultProps", {
    component: "div"
  }), r;
}
const hi = mi(Vr);
function gi(e, t) {
  const {
    children: r,
    upload: n,
    rootClassName: o
  } = e, i = l.useRef(null);
  return l.useImperativeHandle(t, () => i.current), /* @__PURE__ */ l.createElement(Rr, Pe({}, n, {
    showUploadList: !1,
    rootClassName: o,
    ref: i
  }), r);
}
const Yr = /* @__PURE__ */ l.forwardRef(gi);
var Jr = /* @__PURE__ */ _e(function e() {
  Ce(this, e);
}), en = "CALC_UNIT", vi = new RegExp(en, "g");
function wt(e) {
  return typeof e == "number" ? "".concat(e).concat(en) : e;
}
var bi = /* @__PURE__ */ function(e) {
  lt(r, e);
  var t = ct(r);
  function r(n, o) {
    var i;
    Ce(this, r), i = t.call(this), D(ye(i), "result", ""), D(ye(i), "unitlessCssVar", void 0), D(ye(i), "lowPriority", void 0);
    var s = G(n);
    return i.unitlessCssVar = o, n instanceof r ? i.result = "(".concat(n.result, ")") : s === "number" ? i.result = wt(n) : s === "string" && (i.result = n), i;
  }
  return _e(r, [{
    key: "add",
    value: function(o) {
      return o instanceof r ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(wt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof r ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(wt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof r ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof r ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var i = this, s = o || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (c = !1), this.result = this.result.replace(vi, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), r;
}(Jr), yi = /* @__PURE__ */ function(e) {
  lt(r, e);
  var t = ct(r);
  function r(n) {
    var o;
    return Ce(this, r), o = t.call(this), D(ye(o), "result", 0), n instanceof r ? o.result = n.result : typeof n == "number" && (o.result = n), o;
  }
  return _e(r, [{
    key: "add",
    value: function(o) {
      return o instanceof r ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof r ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof r ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof r ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), r;
}(Jr), Si = function(t, r) {
  var n = t === "css" ? bi : yi;
  return function(o) {
    return new n(o, r);
  };
}, vr = function(t, r) {
  return "".concat([r, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function br(e, t, r, n) {
  var o = L({}, t[e]);
  if (n != null && n.deprecatedTokens) {
    var i = n.deprecatedTokens;
    i.forEach(function(a) {
      var c = Q(a, 2), u = c[0], d = c[1];
      if (o != null && o[u] || o != null && o[d]) {
        var f;
        (f = o[d]) !== null && f !== void 0 || (o[d] = o == null ? void 0 : o[u]);
      }
    });
  }
  var s = L(L({}, r), o);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var tn = typeof CSSINJS_STATISTIC < "u", Ft = !0;
function Ut() {
  for (var e = arguments.length, t = new Array(e), r = 0; r < e; r++)
    t[r] = arguments[r];
  if (!tn)
    return Object.assign.apply(Object, [{}].concat(t));
  Ft = !1;
  var n = {};
  return t.forEach(function(o) {
    if (G(o) === "object") {
      var i = Object.keys(o);
      i.forEach(function(s) {
        Object.defineProperty(n, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[s];
          }
        });
      });
    }
  }), Ft = !0, n;
}
var yr = {};
function wi() {
}
var xi = function(t) {
  var r, n = t, o = wi;
  return tn && typeof Proxy < "u" && (r = /* @__PURE__ */ new Set(), n = new Proxy(t, {
    get: function(s, a) {
      if (Ft) {
        var c;
        (c = r) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), o = function(s, a) {
    var c;
    yr[s] = {
      global: Array.from(r),
      component: L(L({}, (c = yr[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: n,
    keys: r,
    flush: o
  };
};
function Sr(e, t, r) {
  if (typeof r == "function") {
    var n;
    return r(Ut(t, (n = t[e]) !== null && n !== void 0 ? n : {}));
  }
  return r ?? {};
}
function Ei(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var r = arguments.length, n = new Array(r), o = 0; o < r; o++)
        n[o] = arguments[o];
      return "max(".concat(n.map(function(i) {
        return Vt(i);
      }).join(","), ")");
    },
    min: function() {
      for (var r = arguments.length, n = new Array(r), o = 0; o < r; o++)
        n[o] = arguments[o];
      return "min(".concat(n.map(function(i) {
        return Vt(i);
      }).join(","), ")");
    }
  };
}
var Ci = 1e3 * 60 * 10, _i = /* @__PURE__ */ function() {
  function e() {
    Ce(this, e), D(this, "map", /* @__PURE__ */ new Map()), D(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), D(this, "nextID", 0), D(this, "lastAccessBeat", /* @__PURE__ */ new Map()), D(this, "accessBeat", 0);
  }
  return _e(e, [{
    key: "set",
    value: function(r, n) {
      this.clear();
      var o = this.getCompositeKey(r);
      this.map.set(o, n), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(r) {
      var n = this.getCompositeKey(r), o = this.map.get(n);
      return this.lastAccessBeat.set(n, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(r) {
      var n = this, o = r.map(function(i) {
        return i && G(i) === "object" ? "obj_".concat(n.getObjectID(i)) : "".concat(G(i), "_").concat(i);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(r) {
      if (this.objectIDMap.has(r))
        return this.objectIDMap.get(r);
      var n = this.nextID;
      return this.objectIDMap.set(r, n), this.nextID += 1, n;
    }
  }, {
    key: "clear",
    value: function() {
      var r = this;
      if (this.accessBeat > 1e4) {
        var n = Date.now();
        this.lastAccessBeat.forEach(function(o, i) {
          n - o > Ci && (r.map.delete(i), r.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), wr = new _i();
function Li(e, t) {
  return l.useMemo(function() {
    var r = wr.get(t);
    if (r)
      return r;
    var n = e();
    return wr.set(t, n), n;
  }, t);
}
var Ti = function() {
  return {};
};
function Ri(e) {
  var t = e.useCSP, r = t === void 0 ? Ti : t, n = e.useToken, o = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(p, h, v, y) {
    var m = Array.isArray(p) ? p[0] : p;
    function _(x) {
      return "".concat(String(m)).concat(x.slice(0, 1).toUpperCase()).concat(x.slice(1));
    }
    var E = (y == null ? void 0 : y.unitless) || {}, w = typeof a == "function" ? a(p) : {}, S = L(L({}, w), {}, D({}, _("zIndexPopup"), !0));
    Object.keys(E).forEach(function(x) {
      S[_(x)] = E[x];
    });
    var C = L(L({}, y), {}, {
      unitless: S,
      prefixToken: _
    }), g = d(p, h, v, C), b = u(m, v, C);
    return function(x) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : x, A = g(x, P), $ = Q(A, 2), T = $[1], I = b(P), F = Q(I, 2), R = F[0], k = F[1];
      return [R, T, k];
    };
  }
  function u(p, h, v) {
    var y = v.unitless, m = v.injectStyle, _ = m === void 0 ? !0 : m, E = v.prefixToken, w = v.ignore, S = function(b) {
      var x = b.rootCls, P = b.cssVar, A = P === void 0 ? {} : P, $ = n(), T = $.realToken;
      return Fn({
        path: [p],
        prefix: A.prefix,
        key: A.key,
        unitless: y,
        ignore: w,
        token: T,
        scope: x
      }, function() {
        var I = Sr(p, T, h), F = br(p, T, I, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(I).forEach(function(R) {
          F[E(R)] = F[R], delete F[R];
        }), F;
      }), null;
    }, C = function(b) {
      var x = n(), P = x.cssVar;
      return [function(A) {
        return _ && P ? /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(S, {
          rootCls: b,
          cssVar: P,
          component: p
        }), A) : A;
      }, P == null ? void 0 : P.key];
    };
    return C;
  }
  function d(p, h, v) {
    var y = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(p) ? p : [p, p], _ = Q(m, 1), E = _[0], w = m.join("-"), S = e.layer || {
      name: "antd"
    };
    return function(C) {
      var g = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, b = n(), x = b.theme, P = b.realToken, A = b.hashId, $ = b.token, T = b.cssVar, I = o(), F = I.rootPrefixCls, R = I.iconPrefixCls, k = r(), ee = T ? "css" : "js", Y = Li(function() {
        var X = /* @__PURE__ */ new Set();
        return T && Object.keys(y.unitless || {}).forEach(function(ce) {
          X.add(ht(ce, T.prefix)), X.add(ht(ce, vr(E, T.prefix)));
        }), Si(ee, X);
      }, [ee, E, T == null ? void 0 : T.prefix]), le = Ei(ee), B = le.max, N = le.min, H = {
        theme: x,
        token: $,
        hashId: A,
        nonce: function() {
          return k.nonce;
        },
        clientOnly: y.clientOnly,
        layer: S,
        // antd is always at top of styles
        order: y.order || -999
      };
      typeof i == "function" && Wt(L(L({}, H), {}, {
        clientOnly: !1,
        path: ["Shared", F]
      }), function() {
        return i($, {
          prefix: {
            rootPrefixCls: F,
            iconPrefixCls: R
          },
          csp: k
        });
      });
      var K = Wt(L(L({}, H), {}, {
        path: [w, C, R]
      }), function() {
        if (y.injectStyle === !1)
          return [];
        var X = xi($), ce = X.token, ge = X.flush, z = Sr(E, P, v), U = ".".concat(C), q = br(E, P, z, {
          deprecatedTokens: y.deprecatedTokens
        });
        T && z && G(z) === "object" && Object.keys(z).forEach(function(ve) {
          z[ve] = "var(".concat(ht(ve, vr(E, T.prefix)), ")");
        });
        var ue = Ut(ce, {
          componentCls: U,
          prefixCls: C,
          iconCls: ".".concat(R),
          antCls: ".".concat(F),
          calc: Y,
          // @ts-ignore
          max: B,
          // @ts-ignore
          min: N
        }, T ? z : q), V = h(ue, {
          hashId: A,
          prefixCls: C,
          rootPrefixCls: F,
          iconPrefixCls: R
        });
        ge(E, q);
        var se = typeof s == "function" ? s(ue, C, g, y.resetFont) : null;
        return [y.resetStyle === !1 ? null : se, V];
      });
      return [K, A];
    };
  }
  function f(p, h, v) {
    var y = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = d(p, h, v, L({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, y)), _ = function(w) {
      var S = w.prefixCls, C = w.rootCls, g = C === void 0 ? S : C;
      return m(S, g), null;
    };
    return _;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: f,
    genComponentStyleHook: d
  };
}
function Oe(e) {
  "@babel/helpers - typeof";
  return Oe = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Oe(e);
}
function Ii(e, t) {
  if (Oe(e) != "object" || !e) return e;
  var r = e[Symbol.toPrimitive];
  if (r !== void 0) {
    var n = r.call(e, t);
    if (Oe(n) != "object") return n;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Pi(e) {
  var t = Ii(e, "string");
  return Oe(t) == "symbol" ? t : t + "";
}
function re(e, t, r) {
  return (t = Pi(t)) in e ? Object.defineProperty(e, t, {
    value: r,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = r, e;
}
const W = Math.round;
function xt(e, t) {
  const r = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], n = r.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    n[o] = t(n[o] || 0, r[o] || "", o);
  return r[3] ? n[3] = r[3].includes("%") ? n[3] / 100 : n[3] : n[3] = 1, n;
}
const xr = (e, t, r) => r === 0 ? e : e / 100;
function Re(e, t) {
  const r = t || 255;
  return e > r ? r : e < 0 ? 0 : e;
}
class pe {
  constructor(t) {
    re(this, "isValid", !0), re(this, "r", 0), re(this, "g", 0), re(this, "b", 0), re(this, "a", 1), re(this, "_h", void 0), re(this, "_s", void 0), re(this, "_l", void 0), re(this, "_v", void 0), re(this, "_max", void 0), re(this, "_min", void 0), re(this, "_brightness", void 0);
    function r(n) {
      return n[0] in t && n[1] in t && n[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(i) {
        return n.startsWith(i);
      };
      const n = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(n) ? this.fromHexString(n) : o("rgb") ? this.fromRgbString(n) : o("hsl") ? this.fromHslString(n) : (o("hsv") || o("hsb")) && this.fromHsvString(n);
    } else if (t instanceof pe)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (r("rgb"))
      this.r = Re(t.r), this.g = Re(t.g), this.b = Re(t.b), this.a = typeof t.a == "number" ? Re(t.a, 1) : 1;
    else if (r("hsl"))
      this.fromHsl(t);
    else if (r("hsv"))
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
    const r = this.toHsv();
    return r.h = t, this._c(r);
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
    const r = t(this.r), n = t(this.g), o = t(this.b);
    return 0.2126 * r + 0.7152 * n + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = W(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const r = this.getHue(), n = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: r,
      s: n,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const r = this.getHue(), n = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: r,
      s: n,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, r = 50) {
    const n = this._c(t), o = r / 100, i = (a) => (n[a] - this[a]) * o + this[a], s = {
      r: W(i("r")),
      g: W(i("g")),
      b: W(i("b")),
      a: W(i("a") * 100) / 100
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
    const r = this._c(t), n = this.a + r.a * (1 - this.a), o = (i) => W((this[i] * this.a + r[i] * r.a * (1 - this.a)) / n);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: n
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
    const r = (this.r || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const n = (this.g || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = W(this.a * 255).toString(16);
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
    const t = this.getHue(), r = W(this.getSaturation() * 100), n = W(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${r}%,${n}%,${this.a})` : `hsl(${t},${r}%,${n}%)`;
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
  _sc(t, r, n) {
    const o = this.clone();
    return o[t] = Re(r, n), o;
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
    const r = t.replace("#", "");
    function n(o, i) {
      return parseInt(r[o] + r[i || o], 16);
    }
    r.length < 6 ? (this.r = n(0), this.g = n(1), this.b = n(2), this.a = r[3] ? n(3) / 255 : 1) : (this.r = n(0, 1), this.g = n(2, 3), this.b = n(4, 5), this.a = r[6] ? n(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: r,
    l: n,
    a: o
  }) {
    if (this._h = t % 360, this._s = r, this._l = n, this.a = typeof o == "number" ? o : 1, r <= 0) {
      const p = W(n * 255);
      this.r = p, this.g = p, this.b = p;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, u = (1 - Math.abs(2 * n - 1)) * r, d = u * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = u, s = d) : c >= 1 && c < 2 ? (i = d, s = u) : c >= 2 && c < 3 ? (s = u, a = d) : c >= 3 && c < 4 ? (s = d, a = u) : c >= 4 && c < 5 ? (i = d, a = u) : c >= 5 && c < 6 && (i = u, a = d);
    const f = n - u / 2;
    this.r = W((i + f) * 255), this.g = W((s + f) * 255), this.b = W((a + f) * 255);
  }
  fromHsv({
    h: t,
    s: r,
    v: n,
    a: o
  }) {
    this._h = t % 360, this._s = r, this._v = n, this.a = typeof o == "number" ? o : 1;
    const i = W(n * 255);
    if (this.r = i, this.g = i, this.b = i, r <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, u = W(n * (1 - r) * 255), d = W(n * (1 - r * c) * 255), f = W(n * (1 - r * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = u;
        break;
      case 1:
        this.r = d, this.b = u;
        break;
      case 2:
        this.r = u, this.b = f;
        break;
      case 3:
        this.r = u, this.g = d;
        break;
      case 4:
        this.r = f, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = d;
        break;
    }
  }
  fromHsvString(t) {
    const r = xt(t, xr);
    this.fromHsv({
      h: r[0],
      s: r[1],
      v: r[2],
      a: r[3]
    });
  }
  fromHslString(t) {
    const r = xt(t, xr);
    this.fromHsl({
      h: r[0],
      s: r[1],
      l: r[2],
      a: r[3]
    });
  }
  fromRgbString(t) {
    const r = xt(t, (n, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? W(n / 100 * 255) : n
    ));
    this.r = r[0], this.g = r[1], this.b = r[2], this.a = r[3];
  }
}
const Mi = {
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
}, Oi = Object.assign(Object.assign({}, Mi), {
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
function Et(e) {
  return e >= 0 && e <= 255;
}
function ze(e, t) {
  const {
    r,
    g: n,
    b: o,
    a: i
  } = new pe(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new pe(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const d = Math.round((r - s * (1 - u)) / u), f = Math.round((n - a * (1 - u)) / u), p = Math.round((o - c * (1 - u)) / u);
    if (Et(d) && Et(f) && Et(p))
      return new pe({
        r: d,
        g: f,
        b: p,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new pe({
    r,
    g: n,
    b: o,
    a: 1
  }).toRgbString();
}
var Fi = function(e, t) {
  var r = {};
  for (var n in e) Object.prototype.hasOwnProperty.call(e, n) && t.indexOf(n) < 0 && (r[n] = e[n]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, n = Object.getOwnPropertySymbols(e); o < n.length; o++)
    t.indexOf(n[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, n[o]) && (r[n[o]] = e[n[o]]);
  return r;
};
function Ai(e) {
  const {
    override: t
  } = e, r = Fi(e, ["override"]), n = Object.assign({}, t);
  Object.keys(Oi).forEach((p) => {
    delete n[p];
  });
  const o = Object.assign(Object.assign({}, r), n), i = 480, s = 576, a = 768, c = 992, u = 1200, d = 1600;
  if (o.motion === !1) {
    const p = "0s";
    o.motionDurationFast = p, o.motionDurationMid = p, o.motionDurationSlow = p;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: ze(o.colorBorderSecondary, o.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: o.colorTextQuaternary,
    colorTextDisabled: o.colorTextQuaternary,
    colorTextHeading: o.colorText,
    colorTextLabel: o.colorTextSecondary,
    colorTextDescription: o.colorTextTertiary,
    colorTextLightSolid: o.colorWhite,
    colorHighlight: o.colorError,
    colorBgTextHover: o.colorFillSecondary,
    colorBgTextActive: o.colorFill,
    colorIcon: o.colorTextTertiary,
    colorIconHover: o.colorText,
    colorErrorOutline: ze(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: ze(o.colorWarningBg, o.colorBgContainer),
    // Font
    fontSizeIcon: o.fontSizeSM,
    // Line
    lineWidthFocus: o.lineWidth * 3,
    // Control
    lineWidth: o.lineWidth,
    controlOutlineWidth: o.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: o.controlHeight / 2,
    controlItemBgHover: o.colorFillTertiary,
    controlItemBgActive: o.colorPrimaryBg,
    controlItemBgActiveHover: o.colorPrimaryBgHover,
    controlItemBgActiveDisabled: o.colorFill,
    controlTmpOutline: o.colorFillQuaternary,
    controlOutline: ze(o.colorPrimaryBg, o.colorBgContainer),
    lineType: o.lineType,
    borderRadius: o.borderRadius,
    borderRadiusXS: o.borderRadiusXS,
    borderRadiusSM: o.borderRadiusSM,
    borderRadiusLG: o.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: o.sizeXXS,
    paddingXS: o.sizeXS,
    paddingSM: o.sizeSM,
    padding: o.size,
    paddingMD: o.sizeMD,
    paddingLG: o.sizeLG,
    paddingXL: o.sizeXL,
    paddingContentHorizontalLG: o.sizeLG,
    paddingContentVerticalLG: o.sizeMS,
    paddingContentHorizontal: o.sizeMS,
    paddingContentVertical: o.sizeSM,
    paddingContentHorizontalSM: o.size,
    paddingContentVerticalSM: o.sizeXS,
    marginXXS: o.sizeXXS,
    marginXS: o.sizeXS,
    marginSM: o.sizeSM,
    margin: o.size,
    marginMD: o.sizeMD,
    marginLG: o.sizeLG,
    marginXL: o.sizeXL,
    marginXXL: o.sizeXXL,
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
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: d - 1,
    screenXXL: d,
    screenXXLMin: d,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new pe("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new pe("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new pe("rgba(0, 0, 0, 0.09)").toRgbString()}
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
  }), n);
}
const $i = {
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
}, ki = {
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
}, ji = An(We.defaultAlgorithm), Di = {
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
}, rn = (e, t, r) => {
  const n = r.getDerivativeToken(e), {
    override: o,
    ...i
  } = t;
  let s = {
    ...n,
    override: o
  };
  return s = Ai(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: u,
      ...d
    } = c;
    let f = d;
    u && (f = rn({
      ...s,
      ...d
    }, {
      override: d
    }, u)), s[a] = f;
  }), s;
};
function Ni() {
  const {
    token: e,
    hashed: t,
    theme: r = ji,
    override: n,
    cssVar: o
  } = l.useContext(We._internalContext), [i, s, a] = $n(r, [We.defaultSeed, e], {
    salt: `${Co}-${t || ""}`,
    override: n,
    getComputedToken: rn,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: $i,
      ignore: ki,
      preserve: Di
    }
  });
  return [r, a, t ? s : "", i, o];
}
const {
  genStyleHooks: zi
} = Ri({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Ge();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, r, n, o] = Ni();
    return {
      theme: e,
      realToken: t,
      hashId: r,
      token: n,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Ge();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Hi = (e) => {
  const {
    componentCls: t,
    calc: r
  } = e, n = `${t}-list-card`, o = r(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [n]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${n}-name,${n}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${n}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${n}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: r(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: r(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${n}-icon`]: {
          fontSize: r(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: r(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${n}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${n}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: o,
        height: o,
        lineHeight: 1,
        [`&:not(${n}-status-error)`]: {
          border: 0
        },
        // Img
        img: {
          width: "100%",
          height: "100%",
          verticalAlign: "top",
          objectFit: "cover",
          borderRadius: "inherit"
        },
        // Mask
        [`${n}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${n}-status-error`]: {
          [`img, ${n}-img-mask`]: {
            borderRadius: r(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${n}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${n}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${n}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: e.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: e.fontSize,
        cursor: "pointer",
        opacity: e.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: e.opacityLoading
        }
      },
      [`&:hover ${n}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${n}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((i) => `${i} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: r(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, At = {
  "&, *": {
    boxSizing: "border-box"
  }
}, Ui = (e) => {
  const {
    componentCls: t,
    calc: r,
    antCls: n
  } = e, o = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...At,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${i}-inner`]: {
          display: "none"
        }
      },
      [i]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [i]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...At,
        [`${n}-upload-wrapper ${n}-upload${n}-upload-btn`]: {
          padding: 0
        },
        [`&${i}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${i}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${i}-inner`]: {
          gap: r(e.paddingXXS).div(2).equal()
        },
        [`${i}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${i}-title${i}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${i}-description`]: {}
      }
    }
  };
}, Bi = (e) => {
  const {
    componentCls: t,
    calc: r
  } = e, n = `${t}-list`, o = r(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...At,
      // =============================== File List ===============================
      [n]: {
        display: "flex",
        flexWrap: "wrap",
        gap: e.paddingSM,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        color: e.colorText,
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        width: "100%",
        background: e.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${e.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: r(o).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: o,
          height: o,
          fontSize: e.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: e.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&:dir(ltr)": {
          [`&${n}-overflow-ping-start ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-end ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${n}-overflow-ping-end ${n}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${n}-overflow-ping-start ${n}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, Xi = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new pe(t).setA(0.85).toRgbString()
  };
}, nn = zi("Attachments", (e) => {
  const t = Ut(e, {});
  return [Ui(t), Bi(t), Hi(t)];
}, Xi), Vi = (e) => e.indexOf("image/") === 0, He = 200;
function Wi(e) {
  return new Promise((t) => {
    if (!e || !e.type || !Vi(e.type)) {
      t("");
      return;
    }
    const r = new Image();
    if (r.onload = () => {
      const {
        width: n,
        height: o
      } = r, i = n / o, s = i > 1 ? He : He * i, a = i > 1 ? He / i : He, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(r, 0, 0, s, a);
      const d = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(r.src), t(d);
    }, r.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && typeof n.result == "string" && (r.src = n.result);
      }, n.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const n = new FileReader();
      n.onload = () => {
        n.result && t(n.result);
      }, n.readAsDataURL(e);
    } else
      r.src = window.URL.createObjectURL(e);
  });
}
function Gi() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "audio"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function Ki(e) {
  const {
    percent: t
  } = e, {
    token: r
  } = We.useToken();
  return /* @__PURE__ */ l.createElement(yn, {
    type: "circle",
    percent: t,
    size: r.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (n) => /* @__PURE__ */ l.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (n || 0).toFixed(0), "%")
  });
}
function qi() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "video"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const Ct = " ", $t = "#8c8c8c", on = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], Zi = [{
  icon: /* @__PURE__ */ l.createElement(En, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ l.createElement(Cn, null),
  color: $t,
  ext: on
}, {
  icon: /* @__PURE__ */ l.createElement(_n, null),
  color: $t,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Ln, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ l.createElement(Tn, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Rn, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ l.createElement(In, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ l.createElement(qi, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ l.createElement(Gi, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Er(e, t) {
  return t.some((r) => e.toLowerCase() === `.${r}`);
}
function Qi(e) {
  let t = e;
  const r = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let n = 0;
  for (; t >= 1024 && n < r.length - 1; )
    t /= 1024, n++;
  return `${t.toFixed(0)} ${r[n]}`;
}
function Yi(e, t) {
  const {
    prefixCls: r,
    item: n,
    onRemove: o,
    className: i,
    style: s
  } = e, a = l.useContext(Fe), {
    disabled: c
  } = a || {}, {
    name: u,
    size: d,
    percent: f,
    status: p = "done",
    description: h
  } = n, {
    getPrefixCls: v
  } = Ge(), y = v("attachment", r), m = `${y}-list-card`, [_, E, w] = nn(y), [S, C] = l.useMemo(() => {
    const R = u || "", k = R.match(/^(.*)\.[^.]+$/);
    return k ? [k[1], R.slice(k[1].length)] : [R, ""];
  }, [u]), g = l.useMemo(() => Er(C, on), [C]), b = l.useMemo(() => h || (p === "uploading" ? `${f || 0}%` : p === "error" ? n.response || Ct : d ? Qi(d) : Ct), [p, f]), [x, P] = l.useMemo(() => {
    for (const {
      ext: R,
      icon: k,
      color: ee
    } of Zi)
      if (Er(C, R))
        return [k, ee];
    return [/* @__PURE__ */ l.createElement(wn, {
      key: "defaultIcon"
    }), $t];
  }, [C]), [A, $] = l.useState();
  l.useEffect(() => {
    if (n.originFileObj) {
      let R = !0;
      return Wi(n.originFileObj).then((k) => {
        R && $(k);
      }), () => {
        R = !1;
      };
    }
    $(void 0);
  }, [n.originFileObj]);
  let T = null;
  const I = n.thumbUrl || n.url || A, F = g && (n.originFileObj || I);
  return F ? T = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement("img", {
    alt: "preview",
    src: I
  }), p !== "done" && /* @__PURE__ */ l.createElement("div", {
    className: `${m}-img-mask`
  }, p === "uploading" && f !== void 0 && /* @__PURE__ */ l.createElement(Ki, {
    percent: f,
    prefixCls: m
  }), p === "error" && /* @__PURE__ */ l.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, b)))) : T = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-icon`,
    style: {
      color: P
    }
  }, x), /* @__PURE__ */ l.createElement("div", {
    className: `${m}-content`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-name`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, S ?? Ct), /* @__PURE__ */ l.createElement("div", {
    className: `${m}-ellipsis-suffix`
  }, C)), /* @__PURE__ */ l.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, b)))), _(/* @__PURE__ */ l.createElement("div", {
    className: ne(m, {
      [`${m}-status-${p}`]: p,
      [`${m}-type-preview`]: F,
      [`${m}-type-overview`]: !F
    }, i, E, w),
    style: s,
    ref: t
  }, T, !c && o && /* @__PURE__ */ l.createElement("button", {
    type: "button",
    className: `${m}-remove`,
    onClick: () => {
      o(n);
    }
  }, /* @__PURE__ */ l.createElement(xn, null))));
}
const sn = /* @__PURE__ */ l.forwardRef(Yi), Cr = 1;
function Ji(e) {
  const {
    prefixCls: t,
    items: r,
    onRemove: n,
    overflow: o,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: u
  } = e, d = `${t}-list`, f = l.useRef(null), [p, h] = l.useState(!1), {
    disabled: v
  } = l.useContext(Fe);
  l.useEffect(() => (h(!0), () => {
    h(!1);
  }), []);
  const [y, m] = l.useState(!1), [_, E] = l.useState(!1), w = () => {
    const b = f.current;
    b && (o === "scrollX" ? (m(Math.abs(b.scrollLeft) >= Cr), E(b.scrollWidth - b.clientWidth - Math.abs(b.scrollLeft) >= Cr)) : o === "scrollY" && (m(b.scrollTop !== 0), E(b.scrollHeight - b.clientHeight !== b.scrollTop)));
  };
  l.useEffect(() => {
    w();
  }, [o]);
  const S = (b) => {
    const x = f.current;
    x && x.scrollTo({
      left: x.scrollLeft + b * x.clientWidth,
      behavior: "smooth"
    });
  }, C = () => {
    S(-1);
  }, g = () => {
    S(1);
  };
  return /* @__PURE__ */ l.createElement("div", {
    className: ne(d, {
      [`${d}-overflow-${e.overflow}`]: o,
      [`${d}-overflow-ping-start`]: y,
      [`${d}-overflow-ping-end`]: _
    }, s),
    ref: f,
    onScroll: w,
    style: a
  }, /* @__PURE__ */ l.createElement(hi, {
    keys: r.map((b) => ({
      key: b.uid,
      item: b
    })),
    motionName: `${d}-card-motion`,
    component: !1,
    motionAppear: p,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: b,
    item: x,
    className: P,
    style: A
  }) => /* @__PURE__ */ l.createElement(sn, {
    key: b,
    prefixCls: t,
    item: x,
    onRemove: n,
    className: ne(P, c),
    style: {
      ...A,
      ...u
    }
  })), !v && /* @__PURE__ */ l.createElement(Yr, {
    upload: i
  }, /* @__PURE__ */ l.createElement(pt, {
    className: `${d}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ l.createElement(Pn, {
    className: `${d}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(pt, {
    size: "small",
    shape: "circle",
    className: `${d}-prev-btn`,
    icon: /* @__PURE__ */ l.createElement(Mn, null),
    onClick: C
  }), /* @__PURE__ */ l.createElement(pt, {
    size: "small",
    shape: "circle",
    className: `${d}-next-btn`,
    icon: /* @__PURE__ */ l.createElement(On, null),
    onClick: g
  })));
}
function es(e, t) {
  const {
    prefixCls: r,
    placeholder: n = {},
    upload: o,
    className: i,
    style: s
  } = e, a = `${r}-placeholder`, c = n || {}, {
    disabled: u
  } = l.useContext(Fe), [d, f] = l.useState(!1), p = () => {
    f(!0);
  }, h = (m) => {
    m.currentTarget.contains(m.relatedTarget) || f(!1);
  }, v = () => {
    f(!1);
  }, y = /* @__PURE__ */ l.isValidElement(n) ? n : /* @__PURE__ */ l.createElement(Sn, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ l.createElement(mt.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ l.createElement(mt.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ l.createElement(mt.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ l.createElement("div", {
    className: ne(a, {
      [`${a}-drag-in`]: d,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: p,
    onDragLeave: h,
    onDrop: v,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ l.createElement(Rr.Dragger, Pe({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), y));
}
const ts = /* @__PURE__ */ l.forwardRef(es);
function rs(e, t) {
  const {
    prefixCls: r,
    rootClassName: n,
    rootStyle: o,
    className: i,
    style: s,
    items: a,
    children: c,
    getDropContainer: u,
    placeholder: d,
    onChange: f,
    overflow: p,
    disabled: h,
    classNames: v = {},
    styles: y = {},
    ...m
  } = e, {
    getPrefixCls: _,
    direction: E
  } = Ge(), w = _("attachment", r), S = To("attachments"), {
    classNames: C,
    styles: g
  } = S, b = l.useRef(null), x = l.useRef(null);
  l.useImperativeHandle(t, () => ({
    nativeElement: b.current,
    upload: (B) => {
      var H, K;
      const N = (K = (H = x.current) == null ? void 0 : H.nativeElement) == null ? void 0 : K.querySelector('input[type="file"]');
      if (N) {
        const X = new DataTransfer();
        X.items.add(B), N.files = X.files, N.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [P, A, $] = nn(w), T = ne(A, $), [I, F] = Fo([], {
    value: a
  }), R = Ee((B) => {
    F(B.fileList), f == null || f(B);
  }), k = {
    ...m,
    fileList: I,
    onChange: R
  }, ee = (B) => {
    const N = I.filter((H) => H.uid !== B.uid);
    R({
      file: B,
      fileList: N
    });
  };
  let Y;
  const le = (B, N, H) => {
    const K = typeof d == "function" ? d(B) : d;
    return /* @__PURE__ */ l.createElement(ts, {
      placeholder: K,
      upload: k,
      prefixCls: w,
      className: ne(C.placeholder, v.placeholder),
      style: {
        ...g.placeholder,
        ...y.placeholder,
        ...N == null ? void 0 : N.style
      },
      ref: H
    });
  };
  if (c)
    Y = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(Yr, {
      upload: k,
      rootClassName: n,
      ref: x
    }, c), /* @__PURE__ */ l.createElement(ar, {
      getDropContainer: u,
      prefixCls: w,
      className: ne(T, n)
    }, le("drop")));
  else {
    const B = I.length > 0;
    Y = /* @__PURE__ */ l.createElement("div", {
      className: ne(w, T, {
        [`${w}-rtl`]: E === "rtl"
      }, i, n),
      style: {
        ...o,
        ...s
      },
      dir: E || "ltr",
      ref: b
    }, /* @__PURE__ */ l.createElement(Ji, {
      prefixCls: w,
      items: I,
      onRemove: ee,
      overflow: p,
      upload: k,
      listClassName: ne(C.list, v.list),
      listStyle: {
        ...g.list,
        ...y.list,
        ...!B && {
          display: "none"
        }
      },
      itemClassName: ne(C.item, v.item),
      itemStyle: {
        ...g.item,
        ...y.item
      }
    }), le("inline", B ? {
      style: {
        display: "none"
      }
    } : {}, x), /* @__PURE__ */ l.createElement(ar, {
      getDropContainer: u || (() => b.current),
      prefixCls: w,
      className: T
    }, le("drop")));
  }
  return P(/* @__PURE__ */ l.createElement(Fe.Provider, {
    value: {
      disabled: h
    }
  }, Y));
}
const an = /* @__PURE__ */ l.forwardRef(rs);
an.FileCard = sn;
function ns(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function os(e, t = !1) {
  try {
    if (hn(e))
      return e;
    if (t && !ns(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function te(e, t) {
  return qe(() => os(e, t), [e, t]);
}
function is(e, t) {
  const r = qe(() => l.Children.toArray(e.originalChildren || e).filter((i) => i.props.node && !i.props.node.ignore && (!i.props.nodeSlotKey || t)).sort((i, s) => {
    if (i.props.node.slotIndex && s.props.node.slotIndex) {
      const a = Ie(i.props.node.slotIndex) || 0, c = Ie(s.props.node.slotIndex) || 0;
      return a - c === 0 && i.props.node.subSlotIndex && s.props.node.subSlotIndex ? (Ie(i.props.node.subSlotIndex) || 0) - (Ie(s.props.node.subSlotIndex) || 0) : a - c;
    }
    return 0;
  }).map((i) => i.props.node.target), [e, t]);
  return Eo(r);
}
const ss = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function as(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const n = e[r];
    return t[r] = ls(r, n), t;
  }, {}) : {};
}
function ls(e, t) {
  return typeof t == "number" && !ss.includes(e) ? t + "px" : t;
}
function kt(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const o = l.Children.toArray(e._reactElement.props.children).map((i) => {
      if (l.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = kt(i.props.el);
        return l.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...l.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(Ve(l.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const n = Array.from(e.childNodes);
  for (let o = 0; o < n.length; o++) {
    const i = n[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = kt(i);
      t.push(...a), r.appendChild(s);
    } else i.nodeType === 3 && r.appendChild(i.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function cs(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const _r = un(({
  slot: e,
  clone: t,
  className: r,
  style: n,
  observeAttributes: o
}, i) => {
  const s = me(), [a, c] = jt([]), {
    forceClone: u
  } = gn(), d = u ? !0 : t;
  return be(() => {
    var y;
    if (!s.current || !e)
      return;
    let f = e;
    function p() {
      let m = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (m = f.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), cs(i, m), r && m.classList.add(...r.split(" ")), n) {
        const _ = as(n);
        Object.keys(_).forEach((E) => {
          m.style[E] = _[E];
        });
      }
    }
    let h = null, v = null;
    if (d && window.MutationObserver) {
      let m = function() {
        var S, C, g;
        (S = s.current) != null && S.contains(f) && ((C = s.current) == null || C.removeChild(f));
        const {
          portals: E,
          clonedElement: w
        } = kt(e);
        f = w, c(E), f.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          p();
        }, 50), (g = s.current) == null || g.appendChild(f);
      };
      m();
      const _ = Kn(() => {
        m(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0
          // attributes: observeAttributes ?? (forceClone ? true : false),
        });
      }, 50);
      h = new window.MutationObserver(_), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", p(), (y = s.current) == null || y.appendChild(f);
    return () => {
      var m, _;
      f.style.display = "", (m = s.current) != null && m.contains(f) && ((_ = s.current) == null || _.removeChild(f)), h == null || h.disconnect();
    };
  }, [e, d, r, n, i, o, u]), l.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), us = ({
  children: e,
  ...t
}) => /* @__PURE__ */ oe.jsx(oe.Fragment, {
  children: e(t)
});
function fs(e) {
  return l.createElement(us, {
    children: e
  });
}
function Lr(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? fs((r) => /* @__PURE__ */ oe.jsx(vn, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ oe.jsx(_r, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ oe.jsx(_r, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function de({
  key: e,
  slots: t,
  targets: r
}, n) {
  return t[e] ? (...o) => r ? r.map((i, s) => /* @__PURE__ */ oe.jsx(l.Fragment, {
    children: Lr(i, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ oe.jsx(oe.Fragment, {
    children: Lr(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const ds = (e) => !!e.name;
function Tr(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const hs = wo(({
  slots: e,
  upload: t,
  showUploadList: r,
  progress: n,
  beforeUpload: o,
  customRequest: i,
  previewFile: s,
  isImageUrl: a,
  itemRender: c,
  iconRender: u,
  data: d,
  onChange: f,
  onValueChange: p,
  onRemove: h,
  items: v,
  setSlotParams: y,
  placeholder: m,
  getDropContainer: _,
  children: E,
  maxCount: w,
  ...S
}) => {
  const C = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", g = Tr(r), b = e["placeholder.title"] || e["placeholder.description"] || e["placeholder.icon"] || typeof m == "object", x = Tr(m), P = te(g.showPreviewIcon), A = te(g.showRemoveIcon), $ = te(g.showDownloadIcon), T = te(o), I = te(i), F = te(n == null ? void 0 : n.format), R = te(s), k = te(a), ee = te(c), Y = te(u), le = te(m, !0), B = te(_), N = te(d), H = me(!1), [K, X] = jt(v);
  be(() => {
    X(v);
  }, [v]);
  const ce = qe(() => {
    const z = {};
    return K.map((U) => {
      if (!ds(U)) {
        const q = U.uid || U.url || U.path;
        return z[q] || (z[q] = 0), z[q]++, {
          ...U,
          name: U.orig_name || U.path,
          uid: U.uid || q + "-" + z[q],
          status: "done"
        };
      }
      return U;
    }) || [];
  }, [K]), ge = is(E);
  return /* @__PURE__ */ oe.jsxs(oe.Fragment, {
    children: [/* @__PURE__ */ oe.jsx("div", {
      style: {
        display: "none"
      },
      children: ge.length > 0 ? null : E
    }), /* @__PURE__ */ oe.jsx(an, {
      ...S,
      getDropContainer: B,
      placeholder: e.placeholder ? de({
        slots: e,
        key: "placeholder"
      }) : b ? (...z) => {
        var U, q, ue;
        return {
          ...x,
          icon: e["placeholder.icon"] ? (U = de({
            slots: e,
            key: "placeholder.icon"
          })) == null ? void 0 : U(...z) : x.icon,
          title: e["placeholder.title"] ? (q = de({
            slots: e,
            key: "placeholder.title"
          })) == null ? void 0 : q(...z) : x.title,
          description: e["placeholder.description"] ? (ue = de({
            slots: e,
            key: "placeholder.description"
          })) == null ? void 0 : ue(...z) : x.description
        };
      } : le || m,
      items: ce,
      data: N || d,
      previewFile: R,
      isImageUrl: k,
      itemRender: e.itemRender ? de({
        slots: e,
        key: "itemRender"
      }) : ee,
      iconRender: e.iconRender ? de({
        slots: e,
        key: "iconRender"
      }) : Y,
      maxCount: w,
      onChange: async (z) => {
        const U = z.file, q = z.fileList, ue = ce.findIndex((V) => V.uid === U.uid);
        if (ue !== -1) {
          if (H.current)
            return;
          h == null || h(U);
          const V = K.slice();
          V.splice(ue, 1), p == null || p(V), f == null || f(V.map((se) => se.path));
        } else {
          if (T && !await T(U, q) || H.current)
            return;
          H.current = !0;
          let V = q.filter((j) => j.status !== "done");
          if (w === 1)
            V = V.slice(0, 1);
          else if (V.length === 0) {
            H.current = !1;
            return;
          } else if (typeof w == "number") {
            const j = w - K.length;
            V = V.slice(0, j < 0 ? 0 : j);
          }
          const se = K, ve = V.map((j) => ({
            ...j,
            size: j.size,
            uid: j.uid,
            name: j.name,
            status: "uploading"
          }));
          X((j) => [...w === 1 ? [] : j, ...ve]);
          const Le = (await t(V.map((j) => j.originFileObj))).filter(Boolean).map((j, ut) => ({
            ...j,
            uid: ve[ut].uid
          })), Te = w === 1 ? Le : [...se, ...Le];
          H.current = !1, X(Te), p == null || p(Te), f == null || f(Te.map((j) => j.path));
        }
      },
      customRequest: I || Xn,
      progress: n && {
        ...n,
        format: F
      },
      showUploadList: C ? {
        ...g,
        showDownloadIcon: $ || g.showDownloadIcon,
        showRemoveIcon: A || g.showRemoveIcon,
        showPreviewIcon: P || g.showPreviewIcon,
        downloadIcon: e["showUploadList.downloadIcon"] ? de({
          slots: e,
          key: "showUploadList.downloadIcon"
        }) : g.downloadIcon,
        removeIcon: e["showUploadList.removeIcon"] ? de({
          slots: e,
          key: "showUploadList.removeIcon"
        }) : g.removeIcon,
        previewIcon: e["showUploadList.previewIcon"] ? de({
          slots: e,
          key: "showUploadList.previewIcon"
        }) : g.previewIcon,
        extra: e["showUploadList.extra"] ? de({
          slots: e,
          key: "showUploadList.extra"
        }) : g.extra
      } : r,
      children: ge.length > 0 ? E : void 0
    })]
  });
});
export {
  hs as Attachments,
  hs as default
};
