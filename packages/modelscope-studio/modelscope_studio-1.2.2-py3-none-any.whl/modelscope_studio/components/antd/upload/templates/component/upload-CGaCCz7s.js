import { i as Pe, a as X, r as ke, w as A, g as Ue, b as Te } from "./Index-CkQwuzcr.js";
const R = window.ms_globals.React, me = window.ms_globals.React.useMemo, Ce = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, we = window.ms_globals.React.useState, _e = window.ms_globals.React.useEffect, J = window.ms_globals.ReactDOM.createPortal, Oe = window.ms_globals.internalContext.useContextPropsContext, je = window.ms_globals.internalContext.ContextPropsProvider, Ne = window.ms_globals.antd.Upload;
var We = /\s/;
function Ae(e) {
  for (var t = e.length; t-- && We.test(e.charAt(t)); )
    ;
  return t;
}
var De = /^\s+/;
function Me(e) {
  return e && e.slice(0, Ae(e) + 1).replace(De, "");
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
  var i, s, n, o, l, d, g = 0, I = !1, c = !1, _ = !0;
  if (typeof e != "function")
    throw new TypeError(Ke);
  t = ne(t) || 0, X(r) && (I = !!r.leading, c = "maxWait" in r, n = c ? Je(ne(r.maxWait) || 0, t) : n, _ = "trailing" in r ? !!r.trailing : _);
  function f(u) {
    var E = i, k = s;
    return i = s = void 0, g = u, o = e.apply(k, E), o;
  }
  function v(u) {
    return g = u, l = setTimeout(h, t), I ? f(u) : o;
  }
  function S(u) {
    var E = u - d, k = u - g, W = t - E;
    return c ? Xe(W, n - k) : W;
  }
  function m(u) {
    var E = u - d, k = u - g;
    return d === void 0 || E >= t || E < 0 || c && k >= n;
  }
  function h() {
    var u = H();
    if (m(u))
      return x(u);
    l = setTimeout(h, S(u));
  }
  function x(u) {
    return l = void 0, _ && i ? f(u) : (i = s = void 0, o);
  }
  function p() {
    l !== void 0 && clearTimeout(l), g = 0, i = d = s = l = void 0;
  }
  function a() {
    return l === void 0 ? o : x(H());
  }
  function C() {
    var u = H(), E = m(u);
    if (i = arguments, s = this, d = u, E) {
      if (l === void 0)
        return v(d);
      if (c)
        return clearTimeout(l), l = setTimeout(h, t), f(d);
    }
    return l === void 0 && (l = setTimeout(h, t)), o;
  }
  return C.cancel = p, C.flush = a, C;
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
var Qe = R, Ze = Symbol.for("react.element"), Ve = Symbol.for("react.fragment"), $e = Object.prototype.hasOwnProperty, et = Qe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, tt = {
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
var F = he.exports;
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
  insert_hydration: D,
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
      D(n, t, o), s && s.m(t, null), e[9](t), r = !0;
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
      D(o, t, l), e[8](t), D(o, r, l), n && n.m(o, l), D(o, i, l), s = !0;
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
    svelteInit: d
  } = t;
  const g = A(ae(t)), I = A();
  ie(e, I, (a) => r(0, i = a));
  const c = A();
  ie(e, c, (a) => r(1, s = a));
  const _ = [], f = wt("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: S,
    subSlotIndex: m
  } = Ue() || {}, h = d({
    parent: f,
    props: g,
    target: I,
    slot: c,
    slotKey: v,
    slotIndex: S,
    subSlotIndex: m,
    onDestroy(a) {
      _.push(a);
    }
  });
  ht("$$ms-gr-react-wrapper", h), pt(() => {
    g.set(ae(t));
  }), _t(() => {
    _.forEach((a) => a());
  });
  function x(a) {
    oe[a ? "unshift" : "push"](() => {
      i = a, I.set(i);
    });
  }
  function p(a) {
    oe[a ? "unshift" : "push"](() => {
      s = a, c.set(s);
    });
  }
  return e.$$set = (a) => {
    r(17, t = re(re({}, t), le(a))), "svelteInit" in a && r(5, d = a.svelteInit), "$$scope" in a && r(6, o = a.$$scope);
  }, t = le(t), [i, s, I, c, l, d, o, n, x, p];
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
    const s = A(), n = new It({
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
          }, d = o.parent ?? K;
          return d.nodes = [...d.nodes, l], ue({
            createPortal: J,
            node: K
          }), o.onDestroy(() => {
            d.nodes = d.nodes.filter((g) => g.svelteInstance !== s), ue({
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
    const s = R.Children.toArray(e._reactElement.props.children).map((n) => {
      if (R.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: l
        } = Q(n.props.el);
        return R.cloneElement(n, {
          ...n.props,
          el: l,
          children: [...R.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return s.originalChildren = e._reactElement.props.children, t.push(J(R.cloneElement(e._reactElement, {
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
      useCapture: d
    }) => {
      r.addEventListener(l, o, d);
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
  const o = pe(), [l, d] = we([]), {
    forceClone: g
  } = Oe(), I = g ? !0 : t;
  return _e(() => {
    var S;
    if (!o.current || !e)
      return;
    let c = e;
    function _() {
      let m = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (m = c.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Rt(n, m), r && m.classList.add(...r.split(" ")), i) {
        const h = Lt(i);
        Object.keys(h).forEach((x) => {
          m.style[x] = h[x];
        });
      }
    }
    let f = null, v = null;
    if (I && window.MutationObserver) {
      let m = function() {
        var a, C, u;
        (a = o.current) != null && a.contains(c) && ((C = o.current) == null || C.removeChild(c));
        const {
          portals: x,
          clonedElement: p
        } = Q(e);
        c = p, d(x), c.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          _();
        }, 50), (u = o.current) == null || u.appendChild(c);
      };
      m();
      const h = Ye(() => {
        m(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0
          // attributes: observeAttributes ?? (forceClone ? true : false),
        });
      }, 50);
      f = new window.MutationObserver(h), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", _(), (S = o.current) == null || S.appendChild(c);
    return () => {
      var m, h;
      c.style.display = "", (m = o.current) != null && m.contains(c) && ((h = o.current) == null || h.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, I, r, i, n, s, g]), R.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...l);
}), Ft = ({
  children: e,
  ...t
}) => /* @__PURE__ */ F.jsx(F.Fragment, {
  children: e(t)
});
function Ct(e) {
  return R.createElement(Ft, {
    children: e
  });
}
function fe(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? Ct((r) => /* @__PURE__ */ F.jsx(je, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ F.jsx(de, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ F.jsx(de, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function T({
  key: e,
  slots: t,
  targets: r
}, i) {
  return t[e] ? (...s) => r ? r.map((n, o) => /* @__PURE__ */ F.jsx(R.Fragment, {
    children: fe(n, {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }, o)) : /* @__PURE__ */ F.jsx(F.Fragment, {
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
  itemRender: d,
  iconRender: g,
  data: I,
  onChange: c,
  onValueChange: _,
  onRemove: f,
  maxCount: v,
  fileList: S,
  setSlotParams: m,
  ...h
}) => {
  const x = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", p = kt(r), a = L(p.showPreviewIcon), C = L(p.showRemoveIcon), u = L(p.showDownloadIcon), E = L(s), k = L(n), W = L(i == null ? void 0 : i.format), xe = L(o), Ee = L(l), Le = L(d), Se = L(g), Re = L(I), j = pe(!1), [N, B] = we(S);
  _e(() => {
    B(S);
  }, [S]);
  const Z = me(() => {
    const U = {};
    return N.map((y) => {
      if (!Pt(y)) {
        const P = y.uid || y.url || y.path;
        return U[P] || (U[P] = 0), U[P]++, {
          ...y,
          name: y.orig_name || y.path,
          uid: y.uid || P + "-" + U[P],
          status: "done"
        };
      }
      return y;
    }) || [];
  }, [N]);
  return /* @__PURE__ */ F.jsx(Ne, {
    ...h,
    fileList: Z,
    data: Re || I,
    previewFile: xe,
    isImageUrl: Ee,
    maxCount: v,
    itemRender: e.itemRender ? T({
      slots: e,
      key: "itemRender"
    }) : Le,
    iconRender: e.iconRender ? T({
      slots: e,
      key: "iconRender"
    }) : Se,
    customRequest: k || He,
    onChange: async (U) => {
      const y = U.file, P = U.fileList, V = Z.findIndex((b) => b.uid === y.uid);
      if (V !== -1) {
        if (j.current)
          return;
        f == null || f(y);
        const b = N.slice();
        b.splice(V, 1), _ == null || _(b), c == null || c(b.map((q) => q.path));
      } else {
        if (E && !await E(y, P) || j.current)
          return;
        j.current = !0;
        let b = P.filter((w) => w.status !== "done");
        if (v === 1)
          b = b.slice(0, 1);
        else if (b.length === 0) {
          j.current = !1;
          return;
        } else if (typeof v == "number") {
          const w = v - N.length;
          b = b.slice(0, w < 0 ? 0 : w);
        }
        const q = N, $ = b.map((w) => ({
          ...w,
          size: w.size,
          uid: w.uid,
          name: w.name,
          percent: 99,
          status: "uploading"
        }));
        B((w) => [...v === 1 ? [] : w, ...$]);
        const ee = (await t(b.map((w) => w.originFileObj))).filter(Boolean).map((w, Fe) => ({
          ...w,
          uid: $[Fe].uid
        })), G = v === 1 ? ee : [...q, ...ee];
        j.current = !1, B(G), _ == null || _(G), c == null || c(G.map((w) => w.path));
      }
    },
    progress: i && {
      ...i,
      format: W
    },
    showUploadList: x ? {
      ...p,
      showDownloadIcon: u || p.showDownloadIcon,
      showRemoveIcon: C || p.showRemoveIcon,
      showPreviewIcon: a || p.showPreviewIcon,
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
  Ot as Upload,
  Ot as default
};
