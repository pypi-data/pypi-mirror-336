import { i as Pe, a as X, r as ke, w as W, g as Ue, b as Te } from "./Index-C4O95KrE.js";
const S = window.ms_globals.React, me = window.ms_globals.React.useMemo, Ce = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, we = window.ms_globals.React.useState, _e = window.ms_globals.React.useEffect, J = window.ms_globals.ReactDOM.createPortal, Oe = window.ms_globals.internalContext.useContextPropsContext, je = window.ms_globals.internalContext.ContextPropsProvider, De = window.ms_globals.antd.Upload;
var Ne = /\s/;
function We(e) {
  for (var t = e.length; t-- && Ne.test(e.charAt(t)); )
    ;
  return t;
}
var Ae = /^\s+/;
function Me(e) {
  return e && e.slice(0, We(e) + 1).replace(Ae, "");
}
var te = NaN, ze = /^[-+]0x[0-9a-f]+$/i, Be = /^0b[01]+$/i, qe = /^0o[0-7]+$/i, Ge = parseInt;
function ne(e) {
  if (typeof e == "number")
    return e;
  if (Pe(e))
    return te;
  if (X(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = X(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Me(e);
  var r = Be.test(e);
  return r || qe.test(e) ? Ge(e.slice(2), r ? 2 : 8) : ze.test(e) ? te : +e;
}
function He() {
}
var H = function() {
  return ke.Date.now();
}, Ke = "Expected a function", Je = Math.max, Xe = Math.min;
function Ye(e, t, r) {
  var i, s, n, o, l, f, g = 0, v = !1, c = !1, _ = !0;
  if (typeof e != "function")
    throw new TypeError(Ke);
  t = ne(t) || 0, X(r) && (v = !!r.leading, c = "maxWait" in r, n = c ? Je(ne(r.maxWait) || 0, t) : n, _ = "trailing" in r ? !!r.trailing : _);
  function m(d) {
    var E = i, k = s;
    return i = s = void 0, g = d, o = e.apply(k, E), o;
  }
  function b(d) {
    return g = d, l = setTimeout(h, t), v ? m(d) : o;
  }
  function P(d) {
    var E = d - f, k = d - g, N = t - E;
    return c ? Xe(N, n - k) : N;
  }
  function a(d) {
    var E = d - f, k = d - g;
    return f === void 0 || E >= t || E < 0 || c && k >= n;
  }
  function h() {
    var d = H();
    if (a(d))
      return x(d);
    l = setTimeout(h, P(d));
  }
  function x(d) {
    return l = void 0, _ && i ? m(d) : (i = s = void 0, o);
  }
  function p() {
    l !== void 0 && clearTimeout(l), g = 0, i = f = s = l = void 0;
  }
  function u() {
    return l === void 0 ? o : x(H());
  }
  function F() {
    var d = H(), E = a(d);
    if (i = arguments, s = this, f = d, E) {
      if (l === void 0)
        return b(f);
      if (c)
        return clearTimeout(l), l = setTimeout(h, t), m(f);
    }
    return l === void 0 && (l = setTimeout(h, t)), o;
  }
  return F.cancel = p, F.flush = u, F;
}
var he = {
  exports: {}
}, z = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Qe = S, Ze = Symbol.for("react.element"), Ve = Symbol.for("react.fragment"), $e = Object.prototype.hasOwnProperty, et = Qe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, tt = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ge(e, t, r) {
  var i, s = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (i in t) $e.call(t, i) && !tt.hasOwnProperty(i) && (s[i] = t[i]);
  if (e && e.defaultProps) for (i in t = e.defaultProps, t) s[i] === void 0 && (s[i] = t[i]);
  return {
    $$typeof: Ze,
    type: e,
    key: n,
    ref: o,
    props: s,
    _owner: et.current
  };
}
z.Fragment = Ve;
z.jsx = ge;
z.jsxs = ge;
he.exports = z;
var R = he.exports;
const {
  SvelteComponent: nt,
  assign: re,
  binding_callbacks: oe,
  check_outros: rt,
  children: ve,
  claim_element: Ie,
  claim_space: ot,
  component_subscribe: ie,
  compute_slots: it,
  create_slot: st,
  detach: O,
  element: ye,
  empty: se,
  exclude_internal_props: le,
  get_all_dirty_from_scope: lt,
  get_slot_changes: ct,
  group_outros: at,
  init: ut,
  insert_hydration: A,
  safe_not_equal: dt,
  set_custom_element_data: be,
  space: ft,
  transition_in: M,
  transition_out: Y,
  update_slot_base: mt
} = window.__gradio__svelte__internal, {
  beforeUpdate: pt,
  getContext: wt,
  onDestroy: _t,
  setContext: ht
} = window.__gradio__svelte__internal;
function ce(e) {
  let t, r;
  const i = (
    /*#slots*/
    e[7].default
  ), s = st(
    i,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ye("svelte-slot"), s && s.c(), this.h();
    },
    l(n) {
      t = Ie(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = ve(t);
      s && s.l(o), o.forEach(O), this.h();
    },
    h() {
      be(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      A(n, t, o), s && s.m(t, null), e[9](t), r = !0;
    },
    p(n, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && mt(
        s,
        i,
        n,
        /*$$scope*/
        n[6],
        r ? ct(
          i,
          /*$$scope*/
          n[6],
          o,
          null
        ) : lt(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (M(s, n), r = !0);
    },
    o(n) {
      Y(s, n), r = !1;
    },
    d(n) {
      n && O(t), s && s.d(n), e[9](null);
    }
  };
}
function gt(e) {
  let t, r, i, s, n = (
    /*$$slots*/
    e[4].default && ce(e)
  );
  return {
    c() {
      t = ye("react-portal-target"), r = ft(), n && n.c(), i = se(), this.h();
    },
    l(o) {
      t = Ie(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), ve(t).forEach(O), r = ot(o), n && n.l(o), i = se(), this.h();
    },
    h() {
      be(t, "class", "svelte-1rt0kpf");
    },
    m(o, l) {
      A(o, t, l), e[8](t), A(o, r, l), n && n.m(o, l), A(o, i, l), s = !0;
    },
    p(o, [l]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, l), l & /*$$slots*/
      16 && M(n, 1)) : (n = ce(o), n.c(), M(n, 1), n.m(i.parentNode, i)) : n && (at(), Y(n, 1, 1, () => {
        n = null;
      }), rt());
    },
    i(o) {
      s || (M(n), s = !0);
    },
    o(o) {
      Y(n), s = !1;
    },
    d(o) {
      o && (O(t), O(r), O(i)), e[8](null), n && n.d(o);
    }
  };
}
function ae(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function vt(e, t, r) {
  let i, s, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const l = it(n);
  let {
    svelteInit: f
  } = t;
  const g = W(ae(t)), v = W();
  ie(e, v, (u) => r(0, i = u));
  const c = W();
  ie(e, c, (u) => r(1, s = u));
  const _ = [], m = wt("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: P,
    subSlotIndex: a
  } = Ue() || {}, h = f({
    parent: m,
    props: g,
    target: v,
    slot: c,
    slotKey: b,
    slotIndex: P,
    subSlotIndex: a,
    onDestroy(u) {
      _.push(u);
    }
  });
  ht("$$ms-gr-react-wrapper", h), pt(() => {
    g.set(ae(t));
  }), _t(() => {
    _.forEach((u) => u());
  });
  function x(u) {
    oe[u ? "unshift" : "push"](() => {
      i = u, v.set(i);
    });
  }
  function p(u) {
    oe[u ? "unshift" : "push"](() => {
      s = u, c.set(s);
    });
  }
  return e.$$set = (u) => {
    r(17, t = re(re({}, t), le(u))), "svelteInit" in u && r(5, f = u.svelteInit), "$$scope" in u && r(6, o = u.$$scope);
  }, t = le(t), [i, s, v, c, l, f, o, n, x, p];
}
class It extends nt {
  constructor(t) {
    super(), ut(this, t, vt, gt, dt, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: Tt
} = window.__gradio__svelte__internal, ue = window.ms_globals.rerender, K = window.ms_globals.tree;
function yt(e, t = {}) {
  function r(i) {
    const s = W(), n = new It({
      ...i,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: t.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, f = o.parent ?? K;
          return f.nodes = [...f.nodes, l], ue({
            createPortal: J,
            node: K
          }), o.onDestroy(() => {
            f.nodes = f.nodes.filter((g) => g.svelteInstance !== s), ue({
              createPortal: J,
              node: K
            });
          }), l;
        },
        ...i.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((i) => {
    window.ms_globals.initializePromise.then(() => {
      i(r);
    });
  });
}
function bt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function xt(e, t = !1) {
  try {
    if (Te(e))
      return e;
    if (t && !bt(e))
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
function L(e, t) {
  return me(() => xt(e, t), [e, t]);
}
const Et = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Lt(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const i = e[r];
    return t[r] = St(r, i), t;
  }, {}) : {};
}
function St(e, t) {
  return typeof t == "number" && !Et.includes(e) ? t + "px" : t;
}
function Q(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const s = S.Children.toArray(e._reactElement.props.children).map((n) => {
      if (S.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: l
        } = Q(n.props.el);
        return S.cloneElement(n, {
          ...n.props,
          el: l,
          children: [...S.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return s.originalChildren = e._reactElement.props.children, t.push(J(S.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: s
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((s) => {
    e.getEventListeners(s).forEach(({
      listener: o,
      type: l,
      useCapture: f
    }) => {
      r.addEventListener(l, o, f);
    });
  });
  const i = Array.from(e.childNodes);
  for (let s = 0; s < i.length; s++) {
    const n = i[s];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: l
      } = Q(n);
      t.push(...l), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Rt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const de = Ce(({
  slot: e,
  clone: t,
  className: r,
  style: i,
  observeAttributes: s
}, n) => {
  const o = pe(), [l, f] = we([]), {
    forceClone: g
  } = Oe(), v = g ? !0 : t;
  return _e(() => {
    var P;
    if (!o.current || !e)
      return;
    let c = e;
    function _() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Rt(n, a), r && a.classList.add(...r.split(" ")), i) {
        const h = Lt(i);
        Object.keys(h).forEach((x) => {
          a.style[x] = h[x];
        });
      }
    }
    let m = null, b = null;
    if (v && window.MutationObserver) {
      let a = function() {
        var u, F, d;
        (u = o.current) != null && u.contains(c) && ((F = o.current) == null || F.removeChild(c));
        const {
          portals: x,
          clonedElement: p
        } = Q(e);
        c = p, f(x), c.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          _();
        }, 50), (d = o.current) == null || d.appendChild(c);
      };
      a();
      const h = Ye(() => {
        a(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0
          // attributes: observeAttributes ?? (forceClone ? true : false),
        });
      }, 50);
      m = new window.MutationObserver(h), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", _(), (P = o.current) == null || P.appendChild(c);
    return () => {
      var a, h;
      c.style.display = "", (a = o.current) != null && a.contains(c) && ((h = o.current) == null || h.removeChild(c)), m == null || m.disconnect();
    };
  }, [e, v, r, i, n, s, g]), S.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...l);
}), Ft = ({
  children: e,
  ...t
}) => /* @__PURE__ */ R.jsx(R.Fragment, {
  children: e(t)
});
function Ct(e) {
  return S.createElement(Ft, {
    children: e
  });
}
function fe(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? Ct((r) => /* @__PURE__ */ R.jsx(je, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ R.jsx(de, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ R.jsx(de, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function T({
  key: e,
  slots: t,
  targets: r
}, i) {
  return t[e] ? (...s) => r ? r.map((n, o) => /* @__PURE__ */ R.jsx(S.Fragment, {
    children: fe(n, {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }, o)) : /* @__PURE__ */ R.jsx(R.Fragment, {
    children: fe(t[e], {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }) : void 0;
}
const Pt = (e) => !!e.name;
function kt(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Ot = yt(({
  slots: e,
  upload: t,
  showUploadList: r,
  progress: i,
  beforeUpload: s,
  customRequest: n,
  previewFile: o,
  isImageUrl: l,
  itemRender: f,
  iconRender: g,
  data: v,
  onChange: c,
  onValueChange: _,
  onRemove: m,
  fileList: b,
  setSlotParams: P,
  maxCount: a,
  ...h
}) => {
  const x = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", p = kt(r), u = L(p.showPreviewIcon), F = L(p.showRemoveIcon), d = L(p.showDownloadIcon), E = L(s), k = L(n), N = L(i == null ? void 0 : i.format), xe = L(o), Ee = L(l), Le = L(f), Se = L(g), Re = L(v), j = pe(!1), [D, B] = we(b);
  _e(() => {
    B(b);
  }, [b]);
  const Z = me(() => {
    const U = {};
    return D.map((I) => {
      if (!Pt(I)) {
        const C = I.uid || I.url || I.path;
        return U[C] || (U[C] = 0), U[C]++, {
          ...I,
          name: I.orig_name || I.path,
          uid: I.uid || C + "-" + U[C],
          status: "done"
        };
      }
      return I;
    }) || [];
  }, [D]);
  return /* @__PURE__ */ R.jsx(De.Dragger, {
    ...h,
    fileList: Z,
    data: Re || v,
    previewFile: xe,
    isImageUrl: Ee,
    itemRender: e.itemRender ? T({
      slots: e,
      key: "itemRender"
    }) : Le,
    iconRender: e.iconRender ? T({
      slots: e,
      key: "iconRender"
    }) : Se,
    maxCount: a,
    onChange: async (U) => {
      const I = U.file, C = U.fileList, V = Z.findIndex((y) => y.uid === I.uid);
      if (V !== -1) {
        if (j.current)
          return;
        m == null || m(I);
        const y = D.slice();
        y.splice(V, 1), _ == null || _(y), c == null || c(y.map((q) => q.path));
      } else {
        if (E && !await E(I, C) || j.current)
          return;
        j.current = !0;
        let y = C.filter((w) => w.status !== "done");
        if (a === 1)
          y = y.slice(0, 1);
        else if (y.length === 0) {
          j.current = !1;
          return;
        } else if (typeof a == "number") {
          const w = a - D.length;
          y = y.slice(0, w < 0 ? 0 : w);
        }
        const q = D, $ = y.map((w) => ({
          ...w,
          size: w.size,
          uid: w.uid,
          name: w.name,
          percent: 99,
          status: "uploading"
        }));
        B((w) => [...a === 1 ? [] : w, ...$]);
        const ee = (await t(y.map((w) => w.originFileObj))).filter(Boolean).map((w, Fe) => ({
          ...w,
          uid: $[Fe].uid
        })), G = a === 1 ? ee : [...q, ...ee];
        j.current = !1, B(G), _ == null || _(G), c == null || c(G.map((w) => w.path));
      }
    },
    customRequest: k || He,
    progress: i && {
      ...i,
      format: N
    },
    showUploadList: x ? {
      ...p,
      showDownloadIcon: d || p.showDownloadIcon,
      showRemoveIcon: F || p.showRemoveIcon,
      showPreviewIcon: u || p.showPreviewIcon,
      downloadIcon: e["showUploadList.downloadIcon"] ? T({
        slots: e,
        key: "showUploadList.downloadIcon"
      }) : p.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? T({
        slots: e,
        key: "showUploadList.removeIcon"
      }) : p.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? T({
        slots: e,
        key: "showUploadList.previewIcon"
      }) : p.previewIcon,
      extra: e["showUploadList.extra"] ? T({
        slots: e,
        key: "showUploadList.extra"
      }) : p.extra
    } : r
  });
});
export {
  Ot as UploadDragger,
  Ot as default
};
