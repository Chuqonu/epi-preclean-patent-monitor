/**
 * EPI / Preclean Patent Monitoring Report — independent client renderer.
 * Loads data/report.json. Does not auto-open closed months on scroll.
 */
(function () {
  "use strict";

  const SIDEBAR_KEY = "epi-preclean-sidebar-width";
  const SIDEBAR_MIN = 220;
  const SIDEBAR_MAX = 520;

  const $ = (sel, root) => (root || document).querySelector(sel);

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function text(s) {
    return esc(s).replace(/\n/g, "<br>");
  }


  function pick(obj, keys, fallback) {
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i];
      if (obj && obj[k] != null && obj[k] !== "") return obj[k];
    }
    return fallback;
  }

  /** Publication/event date for within-month sort (newest first). */
  function familySortTime(raw) {
    const d = pick(raw, ["event_date", "publication_date", "date"], "");
    const t = Date.parse(d);
    return Number.isFinite(t) ? t : 0;
  }

  function familiesNewestFirst(month) {
    return (month.families || []).slice().sort((a, b) => familySortTime(b) - familySortTime(a));
  }

  function scopeLabelZh(status) {
    const map = {
      core: "核心",
      related: "关联",
      pending: "待核",
      excluded: "排除",
    };
    return map[status] || "";
  }

  function importTagZh(tag) {
    if (!tag) return "";
    if (tag === "imported baseline") return "基线导入";
    return tag;
  }

  function discoveryLabelZh(src) {
    if (src === "independent_search") return "独立检索纳入";
    if (src === "reference_report") return "参考报告基线";
    return "";
  }

  function computeFigureStats(data) {
    let refs = 0;
    let loadable = 0;
    (data.months || []).forEach((m) => {
      (m.families || []).forEach((fam) => {
        (pick(fam, ["figures", "images"], []) || []).forEach((fig) => {
          refs += 1;
          const p = pick(fig, ["local_asset_path", "path"], "");
          if (String(p).trim()) loadable += 1;
        });
      });
    });
    const cited = (data.counts && data.counts.figures != null) ? data.counts.figures : refs;
    const pending = Math.max(0, refs - loadable);
    return { cited: cited, refs: refs, loadable: loadable, pending: pending };
  }

  function normFamily(f, monthLabel) {
    const publication_id = pick(f, ["publication_id", "publication_number"], "");
    const month = f.month || monthLabel || "";
    const id = f.id || (month && publication_id ? month + "-" + publication_id : publication_id);
    const figures = pick(f, ["figures", "images"], []) || [];
    const mappedFigures = figures.map(function (img) {
      const displayRotation = Number(pick(img, ["display_rotation"], 0)) || 0;
      return {
        caption: pick(img, ["caption", "display_caption"], ""),
        display_caption: pick(img, ["display_caption", "caption"], ""),
        source_url: img.source_url || "",
        source_publication: pick(img, ["source_publication_id", "source_publication"], ""),
        figure_label: pick(img, ["figure_number", "figure_label"], ""),
        width: img.width,
        height: img.height,
        display_rotation: displayRotation,
        path: pick(img, ["local_asset_path", "path"], ""),
        sha256: pick(img, ["asset_sha256", "source_display_sha256", "sha256"], ""),
        annotations: img.annotations || null,
        annotation_coverage_status: img.annotation_coverage_status || "",
      };
    });
    const events = pick(f, ["family_events", "events"], []) || [];
    const mappedEvents = events.map(function (ev) {
      return {
        number: pick(ev, ["publication_id", "number"], ""),
        date: pick(ev, ["event_date", "date"], ""),
        event: pick(ev, ["event_type", "event"], ""),
        source_url: ev.source_url || "",
        application_number: pick(ev, ["application_id", "application_number"], ""),
      };
    });
    return Object.assign({}, f, {
      id: id,
      month: month,
      publication_number: publication_id,
      title: pick(f, ["title_zh", "title"], ""),
      title_original: f.title_original || null,
      applicant: pick(f, ["applicant_normalized", "applicant"], ""),
      publication_date: pick(f, ["event_date", "publication_date"], ""),
      brief: pick(f, ["short_preview", "brief", "technical_summary", "summary"], ""),
      summary: pick(f, ["technical_summary", "summary", "short_preview"], ""),
      claims: pick(f, ["claims_or_embodiment_basis", "claims"], ""),
      relevance: pick(f, ["scope_reason", "relevance"], ""),
      family_key: pick(f, ["family_id", "family_key"], ""),
      events: mappedEvents,
      images: mappedFigures,
      scope_status: f.scope_status || "",
      family_completion_status: f.family_completion_status || "",
      import_tag: f.import_tag || "",
      discovery_source: f.discovery_source || "",
    });
  }


  function loadSidebarWidth() {
    const n = parseInt(localStorage.getItem(SIDEBAR_KEY) || "", 10);
    if (Number.isFinite(n) && n >= SIDEBAR_MIN && n <= SIDEBAR_MAX) {
      document.documentElement.style.setProperty("--sidebar-width", n + "px");
    }
  }

  function initMobileDrawer() {
    const toggle = $("#toc-drawer-toggle");
    const shell = $(".shell");
    const side = $(".side");
    if (!toggle || !shell || !side) return;

    function setOpen(open) {
      shell.classList.toggle("drawer-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("drawer-scroll-lock", open);
    }

    toggle.addEventListener("click", () => setOpen(!shell.classList.contains("drawer-open")));

    side.addEventListener("click", (e) => {
      const mini = e.target.closest(".mini");
      if (mini && shell.classList.contains("drawer-open")) setOpen(false);
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && shell.classList.contains("drawer-open")) setOpen(false);
    });

    document.addEventListener("click", (e) => {
      if (!shell.classList.contains("drawer-open")) return;
      if (side.contains(e.target) || toggle.contains(e.target)) return;
      setOpen(false);
    });
  }

  function initResizer() {
    const handle = $("#resizer");
    if (!handle) return;
    let dragging = false;
    let startX = 0;
    let startW = 0;

    function widthNow() {
      return parseInt(getComputedStyle(document.documentElement).getPropertyValue("--sidebar-width"), 10) || 320;
    }

    function onMove(clientX) {
      if (!dragging) return;
      const next = Math.min(SIDEBAR_MAX, Math.max(SIDEBAR_MIN, startW + (clientX - startX)));
      document.documentElement.style.setProperty("--sidebar-width", next + "px");
    }

    handle.addEventListener("pointerdown", (e) => {
      dragging = true;
      startX = e.clientX;
      startW = widthNow();
      handle.setPointerCapture(e.pointerId);
      e.preventDefault();
    });
    handle.addEventListener("pointermove", (e) => onMove(e.clientX));
    handle.addEventListener("pointerup", (e) => {
      if (!dragging) return;
      dragging = false;
      localStorage.setItem(SIDEBAR_KEY, String(widthNow()));
      try { handle.releasePointerCapture(e.pointerId); } catch (_) {}
    });
    handle.addEventListener("keydown", (e) => {
      const step = e.shiftKey ? 24 : 12;
      let w = widthNow();
      if (e.key === "ArrowLeft") w -= step;
      else if (e.key === "ArrowRight") w += step;
      else return;
      w = Math.min(SIDEBAR_MAX, Math.max(SIDEBAR_MIN, w));
      document.documentElement.style.setProperty("--sidebar-width", w + "px");
      localStorage.setItem(SIDEBAR_KEY, String(w));
      e.preventDefault();
    });
  }

  function hasIndependentIncrement(data) {
    return (data.months || []).some((m) =>
      (m.families || []).some((f) => f.discovery_source === "independent_search")
    );
  }

  function editionLabel(data) {
    return hasIndependentIncrement(data) ? "初版 · 含独立检索增量" : "初版 · 基线导入";
  }

  function formatMonthLabel(ym) {
    if (!ym) return "";
    const m = String(ym).match(/^(\d{4})-(\d{2})$/);
    return m ? m[1] + "-" + m[2] : ym;
  }

  function renderSideMeta() {
    /* Dot shell: home link only (static in index.html). */
  }

  function classifyFamily(f) {
    const cat = String(f.category || "");
    const tags = (f.technology_tags || []).map((t) => String(t).toLowerCase());
    const lane = String(f.discovery_lane || "");
    const domains = [];
    if (/设备|控制|计量|装置/.test(cat)) domains.push("hardware");
    if (/工艺|外延|清洗|集成|结构|沉积|晶圆|腔室|Si\s*\/\s*SiGe/i.test(cat) || tags.includes("chamber_clean")) {
      domains.push("process");
    }
    if (!domains.length) domains.push(/设备/.test(cat) ? "hardware" : "process");

    const lanes = [];
    if (tags.includes("preclean") || /preclean/i.test(cat) || lane === "Preclean") lanes.push("preclean");
    if (tags.includes("epi") || /EPI|外延/i.test(cat) || lane === "EPI" || !lanes.length) lanes.push("epi");

    return { domains: domains, lanes: lanes };
  }

  function familyPassesChipFilter(f, activeDomain, activeLane) {
    const c = classifyFamily(f);
    if (activeDomain.size) {
      for (const d of activeDomain) {
        if (c.domains.indexOf(d) === -1) return false;
      }
    }
    if (activeLane.size) {
      for (const l of activeLane) {
        if (c.lanes.indexOf(l) === -1) return false;
      }
    }
    return true;
  }

  const PATENT_COLGROUP =
    "<colgroup><col class=\"patent-col-label\"><col class=\"patent-col-value\"></colgroup>";

  function patentFieldRow(label, valueHtml, valueClass) {
    const vc = valueClass ? " " + valueClass : "";
    return (
      "<tr><th scope=\"row\" class=\"patent-label\">" + esc(label) + "</th>" +
      "<td class=\"patent-value" + vc + "\">" + valueHtml + "</td></tr>"
    );
  }

  function countBag(c) {
    const monthEntries = (c.month_family_entries != null) ? c.month_family_entries
      : (c.candidates_total != null ? c.candidates_total : 0);
    const events = (c.publication_events != null) ? c.publication_events
      : (c.events_core != null ? c.events_core : 0);
    const families = (c.unique_families != null) ? c.unique_families
      : (c.families_core != null ? c.families_core : 0);
    // Locked ruling count only — never infer from independent_search row count.
    const read = (c.actually_read != null) ? c.actually_read : 0;
    return { monthEntries: monthEntries, events: events, families: families, read: read };
  }

  function figureLabelFromCaption(caption, fallback) {
    if (!caption) return fallback || "";
    const m = String(caption).match(/FIGS?\.?\s*([\dA-Za-z][\dA-Za-z.\-–—]*)/i);
    if (m) return "Fig. " + m[1].replace(/\s+/g, "");
    const m2 = String(caption).match(/图\s*([\dA-Za-z][\dA-Za-z.\-–—]*)/);
    if (m2) return "图" + m2[1];
    return fallback || "";
  }

  function renderReportNotes(data) {
    const parts = [];
    if (data.scope) {
      parts.push("<p><strong>范围</strong> " + esc(data.scope) + "</p>");
    }
    if (data.excluded_scope) {
      parts.push("<p><strong>排除</strong> " + esc(data.excluded_scope) + "</p>");
    }
    if (data.count_basis) {
      parts.push("<p><strong>计数口径</strong> " + esc(data.count_basis) + "</p>");
    }
    if (data.coverage_note) {
      parts.push("<p>" + esc(data.coverage_note) + "</p>");
    }
    const read = (data.counts && data.counts.actually_read != null) ? data.counts.actually_read : 0;
    parts.push(
      "<p class=\"subtle\">初版（非正式交付）：含 Dot 基线导入与 Gate ③ 独立检索增量。" +
      "「本团队已读」= 证据裁定权利要求级阅读（锁定 " + esc(read) + "，见 EVIDENCE-READ-RULING-COMBINED）；独立纳入 9 条 ≠ 已读 9。</p>"
    );
    if ((data.counts && data.counts.pending) > 0) {
      parts.push("<p class=\"subtle\">待核 " + esc(data.counts.pending) + " 条见下方「关联待核」区，未作为独立新发现纳入主表。</p>");
    }
    return parts.join("");
  }

  function renderReportInfoFooter(data) {
    const el = $("#banner");
    if (!el) return;
    const c = data.counts || {};
    const bag = countBag(c);
    const fig = computeFigureStats(data);
    const statsBlock =
      "<dl class=\"report-stats-dl\">" +
      "<dt>版本</dt><dd>" + esc(editionLabel(data)) + "</dd>" +
      "<dt>族月条目</dt><dd>" + esc(bag.monthEntries) + "</dd>" +
      "<dt>事件（去重公开号）</dt><dd>" + esc(bag.events) + "</dd>" +
      "<dt>族</dt><dd>" + esc(bag.families) + "</dd>" +
      "<dt>本团队已读</dt><dd>" + esc(bag.read) + "</dd>" +
      "<dt>附图</dt><dd>引用 " + esc(fig.cited) + " · 可加载 " + esc(fig.loadable) + " · 待补 " + esc(fig.pending) + "</dd>" +
      "</dl>";
    el.innerHTML =
      "<details class=\"report-info\">" +
      "<summary>报告信息（计数与说明，默认收起）</summary>" +
      "<div class=\"report-info-body\">" +
      statsBlock +
      renderReportNotes(data) +
      "</div></details>";
  }


  function renderTree(data) {
    const tree = $("#tree");
    if (!tree) return;
    const months = data.months || [];
    if (!months.length) {
      tree.innerHTML = "<p class=\"month-empty\">无月份数据</p>";
      return;
    }

    const frag = document.createDocumentFragment();
    months.forEach((m, idx) => {
      const details = document.createElement("details");
      details.className = "month";
      details.dataset.month = m.month;
      // Do not auto-open on scroll; only open newest by default if it has content, else leave closed.
      // Scaffold: leave all closed so empty months stay compact.
      const summary = document.createElement("summary");
      const count = (m.families || []).length;
      summary.innerHTML =
        "<span class=\"month-summary-head\">" +
        "<span class=\"month-label\">" + esc(formatMonthLabel(m.month)) + "</span>" +
        "<span class=\"month-count\">" + count + " 族</span>" +
        "</span>";
      details.appendChild(summary);

      const body = document.createElement("div");
      body.className = "month-body";
      const families = familiesNewestFirst(m);
      if (!families.length) {
        body.innerHTML =
          "<div class=\"month-empty\">" +
          esc(m.status || "暂无条目") +
          (m.through_date ? " · 截至 " + esc(m.through_date) : "") +
          "</div>";
      } else {
        families.forEach((raw) => {
          const f = normFamily(raw, m.month);
          const chipClass = classifyFamily(f);
          const domain = chipClass.domains.join(" ");
          const lane = chipClass.lanes.join(" ");

          const collapsed = document.createElement("a");
          collapsed.className = "mini mini--toc-collapsed";
          collapsed.href = "#" + encodeURIComponent(f.id);
          collapsed.dataset.target = f.id;
          collapsed.dataset.filterDomain = domain;
          collapsed.dataset.filterLane = lane;
          collapsed.innerHTML =
            "<span class=\"mini-collapsed-date\">" + esc(f.publication_date || "") + "</span>" +
            "<span class=\"mini-collapsed-pub\">" + esc(f.publication_number || "") + "</span>";
          collapsed.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            jumpToPatent(f.id, collapsed);
          });
          collapsedStrip.appendChild(collapsed);

          const a = document.createElement("a");
          a.className = "mini mini--toc-expanded";
          a.href = "#" + encodeURIComponent(f.id);
          a.dataset.target = f.id;
          a.dataset.filterDomain = domain;
          a.dataset.filterLane = lane;
          a.innerHTML =
            "<span class=\"mini-date\">" + esc(f.publication_date || "") + "</span>" +
            "<span class=\"mini-title\">" + esc(f.title || f.publication_number || "") + "</span>" +
            "<span class=\"mini-meta\">" + esc(f.publication_number || "") +
            (f.applicant ? " · " + esc(f.applicant) : "") + "</span>" +
            "<span class=\"mini-brief\">" + esc(f.brief || f.summary || "") + "</span>";
          a.addEventListener("click", (e) => {
            e.preventDefault();
            jumpToPatent(f.id, a);
          });
          body.appendChild(a);
        });
      }
      details.appendChild(body);
      frag.appendChild(details);
    });
    tree.innerHTML = "";
    tree.appendChild(frag);
  }

  function setActiveMini(id) {
    document.querySelectorAll(".mini.active").forEach((n) => n.classList.remove("active"));
    document.querySelectorAll(".month.month--spy-active").forEach((n) => n.classList.remove("month--spy-active"));
    const links = document.querySelectorAll('.mini[data-target="' + CSS.escape(id) + '"]');
    links.forEach((link) => link.classList.add("active"));
    const month = links.length ? links[0].closest("details.month") : null;
    if (month && !month.open) month.classList.add("month--spy-active");

    const tree = $("#tree");
    if (!tree || !links.length) return;
    const collapsed = document.querySelector(
      '.mini--toc-collapsed[data-target="' + CSS.escape(id) + '"]'
    );
    const expanded = document.querySelector(
      '.mini--toc-expanded[data-target="' + CSS.escape(id) + '"]'
    );
    const scrollEl =
      collapsed && collapsed.offsetParent !== null
        ? collapsed
        : expanded && expanded.offsetParent !== null
          ? expanded
          : collapsed || expanded;
    if (!scrollEl) return;
    const tRect = tree.getBoundingClientRect();
    const eRect = scrollEl.getBoundingClientRect();
    if (eRect.top < tRect.top + 4 || eRect.bottom > tRect.bottom - 4) {
      scrollEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  }

  function jumpToPatent(id, miniEl) {
    const page = document.getElementById(id);
    if (!page) return;
    // Open only the month that owns this patent; do not touch other months' open state beyond ensuring target's month is open.
    const monthDetails = miniEl ? miniEl.closest("details.month") : null;
    if (monthDetails) monthDetails.open = true;
    setActiveMini(id);
    page.focus({ preventScroll: true });
    page.scrollIntoView({ behavior: "smooth", block: "start" });
    history.replaceState(null, "", "#" + encodeURIComponent(id));
  }

  function renderEvents(events) {
    if (!events || !events.length) return "<span class=\"subtle\">—</span>";
    let html = "<table class=\"events\"><thead><tr><th>号</th><th>日期</th><th>事件</th></tr></thead><tbody>";
    events.forEach((ev) => {
      const num = ev.source_url
        ? "<a href=\"" + esc(ev.source_url) + "\" target=\"_blank\" rel=\"noopener\">" + esc(ev.number) + "</a>"
        : esc(ev.number);
      html += "<tr><td>" + num + "</td><td>" + esc(ev.date || "") + "</td><td>" + esc(ev.event || "") + "</td></tr>";
    });
    html += "</tbody></table>";
    return html;
  }

  function renderFamilyContext(ctx) {
    if (!ctx || !ctx.length) return "<span class=\"subtle\">—</span>";
    return ctx.map((c) => esc(c.number) + (c.date ? " (" + esc(c.date) + ")" : "")).join("； ");
  }

  function reportDataUrl() {
    const meta = document.querySelector('meta[name="epi-report-data"]');
    const url = meta && meta.getAttribute("content");
    return (url && url.trim()) ? url.trim() : "data/report.json";
  }

  /** display_rotation only — never combine with extraction_rotation (baked into bytes). */
  function effectiveDisplayRotation(img) {
    const rot = Number(img.display_rotation) || 0;
    if (!rot) return 0;
    const w = Number(img.width) || 0;
    const h = Number(img.height) || 0;
    if (w <= 0 || h <= 0) return 0;
    return rot % 360;
  }

  function annotationsVerified(img) {
    const ann = img.annotations;
    if (!ann || ann.version !== 1 || !ann.labels || !ann.labels.length) return null;
    const sha = img.sha256 || "";
    if (!sha || ann.image_sha256 !== sha) return null;
    return ann;
  }

  function labelByNumber(ann) {
    const map = {};
    (ann.labels || []).forEach((l) => {
      if (l && l.number != null) map[String(l.number)] = l;
    });
    return map;
  }

  function renderFigureLabelList(ann) {
    const n = (ann.labels || []).length;
    if (!n) return "";
    const rows = ann.labels
      .map(
        (l) =>
          "<dt>" + esc(l.number) + "</dt><dd><strong>" + esc(l.display_name || "") + "</strong> " +
          esc(l.display_description || "") + "</dd>"
      )
      .join("");
    return (
      "<details class=\"figure-label-list\">" +
      "<summary>标号释义（" + n + "项）</summary><dl>" + rows + "</dl></details>"
    );
  }

  function renderFigureHotspots(ann) {
    const byNum = labelByNumber(ann);
    const occ = ann.occurrences || [];
    if (!occ.length) return "";
    const buttons = occ
      .map((o) => {
        const box = o.box;
        if (!box || box.length < 4) return "";
        const lab = byNum[String(o.number)];
        if (!lab) return "";
        const x = box[0] * 100;
        const y = box[1] * 100;
        const w = box[2] * 100;
        const h = box[3] * 100;
        const title = lab.number + " · " + (lab.display_name || "");
        return (
          "<button type=\"button\" class=\"figure-label-hotspot\" " +
          "style=\"left:" + x + "%;top:" + y + "%;width:" + w + "%;height:" + h + "%\" " +
          "data-label-number=\"" + esc(lab.number) + "\" " +
          "data-popup-title=\"" + esc(title) + "\" " +
          "data-popup-desc=\"" + esc(lab.display_description || "") + "\" " +
          "aria-label=\"" + esc(title) + "\"></button>"
        );
      })
      .filter(Boolean)
      .join("");
    if (!buttons) return "";
    return "<div class=\"figure-label-overlay\" aria-hidden=\"false\">" + buttons + "</div>";
  }

  function stripFigureRotationIfUpright(img) {
    const nw = img.naturalWidth;
    const nh = img.naturalHeight;
    if (!nw || !nh) return;
    const metaRot = Number(img.getAttribute("data-display-rotation") || "0") || 0;
    if (metaRot) return;
    if (nh >= nw) {
      img.classList.remove("fig-display-rot-90", "fig-display-rot-270", "fig-display-rot-180");
      img.style.transform = "none";
      const wrap = img.closest(".fig-media");
      if (wrap) wrap.classList.remove("fig-display-rot-90", "fig-display-rot-270", "fig-display-rot-180");
      const plane = img.closest(".figure-display-plane");
      if (plane) plane.classList.remove("fig-display-rot-90", "fig-display-rot-270", "fig-display-rot-180");
    }
  }

  /** Layout box for display_rotation (extraction_rotation already baked into file bytes). */
  function figureLayoutDims(w, h, displayRotation) {
    const rw = w > 0 ? w : 640;
    const rh = h > 0 ? h : 480;
    const rot = displayRotation % 360;
    if (rot === 90 || rot === 270) {
      return { layoutW: rh, layoutH: rw, rotClass: "fig-display-rot-" + rot };
    }
    if (rot === 180) {
      return { layoutW: rw, layoutH: rh, rotClass: "fig-display-rot-180" };
    }
    return { layoutW: rw, layoutH: rh, rotClass: "" };
  }

  function figureFailBox(w, h, pub, figLabel, reason) {
    const meta = [pub, figLabel].filter(Boolean).join(" · ");
    const why = reason || "真图缺失";
    return (
      "<div class=\"fig-fail\" role=\"img\" " +
      "aria-label=\"图加载失败：" + esc(why) + (meta ? " " + esc(meta) : "") + "\">" +
      "<div class=\"fig-fail-title\">图加载失败 / " + esc(why) + "</div>" +
      (meta ? "<div class=\"fig-fail-meta\">" + esc(meta) + "</div>" : "") +
      "<div class=\"fig-fail-hint\">仅真实专利附图；不用 AI 生成图占位</div>" +
      "</div>"
    );
  }

  function renderImages(images) {
    if (!images || !images.length) return "";
    const blocks = images.map((img) => {
      const caption =
        img.display_caption ||
        img.caption ||
        [img.source_publication, img.figure_label].filter(Boolean).join(" · ");
      const pub = img.source_publication || "";
      const figLabel = figureLabelFromCaption(img.caption || img.display_caption, img.figure_label || "");
      const w = img.width || 640;
      const h = img.height || 480;
      const effRot = effectiveDisplayRotation(img);
      const layout = figureLayoutDims(w, h, effRot);
      const ar = (layout.layoutW > 0 && layout.layoutH / layout.layoutW <= 1.6)
        ? layout.layoutW + "/" + layout.layoutH
        : "16/10";
      const rotClass = layout.rotClass ? " " + layout.rotClass : "";
      const planeAspect =
        effRot === 90 || effRot === 270
          ? " style=\"aspect-ratio:" + w + "/" + h + "\""
          : "";
      const src = img.path || "";
      let body;
      const ann = src ? annotationsVerified(img) : null;
      const hotspotHtml = ann ? renderFigureHotspots(ann) : "";
      const labelListHtml = ann ? renderFigureLabelList(ann) : "";
      if (src) {
        body =
          "<div class=\"figure-display-stage\"" + (ann ? " data-annotate=\"1\"" : "") + ">" +
          "<div class=\"fig-media" + rotClass + "\" style=\"aspect-ratio:" + ar + "\">" +
          "<div class=\"figure-display-plane" + rotClass + "\"" + planeAspect + ">" +
          "<img class=\"fig-img\" data-src=\"" + esc(src) +
          "\" width=\"" + layout.layoutW + "\" height=\"" + layout.layoutH +
          "\" alt=\"" + esc(caption) + "\" loading=\"lazy\" decoding=\"async\" " +
          "data-display-rotation=\"" + effRot + "\" " +
          "data-fig-pub=\"" + esc(pub) + "\" data-fig-label=\"" + esc(figLabel) + "\">" +
          hotspotHtml +
          "</div></div></div>";
      } else {
        body = figureFailBox(w, h, pub, figLabel, "真图缺失");
      }
      return (
        "<figure class=\"fig" + (src ? "" : " fig--missing") + "\">" +
        body +
        labelListHtml +
        "<figcaption>" + esc(caption) +
        (img.source_url ? " · <a href=\"" + esc(img.source_url) + "\" target=\"_blank\" rel=\"noopener\">来源</a>" : "") +
        "</figcaption></figure>"
      );
    }).join("");
    if (images.length < 2) return blocks;
    return (
      "<div class=\"patent-fig-grid\" data-fig-count=\"" + images.length + "\">" +
      blocks +
      "</div>"
    );
  }

  function renderSources(urls) {
    if (!urls || !urls.length) return "<span class=\"subtle\">—</span>";
    return "<ul class=\"source-list\">" +
      urls.map((u) => "<li><a href=\"" + esc(u) + "\" target=\"_blank\" rel=\"noopener\">" + esc(u) + "</a></li>").join("") +
      "</ul>";
  }

  function renderPatentPage(f) {
    const chipClass = classifyFamily(f);
    const titleBlock =
      "<span class=\"patent-title\">" + esc(f.title || "") + "</span>" +
      (f.title_original
        ? "<span class=\"title-translation\">" + esc(f.title_original) + "</span>"
        : "");

    const figBlock = renderImages(f.images) || "<span class=\"subtle\">无附图（不得用生成图替代）</span>";
    return (
      "<article class=\"patent-page\" id=\"" + esc(f.id) + "\" tabindex=\"-1\" data-month=\"" + esc(f.month || "") + "\" " +
      "data-filter-domain=\"" + esc(chipClass.domains.join(" ")) + "\" " +
      "data-filter-lane=\"" + esc(chipClass.lanes.join(" ")) + "\">" +
      "<header class=\"patent-page-header\">" + titleBlock + "</header>" +
      "<table class=\"patent-table\">" + PATENT_COLGROUP +
      patentFieldRow("公开号", esc(f.publication_number || "")) +
      patentFieldRow("申请人", esc(f.applicant || "")) +
      patentFieldRow(
        "公开/授权日",
        esc(f.publication_date || "") + (f.category ? " · " + esc(f.category) : "")
      ) +
      patentFieldRow(
        "同族 / 事件",
        "<div class=\"section-label\">同族关系</div>" + renderFamilyContext(f.family_context) +
        "<div class=\"section-label\">公开/授权事件</div>" + renderEvents(f.events) +
        (f.event_note ? "<div class=\"subtle\">" + esc(f.event_note) + "</div>" : ""),
        "section-body"
      ) +
      patentFieldRow(
        "中文技术简介",
        text(f.summary || f.brief || "") +
        (f.purpose ? "<div class=\"section-label\">目的</div>" + text(f.purpose) : "") +
        (f.novelty ? "<div class=\"section-label\">要点</div>" + text(f.novelty) : "") +
        (f.use ? "<div class=\"section-label\">用途</div>" + text(f.use) : ""),
        "section-body"
      ) +
      patentFieldRow("关键权利要求 / 实施方式", text(f.claims || "—"), "section-body claim-text") +
      patentFieldRow(
        "相关性",
        text(f.relevance || "") +
        (scopeLabelZh(f.scope_status)
          ? "<div class=\"subtle\">范围：" + esc(scopeLabelZh(f.scope_status)) + "</div>"
          : "") +
        (discoveryLabelZh(f.discovery_source)
          ? "<div class=\"subtle\">来源：" + esc(discoveryLabelZh(f.discovery_source)) + "</div>"
          : "") +
        (importTagZh(f.import_tag) && f.import_tag === "imported baseline"
          ? "<div class=\"subtle import-tag\">基线导入（非独立发现）</div>"
          : "") +
        (f.family_merge_note
          ? "<div class=\"subtle\">同族：" + esc(f.family_merge_note) + "</div>"
          : ""),
        "section-body"
      ) +
      patentFieldRow("来源链接", renderSources(f.source_urls), "section-body") +
      "<tr class=\"patent-row-figures\"><th colspan=\"2\" class=\"patent-section-heading\">附图</th></tr>" +
      "<tr class=\"patent-row-figures\"><td colspan=\"2\" class=\"patent-figures-cell section-body\">" +
      figBlock + "</td></tr>" +
      "</table></article>"
    );
  }

  function renderContent(data) {
    const main = $("#content");
    if (!main) return;
    const pages = [];
    (data.months || []).forEach((m) => {
      familiesNewestFirst(m).forEach((raw) => pages.push(renderPatentPage(normFamily(raw, m.month))));
    });
    if (!pages.length) {
      main.innerHTML =
        "<div class=\"empty-state\">" +
        "<p><strong>尚无专利条目</strong></p>" +
        "<p>月份目录已就位（" + esc((data.period_start || "") + "–" + (data.period_end || "")) +
        "）。待独立检索与 Codex 材料填入 <code>data/report.json</code> 后刷新本页。</p>" +
        "<p>空月 ≠ 零命中。检索失败与待核须保留原因。</p>" +
        "</div>";
      return;
    }
    main.innerHTML = pages.join("") + renderPendingQueue(data);
  }

  function renderPendingQueue(data) {
    const rows = data.pending_or_related || [];
    if (!rows.length) return "";
    let body = "<ul class=\"pending-list\">";
    rows.forEach((r) => {
      const pub = r.publication_id || "—";
      const date = r.event_date ? " · " + r.event_date : "";
      const onMain = r.on_main_month_cards
        ? "（基线主表已有，待核不复核升格）"
        : "（未入主表）";
      body +=
        "<li><strong>" + esc(pub) + "</strong>" + esc(date) +
        " — " + esc(r.title_zh || "") +
        "<div class=\"subtle\">" + esc(r.pending_reason || r.failure_or_pending_reason || "") +
        " " + esc(onMain) + "</div></li>";
    });
    body += "</ul>";
    return (
      "<details class=\"pending-queue\">" +
      "<summary>关联待核（" + rows.length + "）</summary>" +
      "<div class=\"pending-queue-body\">" + body + "</div></details>"
    );
  }

  function swapImgToFail(img, reason) {
    const figure = img.closest("figure.fig");
    const w = parseInt(img.getAttribute("width"), 10) || 640;
    const h = parseInt(img.getAttribute("height"), 10) || 480;
    const pub = img.getAttribute("data-fig-pub") || "";
    const figLabel = img.getAttribute("data-fig-label") || "";
    const wrap = document.createElement("div");
    wrap.innerHTML = figureFailBox(w, h, pub, figLabel, reason || "路径损坏");
    const box = wrap.firstChild;
    img.replaceWith(box);
    if (figure) figure.classList.add("fig--missing");
  }

  function initLazyImages() {
    const imgs = document.querySelectorAll("img[data-src]");
    if (!imgs.length) return;

    function reveal(img) {
      const src = img.getAttribute("data-src");
      if (!src) {
        swapImgToFail(img, "真图缺失");
        return;
      }
      img.onerror = function () {
        swapImgToFail(img, "路径损坏");
      };
      img.onload = function () {
        stripFigureRotationIfUpright(img);
      };
      img.src = src;
      img.removeAttribute("data-src");
    }

    if (!("IntersectionObserver" in window)) {
      imgs.forEach(reveal);
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            reveal(e.target);
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: "600px 0px" }
    );
    imgs.forEach((img) => io.observe(img));
  }


  function initChipFilters() {
    const chips = document.querySelectorAll(".filter-chip");
    const countEl = $("#filter-count");
    const clearBtn = $("#filter-clear");
    if (!chips.length) return;

    const activeDomain = new Set();
    const activeLane = new Set();

    function pagePasses(page) {
      const domains = (page.dataset.filterDomain || "").split(/\s+/).filter(Boolean);
      const lanes = (page.dataset.filterLane || "").split(/\s+/).filter(Boolean);
      if (activeDomain.size) {
        for (const d of activeDomain) {
          if (domains.indexOf(d) === -1) return false;
        }
      }
      if (activeLane.size) {
        for (const l of activeLane) {
          if (lanes.indexOf(l) === -1) return false;
        }
      }
      return true;
    }

    function applyFilter() {
      let visible = 0;
      document.querySelectorAll(".patent-page").forEach((page) => {
        const show = pagePasses(page);
        page.hidden = !show;
        if (show) visible += 1;
      });
      document.querySelectorAll(".mini").forEach((mini) => {
        const page = document.getElementById(mini.dataset.target || "");
        mini.style.display = page && !page.hidden ? "" : "none";
      });
      document.querySelectorAll("details.month").forEach((month) => {
        const any = month.querySelector('.mini:not([style*="display: none"])');
        month.classList.toggle("month--filter-empty", !!activeDomain.size || !!activeLane.size ? !any : false);
      });
      const filtered = activeDomain.size > 0 || activeLane.size > 0;
      if (countEl) countEl.textContent = filtered ? "显示 " + visible + " 族" : "";
      if (clearBtn) clearBtn.hidden = !filtered;
    }

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const key = chip.dataset.filter;
        const group = chip.closest("[data-filter-group]");
        const laneGroup = group && group.dataset.filterGroup === "lane";
        const set = laneGroup ? activeLane : activeDomain;
        if (set.has(key)) set.delete(key);
        else set.add(key);
        chip.setAttribute("aria-pressed", set.has(key) ? "true" : "false");
        applyFilter();
      });
    });

    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        activeDomain.clear();
        activeLane.clear();
        chips.forEach((c) => c.setAttribute("aria-pressed", "false"));
        applyFilter();
      });
    }
    applyFilter();
  }

  function initFigureLabelUI() {
    const popup = $("#figure-label-popup");
    if (!popup) return;
    const titleEl = $(".figure-label-popup-title", popup);
    const descEl = $(".figure-label-popup-desc", popup);
    const closeBtn = $(".figure-label-popup-close", popup);
    const coarsePointer = window.matchMedia("(hover: none), (pointer: coarse)").matches;
    let pinned = false;
    let closeTimer = null;
    let anchorBtn = null;

    function clearCloseTimer() {
      if (closeTimer) {
        clearTimeout(closeTimer);
        closeTimer = null;
      }
    }

    function scheduleClose() {
      clearCloseTimer();
      if (pinned) return;
      closeTimer = setTimeout(closePopup, 160);
    }

    function closePopup() {
      pinned = false;
      anchorBtn = null;
      popup.hidden = true;
      popup.removeAttribute("data-pinned");
    }

    function positionPopup() {
      if (!anchorBtn || popup.hidden) return;
      const r = anchorBtn.getBoundingClientRect();
      const margin = 8;
      let top = r.bottom + margin;
      let left = r.left + r.width / 2;
      popup.style.left = left + "px";
      popup.style.top = top + "px";
      popup.style.transform = "translate(-50%, 0)";
      const pr = popup.getBoundingClientRect();
      const vw = window.visualViewport ? window.visualViewport.width : window.innerWidth;
      const vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
      const voX = window.visualViewport ? window.visualViewport.offsetLeft : 0;
      const voY = window.visualViewport ? window.visualViewport.offsetTop : 0;
      if (pr.right > voX + vw - margin) {
        left = voX + vw - margin - pr.width / 2;
        popup.style.left = left + "px";
      }
      if (pr.left < voX + margin) {
        left = voX + margin + pr.width / 2;
        popup.style.left = left + "px";
      }
      if (pr.bottom > voY + vh - margin) {
        top = r.top - margin - pr.height;
        popup.style.top = top + "px";
        popup.style.transform = "translate(-50%, -100%)";
      }
      const pr2 = popup.getBoundingClientRect();
      if (pr2.top < voY + margin || pr2.bottom > voY + vh - margin) closePopup();
    }

    function openPopup(btn, pin) {
      anchorBtn = btn;
      pinned = !!pin;
      titleEl.textContent = btn.getAttribute("data-popup-title") || "";
      descEl.textContent = btn.getAttribute("data-popup-desc") || "";
      popup.hidden = false;
      if (pinned) popup.setAttribute("data-pinned", "1");
      else popup.removeAttribute("data-pinned");
      positionPopup();
    }

    function wireHotspot(btn) {
      if (btn.dataset.labelWired === "1") return;
      btn.dataset.labelWired = "1";
      btn.addEventListener("pointerenter", () => {
        if (coarsePointer) return;
        clearCloseTimer();
        openPopup(btn, false);
      });
      btn.addEventListener("pointerleave", () => {
        if (coarsePointer) return;
        scheduleClose();
      });
      btn.addEventListener("focus", () => openPopup(btn, false));
      btn.addEventListener("blur", () => {
        if (!pinned) scheduleClose();
      });
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (pinned && anchorBtn === btn) closePopup();
        else openPopup(btn, true);
      });
    }

    function mountStage(stage) {
      if (stage.dataset.annotMounted === "1") return;
      stage.dataset.annotMounted = "1";
      stage.querySelectorAll(".figure-label-hotspot").forEach(wireHotspot);
    }

    function observeStages() {
      const stages = document.querySelectorAll(".figure-display-stage[data-annotate=\"1\"]");
      if (!stages.length) return;
      if (!("IntersectionObserver" in window)) {
        stages.forEach(mountStage);
        return;
      }
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            if (e.isIntersecting) {
              mountStage(e.target);
              io.unobserve(e.target);
            }
          });
        },
        { rootMargin: "700px 0px" }
      );
      stages.forEach((s) => io.observe(s));
    }

    popup.addEventListener("pointerenter", clearCloseTimer);
    popup.addEventListener("pointerleave", scheduleClose);
    if (closeBtn) closeBtn.addEventListener("click", closePopup);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !popup.hidden) closePopup();
    });
    document.addEventListener(
      "pointerdown",
      (e) => {
        if (popup.hidden) return;
        if (popup.contains(e.target) || e.target.closest(".figure-label-hotspot")) return;
        closePopup();
      },
      true
    );
    window.addEventListener("scroll", positionPopup, true);
    window.addEventListener("resize", positionPopup);
    if (window.visualViewport) {
      window.visualViewport.addEventListener("resize", positionPopup);
      window.visualViewport.addEventListener("scroll", positionPopup);
    }
    observeStages();
  }

  function initScrollSpy() {
    const pages = document.querySelectorAll(".patent-page");
    if (!pages.length || !("IntersectionObserver" in window)) return;
    const visible = new Map();

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) visible.set(e.target.id, e.intersectionRatio);
          else visible.delete(e.target.id);
        });
        let bestId = null;
        let bestRatio = 0;
        visible.forEach((ratio, id) => {
          if (ratio > bestRatio) {
            bestRatio = ratio;
            bestId = id;
          }
        });
        if (bestId) setActiveMini(bestId);
        // No details.open = true here — scroll must not auto-expand closed months.
      },
      { rootMargin: "-20% 0px -55% 0px", threshold: [0, 0.1, 0.25, 0.5] }
    );
    pages.forEach((p) => io.observe(p));
  }

  async function main() {
    loadSidebarWidth();
    initResizer();
    initMobileDrawer();

    let data;
    try {
      const res = await fetch(reportDataUrl(), { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      data = await res.json();
    } catch (err) {
      $("#content").innerHTML =
        "<div class=\"empty-state\"><p>无法加载 <code>data/report.json</code>：" +
        esc(err.message) +
        "</p><p>请用本地静态服务器打开（见 README），不要直接用 file://。</p></div>";
      return;
    }

    document.title = data.browser_title || data.title || document.title;
    renderSideMeta();
    renderTree(data);
    renderContent(data);
    renderReportInfoFooter(data);
    initChipFilters();
    initLazyImages();
    initFigureLabelUI();
    initScrollSpy();

    if (location.hash) {
      const id = decodeURIComponent(location.hash.slice(1));
      const mini = document.querySelector('.mini[data-target="' + CSS.escape(id) + '"]');
      if (mini) jumpToPatent(id, mini);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", main);
  } else {
    main();
  }
})();
