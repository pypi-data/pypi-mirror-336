import { i as Xr, a as zt, r as Gr, b as qr, w as tt, g as Kr, c as Z, d as Yr, o as Zr } from "./Index-D29aGQay.js";
const R = window.ms_globals.React, h = window.ms_globals.React, jr = window.ms_globals.React.forwardRef, se = window.ms_globals.React.useRef, De = window.ms_globals.React.useState, ge = window.ms_globals.React.useEffect, Br = window.ms_globals.React.isValidElement, Hr = window.ms_globals.React.useLayoutEffect, zr = window.ms_globals.React.useImperativeHandle, Vr = window.ms_globals.React.memo, Ur = window.ms_globals.React.useCallback, un = window.ms_globals.React.useMemo, dn = window.ms_globals.ReactDOM, at = window.ms_globals.ReactDOM.createPortal, Qr = window.ms_globals.internalContext.useContextPropsContext, Jr = window.ms_globals.internalContext.useSuggestionOpenContext, ei = window.ms_globals.antdIcons.FileTextFilled, ti = window.ms_globals.antdIcons.CloseCircleFilled, ni = window.ms_globals.antdIcons.FileExcelFilled, ri = window.ms_globals.antdIcons.FileImageFilled, ii = window.ms_globals.antdIcons.FileMarkdownFilled, oi = window.ms_globals.antdIcons.FilePdfFilled, si = window.ms_globals.antdIcons.FilePptFilled, ai = window.ms_globals.antdIcons.FileWordFilled, li = window.ms_globals.antdIcons.FileZipFilled, ci = window.ms_globals.antdIcons.PlusOutlined, ui = window.ms_globals.antdIcons.LeftOutlined, di = window.ms_globals.antdIcons.RightOutlined, fi = window.ms_globals.antdIcons.CloseOutlined, hi = window.ms_globals.antdIcons.ClearOutlined, pi = window.ms_globals.antdIcons.ArrowUpOutlined, mi = window.ms_globals.antdIcons.AudioMutedOutlined, gi = window.ms_globals.antdIcons.AudioOutlined, vi = window.ms_globals.antdIcons.CloudUploadOutlined, bi = window.ms_globals.antdIcons.LinkOutlined, yi = window.ms_globals.antd.ConfigProvider, er = window.ms_globals.antd.Upload, lt = window.ms_globals.antd.theme, wi = window.ms_globals.antd.Progress, _e = window.ms_globals.antd.Button, tr = window.ms_globals.antd.Flex, Mt = window.ms_globals.antd.Typography, Si = window.ms_globals.antd.Input, xi = window.ms_globals.antd.Tooltip, Ci = window.ms_globals.antd.Badge, Vt = window.ms_globals.antdCssinjs.unit, Lt = window.ms_globals.antdCssinjs.token2CSSVar, fn = window.ms_globals.antdCssinjs.useStyleRegister, Ei = window.ms_globals.antdCssinjs.useCSSVarRegister, _i = window.ms_globals.antdCssinjs.createTheme, Ri = window.ms_globals.antdCssinjs.useCacheToken;
var Ti = /\s/;
function Pi(n) {
  for (var e = n.length; e-- && Ti.test(n.charAt(e)); )
    ;
  return e;
}
var Mi = /^\s+/;
function Li(n) {
  return n && n.slice(0, Pi(n) + 1).replace(Mi, "");
}
var hn = NaN, Oi = /^[-+]0x[0-9a-f]+$/i, Ai = /^0b[01]+$/i, $i = /^0o[0-7]+$/i, ki = parseInt;
function pn(n) {
  if (typeof n == "number")
    return n;
  if (Xr(n))
    return hn;
  if (zt(n)) {
    var e = typeof n.valueOf == "function" ? n.valueOf() : n;
    n = zt(e) ? e + "" : e;
  }
  if (typeof n != "string")
    return n === 0 ? n : +n;
  n = Li(n);
  var t = Ai.test(n);
  return t || $i.test(n) ? ki(n.slice(2), t ? 2 : 8) : Oi.test(n) ? hn : +n;
}
function Ii() {
}
var Ot = function() {
  return Gr.Date.now();
}, Di = "Expected a function", Ni = Math.max, Wi = Math.min;
function Fi(n, e, t) {
  var r, i, o, s, a, u, l = 0, c = !1, d = !1, f = !0;
  if (typeof n != "function")
    throw new TypeError(Di);
  e = pn(e) || 0, zt(t) && (c = !!t.leading, d = "maxWait" in t, o = d ? Ni(pn(t.maxWait) || 0, e) : o, f = "trailing" in t ? !!t.trailing : f);
  function m(C) {
    var E = r, T = i;
    return r = i = void 0, l = C, s = n.apply(T, E), s;
  }
  function v(C) {
    return l = C, a = setTimeout(y, e), c ? m(C) : s;
  }
  function g(C) {
    var E = C - u, T = C - l, I = e - E;
    return d ? Wi(I, o - T) : I;
  }
  function p(C) {
    var E = C - u, T = C - l;
    return u === void 0 || E >= e || E < 0 || d && T >= o;
  }
  function y() {
    var C = Ot();
    if (p(C))
      return S(C);
    a = setTimeout(y, g(C));
  }
  function S(C) {
    return a = void 0, f && r ? m(C) : (r = i = void 0, s);
  }
  function x() {
    a !== void 0 && clearTimeout(a), l = 0, r = u = i = a = void 0;
  }
  function b() {
    return a === void 0 ? s : S(Ot());
  }
  function _() {
    var C = Ot(), E = p(C);
    if (r = arguments, i = this, u = C, E) {
      if (a === void 0)
        return v(u);
      if (d)
        return clearTimeout(a), a = setTimeout(y, e), m(u);
    }
    return a === void 0 && (a = setTimeout(y, e)), s;
  }
  return _.cancel = x, _.flush = b, _;
}
function ji(n, e) {
  return qr(n, e);
}
var nr = {
  exports: {}
}, dt = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Bi = h, Hi = Symbol.for("react.element"), zi = Symbol.for("react.fragment"), Vi = Object.prototype.hasOwnProperty, Ui = Bi.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Xi = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function rr(n, e, t) {
  var r, i = {}, o = null, s = null;
  t !== void 0 && (o = "" + t), e.key !== void 0 && (o = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) Vi.call(e, r) && !Xi.hasOwnProperty(r) && (i[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) i[r] === void 0 && (i[r] = e[r]);
  return {
    $$typeof: Hi,
    type: n,
    key: o,
    ref: s,
    props: i,
    _owner: Ui.current
  };
}
dt.Fragment = zi;
dt.jsx = rr;
dt.jsxs = rr;
nr.exports = dt;
var oe = nr.exports;
const {
  SvelteComponent: Gi,
  assign: mn,
  binding_callbacks: gn,
  check_outros: qi,
  children: ir,
  claim_element: or,
  claim_space: Ki,
  component_subscribe: vn,
  compute_slots: Yi,
  create_slot: Zi,
  detach: xe,
  element: sr,
  empty: bn,
  exclude_internal_props: yn,
  get_all_dirty_from_scope: Qi,
  get_slot_changes: Ji,
  group_outros: eo,
  init: to,
  insert_hydration: nt,
  safe_not_equal: no,
  set_custom_element_data: ar,
  space: ro,
  transition_in: rt,
  transition_out: Ut,
  update_slot_base: io
} = window.__gradio__svelte__internal, {
  beforeUpdate: oo,
  getContext: so,
  onDestroy: ao,
  setContext: lo
} = window.__gradio__svelte__internal;
function wn(n) {
  let e, t;
  const r = (
    /*#slots*/
    n[7].default
  ), i = Zi(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = sr("svelte-slot"), i && i.c(), this.h();
    },
    l(o) {
      e = or(o, "SVELTE-SLOT", {
        class: !0
      });
      var s = ir(e);
      i && i.l(s), s.forEach(xe), this.h();
    },
    h() {
      ar(e, "class", "svelte-1rt0kpf");
    },
    m(o, s) {
      nt(o, e, s), i && i.m(e, null), n[9](e), t = !0;
    },
    p(o, s) {
      i && i.p && (!t || s & /*$$scope*/
      64) && io(
        i,
        r,
        o,
        /*$$scope*/
        o[6],
        t ? Ji(
          r,
          /*$$scope*/
          o[6],
          s,
          null
        ) : Qi(
          /*$$scope*/
          o[6]
        ),
        null
      );
    },
    i(o) {
      t || (rt(i, o), t = !0);
    },
    o(o) {
      Ut(i, o), t = !1;
    },
    d(o) {
      o && xe(e), i && i.d(o), n[9](null);
    }
  };
}
function co(n) {
  let e, t, r, i, o = (
    /*$$slots*/
    n[4].default && wn(n)
  );
  return {
    c() {
      e = sr("react-portal-target"), t = ro(), o && o.c(), r = bn(), this.h();
    },
    l(s) {
      e = or(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), ir(e).forEach(xe), t = Ki(s), o && o.l(s), r = bn(), this.h();
    },
    h() {
      ar(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      nt(s, e, a), n[8](e), nt(s, t, a), o && o.m(s, a), nt(s, r, a), i = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? o ? (o.p(s, a), a & /*$$slots*/
      16 && rt(o, 1)) : (o = wn(s), o.c(), rt(o, 1), o.m(r.parentNode, r)) : o && (eo(), Ut(o, 1, 1, () => {
        o = null;
      }), qi());
    },
    i(s) {
      i || (rt(o), i = !0);
    },
    o(s) {
      Ut(o), i = !1;
    },
    d(s) {
      s && (xe(e), xe(t), xe(r)), n[8](null), o && o.d(s);
    }
  };
}
function Sn(n) {
  const {
    svelteInit: e,
    ...t
  } = n;
  return t;
}
function uo(n, e, t) {
  let r, i, {
    $$slots: o = {},
    $$scope: s
  } = e;
  const a = Yi(o);
  let {
    svelteInit: u
  } = e;
  const l = tt(Sn(e)), c = tt();
  vn(n, c, (b) => t(0, r = b));
  const d = tt();
  vn(n, d, (b) => t(1, i = b));
  const f = [], m = so("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: g,
    subSlotIndex: p
  } = Kr() || {}, y = u({
    parent: m,
    props: l,
    target: c,
    slot: d,
    slotKey: v,
    slotIndex: g,
    subSlotIndex: p,
    onDestroy(b) {
      f.push(b);
    }
  });
  lo("$$ms-gr-react-wrapper", y), oo(() => {
    l.set(Sn(e));
  }), ao(() => {
    f.forEach((b) => b());
  });
  function S(b) {
    gn[b ? "unshift" : "push"](() => {
      r = b, c.set(r);
    });
  }
  function x(b) {
    gn[b ? "unshift" : "push"](() => {
      i = b, d.set(i);
    });
  }
  return n.$$set = (b) => {
    t(17, e = mn(mn({}, e), yn(b))), "svelteInit" in b && t(5, u = b.svelteInit), "$$scope" in b && t(6, s = b.$$scope);
  }, e = yn(e), [r, i, c, d, a, u, s, o, S, x];
}
class fo extends Gi {
  constructor(e) {
    super(), to(this, e, uo, co, no, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: Va
} = window.__gradio__svelte__internal, xn = window.ms_globals.rerender, At = window.ms_globals.tree;
function ho(n, e = {}) {
  function t(r) {
    const i = tt(), o = new fo({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: i,
            reactComponent: n,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, u = s.parent ?? At;
          return u.nodes = [...u.nodes, a], xn({
            createPortal: at,
            node: At
          }), s.onDestroy(() => {
            u.nodes = u.nodes.filter((l) => l.svelteInstance !== i), xn({
              createPortal: at,
              node: At
            });
          }), a;
        },
        ...r.props
      }
    });
    return i.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const po = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function mo(n) {
  return n ? Object.keys(n).reduce((e, t) => {
    const r = n[t];
    return e[t] = go(t, r), e;
  }, {}) : {};
}
function go(n, e) {
  return typeof e == "number" && !po.includes(n) ? e + "px" : e;
}
function Xt(n) {
  const e = [], t = n.cloneNode(!1);
  if (n._reactElement) {
    const i = h.Children.toArray(n._reactElement.props.children).map((o) => {
      if (h.isValidElement(o) && o.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Xt(o.props.el);
        return h.cloneElement(o, {
          ...o.props,
          el: a,
          children: [...h.Children.toArray(o.props.children), ...s]
        });
      }
      return null;
    });
    return i.originalChildren = n._reactElement.props.children, e.push(at(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: i
    }), t)), {
      clonedElement: t,
      portals: e
    };
  }
  Object.keys(n.getEventListeners()).forEach((i) => {
    n.getEventListeners(i).forEach(({
      listener: s,
      type: a,
      useCapture: u
    }) => {
      t.addEventListener(a, s, u);
    });
  });
  const r = Array.from(n.childNodes);
  for (let i = 0; i < r.length; i++) {
    const o = r[i];
    if (o.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Xt(o);
      e.push(...a), t.appendChild(s);
    } else o.nodeType === 3 && t.appendChild(o.cloneNode());
  }
  return {
    clonedElement: t,
    portals: e
  };
}
function vo(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const bo = jr(({
  slot: n,
  clone: e,
  className: t,
  style: r,
  observeAttributes: i
}, o) => {
  const s = se(), [a, u] = De([]), {
    forceClone: l
  } = Qr(), c = l ? !0 : e;
  return ge(() => {
    var g;
    if (!s.current || !n)
      return;
    let d = n;
    function f() {
      let p = d;
      if (d.tagName.toLowerCase() === "svelte-slot" && d.children.length === 1 && d.children[0] && (p = d.children[0], p.tagName.toLowerCase() === "react-portal-target" && p.children[0] && (p = p.children[0])), vo(o, p), t && p.classList.add(...t.split(" ")), r) {
        const y = mo(r);
        Object.keys(y).forEach((S) => {
          p.style[S] = y[S];
        });
      }
    }
    let m = null, v = null;
    if (c && window.MutationObserver) {
      let p = function() {
        var b, _, C;
        (b = s.current) != null && b.contains(d) && ((_ = s.current) == null || _.removeChild(d));
        const {
          portals: S,
          clonedElement: x
        } = Xt(n);
        d = x, u(S), d.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          f();
        }, 50), (C = s.current) == null || C.appendChild(d);
      };
      p();
      const y = Fi(() => {
        p(), m == null || m.disconnect(), m == null || m.observe(n, {
          childList: !0,
          subtree: !0
          // attributes: observeAttributes ?? (forceClone ? true : false),
        });
      }, 50);
      m = new window.MutationObserver(y), m.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      d.style.display = "contents", f(), (g = s.current) == null || g.appendChild(d);
    return () => {
      var p, y;
      d.style.display = "", (p = s.current) != null && p.contains(d) && ((y = s.current) == null || y.removeChild(d)), m == null || m.disconnect();
    };
  }, [n, c, t, r, o, i, l]), h.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), yo = "1.0.5", wo = /* @__PURE__ */ h.createContext({}), So = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, lr = (n) => {
  const e = h.useContext(wo);
  return h.useMemo(() => ({
    ...So,
    ...e[n]
  }), [e[n]]);
};
function de() {
  return de = Object.assign ? Object.assign.bind() : function(n) {
    for (var e = 1; e < arguments.length; e++) {
      var t = arguments[e];
      for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]);
    }
    return n;
  }, de.apply(null, arguments);
}
function Ne() {
  const {
    getPrefixCls: n,
    direction: e,
    csp: t,
    iconPrefixCls: r,
    theme: i
  } = h.useContext(yi.ConfigContext);
  return {
    theme: i,
    getPrefixCls: n,
    direction: e,
    csp: t,
    iconPrefixCls: r
  };
}
function ye(n) {
  var e = R.useRef();
  e.current = n;
  var t = R.useCallback(function() {
    for (var r, i = arguments.length, o = new Array(i), s = 0; s < i; s++)
      o[s] = arguments[s];
    return (r = e.current) === null || r === void 0 ? void 0 : r.call.apply(r, [e].concat(o));
  }, []);
  return t;
}
function xo(n) {
  if (Array.isArray(n)) return n;
}
function Co(n, e) {
  var t = n == null ? null : typeof Symbol < "u" && n[Symbol.iterator] || n["@@iterator"];
  if (t != null) {
    var r, i, o, s, a = [], u = !0, l = !1;
    try {
      if (o = (t = t.call(n)).next, e === 0) {
        if (Object(t) !== t) return;
        u = !1;
      } else for (; !(u = (r = o.call(t)).done) && (a.push(r.value), a.length !== e); u = !0) ;
    } catch (c) {
      l = !0, i = c;
    } finally {
      try {
        if (!u && t.return != null && (s = t.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw i;
      }
    }
    return a;
  }
}
function Cn(n, e) {
  (e == null || e > n.length) && (e = n.length);
  for (var t = 0, r = Array(e); t < e; t++) r[t] = n[t];
  return r;
}
function Eo(n, e) {
  if (n) {
    if (typeof n == "string") return Cn(n, e);
    var t = {}.toString.call(n).slice(8, -1);
    return t === "Object" && n.constructor && (t = n.constructor.name), t === "Map" || t === "Set" ? Array.from(n) : t === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? Cn(n, e) : void 0;
  }
}
function _o() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ne(n, e) {
  return xo(n) || Co(n, e) || Eo(n, e) || _o();
}
function ft() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var En = ft() ? R.useLayoutEffect : R.useEffect, Ro = function(e, t) {
  var r = R.useRef(!0);
  En(function() {
    return e(r.current);
  }, t), En(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, _n = function(e, t) {
  Ro(function(r) {
    if (!r)
      return e();
  }, t);
};
function We(n) {
  var e = R.useRef(!1), t = R.useState(n), r = ne(t, 2), i = r[0], o = r[1];
  R.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function s(a, u) {
    u && e.current || o(a);
  }
  return [i, s];
}
function $t(n) {
  return n !== void 0;
}
function rn(n, e) {
  var t = e || {}, r = t.defaultValue, i = t.value, o = t.onChange, s = t.postState, a = We(function() {
    return $t(i) ? i : $t(r) ? typeof r == "function" ? r() : r : typeof n == "function" ? n() : n;
  }), u = ne(a, 2), l = u[0], c = u[1], d = i !== void 0 ? i : l, f = s ? s(d) : d, m = ye(o), v = We([d]), g = ne(v, 2), p = g[0], y = g[1];
  _n(function() {
    var x = p[0];
    l !== x && m(l, x);
  }, [p]), _n(function() {
    $t(i) || c(i);
  }, [i]);
  var S = ye(function(x, b) {
    c(x, b), y([d], b);
  });
  return [f, S];
}
function te(n) {
  "@babel/helpers - typeof";
  return te = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, te(n);
}
var cr = {
  exports: {}
}, B = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var on = Symbol.for("react.element"), sn = Symbol.for("react.portal"), ht = Symbol.for("react.fragment"), pt = Symbol.for("react.strict_mode"), mt = Symbol.for("react.profiler"), gt = Symbol.for("react.provider"), vt = Symbol.for("react.context"), To = Symbol.for("react.server_context"), bt = Symbol.for("react.forward_ref"), yt = Symbol.for("react.suspense"), wt = Symbol.for("react.suspense_list"), St = Symbol.for("react.memo"), xt = Symbol.for("react.lazy"), Po = Symbol.for("react.offscreen"), ur;
ur = Symbol.for("react.module.reference");
function le(n) {
  if (typeof n == "object" && n !== null) {
    var e = n.$$typeof;
    switch (e) {
      case on:
        switch (n = n.type, n) {
          case ht:
          case mt:
          case pt:
          case yt:
          case wt:
            return n;
          default:
            switch (n = n && n.$$typeof, n) {
              case To:
              case vt:
              case bt:
              case xt:
              case St:
              case gt:
                return n;
              default:
                return e;
            }
        }
      case sn:
        return e;
    }
  }
}
B.ContextConsumer = vt;
B.ContextProvider = gt;
B.Element = on;
B.ForwardRef = bt;
B.Fragment = ht;
B.Lazy = xt;
B.Memo = St;
B.Portal = sn;
B.Profiler = mt;
B.StrictMode = pt;
B.Suspense = yt;
B.SuspenseList = wt;
B.isAsyncMode = function() {
  return !1;
};
B.isConcurrentMode = function() {
  return !1;
};
B.isContextConsumer = function(n) {
  return le(n) === vt;
};
B.isContextProvider = function(n) {
  return le(n) === gt;
};
B.isElement = function(n) {
  return typeof n == "object" && n !== null && n.$$typeof === on;
};
B.isForwardRef = function(n) {
  return le(n) === bt;
};
B.isFragment = function(n) {
  return le(n) === ht;
};
B.isLazy = function(n) {
  return le(n) === xt;
};
B.isMemo = function(n) {
  return le(n) === St;
};
B.isPortal = function(n) {
  return le(n) === sn;
};
B.isProfiler = function(n) {
  return le(n) === mt;
};
B.isStrictMode = function(n) {
  return le(n) === pt;
};
B.isSuspense = function(n) {
  return le(n) === yt;
};
B.isSuspenseList = function(n) {
  return le(n) === wt;
};
B.isValidElementType = function(n) {
  return typeof n == "string" || typeof n == "function" || n === ht || n === mt || n === pt || n === yt || n === wt || n === Po || typeof n == "object" && n !== null && (n.$$typeof === xt || n.$$typeof === St || n.$$typeof === gt || n.$$typeof === vt || n.$$typeof === bt || n.$$typeof === ur || n.getModuleId !== void 0);
};
B.typeOf = le;
cr.exports = B;
var kt = cr.exports, Mo = Symbol.for("react.element"), Lo = Symbol.for("react.transitional.element"), Oo = Symbol.for("react.fragment");
function Ao(n) {
  return (
    // Base object type
    n && te(n) === "object" && // React Element type
    (n.$$typeof === Mo || n.$$typeof === Lo) && // React Fragment type
    n.type === Oo
  );
}
var $o = function(e, t) {
  typeof e == "function" ? e(t) : te(e) === "object" && e && "current" in e && (e.current = t);
}, ko = function(e) {
  var t, r;
  if (!e)
    return !1;
  if (dr(e) && e.props.propertyIsEnumerable("ref"))
    return !0;
  var i = kt.isMemo(e) ? e.type.type : e.type;
  return !(typeof i == "function" && !((t = i.prototype) !== null && t !== void 0 && t.render) && i.$$typeof !== kt.ForwardRef || typeof e == "function" && !((r = e.prototype) !== null && r !== void 0 && r.render) && e.$$typeof !== kt.ForwardRef);
};
function dr(n) {
  return /* @__PURE__ */ Br(n) && !Ao(n);
}
var Io = function(e) {
  if (e && dr(e)) {
    var t = e;
    return t.props.propertyIsEnumerable("ref") ? t.props.ref : t.ref;
  }
  return null;
};
function Do(n, e) {
  for (var t = n, r = 0; r < e.length; r += 1) {
    if (t == null)
      return;
    t = t[e[r]];
  }
  return t;
}
function No(n, e) {
  if (te(n) != "object" || !n) return n;
  var t = n[Symbol.toPrimitive];
  if (t !== void 0) {
    var r = t.call(n, e);
    if (te(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(n);
}
function fr(n) {
  var e = No(n, "string");
  return te(e) == "symbol" ? e : e + "";
}
function U(n, e, t) {
  return (e = fr(e)) in n ? Object.defineProperty(n, e, {
    value: t,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : n[e] = t, n;
}
function Rn(n, e) {
  var t = Object.keys(n);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(n);
    e && (r = r.filter(function(i) {
      return Object.getOwnPropertyDescriptor(n, i).enumerable;
    })), t.push.apply(t, r);
  }
  return t;
}
function k(n) {
  for (var e = 1; e < arguments.length; e++) {
    var t = arguments[e] != null ? arguments[e] : {};
    e % 2 ? Rn(Object(t), !0).forEach(function(r) {
      U(n, r, t[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(n, Object.getOwnPropertyDescriptors(t)) : Rn(Object(t)).forEach(function(r) {
      Object.defineProperty(n, r, Object.getOwnPropertyDescriptor(t, r));
    });
  }
  return n;
}
const je = /* @__PURE__ */ h.createContext(null);
function Tn(n) {
  const {
    getDropContainer: e,
    className: t,
    prefixCls: r,
    children: i
  } = n, {
    disabled: o
  } = h.useContext(je), [s, a] = h.useState(), [u, l] = h.useState(null);
  if (h.useEffect(() => {
    const f = e == null ? void 0 : e();
    s !== f && a(f);
  }, [e]), h.useEffect(() => {
    if (s) {
      const f = () => {
        l(!0);
      }, m = (p) => {
        p.preventDefault();
      }, v = (p) => {
        p.relatedTarget || l(!1);
      }, g = (p) => {
        l(!1), p.preventDefault();
      };
      return document.addEventListener("dragenter", f), document.addEventListener("dragover", m), document.addEventListener("dragleave", v), document.addEventListener("drop", g), () => {
        document.removeEventListener("dragenter", f), document.removeEventListener("dragover", m), document.removeEventListener("dragleave", v), document.removeEventListener("drop", g);
      };
    }
  }, [!!s]), !(e && s && !o))
    return null;
  const d = `${r}-drop-area`;
  return /* @__PURE__ */ at(/* @__PURE__ */ h.createElement("div", {
    className: Z(d, t, {
      [`${d}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: u ? "block" : "none"
    }
  }, i), s);
}
function Pn(n) {
  return n instanceof HTMLElement || n instanceof SVGElement;
}
function Wo(n) {
  return n && te(n) === "object" && Pn(n.nativeElement) ? n.nativeElement : Pn(n) ? n : null;
}
function Fo(n) {
  var e = Wo(n);
  if (e)
    return e;
  if (n instanceof h.Component) {
    var t;
    return (t = dn.findDOMNode) === null || t === void 0 ? void 0 : t.call(dn, n);
  }
  return null;
}
function jo(n, e) {
  if (n == null) return {};
  var t = {};
  for (var r in n) if ({}.hasOwnProperty.call(n, r)) {
    if (e.includes(r)) continue;
    t[r] = n[r];
  }
  return t;
}
function Mn(n, e) {
  if (n == null) return {};
  var t, r, i = jo(n, e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(n);
    for (r = 0; r < o.length; r++) t = o[r], e.includes(t) || {}.propertyIsEnumerable.call(n, t) && (i[t] = n[t]);
  }
  return i;
}
var Bo = /* @__PURE__ */ R.createContext({});
function Te(n, e) {
  if (!(n instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function Ln(n, e) {
  for (var t = 0; t < e.length; t++) {
    var r = e[t];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(n, fr(r.key), r);
  }
}
function Pe(n, e, t) {
  return e && Ln(n.prototype, e), t && Ln(n, t), Object.defineProperty(n, "prototype", {
    writable: !1
  }), n;
}
function Gt(n, e) {
  return Gt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(t, r) {
    return t.__proto__ = r, t;
  }, Gt(n, e);
}
function Ct(n, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  n.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: n,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(n, "prototype", {
    writable: !1
  }), e && Gt(n, e);
}
function ct(n) {
  return ct = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, ct(n);
}
function hr() {
  try {
    var n = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (hr = function() {
    return !!n;
  })();
}
function we(n) {
  if (n === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return n;
}
function Ho(n, e) {
  if (e && (te(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return we(n);
}
function Et(n) {
  var e = hr();
  return function() {
    var t, r = ct(n);
    if (e) {
      var i = ct(this).constructor;
      t = Reflect.construct(r, arguments, i);
    } else t = r.apply(this, arguments);
    return Ho(this, t);
  };
}
var zo = /* @__PURE__ */ function(n) {
  Ct(t, n);
  var e = Et(t);
  function t() {
    return Te(this, t), e.apply(this, arguments);
  }
  return Pe(t, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), t;
}(R.Component);
function Vo(n) {
  var e = R.useReducer(function(a) {
    return a + 1;
  }, 0), t = ne(e, 2), r = t[1], i = R.useRef(n), o = ye(function() {
    return i.current;
  }), s = ye(function(a) {
    i.current = typeof a == "function" ? a(i.current) : a, r();
  });
  return [o, s];
}
var be = "none", Xe = "appear", Ge = "enter", qe = "leave", On = "none", ue = "prepare", Ce = "start", Ee = "active", an = "end", pr = "prepared";
function An(n, e) {
  var t = {};
  return t[n.toLowerCase()] = e.toLowerCase(), t["Webkit".concat(n)] = "webkit".concat(e), t["Moz".concat(n)] = "moz".concat(e), t["ms".concat(n)] = "MS".concat(e), t["O".concat(n)] = "o".concat(e.toLowerCase()), t;
}
function Uo(n, e) {
  var t = {
    animationend: An("Animation", "AnimationEnd"),
    transitionend: An("Transition", "TransitionEnd")
  };
  return n && ("AnimationEvent" in e || delete t.animationend.animation, "TransitionEvent" in e || delete t.transitionend.transition), t;
}
var Xo = Uo(ft(), typeof window < "u" ? window : {}), mr = {};
if (ft()) {
  var Go = document.createElement("div");
  mr = Go.style;
}
var Ke = {};
function gr(n) {
  if (Ke[n])
    return Ke[n];
  var e = Xo[n];
  if (e)
    for (var t = Object.keys(e), r = t.length, i = 0; i < r; i += 1) {
      var o = t[i];
      if (Object.prototype.hasOwnProperty.call(e, o) && o in mr)
        return Ke[n] = e[o], Ke[n];
    }
  return "";
}
var vr = gr("animationend"), br = gr("transitionend"), yr = !!(vr && br), $n = vr || "animationend", kn = br || "transitionend";
function In(n, e) {
  if (!n) return null;
  if (te(n) === "object") {
    var t = e.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return n[t];
  }
  return "".concat(n, "-").concat(e);
}
const qo = function(n) {
  var e = se();
  function t(i) {
    i && (i.removeEventListener(kn, n), i.removeEventListener($n, n));
  }
  function r(i) {
    e.current && e.current !== i && t(e.current), i && i !== e.current && (i.addEventListener(kn, n), i.addEventListener($n, n), e.current = i);
  }
  return R.useEffect(function() {
    return function() {
      t(e.current);
    };
  }, []), [r, t];
};
var wr = ft() ? Hr : ge, Sr = function(e) {
  return +setTimeout(e, 16);
}, xr = function(e) {
  return clearTimeout(e);
};
typeof window < "u" && "requestAnimationFrame" in window && (Sr = function(e) {
  return window.requestAnimationFrame(e);
}, xr = function(e) {
  return window.cancelAnimationFrame(e);
});
var Dn = 0, ln = /* @__PURE__ */ new Map();
function Cr(n) {
  ln.delete(n);
}
var qt = function(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  Dn += 1;
  var r = Dn;
  function i(o) {
    if (o === 0)
      Cr(r), e();
    else {
      var s = Sr(function() {
        i(o - 1);
      });
      ln.set(r, s);
    }
  }
  return i(t), r;
};
qt.cancel = function(n) {
  var e = ln.get(n);
  return Cr(n), xr(e);
};
const Ko = function() {
  var n = R.useRef(null);
  function e() {
    qt.cancel(n.current);
  }
  function t(r) {
    var i = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    e();
    var o = qt(function() {
      i <= 1 ? r({
        isCanceled: function() {
          return o !== n.current;
        }
      }) : t(r, i - 1);
    });
    n.current = o;
  }
  return R.useEffect(function() {
    return function() {
      e();
    };
  }, []), [t, e];
};
var Yo = [ue, Ce, Ee, an], Zo = [ue, pr], Er = !1, Qo = !0;
function _r(n) {
  return n === Ee || n === an;
}
const Jo = function(n, e, t) {
  var r = We(On), i = ne(r, 2), o = i[0], s = i[1], a = Ko(), u = ne(a, 2), l = u[0], c = u[1];
  function d() {
    s(ue, !0);
  }
  var f = e ? Zo : Yo;
  return wr(function() {
    if (o !== On && o !== an) {
      var m = f.indexOf(o), v = f[m + 1], g = t(o);
      g === Er ? s(v, !0) : v && l(function(p) {
        function y() {
          p.isCanceled() || s(v, !0);
        }
        g === !0 ? y() : Promise.resolve(g).then(y);
      });
    }
  }, [n, o]), R.useEffect(function() {
    return function() {
      c();
    };
  }, []), [d, o];
};
function es(n, e, t, r) {
  var i = r.motionEnter, o = i === void 0 ? !0 : i, s = r.motionAppear, a = s === void 0 ? !0 : s, u = r.motionLeave, l = u === void 0 ? !0 : u, c = r.motionDeadline, d = r.motionLeaveImmediately, f = r.onAppearPrepare, m = r.onEnterPrepare, v = r.onLeavePrepare, g = r.onAppearStart, p = r.onEnterStart, y = r.onLeaveStart, S = r.onAppearActive, x = r.onEnterActive, b = r.onLeaveActive, _ = r.onAppearEnd, C = r.onEnterEnd, E = r.onLeaveEnd, T = r.onVisibleChanged, I = We(), W = ne(I, 2), N = W[0], P = W[1], O = Vo(be), w = ne(O, 2), $ = w[0], D = w[1], q = We(null), K = ne(q, 2), re = K[0], Y = K[1], L = $(), M = se(!1), F = se(null);
  function j() {
    return t();
  }
  var H = se(!1);
  function V() {
    D(be), Y(null, !0);
  }
  var J = ye(function(Q) {
    var A = $();
    if (A !== be) {
      var G = j();
      if (!(Q && !Q.deadline && Q.target !== G)) {
        var he = H.current, Ue;
        A === Xe && he ? Ue = _ == null ? void 0 : _(G, Q) : A === Ge && he ? Ue = C == null ? void 0 : C(G, Q) : A === qe && he && (Ue = E == null ? void 0 : E(G, Q)), he && Ue !== !1 && V();
      }
    }
  }), ie = qo(J), X = ne(ie, 1), ce = X[0], ve = function(A) {
    switch (A) {
      case Xe:
        return U(U(U({}, ue, f), Ce, g), Ee, S);
      case Ge:
        return U(U(U({}, ue, m), Ce, p), Ee, x);
      case qe:
        return U(U(U({}, ue, v), Ce, y), Ee, b);
      default:
        return {};
    }
  }, z = R.useMemo(function() {
    return ve(L);
  }, [L]), fe = Jo(L, !n, function(Q) {
    if (Q === ue) {
      var A = z[ue];
      return A ? A(j()) : Er;
    }
    if (me in z) {
      var G;
      Y(((G = z[me]) === null || G === void 0 ? void 0 : G.call(z, j(), null)) || null);
    }
    return me === Ee && L !== be && (ce(j()), c > 0 && (clearTimeout(F.current), F.current = setTimeout(function() {
      J({
        deadline: !0
      });
    }, c))), me === pr && V(), Qo;
  }), ze = ne(fe, 2), Me = ze[0], me = ze[1], Pt = _r(me);
  H.current = Pt;
  var Ve = se(null);
  wr(function() {
    if (!(M.current && Ve.current === e)) {
      P(e);
      var Q = M.current;
      M.current = !0;
      var A;
      !Q && e && a && (A = Xe), Q && e && o && (A = Ge), (Q && !e && l || !Q && d && !e && l) && (A = qe);
      var G = ve(A);
      A && (n || G[ue]) ? (D(A), Me()) : D(be), Ve.current = e;
    }
  }, [e]), ge(function() {
    // Cancel appear
    (L === Xe && !a || // Cancel enter
    L === Ge && !o || // Cancel leave
    L === qe && !l) && D(be);
  }, [a, o, l]), ge(function() {
    return function() {
      M.current = !1, clearTimeout(F.current);
    };
  }, []);
  var Le = R.useRef(!1);
  ge(function() {
    N && (Le.current = !0), N !== void 0 && L === be && ((Le.current || N) && (T == null || T(N)), Le.current = !0);
  }, [N, L]);
  var Oe = re;
  return z[ue] && me === Ce && (Oe = k({
    transition: "none"
  }, Oe)), [L, me, Oe, N ?? e];
}
function ts(n) {
  var e = n;
  te(n) === "object" && (e = n.transitionSupport);
  function t(i, o) {
    return !!(i.motionName && e && o !== !1);
  }
  var r = /* @__PURE__ */ R.forwardRef(function(i, o) {
    var s = i.visible, a = s === void 0 ? !0 : s, u = i.removeOnLeave, l = u === void 0 ? !0 : u, c = i.forceRender, d = i.children, f = i.motionName, m = i.leavedClassName, v = i.eventProps, g = R.useContext(Bo), p = g.motion, y = t(i, p), S = se(), x = se();
    function b() {
      try {
        return S.current instanceof HTMLElement ? S.current : Fo(x.current);
      } catch {
        return null;
      }
    }
    var _ = es(y, a, b, i), C = ne(_, 4), E = C[0], T = C[1], I = C[2], W = C[3], N = R.useRef(W);
    W && (N.current = !0);
    var P = R.useCallback(function(K) {
      S.current = K, $o(o, K);
    }, [o]), O, w = k(k({}, v), {}, {
      visible: a
    });
    if (!d)
      O = null;
    else if (E === be)
      W ? O = d(k({}, w), P) : !l && N.current && m ? O = d(k(k({}, w), {}, {
        className: m
      }), P) : c || !l && !m ? O = d(k(k({}, w), {}, {
        style: {
          display: "none"
        }
      }), P) : O = null;
    else {
      var $;
      T === ue ? $ = "prepare" : _r(T) ? $ = "active" : T === Ce && ($ = "start");
      var D = In(f, "".concat(E, "-").concat($));
      O = d(k(k({}, w), {}, {
        className: Z(In(f, E), U(U({}, D, D && $), f, typeof f == "string")),
        style: I
      }), P);
    }
    if (/* @__PURE__ */ R.isValidElement(O) && ko(O)) {
      var q = Io(O);
      q || (O = /* @__PURE__ */ R.cloneElement(O, {
        ref: P
      }));
    }
    return /* @__PURE__ */ R.createElement(zo, {
      ref: x
    }, O);
  });
  return r.displayName = "CSSMotion", r;
}
const Rr = ts(yr);
var Kt = "add", Yt = "keep", Zt = "remove", It = "removed";
function ns(n) {
  var e;
  return n && te(n) === "object" && "key" in n ? e = n : e = {
    key: n
  }, k(k({}, e), {}, {
    key: String(e.key)
  });
}
function Qt() {
  var n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return n.map(ns);
}
function rs() {
  var n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], t = [], r = 0, i = e.length, o = Qt(n), s = Qt(e);
  o.forEach(function(l) {
    for (var c = !1, d = r; d < i; d += 1) {
      var f = s[d];
      if (f.key === l.key) {
        r < d && (t = t.concat(s.slice(r, d).map(function(m) {
          return k(k({}, m), {}, {
            status: Kt
          });
        })), r = d), t.push(k(k({}, f), {}, {
          status: Yt
        })), r += 1, c = !0;
        break;
      }
    }
    c || t.push(k(k({}, l), {}, {
      status: Zt
    }));
  }), r < i && (t = t.concat(s.slice(r).map(function(l) {
    return k(k({}, l), {}, {
      status: Kt
    });
  })));
  var a = {};
  t.forEach(function(l) {
    var c = l.key;
    a[c] = (a[c] || 0) + 1;
  });
  var u = Object.keys(a).filter(function(l) {
    return a[l] > 1;
  });
  return u.forEach(function(l) {
    t = t.filter(function(c) {
      var d = c.key, f = c.status;
      return d !== l || f !== Zt;
    }), t.forEach(function(c) {
      c.key === l && (c.status = Yt);
    });
  }), t;
}
var is = ["component", "children", "onVisibleChanged", "onAllRemoved"], os = ["status"], ss = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function as(n) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Rr, t = /* @__PURE__ */ function(r) {
    Ct(o, r);
    var i = Et(o);
    function o() {
      var s;
      Te(this, o);
      for (var a = arguments.length, u = new Array(a), l = 0; l < a; l++)
        u[l] = arguments[l];
      return s = i.call.apply(i, [this].concat(u)), U(we(s), "state", {
        keyEntities: []
      }), U(we(s), "removeKey", function(c) {
        s.setState(function(d) {
          var f = d.keyEntities.map(function(m) {
            return m.key !== c ? m : k(k({}, m), {}, {
              status: It
            });
          });
          return {
            keyEntities: f
          };
        }, function() {
          var d = s.state.keyEntities, f = d.filter(function(m) {
            var v = m.status;
            return v !== It;
          }).length;
          f === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Pe(o, [{
      key: "render",
      value: function() {
        var a = this, u = this.state.keyEntities, l = this.props, c = l.component, d = l.children, f = l.onVisibleChanged;
        l.onAllRemoved;
        var m = Mn(l, is), v = c || R.Fragment, g = {};
        return ss.forEach(function(p) {
          g[p] = m[p], delete m[p];
        }), delete m.keys, /* @__PURE__ */ R.createElement(v, m, u.map(function(p, y) {
          var S = p.status, x = Mn(p, os), b = S === Kt || S === Yt;
          return /* @__PURE__ */ R.createElement(e, de({}, g, {
            key: x.key,
            visible: b,
            eventProps: x,
            onVisibleChanged: function(C) {
              f == null || f(C, {
                key: x.key
              }), C || a.removeKey(x.key);
            }
          }), function(_, C) {
            return d(k(k({}, _), {}, {
              index: y
            }), C);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, u) {
        var l = a.keys, c = u.keyEntities, d = Qt(l), f = rs(c, d);
        return {
          keyEntities: f.filter(function(m) {
            var v = c.find(function(g) {
              var p = g.key;
              return m.key === p;
            });
            return !(v && v.status === It && m.status === Zt);
          })
        };
      }
    }]), o;
  }(R.Component);
  return U(t, "defaultProps", {
    component: "div"
  }), t;
}
const ls = as(yr);
function cs(n, e) {
  const {
    children: t,
    upload: r,
    rootClassName: i
  } = n, o = h.useRef(null);
  return h.useImperativeHandle(e, () => o.current), /* @__PURE__ */ h.createElement(er, de({}, r, {
    showUploadList: !1,
    rootClassName: i,
    ref: o
  }), t);
}
const Tr = /* @__PURE__ */ h.forwardRef(cs);
var Pr = /* @__PURE__ */ Pe(function n() {
  Te(this, n);
}), Mr = "CALC_UNIT", us = new RegExp(Mr, "g");
function Dt(n) {
  return typeof n == "number" ? "".concat(n).concat(Mr) : n;
}
var ds = /* @__PURE__ */ function(n) {
  Ct(t, n);
  var e = Et(t);
  function t(r, i) {
    var o;
    Te(this, t), o = e.call(this), U(we(o), "result", ""), U(we(o), "unitlessCssVar", void 0), U(we(o), "lowPriority", void 0);
    var s = te(r);
    return o.unitlessCssVar = i, r instanceof t ? o.result = "(".concat(r.result, ")") : s === "number" ? o.result = Dt(r) : s === "string" && (o.result = r), o;
  }
  return Pe(t, [{
    key: "add",
    value: function(i) {
      return i instanceof t ? this.result = "".concat(this.result, " + ").concat(i.getResult()) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " + ").concat(Dt(i))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(i) {
      return i instanceof t ? this.result = "".concat(this.result, " - ").concat(i.getResult()) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " - ").concat(Dt(i))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(i) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), i instanceof t ? this.result = "".concat(this.result, " * ").concat(i.getResult(!0)) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " * ").concat(i)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(i) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), i instanceof t ? this.result = "".concat(this.result, " / ").concat(i.getResult(!0)) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " / ").concat(i)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(i) {
      return this.lowPriority || i ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(i) {
      var o = this, s = i || {}, a = s.unit, u = !0;
      return typeof a == "boolean" ? u = a : Array.from(this.unitlessCssVar).some(function(l) {
        return o.result.includes(l);
      }) && (u = !1), this.result = this.result.replace(us, u ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), t;
}(Pr), fs = /* @__PURE__ */ function(n) {
  Ct(t, n);
  var e = Et(t);
  function t(r) {
    var i;
    return Te(this, t), i = e.call(this), U(we(i), "result", 0), r instanceof t ? i.result = r.result : typeof r == "number" && (i.result = r), i;
  }
  return Pe(t, [{
    key: "add",
    value: function(i) {
      return i instanceof t ? this.result += i.result : typeof i == "number" && (this.result += i), this;
    }
  }, {
    key: "sub",
    value: function(i) {
      return i instanceof t ? this.result -= i.result : typeof i == "number" && (this.result -= i), this;
    }
  }, {
    key: "mul",
    value: function(i) {
      return i instanceof t ? this.result *= i.result : typeof i == "number" && (this.result *= i), this;
    }
  }, {
    key: "div",
    value: function(i) {
      return i instanceof t ? this.result /= i.result : typeof i == "number" && (this.result /= i), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), t;
}(Pr), hs = function(e, t) {
  var r = e === "css" ? ds : fs;
  return function(i) {
    return new r(i, t);
  };
}, Nn = function(e, t) {
  return "".concat([t, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function Wn(n, e, t, r) {
  var i = k({}, e[n]);
  if (r != null && r.deprecatedTokens) {
    var o = r.deprecatedTokens;
    o.forEach(function(a) {
      var u = ne(a, 2), l = u[0], c = u[1];
      if (i != null && i[l] || i != null && i[c]) {
        var d;
        (d = i[c]) !== null && d !== void 0 || (i[c] = i == null ? void 0 : i[l]);
      }
    });
  }
  var s = k(k({}, t), i);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var Lr = typeof CSSINJS_STATISTIC < "u", Jt = !0;
function _t() {
  for (var n = arguments.length, e = new Array(n), t = 0; t < n; t++)
    e[t] = arguments[t];
  if (!Lr)
    return Object.assign.apply(Object, [{}].concat(e));
  Jt = !1;
  var r = {};
  return e.forEach(function(i) {
    if (te(i) === "object") {
      var o = Object.keys(i);
      o.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return i[s];
          }
        });
      });
    }
  }), Jt = !0, r;
}
var Fn = {};
function ps() {
}
var ms = function(e) {
  var t, r = e, i = ps;
  return Lr && typeof Proxy < "u" && (t = /* @__PURE__ */ new Set(), r = new Proxy(e, {
    get: function(s, a) {
      if (Jt) {
        var u;
        (u = t) === null || u === void 0 || u.add(a);
      }
      return s[a];
    }
  }), i = function(s, a) {
    var u;
    Fn[s] = {
      global: Array.from(t),
      component: k(k({}, (u = Fn[s]) === null || u === void 0 ? void 0 : u.component), a)
    };
  }), {
    token: r,
    keys: t,
    flush: i
  };
};
function jn(n, e, t) {
  if (typeof t == "function") {
    var r;
    return t(_t(e, (r = e[n]) !== null && r !== void 0 ? r : {}));
  }
  return t ?? {};
}
function gs(n) {
  return n === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var t = arguments.length, r = new Array(t), i = 0; i < t; i++)
        r[i] = arguments[i];
      return "max(".concat(r.map(function(o) {
        return Vt(o);
      }).join(","), ")");
    },
    min: function() {
      for (var t = arguments.length, r = new Array(t), i = 0; i < t; i++)
        r[i] = arguments[i];
      return "min(".concat(r.map(function(o) {
        return Vt(o);
      }).join(","), ")");
    }
  };
}
var vs = 1e3 * 60 * 10, bs = /* @__PURE__ */ function() {
  function n() {
    Te(this, n), U(this, "map", /* @__PURE__ */ new Map()), U(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), U(this, "nextID", 0), U(this, "lastAccessBeat", /* @__PURE__ */ new Map()), U(this, "accessBeat", 0);
  }
  return Pe(n, [{
    key: "set",
    value: function(t, r) {
      this.clear();
      var i = this.getCompositeKey(t);
      this.map.set(i, r), this.lastAccessBeat.set(i, Date.now());
    }
  }, {
    key: "get",
    value: function(t) {
      var r = this.getCompositeKey(t), i = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, i;
    }
  }, {
    key: "getCompositeKey",
    value: function(t) {
      var r = this, i = t.map(function(o) {
        return o && te(o) === "object" ? "obj_".concat(r.getObjectID(o)) : "".concat(te(o), "_").concat(o);
      });
      return i.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(t) {
      if (this.objectIDMap.has(t))
        return this.objectIDMap.get(t);
      var r = this.nextID;
      return this.objectIDMap.set(t, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var t = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(i, o) {
          r - i > vs && (t.map.delete(o), t.lastAccessBeat.delete(o));
        }), this.accessBeat = 0;
      }
    }
  }]), n;
}(), Bn = new bs();
function ys(n, e) {
  return h.useMemo(function() {
    var t = Bn.get(e);
    if (t)
      return t;
    var r = n();
    return Bn.set(e, r), r;
  }, e);
}
var ws = function() {
  return {};
};
function Ss(n) {
  var e = n.useCSP, t = e === void 0 ? ws : e, r = n.useToken, i = n.usePrefix, o = n.getResetStyles, s = n.getCommonStyle, a = n.getCompUnitless;
  function u(f, m, v, g) {
    var p = Array.isArray(f) ? f[0] : f;
    function y(T) {
      return "".concat(String(p)).concat(T.slice(0, 1).toUpperCase()).concat(T.slice(1));
    }
    var S = (g == null ? void 0 : g.unitless) || {}, x = typeof a == "function" ? a(f) : {}, b = k(k({}, x), {}, U({}, y("zIndexPopup"), !0));
    Object.keys(S).forEach(function(T) {
      b[y(T)] = S[T];
    });
    var _ = k(k({}, g), {}, {
      unitless: b,
      prefixToken: y
    }), C = c(f, m, v, _), E = l(p, v, _);
    return function(T) {
      var I = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : T, W = C(T, I), N = ne(W, 2), P = N[1], O = E(I), w = ne(O, 2), $ = w[0], D = w[1];
      return [$, P, D];
    };
  }
  function l(f, m, v) {
    var g = v.unitless, p = v.injectStyle, y = p === void 0 ? !0 : p, S = v.prefixToken, x = v.ignore, b = function(E) {
      var T = E.rootCls, I = E.cssVar, W = I === void 0 ? {} : I, N = r(), P = N.realToken;
      return Ei({
        path: [f],
        prefix: W.prefix,
        key: W.key,
        unitless: g,
        ignore: x,
        token: P,
        scope: T
      }, function() {
        var O = jn(f, P, m), w = Wn(f, P, O, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(O).forEach(function($) {
          w[S($)] = w[$], delete w[$];
        }), w;
      }), null;
    }, _ = function(E) {
      var T = r(), I = T.cssVar;
      return [function(W) {
        return y && I ? /* @__PURE__ */ h.createElement(h.Fragment, null, /* @__PURE__ */ h.createElement(b, {
          rootCls: E,
          cssVar: I,
          component: f
        }), W) : W;
      }, I == null ? void 0 : I.key];
    };
    return _;
  }
  function c(f, m, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = Array.isArray(f) ? f : [f, f], y = ne(p, 1), S = y[0], x = p.join("-"), b = n.layer || {
      name: "antd"
    };
    return function(_) {
      var C = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : _, E = r(), T = E.theme, I = E.realToken, W = E.hashId, N = E.token, P = E.cssVar, O = i(), w = O.rootPrefixCls, $ = O.iconPrefixCls, D = t(), q = P ? "css" : "js", K = ys(function() {
        var j = /* @__PURE__ */ new Set();
        return P && Object.keys(g.unitless || {}).forEach(function(H) {
          j.add(Lt(H, P.prefix)), j.add(Lt(H, Nn(S, P.prefix)));
        }), hs(q, j);
      }, [q, S, P == null ? void 0 : P.prefix]), re = gs(q), Y = re.max, L = re.min, M = {
        theme: T,
        token: N,
        hashId: W,
        nonce: function() {
          return D.nonce;
        },
        clientOnly: g.clientOnly,
        layer: b,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof o == "function" && fn(k(k({}, M), {}, {
        clientOnly: !1,
        path: ["Shared", w]
      }), function() {
        return o(N, {
          prefix: {
            rootPrefixCls: w,
            iconPrefixCls: $
          },
          csp: D
        });
      });
      var F = fn(k(k({}, M), {}, {
        path: [x, _, $]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var j = ms(N), H = j.token, V = j.flush, J = jn(S, I, v), ie = ".".concat(_), X = Wn(S, I, J, {
          deprecatedTokens: g.deprecatedTokens
        });
        P && J && te(J) === "object" && Object.keys(J).forEach(function(fe) {
          J[fe] = "var(".concat(Lt(fe, Nn(S, P.prefix)), ")");
        });
        var ce = _t(H, {
          componentCls: ie,
          prefixCls: _,
          iconCls: ".".concat($),
          antCls: ".".concat(w),
          calc: K,
          // @ts-ignore
          max: Y,
          // @ts-ignore
          min: L
        }, P ? J : X), ve = m(ce, {
          hashId: W,
          prefixCls: _,
          rootPrefixCls: w,
          iconPrefixCls: $
        });
        V(S, X);
        var z = typeof s == "function" ? s(ce, _, C, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : z, ve];
      });
      return [F, W];
    };
  }
  function d(f, m, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, p = c(f, m, v, k({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), y = function(x) {
      var b = x.prefixCls, _ = x.rootCls, C = _ === void 0 ? b : _;
      return p(b, C), null;
    };
    return y;
  }
  return {
    genStyleHooks: u,
    genSubStyleComponent: d,
    genComponentStyleHook: c
  };
}
function Fe(n) {
  "@babel/helpers - typeof";
  return Fe = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, Fe(n);
}
function xs(n, e) {
  if (Fe(n) != "object" || !n) return n;
  var t = n[Symbol.toPrimitive];
  if (t !== void 0) {
    var r = t.call(n, e);
    if (Fe(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(n);
}
function Cs(n) {
  var e = xs(n, "string");
  return Fe(e) == "symbol" ? e : e + "";
}
function ae(n, e, t) {
  return (e = Cs(e)) in n ? Object.defineProperty(n, e, {
    value: t,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : n[e] = t, n;
}
const ee = Math.round;
function Nt(n, e) {
  const t = n.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = t.map((i) => parseFloat(i));
  for (let i = 0; i < 3; i += 1)
    r[i] = e(r[i] || 0, t[i] || "", i);
  return t[3] ? r[3] = t[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const Hn = (n, e, t) => t === 0 ? n : n / 100;
function Ae(n, e) {
  const t = e || 255;
  return n > t ? t : n < 0 ? 0 : n;
}
class pe {
  constructor(e) {
    ae(this, "isValid", !0), ae(this, "r", 0), ae(this, "g", 0), ae(this, "b", 0), ae(this, "a", 1), ae(this, "_h", void 0), ae(this, "_s", void 0), ae(this, "_l", void 0), ae(this, "_v", void 0), ae(this, "_max", void 0), ae(this, "_min", void 0), ae(this, "_brightness", void 0);
    function t(r) {
      return r[0] in e && r[1] in e && r[2] in e;
    }
    if (e) if (typeof e == "string") {
      let i = function(o) {
        return r.startsWith(o);
      };
      const r = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : i("rgb") ? this.fromRgbString(r) : i("hsl") ? this.fromHslString(r) : (i("hsv") || i("hsb")) && this.fromHsvString(r);
    } else if (e instanceof pe)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (t("rgb"))
      this.r = Ae(e.r), this.g = Ae(e.g), this.b = Ae(e.b), this.a = typeof e.a == "number" ? Ae(e.a, 1) : 1;
    else if (t("hsl"))
      this.fromHsl(e);
    else if (t("hsv"))
      this.fromHsv(e);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(e));
  }
  // ======================= Setter =======================
  setR(e) {
    return this._sc("r", e);
  }
  setG(e) {
    return this._sc("g", e);
  }
  setB(e) {
    return this._sc("b", e);
  }
  setA(e) {
    return this._sc("a", e, 1);
  }
  setHue(e) {
    const t = this.toHsv();
    return t.h = e, this._c(t);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(o) {
      const s = o / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const t = e(this.r), r = e(this.g), i = e(this.b);
    return 0.2126 * t + 0.7152 * r + 0.0722 * i;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = ee(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._s = 0 : this._s = e / this.getMax();
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
  darken(e = 10) {
    const t = this.getHue(), r = this.getSaturation();
    let i = this.getLightness() - e / 100;
    return i < 0 && (i = 0), this._c({
      h: t,
      s: r,
      l: i,
      a: this.a
    });
  }
  lighten(e = 10) {
    const t = this.getHue(), r = this.getSaturation();
    let i = this.getLightness() + e / 100;
    return i > 1 && (i = 1), this._c({
      h: t,
      s: r,
      l: i,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(e, t = 50) {
    const r = this._c(e), i = t / 100, o = (a) => (r[a] - this[a]) * i + this[a], s = {
      r: ee(o("r")),
      g: ee(o("g")),
      b: ee(o("b")),
      a: ee(o("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(e = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, e);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(e = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, e);
  }
  onBackground(e) {
    const t = this._c(e), r = this.a + t.a * (1 - this.a), i = (o) => ee((this[o] * this.a + t[o] * t.a * (1 - this.a)) / r);
    return this._c({
      r: i("r"),
      g: i("g"),
      b: i("b"),
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
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const t = (this.r || 0).toString(16);
    e += t.length === 2 ? t : "0" + t;
    const r = (this.g || 0).toString(16);
    e += r.length === 2 ? r : "0" + r;
    const i = (this.b || 0).toString(16);
    if (e += i.length === 2 ? i : "0" + i, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const o = ee(this.a * 255).toString(16);
      e += o.length === 2 ? o : "0" + o;
    }
    return e;
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
    const e = this.getHue(), t = ee(this.getSaturation() * 100), r = ee(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${t}%,${r}%,${this.a})` : `hsl(${e},${t}%,${r}%)`;
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
  _sc(e, t, r) {
    const i = this.clone();
    return i[e] = Ae(t, r), i;
  }
  _c(e) {
    return new this.constructor(e);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(e) {
    const t = e.replace("#", "");
    function r(i, o) {
      return parseInt(t[i] + t[o || i], 16);
    }
    t.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = t[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = t[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: t,
    l: r,
    a: i
  }) {
    if (this._h = e % 360, this._s = t, this._l = r, this.a = typeof i == "number" ? i : 1, t <= 0) {
      const f = ee(r * 255);
      this.r = f, this.g = f, this.b = f;
    }
    let o = 0, s = 0, a = 0;
    const u = e / 60, l = (1 - Math.abs(2 * r - 1)) * t, c = l * (1 - Math.abs(u % 2 - 1));
    u >= 0 && u < 1 ? (o = l, s = c) : u >= 1 && u < 2 ? (o = c, s = l) : u >= 2 && u < 3 ? (s = l, a = c) : u >= 3 && u < 4 ? (s = c, a = l) : u >= 4 && u < 5 ? (o = c, a = l) : u >= 5 && u < 6 && (o = l, a = c);
    const d = r - l / 2;
    this.r = ee((o + d) * 255), this.g = ee((s + d) * 255), this.b = ee((a + d) * 255);
  }
  fromHsv({
    h: e,
    s: t,
    v: r,
    a: i
  }) {
    this._h = e % 360, this._s = t, this._v = r, this.a = typeof i == "number" ? i : 1;
    const o = ee(r * 255);
    if (this.r = o, this.g = o, this.b = o, t <= 0)
      return;
    const s = e / 60, a = Math.floor(s), u = s - a, l = ee(r * (1 - t) * 255), c = ee(r * (1 - t * u) * 255), d = ee(r * (1 - t * (1 - u)) * 255);
    switch (a) {
      case 0:
        this.g = d, this.b = l;
        break;
      case 1:
        this.r = c, this.b = l;
        break;
      case 2:
        this.r = l, this.b = d;
        break;
      case 3:
        this.r = l, this.g = c;
        break;
      case 4:
        this.r = d, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = c;
        break;
    }
  }
  fromHsvString(e) {
    const t = Nt(e, Hn);
    this.fromHsv({
      h: t[0],
      s: t[1],
      v: t[2],
      a: t[3]
    });
  }
  fromHslString(e) {
    const t = Nt(e, Hn);
    this.fromHsl({
      h: t[0],
      s: t[1],
      l: t[2],
      a: t[3]
    });
  }
  fromRgbString(e) {
    const t = Nt(e, (r, i) => (
      // Convert percentage to number. e.g. 50% -> 128
      i.includes("%") ? ee(r / 100 * 255) : r
    ));
    this.r = t[0], this.g = t[1], this.b = t[2], this.a = t[3];
  }
}
const Es = {
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
}, _s = Object.assign(Object.assign({}, Es), {
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
function Wt(n) {
  return n >= 0 && n <= 255;
}
function Ye(n, e) {
  const {
    r: t,
    g: r,
    b: i,
    a: o
  } = new pe(n).toRgb();
  if (o < 1)
    return n;
  const {
    r: s,
    g: a,
    b: u
  } = new pe(e).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const c = Math.round((t - s * (1 - l)) / l), d = Math.round((r - a * (1 - l)) / l), f = Math.round((i - u * (1 - l)) / l);
    if (Wt(c) && Wt(d) && Wt(f))
      return new pe({
        r: c,
        g: d,
        b: f,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new pe({
    r: t,
    g: r,
    b: i,
    a: 1
  }).toRgbString();
}
var Rs = function(n, e) {
  var t = {};
  for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && e.indexOf(r) < 0 && (t[r] = n[r]);
  if (n != null && typeof Object.getOwnPropertySymbols == "function") for (var i = 0, r = Object.getOwnPropertySymbols(n); i < r.length; i++)
    e.indexOf(r[i]) < 0 && Object.prototype.propertyIsEnumerable.call(n, r[i]) && (t[r[i]] = n[r[i]]);
  return t;
};
function Ts(n) {
  const {
    override: e
  } = n, t = Rs(n, ["override"]), r = Object.assign({}, e);
  Object.keys(_s).forEach((f) => {
    delete r[f];
  });
  const i = Object.assign(Object.assign({}, t), r), o = 480, s = 576, a = 768, u = 992, l = 1200, c = 1600;
  if (i.motion === !1) {
    const f = "0s";
    i.motionDurationFast = f, i.motionDurationMid = f, i.motionDurationSlow = f;
  }
  return Object.assign(Object.assign(Object.assign({}, i), {
    // ============== Background ============== //
    colorFillContent: i.colorFillSecondary,
    colorFillContentHover: i.colorFill,
    colorFillAlter: i.colorFillQuaternary,
    colorBgContainerDisabled: i.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: i.colorBgContainer,
    colorSplit: Ye(i.colorBorderSecondary, i.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: i.colorTextQuaternary,
    colorTextDisabled: i.colorTextQuaternary,
    colorTextHeading: i.colorText,
    colorTextLabel: i.colorTextSecondary,
    colorTextDescription: i.colorTextTertiary,
    colorTextLightSolid: i.colorWhite,
    colorHighlight: i.colorError,
    colorBgTextHover: i.colorFillSecondary,
    colorBgTextActive: i.colorFill,
    colorIcon: i.colorTextTertiary,
    colorIconHover: i.colorText,
    colorErrorOutline: Ye(i.colorErrorBg, i.colorBgContainer),
    colorWarningOutline: Ye(i.colorWarningBg, i.colorBgContainer),
    // Font
    fontSizeIcon: i.fontSizeSM,
    // Line
    lineWidthFocus: i.lineWidth * 3,
    // Control
    lineWidth: i.lineWidth,
    controlOutlineWidth: i.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: i.controlHeight / 2,
    controlItemBgHover: i.colorFillTertiary,
    controlItemBgActive: i.colorPrimaryBg,
    controlItemBgActiveHover: i.colorPrimaryBgHover,
    controlItemBgActiveDisabled: i.colorFill,
    controlTmpOutline: i.colorFillQuaternary,
    controlOutline: Ye(i.colorPrimaryBg, i.colorBgContainer),
    lineType: i.lineType,
    borderRadius: i.borderRadius,
    borderRadiusXS: i.borderRadiusXS,
    borderRadiusSM: i.borderRadiusSM,
    borderRadiusLG: i.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: i.sizeXXS,
    paddingXS: i.sizeXS,
    paddingSM: i.sizeSM,
    padding: i.size,
    paddingMD: i.sizeMD,
    paddingLG: i.sizeLG,
    paddingXL: i.sizeXL,
    paddingContentHorizontalLG: i.sizeLG,
    paddingContentVerticalLG: i.sizeMS,
    paddingContentHorizontal: i.sizeMS,
    paddingContentVertical: i.sizeSM,
    paddingContentHorizontalSM: i.size,
    paddingContentVerticalSM: i.sizeXS,
    marginXXS: i.sizeXXS,
    marginXS: i.sizeXS,
    marginSM: i.sizeSM,
    margin: i.size,
    marginMD: i.sizeMD,
    marginLG: i.sizeLG,
    marginXL: i.sizeXL,
    marginXXL: i.sizeXXL,
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
    screenXS: o,
    screenXSMin: o,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: u - 1,
    screenLG: u,
    screenLGMin: u,
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: c - 1,
    screenXXL: c,
    screenXXLMin: c,
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
  }), r);
}
const Ps = {
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
}, Ms = {
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
}, Ls = _i(lt.defaultAlgorithm), Os = {
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
}, Or = (n, e, t) => {
  const r = t.getDerivativeToken(n), {
    override: i,
    ...o
  } = e;
  let s = {
    ...r,
    override: i
  };
  return s = Ts(s), o && Object.entries(o).forEach(([a, u]) => {
    const {
      theme: l,
      ...c
    } = u;
    let d = c;
    l && (d = Or({
      ...s,
      ...c
    }, {
      override: c
    }, l)), s[a] = d;
  }), s;
};
function As() {
  const {
    token: n,
    hashed: e,
    theme: t = Ls,
    override: r,
    cssVar: i
  } = h.useContext(lt._internalContext), [o, s, a] = Ri(t, [lt.defaultSeed, n], {
    salt: `${yo}-${e || ""}`,
    override: r,
    getComputedToken: Or,
    cssVar: i && {
      prefix: i.prefix,
      key: i.key,
      unitless: Ps,
      ignore: Ms,
      preserve: Os
    }
  });
  return [t, a, e ? s : "", o, i];
}
const {
  genStyleHooks: Ar
} = Ss({
  usePrefix: () => {
    const {
      getPrefixCls: n,
      iconPrefixCls: e
    } = Ne();
    return {
      iconPrefixCls: e,
      rootPrefixCls: n()
    };
  },
  useToken: () => {
    const [n, e, t, r, i] = As();
    return {
      theme: n,
      realToken: e,
      hashId: t,
      token: r,
      cssVar: i
    };
  },
  useCSP: () => {
    const {
      csp: n
    } = Ne();
    return n ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), $s = (n) => {
  const {
    componentCls: e,
    calc: t
  } = n, r = `${e}-list-card`, i = t(n.fontSize).mul(n.lineHeight).mul(2).add(n.paddingSM).add(n.paddingSM).equal();
  return {
    [r]: {
      borderRadius: n.borderRadius,
      position: "relative",
      background: n.colorFillContent,
      borderWidth: n.lineWidth,
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
        padding: t(n.paddingSM).sub(n.lineWidth).equal(),
        paddingInlineStart: t(n.padding).add(n.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: n.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: t(n.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: t(n.paddingXXS).mul(1.5).equal(),
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
          color: n.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: i,
        height: i,
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
          background: `rgba(0, 0, 0, ${n.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${r}-status-error`]: {
          [`img, ${r}-img-mask`]: {
            borderRadius: t(n.borderRadius).sub(n.lineWidth).equal()
          },
          [`${r}-desc`]: {
            paddingInline: n.paddingXXS
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
        padding: n.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: n.fontSize,
        cursor: "pointer",
        opacity: n.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: n.opacityLoading
        }
      },
      [`&:hover ${r}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: n.colorError,
        [`${r}-desc`]: {
          color: n.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((o) => `${o} ${n.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: t(n.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, en = {
  "&, *": {
    boxSizing: "border-box"
  }
}, ks = (n) => {
  const {
    componentCls: e,
    calc: t,
    antCls: r
  } = n, i = `${e}-drop-area`, o = `${e}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [i]: {
      position: "absolute",
      inset: 0,
      zIndex: n.zIndexPopupBase,
      ...en,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${o}-inner`]: {
          display: "none"
        }
      },
      [o]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [o]: {
        height: "100%",
        borderRadius: n.borderRadius,
        borderWidth: n.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: n.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: n.colorBgPlaceholderHover,
        ...en,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
          padding: 0
        },
        [`&${o}-drag-in`]: {
          borderColor: n.colorPrimaryHover
        },
        [`&${o}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${o}-inner`]: {
          gap: t(n.paddingXXS).div(2).equal()
        },
        [`${o}-icon`]: {
          fontSize: n.fontSizeHeading2,
          lineHeight: 1
        },
        [`${o}-title${o}-title`]: {
          margin: 0,
          fontSize: n.fontSize,
          lineHeight: n.lineHeight
        },
        [`${o}-description`]: {}
      }
    }
  };
}, Is = (n) => {
  const {
    componentCls: e,
    calc: t
  } = n, r = `${e}-list`, i = t(n.fontSize).mul(n.lineHeight).mul(2).add(n.paddingSM).add(n.paddingSM).equal();
  return {
    [e]: {
      position: "relative",
      width: "100%",
      ...en,
      // =============================== File List ===============================
      [r]: {
        display: "flex",
        flexWrap: "wrap",
        gap: n.paddingSM,
        fontSize: n.fontSize,
        lineHeight: n.lineHeight,
        color: n.colorText,
        paddingBlock: n.paddingSM,
        paddingInline: n.padding,
        width: "100%",
        background: n.colorBgContainer,
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
            transition: `opacity ${n.motionDurationSlow}`,
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
          maxHeight: t(i).mul(3).equal(),
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
          width: i,
          height: i,
          fontSize: n.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: n.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: n.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: n.padding
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
}, Ds = (n) => {
  const {
    colorBgContainer: e
  } = n;
  return {
    colorBgPlaceholderHover: new pe(e).setA(0.85).toRgbString()
  };
}, $r = Ar("Attachments", (n) => {
  const e = _t(n, {});
  return [ks(e), Is(e), $s(e)];
}, Ds), Ns = (n) => n.indexOf("image/") === 0, Ze = 200;
function Ws(n) {
  return new Promise((e) => {
    if (!n || !n.type || !Ns(n.type)) {
      e("");
      return;
    }
    const t = new Image();
    if (t.onload = () => {
      const {
        width: r,
        height: i
      } = t, o = r / i, s = o > 1 ? Ze : Ze * o, a = o > 1 ? Ze / o : Ze, u = document.createElement("canvas");
      u.width = s, u.height = a, u.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(u), u.getContext("2d").drawImage(t, 0, 0, s, a);
      const c = u.toDataURL();
      document.body.removeChild(u), window.URL.revokeObjectURL(t.src), e(c);
    }, t.crossOrigin = "anonymous", n.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (t.src = r.result);
      }, r.readAsDataURL(n);
    } else if (n.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && e(r.result);
      }, r.readAsDataURL(n);
    } else
      t.src = window.URL.createObjectURL(n);
  });
}
function Fs() {
  return /* @__PURE__ */ h.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ h.createElement("title", null, "audio"), /* @__PURE__ */ h.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ h.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function js(n) {
  const {
    percent: e
  } = n, {
    token: t
  } = lt.useToken();
  return /* @__PURE__ */ h.createElement(wi, {
    type: "circle",
    percent: e,
    size: t.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ h.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function Bs() {
  return /* @__PURE__ */ h.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ h.createElement("title", null, "video"), /* @__PURE__ */ h.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ h.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const Ft = " ", tn = "#8c8c8c", kr = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], Hs = [{
  icon: /* @__PURE__ */ h.createElement(ni, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ h.createElement(ri, null),
  color: tn,
  ext: kr
}, {
  icon: /* @__PURE__ */ h.createElement(ii, null),
  color: tn,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ h.createElement(oi, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ h.createElement(si, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ h.createElement(ai, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ h.createElement(li, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ h.createElement(Bs, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ h.createElement(Fs, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function zn(n, e) {
  return e.some((t) => n.toLowerCase() === `.${t}`);
}
function zs(n) {
  let e = n;
  const t = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; e >= 1024 && r < t.length - 1; )
    e /= 1024, r++;
  return `${e.toFixed(0)} ${t[r]}`;
}
function Vs(n, e) {
  const {
    prefixCls: t,
    item: r,
    onRemove: i,
    className: o,
    style: s
  } = n, a = h.useContext(je), {
    disabled: u
  } = a || {}, {
    name: l,
    size: c,
    percent: d,
    status: f = "done",
    description: m
  } = r, {
    getPrefixCls: v
  } = Ne(), g = v("attachment", t), p = `${g}-list-card`, [y, S, x] = $r(g), [b, _] = h.useMemo(() => {
    const $ = l || "", D = $.match(/^(.*)\.[^.]+$/);
    return D ? [D[1], $.slice(D[1].length)] : [$, ""];
  }, [l]), C = h.useMemo(() => zn(_, kr), [_]), E = h.useMemo(() => m || (f === "uploading" ? `${d || 0}%` : f === "error" ? r.response || Ft : c ? zs(c) : Ft), [f, d]), [T, I] = h.useMemo(() => {
    for (const {
      ext: $,
      icon: D,
      color: q
    } of Hs)
      if (zn(_, $))
        return [D, q];
    return [/* @__PURE__ */ h.createElement(ei, {
      key: "defaultIcon"
    }), tn];
  }, [_]), [W, N] = h.useState();
  h.useEffect(() => {
    if (r.originFileObj) {
      let $ = !0;
      return Ws(r.originFileObj).then((D) => {
        $ && N(D);
      }), () => {
        $ = !1;
      };
    }
    N(void 0);
  }, [r.originFileObj]);
  let P = null;
  const O = r.thumbUrl || r.url || W, w = C && (r.originFileObj || O);
  return w ? P = /* @__PURE__ */ h.createElement(h.Fragment, null, /* @__PURE__ */ h.createElement("img", {
    alt: "preview",
    src: O
  }), f !== "done" && /* @__PURE__ */ h.createElement("div", {
    className: `${p}-img-mask`
  }, f === "uploading" && d !== void 0 && /* @__PURE__ */ h.createElement(js, {
    percent: d,
    prefixCls: p
  }), f === "error" && /* @__PURE__ */ h.createElement("div", {
    className: `${p}-desc`
  }, /* @__PURE__ */ h.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, E)))) : P = /* @__PURE__ */ h.createElement(h.Fragment, null, /* @__PURE__ */ h.createElement("div", {
    className: `${p}-icon`,
    style: {
      color: I
    }
  }, T), /* @__PURE__ */ h.createElement("div", {
    className: `${p}-content`
  }, /* @__PURE__ */ h.createElement("div", {
    className: `${p}-name`
  }, /* @__PURE__ */ h.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, b ?? Ft), /* @__PURE__ */ h.createElement("div", {
    className: `${p}-ellipsis-suffix`
  }, _)), /* @__PURE__ */ h.createElement("div", {
    className: `${p}-desc`
  }, /* @__PURE__ */ h.createElement("div", {
    className: `${p}-ellipsis-prefix`
  }, E)))), y(/* @__PURE__ */ h.createElement("div", {
    className: Z(p, {
      [`${p}-status-${f}`]: f,
      [`${p}-type-preview`]: w,
      [`${p}-type-overview`]: !w
    }, o, S, x),
    style: s,
    ref: e
  }, P, !u && i && /* @__PURE__ */ h.createElement("button", {
    type: "button",
    className: `${p}-remove`,
    onClick: () => {
      i(r);
    }
  }, /* @__PURE__ */ h.createElement(ti, null))));
}
const Ir = /* @__PURE__ */ h.forwardRef(Vs), Vn = 1;
function Us(n) {
  const {
    prefixCls: e,
    items: t,
    onRemove: r,
    overflow: i,
    upload: o,
    listClassName: s,
    listStyle: a,
    itemClassName: u,
    itemStyle: l
  } = n, c = `${e}-list`, d = h.useRef(null), [f, m] = h.useState(!1), {
    disabled: v
  } = h.useContext(je);
  h.useEffect(() => (m(!0), () => {
    m(!1);
  }), []);
  const [g, p] = h.useState(!1), [y, S] = h.useState(!1), x = () => {
    const E = d.current;
    E && (i === "scrollX" ? (p(Math.abs(E.scrollLeft) >= Vn), S(E.scrollWidth - E.clientWidth - Math.abs(E.scrollLeft) >= Vn)) : i === "scrollY" && (p(E.scrollTop !== 0), S(E.scrollHeight - E.clientHeight !== E.scrollTop)));
  };
  h.useEffect(() => {
    x();
  }, [i]);
  const b = (E) => {
    const T = d.current;
    T && T.scrollTo({
      left: T.scrollLeft + E * T.clientWidth,
      behavior: "smooth"
    });
  }, _ = () => {
    b(-1);
  }, C = () => {
    b(1);
  };
  return /* @__PURE__ */ h.createElement("div", {
    className: Z(c, {
      [`${c}-overflow-${n.overflow}`]: i,
      [`${c}-overflow-ping-start`]: g,
      [`${c}-overflow-ping-end`]: y
    }, s),
    ref: d,
    onScroll: x,
    style: a
  }, /* @__PURE__ */ h.createElement(ls, {
    keys: t.map((E) => ({
      key: E.uid,
      item: E
    })),
    motionName: `${c}-card-motion`,
    component: !1,
    motionAppear: f,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: E,
    item: T,
    className: I,
    style: W
  }) => /* @__PURE__ */ h.createElement(Ir, {
    key: E,
    prefixCls: e,
    item: T,
    onRemove: r,
    className: Z(I, u),
    style: {
      ...W,
      ...l
    }
  })), !v && /* @__PURE__ */ h.createElement(Tr, {
    upload: o
  }, /* @__PURE__ */ h.createElement(_e, {
    className: `${c}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ h.createElement(ci, {
    className: `${c}-upload-btn-icon`
  }))), i === "scrollX" && /* @__PURE__ */ h.createElement(h.Fragment, null, /* @__PURE__ */ h.createElement(_e, {
    size: "small",
    shape: "circle",
    className: `${c}-prev-btn`,
    icon: /* @__PURE__ */ h.createElement(ui, null),
    onClick: _
  }), /* @__PURE__ */ h.createElement(_e, {
    size: "small",
    shape: "circle",
    className: `${c}-next-btn`,
    icon: /* @__PURE__ */ h.createElement(di, null),
    onClick: C
  })));
}
function Xs(n, e) {
  const {
    prefixCls: t,
    placeholder: r = {},
    upload: i,
    className: o,
    style: s
  } = n, a = `${t}-placeholder`, u = r || {}, {
    disabled: l
  } = h.useContext(je), [c, d] = h.useState(!1), f = () => {
    d(!0);
  }, m = (p) => {
    p.currentTarget.contains(p.relatedTarget) || d(!1);
  }, v = () => {
    d(!1);
  }, g = /* @__PURE__ */ h.isValidElement(r) ? r : /* @__PURE__ */ h.createElement(tr, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ h.createElement(Mt.Text, {
    className: `${a}-icon`
  }, u.icon), /* @__PURE__ */ h.createElement(Mt.Title, {
    className: `${a}-title`,
    level: 5
  }, u.title), /* @__PURE__ */ h.createElement(Mt.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, u.description));
  return /* @__PURE__ */ h.createElement("div", {
    className: Z(a, {
      [`${a}-drag-in`]: c,
      [`${a}-disabled`]: l
    }, o),
    onDragEnter: f,
    onDragLeave: m,
    onDrop: v,
    "aria-hidden": l,
    style: s
  }, /* @__PURE__ */ h.createElement(er.Dragger, de({
    showUploadList: !1
  }, i, {
    ref: e,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), g));
}
const Gs = /* @__PURE__ */ h.forwardRef(Xs);
function qs(n, e) {
  const {
    prefixCls: t,
    rootClassName: r,
    rootStyle: i,
    className: o,
    style: s,
    items: a,
    children: u,
    getDropContainer: l,
    placeholder: c,
    onChange: d,
    overflow: f,
    disabled: m,
    classNames: v = {},
    styles: g = {},
    ...p
  } = n, {
    getPrefixCls: y,
    direction: S
  } = Ne(), x = y("attachment", t), b = lr("attachments"), {
    classNames: _,
    styles: C
  } = b, E = h.useRef(null), T = h.useRef(null);
  h.useImperativeHandle(e, () => ({
    nativeElement: E.current,
    upload: (Y) => {
      var M, F;
      const L = (F = (M = T.current) == null ? void 0 : M.nativeElement) == null ? void 0 : F.querySelector('input[type="file"]');
      if (L) {
        const j = new DataTransfer();
        j.items.add(Y), L.files = j.files, L.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [I, W, N] = $r(x), P = Z(W, N), [O, w] = rn([], {
    value: a
  }), $ = ye((Y) => {
    w(Y.fileList), d == null || d(Y);
  }), D = {
    ...p,
    fileList: O,
    onChange: $
  }, q = (Y) => {
    const L = O.filter((M) => M.uid !== Y.uid);
    $({
      file: Y,
      fileList: L
    });
  };
  let K;
  const re = (Y, L, M) => {
    const F = typeof c == "function" ? c(Y) : c;
    return /* @__PURE__ */ h.createElement(Gs, {
      placeholder: F,
      upload: D,
      prefixCls: x,
      className: Z(_.placeholder, v.placeholder),
      style: {
        ...C.placeholder,
        ...g.placeholder,
        ...L == null ? void 0 : L.style
      },
      ref: M
    });
  };
  if (u)
    K = /* @__PURE__ */ h.createElement(h.Fragment, null, /* @__PURE__ */ h.createElement(Tr, {
      upload: D,
      rootClassName: r,
      ref: T
    }, u), /* @__PURE__ */ h.createElement(Tn, {
      getDropContainer: l,
      prefixCls: x,
      className: Z(P, r)
    }, re("drop")));
  else {
    const Y = O.length > 0;
    K = /* @__PURE__ */ h.createElement("div", {
      className: Z(x, P, {
        [`${x}-rtl`]: S === "rtl"
      }, o, r),
      style: {
        ...i,
        ...s
      },
      dir: S || "ltr",
      ref: E
    }, /* @__PURE__ */ h.createElement(Us, {
      prefixCls: x,
      items: O,
      onRemove: q,
      overflow: f,
      upload: D,
      listClassName: Z(_.list, v.list),
      listStyle: {
        ...C.list,
        ...g.list,
        ...!Y && {
          display: "none"
        }
      },
      itemClassName: Z(_.item, v.item),
      itemStyle: {
        ...C.item,
        ...g.item
      }
    }), re("inline", Y ? {
      style: {
        display: "none"
      }
    } : {}, T), /* @__PURE__ */ h.createElement(Tn, {
      getDropContainer: l || (() => E.current),
      prefixCls: x,
      className: P
    }, re("drop")));
  }
  return I(/* @__PURE__ */ h.createElement(je.Provider, {
    value: {
      disabled: m
    }
  }, K));
}
const Dr = /* @__PURE__ */ h.forwardRef(qs);
Dr.FileCard = Ir;
var Ks = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, Ys = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Zs = "".concat(Ks, " ").concat(Ys).split(/[\s\n]+/), Qs = "aria-", Js = "data-";
function Un(n, e) {
  return n.indexOf(e) === 0;
}
function ea(n) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, t;
  e === !1 ? t = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? t = {
    aria: !0
  } : t = k({}, e);
  var r = {};
  return Object.keys(n).forEach(function(i) {
    // Aria
    (t.aria && (i === "role" || Un(i, Qs)) || // Data
    t.data && Un(i, Js) || // Attr
    t.attr && Zs.includes(i)) && (r[i] = n[i]);
  }), r;
}
function ta(n, e) {
  return zr(n, () => {
    const t = e(), {
      nativeElement: r
    } = t;
    return new Proxy(r, {
      get(i, o) {
        return t[o] ? t[o] : Reflect.get(i, o);
      }
    });
  });
}
const Nr = /* @__PURE__ */ R.createContext({}), Xn = () => ({
  height: 0
}), Gn = (n) => ({
  height: n.scrollHeight
});
function na(n) {
  const {
    title: e,
    onOpenChange: t,
    open: r,
    children: i,
    className: o,
    style: s,
    classNames: a = {},
    styles: u = {},
    closable: l,
    forceRender: c
  } = n, {
    prefixCls: d
  } = R.useContext(Nr), f = `${d}-header`;
  return /* @__PURE__ */ R.createElement(Rr, {
    motionEnter: !0,
    motionLeave: !0,
    motionName: `${f}-motion`,
    leavedClassName: `${f}-motion-hidden`,
    onEnterStart: Xn,
    onEnterActive: Gn,
    onLeaveStart: Gn,
    onLeaveActive: Xn,
    visible: r,
    forceRender: c
  }, ({
    className: m,
    style: v
  }) => /* @__PURE__ */ R.createElement("div", {
    className: Z(f, m, o),
    style: {
      ...v,
      ...s
    }
  }, (l !== !1 || e) && /* @__PURE__ */ R.createElement("div", {
    className: (
      // We follow antd naming standard here.
      // So the header part is use `-header` suffix.
      // Though its little bit weird for double `-header`.
      Z(`${f}-header`, a.header)
    ),
    style: {
      ...u.header
    }
  }, /* @__PURE__ */ R.createElement("div", {
    className: `${f}-title`
  }, e), l !== !1 && /* @__PURE__ */ R.createElement("div", {
    className: `${f}-close`
  }, /* @__PURE__ */ R.createElement(_e, {
    type: "text",
    icon: /* @__PURE__ */ R.createElement(fi, null),
    size: "small",
    onClick: () => {
      t == null || t(!r);
    }
  }))), i && /* @__PURE__ */ R.createElement("div", {
    className: Z(`${f}-content`, a.content),
    style: {
      ...u.content
    }
  }, i)));
}
const Rt = /* @__PURE__ */ R.createContext(null);
function ra(n, e) {
  const {
    className: t,
    action: r,
    onClick: i,
    ...o
  } = n, s = R.useContext(Rt), {
    prefixCls: a,
    disabled: u
  } = s, l = s[r], c = u ?? o.disabled ?? s[`${r}Disabled`];
  return /* @__PURE__ */ R.createElement(_e, de({
    type: "text"
  }, o, {
    ref: e,
    onClick: (d) => {
      c || (l && l(), i && i(d));
    },
    className: Z(a, t, {
      [`${a}-disabled`]: c
    })
  }));
}
const Tt = /* @__PURE__ */ R.forwardRef(ra);
function ia(n, e) {
  return /* @__PURE__ */ R.createElement(Tt, de({
    icon: /* @__PURE__ */ R.createElement(hi, null)
  }, n, {
    action: "onClear",
    ref: e
  }));
}
const oa = /* @__PURE__ */ R.forwardRef(ia), sa = /* @__PURE__ */ Vr((n) => {
  const {
    className: e
  } = n;
  return /* @__PURE__ */ h.createElement("svg", {
    color: "currentColor",
    viewBox: "0 0 1000 1000",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink",
    className: e
  }, /* @__PURE__ */ h.createElement("title", null, "Stop Loading"), /* @__PURE__ */ h.createElement("rect", {
    fill: "currentColor",
    height: "250",
    rx: "24",
    ry: "24",
    width: "250",
    x: "375",
    y: "375"
  }), /* @__PURE__ */ h.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    opacity: "0.45"
  }), /* @__PURE__ */ h.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    strokeDasharray: "600 9999999"
  }, /* @__PURE__ */ h.createElement("animateTransform", {
    attributeName: "transform",
    dur: "1s",
    from: "0 500 500",
    repeatCount: "indefinite",
    to: "360 500 500",
    type: "rotate"
  })));
});
function aa(n, e) {
  const {
    prefixCls: t
  } = R.useContext(Rt), {
    className: r
  } = n;
  return /* @__PURE__ */ R.createElement(Tt, de({
    icon: null,
    color: "primary",
    variant: "text",
    shape: "circle"
  }, n, {
    className: Z(r, `${t}-loading-button`),
    action: "onCancel",
    ref: e
  }), /* @__PURE__ */ R.createElement(sa, {
    className: `${t}-loading-icon`
  }));
}
const qn = /* @__PURE__ */ R.forwardRef(aa);
function la(n, e) {
  return /* @__PURE__ */ R.createElement(Tt, de({
    icon: /* @__PURE__ */ R.createElement(pi, null),
    type: "primary",
    shape: "circle"
  }, n, {
    action: "onSend",
    ref: e
  }));
}
const Kn = /* @__PURE__ */ R.forwardRef(la), $e = 1e3, ke = 4, it = 140, Yn = it / 2, Qe = 250, Zn = 500, Je = 0.8;
function ca({
  className: n
}) {
  return /* @__PURE__ */ h.createElement("svg", {
    color: "currentColor",
    viewBox: `0 0 ${$e} ${$e}`,
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink",
    className: n
  }, /* @__PURE__ */ h.createElement("title", null, "Speech Recording"), Array.from({
    length: ke
  }).map((e, t) => {
    const r = ($e - it * ke) / (ke - 1), i = t * (r + it), o = $e / 2 - Qe / 2, s = $e / 2 - Zn / 2;
    return /* @__PURE__ */ h.createElement("rect", {
      fill: "currentColor",
      rx: Yn,
      ry: Yn,
      height: Qe,
      width: it,
      x: i,
      y: o,
      key: t
    }, /* @__PURE__ */ h.createElement("animate", {
      attributeName: "height",
      values: `${Qe}; ${Zn}; ${Qe}`,
      keyTimes: "0; 0.5; 1",
      dur: `${Je}s`,
      begin: `${Je / ke * t}s`,
      repeatCount: "indefinite"
    }), /* @__PURE__ */ h.createElement("animate", {
      attributeName: "y",
      values: `${o}; ${s}; ${o}`,
      keyTimes: "0; 0.5; 1",
      dur: `${Je}s`,
      begin: `${Je / ke * t}s`,
      repeatCount: "indefinite"
    }));
  }));
}
function ua(n, e) {
  const {
    speechRecording: t,
    onSpeechDisabled: r,
    prefixCls: i
  } = R.useContext(Rt);
  let o = null;
  return t ? o = /* @__PURE__ */ R.createElement(ca, {
    className: `${i}-recording-icon`
  }) : r ? o = /* @__PURE__ */ R.createElement(mi, null) : o = /* @__PURE__ */ R.createElement(gi, null), /* @__PURE__ */ R.createElement(Tt, de({
    icon: o,
    color: "primary",
    variant: "text"
  }, n, {
    action: "onSpeech",
    ref: e
  }));
}
const da = /* @__PURE__ */ R.forwardRef(ua), fa = (n) => {
  const {
    componentCls: e,
    calc: t
  } = n, r = `${e}-header`;
  return {
    [e]: {
      [r]: {
        borderBottomWidth: n.lineWidth,
        borderBottomStyle: "solid",
        borderBottomColor: n.colorBorder,
        // ======================== Header ========================
        "&-header": {
          background: n.colorFillAlter,
          fontSize: n.fontSize,
          lineHeight: n.lineHeight,
          paddingBlock: t(n.paddingSM).sub(n.lineWidthBold).equal(),
          paddingInlineStart: n.padding,
          paddingInlineEnd: n.paddingXS,
          display: "flex",
          [`${r}-title`]: {
            flex: "auto"
          }
        },
        // ======================= Content ========================
        "&-content": {
          padding: n.padding
        },
        // ======================== Motion ========================
        "&-motion": {
          transition: ["height", "border"].map((i) => `${i} ${n.motionDurationSlow}`).join(","),
          overflow: "hidden",
          "&-enter-start, &-leave-active": {
            borderBottomColor: "transparent"
          },
          "&-hidden": {
            display: "none"
          }
        }
      }
    }
  };
}, ha = (n) => {
  const {
    componentCls: e,
    padding: t,
    paddingSM: r,
    paddingXS: i,
    lineWidth: o,
    lineWidthBold: s,
    calc: a
  } = n;
  return {
    [e]: {
      position: "relative",
      width: "100%",
      boxSizing: "border-box",
      boxShadow: `${n.boxShadowTertiary}`,
      transition: `background ${n.motionDurationSlow}`,
      // Border
      borderRadius: {
        _skip_check_: !0,
        value: a(n.borderRadius).mul(2).equal()
      },
      borderColor: n.colorBorder,
      borderWidth: 0,
      borderStyle: "solid",
      // Border
      "&:after": {
        content: '""',
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        transition: `border-color ${n.motionDurationSlow}`,
        borderRadius: {
          _skip_check_: !0,
          value: "inherit"
        },
        borderStyle: "inherit",
        borderColor: "inherit",
        borderWidth: o
      },
      // Focus
      "&:focus-within": {
        boxShadow: `${n.boxShadowSecondary}`,
        borderColor: n.colorPrimary,
        "&:after": {
          borderWidth: s
        }
      },
      "&-disabled": {
        background: n.colorBgContainerDisabled
      },
      // ============================== RTL ==============================
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      // ============================ Content ============================
      [`${e}-content`]: {
        display: "flex",
        gap: i,
        width: "100%",
        paddingBlock: r,
        paddingInlineStart: t,
        paddingInlineEnd: r,
        boxSizing: "border-box",
        alignItems: "flex-end"
      },
      // ============================ Prefix =============================
      [`${e}-prefix`]: {
        flex: "none"
      },
      // ============================= Input =============================
      [`${e}-input`]: {
        padding: 0,
        borderRadius: 0,
        flex: "auto",
        alignSelf: "center",
        minHeight: "auto"
      },
      // ============================ Actions ============================
      [`${e}-actions-list`]: {
        flex: "none",
        display: "flex",
        "&-presets": {
          gap: n.paddingXS
        }
      },
      [`${e}-actions-btn`]: {
        "&-disabled": {
          opacity: 0.45
        },
        "&-loading-button": {
          padding: 0,
          border: 0
        },
        "&-loading-icon": {
          height: n.controlHeight,
          width: n.controlHeight,
          verticalAlign: "top"
        },
        "&-recording-icon": {
          height: "1.2em",
          width: "1.2em",
          verticalAlign: "top"
        }
      }
    }
  };
}, pa = () => ({}), ma = Ar("Sender", (n) => {
  const {
    paddingXS: e,
    calc: t
  } = n, r = _t(n, {
    SenderContentMaxWidth: `calc(100% - ${Vt(t(e).add(32).equal())})`
  });
  return [ha(r), fa(r)];
}, pa);
let ut;
!ut && typeof window < "u" && (ut = window.SpeechRecognition || window.webkitSpeechRecognition);
function ga(n, e) {
  const t = ye(n), [r, i, o] = h.useMemo(() => typeof e == "object" ? [e.recording, e.onRecordingChange, typeof e.recording == "boolean"] : [void 0, void 0, !1], [e]), [s, a] = h.useState(null);
  h.useEffect(() => {
    if (typeof navigator < "u" && "permissions" in navigator) {
      let g = null;
      return navigator.permissions.query({
        name: "microphone"
      }).then((p) => {
        a(p.state), p.onchange = function() {
          a(this.state);
        }, g = p;
      }), () => {
        g && (g.onchange = null);
      };
    }
  }, []);
  const u = ut && s !== "denied", l = h.useRef(null), [c, d] = rn(!1, {
    value: r
  }), f = h.useRef(!1), m = () => {
    if (u && !l.current) {
      const g = new ut();
      g.onstart = () => {
        d(!0);
      }, g.onend = () => {
        d(!1);
      }, g.onresult = (p) => {
        var y, S, x;
        if (!f.current) {
          const b = (x = (S = (y = p.results) == null ? void 0 : y[0]) == null ? void 0 : S[0]) == null ? void 0 : x.transcript;
          t(b);
        }
        f.current = !1;
      }, l.current = g;
    }
  }, v = ye((g) => {
    g && !c || (f.current = g, o ? i == null || i(!c) : (m(), l.current && (c ? (l.current.stop(), i == null || i(!1)) : (l.current.start(), i == null || i(!0)))));
  });
  return [u, v, c];
}
function va(n, e, t) {
  return Do(n, e) || t;
}
const ba = /* @__PURE__ */ h.forwardRef((n, e) => {
  const {
    prefixCls: t,
    styles: r = {},
    classNames: i = {},
    className: o,
    rootClassName: s,
    style: a,
    defaultValue: u,
    value: l,
    readOnly: c,
    submitType: d = "enter",
    onSubmit: f,
    loading: m,
    components: v,
    onCancel: g,
    onChange: p,
    actions: y,
    onKeyPress: S,
    onKeyDown: x,
    disabled: b,
    allowSpeech: _,
    prefix: C,
    header: E,
    onPaste: T,
    onPasteFile: I,
    ...W
  } = n, {
    direction: N,
    getPrefixCls: P
  } = Ne(), O = P("sender", t), w = h.useRef(null), $ = h.useRef(null);
  ta(e, () => {
    var A, G;
    return {
      nativeElement: w.current,
      focus: (A = $.current) == null ? void 0 : A.focus,
      blur: (G = $.current) == null ? void 0 : G.blur
    };
  });
  const D = lr("sender"), q = `${O}-input`, [K, re, Y] = ma(O), L = Z(O, D.className, o, s, re, Y, {
    [`${O}-rtl`]: N === "rtl",
    [`${O}-disabled`]: b
  }), M = `${O}-actions-btn`, F = `${O}-actions-list`, [j, H] = rn(u || "", {
    value: l
  }), V = (A, G) => {
    H(A), p && p(A, G);
  }, [J, ie, X] = ga((A) => {
    V(`${j} ${A}`);
  }, _), ce = va(v, ["input"], Si.TextArea), z = {
    ...ea(W, {
      attr: !0,
      aria: !0,
      data: !0
    }),
    ref: $
  }, fe = () => {
    j && f && !m && f(j);
  }, ze = () => {
    V("");
  }, Me = h.useRef(!1), me = () => {
    Me.current = !0;
  }, Pt = () => {
    Me.current = !1;
  }, Ve = (A) => {
    const G = A.key === "Enter" && !Me.current;
    switch (d) {
      case "enter":
        G && !A.shiftKey && (A.preventDefault(), fe());
        break;
      case "shiftEnter":
        G && A.shiftKey && (A.preventDefault(), fe());
        break;
    }
    S && S(A);
  }, Le = (A) => {
    var he;
    const G = (he = A.clipboardData) == null ? void 0 : he.files[0];
    G && I && (I(G), A.preventDefault()), T == null || T(A);
  }, Oe = (A) => {
    var G, he;
    A.target !== ((G = w.current) == null ? void 0 : G.querySelector(`.${q}`)) && A.preventDefault(), (he = $.current) == null || he.focus();
  };
  let Q = /* @__PURE__ */ h.createElement(tr, {
    className: `${F}-presets`
  }, _ && /* @__PURE__ */ h.createElement(da, null), m ? /* @__PURE__ */ h.createElement(qn, null) : /* @__PURE__ */ h.createElement(Kn, null));
  return typeof y == "function" ? Q = y(Q, {
    components: {
      SendButton: Kn,
      ClearButton: oa,
      LoadingButton: qn
    }
  }) : y && (Q = y), K(/* @__PURE__ */ h.createElement("div", {
    ref: w,
    className: L,
    style: {
      ...D.style,
      ...a
    }
  }, E && /* @__PURE__ */ h.createElement(Nr.Provider, {
    value: {
      prefixCls: O
    }
  }, E), /* @__PURE__ */ h.createElement("div", {
    className: `${O}-content`,
    onMouseDown: Oe
  }, C && /* @__PURE__ */ h.createElement("div", {
    className: Z(`${O}-prefix`, D.classNames.prefix, i.prefix),
    style: {
      ...D.styles.prefix,
      ...r.prefix
    }
  }, C), /* @__PURE__ */ h.createElement(ce, de({}, z, {
    disabled: b,
    style: {
      ...D.styles.input,
      ...r.input
    },
    className: Z(q, D.classNames.input, i.input),
    autoSize: {
      maxRows: 8
    },
    value: j,
    onChange: (A) => {
      V(A.target.value, A), ie(!0);
    },
    onPressEnter: Ve,
    onCompositionStart: me,
    onCompositionEnd: Pt,
    onKeyDown: x,
    onPaste: Le,
    variant: "borderless",
    readOnly: c
  })), /* @__PURE__ */ h.createElement("div", {
    className: Z(F, D.classNames.actions, i.actions),
    style: {
      ...D.styles.actions,
      ...r.actions
    }
  }, /* @__PURE__ */ h.createElement(Rt.Provider, {
    value: {
      prefixCls: M,
      onSend: fe,
      onSendDisabled: !j,
      onClear: ze,
      onClearDisabled: !j,
      onCancel: g,
      onCancelDisabled: !m,
      onSpeech: () => ie(!1),
      onSpeechDisabled: !J,
      speechRecording: X,
      disabled: b
    }
  }, Q)))));
}), nn = ba;
nn.Header = na;
function ot(n) {
  const e = se(n);
  return e.current = n, Ur((...t) => {
    var r;
    return (r = e.current) == null ? void 0 : r.call(e, ...t);
  }, []);
}
function ya({
  value: n,
  onValueChange: e
}) {
  const [t, r] = De(n), i = se(e);
  i.current = e;
  const o = se(t);
  return o.current = t, ge(() => {
    i.current(t);
  }, [t]), ge(() => {
    ji(n, o.current) || r(n);
  }, [n]), [t, r];
}
function wa(n, e) {
  return Object.keys(n).reduce((t, r) => (n[r] !== void 0 && n[r] !== null && (t[r] = n[r]), t), {});
}
function jt(n, e, t, r) {
  return new (t || (t = Promise))(function(i, o) {
    function s(l) {
      try {
        u(r.next(l));
      } catch (c) {
        o(c);
      }
    }
    function a(l) {
      try {
        u(r.throw(l));
      } catch (c) {
        o(c);
      }
    }
    function u(l) {
      var c;
      l.done ? i(l.value) : (c = l.value, c instanceof t ? c : new t(function(d) {
        d(c);
      })).then(s, a);
    }
    u((r = r.apply(n, [])).next());
  });
}
class Wr {
  constructor() {
    this.listeners = {};
  }
  on(e, t, r) {
    if (this.listeners[e] || (this.listeners[e] = /* @__PURE__ */ new Set()), this.listeners[e].add(t), r == null ? void 0 : r.once) {
      const i = () => {
        this.un(e, i), this.un(e, t);
      };
      return this.on(e, i), i;
    }
    return () => this.un(e, t);
  }
  un(e, t) {
    var r;
    (r = this.listeners[e]) === null || r === void 0 || r.delete(t);
  }
  once(e, t) {
    return this.on(e, t, {
      once: !0
    });
  }
  unAll() {
    this.listeners = {};
  }
  emit(e, ...t) {
    this.listeners[e] && this.listeners[e].forEach((r) => r(...t));
  }
}
class Sa extends Wr {
  constructor(e) {
    super(), this.subscriptions = [], this.options = e;
  }
  onInit() {
  }
  _init(e) {
    this.wavesurfer = e, this.onInit();
  }
  destroy() {
    this.emit("destroy"), this.subscriptions.forEach((e) => e());
  }
}
class xa extends Wr {
  constructor() {
    super(...arguments), this.unsubscribe = () => {
    };
  }
  start() {
    this.unsubscribe = this.on("tick", () => {
      requestAnimationFrame(() => {
        this.emit("tick");
      });
    }), this.emit("tick");
  }
  stop() {
    this.unsubscribe();
  }
  destroy() {
    this.unsubscribe();
  }
}
const Ca = ["audio/webm", "audio/wav", "audio/mpeg", "audio/mp4", "audio/mp3"];
class cn extends Sa {
  constructor(e) {
    var t, r, i, o, s, a;
    super(Object.assign(Object.assign({}, e), {
      audioBitsPerSecond: (t = e.audioBitsPerSecond) !== null && t !== void 0 ? t : 128e3,
      scrollingWaveform: (r = e.scrollingWaveform) !== null && r !== void 0 && r,
      scrollingWaveformWindow: (i = e.scrollingWaveformWindow) !== null && i !== void 0 ? i : 5,
      continuousWaveform: (o = e.continuousWaveform) !== null && o !== void 0 && o,
      renderRecordedAudio: (s = e.renderRecordedAudio) === null || s === void 0 || s,
      mediaRecorderTimeslice: (a = e.mediaRecorderTimeslice) !== null && a !== void 0 ? a : void 0
    })), this.stream = null, this.mediaRecorder = null, this.dataWindow = null, this.isWaveformPaused = !1, this.lastStartTime = 0, this.lastDuration = 0, this.duration = 0, this.timer = new xa(), this.subscriptions.push(this.timer.on("tick", () => {
      const u = performance.now() - this.lastStartTime;
      this.duration = this.isPaused() ? this.duration : this.lastDuration + u, this.emit("record-progress", this.duration);
    }));
  }
  static create(e) {
    return new cn(e || {});
  }
  renderMicStream(e) {
    var t;
    const r = new AudioContext(), i = r.createMediaStreamSource(e), o = r.createAnalyser();
    i.connect(o), this.options.continuousWaveform && (o.fftSize = 32);
    const s = o.frequencyBinCount, a = new Float32Array(s);
    let u = 0;
    this.wavesurfer && ((t = this.originalOptions) !== null && t !== void 0 || (this.originalOptions = Object.assign({}, this.wavesurfer.options)), this.wavesurfer.options.interact = !1, this.options.scrollingWaveform && (this.wavesurfer.options.cursorWidth = 0));
    const l = setInterval(() => {
      var c, d, f, m;
      if (!this.isWaveformPaused) {
        if (o.getFloatTimeDomainData(a), this.options.scrollingWaveform) {
          const v = Math.floor((this.options.scrollingWaveformWindow || 0) * r.sampleRate), g = Math.min(v, this.dataWindow ? this.dataWindow.length + s : s), p = new Float32Array(v);
          if (this.dataWindow) {
            const y = Math.max(0, v - this.dataWindow.length);
            p.set(this.dataWindow.slice(-g + s), y);
          }
          p.set(a, v - s), this.dataWindow = p;
        } else if (this.options.continuousWaveform) {
          if (!this.dataWindow) {
            const g = this.options.continuousWaveformDuration ? Math.round(100 * this.options.continuousWaveformDuration) : ((d = (c = this.wavesurfer) === null || c === void 0 ? void 0 : c.getWidth()) !== null && d !== void 0 ? d : 0) * window.devicePixelRatio;
            this.dataWindow = new Float32Array(g);
          }
          let v = 0;
          for (let g = 0; g < s; g++) {
            const p = Math.abs(a[g]);
            p > v && (v = p);
          }
          if (u + 1 > this.dataWindow.length) {
            const g = new Float32Array(2 * this.dataWindow.length);
            g.set(this.dataWindow, 0), this.dataWindow = g;
          }
          this.dataWindow[u] = v, u++;
        } else this.dataWindow = a;
        if (this.wavesurfer) {
          const v = ((m = (f = this.dataWindow) === null || f === void 0 ? void 0 : f.length) !== null && m !== void 0 ? m : 0) / 100;
          this.wavesurfer.load("", [this.dataWindow], this.options.scrollingWaveform ? this.options.scrollingWaveformWindow : v).then(() => {
            this.wavesurfer && this.options.continuousWaveform && (this.wavesurfer.setTime(this.getDuration() / 1e3), this.wavesurfer.options.minPxPerSec || this.wavesurfer.setOptions({
              minPxPerSec: this.wavesurfer.getWidth() / this.wavesurfer.getDuration()
            }));
          }).catch((g) => {
            console.error("Error rendering real-time recording data:", g);
          });
        }
      }
    }, 10);
    return {
      onDestroy: () => {
        clearInterval(l), i == null || i.disconnect(), r == null || r.close();
      },
      onEnd: () => {
        this.isWaveformPaused = !0, clearInterval(l), this.stopMic();
      }
    };
  }
  startMic(e) {
    return jt(this, void 0, void 0, function* () {
      let t;
      try {
        t = yield navigator.mediaDevices.getUserMedia({
          audio: !(e != null && e.deviceId) || {
            deviceId: e.deviceId
          }
        });
      } catch (o) {
        throw new Error("Error accessing the microphone: " + o.message);
      }
      const {
        onDestroy: r,
        onEnd: i
      } = this.renderMicStream(t);
      return this.subscriptions.push(this.once("destroy", r)), this.subscriptions.push(this.once("record-end", i)), this.stream = t, t;
    });
  }
  stopMic() {
    this.stream && (this.stream.getTracks().forEach((e) => e.stop()), this.stream = null, this.mediaRecorder = null);
  }
  startRecording(e) {
    return jt(this, void 0, void 0, function* () {
      const t = this.stream || (yield this.startMic(e));
      this.dataWindow = null;
      const r = this.mediaRecorder || new MediaRecorder(t, {
        mimeType: this.options.mimeType || Ca.find((s) => MediaRecorder.isTypeSupported(s)),
        audioBitsPerSecond: this.options.audioBitsPerSecond
      });
      this.mediaRecorder = r, this.stopRecording();
      const i = [];
      r.ondataavailable = (s) => {
        s.data.size > 0 && i.push(s.data), this.emit("record-data-available", s.data);
      };
      const o = (s) => {
        var a;
        const u = new Blob(i, {
          type: r.mimeType
        });
        this.emit(s, u), this.options.renderRecordedAudio && (this.applyOriginalOptionsIfNeeded(), (a = this.wavesurfer) === null || a === void 0 || a.load(URL.createObjectURL(u)));
      };
      r.onpause = () => o("record-pause"), r.onstop = () => o("record-end"), r.start(this.options.mediaRecorderTimeslice), this.lastStartTime = performance.now(), this.lastDuration = 0, this.duration = 0, this.isWaveformPaused = !1, this.timer.start(), this.emit("record-start");
    });
  }
  getDuration() {
    return this.duration;
  }
  isRecording() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) === "recording";
  }
  isPaused() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) === "paused";
  }
  isActive() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) !== "inactive";
  }
  stopRecording() {
    var e;
    this.isActive() && ((e = this.mediaRecorder) === null || e === void 0 || e.stop(), this.timer.stop());
  }
  pauseRecording() {
    var e, t;
    this.isRecording() && (this.isWaveformPaused = !0, (e = this.mediaRecorder) === null || e === void 0 || e.requestData(), (t = this.mediaRecorder) === null || t === void 0 || t.pause(), this.timer.stop(), this.lastDuration = this.duration);
  }
  resumeRecording() {
    var e;
    this.isPaused() && (this.isWaveformPaused = !1, (e = this.mediaRecorder) === null || e === void 0 || e.resume(), this.timer.start(), this.lastStartTime = performance.now(), this.emit("record-resume"));
  }
  static getAvailableAudioDevices() {
    return jt(this, void 0, void 0, function* () {
      return navigator.mediaDevices.enumerateDevices().then((e) => e.filter((t) => t.kind === "audioinput"));
    });
  }
  destroy() {
    this.applyOriginalOptionsIfNeeded(), super.destroy(), this.stopRecording(), this.stopMic();
  }
  applyOriginalOptionsIfNeeded() {
    this.wavesurfer && this.originalOptions && (this.wavesurfer.setOptions(this.originalOptions), delete this.originalOptions);
  }
}
class Be {
  constructor() {
    this.listeners = {};
  }
  /** Subscribe to an event. Returns an unsubscribe function. */
  on(e, t, r) {
    if (this.listeners[e] || (this.listeners[e] = /* @__PURE__ */ new Set()), this.listeners[e].add(t), r != null && r.once) {
      const i = () => {
        this.un(e, i), this.un(e, t);
      };
      return this.on(e, i), i;
    }
    return () => this.un(e, t);
  }
  /** Unsubscribe from an event */
  un(e, t) {
    var r;
    (r = this.listeners[e]) === null || r === void 0 || r.delete(t);
  }
  /** Subscribe to an event only once */
  once(e, t) {
    return this.on(e, t, {
      once: !0
    });
  }
  /** Clear all events */
  unAll() {
    this.listeners = {};
  }
  /** Emit an event */
  emit(e, ...t) {
    this.listeners[e] && this.listeners[e].forEach((r) => r(...t));
  }
}
class Ea extends Be {
  /** Create a plugin instance */
  constructor(e) {
    super(), this.subscriptions = [], this.options = e;
  }
  /** Called after this.wavesurfer is available */
  onInit() {
  }
  /** Do not call directly, only called by WavesSurfer internally */
  _init(e) {
    this.wavesurfer = e, this.onInit();
  }
  /** Destroy the plugin and unsubscribe from all events */
  destroy() {
    this.emit("destroy"), this.subscriptions.forEach((e) => e());
  }
}
var _a = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(c) {
      try {
        l(r.next(c));
      } catch (d) {
        s(d);
      }
    }
    function u(c) {
      try {
        l(r.throw(c));
      } catch (d) {
        s(d);
      }
    }
    function l(c) {
      c.done ? o(c.value) : i(c.value).then(a, u);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
function Ra(n, e) {
  return _a(this, void 0, void 0, function* () {
    const t = new AudioContext({
      sampleRate: e
    });
    return t.decodeAudioData(n).finally(() => t.close());
  });
}
function Ta(n) {
  const e = n[0];
  if (e.some((t) => t > 1 || t < -1)) {
    const t = e.length;
    let r = 0;
    for (let i = 0; i < t; i++) {
      const o = Math.abs(e[i]);
      o > r && (r = o);
    }
    for (const i of n)
      for (let o = 0; o < t; o++)
        i[o] /= r;
  }
  return n;
}
function Pa(n, e) {
  return typeof n[0] == "number" && (n = [n]), Ta(n), {
    duration: e,
    length: n[0].length,
    sampleRate: n[0].length / e,
    numberOfChannels: n.length,
    getChannelData: (t) => n == null ? void 0 : n[t],
    copyFromChannel: AudioBuffer.prototype.copyFromChannel,
    copyToChannel: AudioBuffer.prototype.copyToChannel
  };
}
const et = {
  decode: Ra,
  createBuffer: Pa
};
function Fr(n, e) {
  const t = e.xmlns ? document.createElementNS(e.xmlns, n) : document.createElement(n);
  for (const [r, i] of Object.entries(e))
    if (r === "children")
      for (const [o, s] of Object.entries(e))
        typeof s == "string" ? t.appendChild(document.createTextNode(s)) : t.appendChild(Fr(o, s));
    else r === "style" ? Object.assign(t.style, i) : r === "textContent" ? t.textContent = i : t.setAttribute(r, i.toString());
  return t;
}
function Qn(n, e, t) {
  const r = Fr(n, e || {});
  return t == null || t.appendChild(r), r;
}
const Ma = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  createElement: Qn,
  default: Qn
}, Symbol.toStringTag, {
  value: "Module"
}));
var st = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(c) {
      try {
        l(r.next(c));
      } catch (d) {
        s(d);
      }
    }
    function u(c) {
      try {
        l(r.throw(c));
      } catch (d) {
        s(d);
      }
    }
    function l(c) {
      c.done ? o(c.value) : i(c.value).then(a, u);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
function La(n, e) {
  return st(this, void 0, void 0, function* () {
    if (!n.body || !n.headers) return;
    const t = n.body.getReader(), r = Number(n.headers.get("Content-Length")) || 0;
    let i = 0;
    const o = (a) => st(this, void 0, void 0, function* () {
      i += (a == null ? void 0 : a.length) || 0;
      const u = Math.round(i / r * 100);
      e(u);
    }), s = () => st(this, void 0, void 0, function* () {
      let a;
      try {
        a = yield t.read();
      } catch {
        return;
      }
      a.done || (o(a.value), yield s());
    });
    s();
  });
}
function Oa(n, e, t) {
  return st(this, void 0, void 0, function* () {
    const r = yield fetch(n, t);
    if (r.status >= 400)
      throw new Error(`Failed to fetch ${n}: ${r.status} (${r.statusText})`);
    return La(r.clone(), e), r.blob();
  });
}
const Aa = {
  fetchBlob: Oa
};
var $a = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(c) {
      try {
        l(r.next(c));
      } catch (d) {
        s(d);
      }
    }
    function u(c) {
      try {
        l(r.throw(c));
      } catch (d) {
        s(d);
      }
    }
    function l(c) {
      c.done ? o(c.value) : i(c.value).then(a, u);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
class ka extends Be {
  constructor(e) {
    super(), this.isExternalMedia = !1, e.media ? (this.media = e.media, this.isExternalMedia = !0) : this.media = document.createElement("audio"), e.mediaControls && (this.media.controls = !0), e.autoplay && (this.media.autoplay = !0), e.playbackRate != null && this.onMediaEvent("canplay", () => {
      e.playbackRate != null && (this.media.playbackRate = e.playbackRate);
    }, {
      once: !0
    });
  }
  onMediaEvent(e, t, r) {
    return this.media.addEventListener(e, t, r), () => this.media.removeEventListener(e, t, r);
  }
  getSrc() {
    return this.media.currentSrc || this.media.src || "";
  }
  revokeSrc() {
    const e = this.getSrc();
    e.startsWith("blob:") && URL.revokeObjectURL(e);
  }
  canPlayType(e) {
    return this.media.canPlayType(e) !== "";
  }
  setSrc(e, t) {
    const r = this.getSrc();
    if (e && r === e) return;
    this.revokeSrc();
    const i = t instanceof Blob && (this.canPlayType(t.type) || !e) ? URL.createObjectURL(t) : e;
    r && (this.media.src = "");
    try {
      this.media.src = i;
    } catch {
      this.media.src = e;
    }
  }
  destroy() {
    this.isExternalMedia || (this.media.pause(), this.media.remove(), this.revokeSrc(), this.media.src = "", this.media.load());
  }
  setMediaElement(e) {
    this.media = e;
  }
  /** Start playing the audio */
  play() {
    return $a(this, void 0, void 0, function* () {
      return this.media.play();
    });
  }
  /** Pause the audio */
  pause() {
    this.media.pause();
  }
  /** Check if the audio is playing */
  isPlaying() {
    return !this.media.paused && !this.media.ended;
  }
  /** Jump to a specific time in the audio (in seconds) */
  setTime(e) {
    this.media.currentTime = Math.max(0, Math.min(e, this.getDuration()));
  }
  /** Get the duration of the audio in seconds */
  getDuration() {
    return this.media.duration;
  }
  /** Get the current audio position in seconds */
  getCurrentTime() {
    return this.media.currentTime;
  }
  /** Get the audio volume */
  getVolume() {
    return this.media.volume;
  }
  /** Set the audio volume */
  setVolume(e) {
    this.media.volume = e;
  }
  /** Get the audio muted state */
  getMuted() {
    return this.media.muted;
  }
  /** Mute or unmute the audio */
  setMuted(e) {
    this.media.muted = e;
  }
  /** Get the playback speed */
  getPlaybackRate() {
    return this.media.playbackRate;
  }
  /** Check if the audio is seeking */
  isSeeking() {
    return this.media.seeking;
  }
  /** Set the playback speed, pass an optional false to NOT preserve the pitch */
  setPlaybackRate(e, t) {
    t != null && (this.media.preservesPitch = t), this.media.playbackRate = e;
  }
  /** Get the HTML media element */
  getMediaElement() {
    return this.media;
  }
  /** Set a sink id to change the audio output device */
  setSinkId(e) {
    return this.media.setSinkId(e);
  }
}
function Ia(n, e, t, r, i = 3, o = 0, s = 100) {
  if (!n) return () => {
  };
  const a = matchMedia("(pointer: coarse)").matches;
  let u = () => {
  };
  const l = (c) => {
    if (c.button !== o) return;
    c.preventDefault(), c.stopPropagation();
    let d = c.clientX, f = c.clientY, m = !1;
    const v = Date.now(), g = (b) => {
      if (b.preventDefault(), b.stopPropagation(), a && Date.now() - v < s) return;
      const _ = b.clientX, C = b.clientY, E = _ - d, T = C - f;
      if (m || Math.abs(E) > i || Math.abs(T) > i) {
        const I = n.getBoundingClientRect(), {
          left: W,
          top: N
        } = I;
        m || (t == null || t(d - W, f - N), m = !0), e(E, T, _ - W, C - N), d = _, f = C;
      }
    }, p = (b) => {
      if (m) {
        const _ = b.clientX, C = b.clientY, E = n.getBoundingClientRect(), {
          left: T,
          top: I
        } = E;
        r == null || r(_ - T, C - I);
      }
      u();
    }, y = (b) => {
      (!b.relatedTarget || b.relatedTarget === document.documentElement) && p(b);
    }, S = (b) => {
      m && (b.stopPropagation(), b.preventDefault());
    }, x = (b) => {
      m && b.preventDefault();
    };
    document.addEventListener("pointermove", g), document.addEventListener("pointerup", p), document.addEventListener("pointerout", y), document.addEventListener("pointercancel", y), document.addEventListener("touchmove", x, {
      passive: !1
    }), document.addEventListener("click", S, {
      capture: !0
    }), u = () => {
      document.removeEventListener("pointermove", g), document.removeEventListener("pointerup", p), document.removeEventListener("pointerout", y), document.removeEventListener("pointercancel", y), document.removeEventListener("touchmove", x), setTimeout(() => {
        document.removeEventListener("click", S, {
          capture: !0
        });
      }, 10);
    };
  };
  return n.addEventListener("pointerdown", l), () => {
    u(), n.removeEventListener("pointerdown", l);
  };
}
var Jn = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(c) {
      try {
        l(r.next(c));
      } catch (d) {
        s(d);
      }
    }
    function u(c) {
      try {
        l(r.throw(c));
      } catch (d) {
        s(d);
      }
    }
    function l(c) {
      c.done ? o(c.value) : i(c.value).then(a, u);
    }
    l((r = r.apply(n, e || [])).next());
  });
}, Da = function(n, e) {
  var t = {};
  for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && e.indexOf(r) < 0 && (t[r] = n[r]);
  if (n != null && typeof Object.getOwnPropertySymbols == "function") for (var i = 0, r = Object.getOwnPropertySymbols(n); i < r.length; i++)
    e.indexOf(r[i]) < 0 && Object.prototype.propertyIsEnumerable.call(n, r[i]) && (t[r[i]] = n[r[i]]);
  return t;
};
class Re extends Be {
  constructor(e, t) {
    super(), this.timeouts = [], this.isScrollable = !1, this.audioData = null, this.resizeObserver = null, this.lastContainerWidth = 0, this.isDragging = !1, this.subscriptions = [], this.unsubscribeOnScroll = [], this.subscriptions = [], this.options = e;
    const r = this.parentFromOptionsContainer(e.container);
    this.parent = r;
    const [i, o] = this.initHtml();
    r.appendChild(i), this.container = i, this.scrollContainer = o.querySelector(".scroll"), this.wrapper = o.querySelector(".wrapper"), this.canvasWrapper = o.querySelector(".canvases"), this.progressWrapper = o.querySelector(".progress"), this.cursor = o.querySelector(".cursor"), t && o.appendChild(t), this.initEvents();
  }
  parentFromOptionsContainer(e) {
    let t;
    if (typeof e == "string" ? t = document.querySelector(e) : e instanceof HTMLElement && (t = e), !t)
      throw new Error("Container not found");
    return t;
  }
  initEvents() {
    const e = (t) => {
      const r = this.wrapper.getBoundingClientRect(), i = t.clientX - r.left, o = t.clientY - r.top, s = i / r.width, a = o / r.height;
      return [s, a];
    };
    if (this.wrapper.addEventListener("click", (t) => {
      const [r, i] = e(t);
      this.emit("click", r, i);
    }), this.wrapper.addEventListener("dblclick", (t) => {
      const [r, i] = e(t);
      this.emit("dblclick", r, i);
    }), (this.options.dragToSeek === !0 || typeof this.options.dragToSeek == "object") && this.initDrag(), this.scrollContainer.addEventListener("scroll", () => {
      const {
        scrollLeft: t,
        scrollWidth: r,
        clientWidth: i
      } = this.scrollContainer, o = t / r, s = (t + i) / r;
      this.emit("scroll", o, s, t, t + i);
    }), typeof ResizeObserver == "function") {
      const t = this.createDelay(100);
      this.resizeObserver = new ResizeObserver(() => {
        t().then(() => this.onContainerResize()).catch(() => {
        });
      }), this.resizeObserver.observe(this.scrollContainer);
    }
  }
  onContainerResize() {
    const e = this.parent.clientWidth;
    e === this.lastContainerWidth && this.options.height !== "auto" || (this.lastContainerWidth = e, this.reRender());
  }
  initDrag() {
    this.subscriptions.push(Ia(
      this.wrapper,
      // On drag
      (e, t, r) => {
        this.emit("drag", Math.max(0, Math.min(1, r / this.wrapper.getBoundingClientRect().width)));
      },
      // On start drag
      (e) => {
        this.isDragging = !0, this.emit("dragstart", Math.max(0, Math.min(1, e / this.wrapper.getBoundingClientRect().width)));
      },
      // On end drag
      (e) => {
        this.isDragging = !1, this.emit("dragend", Math.max(0, Math.min(1, e / this.wrapper.getBoundingClientRect().width)));
      }
    ));
  }
  getHeight(e, t) {
    var r;
    const o = ((r = this.audioData) === null || r === void 0 ? void 0 : r.numberOfChannels) || 1;
    if (e == null) return 128;
    if (!isNaN(Number(e))) return Number(e);
    if (e === "auto") {
      const s = this.parent.clientHeight || 128;
      return t != null && t.every((a) => !a.overlay) ? s / o : s;
    }
    return 128;
  }
  initHtml() {
    const e = document.createElement("div"), t = e.attachShadow({
      mode: "open"
    }), r = this.options.cspNonce && typeof this.options.cspNonce == "string" ? this.options.cspNonce.replace(/"/g, "") : "";
    return t.innerHTML = `
      <style${r ? ` nonce="${r}"` : ""}>
        :host {
          user-select: none;
          min-width: 1px;
        }
        :host audio {
          display: block;
          width: 100%;
        }
        :host .scroll {
          overflow-x: auto;
          overflow-y: hidden;
          width: 100%;
          position: relative;
        }
        :host .noScrollbar {
          scrollbar-color: transparent;
          scrollbar-width: none;
        }
        :host .noScrollbar::-webkit-scrollbar {
          display: none;
          -webkit-appearance: none;
        }
        :host .wrapper {
          position: relative;
          overflow: visible;
          z-index: 2;
        }
        :host .canvases {
          min-height: ${this.getHeight(this.options.height, this.options.splitChannels)}px;
        }
        :host .canvases > div {
          position: relative;
        }
        :host canvas {
          display: block;
          position: absolute;
          top: 0;
          image-rendering: pixelated;
        }
        :host .progress {
          pointer-events: none;
          position: absolute;
          z-index: 2;
          top: 0;
          left: 0;
          width: 0;
          height: 100%;
          overflow: hidden;
        }
        :host .progress > div {
          position: relative;
        }
        :host .cursor {
          pointer-events: none;
          position: absolute;
          z-index: 5;
          top: 0;
          left: 0;
          height: 100%;
          border-radius: 2px;
        }
      </style>

      <div class="scroll" part="scroll">
        <div class="wrapper" part="wrapper">
          <div class="canvases" part="canvases"></div>
          <div class="progress" part="progress"></div>
          <div class="cursor" part="cursor"></div>
        </div>
      </div>
    `, [e, t];
  }
  /** Wavesurfer itself calls this method. Do not call it manually. */
  setOptions(e) {
    if (this.options.container !== e.container) {
      const t = this.parentFromOptionsContainer(e.container);
      t.appendChild(this.container), this.parent = t;
    }
    (e.dragToSeek === !0 || typeof this.options.dragToSeek == "object") && this.initDrag(), this.options = e, this.reRender();
  }
  getWrapper() {
    return this.wrapper;
  }
  getWidth() {
    return this.scrollContainer.clientWidth;
  }
  getScroll() {
    return this.scrollContainer.scrollLeft;
  }
  setScroll(e) {
    this.scrollContainer.scrollLeft = e;
  }
  setScrollPercentage(e) {
    const {
      scrollWidth: t
    } = this.scrollContainer, r = t * e;
    this.setScroll(r);
  }
  destroy() {
    var e, t;
    this.subscriptions.forEach((r) => r()), this.container.remove(), (e = this.resizeObserver) === null || e === void 0 || e.disconnect(), (t = this.unsubscribeOnScroll) === null || t === void 0 || t.forEach((r) => r()), this.unsubscribeOnScroll = [];
  }
  createDelay(e = 10) {
    let t, r;
    const i = () => {
      t && clearTimeout(t), r && r();
    };
    return this.timeouts.push(i), () => new Promise((o, s) => {
      i(), r = s, t = setTimeout(() => {
        t = void 0, r = void 0, o();
      }, e);
    });
  }
  // Convert array of color values to linear gradient
  convertColorValues(e) {
    if (!Array.isArray(e)) return e || "";
    if (e.length < 2) return e[0] || "";
    const t = document.createElement("canvas"), r = t.getContext("2d"), i = t.height * (window.devicePixelRatio || 1), o = r.createLinearGradient(0, 0, 0, i), s = 1 / (e.length - 1);
    return e.forEach((a, u) => {
      const l = u * s;
      o.addColorStop(l, a);
    }), o;
  }
  getPixelRatio() {
    return Math.max(1, window.devicePixelRatio || 1);
  }
  renderBarWaveform(e, t, r, i) {
    const o = e[0], s = e[1] || e[0], a = o.length, {
      width: u,
      height: l
    } = r.canvas, c = l / 2, d = this.getPixelRatio(), f = t.barWidth ? t.barWidth * d : 1, m = t.barGap ? t.barGap * d : t.barWidth ? f / 2 : 0, v = t.barRadius || 0, g = u / (f + m) / a, p = v && "roundRect" in r ? "roundRect" : "rect";
    r.beginPath();
    let y = 0, S = 0, x = 0;
    for (let b = 0; b <= a; b++) {
      const _ = Math.round(b * g);
      if (_ > y) {
        const T = Math.round(S * c * i), I = Math.round(x * c * i), W = T + I || 1;
        let N = c - T;
        t.barAlign === "top" ? N = 0 : t.barAlign === "bottom" && (N = l - W), r[p](y * (f + m), N, f, W, v), y = _, S = 0, x = 0;
      }
      const C = Math.abs(o[b] || 0), E = Math.abs(s[b] || 0);
      C > S && (S = C), E > x && (x = E);
    }
    r.fill(), r.closePath();
  }
  renderLineWaveform(e, t, r, i) {
    const o = (s) => {
      const a = e[s] || e[0], u = a.length, {
        height: l
      } = r.canvas, c = l / 2, d = r.canvas.width / u;
      r.moveTo(0, c);
      let f = 0, m = 0;
      for (let v = 0; v <= u; v++) {
        const g = Math.round(v * d);
        if (g > f) {
          const y = Math.round(m * c * i) || 1, S = c + y * (s === 0 ? -1 : 1);
          r.lineTo(f, S), f = g, m = 0;
        }
        const p = Math.abs(a[v] || 0);
        p > m && (m = p);
      }
      r.lineTo(f, c);
    };
    r.beginPath(), o(0), o(1), r.fill(), r.closePath();
  }
  renderWaveform(e, t, r) {
    if (r.fillStyle = this.convertColorValues(t.waveColor), t.renderFunction) {
      t.renderFunction(e, r);
      return;
    }
    let i = t.barHeight || 1;
    if (t.normalize) {
      const o = Array.from(e[0]).reduce((s, a) => Math.max(s, Math.abs(a)), 0);
      i = o ? 1 / o : 1;
    }
    if (t.barWidth || t.barGap || t.barAlign) {
      this.renderBarWaveform(e, t, r, i);
      return;
    }
    this.renderLineWaveform(e, t, r, i);
  }
  renderSingleCanvas(e, t, r, i, o, s, a) {
    const u = this.getPixelRatio(), l = document.createElement("canvas");
    l.width = Math.round(r * u), l.height = Math.round(i * u), l.style.width = `${r}px`, l.style.height = `${i}px`, l.style.left = `${Math.round(o)}px`, s.appendChild(l);
    const c = l.getContext("2d");
    if (this.renderWaveform(e, t, c), l.width > 0 && l.height > 0) {
      const d = l.cloneNode(), f = d.getContext("2d");
      f.drawImage(l, 0, 0), f.globalCompositeOperation = "source-in", f.fillStyle = this.convertColorValues(t.progressColor), f.fillRect(0, 0, l.width, l.height), a.appendChild(d);
    }
  }
  renderMultiCanvas(e, t, r, i, o, s) {
    const a = this.getPixelRatio(), {
      clientWidth: u
    } = this.scrollContainer, l = r / a;
    let c = Math.min(Re.MAX_CANVAS_WIDTH, u, l), d = {};
    if (c === 0) return;
    if (t.barWidth || t.barGap) {
      const y = t.barWidth || 0.5, S = t.barGap || y / 2, x = y + S;
      c % x !== 0 && (c = Math.floor(c / x) * x);
    }
    const f = (y) => {
      if (y < 0 || y >= v || d[y]) return;
      d[y] = !0;
      const S = y * c, x = Math.min(l - S, c);
      if (x <= 0) return;
      const b = e.map((_) => {
        const C = Math.floor(S / l * _.length), E = Math.floor((S + x) / l * _.length);
        return _.slice(C, E);
      });
      this.renderSingleCanvas(b, t, x, i, S, o, s);
    }, m = () => {
      Object.keys(d).length > Re.MAX_NODES && (o.innerHTML = "", s.innerHTML = "", d = {});
    }, v = Math.ceil(l / c);
    if (!this.isScrollable) {
      for (let y = 0; y < v; y++)
        f(y);
      return;
    }
    const g = this.scrollContainer.scrollLeft / l, p = Math.floor(g * v);
    if (f(p - 1), f(p), f(p + 1), v > 1) {
      const y = this.on("scroll", () => {
        const {
          scrollLeft: S
        } = this.scrollContainer, x = Math.floor(S / l * v);
        m(), f(x - 1), f(x), f(x + 1);
      });
      this.unsubscribeOnScroll.push(y);
    }
  }
  renderChannel(e, t, r, i) {
    var {
      overlay: o
    } = t, s = Da(t, ["overlay"]);
    const a = document.createElement("div"), u = this.getHeight(s.height, s.splitChannels);
    a.style.height = `${u}px`, o && i > 0 && (a.style.marginTop = `-${u}px`), this.canvasWrapper.style.minHeight = `${u}px`, this.canvasWrapper.appendChild(a);
    const l = a.cloneNode();
    this.progressWrapper.appendChild(l), this.renderMultiCanvas(e, s, r, u, a, l);
  }
  render(e) {
    return Jn(this, void 0, void 0, function* () {
      var t;
      this.timeouts.forEach((u) => u()), this.timeouts = [], this.canvasWrapper.innerHTML = "", this.progressWrapper.innerHTML = "", this.options.width != null && (this.scrollContainer.style.width = typeof this.options.width == "number" ? `${this.options.width}px` : this.options.width);
      const r = this.getPixelRatio(), i = this.scrollContainer.clientWidth, o = Math.ceil(e.duration * (this.options.minPxPerSec || 0));
      this.isScrollable = o > i;
      const s = this.options.fillParent && !this.isScrollable, a = (s ? i : o) * r;
      if (this.wrapper.style.width = s ? "100%" : `${o}px`, this.scrollContainer.style.overflowX = this.isScrollable ? "auto" : "hidden", this.scrollContainer.classList.toggle("noScrollbar", !!this.options.hideScrollbar), this.cursor.style.backgroundColor = `${this.options.cursorColor || this.options.progressColor}`, this.cursor.style.width = `${this.options.cursorWidth}px`, this.audioData = e, this.emit("render"), this.options.splitChannels)
        for (let u = 0; u < e.numberOfChannels; u++) {
          const l = Object.assign(Object.assign({}, this.options), (t = this.options.splitChannels) === null || t === void 0 ? void 0 : t[u]);
          this.renderChannel([e.getChannelData(u)], l, a, u);
        }
      else {
        const u = [e.getChannelData(0)];
        e.numberOfChannels > 1 && u.push(e.getChannelData(1)), this.renderChannel(u, this.options, a, 0);
      }
      Promise.resolve().then(() => this.emit("rendered"));
    });
  }
  reRender() {
    if (this.unsubscribeOnScroll.forEach((r) => r()), this.unsubscribeOnScroll = [], !this.audioData) return;
    const {
      scrollWidth: e
    } = this.scrollContainer, {
      right: t
    } = this.progressWrapper.getBoundingClientRect();
    if (this.render(this.audioData), this.isScrollable && e !== this.scrollContainer.scrollWidth) {
      const {
        right: r
      } = this.progressWrapper.getBoundingClientRect();
      let i = r - t;
      i *= 2, i = i < 0 ? Math.floor(i) : Math.ceil(i), i /= 2, this.scrollContainer.scrollLeft += i;
    }
  }
  zoom(e) {
    this.options.minPxPerSec = e, this.reRender();
  }
  scrollIntoView(e, t = !1) {
    const {
      scrollLeft: r,
      scrollWidth: i,
      clientWidth: o
    } = this.scrollContainer, s = e * i, a = r, u = r + o, l = o / 2;
    if (this.isDragging)
      s + 30 > u ? this.scrollContainer.scrollLeft += 30 : s - 30 < a && (this.scrollContainer.scrollLeft -= 30);
    else {
      (s < a || s > u) && (this.scrollContainer.scrollLeft = s - (this.options.autoCenter ? l : 0));
      const c = s - r - l;
      t && this.options.autoCenter && c > 0 && (this.scrollContainer.scrollLeft += Math.min(c, 10));
    }
    {
      const c = this.scrollContainer.scrollLeft, d = c / i, f = (c + o) / i;
      this.emit("scroll", d, f, c, c + o);
    }
  }
  renderProgress(e, t) {
    if (isNaN(e)) return;
    const r = e * 100;
    this.canvasWrapper.style.clipPath = `polygon(${r}% 0, 100% 0, 100% 100%, ${r}% 100%)`, this.progressWrapper.style.width = `${r}%`, this.cursor.style.left = `${r}%`, this.cursor.style.transform = `translateX(-${Math.round(r) === 100 ? this.options.cursorWidth : 0}px)`, this.isScrollable && this.options.autoScroll && this.scrollIntoView(e, t);
  }
  exportImage(e, t, r) {
    return Jn(this, void 0, void 0, function* () {
      const i = this.canvasWrapper.querySelectorAll("canvas");
      if (!i.length)
        throw new Error("No waveform data");
      if (r === "dataURL") {
        const o = Array.from(i).map((s) => s.toDataURL(e, t));
        return Promise.resolve(o);
      }
      return Promise.all(Array.from(i).map((o) => new Promise((s, a) => {
        o.toBlob((u) => {
          u ? s(u) : a(new Error("Could not export image"));
        }, e, t);
      })));
    });
  }
}
Re.MAX_CANVAS_WIDTH = 8e3;
Re.MAX_NODES = 10;
class Na extends Be {
  constructor() {
    super(...arguments), this.unsubscribe = () => {
    };
  }
  start() {
    this.unsubscribe = this.on("tick", () => {
      requestAnimationFrame(() => {
        this.emit("tick");
      });
    }), this.emit("tick");
  }
  stop() {
    this.unsubscribe();
  }
  destroy() {
    this.unsubscribe();
  }
}
var Bt = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(c) {
      try {
        l(r.next(c));
      } catch (d) {
        s(d);
      }
    }
    function u(c) {
      try {
        l(r.throw(c));
      } catch (d) {
        s(d);
      }
    }
    function l(c) {
      c.done ? o(c.value) : i(c.value).then(a, u);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
class Ht extends Be {
  constructor(e = new AudioContext()) {
    super(), this.bufferNode = null, this.playStartTime = 0, this.playedDuration = 0, this._muted = !1, this._playbackRate = 1, this._duration = void 0, this.buffer = null, this.currentSrc = "", this.paused = !0, this.crossOrigin = null, this.seeking = !1, this.autoplay = !1, this.addEventListener = this.on, this.removeEventListener = this.un, this.audioContext = e, this.gainNode = this.audioContext.createGain(), this.gainNode.connect(this.audioContext.destination);
  }
  load() {
    return Bt(this, void 0, void 0, function* () {
    });
  }
  get src() {
    return this.currentSrc;
  }
  set src(e) {
    if (this.currentSrc = e, this._duration = void 0, !e) {
      this.buffer = null, this.emit("emptied");
      return;
    }
    fetch(e).then((t) => {
      if (t.status >= 400)
        throw new Error(`Failed to fetch ${e}: ${t.status} (${t.statusText})`);
      return t.arrayBuffer();
    }).then((t) => this.currentSrc !== e ? null : this.audioContext.decodeAudioData(t)).then((t) => {
      this.currentSrc === e && (this.buffer = t, this.emit("loadedmetadata"), this.emit("canplay"), this.autoplay && this.play());
    });
  }
  _play() {
    var e;
    if (!this.paused) return;
    this.paused = !1, (e = this.bufferNode) === null || e === void 0 || e.disconnect(), this.bufferNode = this.audioContext.createBufferSource(), this.buffer && (this.bufferNode.buffer = this.buffer), this.bufferNode.playbackRate.value = this._playbackRate, this.bufferNode.connect(this.gainNode);
    let t = this.playedDuration * this._playbackRate;
    (t >= this.duration || t < 0) && (t = 0, this.playedDuration = 0), this.bufferNode.start(this.audioContext.currentTime, t), this.playStartTime = this.audioContext.currentTime, this.bufferNode.onended = () => {
      this.currentTime >= this.duration && (this.pause(), this.emit("ended"));
    };
  }
  _pause() {
    var e;
    this.paused = !0, (e = this.bufferNode) === null || e === void 0 || e.stop(), this.playedDuration += this.audioContext.currentTime - this.playStartTime;
  }
  play() {
    return Bt(this, void 0, void 0, function* () {
      this.paused && (this._play(), this.emit("play"));
    });
  }
  pause() {
    this.paused || (this._pause(), this.emit("pause"));
  }
  stopAt(e) {
    var t, r;
    const i = e - this.currentTime;
    (t = this.bufferNode) === null || t === void 0 || t.stop(this.audioContext.currentTime + i), (r = this.bufferNode) === null || r === void 0 || r.addEventListener("ended", () => {
      this.bufferNode = null, this.pause();
    }, {
      once: !0
    });
  }
  setSinkId(e) {
    return Bt(this, void 0, void 0, function* () {
      return this.audioContext.setSinkId(e);
    });
  }
  get playbackRate() {
    return this._playbackRate;
  }
  set playbackRate(e) {
    this._playbackRate = e, this.bufferNode && (this.bufferNode.playbackRate.value = e);
  }
  get currentTime() {
    return (this.paused ? this.playedDuration : this.playedDuration + (this.audioContext.currentTime - this.playStartTime)) * this._playbackRate;
  }
  set currentTime(e) {
    const t = !this.paused;
    t && this._pause(), this.playedDuration = e / this._playbackRate, t && this._play(), this.emit("seeking"), this.emit("timeupdate");
  }
  get duration() {
    var e, t;
    return (e = this._duration) !== null && e !== void 0 ? e : ((t = this.buffer) === null || t === void 0 ? void 0 : t.duration) || 0;
  }
  set duration(e) {
    this._duration = e;
  }
  get volume() {
    return this.gainNode.gain.value;
  }
  set volume(e) {
    this.gainNode.gain.value = e, this.emit("volumechange");
  }
  get muted() {
    return this._muted;
  }
  set muted(e) {
    this._muted !== e && (this._muted = e, this._muted ? this.gainNode.disconnect() : this.gainNode.connect(this.audioContext.destination));
  }
  canPlayType(e) {
    return /^(audio|video)\//.test(e);
  }
  /** Get the GainNode used to play the audio. Can be used to attach filters. */
  getGainNode() {
    return this.gainNode;
  }
  /** Get decoded audio */
  getChannelData() {
    const e = [];
    if (!this.buffer) return e;
    const t = this.buffer.numberOfChannels;
    for (let r = 0; r < t; r++)
      e.push(this.buffer.getChannelData(r));
    return e;
  }
}
var Se = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(c) {
      try {
        l(r.next(c));
      } catch (d) {
        s(d);
      }
    }
    function u(c) {
      try {
        l(r.throw(c));
      } catch (d) {
        s(d);
      }
    }
    function l(c) {
      c.done ? o(c.value) : i(c.value).then(a, u);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
const Wa = {
  waveColor: "#999",
  progressColor: "#555",
  cursorWidth: 1,
  minPxPerSec: 0,
  fillParent: !0,
  interact: !0,
  dragToSeek: !1,
  autoScroll: !0,
  autoCenter: !0,
  sampleRate: 8e3
};
class He extends ka {
  /** Create a new WaveSurfer instance */
  static create(e) {
    return new He(e);
  }
  /** Create a new WaveSurfer instance */
  constructor(e) {
    const t = e.media || (e.backend === "WebAudio" ? new Ht() : void 0);
    super({
      media: t,
      mediaControls: e.mediaControls,
      autoplay: e.autoplay,
      playbackRate: e.audioRate
    }), this.plugins = [], this.decodedData = null, this.stopAtPosition = null, this.subscriptions = [], this.mediaSubscriptions = [], this.abortController = null, this.options = Object.assign({}, Wa, e), this.timer = new Na();
    const r = t ? void 0 : this.getMediaElement();
    this.renderer = new Re(this.options, r), this.initPlayerEvents(), this.initRendererEvents(), this.initTimerEvents(), this.initPlugins();
    const i = this.options.url || this.getSrc() || "";
    Promise.resolve().then(() => {
      this.emit("init");
      const {
        peaks: o,
        duration: s
      } = this.options;
      (i || o && s) && this.load(i, o, s).catch(() => null);
    });
  }
  updateProgress(e = this.getCurrentTime()) {
    return this.renderer.renderProgress(e / this.getDuration(), this.isPlaying()), e;
  }
  initTimerEvents() {
    this.subscriptions.push(this.timer.on("tick", () => {
      if (!this.isSeeking()) {
        const e = this.updateProgress();
        this.emit("timeupdate", e), this.emit("audioprocess", e), this.stopAtPosition != null && this.isPlaying() && e >= this.stopAtPosition && this.pause();
      }
    }));
  }
  initPlayerEvents() {
    this.isPlaying() && (this.emit("play"), this.timer.start()), this.mediaSubscriptions.push(this.onMediaEvent("timeupdate", () => {
      const e = this.updateProgress();
      this.emit("timeupdate", e);
    }), this.onMediaEvent("play", () => {
      this.emit("play"), this.timer.start();
    }), this.onMediaEvent("pause", () => {
      this.emit("pause"), this.timer.stop(), this.stopAtPosition = null;
    }), this.onMediaEvent("emptied", () => {
      this.timer.stop(), this.stopAtPosition = null;
    }), this.onMediaEvent("ended", () => {
      this.emit("timeupdate", this.getDuration()), this.emit("finish"), this.stopAtPosition = null;
    }), this.onMediaEvent("seeking", () => {
      this.emit("seeking", this.getCurrentTime());
    }), this.onMediaEvent("error", () => {
      var e;
      this.emit("error", (e = this.getMediaElement().error) !== null && e !== void 0 ? e : new Error("Media error")), this.stopAtPosition = null;
    }));
  }
  initRendererEvents() {
    this.subscriptions.push(
      // Seek on click
      this.renderer.on("click", (e, t) => {
        this.options.interact && (this.seekTo(e), this.emit("interaction", e * this.getDuration()), this.emit("click", e, t));
      }),
      // Double click
      this.renderer.on("dblclick", (e, t) => {
        this.emit("dblclick", e, t);
      }),
      // Scroll
      this.renderer.on("scroll", (e, t, r, i) => {
        const o = this.getDuration();
        this.emit("scroll", e * o, t * o, r, i);
      }),
      // Redraw
      this.renderer.on("render", () => {
        this.emit("redraw");
      }),
      // RedrawComplete
      this.renderer.on("rendered", () => {
        this.emit("redrawcomplete");
      }),
      // DragStart
      this.renderer.on("dragstart", (e) => {
        this.emit("dragstart", e);
      }),
      // DragEnd
      this.renderer.on("dragend", (e) => {
        this.emit("dragend", e);
      })
    );
    {
      let e;
      this.subscriptions.push(this.renderer.on("drag", (t) => {
        if (!this.options.interact) return;
        this.renderer.renderProgress(t), clearTimeout(e);
        let r;
        this.isPlaying() ? r = 0 : this.options.dragToSeek === !0 ? r = 200 : typeof this.options.dragToSeek == "object" && this.options.dragToSeek !== void 0 && (r = this.options.dragToSeek.debounceTime), e = setTimeout(() => {
          this.seekTo(t);
        }, r), this.emit("interaction", t * this.getDuration()), this.emit("drag", t);
      }));
    }
  }
  initPlugins() {
    var e;
    !((e = this.options.plugins) === null || e === void 0) && e.length && this.options.plugins.forEach((t) => {
      this.registerPlugin(t);
    });
  }
  unsubscribePlayerEvents() {
    this.mediaSubscriptions.forEach((e) => e()), this.mediaSubscriptions = [];
  }
  /** Set new wavesurfer options and re-render it */
  setOptions(e) {
    this.options = Object.assign({}, this.options, e), e.duration && !e.peaks && (this.decodedData = et.createBuffer(this.exportPeaks(), e.duration)), e.peaks && e.duration && (this.decodedData = et.createBuffer(e.peaks, e.duration)), this.renderer.setOptions(this.options), e.audioRate && this.setPlaybackRate(e.audioRate), e.mediaControls != null && (this.getMediaElement().controls = e.mediaControls);
  }
  /** Register a wavesurfer.js plugin */
  registerPlugin(e) {
    return e._init(this), this.plugins.push(e), this.subscriptions.push(e.once("destroy", () => {
      this.plugins = this.plugins.filter((t) => t !== e);
    })), e;
  }
  /** For plugins only: get the waveform wrapper div */
  getWrapper() {
    return this.renderer.getWrapper();
  }
  /** For plugins only: get the scroll container client width */
  getWidth() {
    return this.renderer.getWidth();
  }
  /** Get the current scroll position in pixels */
  getScroll() {
    return this.renderer.getScroll();
  }
  /** Set the current scroll position in pixels */
  setScroll(e) {
    return this.renderer.setScroll(e);
  }
  /** Move the start of the viewing window to a specific time in the audio (in seconds) */
  setScrollTime(e) {
    const t = e / this.getDuration();
    this.renderer.setScrollPercentage(t);
  }
  /** Get all registered plugins */
  getActivePlugins() {
    return this.plugins;
  }
  loadAudio(e, t, r, i) {
    return Se(this, void 0, void 0, function* () {
      var o;
      if (this.emit("load", e), !this.options.media && this.isPlaying() && this.pause(), this.decodedData = null, this.stopAtPosition = null, !t && !r) {
        const a = this.options.fetchParams || {};
        window.AbortController && !a.signal && (this.abortController = new AbortController(), a.signal = (o = this.abortController) === null || o === void 0 ? void 0 : o.signal);
        const u = (c) => this.emit("loading", c);
        t = yield Aa.fetchBlob(e, u, a);
        const l = this.options.blobMimeType;
        l && (t = new Blob([t], {
          type: l
        }));
      }
      this.setSrc(e, t);
      const s = yield new Promise((a) => {
        const u = i || this.getDuration();
        u ? a(u) : this.mediaSubscriptions.push(this.onMediaEvent("loadedmetadata", () => a(this.getDuration()), {
          once: !0
        }));
      });
      if (!e && !t) {
        const a = this.getMediaElement();
        a instanceof Ht && (a.duration = s);
      }
      if (r)
        this.decodedData = et.createBuffer(r, s || 0);
      else if (t) {
        const a = yield t.arrayBuffer();
        this.decodedData = yield et.decode(a, this.options.sampleRate);
      }
      this.decodedData && (this.emit("decode", this.getDuration()), this.renderer.render(this.decodedData)), this.emit("ready", this.getDuration());
    });
  }
  /** Load an audio file by URL, with optional pre-decoded audio data */
  load(e, t, r) {
    return Se(this, void 0, void 0, function* () {
      try {
        return yield this.loadAudio(e, void 0, t, r);
      } catch (i) {
        throw this.emit("error", i), i;
      }
    });
  }
  /** Load an audio blob */
  loadBlob(e, t, r) {
    return Se(this, void 0, void 0, function* () {
      try {
        return yield this.loadAudio("", e, t, r);
      } catch (i) {
        throw this.emit("error", i), i;
      }
    });
  }
  /** Zoom the waveform by a given pixels-per-second factor */
  zoom(e) {
    if (!this.decodedData)
      throw new Error("No audio loaded");
    this.renderer.zoom(e), this.emit("zoom", e);
  }
  /** Get the decoded audio data */
  getDecodedData() {
    return this.decodedData;
  }
  /** Get decoded peaks */
  exportPeaks({
    channels: e = 2,
    maxLength: t = 8e3,
    precision: r = 1e4
  } = {}) {
    if (!this.decodedData)
      throw new Error("The audio has not been decoded yet");
    const i = Math.min(e, this.decodedData.numberOfChannels), o = [];
    for (let s = 0; s < i; s++) {
      const a = this.decodedData.getChannelData(s), u = [], l = a.length / t;
      for (let c = 0; c < t; c++) {
        const d = a.slice(Math.floor(c * l), Math.ceil((c + 1) * l));
        let f = 0;
        for (let m = 0; m < d.length; m++) {
          const v = d[m];
          Math.abs(v) > Math.abs(f) && (f = v);
        }
        u.push(Math.round(f * r) / r);
      }
      o.push(u);
    }
    return o;
  }
  /** Get the duration of the audio in seconds */
  getDuration() {
    let e = super.getDuration() || 0;
    return (e === 0 || e === 1 / 0) && this.decodedData && (e = this.decodedData.duration), e;
  }
  /** Toggle if the waveform should react to clicks */
  toggleInteraction(e) {
    this.options.interact = e;
  }
  /** Jump to a specific time in the audio (in seconds) */
  setTime(e) {
    this.stopAtPosition = null, super.setTime(e), this.updateProgress(e), this.emit("timeupdate", e);
  }
  /** Seek to a percentage of audio as [0..1] (0 = beginning, 1 = end) */
  seekTo(e) {
    const t = this.getDuration() * e;
    this.setTime(t);
  }
  /** Start playing the audio */
  play(e, t) {
    const r = Object.create(null, {
      play: {
        get: () => super.play
      }
    });
    return Se(this, void 0, void 0, function* () {
      return e != null && this.setTime(e), t != null && (this.media instanceof Ht ? this.media.stopAt(t) : this.stopAtPosition = t), r.play.call(this);
    });
  }
  /** Play or pause the audio */
  playPause() {
    return Se(this, void 0, void 0, function* () {
      return this.isPlaying() ? this.pause() : this.play();
    });
  }
  /** Stop the audio and go to the beginning */
  stop() {
    this.pause(), this.setTime(0);
  }
  /** Skip N or -N seconds from the current position */
  skip(e) {
    this.setTime(this.getCurrentTime() + e);
  }
  /** Empty the waveform */
  empty() {
    this.load("", [[0]], 1e-3);
  }
  /** Set HTML media element */
  setMediaElement(e) {
    this.unsubscribePlayerEvents(), super.setMediaElement(e), this.initPlayerEvents();
  }
  exportImage() {
    return Se(this, arguments, void 0, function* (e = "image/png", t = 1, r = "dataURL") {
      return this.renderer.exportImage(e, t, r);
    });
  }
  /** Unmount wavesurfer */
  destroy() {
    var e;
    this.emit("destroy"), (e = this.abortController) === null || e === void 0 || e.abort(), this.plugins.forEach((t) => t.destroy()), this.subscriptions.forEach((t) => t()), this.unsubscribePlayerEvents(), this.timer.destroy(), this.renderer.destroy(), super.destroy();
  }
}
He.BasePlugin = Ea;
He.dom = Ma;
function Fa({
  container: n,
  onStop: e
}) {
  const t = se(null), [r, i] = De(!1), o = ot(() => {
    var u;
    (u = t.current) == null || u.startRecording();
  }), s = ot(() => {
    var u;
    (u = t.current) == null || u.stopRecording();
  }), a = ot(e);
  return ge(() => {
    if (n) {
      const l = He.create({
        normalize: !1,
        container: n
      }).registerPlugin(cn.create());
      t.current = l, l.on("record-start", () => {
        i(!0);
      }), l.on("record-end", (c) => {
        a(c), i(!1);
      });
    }
  }, [n, a]), {
    recording: r,
    start: o,
    stop: s
  };
}
function ja(n) {
  const e = function(a, u, l) {
    for (let c = 0; c < l.length; c++)
      a.setUint8(u + c, l.charCodeAt(c));
  }, t = n.numberOfChannels, r = n.length * t * 2 + 44, i = new ArrayBuffer(r), o = new DataView(i);
  let s = 0;
  e(o, s, "RIFF"), s += 4, o.setUint32(s, r - 8, !0), s += 4, e(o, s, "WAVE"), s += 4, e(o, s, "fmt "), s += 4, o.setUint32(s, 16, !0), s += 4, o.setUint16(s, 1, !0), s += 2, o.setUint16(s, t, !0), s += 2, o.setUint32(s, n.sampleRate, !0), s += 4, o.setUint32(s, n.sampleRate * 2 * t, !0), s += 4, o.setUint16(s, t * 2, !0), s += 2, o.setUint16(s, 16, !0), s += 2, e(o, s, "data"), s += 4, o.setUint32(s, n.length * t * 2, !0), s += 4;
  for (let a = 0; a < n.numberOfChannels; a++) {
    const u = n.getChannelData(a);
    for (let l = 0; l < u.length; l++)
      o.setInt16(s, u[l] * 65535, !0), s += 2;
  }
  return new Uint8Array(i);
}
async function Ba(n, e, t) {
  const r = await n.arrayBuffer(), o = await new AudioContext().decodeAudioData(r), s = new AudioContext(), a = o.numberOfChannels, u = o.sampleRate;
  let l = o.length, c = 0;
  const d = s.createBuffer(a, l, u);
  for (let f = 0; f < a; f++) {
    const m = o.getChannelData(f), v = d.getChannelData(f);
    for (let g = 0; g < l; g++)
      v[g] = m[c + g];
  }
  return Promise.resolve(ja(d));
}
const Ha = (n) => !!n.name, Ie = (n) => {
  var e;
  return {
    text: (n == null ? void 0 : n.text) || "",
    files: ((e = n == null ? void 0 : n.files) == null ? void 0 : e.map((t) => t.path)) || []
  };
}, Ua = ho(({
  onValueChange: n,
  onChange: e,
  onPasteFile: t,
  onUpload: r,
  onSubmit: i,
  onRemove: o,
  onDownload: s,
  onDrop: a,
  onPreview: u,
  upload: l,
  onCancel: c,
  children: d,
  readOnly: f,
  loading: m,
  disabled: v,
  placeholder: g,
  elRef: p,
  slots: y,
  uploadConfig: S,
  value: x,
  ...b
}) => {
  const [_, C] = De(!1), E = Jr(), T = se(null), {
    start: I,
    stop: W,
    recording: N
  } = Fa({
    container: T.current,
    async onStop(L) {
      const M = new File([await Ba(L)], `${Date.now()}_recording_result.wav`, {
        type: "audio/wav"
      });
      D(M);
    }
  }), [P, O] = ya({
    onValueChange: n,
    value: x
  }), w = un(() => Yr(S), [S]), $ = v || (w == null ? void 0 : w.disabled) || m || f, D = ot(async (L) => {
    if ($)
      return;
    q.current = !0;
    const M = w == null ? void 0 : w.maxCount;
    if (typeof M == "number" && M > 0 && K.length >= M)
      return;
    let F = Array.isArray(L) ? L : [L];
    if (M === 1)
      F = F.slice(0, 1);
    else if (F.length === 0) {
      q.current = !1;
      return;
    } else if (typeof M == "number") {
      const X = M - K.length;
      F = F.slice(0, X < 0 ? 0 : X);
    }
    const j = K, H = F.map((X) => ({
      ...X,
      size: X.size,
      uid: `${X.name}-${Date.now()}`,
      name: X.name,
      status: "uploading"
    }));
    re((X) => [...M === 1 ? [] : X, ...H]);
    const V = (await l(F)).filter(Boolean).map((X, ce) => ({
      ...X,
      uid: H[ce].uid
    })), J = M === 1 ? V : [...j, ...V];
    r == null || r(V.map((X) => X.path)), q.current = !1;
    const ie = {
      ...P,
      files: J
    };
    return e == null || e(Ie(ie)), O(ie), V;
  }), q = se(!1), [K, re] = De(() => (P == null ? void 0 : P.files) || []);
  ge(() => {
    re((P == null ? void 0 : P.files) || []);
  }, [P == null ? void 0 : P.files]);
  const Y = un(() => {
    const L = {};
    return K.map((M) => {
      if (!Ha(M)) {
        const F = M.uid || M.url || M.path;
        return L[F] || (L[F] = 0), L[F]++, {
          ...M,
          name: M.orig_name || M.path,
          uid: M.uid || F + "-" + L[F],
          status: "done"
        };
      }
      return M;
    }) || [];
  }, [K]);
  return /* @__PURE__ */ oe.jsxs(oe.Fragment, {
    children: [/* @__PURE__ */ oe.jsx("div", {
      style: {
        display: "none"
      },
      ref: T
    }), /* @__PURE__ */ oe.jsx("div", {
      style: {
        display: "none"
      },
      children: d
    }), /* @__PURE__ */ oe.jsx(nn, {
      ...b,
      value: P == null ? void 0 : P.text,
      ref: p,
      disabled: v,
      readOnly: f,
      allowSpeech: w != null && w.allowSpeech ? {
        recording: N,
        onRecordingChange(L) {
          $ || (L ? I() : W());
        }
      } : !1,
      placeholder: g,
      loading: m,
      onSubmit: () => {
        E || i == null || i(Ie(P));
      },
      onCancel: () => {
        c == null || c();
      },
      onChange: (L) => {
        const M = {
          ...P,
          text: L
        };
        e == null || e(Ie(M)), O(M);
      },
      onPasteFile: async (L) => {
        if (!((w == null ? void 0 : w.allowPasteFile) ?? !0))
          return;
        const M = await D(L);
        M && (t == null || t(M.map((F) => F.path)));
      },
      prefix: /* @__PURE__ */ oe.jsxs(oe.Fragment, {
        children: [/* @__PURE__ */ oe.jsx(xi, {
          title: w == null ? void 0 : w.uploadButtonTooltip,
          children: /* @__PURE__ */ oe.jsx(Ci, {
            count: ((w == null ? void 0 : w.showCount) ?? !0) && !_ ? Y.length : 0,
            children: /* @__PURE__ */ oe.jsx(_e, {
              onClick: () => {
                C(!_);
              },
              color: "default",
              variant: "text",
              icon: /* @__PURE__ */ oe.jsx(bi, {})
            })
          })
        }), y.prefix ? /* @__PURE__ */ oe.jsx(bo, {
          slot: y.prefix
        }) : null]
      }),
      header: /* @__PURE__ */ oe.jsx(nn.Header, {
        title: (w == null ? void 0 : w.title) || "Attachments",
        open: _,
        onOpenChange: C,
        children: /* @__PURE__ */ oe.jsx(Dr, {
          ...wa(Zr(w, ["title", "placeholder", "showCount", "buttonTooltip", "allowPasteFile"])),
          disabled: $,
          getDropContainer: () => w != null && w.fullscreenDrop ? document.body : null,
          items: Y,
          placeholder: (L) => {
            var F, j, H, V, J, ie;
            const M = L === "drop";
            return {
              title: M ? ((F = w == null ? void 0 : w.placeholder) == null ? void 0 : F.drop.title) ?? "Drop file here" : ((j = w == null ? void 0 : w.placeholder) == null ? void 0 : j.inline.title) ?? "Upload files",
              description: M ? ((H = w == null ? void 0 : w.placeholder) == null ? void 0 : H.drop.description) ?? void 0 : ((V = w == null ? void 0 : w.placeholder) == null ? void 0 : V.inline.description) ?? "Click or drag files to this area to upload",
              icon: M ? ((J = w == null ? void 0 : w.placeholder) == null ? void 0 : J.drop.icon) ?? void 0 : ((ie = w == null ? void 0 : w.placeholder) == null ? void 0 : ie.inline.icon) ?? /* @__PURE__ */ oe.jsx(vi, {})
            };
          },
          onDownload: s,
          onPreview: u,
          onDrop: a,
          onChange: async (L) => {
            const M = L.file, F = L.fileList, j = Y.findIndex((H) => H.uid === M.uid);
            if (j !== -1) {
              if (q.current)
                return;
              o == null || o(M);
              const H = K.slice();
              H.splice(j, 1);
              const V = {
                ...P,
                files: H
              };
              O(V), e == null || e(Ie(V));
            } else {
              if (q.current)
                return;
              q.current = !0;
              let H = F.filter((z) => z.status !== "done");
              const V = w == null ? void 0 : w.maxCount;
              if (V === 1)
                H = H.slice(0, 1);
              else if (H.length === 0) {
                q.current = !1;
                return;
              } else if (typeof V == "number") {
                const z = V - K.length;
                H = H.slice(0, z < 0 ? 0 : z);
              }
              const J = K, ie = H.map((z) => ({
                ...z,
                size: z.size,
                uid: z.uid,
                name: z.name,
                status: "uploading"
              }));
              re((z) => [...V === 1 ? [] : z, ...ie]);
              const X = (await l(H.map((z) => z.originFileObj))).filter(Boolean).map((z, fe) => ({
                ...z,
                uid: ie[fe].uid
              })), ce = V === 1 ? X : [...J, ...X];
              r == null || r(X.map((z) => z.path)), q.current = !1;
              const ve = {
                ...P,
                files: ce
              };
              re(ce), n == null || n(ve), e == null || e(Ie(ve));
            }
          },
          customRequest: Ii
        })
      })
    })]
  });
});
export {
  Ua as MultimodalInput,
  Ua as default
};
