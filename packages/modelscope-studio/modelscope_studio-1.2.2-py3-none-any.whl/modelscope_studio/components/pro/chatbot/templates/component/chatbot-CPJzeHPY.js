var In = (e) => {
  throw TypeError(e);
};
var Mn = (e, t, n) => t.has(e) || In("Cannot " + n);
var Ae = (e, t, n) => (Mn(e, t, "read from private field"), n ? n.call(e) : t.get(e)), Ln = (e, t, n) => t.has(e) ? In("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), Nn = (e, t, n, r) => (Mn(e, t, "write to private field"), r ? r.call(e, n) : t.set(e, n), n);
import { i as Io, a as be, r as Mo, b as Lo, w as mt, g as No, c as k, d as xn, e as pt, o as Fn } from "./Index-Ao5Jmr68.js";
const M = window.ms_globals.React, c = window.ms_globals.React, To = window.ms_globals.React.isValidElement, J = window.ms_globals.React.useRef, $o = window.ms_globals.React.useLayoutEffect, we = window.ms_globals.React.useEffect, Po = window.ms_globals.React.useCallback, he = window.ms_globals.React.useMemo, Ro = window.ms_globals.React.forwardRef, Ye = window.ms_globals.React.useState, On = window.ms_globals.ReactDOM, yt = window.ms_globals.ReactDOM.createPortal, Oo = window.ms_globals.antdIcons.FileTextFilled, Fo = window.ms_globals.antdIcons.CloseCircleFilled, jo = window.ms_globals.antdIcons.FileExcelFilled, ko = window.ms_globals.antdIcons.FileImageFilled, Ao = window.ms_globals.antdIcons.FileMarkdownFilled, zo = window.ms_globals.antdIcons.FilePdfFilled, Do = window.ms_globals.antdIcons.FilePptFilled, Ho = window.ms_globals.antdIcons.FileWordFilled, Bo = window.ms_globals.antdIcons.FileZipFilled, Vo = window.ms_globals.antdIcons.PlusOutlined, Wo = window.ms_globals.antdIcons.LeftOutlined, Xo = window.ms_globals.antdIcons.RightOutlined, Uo = window.ms_globals.antdIcons.CloseOutlined, Rr = window.ms_globals.antdIcons.CheckOutlined, Go = window.ms_globals.antdIcons.DeleteOutlined, Ko = window.ms_globals.antdIcons.EditOutlined, qo = window.ms_globals.antdIcons.SyncOutlined, Yo = window.ms_globals.antdIcons.DislikeOutlined, Qo = window.ms_globals.antdIcons.LikeOutlined, Zo = window.ms_globals.antdIcons.CopyOutlined, Jo = window.ms_globals.antdIcons.EyeOutlined, ei = window.ms_globals.antdIcons.ArrowDownOutlined, ti = window.ms_globals.antd.ConfigProvider, Ir = window.ms_globals.antd.Upload, Qe = window.ms_globals.antd.theme, ni = window.ms_globals.antd.Progress, oe = window.ms_globals.antd.Button, _e = window.ms_globals.antd.Flex, Te = window.ms_globals.antd.Typography, ri = window.ms_globals.antd.Avatar, oi = window.ms_globals.antd.Popconfirm, ii = window.ms_globals.antd.Tooltip, si = window.ms_globals.antd.Collapse, ai = window.ms_globals.antd.Input, Mr = window.ms_globals.createItemsContext.createItemsContext, li = window.ms_globals.internalContext.useContextPropsContext, jn = window.ms_globals.internalContext.ContextPropsProvider, Be = window.ms_globals.antdCssinjs.unit, Wt = window.ms_globals.antdCssinjs.token2CSSVar, kn = window.ms_globals.antdCssinjs.useStyleRegister, ci = window.ms_globals.antdCssinjs.useCSSVarRegister, ui = window.ms_globals.antdCssinjs.createTheme, fi = window.ms_globals.antdCssinjs.useCacheToken, Lr = window.ms_globals.antdCssinjs.Keyframes, vt = window.ms_globals.components.Markdown;
var di = /\s/;
function mi(e) {
  for (var t = e.length; t-- && di.test(e.charAt(t)); )
    ;
  return t;
}
var pi = /^\s+/;
function gi(e) {
  return e && e.slice(0, mi(e) + 1).replace(pi, "");
}
var An = NaN, hi = /^[-+]0x[0-9a-f]+$/i, yi = /^0b[01]+$/i, vi = /^0o[0-7]+$/i, bi = parseInt;
function zn(e) {
  if (typeof e == "number")
    return e;
  if (Io(e))
    return An;
  if (be(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = be(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = gi(e);
  var n = yi.test(e);
  return n || vi.test(e) ? bi(e.slice(2), n ? 2 : 8) : hi.test(e) ? An : +e;
}
var Xt = function() {
  return Mo.Date.now();
}, Si = "Expected a function", xi = Math.max, wi = Math.min;
function _i(e, t, n) {
  var r, o, i, s, a, l, u = 0, f = !1, m = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Si);
  t = zn(t) || 0, be(n) && (f = !!n.leading, m = "maxWait" in n, i = m ? xi(zn(n.maxWait) || 0, t) : i, d = "trailing" in n ? !!n.trailing : d);
  function h(b) {
    var w = r, R = o;
    return r = o = void 0, u = b, s = e.apply(R, w), s;
  }
  function y(b) {
    return u = b, a = setTimeout(v, t), f ? h(b) : s;
  }
  function g(b) {
    var w = b - l, R = b - u, L = t - w;
    return m ? wi(L, i - R) : L;
  }
  function p(b) {
    var w = b - l, R = b - u;
    return l === void 0 || w >= t || w < 0 || m && R >= i;
  }
  function v() {
    var b = Xt();
    if (p(b))
      return _(b);
    a = setTimeout(v, g(b));
  }
  function _(b) {
    return a = void 0, d && r ? h(b) : (r = o = void 0, s);
  }
  function T() {
    a !== void 0 && clearTimeout(a), u = 0, r = l = o = a = void 0;
  }
  function $() {
    return a === void 0 ? s : _(Xt());
  }
  function C() {
    var b = Xt(), w = p(b);
    if (r = arguments, o = this, l = b, w) {
      if (a === void 0)
        return y(l);
      if (m)
        return clearTimeout(a), a = setTimeout(v, t), h(l);
    }
    return a === void 0 && (a = setTimeout(v, t)), s;
  }
  return C.cancel = T, C.flush = $, C;
}
function Ci(e, t) {
  return Lo(e, t);
}
var Nr = {
  exports: {}
}, _t = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ei = c, Ti = Symbol.for("react.element"), $i = Symbol.for("react.fragment"), Pi = Object.prototype.hasOwnProperty, Ri = Ei.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ii = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Or(e, t, n) {
  var r, o = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) Pi.call(t, r) && !Ii.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Ti,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: Ri.current
  };
}
_t.Fragment = $i;
_t.jsx = Or;
_t.jsxs = Or;
Nr.exports = _t;
var S = Nr.exports;
const {
  SvelteComponent: Mi,
  assign: Dn,
  binding_callbacks: Hn,
  check_outros: Li,
  children: Fr,
  claim_element: jr,
  claim_space: Ni,
  component_subscribe: Bn,
  compute_slots: Oi,
  create_slot: Fi,
  detach: ze,
  element: kr,
  empty: Vn,
  exclude_internal_props: Wn,
  get_all_dirty_from_scope: ji,
  get_slot_changes: ki,
  group_outros: Ai,
  init: zi,
  insert_hydration: gt,
  safe_not_equal: Di,
  set_custom_element_data: Ar,
  space: Hi,
  transition_in: ht,
  transition_out: nn,
  update_slot_base: Bi
} = window.__gradio__svelte__internal, {
  beforeUpdate: Vi,
  getContext: Wi,
  onDestroy: Xi,
  setContext: Ui
} = window.__gradio__svelte__internal;
function Xn(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), o = Fi(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = kr("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = jr(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Fr(t);
      o && o.l(s), s.forEach(ze), this.h();
    },
    h() {
      Ar(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      gt(i, t, s), o && o.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && Bi(
        o,
        r,
        i,
        /*$$scope*/
        i[6],
        n ? ki(
          r,
          /*$$scope*/
          i[6],
          s,
          null
        ) : ji(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (ht(o, i), n = !0);
    },
    o(i) {
      nn(o, i), n = !1;
    },
    d(i) {
      i && ze(t), o && o.d(i), e[9](null);
    }
  };
}
function Gi(e) {
  let t, n, r, o, i = (
    /*$$slots*/
    e[4].default && Xn(e)
  );
  return {
    c() {
      t = kr("react-portal-target"), n = Hi(), i && i.c(), r = Vn(), this.h();
    },
    l(s) {
      t = jr(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Fr(t).forEach(ze), n = Ni(s), i && i.l(s), r = Vn(), this.h();
    },
    h() {
      Ar(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      gt(s, t, a), e[8](t), gt(s, n, a), i && i.m(s, a), gt(s, r, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && ht(i, 1)) : (i = Xn(s), i.c(), ht(i, 1), i.m(r.parentNode, r)) : i && (Ai(), nn(i, 1, 1, () => {
        i = null;
      }), Li());
    },
    i(s) {
      o || (ht(i), o = !0);
    },
    o(s) {
      nn(i), o = !1;
    },
    d(s) {
      s && (ze(t), ze(n), ze(r)), e[8](null), i && i.d(s);
    }
  };
}
function Un(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Ki(e, t, n) {
  let r, o, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = Oi(i);
  let {
    svelteInit: l
  } = t;
  const u = mt(Un(t)), f = mt();
  Bn(e, f, ($) => n(0, r = $));
  const m = mt();
  Bn(e, m, ($) => n(1, o = $));
  const d = [], h = Wi("$$ms-gr-react-wrapper"), {
    slotKey: y,
    slotIndex: g,
    subSlotIndex: p
  } = No() || {}, v = l({
    parent: h,
    props: u,
    target: f,
    slot: m,
    slotKey: y,
    slotIndex: g,
    subSlotIndex: p,
    onDestroy($) {
      d.push($);
    }
  });
  Ui("$$ms-gr-react-wrapper", v), Vi(() => {
    u.set(Un(t));
  }), Xi(() => {
    d.forEach(($) => $());
  });
  function _($) {
    Hn[$ ? "unshift" : "push"](() => {
      r = $, f.set(r);
    });
  }
  function T($) {
    Hn[$ ? "unshift" : "push"](() => {
      o = $, m.set(o);
    });
  }
  return e.$$set = ($) => {
    n(17, t = Dn(Dn({}, t), Wn($))), "svelteInit" in $ && n(5, l = $.svelteInit), "$$scope" in $ && n(6, s = $.$$scope);
  }, t = Wn(t), [r, o, f, m, a, l, s, i, _, T];
}
class qi extends Mi {
  constructor(t) {
    super(), zi(this, t, Ki, Gi, Di, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: Ql
} = window.__gradio__svelte__internal, Gn = window.ms_globals.rerender, Ut = window.ms_globals.tree;
function Yi(e, t = {}) {
  function n(r) {
    const o = mt(), i = new qi({
      ...r,
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
          }, l = s.parent ?? Ut;
          return l.nodes = [...l.nodes, a], Gn({
            createPortal: yt,
            node: Ut
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((u) => u.svelteInstance !== o), Gn({
              createPortal: yt,
              node: Ut
            });
          }), a;
        },
        ...r.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const Qi = "1.0.5", Zi = /* @__PURE__ */ c.createContext({}), Ji = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Ct = (e) => {
  const t = c.useContext(Zi);
  return c.useMemo(() => ({
    ...Ji,
    ...t[e]
  }), [t[e]]);
};
function Ce() {
  return Ce = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, Ce.apply(null, arguments);
}
function $e() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r,
    theme: o
  } = c.useContext(ti.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r
  };
}
function Pe(e) {
  var t = M.useRef();
  t.current = e;
  var n = M.useCallback(function() {
    for (var r, o = arguments.length, i = new Array(o), s = 0; s < o; s++)
      i[s] = arguments[s];
    return (r = t.current) === null || r === void 0 ? void 0 : r.call.apply(r, [t].concat(i));
  }, []);
  return n;
}
function es(e) {
  if (Array.isArray(e)) return e;
}
function ts(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var r, o, i, s, a = [], l = !0, u = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (r = i.call(n)).done) && (a.push(r.value), a.length !== t); l = !0) ;
    } catch (f) {
      u = !0, o = f;
    } finally {
      try {
        if (!l && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function Kn(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
  return r;
}
function ns(e, t) {
  if (e) {
    if (typeof e == "string") return Kn(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? Kn(e, t) : void 0;
  }
}
function rs() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ne(e, t) {
  return es(e) || ts(e, t) || ns(e, t) || rs();
}
function Et() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var qn = Et() ? M.useLayoutEffect : M.useEffect, zr = function(t, n) {
  var r = M.useRef(!0);
  qn(function() {
    return t(r.current);
  }, n), qn(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, Yn = function(t, n) {
  zr(function(r) {
    if (!r)
      return t();
  }, n);
};
function Ze(e) {
  var t = M.useRef(!1), n = M.useState(e), r = ne(n, 2), o = r[0], i = r[1];
  M.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, l) {
    l && t.current || i(a);
  }
  return [o, s];
}
function Gt(e) {
  return e !== void 0;
}
function os(e, t) {
  var n = t || {}, r = n.defaultValue, o = n.value, i = n.onChange, s = n.postState, a = Ze(function() {
    return Gt(o) ? o : Gt(r) ? typeof r == "function" ? r() : r : typeof e == "function" ? e() : e;
  }), l = ne(a, 2), u = l[0], f = l[1], m = o !== void 0 ? o : u, d = s ? s(m) : m, h = Pe(i), y = Ze([m]), g = ne(y, 2), p = g[0], v = g[1];
  Yn(function() {
    var T = p[0];
    u !== T && h(u, T);
  }, [p]), Yn(function() {
    Gt(o) || f(o);
  }, [o]);
  var _ = Pe(function(T, $) {
    f(T, $), v([m], $);
  });
  return [d, _];
}
function ee(e) {
  "@babel/helpers - typeof";
  return ee = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, ee(e);
}
var Dr = {
  exports: {}
}, D = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var wn = Symbol.for("react.element"), _n = Symbol.for("react.portal"), Tt = Symbol.for("react.fragment"), $t = Symbol.for("react.strict_mode"), Pt = Symbol.for("react.profiler"), Rt = Symbol.for("react.provider"), It = Symbol.for("react.context"), is = Symbol.for("react.server_context"), Mt = Symbol.for("react.forward_ref"), Lt = Symbol.for("react.suspense"), Nt = Symbol.for("react.suspense_list"), Ot = Symbol.for("react.memo"), Ft = Symbol.for("react.lazy"), ss = Symbol.for("react.offscreen"), Hr;
Hr = Symbol.for("react.module.reference");
function ue(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case wn:
        switch (e = e.type, e) {
          case Tt:
          case Pt:
          case $t:
          case Lt:
          case Nt:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case is:
              case It:
              case Mt:
              case Ft:
              case Ot:
              case Rt:
                return e;
              default:
                return t;
            }
        }
      case _n:
        return t;
    }
  }
}
D.ContextConsumer = It;
D.ContextProvider = Rt;
D.Element = wn;
D.ForwardRef = Mt;
D.Fragment = Tt;
D.Lazy = Ft;
D.Memo = Ot;
D.Portal = _n;
D.Profiler = Pt;
D.StrictMode = $t;
D.Suspense = Lt;
D.SuspenseList = Nt;
D.isAsyncMode = function() {
  return !1;
};
D.isConcurrentMode = function() {
  return !1;
};
D.isContextConsumer = function(e) {
  return ue(e) === It;
};
D.isContextProvider = function(e) {
  return ue(e) === Rt;
};
D.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === wn;
};
D.isForwardRef = function(e) {
  return ue(e) === Mt;
};
D.isFragment = function(e) {
  return ue(e) === Tt;
};
D.isLazy = function(e) {
  return ue(e) === Ft;
};
D.isMemo = function(e) {
  return ue(e) === Ot;
};
D.isPortal = function(e) {
  return ue(e) === _n;
};
D.isProfiler = function(e) {
  return ue(e) === Pt;
};
D.isStrictMode = function(e) {
  return ue(e) === $t;
};
D.isSuspense = function(e) {
  return ue(e) === Lt;
};
D.isSuspenseList = function(e) {
  return ue(e) === Nt;
};
D.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Tt || e === Pt || e === $t || e === Lt || e === Nt || e === ss || typeof e == "object" && e !== null && (e.$$typeof === Ft || e.$$typeof === Ot || e.$$typeof === Rt || e.$$typeof === It || e.$$typeof === Mt || e.$$typeof === Hr || e.getModuleId !== void 0);
};
D.typeOf = ue;
Dr.exports = D;
var Kt = Dr.exports, as = Symbol.for("react.element"), ls = Symbol.for("react.transitional.element"), cs = Symbol.for("react.fragment");
function us(e) {
  return (
    // Base object type
    e && ee(e) === "object" && // React Element type
    (e.$$typeof === as || e.$$typeof === ls) && // React Fragment type
    e.type === cs
  );
}
var fs = function(t, n) {
  typeof t == "function" ? t(n) : ee(t) === "object" && t && "current" in t && (t.current = n);
}, ds = function(t) {
  var n, r;
  if (!t)
    return !1;
  if (Br(t) && t.props.propertyIsEnumerable("ref"))
    return !0;
  var o = Kt.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((n = o.prototype) !== null && n !== void 0 && n.render) && o.$$typeof !== Kt.ForwardRef || typeof t == "function" && !((r = t.prototype) !== null && r !== void 0 && r.render) && t.$$typeof !== Kt.ForwardRef);
};
function Br(e) {
  return /* @__PURE__ */ To(e) && !us(e);
}
var ms = function(t) {
  if (t && Br(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function ps(e, t) {
  if (ee(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t);
    if (ee(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Vr(e) {
  var t = ps(e, "string");
  return ee(t) == "symbol" ? t : t + "";
}
function B(e, t, n) {
  return (t = Vr(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function Qn(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e);
    t && (r = r.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), n.push.apply(n, r);
  }
  return n;
}
function j(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? Qn(Object(n), !0).forEach(function(r) {
      B(e, r, n[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : Qn(Object(n)).forEach(function(r) {
      Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r));
    });
  }
  return e;
}
const nt = /* @__PURE__ */ c.createContext(null);
function Zn(e) {
  const {
    getDropContainer: t,
    className: n,
    prefixCls: r,
    children: o
  } = e, {
    disabled: i
  } = c.useContext(nt), [s, a] = c.useState(), [l, u] = c.useState(null);
  if (c.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && a(d);
  }, [t]), c.useEffect(() => {
    if (s) {
      const d = () => {
        u(!0);
      }, h = (p) => {
        p.preventDefault();
      }, y = (p) => {
        p.relatedTarget || u(!1);
      }, g = (p) => {
        u(!1), p.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", h), document.addEventListener("dragleave", y), document.addEventListener("drop", g), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", h), document.removeEventListener("dragleave", y), document.removeEventListener("drop", g);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const m = `${r}-drop-area`;
  return /* @__PURE__ */ yt(/* @__PURE__ */ c.createElement("div", {
    className: k(m, n, {
      [`${m}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: l ? "block" : "none"
    }
  }, o), s);
}
function Jn(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function gs(e) {
  return e && ee(e) === "object" && Jn(e.nativeElement) ? e.nativeElement : Jn(e) ? e : null;
}
function hs(e) {
  var t = gs(e);
  if (t)
    return t;
  if (e instanceof c.Component) {
    var n;
    return (n = On.findDOMNode) === null || n === void 0 ? void 0 : n.call(On, e);
  }
  return null;
}
function ys(e, t) {
  if (e == null) return {};
  var n = {};
  for (var r in e) if ({}.hasOwnProperty.call(e, r)) {
    if (t.includes(r)) continue;
    n[r] = e[r];
  }
  return n;
}
function er(e, t) {
  if (e == null) return {};
  var n, r, o = ys(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (r = 0; r < i.length; r++) n = i[r], t.includes(n) || {}.propertyIsEnumerable.call(e, n) && (o[n] = e[n]);
  }
  return o;
}
var vs = /* @__PURE__ */ M.createContext({});
function Xe(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function tr(e, t) {
  for (var n = 0; n < t.length; n++) {
    var r = t[n];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, Vr(r.key), r);
  }
}
function Ue(e, t, n) {
  return t && tr(e.prototype, t), n && tr(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function rn(e, t) {
  return rn = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, rn(e, t);
}
function jt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && rn(e, t);
}
function bt(e) {
  return bt = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, bt(e);
}
function Wr() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Wr = function() {
    return !!e;
  })();
}
function Ie(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function bs(e, t) {
  if (t && (ee(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Ie(e);
}
function kt(e) {
  var t = Wr();
  return function() {
    var n, r = bt(e);
    if (t) {
      var o = bt(this).constructor;
      n = Reflect.construct(r, arguments, o);
    } else n = r.apply(this, arguments);
    return bs(this, n);
  };
}
var Ss = /* @__PURE__ */ function(e) {
  jt(n, e);
  var t = kt(n);
  function n() {
    return Xe(this, n), t.apply(this, arguments);
  }
  return Ue(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(M.Component);
function xs(e) {
  var t = M.useReducer(function(a) {
    return a + 1;
  }, 0), n = ne(t, 2), r = n[1], o = M.useRef(e), i = Pe(function() {
    return o.current;
  }), s = Pe(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, r();
  });
  return [i, s];
}
var Ee = "none", st = "appear", at = "enter", lt = "leave", nr = "none", me = "prepare", De = "start", He = "active", Cn = "end", Xr = "prepared";
function rr(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function ws(e, t) {
  var n = {
    animationend: rr("Animation", "AnimationEnd"),
    transitionend: rr("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var _s = ws(Et(), typeof window < "u" ? window : {}), Ur = {};
if (Et()) {
  var Cs = document.createElement("div");
  Ur = Cs.style;
}
var ct = {};
function Gr(e) {
  if (ct[e])
    return ct[e];
  var t = _s[e];
  if (t)
    for (var n = Object.keys(t), r = n.length, o = 0; o < r; o += 1) {
      var i = n[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Ur)
        return ct[e] = t[i], ct[e];
    }
  return "";
}
var Kr = Gr("animationend"), qr = Gr("transitionend"), Yr = !!(Kr && qr), or = Kr || "animationend", ir = qr || "transitionend";
function sr(e, t) {
  if (!e) return null;
  if (ee(e) === "object") {
    var n = t.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const Es = function(e) {
  var t = J();
  function n(o) {
    o && (o.removeEventListener(ir, e), o.removeEventListener(or, e));
  }
  function r(o) {
    t.current && t.current !== o && n(t.current), o && o !== t.current && (o.addEventListener(ir, e), o.addEventListener(or, e), t.current = o);
  }
  return M.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [r, n];
};
var Qr = Et() ? $o : we, Zr = function(t) {
  return +setTimeout(t, 16);
}, Jr = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Zr = function(t) {
  return window.requestAnimationFrame(t);
}, Jr = function(t) {
  return window.cancelAnimationFrame(t);
});
var ar = 0, En = /* @__PURE__ */ new Map();
function eo(e) {
  En.delete(e);
}
var on = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  ar += 1;
  var r = ar;
  function o(i) {
    if (i === 0)
      eo(r), t();
    else {
      var s = Zr(function() {
        o(i - 1);
      });
      En.set(r, s);
    }
  }
  return o(n), r;
};
on.cancel = function(e) {
  var t = En.get(e);
  return eo(e), Jr(t);
};
const Ts = function() {
  var e = M.useRef(null);
  function t() {
    on.cancel(e.current);
  }
  function n(r) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = on(function() {
      o <= 1 ? r({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(r, o - 1);
    });
    e.current = i;
  }
  return M.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var $s = [me, De, He, Cn], Ps = [me, Xr], to = !1, Rs = !0;
function no(e) {
  return e === He || e === Cn;
}
const Is = function(e, t, n) {
  var r = Ze(nr), o = ne(r, 2), i = o[0], s = o[1], a = Ts(), l = ne(a, 2), u = l[0], f = l[1];
  function m() {
    s(me, !0);
  }
  var d = t ? Ps : $s;
  return Qr(function() {
    if (i !== nr && i !== Cn) {
      var h = d.indexOf(i), y = d[h + 1], g = n(i);
      g === to ? s(y, !0) : y && u(function(p) {
        function v() {
          p.isCanceled() || s(y, !0);
        }
        g === !0 ? v() : Promise.resolve(g).then(v);
      });
    }
  }, [e, i]), M.useEffect(function() {
    return function() {
      f();
    };
  }, []), [m, i];
};
function Ms(e, t, n, r) {
  var o = r.motionEnter, i = o === void 0 ? !0 : o, s = r.motionAppear, a = s === void 0 ? !0 : s, l = r.motionLeave, u = l === void 0 ? !0 : l, f = r.motionDeadline, m = r.motionLeaveImmediately, d = r.onAppearPrepare, h = r.onEnterPrepare, y = r.onLeavePrepare, g = r.onAppearStart, p = r.onEnterStart, v = r.onLeaveStart, _ = r.onAppearActive, T = r.onEnterActive, $ = r.onLeaveActive, C = r.onAppearEnd, b = r.onEnterEnd, w = r.onLeaveEnd, R = r.onVisibleChanged, L = Ze(), O = ne(L, 2), A = O[0], F = O[1], P = xs(Ee), x = ne(P, 2), I = x[0], N = x[1], V = Ze(null), W = ne(V, 2), Y = W[0], H = W[1], z = I(), K = J(!1), Q = J(null);
  function U() {
    return n();
  }
  var ie = J(!1);
  function Ne() {
    N(Ee), H(null, !0);
  }
  var fe = Pe(function(Z) {
    var te = I();
    if (te !== Ee) {
      var ge = U();
      if (!(Z && !Z.deadline && Z.target !== ge)) {
        var ot = ie.current, it;
        te === st && ot ? it = C == null ? void 0 : C(ge, Z) : te === at && ot ? it = b == null ? void 0 : b(ge, Z) : te === lt && ot && (it = w == null ? void 0 : w(ge, Z)), ot && it !== !1 && Ne();
      }
    }
  }), Ke = Es(fe), Oe = ne(Ke, 1), Fe = Oe[0], je = function(te) {
    switch (te) {
      case st:
        return B(B(B({}, me, d), De, g), He, _);
      case at:
        return B(B(B({}, me, h), De, p), He, T);
      case lt:
        return B(B(B({}, me, y), De, v), He, $);
      default:
        return {};
    }
  }, Se = M.useMemo(function() {
    return je(z);
  }, [z]), ke = Is(z, !e, function(Z) {
    if (Z === me) {
      var te = Se[me];
      return te ? te(U()) : to;
    }
    if (E in Se) {
      var ge;
      H(((ge = Se[E]) === null || ge === void 0 ? void 0 : ge.call(Se, U(), null)) || null);
    }
    return E === He && z !== Ee && (Fe(U()), f > 0 && (clearTimeout(Q.current), Q.current = setTimeout(function() {
      fe({
        deadline: !0
      });
    }, f))), E === Xr && Ne(), Rs;
  }), rt = ne(ke, 2), Vt = rt[0], E = rt[1], G = no(E);
  ie.current = G;
  var X = J(null);
  Qr(function() {
    if (!(K.current && X.current === t)) {
      F(t);
      var Z = K.current;
      K.current = !0;
      var te;
      !Z && t && a && (te = st), Z && t && i && (te = at), (Z && !t && u || !Z && m && !t && u) && (te = lt);
      var ge = je(te);
      te && (e || ge[me]) ? (N(te), Vt()) : N(Ee), X.current = t;
    }
  }, [t]), we(function() {
    // Cancel appear
    (z === st && !a || // Cancel enter
    z === at && !i || // Cancel leave
    z === lt && !u) && N(Ee);
  }, [a, i, u]), we(function() {
    return function() {
      K.current = !1, clearTimeout(Q.current);
    };
  }, []);
  var de = M.useRef(!1);
  we(function() {
    A && (de.current = !0), A !== void 0 && z === Ee && ((de.current || A) && (R == null || R(A)), de.current = !0);
  }, [A, z]);
  var le = Y;
  return Se[me] && E === De && (le = j({
    transition: "none"
  }, le)), [z, E, le, A ?? t];
}
function Ls(e) {
  var t = e;
  ee(e) === "object" && (t = e.transitionSupport);
  function n(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var r = /* @__PURE__ */ M.forwardRef(function(o, i) {
    var s = o.visible, a = s === void 0 ? !0 : s, l = o.removeOnLeave, u = l === void 0 ? !0 : l, f = o.forceRender, m = o.children, d = o.motionName, h = o.leavedClassName, y = o.eventProps, g = M.useContext(vs), p = g.motion, v = n(o, p), _ = J(), T = J();
    function $() {
      try {
        return _.current instanceof HTMLElement ? _.current : hs(T.current);
      } catch {
        return null;
      }
    }
    var C = Ms(v, a, $, o), b = ne(C, 4), w = b[0], R = b[1], L = b[2], O = b[3], A = M.useRef(O);
    O && (A.current = !0);
    var F = M.useCallback(function(W) {
      _.current = W, fs(i, W);
    }, [i]), P, x = j(j({}, y), {}, {
      visible: a
    });
    if (!m)
      P = null;
    else if (w === Ee)
      O ? P = m(j({}, x), F) : !u && A.current && h ? P = m(j(j({}, x), {}, {
        className: h
      }), F) : f || !u && !h ? P = m(j(j({}, x), {}, {
        style: {
          display: "none"
        }
      }), F) : P = null;
    else {
      var I;
      R === me ? I = "prepare" : no(R) ? I = "active" : R === De && (I = "start");
      var N = sr(d, "".concat(w, "-").concat(I));
      P = m(j(j({}, x), {}, {
        className: k(sr(d, w), B(B({}, N, N && I), d, typeof d == "string")),
        style: L
      }), F);
    }
    if (/* @__PURE__ */ M.isValidElement(P) && ds(P)) {
      var V = ms(P);
      V || (P = /* @__PURE__ */ M.cloneElement(P, {
        ref: F
      }));
    }
    return /* @__PURE__ */ M.createElement(Ss, {
      ref: T
    }, P);
  });
  return r.displayName = "CSSMotion", r;
}
const Ns = Ls(Yr);
var sn = "add", an = "keep", ln = "remove", qt = "removed";
function Os(e) {
  var t;
  return e && ee(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, j(j({}, t), {}, {
    key: String(t.key)
  });
}
function cn() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Os);
}
function Fs() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], r = 0, o = t.length, i = cn(e), s = cn(t);
  i.forEach(function(u) {
    for (var f = !1, m = r; m < o; m += 1) {
      var d = s[m];
      if (d.key === u.key) {
        r < m && (n = n.concat(s.slice(r, m).map(function(h) {
          return j(j({}, h), {}, {
            status: sn
          });
        })), r = m), n.push(j(j({}, d), {}, {
          status: an
        })), r += 1, f = !0;
        break;
      }
    }
    f || n.push(j(j({}, u), {}, {
      status: ln
    }));
  }), r < o && (n = n.concat(s.slice(r).map(function(u) {
    return j(j({}, u), {}, {
      status: sn
    });
  })));
  var a = {};
  n.forEach(function(u) {
    var f = u.key;
    a[f] = (a[f] || 0) + 1;
  });
  var l = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return l.forEach(function(u) {
    n = n.filter(function(f) {
      var m = f.key, d = f.status;
      return m !== u || d !== ln;
    }), n.forEach(function(f) {
      f.key === u && (f.status = an);
    });
  }), n;
}
var js = ["component", "children", "onVisibleChanged", "onAllRemoved"], ks = ["status"], As = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function zs(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Ns, n = /* @__PURE__ */ function(r) {
    jt(i, r);
    var o = kt(i);
    function i() {
      var s;
      Xe(this, i);
      for (var a = arguments.length, l = new Array(a), u = 0; u < a; u++)
        l[u] = arguments[u];
      return s = o.call.apply(o, [this].concat(l)), B(Ie(s), "state", {
        keyEntities: []
      }), B(Ie(s), "removeKey", function(f) {
        s.setState(function(m) {
          var d = m.keyEntities.map(function(h) {
            return h.key !== f ? h : j(j({}, h), {}, {
              status: qt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var m = s.state.keyEntities, d = m.filter(function(h) {
            var y = h.status;
            return y !== qt;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Ue(i, [{
      key: "render",
      value: function() {
        var a = this, l = this.state.keyEntities, u = this.props, f = u.component, m = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var h = er(u, js), y = f || M.Fragment, g = {};
        return As.forEach(function(p) {
          g[p] = h[p], delete h[p];
        }), delete h.keys, /* @__PURE__ */ M.createElement(y, h, l.map(function(p, v) {
          var _ = p.status, T = er(p, ks), $ = _ === sn || _ === an;
          return /* @__PURE__ */ M.createElement(t, Ce({}, g, {
            key: T.key,
            visible: $,
            eventProps: T,
            onVisibleChanged: function(b) {
              d == null || d(b, {
                key: T.key
              }), b || a.removeKey(T.key);
            }
          }), function(C, b) {
            return m(j(j({}, C), {}, {
              index: v
            }), b);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, l) {
        var u = a.keys, f = l.keyEntities, m = cn(u), d = Fs(f, m);
        return {
          keyEntities: d.filter(function(h) {
            var y = f.find(function(g) {
              var p = g.key;
              return h.key === p;
            });
            return !(y && y.status === qt && h.status === ln);
          })
        };
      }
    }]), i;
  }(M.Component);
  return B(n, "defaultProps", {
    component: "div"
  }), n;
}
const Ds = zs(Yr);
function Hs(e, t) {
  const {
    children: n,
    upload: r,
    rootClassName: o
  } = e, i = c.useRef(null);
  return c.useImperativeHandle(t, () => i.current), /* @__PURE__ */ c.createElement(Ir, Ce({}, r, {
    showUploadList: !1,
    rootClassName: o,
    ref: i
  }), n);
}
const ro = /* @__PURE__ */ c.forwardRef(Hs);
var oo = /* @__PURE__ */ Ue(function e() {
  Xe(this, e);
}), io = "CALC_UNIT", Bs = new RegExp(io, "g");
function Yt(e) {
  return typeof e == "number" ? "".concat(e).concat(io) : e;
}
var Vs = /* @__PURE__ */ function(e) {
  jt(n, e);
  var t = kt(n);
  function n(r, o) {
    var i;
    Xe(this, n), i = t.call(this), B(Ie(i), "result", ""), B(Ie(i), "unitlessCssVar", void 0), B(Ie(i), "lowPriority", void 0);
    var s = ee(r);
    return i.unitlessCssVar = o, r instanceof n ? i.result = "(".concat(r.result, ")") : s === "number" ? i.result = Yt(r) : s === "string" && (i.result = r), i;
  }
  return Ue(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(Yt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(Yt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var i = this, s = o || {}, a = s.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (l = !1), this.result = this.result.replace(Bs, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(oo), Ws = /* @__PURE__ */ function(e) {
  jt(n, e);
  var t = kt(n);
  function n(r) {
    var o;
    return Xe(this, n), o = t.call(this), B(Ie(o), "result", 0), r instanceof n ? o.result = r.result : typeof r == "number" && (o.result = r), o;
  }
  return Ue(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof n ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof n ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(oo), Xs = function(t, n) {
  var r = t === "css" ? Vs : Ws;
  return function(o) {
    return new r(o, n);
  };
}, lr = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function cr(e, t, n, r) {
  var o = j({}, t[e]);
  if (r != null && r.deprecatedTokens) {
    var i = r.deprecatedTokens;
    i.forEach(function(a) {
      var l = ne(a, 2), u = l[0], f = l[1];
      if (o != null && o[u] || o != null && o[f]) {
        var m;
        (m = o[f]) !== null && m !== void 0 || (o[f] = o == null ? void 0 : o[u]);
      }
    });
  }
  var s = j(j({}, n), o);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var so = typeof CSSINJS_STATISTIC < "u", un = !0;
function Ge() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!so)
    return Object.assign.apply(Object, [{}].concat(t));
  un = !1;
  var r = {};
  return t.forEach(function(o) {
    if (ee(o) === "object") {
      var i = Object.keys(o);
      i.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[s];
          }
        });
      });
    }
  }), un = !0, r;
}
var ur = {};
function Us() {
}
var Gs = function(t) {
  var n, r = t, o = Us;
  return so && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), r = new Proxy(t, {
    get: function(s, a) {
      if (un) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), o = function(s, a) {
    var l;
    ur[s] = {
      global: Array.from(n),
      component: j(j({}, (l = ur[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: r,
    keys: n,
    flush: o
  };
};
function fr(e, t, n) {
  if (typeof n == "function") {
    var r;
    return n(Ge(t, (r = t[e]) !== null && r !== void 0 ? r : {}));
  }
  return n ?? {};
}
function Ks(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "max(".concat(r.map(function(i) {
        return Be(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "min(".concat(r.map(function(i) {
        return Be(i);
      }).join(","), ")");
    }
  };
}
var qs = 1e3 * 60 * 10, Ys = /* @__PURE__ */ function() {
  function e() {
    Xe(this, e), B(this, "map", /* @__PURE__ */ new Map()), B(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), B(this, "nextID", 0), B(this, "lastAccessBeat", /* @__PURE__ */ new Map()), B(this, "accessBeat", 0);
  }
  return Ue(e, [{
    key: "set",
    value: function(n, r) {
      this.clear();
      var o = this.getCompositeKey(n);
      this.map.set(o, r), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var r = this.getCompositeKey(n), o = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var r = this, o = n.map(function(i) {
        return i && ee(i) === "object" ? "obj_".concat(r.getObjectID(i)) : "".concat(ee(i), "_").concat(i);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var r = this.nextID;
      return this.objectIDMap.set(n, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(o, i) {
          r - o > qs && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), dr = new Ys();
function Qs(e, t) {
  return c.useMemo(function() {
    var n = dr.get(t);
    if (n)
      return n;
    var r = e();
    return dr.set(t, r), r;
  }, t);
}
var Zs = function() {
  return {};
};
function Js(e) {
  var t = e.useCSP, n = t === void 0 ? Zs : t, r = e.useToken, o = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, h, y, g) {
    var p = Array.isArray(d) ? d[0] : d;
    function v(R) {
      return "".concat(String(p)).concat(R.slice(0, 1).toUpperCase()).concat(R.slice(1));
    }
    var _ = (g == null ? void 0 : g.unitless) || {}, T = typeof a == "function" ? a(d) : {}, $ = j(j({}, T), {}, B({}, v("zIndexPopup"), !0));
    Object.keys(_).forEach(function(R) {
      $[v(R)] = _[R];
    });
    var C = j(j({}, g), {}, {
      unitless: $,
      prefixToken: v
    }), b = f(d, h, y, C), w = u(p, y, C);
    return function(R) {
      var L = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : R, O = b(R, L), A = ne(O, 2), F = A[1], P = w(L), x = ne(P, 2), I = x[0], N = x[1];
      return [I, F, N];
    };
  }
  function u(d, h, y) {
    var g = y.unitless, p = y.injectStyle, v = p === void 0 ? !0 : p, _ = y.prefixToken, T = y.ignore, $ = function(w) {
      var R = w.rootCls, L = w.cssVar, O = L === void 0 ? {} : L, A = r(), F = A.realToken;
      return ci({
        path: [d],
        prefix: O.prefix,
        key: O.key,
        unitless: g,
        ignore: T,
        token: F,
        scope: R
      }, function() {
        var P = fr(d, F, h), x = cr(d, F, P, {
          deprecatedTokens: y == null ? void 0 : y.deprecatedTokens
        });
        return Object.keys(P).forEach(function(I) {
          x[_(I)] = x[I], delete x[I];
        }), x;
      }), null;
    }, C = function(w) {
      var R = r(), L = R.cssVar;
      return [function(O) {
        return v && L ? /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement($, {
          rootCls: w,
          cssVar: L,
          component: d
        }), O) : O;
      }, L == null ? void 0 : L.key];
    };
    return C;
  }
  function f(d, h, y) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = Array.isArray(d) ? d : [d, d], v = ne(p, 1), _ = v[0], T = p.join("-"), $ = e.layer || {
      name: "antd"
    };
    return function(C) {
      var b = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, w = r(), R = w.theme, L = w.realToken, O = w.hashId, A = w.token, F = w.cssVar, P = o(), x = P.rootPrefixCls, I = P.iconPrefixCls, N = n(), V = F ? "css" : "js", W = Qs(function() {
        var U = /* @__PURE__ */ new Set();
        return F && Object.keys(g.unitless || {}).forEach(function(ie) {
          U.add(Wt(ie, F.prefix)), U.add(Wt(ie, lr(_, F.prefix)));
        }), Xs(V, U);
      }, [V, _, F == null ? void 0 : F.prefix]), Y = Ks(V), H = Y.max, z = Y.min, K = {
        theme: R,
        token: A,
        hashId: O,
        nonce: function() {
          return N.nonce;
        },
        clientOnly: g.clientOnly,
        layer: $,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof i == "function" && kn(j(j({}, K), {}, {
        clientOnly: !1,
        path: ["Shared", x]
      }), function() {
        return i(A, {
          prefix: {
            rootPrefixCls: x,
            iconPrefixCls: I
          },
          csp: N
        });
      });
      var Q = kn(j(j({}, K), {}, {
        path: [T, C, I]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var U = Gs(A), ie = U.token, Ne = U.flush, fe = fr(_, L, y), Ke = ".".concat(C), Oe = cr(_, L, fe, {
          deprecatedTokens: g.deprecatedTokens
        });
        F && fe && ee(fe) === "object" && Object.keys(fe).forEach(function(ke) {
          fe[ke] = "var(".concat(Wt(ke, lr(_, F.prefix)), ")");
        });
        var Fe = Ge(ie, {
          componentCls: Ke,
          prefixCls: C,
          iconCls: ".".concat(I),
          antCls: ".".concat(x),
          calc: W,
          // @ts-ignore
          max: H,
          // @ts-ignore
          min: z
        }, F ? fe : Oe), je = h(Fe, {
          hashId: O,
          prefixCls: C,
          rootPrefixCls: x,
          iconPrefixCls: I
        });
        Ne(_, Oe);
        var Se = typeof s == "function" ? s(Fe, C, b, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : Se, je];
      });
      return [Q, O];
    };
  }
  function m(d, h, y) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = f(d, h, y, j({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), v = function(T) {
      var $ = T.prefixCls, C = T.rootCls, b = C === void 0 ? $ : C;
      return p($, b), null;
    };
    return v;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: m,
    genComponentStyleHook: f
  };
}
function Je(e) {
  "@babel/helpers - typeof";
  return Je = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, Je(e);
}
function ea(e, t) {
  if (Je(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t);
    if (Je(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function ta(e) {
  var t = ea(e, "string");
  return Je(t) == "symbol" ? t : t + "";
}
function ce(e, t, n) {
  return (t = ta(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
const q = Math.round;
function Qt(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = n.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    r[o] = t(r[o] || 0, n[o] || "", o);
  return n[3] ? r[3] = n[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const mr = (e, t, n) => n === 0 ? e : e / 100;
function qe(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class ve {
  constructor(t) {
    ce(this, "isValid", !0), ce(this, "r", 0), ce(this, "g", 0), ce(this, "b", 0), ce(this, "a", 1), ce(this, "_h", void 0), ce(this, "_s", void 0), ce(this, "_l", void 0), ce(this, "_v", void 0), ce(this, "_max", void 0), ce(this, "_min", void 0), ce(this, "_brightness", void 0);
    function n(r) {
      return r[0] in t && r[1] in t && r[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(i) {
        return r.startsWith(i);
      };
      const r = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : o("rgb") ? this.fromRgbString(r) : o("hsl") ? this.fromHslString(r) : (o("hsv") || o("hsb")) && this.fromHsvString(r);
    } else if (t instanceof ve)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = qe(t.r), this.g = qe(t.g), this.b = qe(t.b), this.a = typeof t.a == "number" ? qe(t.a, 1) : 1;
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
    const n = t(this.r), r = t(this.g), o = t(this.b);
    return 0.2126 * n + 0.7152 * r + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = q(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const r = this._c(t), o = n / 100, i = (a) => (r[a] - this[a]) * o + this[a], s = {
      r: q(i("r")),
      g: q(i("g")),
      b: q(i("b")),
      a: q(i("a") * 100) / 100
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
    const n = this._c(t), r = this.a + n.a * (1 - this.a), o = (i) => q((this[i] * this.a + n[i] * n.a * (1 - this.a)) / r);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: r
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
    const r = (this.g || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = q(this.a * 255).toString(16);
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
    const t = this.getHue(), n = q(this.getSaturation() * 100), r = q(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${r}%,${this.a})` : `hsl(${t},${n}%,${r}%)`;
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
  _sc(t, n, r) {
    const o = this.clone();
    return o[t] = qe(n, r), o;
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
    function r(o, i) {
      return parseInt(n[o] + n[i || o], 16);
    }
    n.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = n[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = n[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: r,
    a: o
  }) {
    if (this._h = t % 360, this._s = n, this._l = r, this.a = typeof o == "number" ? o : 1, n <= 0) {
      const d = q(r * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const l = t / 60, u = (1 - Math.abs(2 * r - 1)) * n, f = u * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = u, s = f) : l >= 1 && l < 2 ? (i = f, s = u) : l >= 2 && l < 3 ? (s = u, a = f) : l >= 3 && l < 4 ? (s = f, a = u) : l >= 4 && l < 5 ? (i = f, a = u) : l >= 5 && l < 6 && (i = u, a = f);
    const m = r - u / 2;
    this.r = q((i + m) * 255), this.g = q((s + m) * 255), this.b = q((a + m) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: r,
    a: o
  }) {
    this._h = t % 360, this._s = n, this._v = r, this.a = typeof o == "number" ? o : 1;
    const i = q(r * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), l = s - a, u = q(r * (1 - n) * 255), f = q(r * (1 - n * l) * 255), m = q(r * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = m, this.b = u;
        break;
      case 1:
        this.r = f, this.b = u;
        break;
      case 2:
        this.r = u, this.b = m;
        break;
      case 3:
        this.r = u, this.g = f;
        break;
      case 4:
        this.r = m, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const n = Qt(t, mr);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = Qt(t, mr);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = Qt(t, (r, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? q(r / 100 * 255) : r
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const na = {
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
}, ra = Object.assign(Object.assign({}, na), {
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
function Zt(e) {
  return e >= 0 && e <= 255;
}
function ut(e, t) {
  const {
    r: n,
    g: r,
    b: o,
    a: i
  } = new ve(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: l
  } = new ve(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const f = Math.round((n - s * (1 - u)) / u), m = Math.round((r - a * (1 - u)) / u), d = Math.round((o - l * (1 - u)) / u);
    if (Zt(f) && Zt(m) && Zt(d))
      return new ve({
        r: f,
        g: m,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new ve({
    r: n,
    g: r,
    b: o,
    a: 1
  }).toRgbString();
}
var oa = function(e, t) {
  var n = {};
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
    t.indexOf(r[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, r[o]) && (n[r[o]] = e[r[o]]);
  return n;
};
function ia(e) {
  const {
    override: t
  } = e, n = oa(e, ["override"]), r = Object.assign({}, t);
  Object.keys(ra).forEach((d) => {
    delete r[d];
  });
  const o = Object.assign(Object.assign({}, n), r), i = 480, s = 576, a = 768, l = 992, u = 1200, f = 1600;
  if (o.motion === !1) {
    const d = "0s";
    o.motionDurationFast = d, o.motionDurationMid = d, o.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: ut(o.colorBorderSecondary, o.colorBgContainer),
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
    colorErrorOutline: ut(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: ut(o.colorWarningBg, o.colorBgContainer),
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
    controlOutline: ut(o.colorPrimaryBg, o.colorBgContainer),
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
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new ve("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new ve("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new ve("rgba(0, 0, 0, 0.09)").toRgbString()}
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
  }), r);
}
const sa = {
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
}, aa = {
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
}, la = ui(Qe.defaultAlgorithm), ca = {
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
}, ao = (e, t, n) => {
  const r = n.getDerivativeToken(e), {
    override: o,
    ...i
  } = t;
  let s = {
    ...r,
    override: o
  };
  return s = ia(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: u,
      ...f
    } = l;
    let m = f;
    u && (m = ao({
      ...s,
      ...f
    }, {
      override: f
    }, u)), s[a] = m;
  }), s;
};
function ua() {
  const {
    token: e,
    hashed: t,
    theme: n = la,
    override: r,
    cssVar: o
  } = c.useContext(Qe._internalContext), [i, s, a] = fi(n, [Qe.defaultSeed, e], {
    salt: `${Qi}-${t || ""}`,
    override: r,
    getComputedToken: ao,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: sa,
      ignore: aa,
      preserve: ca
    }
  });
  return [n, a, t ? s : "", i, o];
}
const {
  genStyleHooks: At
} = Js({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = $e();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, r, o] = ua();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: r,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = $e();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), fa = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list-card`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [r]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${r}-name,${r}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${r}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${r}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: n(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: n(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: n(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: n(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${r}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${r}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: o,
        height: o,
        lineHeight: 1,
        [`&:not(${r}-status-error)`]: {
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
        [`${r}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${r}-status-error`]: {
          [`img, ${r}-img-mask`]: {
            borderRadius: n(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${r}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${r}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${r}-remove`]: {
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
      [`&:hover ${r}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${r}-desc`]: {
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
          marginInlineEnd: n(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, fn = {
  "&, *": {
    boxSizing: "border-box"
  }
}, da = (e) => {
  const {
    componentCls: t,
    calc: n,
    antCls: r
  } = e, o = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...fn,
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
        ...fn,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
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
          gap: n(e.paddingXXS).div(2).equal()
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
}, ma = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...fn,
      // =============================== File List ===============================
      [r]: {
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
          maxHeight: n(o).mul(3).equal(),
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
          [`&${r}-overflow-ping-start ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-end ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${r}-overflow-ping-end ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-start ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, pa = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new ve(t).setA(0.85).toRgbString()
  };
}, lo = At("Attachments", (e) => {
  const t = Ge(e, {});
  return [da(t), ma(t), fa(t)];
}, pa), ga = (e) => e.indexOf("image/") === 0, ft = 200;
function ha(e) {
  return new Promise((t) => {
    if (!e || !e.type || !ga(e.type)) {
      t("");
      return;
    }
    const n = new Image();
    if (n.onload = () => {
      const {
        width: r,
        height: o
      } = n, i = r / o, s = i > 1 ? ft : ft * i, a = i > 1 ? ft / i : ft, l = document.createElement("canvas");
      l.width = s, l.height = a, l.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(l), l.getContext("2d").drawImage(n, 0, 0, s, a);
      const f = l.toDataURL();
      document.body.removeChild(l), window.URL.revokeObjectURL(n.src), t(f);
    }, n.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (n.src = r.result);
      }, r.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && t(r.result);
      }, r.readAsDataURL(e);
    } else
      n.src = window.URL.createObjectURL(e);
  });
}
function ya() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "audio"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function va(e) {
  const {
    percent: t
  } = e, {
    token: n
  } = Qe.useToken();
  return /* @__PURE__ */ c.createElement(ni, {
    type: "circle",
    percent: t,
    size: n.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ c.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function ba() {
  return /* @__PURE__ */ c.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ c.createElement("title", null, "video"), /* @__PURE__ */ c.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ c.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const Jt = " ", dn = "#8c8c8c", co = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], Sa = [{
  icon: /* @__PURE__ */ c.createElement(jo, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ c.createElement(ko, null),
  color: dn,
  ext: co
}, {
  icon: /* @__PURE__ */ c.createElement(Ao, null),
  color: dn,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ c.createElement(zo, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ c.createElement(Do, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Ho, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ c.createElement(Bo, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ c.createElement(ba, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ c.createElement(ya, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function pr(e, t) {
  return t.some((n) => e.toLowerCase() === `.${n}`);
}
function xa(e) {
  let t = e;
  const n = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; t >= 1024 && r < n.length - 1; )
    t /= 1024, r++;
  return `${t.toFixed(0)} ${n[r]}`;
}
function wa(e, t) {
  const {
    prefixCls: n,
    item: r,
    onRemove: o,
    className: i,
    style: s
  } = e, a = c.useContext(nt), {
    disabled: l
  } = a || {}, {
    name: u,
    size: f,
    percent: m,
    status: d = "done",
    description: h
  } = r, {
    getPrefixCls: y
  } = $e(), g = y("attachment", n), p = `${g}-list-card`, [v, _, T] = lo(g), [$, C] = c.useMemo(() => {
    const I = u || "", N = I.match(/^(.*)\.[^.]+$/);
    return N ? [N[1], I.slice(N[1].length)] : [I, ""];
  }, [u]), b = c.useMemo(() => pr(C, co), [C]), w = c.useMemo(() => h || (d === "uploading" ? `${m || 0}%` : d === "error" ? r.response || Jt : f ? xa(f) : Jt), [d, m]), [R, L] = c.useMemo(() => {
    for (const {
      ext: I,
      icon: N,
      color: V
    } of Sa)
      if (pr(C, I))
        return [N, V];
    return [/* @__PURE__ */ c.createElement(Oo, {
      key: "defaultIcon"
    }), dn];
  }, [C]), [O, A] = c.useState();
  c.useEffect(() => {
    if (r.originFileObj) {
      let I = !0;
      return ha(r.originFileObj).then((N) => {
        I && A(N);
      }), () => {
        I = !1;
      };
    }
    A(void 0);
  }, [r.originFileObj]);
  let F = null;
  const P = r.thumbUrl || r.url || O, x = b && (r.originFileObj || P);
  return x ? F = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement("img", {
    alt: "preview",
    src: P
  }), d !== "done" && /* @__PURE__ */ c.createElement("div", {
    className: `${p}-img-mask`
  }, d === "uploading" && m !== void 0 && /* @__PURE__ */ c.createElement(va, {
    percent: m,
    prefixCls: p
  }), d === "error" && /* @__PURE__ */ c.createElement("div", {
    className: `${p}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, w)))) : F = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-icon`,
    style: {
      color: L
    }
  }, R), /* @__PURE__ */ c.createElement("div", {
    className: `${p}-content`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-name`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, $ ?? Jt), /* @__PURE__ */ c.createElement("div", {
    className: `${p}-ellipsis-suffix`
  }, C)), /* @__PURE__ */ c.createElement("div", {
    className: `${p}-desc`
  }, /* @__PURE__ */ c.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, w)))), v(/* @__PURE__ */ c.createElement("div", {
    className: k(p, {
      [`${p}-status-${d}`]: d,
      [`${p}-type-preview`]: x,
      [`${p}-type-overview`]: !x
    }, i, _, T),
    style: s,
    ref: t
  }, F, !l && o && /* @__PURE__ */ c.createElement("button", {
    type: "button",
    className: `${p}-remove`,
    onClick: () => {
      o(r);
    }
  }, /* @__PURE__ */ c.createElement(Fo, null))));
}
const uo = /* @__PURE__ */ c.forwardRef(wa), gr = 1;
function _a(e) {
  const {
    prefixCls: t,
    items: n,
    onRemove: r,
    overflow: o,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: l,
    itemStyle: u
  } = e, f = `${t}-list`, m = c.useRef(null), [d, h] = c.useState(!1), {
    disabled: y
  } = c.useContext(nt);
  c.useEffect(() => (h(!0), () => {
    h(!1);
  }), []);
  const [g, p] = c.useState(!1), [v, _] = c.useState(!1), T = () => {
    const w = m.current;
    w && (o === "scrollX" ? (p(Math.abs(w.scrollLeft) >= gr), _(w.scrollWidth - w.clientWidth - Math.abs(w.scrollLeft) >= gr)) : o === "scrollY" && (p(w.scrollTop !== 0), _(w.scrollHeight - w.clientHeight !== w.scrollTop)));
  };
  c.useEffect(() => {
    T();
  }, [o]);
  const $ = (w) => {
    const R = m.current;
    R && R.scrollTo({
      left: R.scrollLeft + w * R.clientWidth,
      behavior: "smooth"
    });
  }, C = () => {
    $(-1);
  }, b = () => {
    $(1);
  };
  return /* @__PURE__ */ c.createElement("div", {
    className: k(f, {
      [`${f}-overflow-${e.overflow}`]: o,
      [`${f}-overflow-ping-start`]: g,
      [`${f}-overflow-ping-end`]: v
    }, s),
    ref: m,
    onScroll: T,
    style: a
  }, /* @__PURE__ */ c.createElement(Ds, {
    keys: n.map((w) => ({
      key: w.uid,
      item: w
    })),
    motionName: `${f}-card-motion`,
    component: !1,
    motionAppear: d,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: w,
    item: R,
    className: L,
    style: O
  }) => /* @__PURE__ */ c.createElement(uo, {
    key: w,
    prefixCls: t,
    item: R,
    onRemove: r,
    className: k(L, l),
    style: {
      ...O,
      ...u
    }
  })), !y && /* @__PURE__ */ c.createElement(ro, {
    upload: i
  }, /* @__PURE__ */ c.createElement(oe, {
    className: `${f}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ c.createElement(Vo, {
    className: `${f}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(oe, {
    size: "small",
    shape: "circle",
    className: `${f}-prev-btn`,
    icon: /* @__PURE__ */ c.createElement(Wo, null),
    onClick: C
  }), /* @__PURE__ */ c.createElement(oe, {
    size: "small",
    shape: "circle",
    className: `${f}-next-btn`,
    icon: /* @__PURE__ */ c.createElement(Xo, null),
    onClick: b
  })));
}
function Ca(e, t) {
  const {
    prefixCls: n,
    placeholder: r = {},
    upload: o,
    className: i,
    style: s
  } = e, a = `${n}-placeholder`, l = r || {}, {
    disabled: u
  } = c.useContext(nt), [f, m] = c.useState(!1), d = () => {
    m(!0);
  }, h = (p) => {
    p.currentTarget.contains(p.relatedTarget) || m(!1);
  }, y = () => {
    m(!1);
  }, g = /* @__PURE__ */ c.isValidElement(r) ? r : /* @__PURE__ */ c.createElement(_e, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ c.createElement(Te.Text, {
    className: `${a}-icon`
  }, l.icon), /* @__PURE__ */ c.createElement(Te.Title, {
    className: `${a}-title`,
    level: 5
  }, l.title), /* @__PURE__ */ c.createElement(Te.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, l.description));
  return /* @__PURE__ */ c.createElement("div", {
    className: k(a, {
      [`${a}-drag-in`]: f,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: d,
    onDragLeave: h,
    onDrop: y,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ c.createElement(Ir.Dragger, Ce({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), g));
}
const Ea = /* @__PURE__ */ c.forwardRef(Ca);
function Ta(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    rootStyle: o,
    className: i,
    style: s,
    items: a,
    children: l,
    getDropContainer: u,
    placeholder: f,
    onChange: m,
    overflow: d,
    disabled: h,
    classNames: y = {},
    styles: g = {},
    ...p
  } = e, {
    getPrefixCls: v,
    direction: _
  } = $e(), T = v("attachment", n), $ = Ct("attachments"), {
    classNames: C,
    styles: b
  } = $, w = c.useRef(null), R = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: w.current,
    upload: (H) => {
      var K, Q;
      const z = (Q = (K = R.current) == null ? void 0 : K.nativeElement) == null ? void 0 : Q.querySelector('input[type="file"]');
      if (z) {
        const U = new DataTransfer();
        U.items.add(H), z.files = U.files, z.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [L, O, A] = lo(T), F = k(O, A), [P, x] = os([], {
    value: a
  }), I = Pe((H) => {
    x(H.fileList), m == null || m(H);
  }), N = {
    ...p,
    fileList: P,
    onChange: I
  }, V = (H) => {
    const z = P.filter((K) => K.uid !== H.uid);
    I({
      file: H,
      fileList: z
    });
  };
  let W;
  const Y = (H, z, K) => {
    const Q = typeof f == "function" ? f(H) : f;
    return /* @__PURE__ */ c.createElement(Ea, {
      placeholder: Q,
      upload: N,
      prefixCls: T,
      className: k(C.placeholder, y.placeholder),
      style: {
        ...b.placeholder,
        ...g.placeholder,
        ...z == null ? void 0 : z.style
      },
      ref: K
    });
  };
  if (l)
    W = /* @__PURE__ */ c.createElement(c.Fragment, null, /* @__PURE__ */ c.createElement(ro, {
      upload: N,
      rootClassName: r,
      ref: R
    }, l), /* @__PURE__ */ c.createElement(Zn, {
      getDropContainer: u,
      prefixCls: T,
      className: k(F, r)
    }, Y("drop")));
  else {
    const H = P.length > 0;
    W = /* @__PURE__ */ c.createElement("div", {
      className: k(T, F, {
        [`${T}-rtl`]: _ === "rtl"
      }, i, r),
      style: {
        ...o,
        ...s
      },
      dir: _ || "ltr",
      ref: w
    }, /* @__PURE__ */ c.createElement(_a, {
      prefixCls: T,
      items: P,
      onRemove: V,
      overflow: d,
      upload: N,
      listClassName: k(C.list, y.list),
      listStyle: {
        ...b.list,
        ...g.list,
        ...!H && {
          display: "none"
        }
      },
      itemClassName: k(C.item, y.item),
      itemStyle: {
        ...b.item,
        ...g.item
      }
    }), Y("inline", H ? {
      style: {
        display: "none"
      }
    } : {}, R), /* @__PURE__ */ c.createElement(Zn, {
      getDropContainer: u || (() => w.current),
      prefixCls: T,
      className: F
    }, Y("drop")));
  }
  return L(/* @__PURE__ */ c.createElement(nt.Provider, {
    value: {
      disabled: h
    }
  }, W));
}
const fo = /* @__PURE__ */ c.forwardRef(Ta);
fo.FileCard = uo;
var $a = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, Pa = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Ra = "".concat($a, " ").concat(Pa).split(/[\s\n]+/), Ia = "aria-", Ma = "data-";
function hr(e, t) {
  return e.indexOf(t) === 0;
}
function La(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = j({}, t);
  var r = {};
  return Object.keys(e).forEach(function(o) {
    // Aria
    (n.aria && (o === "role" || hr(o, Ia)) || // Data
    n.data && hr(o, Ma) || // Attr
    n.attr && Ra.includes(o)) && (r[o] = e[o]);
  }), r;
}
function dt(e) {
  return typeof e == "string";
}
const Na = (e, t, n, r) => {
  const [o, i] = M.useState(""), [s, a] = M.useState(1), l = t && dt(e);
  return zr(() => {
    i(e), !l && dt(e) ? a(e.length) : dt(e) && dt(o) && e.indexOf(o) !== 0 && a(1);
  }, [e]), M.useEffect(() => {
    if (l && s < e.length) {
      const f = setTimeout(() => {
        a((m) => m + n);
      }, r);
      return () => {
        clearTimeout(f);
      };
    }
  }, [s, t, e]), [l ? e.slice(0, s) : e, l && s < e.length];
};
function Oa(e) {
  return M.useMemo(() => {
    if (!e)
      return [!1, 0, 0, null];
    let t = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof e == "object" && (t = {
      ...t,
      ...e
    }), [!0, t.step, t.interval, t.suffix];
  }, [e]);
}
const Fa = ({
  prefixCls: e
}) => /* @__PURE__ */ c.createElement("span", {
  className: `${e}-dot`
}, /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ c.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-3"
})), ja = (e) => {
  const {
    componentCls: t,
    paddingSM: n,
    padding: r
  } = e;
  return {
    [t]: {
      [`${t}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${Be(n)} ${Be(r)}`,
          borderRadius: e.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: e.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${e.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: e.boxShadowTertiary
        }
      }
    }
  };
}, ka = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: r,
    paddingSM: o,
    padding: i,
    calc: s
  } = e, a = s(n).mul(r).div(2).add(o).equal(), l = `${t}-content`;
  return {
    [t]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: s(i).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: e.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: e.borderRadiusXS
      }
    }
  };
}, Aa = (e) => {
  const {
    componentCls: t,
    padding: n
  } = e;
  return {
    [`${t}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: n,
      overflowY: "auto"
    }
  };
}, za = new Lr("loadingMove", {
  "0%": {
    transform: "translateY(0)"
  },
  "10%": {
    transform: "translateY(4px)"
  },
  "20%": {
    transform: "translateY(0)"
  },
  "30%": {
    transform: "translateY(-4px)"
  },
  "40%": {
    transform: "translateY(0)"
  }
}), Da = new Lr("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), Ha = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: r,
    paddingSM: o,
    colorText: i,
    calc: s
  } = e;
  return {
    [t]: {
      display: "flex",
      columnGap: o,
      [`&${t}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${t}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`&${t}-typing ${t}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: Da,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${t}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${t}-header, & ${t}-footer`]: {
        fontSize: n,
        lineHeight: r,
        color: e.colorText
      },
      [`& ${t}-header`]: {
        marginBottom: e.paddingXXS
      },
      [`& ${t}-footer`]: {
        marginTop: o
      },
      // =========================== Content =============================
      [`& ${t}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${t}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: i,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        minHeight: s(o).mul(2).add(s(r).mul(n)).equal(),
        wordBreak: "break-word",
        [`& ${t}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: e.marginXS,
          padding: `0 ${Be(e.paddingXXS)}`,
          "&-item": {
            backgroundColor: e.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: za,
            animationDuration: "2s",
            animationIterationCount: "infinite",
            animationTimingFunction: "linear",
            "&:nth-child(1)": {
              animationDelay: "0s"
            },
            "&:nth-child(2)": {
              animationDelay: "0.2s"
            },
            "&:nth-child(3)": {
              animationDelay: "0.4s"
            }
          }
        }
      }
    }
  };
}, Ba = () => ({}), mo = At("Bubble", (e) => {
  const t = Ge(e, {});
  return [Ha(t), Aa(t), ja(t), ka(t)];
}, Ba), po = /* @__PURE__ */ c.createContext({}), Va = (e, t) => {
  const {
    prefixCls: n,
    className: r,
    rootClassName: o,
    style: i,
    classNames: s = {},
    styles: a = {},
    avatar: l,
    placement: u = "start",
    loading: f = !1,
    loadingRender: m,
    typing: d,
    content: h = "",
    messageRender: y,
    variant: g = "filled",
    shape: p,
    onTypingComplete: v,
    header: _,
    footer: T,
    ...$
  } = e, {
    onUpdate: C
  } = c.useContext(po), b = c.useRef(null);
  c.useImperativeHandle(t, () => ({
    nativeElement: b.current
  }));
  const {
    direction: w,
    getPrefixCls: R
  } = $e(), L = R("bubble", n), O = Ct("bubble"), [A, F, P, x] = Oa(d), [I, N] = Na(h, A, F, P);
  c.useEffect(() => {
    C == null || C();
  }, [I]);
  const V = c.useRef(!1);
  c.useEffect(() => {
    !N && !f ? V.current || (V.current = !0, v == null || v()) : V.current = !1;
  }, [N, f]);
  const [W, Y, H] = mo(L), z = k(L, o, O.className, r, Y, H, `${L}-${u}`, {
    [`${L}-rtl`]: w === "rtl",
    [`${L}-typing`]: N && !f && !y && !x
  }), K = /* @__PURE__ */ c.isValidElement(l) ? l : /* @__PURE__ */ c.createElement(ri, l), Q = y ? y(I) : I;
  let U;
  f ? U = m ? m() : /* @__PURE__ */ c.createElement(Fa, {
    prefixCls: L
  }) : U = /* @__PURE__ */ c.createElement(c.Fragment, null, Q, N && x);
  let ie = /* @__PURE__ */ c.createElement("div", {
    style: {
      ...O.styles.content,
      ...a.content
    },
    className: k(`${L}-content`, `${L}-content-${g}`, p && `${L}-content-${p}`, O.classNames.content, s.content)
  }, U);
  return (_ || T) && (ie = /* @__PURE__ */ c.createElement("div", {
    className: `${L}-content-wrapper`
  }, _ && /* @__PURE__ */ c.createElement("div", {
    className: k(`${L}-header`, O.classNames.header, s.header),
    style: {
      ...O.styles.header,
      ...a.header
    }
  }, _), ie, T && /* @__PURE__ */ c.createElement("div", {
    className: k(`${L}-footer`, O.classNames.footer, s.footer),
    style: {
      ...O.styles.footer,
      ...a.footer
    }
  }, T))), W(/* @__PURE__ */ c.createElement("div", Ce({
    style: {
      ...O.style,
      ...i
    },
    className: z
  }, $, {
    ref: b
  }), l && /* @__PURE__ */ c.createElement("div", {
    style: {
      ...O.styles.avatar,
      ...a.avatar
    },
    className: k(`${L}-avatar`, O.classNames.avatar, s.avatar)
  }, K), ie));
}, Tn = /* @__PURE__ */ c.forwardRef(Va);
function Wa(e) {
  const [t, n] = c.useState(e.length), r = c.useMemo(() => e.slice(0, t), [e, t]), o = c.useMemo(() => {
    const s = r[r.length - 1];
    return s ? s.key : null;
  }, [r]);
  c.useEffect(() => {
    var s;
    if (!(r.length && r.every((a, l) => {
      var u;
      return a.key === ((u = e[l]) == null ? void 0 : u.key);
    }))) {
      if (r.length === 0)
        n(1);
      else
        for (let a = 0; a < r.length; a += 1)
          if (r[a].key !== ((s = e[a]) == null ? void 0 : s.key)) {
            n(a);
            break;
          }
    }
  }, [e]);
  const i = Pe((s) => {
    s === o && n(t + 1);
  });
  return [r, i];
}
function Xa(e, t) {
  const n = M.useCallback((r) => typeof t == "function" ? t(r) : t ? t[r.role] || {} : {}, [t]);
  return M.useMemo(() => (e || []).map((r, o) => {
    const i = r.key ?? `preset_${o}`;
    return {
      ...n(r),
      ...r,
      key: i
    };
  }), [e, n]);
}
const Ua = 1, Ga = (e, t) => {
  const {
    prefixCls: n,
    rootClassName: r,
    className: o,
    items: i,
    autoScroll: s = !0,
    roles: a,
    ...l
  } = e, u = La(l, {
    attr: !0,
    aria: !0
  }), f = M.useRef(null), m = M.useRef({}), {
    getPrefixCls: d
  } = $e(), h = d("bubble", n), y = `${h}-list`, [g, p, v] = mo(h), [_, T] = M.useState(!1);
  M.useEffect(() => (T(!0), () => {
    T(!1);
  }), []);
  const $ = Xa(i, a), [C, b] = Wa($), [w, R] = M.useState(!0), [L, O] = M.useState(0), A = (x) => {
    const I = x.target;
    R(I.scrollHeight - Math.abs(I.scrollTop) - I.clientHeight <= Ua);
  };
  M.useEffect(() => {
    s && f.current && w && f.current.scrollTo({
      top: f.current.scrollHeight
    });
  }, [L]), M.useEffect(() => {
    var x;
    if (s) {
      const I = (x = C[C.length - 2]) == null ? void 0 : x.key, N = m.current[I];
      if (N) {
        const {
          nativeElement: V
        } = N, {
          top: W,
          bottom: Y
        } = V.getBoundingClientRect(), {
          top: H,
          bottom: z
        } = f.current.getBoundingClientRect();
        W < z && Y > H && (O((Q) => Q + 1), R(!0));
      }
    }
  }, [C.length]), M.useImperativeHandle(t, () => ({
    nativeElement: f.current,
    scrollTo: ({
      key: x,
      offset: I,
      behavior: N = "smooth",
      block: V
    }) => {
      if (typeof I == "number")
        f.current.scrollTo({
          top: I,
          behavior: N
        });
      else if (x !== void 0) {
        const W = m.current[x];
        if (W) {
          const Y = C.findIndex((H) => H.key === x);
          R(Y === C.length - 1), W.nativeElement.scrollIntoView({
            behavior: N,
            block: V
          });
        }
      }
    }
  }));
  const F = Pe(() => {
    s && O((x) => x + 1);
  }), P = M.useMemo(() => ({
    onUpdate: F
  }), []);
  return g(/* @__PURE__ */ M.createElement(po.Provider, {
    value: P
  }, /* @__PURE__ */ M.createElement("div", Ce({}, u, {
    className: k(y, r, o, p, v, {
      [`${y}-reach-end`]: w
    }),
    ref: f,
    onScroll: A
  }), C.map(({
    key: x,
    ...I
  }) => /* @__PURE__ */ M.createElement(Tn, Ce({}, I, {
    key: x,
    ref: (N) => {
      N ? m.current[x] = N : delete m.current[x];
    },
    typing: _ ? I.typing : !1,
    onTypingComplete: () => {
      var N;
      (N = I.onTypingComplete) == null || N.call(I), b(x);
    }
  }))))));
}, Ka = /* @__PURE__ */ M.forwardRef(Ga);
Tn.List = Ka;
const qa = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Prompt ========================
      "&, & *": {
        boxSizing: "border-box"
      },
      maxWidth: "100%",
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`& ${t}-title`]: {
        marginBlockStart: 0,
        fontWeight: "normal",
        color: e.colorTextTertiary
      },
      [`& ${t}-list`]: {
        display: "flex",
        gap: e.paddingSM,
        overflowX: "scroll",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        listStyle: "none",
        paddingInlineStart: 0,
        marginBlock: 0,
        alignItems: "stretch",
        "&-wrap": {
          flexWrap: "wrap"
        },
        "&-vertical": {
          flexDirection: "column",
          alignItems: "flex-start"
        }
      },
      // ========================= Item =========================
      [`${t}-item`]: {
        flex: "none",
        display: "flex",
        gap: e.paddingXS,
        height: "auto",
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        alignItems: "flex-start",
        justifyContent: "flex-start",
        background: e.colorBgContainer,
        borderRadius: e.borderRadiusLG,
        transition: ["border", "background"].map((n) => `${n} ${e.motionDurationSlow}`).join(","),
        border: `${Be(e.lineWidth)} ${e.lineType} ${e.colorBorderSecondary}`,
        [`&:not(${t}-item-has-nest)`]: {
          "&:hover": {
            cursor: "pointer",
            background: e.colorFillTertiary
          },
          "&:active": {
            background: e.colorFill
          }
        },
        [`${t}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          gap: e.paddingXXS,
          flexDirection: "column",
          alignItems: "flex-start"
        },
        [`${t}-icon, ${t}-label, ${t}-desc`]: {
          margin: 0,
          padding: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight,
          textAlign: "start",
          whiteSpace: "normal"
        },
        [`${t}-label`]: {
          color: e.colorTextHeading,
          fontWeight: 500
        },
        [`${t}-label + ${t}-desc`]: {
          color: e.colorTextTertiary
        },
        // Disabled
        [`&${t}-item-disabled`]: {
          pointerEvents: "none",
          background: e.colorBgContainerDisabled,
          [`${t}-label, ${t}-desc`]: {
            color: e.colorTextTertiary
          }
        }
      }
    }
  };
}, Ya = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ========================= Parent =========================
      [`${t}-item-has-nest`]: {
        [`> ${t}-content`]: {
          // gap: token.paddingSM,
          [`> ${t}-label`]: {
            fontSize: e.fontSizeLG,
            lineHeight: e.lineHeightLG
          }
        }
      },
      // ========================= Nested =========================
      [`&${t}-nested`]: {
        marginTop: e.paddingXS,
        // ======================== Prompt ========================
        alignSelf: "stretch",
        [`${t}-list`]: {
          alignItems: "stretch"
        },
        // ========================= Item =========================
        [`${t}-item`]: {
          border: 0,
          background: e.colorFillQuaternary
        }
      }
    }
  };
}, Qa = () => ({}), Za = At("Prompts", (e) => {
  const t = Ge(e, {});
  return [qa(t), Ya(t)];
}, Qa), $n = (e) => {
  const {
    prefixCls: t,
    title: n,
    className: r,
    items: o,
    onItemClick: i,
    vertical: s,
    wrap: a,
    rootClassName: l,
    styles: u = {},
    classNames: f = {},
    style: m,
    ...d
  } = e, {
    getPrefixCls: h,
    direction: y
  } = $e(), g = h("prompts", t), p = Ct("prompts"), [v, _, T] = Za(g), $ = k(g, p.className, r, l, _, T, {
    [`${g}-rtl`]: y === "rtl"
  }), C = k(`${g}-list`, p.classNames.list, f.list, {
    [`${g}-list-wrap`]: a
  }, {
    [`${g}-list-vertical`]: s
  });
  return v(/* @__PURE__ */ c.createElement("div", Ce({}, d, {
    className: $,
    style: {
      ...m,
      ...p.style
    }
  }), n && /* @__PURE__ */ c.createElement(Te.Title, {
    level: 5,
    className: k(`${g}-title`, p.classNames.title, f.title),
    style: {
      ...p.styles.title,
      ...u.title
    }
  }, n), /* @__PURE__ */ c.createElement("div", {
    className: C,
    style: {
      ...p.styles.list,
      ...u.list
    }
  }, o == null ? void 0 : o.map((b, w) => {
    const R = b.children && b.children.length > 0;
    return /* @__PURE__ */ c.createElement("div", {
      key: b.key || `key_${w}`,
      style: {
        ...p.styles.item,
        ...u.item
      },
      className: k(`${g}-item`, p.classNames.item, f.item, {
        [`${g}-item-disabled`]: b.disabled,
        [`${g}-item-has-nest`]: R
      }),
      onClick: () => {
        !R && i && i({
          data: b
        });
      }
    }, b.icon && /* @__PURE__ */ c.createElement("div", {
      className: `${g}-icon`
    }, b.icon), /* @__PURE__ */ c.createElement("div", {
      className: k(`${g}-content`, p.classNames.itemContent, f.itemContent),
      style: {
        ...p.styles.itemContent,
        ...u.itemContent
      }
    }, b.label && /* @__PURE__ */ c.createElement("h6", {
      className: `${g}-label`
    }, b.label), b.description && /* @__PURE__ */ c.createElement("p", {
      className: `${g}-desc`
    }, b.description), R && /* @__PURE__ */ c.createElement($n, {
      className: `${g}-nested`,
      items: b.children,
      vertical: !0,
      onItemClick: i,
      classNames: {
        list: f.subList,
        item: f.subItem
      },
      styles: {
        list: u.subList,
        item: u.subItem
      }
    })));
  }))));
}, Ja = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = n(e.fontSizeHeading3).mul(e.lineHeightHeading3).equal(), o = n(e.fontSize).mul(e.lineHeight).equal();
  return {
    [t]: {
      gap: e.padding,
      // ======================== Icon ========================
      [`${t}-icon`]: {
        height: n(r).add(o).add(e.paddingXXS).equal(),
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
}, el = (e) => {
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
}, tl = () => ({}), nl = At("Welcome", (e) => {
  const t = Ge(e, {});
  return [Ja(t), el(t)];
}, tl);
function rl(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    className: o,
    style: i,
    variant: s = "filled",
    // Semantic
    classNames: a = {},
    styles: l = {},
    // Layout
    icon: u,
    title: f,
    description: m,
    extra: d
  } = e, {
    direction: h,
    getPrefixCls: y
  } = $e(), g = y("welcome", n), p = Ct("welcome"), [v, _, T] = nl(g), $ = c.useMemo(() => {
    if (!u)
      return null;
    let w = u;
    return typeof u == "string" && u.startsWith("http") && (w = /* @__PURE__ */ c.createElement("img", {
      src: u,
      alt: "icon"
    })), /* @__PURE__ */ c.createElement("div", {
      className: k(`${g}-icon`, p.classNames.icon, a.icon),
      style: l.icon
    }, w);
  }, [u]), C = c.useMemo(() => f ? /* @__PURE__ */ c.createElement(Te.Title, {
    level: 4,
    className: k(`${g}-title`, p.classNames.title, a.title),
    style: l.title
  }, f) : null, [f]), b = c.useMemo(() => d ? /* @__PURE__ */ c.createElement("div", {
    className: k(`${g}-extra`, p.classNames.extra, a.extra),
    style: l.extra
  }, d) : null, [d]);
  return v(/* @__PURE__ */ c.createElement(_e, {
    ref: t,
    className: k(g, p.className, o, r, _, T, `${g}-${s}`, {
      [`${g}-rtl`]: h === "rtl"
    }),
    style: i
  }, $, /* @__PURE__ */ c.createElement(_e, {
    vertical: !0,
    className: `${g}-content-wrapper`
  }, d ? /* @__PURE__ */ c.createElement(_e, {
    align: "flex-start",
    className: `${g}-title-wrapper`
  }, C, b) : C, m && /* @__PURE__ */ c.createElement(Te.Text, {
    className: k(`${g}-description`, p.classNames.description, a.description),
    style: l.description
  }, m))));
}
const ol = /* @__PURE__ */ c.forwardRef(rl);
function re(e) {
  const t = J(e);
  return t.current = e, Po((...n) => {
    var r;
    return (r = t.current) == null ? void 0 : r.call(t, ...n);
  }, []);
}
function ye(e, t) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (!(t != null && t.omitNull) || e[r] !== null) && (n[r] = e[r]), n), {});
}
var go = Symbol.for("immer-nothing"), yr = Symbol.for("immer-draftable"), se = Symbol.for("immer-state");
function pe(e, ...t) {
  throw new Error(`[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`);
}
var Ve = Object.getPrototypeOf;
function We(e) {
  return !!e && !!e[se];
}
function Me(e) {
  var t;
  return e ? ho(e) || Array.isArray(e) || !!e[yr] || !!((t = e.constructor) != null && t[yr]) || Dt(e) || Ht(e) : !1;
}
var il = Object.prototype.constructor.toString();
function ho(e) {
  if (!e || typeof e != "object") return !1;
  const t = Ve(e);
  if (t === null)
    return !0;
  const n = Object.hasOwnProperty.call(t, "constructor") && t.constructor;
  return n === Object ? !0 : typeof n == "function" && Function.toString.call(n) === il;
}
function St(e, t) {
  zt(e) === 0 ? Reflect.ownKeys(e).forEach((n) => {
    t(n, e[n], e);
  }) : e.forEach((n, r) => t(r, n, e));
}
function zt(e) {
  const t = e[se];
  return t ? t.type_ : Array.isArray(e) ? 1 : Dt(e) ? 2 : Ht(e) ? 3 : 0;
}
function mn(e, t) {
  return zt(e) === 2 ? e.has(t) : Object.prototype.hasOwnProperty.call(e, t);
}
function yo(e, t, n) {
  const r = zt(e);
  r === 2 ? e.set(t, n) : r === 3 ? e.add(n) : e[t] = n;
}
function sl(e, t) {
  return e === t ? e !== 0 || 1 / e === 1 / t : e !== e && t !== t;
}
function Dt(e) {
  return e instanceof Map;
}
function Ht(e) {
  return e instanceof Set;
}
function Re(e) {
  return e.copy_ || e.base_;
}
function pn(e, t) {
  if (Dt(e))
    return new Map(e);
  if (Ht(e))
    return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  const n = ho(e);
  if (t === !0 || t === "class_only" && !n) {
    const r = Object.getOwnPropertyDescriptors(e);
    delete r[se];
    let o = Reflect.ownKeys(r);
    for (let i = 0; i < o.length; i++) {
      const s = o[i], a = r[s];
      a.writable === !1 && (a.writable = !0, a.configurable = !0), (a.get || a.set) && (r[s] = {
        configurable: !0,
        writable: !0,
        // could live with !!desc.set as well here...
        enumerable: a.enumerable,
        value: e[s]
      });
    }
    return Object.create(Ve(e), r);
  } else {
    const r = Ve(e);
    if (r !== null && n)
      return {
        ...e
      };
    const o = Object.create(r);
    return Object.assign(o, e);
  }
}
function Pn(e, t = !1) {
  return Bt(e) || We(e) || !Me(e) || (zt(e) > 1 && (e.set = e.add = e.clear = e.delete = al), Object.freeze(e), t && Object.entries(e).forEach(([n, r]) => Pn(r, !0))), e;
}
function al() {
  pe(2);
}
function Bt(e) {
  return Object.isFrozen(e);
}
var ll = {};
function Le(e) {
  const t = ll[e];
  return t || pe(0, e), t;
}
var et;
function vo() {
  return et;
}
function cl(e, t) {
  return {
    drafts_: [],
    parent_: e,
    immer_: t,
    // Whenever the modified draft contains a draft from another scope, we
    // need to prevent auto-freezing so the unowned draft can be finalized.
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0
  };
}
function vr(e, t) {
  t && (Le("Patches"), e.patches_ = [], e.inversePatches_ = [], e.patchListener_ = t);
}
function gn(e) {
  hn(e), e.drafts_.forEach(ul), e.drafts_ = null;
}
function hn(e) {
  e === et && (et = e.parent_);
}
function br(e) {
  return et = cl(et, e);
}
function ul(e) {
  const t = e[se];
  t.type_ === 0 || t.type_ === 1 ? t.revoke_() : t.revoked_ = !0;
}
function Sr(e, t) {
  t.unfinalizedDrafts_ = t.drafts_.length;
  const n = t.drafts_[0];
  return e !== void 0 && e !== n ? (n[se].modified_ && (gn(t), pe(4)), Me(e) && (e = xt(t, e), t.parent_ || wt(t, e)), t.patches_ && Le("Patches").generateReplacementPatches_(n[se].base_, e, t.patches_, t.inversePatches_)) : e = xt(t, n, []), gn(t), t.patches_ && t.patchListener_(t.patches_, t.inversePatches_), e !== go ? e : void 0;
}
function xt(e, t, n) {
  if (Bt(t)) return t;
  const r = t[se];
  if (!r)
    return St(t, (o, i) => xr(e, r, t, o, i, n)), t;
  if (r.scope_ !== e) return t;
  if (!r.modified_)
    return wt(e, r.base_, !0), r.base_;
  if (!r.finalized_) {
    r.finalized_ = !0, r.scope_.unfinalizedDrafts_--;
    const o = r.copy_;
    let i = o, s = !1;
    r.type_ === 3 && (i = new Set(o), o.clear(), s = !0), St(i, (a, l) => xr(e, r, o, a, l, n, s)), wt(e, o, !1), n && e.patches_ && Le("Patches").generatePatches_(r, n, e.patches_, e.inversePatches_);
  }
  return r.copy_;
}
function xr(e, t, n, r, o, i, s) {
  if (We(o)) {
    const a = i && t && t.type_ !== 3 && // Set objects are atomic since they have no keys.
    !mn(t.assigned_, r) ? i.concat(r) : void 0, l = xt(e, o, a);
    if (yo(n, r, l), We(l))
      e.canAutoFreeze_ = !1;
    else return;
  } else s && n.add(o);
  if (Me(o) && !Bt(o)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1)
      return;
    xt(e, o), (!t || !t.scope_.parent_) && typeof r != "symbol" && Object.prototype.propertyIsEnumerable.call(n, r) && wt(e, o);
  }
}
function wt(e, t, n = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && Pn(t, n);
}
function fl(e, t) {
  const n = Array.isArray(e), r = {
    type_: n ? 1 : 0,
    // Track which produce call this is associated with.
    scope_: t ? t.scope_ : vo(),
    // True for both shallow and deep changes.
    modified_: !1,
    // Used during finalization.
    finalized_: !1,
    // Track which properties have been assigned (true) or deleted (false).
    assigned_: {},
    // The parent draft state.
    parent_: t,
    // The base state.
    base_: e,
    // The base proxy.
    draft_: null,
    // set below
    // The base copy with any updated values.
    copy_: null,
    // Called by the `produce` function.
    revoke_: null,
    isManual_: !1
  };
  let o = r, i = Rn;
  n && (o = [r], i = tt);
  const {
    revoke: s,
    proxy: a
  } = Proxy.revocable(o, i);
  return r.draft_ = a, r.revoke_ = s, a;
}
var Rn = {
  get(e, t) {
    if (t === se) return e;
    const n = Re(e);
    if (!mn(n, t))
      return dl(e, n, t);
    const r = n[t];
    return e.finalized_ || !Me(r) ? r : r === en(e.base_, t) ? (tn(e), e.copy_[t] = vn(r, e)) : r;
  },
  has(e, t) {
    return t in Re(e);
  },
  ownKeys(e) {
    return Reflect.ownKeys(Re(e));
  },
  set(e, t, n) {
    const r = bo(Re(e), t);
    if (r != null && r.set)
      return r.set.call(e.draft_, n), !0;
    if (!e.modified_) {
      const o = en(Re(e), t), i = o == null ? void 0 : o[se];
      if (i && i.base_ === n)
        return e.copy_[t] = n, e.assigned_[t] = !1, !0;
      if (sl(n, o) && (n !== void 0 || mn(e.base_, t))) return !0;
      tn(e), yn(e);
    }
    return e.copy_[t] === n && // special case: handle new props with value 'undefined'
    (n !== void 0 || t in e.copy_) || // special case: NaN
    Number.isNaN(n) && Number.isNaN(e.copy_[t]) || (e.copy_[t] = n, e.assigned_[t] = !0), !0;
  },
  deleteProperty(e, t) {
    return en(e.base_, t) !== void 0 || t in e.base_ ? (e.assigned_[t] = !1, tn(e), yn(e)) : delete e.assigned_[t], e.copy_ && delete e.copy_[t], !0;
  },
  // Note: We never coerce `desc.value` into an Immer draft, because we can't make
  // the same guarantee in ES5 mode.
  getOwnPropertyDescriptor(e, t) {
    const n = Re(e), r = Reflect.getOwnPropertyDescriptor(n, t);
    return r && {
      writable: !0,
      configurable: e.type_ !== 1 || t !== "length",
      enumerable: r.enumerable,
      value: n[t]
    };
  },
  defineProperty() {
    pe(11);
  },
  getPrototypeOf(e) {
    return Ve(e.base_);
  },
  setPrototypeOf() {
    pe(12);
  }
}, tt = {};
St(Rn, (e, t) => {
  tt[e] = function() {
    return arguments[0] = arguments[0][0], t.apply(this, arguments);
  };
});
tt.deleteProperty = function(e, t) {
  return tt.set.call(this, e, t, void 0);
};
tt.set = function(e, t, n) {
  return Rn.set.call(this, e[0], t, n, e[0]);
};
function en(e, t) {
  const n = e[se];
  return (n ? Re(n) : e)[t];
}
function dl(e, t, n) {
  var o;
  const r = bo(t, n);
  return r ? "value" in r ? r.value : (
    // This is a very special case, if the prop is a getter defined by the
    // prototype, we should invoke it with the draft as context!
    (o = r.get) == null ? void 0 : o.call(e.draft_)
  ) : void 0;
}
function bo(e, t) {
  if (!(t in e)) return;
  let n = Ve(e);
  for (; n; ) {
    const r = Object.getOwnPropertyDescriptor(n, t);
    if (r) return r;
    n = Ve(n);
  }
}
function yn(e) {
  e.modified_ || (e.modified_ = !0, e.parent_ && yn(e.parent_));
}
function tn(e) {
  e.copy_ || (e.copy_ = pn(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var ml = class {
  constructor(e) {
    this.autoFreeze_ = !0, this.useStrictShallowCopy_ = !1, this.produce = (t, n, r) => {
      if (typeof t == "function" && typeof n != "function") {
        const i = n;
        n = t;
        const s = this;
        return function(l = i, ...u) {
          return s.produce(l, (f) => n.call(this, f, ...u));
        };
      }
      typeof n != "function" && pe(6), r !== void 0 && typeof r != "function" && pe(7);
      let o;
      if (Me(t)) {
        const i = br(this), s = vn(t, void 0);
        let a = !0;
        try {
          o = n(s), a = !1;
        } finally {
          a ? gn(i) : hn(i);
        }
        return vr(i, r), Sr(o, i);
      } else if (!t || typeof t != "object") {
        if (o = n(t), o === void 0 && (o = t), o === go && (o = void 0), this.autoFreeze_ && Pn(o, !0), r) {
          const i = [], s = [];
          Le("Patches").generateReplacementPatches_(t, o, i, s), r(i, s);
        }
        return o;
      } else pe(1, t);
    }, this.produceWithPatches = (t, n) => {
      if (typeof t == "function")
        return (s, ...a) => this.produceWithPatches(s, (l) => t(l, ...a));
      let r, o;
      return [this.produce(t, n, (s, a) => {
        r = s, o = a;
      }), r, o];
    }, typeof (e == null ? void 0 : e.autoFreeze) == "boolean" && this.setAutoFreeze(e.autoFreeze), typeof (e == null ? void 0 : e.useStrictShallowCopy) == "boolean" && this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    Me(e) || pe(8), We(e) && (e = pl(e));
    const t = br(this), n = vn(e, void 0);
    return n[se].isManual_ = !0, hn(t), n;
  }
  finishDraft(e, t) {
    const n = e && e[se];
    (!n || !n.isManual_) && pe(9);
    const {
      scope_: r
    } = n;
    return vr(r, t), Sr(void 0, r);
  }
  /**
   * Pass true to automatically freeze all copies created by Immer.
   *
   * By default, auto-freezing is enabled.
   */
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  /**
   * Pass true to enable strict shallow copy.
   *
   * By default, immer does not copy the object descriptors such as getter, setter and non-enumrable properties.
   */
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, t) {
    let n;
    for (n = t.length - 1; n >= 0; n--) {
      const o = t[n];
      if (o.path.length === 0 && o.op === "replace") {
        e = o.value;
        break;
      }
    }
    n > -1 && (t = t.slice(n + 1));
    const r = Le("Patches").applyPatches_;
    return We(e) ? r(e, t) : this.produce(e, (o) => r(o, t));
  }
};
function vn(e, t) {
  const n = Dt(e) ? Le("MapSet").proxyMap_(e, t) : Ht(e) ? Le("MapSet").proxySet_(e, t) : fl(e, t);
  return (t ? t.scope_ : vo()).drafts_.push(n), n;
}
function pl(e) {
  return We(e) || pe(10, e), So(e);
}
function So(e) {
  if (!Me(e) || Bt(e)) return e;
  const t = e[se];
  let n;
  if (t) {
    if (!t.modified_) return t.base_;
    t.finalized_ = !0, n = pn(e, t.scope_.immer_.useStrictShallowCopy_);
  } else
    n = pn(e, !0);
  return St(n, (r, o) => {
    yo(n, r, So(o));
  }), t && (t.finalized_ = !1), n;
}
var ae = new ml(), wr = ae.produce;
ae.produceWithPatches.bind(ae);
ae.setAutoFreeze.bind(ae);
ae.setUseStrictShallowCopy.bind(ae);
ae.applyPatches.bind(ae);
ae.createDraft.bind(ae);
ae.finishDraft.bind(ae);
const {
  useItems: Zl,
  withItemsContextProvider: Jl,
  ItemHandler: ec
} = Mr("antdx-bubble.list-items"), {
  useItems: gl,
  withItemsContextProvider: hl,
  ItemHandler: tc
} = Mr("antdx-bubble.list-roles");
function yl(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function vl(e, t = !1) {
  try {
    if (xn(e))
      return e;
    if (t && !yl(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function bl(e, t) {
  return he(() => vl(e, t), [e, t]);
}
function Sl(e, t) {
  return t((r, o) => xn(r) ? o ? (...i) => r(...i, ...e) : r(...e) : r);
}
const xl = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function wl(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return t[n] = _l(n, r), t;
  }, {}) : {};
}
function _l(e, t) {
  return typeof t == "number" && !xl.includes(e) ? t + "px" : t;
}
function bn(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const o = c.Children.toArray(e._reactElement.props.children).map((i) => {
      if (c.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = bn(i.props.el);
        return c.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...c.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(yt(c.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, s, l);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const i = r[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = bn(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Cl(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const _r = Ro(({
  slot: e,
  clone: t,
  className: n,
  style: r,
  observeAttributes: o
}, i) => {
  const s = J(), [a, l] = Ye([]), {
    forceClone: u
  } = li(), f = u ? !0 : t;
  return we(() => {
    var g;
    if (!s.current || !e)
      return;
    let m = e;
    function d() {
      let p = m;
      if (m.tagName.toLowerCase() === "svelte-slot" && m.children.length === 1 && m.children[0] && (p = m.children[0], p.tagName.toLowerCase() === "react-portal-target" && p.children[0] && (p = p.children[0])), Cl(i, p), n && p.classList.add(...n.split(" ")), r) {
        const v = wl(r);
        Object.keys(v).forEach((_) => {
          p.style[_] = v[_];
        });
      }
    }
    let h = null, y = null;
    if (f && window.MutationObserver) {
      let p = function() {
        var $, C, b;
        ($ = s.current) != null && $.contains(m) && ((C = s.current) == null || C.removeChild(m));
        const {
          portals: _,
          clonedElement: T
        } = bn(e);
        m = T, l(_), m.style.display = "contents", y && clearTimeout(y), y = setTimeout(() => {
          d();
        }, 50), (b = s.current) == null || b.appendChild(m);
      };
      p();
      const v = _i(() => {
        p(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0
          // attributes: observeAttributes ?? (forceClone ? true : false),
        });
      }, 50);
      h = new window.MutationObserver(v), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      m.style.display = "contents", d(), (g = s.current) == null || g.appendChild(m);
    return () => {
      var p, v;
      m.style.display = "", (p = s.current) != null && p.contains(m) && ((v = s.current) == null || v.removeChild(m)), h == null || h.disconnect();
    };
  }, [e, f, n, r, i, o, u]), c.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), El = ({
  children: e,
  ...t
}) => /* @__PURE__ */ S.jsx(S.Fragment, {
  children: e(t)
});
function Tl(e) {
  return c.createElement(El, {
    children: e
  });
}
function xo(e, t, n) {
  const r = e.filter(Boolean);
  if (r.length !== 0)
    return r.map((o, i) => {
      var u;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const s = {
        ...o.props,
        key: ((u = o.props) == null ? void 0 : u.key) ?? (n ? `${n}-${i}` : `${i}`)
      };
      let a = s;
      Object.keys(o.slots).forEach((f) => {
        if (!o.slots[f] || !(o.slots[f] instanceof Element) && !o.slots[f].el)
          return;
        const m = f.split(".");
        m.forEach((v, _) => {
          a[v] || (a[v] = {}), _ !== m.length - 1 && (a = s[v]);
        });
        const d = o.slots[f];
        let h, y, g = (t == null ? void 0 : t.clone) ?? !1, p = t == null ? void 0 : t.forceClone;
        d instanceof Element ? h = d : (h = d.el, y = d.callback, g = d.clone ?? g, p = d.forceClone ?? p), p = p ?? !!y, a[m[m.length - 1]] = h ? y ? (...v) => (y(m[m.length - 1], v), /* @__PURE__ */ S.jsx(jn, {
          ...o.ctx,
          params: v,
          forceClone: p,
          children: /* @__PURE__ */ S.jsx(_r, {
            slot: h,
            clone: g
          })
        })) : Tl((v) => /* @__PURE__ */ S.jsx(jn, {
          ...o.ctx,
          forceClone: p,
          children: /* @__PURE__ */ S.jsx(_r, {
            ...v,
            slot: h,
            clone: g
          })
        })) : a[m[m.length - 1]], a = s;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return o[l] ? s[l] = xo(o[l], t, `${i}`) : t != null && t.children && (s[l] = void 0, Reflect.deleteProperty(s, l)), s;
    });
}
const wo = Symbol();
function $l(e, t) {
  return Sl(t, (n) => {
    var r, o;
    return {
      ...e,
      avatar: xn(e.avatar) ? n(e.avatar) : be(e.avatar) ? {
        ...e.avatar,
        icon: n((r = e.avatar) == null ? void 0 : r.icon),
        src: n((o = e.avatar) == null ? void 0 : o.src)
      } : e.avatar,
      footer: n(e.footer),
      header: n(e.header),
      loadingRender: n(e.loadingRender, !0),
      messageRender: n(e.messageRender, !0)
    };
  });
}
function Pl({
  roles: e,
  preProcess: t,
  postProcess: n
}, r = []) {
  const o = bl(e), i = re(t), s = re(n), {
    items: {
      roles: a
    }
  } = gl(), l = he(() => {
    var f;
    return e || ((f = xo(a, {
      clone: !0,
      forceClone: !0
    })) == null ? void 0 : f.reduce((m, d) => (d.role !== void 0 && (m[d.role] = d), m), {}));
  }, [a, e]), u = he(() => (f, m) => {
    const d = m ?? f[wo], h = i(f, d) || f;
    if (h.role && (l || {})[h.role])
      return $l((l || {})[h.role], [h, d]);
    let y;
    return y = s(h, d), y || {
      messageRender(g) {
        return /* @__PURE__ */ S.jsx(S.Fragment, {
          children: be(g) ? JSON.stringify(g) : g
        });
      }
    };
  }, [l, s, i, ...r]);
  return o || u;
}
function Rl(e) {
  const [t, n] = Ye(!1), r = J(0), o = J(!0), i = J(!0), {
    autoScroll: s,
    scrollButtonOffset: a,
    ref: l,
    value: u
  } = e, f = re((d = "instant") => {
    l.current && (i.current = !0, l.current.scrollTo({
      offset: l.current.nativeElement.scrollHeight,
      behavior: d
    }), n(!1));
  }), m = re((d = 100) => {
    if (!l.current)
      return !1;
    const h = l.current.nativeElement, y = h.scrollHeight, {
      scrollTop: g,
      clientHeight: p
    } = h;
    return y - (g + p) < d;
  });
  return we(() => {
    l.current && s && u.length && (u.length !== r.current && (o.current = !0), o.current && requestAnimationFrame(() => {
      f();
    }), r.current = u.length);
  }, [u, l, s, f, m]), we(() => {
    if (l.current && s) {
      const d = l.current.nativeElement;
      let h = 0, y = 0;
      const g = (p) => {
        const v = p.target;
        i.current ? i.current = !1 : v.scrollTop < h && v.scrollHeight >= y ? o.current = !1 : m() && (o.current = !0), h = v.scrollTop, y = v.scrollHeight, n(!m(a));
      };
      return d.addEventListener("scroll", g), () => {
        d.removeEventListener("scroll", g);
      };
    }
  }, [s, m, a]), {
    showScrollButton: t,
    scrollToBottom: f
  };
}
new Intl.Collator(0, {
  numeric: 1
}).compare;
typeof process < "u" && process.versions && process.versions.node;
var xe;
class nc extends TransformStream {
  /** Constructs a new instance. */
  constructor(n = {
    allowCR: !1
  }) {
    super({
      transform: (r, o) => {
        for (r = Ae(this, xe) + r; ; ) {
          const i = r.indexOf(`
`), s = n.allowCR ? r.indexOf("\r") : -1;
          if (s !== -1 && s !== r.length - 1 && (i === -1 || i - 1 > s)) {
            o.enqueue(r.slice(0, s)), r = r.slice(s + 1);
            continue;
          }
          if (i === -1) break;
          const a = r[i - 1] === "\r" ? i - 1 : i;
          o.enqueue(r.slice(0, a)), r = r.slice(i + 1);
        }
        Nn(this, xe, r);
      },
      flush: (r) => {
        if (Ae(this, xe) === "") return;
        const o = n.allowCR && Ae(this, xe).endsWith("\r") ? Ae(this, xe).slice(0, -1) : Ae(this, xe);
        r.enqueue(o);
      }
    });
    Ln(this, xe, "");
  }
}
xe = new WeakMap();
function Il(e) {
  try {
    const t = new URL(e);
    return t.protocol === "http:" || t.protocol === "https:";
  } catch {
    return !1;
  }
}
function Ml() {
  const e = document.querySelector(".gradio-container");
  if (!e)
    return "";
  const t = e.className.match(/gradio-container-(.+)/);
  return t ? t[1] : "";
}
const Ll = +Ml()[0];
function Sn(e, t, n) {
  const r = Ll >= 5 ? "gradio_api/" : "";
  return e == null ? n ? `/proxy=${n}${r}file=` : `${t}${r}file=` : Il(e) ? e : n ? `/proxy=${n}${r}file=${e}` : `${t}/${r}file=${e}`;
}
const Nl = (e) => !!e.url;
function _o(e, t, n) {
  if (e)
    return Nl(e) ? e.url : typeof e == "string" ? e.startsWith("http") ? e : Sn(e, t, n) : e;
}
const Ol = ({
  options: e,
  urlProxyUrl: t,
  urlRoot: n,
  onWelcomePromptSelect: r
}) => {
  var a;
  const {
    prompts: o,
    ...i
  } = e, s = he(() => ye(o || {}, {
    omitNull: !0
  }), [o]);
  return /* @__PURE__ */ S.jsxs(_e, {
    vertical: !0,
    gap: "middle",
    children: [/* @__PURE__ */ S.jsx(ol, {
      ...i,
      icon: _o(i.icon, n, t),
      styles: {
        ...i == null ? void 0 : i.styles,
        icon: {
          flexShrink: 0,
          ...(a = i == null ? void 0 : i.styles) == null ? void 0 : a.icon
        }
      },
      classNames: i.class_names,
      className: k(i.elem_classes),
      style: i.elem_style
    }), /* @__PURE__ */ S.jsx($n, {
      ...s,
      classNames: s == null ? void 0 : s.class_names,
      className: k(s == null ? void 0 : s.elem_classes),
      style: s == null ? void 0 : s.elem_style,
      onItemClick: ({
        data: l
      }) => {
        r({
          value: l
        });
      }
    })]
  });
}, Cr = Symbol(), Er = Symbol(), Tr = Symbol(), $r = Symbol(), Fl = (e) => e ? typeof e == "string" ? {
  src: e
} : ((n) => !!n.url)(e) ? {
  src: e.url
} : e.src ? {
  ...e,
  src: typeof e.src == "string" ? e.src : e.src.url
} : e : void 0, jl = (e) => typeof e == "string" ? [{
  type: "text",
  content: e
}] : Array.isArray(e) ? e.map((t) => typeof t == "string" ? {
  type: "text",
  content: t
} : t) : be(e) ? [e] : [], kl = (e, t) => {
  if (typeof e == "string")
    return t[0];
  if (Array.isArray(e)) {
    const n = [...e];
    return Object.keys(t).forEach((r) => {
      const o = n[r];
      typeof o == "string" ? n[r] = t[r] : n[r] = {
        ...o,
        content: t[r]
      };
    }), n;
  }
  return be(e) ? {
    ...e,
    content: t[0]
  } : e;
}, Co = (e, t, n) => typeof e == "string" ? e : Array.isArray(e) ? e.map((r) => Co(r, t, n)).filter(Boolean).join(`
`) : be(e) ? e.copyable ?? !0 ? typeof e.content == "string" ? e.content : e.type === "file" ? JSON.stringify(e.content.map((r) => _o(r, t, n))) : JSON.stringify(e.content) : "" : JSON.stringify(e), Eo = (e, t) => (e || []).map((n) => ({
  ...t(n),
  children: Array.isArray(n.children) ? Eo(n.children, t) : void 0
})), Al = ({
  content: e,
  className: t,
  style: n,
  disabled: r,
  urlRoot: o,
  urlProxyUrl: i,
  onCopy: s
}) => {
  const a = he(() => Co(e, o, i), [e, i, o]), l = J(null);
  return /* @__PURE__ */ S.jsx(Te.Text, {
    copyable: {
      tooltips: !1,
      onCopy() {
        s == null || s(a);
      },
      text: a,
      icon: [/* @__PURE__ */ S.jsx(oe, {
        ref: l,
        variant: "text",
        color: "default",
        disabled: r,
        size: "small",
        className: t,
        style: n,
        icon: /* @__PURE__ */ S.jsx(Zo, {})
      }, "copy"), /* @__PURE__ */ S.jsx(oe, {
        variant: "text",
        color: "default",
        size: "small",
        disabled: r,
        className: t,
        style: n,
        icon: /* @__PURE__ */ S.jsx(Rr, {})
      }, "copied")]
    }
  });
}, zl = ({
  action: e,
  disabledActions: t,
  message: n,
  onCopy: r,
  onDelete: o,
  onEdit: i,
  onLike: s,
  onRetry: a,
  urlRoot: l,
  urlProxyUrl: u
}) => {
  var h;
  const f = J(), d = (() => {
    var v, _;
    const {
      action: y,
      disabled: g,
      disableHandler: p
    } = be(e) ? {
      action: e.action,
      disabled: (t == null ? void 0 : t.includes(e.action)) || !!e.disabled,
      disableHandler: !!e.popconfirm
    } : {
      action: e,
      disabled: (t == null ? void 0 : t.includes(e)) || !1,
      disableHandler: !1
    };
    switch (y) {
      case "copy":
        return /* @__PURE__ */ S.jsx(Al, {
          disabled: g,
          content: n.content,
          onCopy: r,
          urlRoot: l,
          urlProxyUrl: u
        });
      case "like":
        return f.current = () => s(!0), /* @__PURE__ */ S.jsx(oe, {
          variant: "text",
          color: ((v = n.meta) == null ? void 0 : v.feedback) === "like" ? "primary" : "default",
          disabled: g,
          size: "small",
          icon: /* @__PURE__ */ S.jsx(Qo, {}),
          onClick: () => {
            !p && s(!0);
          }
        });
      case "dislike":
        return f.current = () => s(!1), /* @__PURE__ */ S.jsx(oe, {
          variant: "text",
          color: ((_ = n.meta) == null ? void 0 : _.feedback) === "dislike" ? "primary" : "default",
          size: "small",
          icon: /* @__PURE__ */ S.jsx(Yo, {}),
          disabled: g,
          onClick: () => !p && s(!1)
        });
      case "retry":
        return f.current = a, /* @__PURE__ */ S.jsx(oe, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(qo, {}),
          onClick: () => !p && a()
        });
      case "edit":
        return f.current = i, /* @__PURE__ */ S.jsx(oe, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(Ko, {}),
          onClick: () => !p && i()
        });
      case "delete":
        return f.current = o, /* @__PURE__ */ S.jsx(oe, {
          variant: "text",
          color: "default",
          size: "small",
          disabled: g,
          icon: /* @__PURE__ */ S.jsx(Go, {}),
          onClick: () => !p && o()
        });
      default:
        return null;
    }
  })();
  if (be(e)) {
    const y = {
      ...typeof e.popconfirm == "string" ? {
        title: e.popconfirm
      } : {
        ...e.popconfirm,
        title: (h = e.popconfirm) == null ? void 0 : h.title
      },
      onConfirm() {
        var g;
        (g = f.current) == null || g.call(f);
      }
    };
    return c.createElement(e.popconfirm ? oi : c.Fragment, e.popconfirm ? y : void 0, c.createElement(e.tooltip ? ii : c.Fragment, e.tooltip ? typeof e.tooltip == "string" ? {
      title: e.tooltip
    } : e.tooltip : void 0, d));
  }
  return d;
}, Dl = ({
  isEditing: e,
  onEditCancel: t,
  onEditConfirm: n,
  onCopy: r,
  onEdit: o,
  onLike: i,
  onDelete: s,
  onRetry: a,
  editValues: l,
  message: u,
  extra: f,
  index: m,
  actions: d,
  disabledActions: h,
  urlRoot: y,
  urlProxyUrl: g
}) => e ? /* @__PURE__ */ S.jsxs(_e, {
  justify: "end",
  children: [/* @__PURE__ */ S.jsx(oe, {
    variant: "text",
    color: "default",
    size: "small",
    icon: /* @__PURE__ */ S.jsx(Uo, {}),
    onClick: () => {
      t == null || t();
    }
  }), /* @__PURE__ */ S.jsx(oe, {
    variant: "text",
    color: "default",
    size: "small",
    icon: /* @__PURE__ */ S.jsx(Rr, {}),
    onClick: () => {
      const p = kl(u.content, l);
      n == null || n({
        index: m,
        value: p,
        previous_value: u.content
      });
    }
  })]
}) : /* @__PURE__ */ S.jsx(_e, {
  justify: "space-between",
  align: "center",
  gap: f && (d != null && d.length) ? "small" : void 0,
  children: (u.role === "user" ? ["extra", "actions"] : ["actions", "extra"]).map((p) => {
    switch (p) {
      case "extra":
        return /* @__PURE__ */ S.jsx(Te.Text, {
          type: "secondary",
          children: f
        }, "extra");
      case "actions":
        return /* @__PURE__ */ S.jsx("div", {
          children: (d || []).map((v, _) => /* @__PURE__ */ S.jsx(zl, {
            urlRoot: y,
            urlProxyUrl: g,
            action: v,
            disabledActions: h,
            message: u,
            onCopy: (T) => r({
              value: T,
              index: m
            }),
            onDelete: () => s({
              index: m,
              value: u.content
            }),
            onEdit: () => o(m),
            onLike: (T) => i == null ? void 0 : i({
              value: u.content,
              liked: T,
              index: m
            }),
            onRetry: () => a == null ? void 0 : a({
              index: m,
              value: u.content
            })
          }, `${v}-${_}`))
        }, "actions");
    }
  })
}), Hl = ({
  markdownConfig: e,
  title: t
}) => t ? e.renderMarkdown ? /* @__PURE__ */ S.jsx(vt, {
  ...e,
  value: t
}) : /* @__PURE__ */ S.jsx(S.Fragment, {
  children: t
}) : null, Bl = (e, t, n) => e ? typeof e == "string" ? {
  url: e.startsWith("http") ? e : Sn(e, t, n),
  uid: e,
  name: e.split("/").pop()
} : {
  ...e,
  uid: e.uid || e.path || e.url,
  name: e.name || e.orig_name || (e.url || e.path).split("/").pop(),
  url: e.url || Sn(e.path, t, n)
} : {}, Vl = ({
  children: e,
  item: t
}) => {
  const {
    token: n
  } = Qe.useToken();
  return /* @__PURE__ */ S.jsxs("div", {
    className: "ms-gr-pro-chatbot-message-file-message-container",
    children: [e, /* @__PURE__ */ S.jsx("div", {
      className: "ms-gr-pro-chatbot-message-file-message-toolbar",
      style: {
        backgroundColor: n.colorBgMask,
        zIndex: n.zIndexPopupBase,
        borderRadius: n.borderRadius
      },
      children: /* @__PURE__ */ S.jsx(oe, {
        icon: /* @__PURE__ */ S.jsx(Jo, {
          style: {
            color: n.colorWhite
          }
        }),
        variant: "link",
        color: "default",
        size: "small",
        href: t.url,
        target: "_blank",
        rel: "noopener noreferrer"
      })
    })]
  });
}, Wl = ({
  value: e,
  urlProxyUrl: t,
  urlRoot: n,
  options: r
}) => /* @__PURE__ */ S.jsx(_e, {
  gap: "small",
  wrap: !0,
  ...r,
  className: "ms-gr-pro-chatbot-message-file-message",
  children: e == null ? void 0 : e.map((o, i) => {
    const s = Bl(o, n, t);
    return /* @__PURE__ */ S.jsx(Vl, {
      item: s,
      children: /* @__PURE__ */ S.jsx(fo.FileCard, {
        item: s
      })
    }, `${s.uid}-${i}`);
  })
}), Xl = ({
  value: e,
  options: t,
  onItemClick: n
}) => {
  const {
    elem_style: r,
    elem_classes: o,
    class_names: i,
    styles: s,
    ...a
  } = t;
  return /* @__PURE__ */ S.jsx($n, {
    ...a,
    classNames: i,
    className: k(o),
    style: r,
    styles: s,
    items: e,
    onItemClick: ({
      data: l
    }) => {
      n(l);
    }
  });
}, Pr = ({
  value: e,
  options: t
}) => {
  const {
    renderMarkdown: n,
    ...r
  } = t;
  return /* @__PURE__ */ S.jsx(S.Fragment, {
    children: n ? /* @__PURE__ */ S.jsx(vt, {
      ...r,
      value: e
    }) : e
  });
}, Ul = ({
  value: e,
  options: t
}) => {
  const {
    renderMarkdown: n,
    status: r,
    title: o,
    ...i
  } = t, [s, a] = Ye(() => r !== "done");
  return we(() => {
    a(r !== "done");
  }, [r]), /* @__PURE__ */ S.jsx(S.Fragment, {
    children: /* @__PURE__ */ S.jsx(si, {
      activeKey: s ? ["tool"] : [],
      onChange: () => {
        a(!s);
      },
      items: [{
        key: "tool",
        label: n ? /* @__PURE__ */ S.jsx(vt, {
          ...i,
          value: o
        }) : o,
        children: n ? /* @__PURE__ */ S.jsx(vt, {
          ...i,
          value: e
        }) : e
      }]
    })
  });
}, Gl = ["text", "tool"], Kl = ({
  isEditing: e,
  index: t,
  message: n,
  isLastMessage: r,
  markdownConfig: o,
  onEdit: i,
  onSuggestionSelect: s,
  urlProxyUrl: a,
  urlRoot: l
}) => {
  const u = J(null), f = () => jl(n.content).map((d, h) => {
    const y = () => {
      var g;
      if (e && (d.editable ?? !0) && Gl.includes(d.type)) {
        const p = d.content, v = (g = u.current) == null ? void 0 : g.getBoundingClientRect().width;
        return /* @__PURE__ */ S.jsx("div", {
          style: {
            width: v,
            minWidth: 200,
            maxWidth: "100%"
          },
          children: /* @__PURE__ */ S.jsx(ai.TextArea, {
            autoSize: {
              minRows: 1,
              maxRows: 10
            },
            defaultValue: p,
            onChange: (_) => {
              i(h, _.target.value);
            }
          })
        });
      }
      switch (d.type) {
        case "text":
          return /* @__PURE__ */ S.jsx(Pr, {
            value: d.content,
            options: ye({
              ...o,
              ...pt(d.options)
            }, {
              omitNull: !0
            })
          });
        case "tool":
          return /* @__PURE__ */ S.jsx(Ul, {
            value: d.content,
            options: ye({
              ...o,
              ...pt(d.options)
            }, {
              omitNull: !0
            })
          });
        case "file":
          return /* @__PURE__ */ S.jsx(Wl, {
            value: d.content,
            urlRoot: l,
            urlProxyUrl: a,
            options: ye(d.options || {}, {
              omitNull: !0
            })
          });
        case "suggestion":
          return /* @__PURE__ */ S.jsx(Xl, {
            value: r ? d.content : Eo(d.content, (p) => ({
              ...p,
              disabled: p.disabled ?? !0
            })),
            options: ye(d.options || {}, {
              omitNull: !0
            }),
            onItemClick: (p) => {
              s({
                index: t,
                value: p
              });
            }
          });
        default:
          return typeof d.content != "string" ? null : /* @__PURE__ */ S.jsx(Pr, {
            value: d.content,
            options: ye({
              ...o,
              ...pt(d.options)
            }, {
              omitNull: !0
            })
          });
      }
    };
    return /* @__PURE__ */ S.jsx(c.Fragment, {
      children: y()
    }, h);
  });
  return /* @__PURE__ */ S.jsx("div", {
    ref: u,
    children: /* @__PURE__ */ S.jsx(_e, {
      vertical: !0,
      gap: "small",
      children: f()
    })
  });
}, rc = Yi(hl(["roles"], ({
  id: e,
  className: t,
  style: n,
  height: r,
  minHeight: o,
  maxHeight: i,
  value: s,
  roles: a,
  urlRoot: l,
  urlProxyUrl: u,
  themeMode: f,
  autoScroll: m = !0,
  showScrollToBottomButton: d = !0,
  scrollToBottomButtonOffset: h = 200,
  markdownConfig: y,
  welcomeConfig: g,
  userConfig: p,
  botConfig: v,
  onValueChange: _,
  onCopy: T,
  onChange: $,
  onEdit: C,
  onRetry: b,
  onDelete: w,
  onLike: R,
  onSuggestionSelect: L,
  onWelcomePromptSelect: O
}) => {
  const A = he(() => ({
    variant: "borderless",
    ...g ? ye(g, {
      omitNull: !0
    }) : {}
  }), [g]), F = he(() => ({
    lineBreaks: !0,
    renderMarkdown: !0,
    ...pt(y),
    urlRoot: l,
    themeMode: f
  }), [y, f, l]), P = he(() => p ? ye(p, {
    omitNull: !0
  }) : {}, [p]), x = he(() => v ? ye(v, {
    omitNull: !0
  }) : {}, [v]), I = he(() => {
    const E = (s || []).map((G, X) => {
      const de = X === s.length - 1, le = ye(G, {
        omitNull: !0
      });
      return {
        ...Fn(le, ["header", "footer", "avatar"]),
        [wo]: X,
        [Cr]: le.header,
        [Er]: le.footer,
        [Tr]: le.avatar,
        [$r]: de,
        key: le.key ?? `${X}`
      };
    }).filter((G) => G.role !== "system");
    return E.length > 0 ? E : [{
      role: "chatbot-internal-welcome"
    }];
  }, [s]), N = J(null), [V, W] = Ye(-1), [Y, H] = Ye({}), z = J(), K = re((E, G) => {
    H((X) => ({
      ...X,
      [E]: G
    }));
  }), Q = re($);
  we(() => {
    Ci(z.current, s) || (Q(), z.current = s);
  }, [s, Q]);
  const U = re((E) => {
    L == null || L(E);
  }), ie = re((E) => {
    O == null || O(E);
  }), Ne = re((E) => {
    b == null || b(E);
  }), fe = re((E) => {
    W(E);
  }), Ke = re(() => {
    W(-1);
  }), Oe = re((E) => {
    W(-1), _([...s.slice(0, E.index), {
      ...s[E.index],
      content: E.value
    }, ...s.slice(E.index + 1)]), C == null || C(E);
  }), Fe = re((E) => {
    T == null || T(E);
  }), je = re((E) => {
    R == null || R(E), _(wr(s, (G) => {
      const X = G[E.index].meta || {}, de = E.liked ? "like" : "dislike";
      G[E.index] = {
        ...G[E.index],
        meta: {
          ...X,
          feedback: X.feedback === de ? null : de
        }
      };
    }));
  }), Se = re((E) => {
    _(wr(s, (G) => {
      G.splice(E.index, 1);
    })), w == null || w(E);
  }), ke = Pl({
    roles: a,
    preProcess(E, G) {
      var X, de, le, Z;
      return {
        ...E,
        style: E.elem_style,
        className: k(E.elem_classes, "ms-gr-pro-chatbot-message"),
        classNames: {
          ...E.class_names,
          avatar: k((X = E.class_names) == null ? void 0 : X.avatar, "ms-gr-pro-chatbot-message-avatar"),
          header: k((de = E.class_names) == null ? void 0 : de.header, "ms-gr-pro-chatbot-message-header"),
          footer: k((le = E.class_names) == null ? void 0 : le.footer, "ms-gr-pro-chatbot-message-footer", G === V ? "ms-gr-pro-chatbot-message-footer-editing" : void 0),
          content: k((Z = E.class_names) == null ? void 0 : Z.content, "ms-gr-pro-chatbot-message-content")
        }
      };
    },
    postProcess(E, G) {
      const X = E.role === "user";
      switch (E.role) {
        case "chatbot-internal-welcome":
          return {
            variant: "borderless",
            styles: {
              content: {
                width: "100%"
              }
            },
            messageRender() {
              return /* @__PURE__ */ S.jsx(Ol, {
                urlRoot: l,
                urlProxyUrl: u,
                options: A || {},
                onWelcomePromptSelect: ie
              });
            }
          };
        case "user":
        case "assistant":
          return {
            ...Fn(X ? P : x, ["actions", "avatar", "header"]),
            ...E,
            style: {
              ...X ? P == null ? void 0 : P.style : x == null ? void 0 : x.style,
              ...E.style
            },
            className: k(E.className, X ? P == null ? void 0 : P.elem_classes : x == null ? void 0 : x.elem_classes),
            header: /* @__PURE__ */ S.jsx(Hl, {
              title: E[Cr] ?? (X ? P == null ? void 0 : P.header : x == null ? void 0 : x.header),
              markdownConfig: F
            }),
            avatar: Fl(E[Tr] ?? (X ? P == null ? void 0 : P.avatar : x == null ? void 0 : x.avatar)),
            footer: (
              // bubbleProps[lastMessageSymbol] &&
              E.loading || E.status === "pending" ? null : /* @__PURE__ */ S.jsx(Dl, {
                isEditing: V === G,
                message: E,
                extra: E[Er] ?? (X ? P == null ? void 0 : P.footer : x == null ? void 0 : x.footer),
                urlRoot: l,
                urlProxyUrl: u,
                editValues: Y,
                index: G,
                actions: E.actions ?? (X ? (P == null ? void 0 : P.actions) || [] : (x == null ? void 0 : x.actions) || []),
                disabledActions: E.disabled_actions ?? (X ? (P == null ? void 0 : P.disabled_actions) || [] : (x == null ? void 0 : x.disabled_actions) || []),
                onEditCancel: Ke,
                onEditConfirm: Oe,
                onCopy: Fe,
                onEdit: fe,
                onDelete: Se,
                onRetry: Ne,
                onLike: je
              })
            ),
            messageRender() {
              return /* @__PURE__ */ S.jsx(Kl, {
                index: G,
                urlProxyUrl: u,
                urlRoot: l,
                isEditing: V === G,
                message: E,
                isLastMessage: E[$r] || !1,
                markdownConfig: F,
                onEdit: K,
                onSuggestionSelect: U
              });
            }
          };
        default:
          return;
      }
    }
  }, [V, P, A, x, F, Y]), {
    scrollToBottom: rt,
    showScrollButton: Vt
  } = Rl({
    ref: N,
    value: s,
    autoScroll: m,
    scrollButtonOffset: h
  });
  return /* @__PURE__ */ S.jsxs("div", {
    id: e,
    className: k(t, "ms-gr-pro-chatbot"),
    style: {
      height: r,
      minHeight: o,
      maxHeight: i,
      ...n
    },
    children: [/* @__PURE__ */ S.jsx(Tn.List, {
      ref: N,
      className: "ms-gr-pro-chatbot-messages",
      autoScroll: !1,
      roles: ke,
      items: I
    }), d && Vt && /* @__PURE__ */ S.jsx("div", {
      className: "ms-gr-pro-chatbot-scroll-to-bottom-button",
      children: /* @__PURE__ */ S.jsx(oe, {
        icon: /* @__PURE__ */ S.jsx(ei, {}),
        shape: "circle",
        variant: "outlined",
        color: "primary",
        onClick: () => rt("smooth")
      })
    })]
  });
}));
export {
  rc as Chatbot,
  rc as default
};
