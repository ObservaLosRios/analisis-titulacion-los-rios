"use strict";

// Titulación Los Ríos – lógica de visualización y UI (extraída del HTML)
(() => {
  // ============================ DATOS ============================
  const dataTitulaciones = [
    { año: 2007, total: 1757 },
    { año: 2008, total: 1800 },
    { año: 2009, total: 2310 },
    { año: 2010, total: 1846 },
    { año: 2011, total: 2329 },
    { año: 2012, total: 2267 },
    { año: 2013, total: 2770 },
    { año: 2014, total: 3078 },
    { año: 2015, total: 3312 },
    { año: 2016, total: 3508 },
    { año: 2017, total: 3842 },
    { año: 2018, total: 3772 },
    { año: 2019, total: 4086 },
    { año: 2020, total: 3000 },
    { año: 2021, total: 4754 },
    { año: 2022, total: 4859 },
    { año: 2023, total: 4782 },
    { año: 2024, total: 5098 }
  ];

  const dataTipo = [
    { año: 2007, Pregrado: 1523, Posgrado: 113, Postítulo: 121 },
    { año: 2008, Pregrado: 1761, Posgrado: 6, Postítulo: 33 },
    { año: 2009, Pregrado: 1964, Posgrado: 153, Postítulo: 193 },
    { año: 2010, Pregrado: 1585, Posgrado: 157, Postítulo: 142 },
    { año: 2011, Pregrado: 2033, Posgrado: 154, Postítulo: 142 },
    { año: 2012, Pregrado: 1999, Posgrado: 196, Postítulo: 72 },
    { año: 2013, Pregrado: 2551, Posgrado: 183, Postítulo: 36 },
    { año: 2014, Pregrado: 2767, Posgrado: 195, Postítulo: 116 },
    { año: 2015, Pregrado: 2975, Posgrado: 185, Postítulo: 152 },
    { año: 2016, Pregrado: 3035, Posgrado: 233, Postítulo: 240 },
    { año: 2017, Pregrado: 3290, Posgrado: 286, Postítulo: 266 },
    { año: 2018, Pregrado: 3298, Posgrado: 295, Postítulo: 179 },
    { año: 2019, Pregrado: 3671, Posgrado: 210, Postítulo: 205 },
    { año: 2020, Pregrado: 2481, Posgrado: 315, Postítulo: 204 },
    { año: 2021, Pregrado: 4341, Posgrado: 306, Postítulo: 204 },
    { año: 2022, Pregrado: 4292, Posgrado: 301, Postítulo: 266 },
    { año: 2023, Pregrado: 4484, Posgrado: 168, Postítulo: 130 },
    { año: 2024, Pregrado: 4702, Posgrado: 292, Postítulo: 104 }
  ];

  const coloresTipo = { Pregrado: "#0072B2", Posgrado: "#D55E00", Postítulo: "#009E73" };
  const tipoVisibility = { Pregrado: true, Posgrado: true, Postítulo: true };

  const dataSexo = [
    { año: 2007, Hombre: 876, Mujer: 881 },
    { año: 2008, Hombre: 773, Mujer: 1027 },
    { año: 2009, Hombre: 1025, Mujer: 1285 },
    { año: 2010, Hombre: 892, Mujer: 954 },
    { año: 2011, Hombre: 1006, Mujer: 1309 },
    { año: 2012, Hombre: 906, Mujer: 1361 },
    { año: 2013, Hombre: 1246, Mujer: 1524 },
    { año: 2014, Hombre: 1380, Mujer: 1698 },
    { año: 2015, Hombre: 1401, Mujer: 1911 },
    { año: 2016, Hombre: 1441, Mujer: 2067 },
    { año: 2017, Hombre: 1656, Mujer: 2186 },
    { año: 2018, Hombre: 1525, Mujer: 2247 },
    { año: 2019, Hombre: 1635, Mujer: 2451 },
    { año: 2020, Hombre: 1316, Mujer: 1684 },
    { año: 2021, Hombre: 1916, Mujer: 2838 },
    { año: 2022, Hombre: 2007, Mujer: 2852 },
    { año: 2023, Hombre: 2026, Mujer: 2756 },
    { año: 2024, Hombre: 2240, Mujer: 2858 }
  ];

  const coloresSexo = { Hombre: "#0072B2", Mujer: "#D55E00" };
  const sexoVisibility = { Hombre: true, Mujer: true };

  // ============================ HELPERS UI ============================
  function isMobileDevice() { return window.innerWidth <= 768; }
  function getResponsivePadding(top = 80, right = 40, bottom = 60, left = 100) {
    const isMobile = window.innerWidth <= 768;
    const isSmall = window.innerWidth <= 480;
    if (isSmall) return { top: Math.max(top * 0.6, 40), right: Math.max(right * 0.5, 20), bottom: Math.max(bottom * 0.8, 40), left: Math.max(left * 0.6, 60) };
    if (isMobile) return { top: Math.max(top * 0.75, 50), right: Math.max(right * 0.7, 30), bottom: Math.max(bottom * 0.9, 50), left: Math.max(left * 0.75, 70) };
    return { top, right, bottom, left };
  }
  function drawElegantVerticalLine(canvas, ctx, x, padding, chartHeight) {
    ctx.save();
    ctx.strokeStyle = "rgba(100, 100, 100, 0.15)";
    ctx.lineWidth = 1;
    ctx.setLineDash([]);
    ctx.beginPath();
    ctx.moveTo(x, padding.top + 10);
    ctx.lineTo(x, padding.top + chartHeight - 10);
    ctx.stroke();
    ctx.restore();
  }
  function getYearFromMousePosition(mouseX, padding, chartWidth, minYear, maxYear) {
    const offset = 15;
    const effectiveWidth = chartWidth - offset;
    const relativeX = mouseX - padding.left - offset;
    if (relativeX < 0 || relativeX > effectiveWidth) return null;
    const yearRange = maxYear - minYear;
    const yearFloat = minYear + (relativeX / effectiveWidth) * yearRange;
    return Math.round(yearFloat);
  }
  function showMinimalistTooltip(event, year, data) {
    const tooltip = document.getElementById("tooltip");
    if (!tooltip) return;
    let content = `<div style="font-weight: bold; font-size: 13px; color: #666; margin-bottom: 8px;">${year}</div>`;
    data.forEach(item => {
      content += `\n<div style="display: flex; align-items: center; margin-bottom: 4px; font-size: 12px;">\n  <div style="width: 10px; height: 10px; background-color: ${item.color}; margin-right: 8px; border-radius: 2px;"></div>\n  <span style="color: #444; margin-right: 10px; min-width: 60px;">${item.label}</span>\n  <span style="color: #666; font-weight: 500;">${item.value}</span>\n</div>`;
    });
    tooltip.innerHTML = content;
    tooltip.style.display = "block";
    tooltip.style.position = "absolute";
    tooltip.style.backgroundColor = "rgba(255, 255, 255, 0.96)";
    tooltip.style.border = "1px solid rgba(200, 200, 200, 0.4)";
    tooltip.style.borderRadius = "6px";
    tooltip.style.padding = "12px 14px";
    tooltip.style.fontSize = "12px";
    tooltip.style.fontFamily = "Georgia, serif";
    tooltip.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
    tooltip.style.backdropFilter = "blur(12px)";
    tooltip.style.zIndex = "1000";
    tooltip.style.pointerEvents = "none";
    tooltip.style.maxWidth = "160px";
    tooltip.style.minWidth = "120px";
    const rect = event.target.getBoundingClientRect();
    let left = event.clientX + 15;
    let top = event.clientY - tooltip.offsetHeight - 15;
    if (left + tooltip.offsetWidth > window.innerWidth) left = event.clientX - tooltip.offsetWidth - 15;
    if (top < 0) top = event.clientY + 15;
    tooltip.style.left = left + "px";
    tooltip.style.top = top + "px";
  }
  function showMobileLegendTooltip(x, y, year, data) {
    let tooltip = document.getElementById("mobile-tooltip");
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.id = "mobile-tooltip";
      tooltip.style.position = "fixed";
      tooltip.style.pointerEvents = "none";
      tooltip.style.zIndex = "1000";
      document.body.appendChild(tooltip);
    }
    let content = `<div style="font-weight: bold; font-size: 14px; color: #666; margin-bottom: 8px;">${year}</div>`;
    data.forEach(item => {
      content += `\n<div style="display: flex; align-items: center; margin-bottom: 5px; font-size: 13px;">\n  <div style="width: 10px; height: 10px; background-color: ${item.color}; margin-right: 8px; border-radius: 2px;"></div>\n  <span style="color: #444; margin-right: 10px; min-width: 60px;">${item.label}</span>\n  <span style="color: #666; font-weight: 500;">${item.value}</span>\n</div>`;
    });
    tooltip.innerHTML = content;
    Object.assign(tooltip.style, {
      display: "block",
      backgroundColor: "rgba(255, 255, 255, 0.96)",
      border: "1px solid rgba(200, 200, 200, 0.4)",
      borderRadius: "8px",
      padding: "14px 16px",
      fontSize: "13px",
      fontFamily: "Georgia, serif",
      boxShadow: "0 6px 16px rgba(0,0,0,0.2)",
      backdropFilter: "blur(12px)",
      maxWidth: "180px",
      minWidth: "140px",
    });
    tooltip.style.left = (x - tooltip.offsetWidth / 2) + "px";
    tooltip.style.top = (y - tooltip.offsetHeight - 20) + "px";
  }
  function showTooltip(event, text) {
    const tooltip = document.getElementById("tooltip");
    if (!tooltip) return;
    tooltip.innerHTML = text;
    tooltip.style.display = "block";
    tooltip.style.position = "fixed";
    tooltip.style.left = event.clientX + 10 + "px";
    tooltip.style.top = event.clientY - 10 + "px";
    tooltip.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    tooltip.style.color = "white";
    tooltip.style.padding = "8px 12px";
    tooltip.style.borderRadius = "4px";
    tooltip.style.fontSize = "12px";
    tooltip.style.zIndex = "1000";
    tooltip.style.maxWidth = "200px";
  }
  function hideTooltip() {
    const tooltip = document.getElementById("tooltip");
    if (tooltip) tooltip.style.display = "none";
    const mobileTooltip = document.getElementById("mobile-tooltip");
    if (mobileTooltip) mobileTooltip.style.display = "none";
  }

  // ============================ PLOTLY: EVOLUCIÓN TOTAL ============================
  function createTitulacionPlotlyChart() {
    const container = document.getElementById("titulacionPlot");
    if (!container) return;
    const x = dataTitulaciones.map(d => d.año);
    const y = dataTitulaciones.map(d => d.total);
    const text = y.map(v => v.toLocaleString("en-US"));
    const textposition = x.map(year => ([2008, 2010, 2012, 2020].includes(year) ? "bottom center" : "top center"));
    const trace = {
      type: "scatter",
      mode: "lines+markers+text",
      x, y,
      line: { color: "#d62728", width: 3 },
      marker: { size: 7, color: "#d62728" },
      text, textposition,
      textfont: { family: "Georgia, serif", size: 10, color: "#1e293b" },
      name: "Titulaciones",
      hoverinfo: "skip"
    };
    const years = Array.from({ length: (2024 - 2007 + 1) }, (_, i) => 2007 + i);
    const layout = {
      title: {
        text: "<b>Evolución de Titulaciones en Los Ríos (2007-2024)</b><br><sub>Número total de profesionales titulados por año</sub>",
        x: 0,
        font: { size: 20, family: "Georgia, serif", color: "#1e293b" }
      },
      autosize: true,
      xaxis: {
        showgrid: false,
        tickfont: { family: "Georgia, serif", size: 12 },
        linecolor: "#d1d5db",
        tickcolor: "#d1d5db",
        range: [2006.5, 2024.5],
        tickmode: "array",
        tickvals: years,
        ticktext: years.map(y => String(y))
      },
      yaxis: {
        showgrid: true,
        gridcolor: "#f3f4f6",
        gridwidth: 1,
        tickfont: { family: "Georgia, serif", size: 12 },
        linecolor: "#d1d5db",
        tickcolor: "#d1d5db",
        tickformat: ",",
        range: [0, 6000]
      },
      plot_bgcolor: "white",
      paper_bgcolor: "white",
      font: { family: "Georgia, serif", color: "#1e293b" },
      showlegend: false,
      margin: { l: 80, r: 80, t: 100, b: 60 }
    };
    container.style.position = "relative";
    Plotly.newPlot(container, [trace], layout, { displayModeBar: false, responsive: true }).then(() => {
      Plotly.Plots.resize(container);
      // Hover/unhover
      container.on("plotly_hover", (data) => {
        if (!data || !data.points || !data.points.length) return;
        const p = data.points[0];
        const year = Math.round(p.x);
        const value = p.y;
        const lineShape = [{ type: "line", x0: year, x1: year, y0: 0, y1: 1, xref: "x", yref: "paper", line: { color: "rgba(100,100,100,0.15)", width: 1 } }];
        Plotly.relayout(container, { shapes: lineShape });
        if (data.event) {
          showMinimalistTooltip(data.event, year, [{ label: "Titulaciones", value: Number(value).toLocaleString(), color: "#d62728" }]);
        }
        container.style.cursor = "crosshair";
      });
      container.on("plotly_unhover", () => {
        Plotly.relayout(container, { shapes: [] });
        hideTooltip();
        container.style.cursor = "default";
      });
      // Overlay para guía en todo el área
      let overlay = document.getElementById("titulacionPlotOverlay");
      if (!overlay) {
        overlay = document.createElement("div");
        overlay.id = "titulacionPlotOverlay";
        Object.assign(overlay.style, { position: "absolute", inset: "0", background: "transparent", zIndex: "5" });
        container.appendChild(overlay);
      }
      const margins = { l: 80, r: 80, t: 100, b: 60 };
      const xmin = 2006.5, xmax = 2024.5;
      const minYear = 2007, maxYear = 2024;
      function handleMove(e) {
        const rect = overlay.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const plotLeft = margins.l;
        const plotRight = rect.width - margins.r;
        const plotTop = margins.t;
        const plotBottom = rect.height - margins.b;
        if (x < plotLeft || x > plotRight || y < plotTop || y > plotBottom) {
          Plotly.relayout(container, { shapes: [] });
          hideTooltip();
          container.style.cursor = "default";
          return;
        }
        const ratio = (x - plotLeft) / (plotRight - plotLeft);
        const xval = xmin + ratio * (xmax - xmin);
        const year = Math.max(minYear, Math.min(maxYear, Math.round(xval)));
        const dp = dataTitulaciones.find(d => d.año === year);
        const value = dp ? dp.total : null;
        const lineShape = [{ type: "line", x0: year, x1: year, y0: 0, y1: 1, xref: "x", yref: "paper", line: { color: "rgba(100,100,100,0.15)", width: 1 } }];
        Plotly.relayout(container, { shapes: lineShape });
        showMinimalistTooltip(e, year, [{ label: "Titulaciones", value: value != null ? Number(value).toLocaleString() : "—", color: "#d62728" }]);
        container.style.cursor = "crosshair";
      }
      function handleLeave() {
        Plotly.relayout(container, { shapes: [] });
        hideTooltip();
        container.style.cursor = "default";
      }
      overlay.addEventListener("mousemove", handleMove);
      overlay.addEventListener("mouseleave", handleLeave);
    });
  }

  // ============================ CANVAS: POR TIPO ============================
  function createTipoChart() {
    const canvas = document.getElementById("tipoChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const container = canvas.parentElement;
    const dpr = window.devicePixelRatio || 1;
    const displayWidth = container.offsetWidth;
    const displayHeight = container.offsetHeight;
    canvas.width = displayWidth * dpr;
    canvas.height = displayHeight * dpr;
    canvas.style.width = displayWidth + "px";
    canvas.style.height = displayHeight + "px";
    ctx.scale(dpr, dpr);
    const padding = getResponsivePadding(120, 40, 100, 100);
    const chartWidth = displayWidth - padding.left - padding.right;
    const chartHeight = displayHeight - padding.top - padding.bottom;
    const minYear = 2007, maxYear = 2024, yearRange = maxYear - minYear;
    const maxValue = 5200;
    function yearToX(year) { const offset = 15; return padding.left + offset + ((year - minYear) / yearRange) * (chartWidth - offset); }
    function valueToY(value) { return padding.top + (1 - value / maxValue) * chartHeight; }
    ctx.clearRect(0, 0, displayWidth, displayHeight);
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high"; ctx.lineJoin = "round"; ctx.lineCap = "round";
    ctx.strokeStyle = "#f3f4f6"; ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) { const y = valueToY(i * 1000); ctx.beginPath(); ctx.moveTo(padding.left, y); ctx.lineTo(displayWidth - padding.right - 1, y); ctx.stroke(); }
    ctx.strokeStyle = "#d1d5db"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(padding.left, padding.top + chartHeight); ctx.lineTo(displayWidth - padding.right - 1, padding.top + chartHeight); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(padding.left, padding.top); ctx.lineTo(padding.left, padding.top + chartHeight); ctx.stroke();
    ctx.fillStyle = "#1e293b"; ctx.font = "12px Georgia, serif"; ctx.textAlign = "center";
    if (isMobileDevice()) {
      [2007, 2010, 2013, 2016, 2019, 2022, 2024].forEach(year => { if (year >= minYear && year <= maxYear) { const x = yearToX(year); ctx.fillText(year, x, padding.top + chartHeight + 20); ctx.strokeStyle = "#d1d5db"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x, padding.top + chartHeight); ctx.lineTo(x, padding.top + chartHeight + 5); ctx.stroke(); } });
    } else {
      for (let year = minYear; year <= maxYear; year++) { const x = yearToX(year); ctx.fillText(year, x, padding.top + chartHeight + 20); ctx.strokeStyle = "#d1d5db"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x, padding.top + chartHeight); ctx.lineTo(x, padding.top + chartHeight + 5); ctx.stroke(); }
    }
    ctx.textAlign = "right";
    for (let i = 0; i <= 5; i++) { const value = i * 1000; const y = valueToY(value); ctx.fillText(value.toLocaleString(), padding.left - 15, y + 5); }
    ["Pregrado", "Posgrado", "Postítulo"].forEach((tipo) => {
      if (!tipoVisibility[tipo]) return;
      const color = coloresTipo[tipo];
      ctx.strokeStyle = color; ctx.lineWidth = 3; ctx.beginPath();
      dataTipo.forEach((point, index) => { const x = yearToX(point.año); const y = valueToY(point[tipo]); if (index === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); });
      ctx.stroke();
      dataTipo.forEach((point) => { const x = yearToX(point.año); const y = valueToY(point[tipo]); ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, 5, 0, 2 * Math.PI); ctx.fill(); ctx.strokeStyle = color; ctx.lineWidth = 1; ctx.stroke(); if (!isMobileDevice()) { ctx.fillStyle = color; ctx.font = "9px Georgia, serif"; ctx.textAlign = "center"; const textY = (tipo === "Pregrado" && point.año === 2020) ? y + 20 : y - 10; ctx.shadowColor = "rgba(255,255,255,0.8)"; ctx.shadowBlur = 2; ctx.fillText(point[tipo].toLocaleString(), x, textY); ctx.shadowBlur = 0; } });
    });
    ctx.fillStyle = "#1e293b"; ctx.font = "bold 20px Georgia, serif"; ctx.textAlign = "left"; ctx.fillText("Evolución de Titulaciones por Tipo en Los Ríos (2007-2024)", padding.left, 30);
    const legendY = 70; const legendSpacing = 120; let legendX = padding.left;
    ["Pregrado", "Posgrado", "Postítulo"].forEach((tipo) => {
      const color = coloresTipo[tipo]; const isVisible = tipoVisibility[tipo];
      if (isVisible) { ctx.fillStyle = color; ctx.beginPath(); ctx.arc(legendX, legendY, 6, 0, 2 * Math.PI); ctx.fill(); }
      else { ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(legendX, legendY, 6, 0, 2 * Math.PI); ctx.stroke(); }
      ctx.fillStyle = isVisible ? "#1e293b" : "#999"; ctx.font = "13px Georgia, serif"; ctx.textAlign = "left"; ctx.fillText(tipo, legendX + 15, legendY + 5);
      if (!window.legendPositions) window.legendPositions = {};
      window.legendPositions[tipo] = { x: legendX - 10, y: legendY - 10, width: ctx.measureText(tipo).width + 35, height: 20 };
      legendX += legendSpacing;
    });
    const covidYear = 2020; const covidX = yearToX(covidYear);
    ctx.strokeStyle = "#999999"; ctx.lineWidth = 1.5; ctx.setLineDash([8, 6]); ctx.beginPath(); ctx.moveTo(covidX, padding.top + 20); ctx.lineTo(covidX, padding.top + chartHeight - 20); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = "rgba(255,255,255,0.9)"; const textWidth = ctx.measureText("Inicio de COVID-19").width; const labelX = covidX + 8; const labelY = padding.top + 40; ctx.fillRect(labelX - 4, labelY - 14, textWidth + 8, 18);
    ctx.fillStyle = "#666666"; ctx.font = "11px Georgia, serif"; ctx.textAlign = "left"; ctx.fillText("Inicio de COVID-19", labelX, labelY);
  }

  function setupTipoChartInteractivity() {
    const canvas = document.getElementById("tipoChart");
    if (!canvas) return;
    canvas.addEventListener("click", handleTipoClick);
    canvas.addEventListener("touchend", handleTipoTouchEndClick, { passive: false });
    if (isMobileDevice()) {
      canvas.addEventListener("touchstart", handleTipoTouchStart, { passive: false });
      canvas.addEventListener("touchmove", handleTipoTouchMove, { passive: false });
      canvas.addEventListener("touchend", handleTipoTouchEnd, { passive: false });
    } else {
      canvas.addEventListener("mousemove", handleTipoMouseMove);
      canvas.addEventListener("mouseleave", handleTipoMouseLeave);
    }
    function handleTipoTouchStart(e) { e.preventDefault(); handleTipoTouch(e); }
    function handleTipoTouchMove(e) { e.preventDefault(); handleTipoTouch(e); }
    function handleTipoTouch(e) {
      const rect = canvas.getBoundingClientRect();
      const touch = e.touches[0];
      const touchX = touch.clientX - rect.left;
      const touchY = touch.clientY - rect.top;
      const padding = getResponsivePadding(120, 40, 100, 100);
      const chartWidth = rect.width - padding.left - padding.right;
      const chartHeight = rect.height - padding.top - padding.bottom;
      const yearRange = 2024 - 2007; const offset = 15; const tipos = ["Pregrado", "Posgrado", "Postítulo"];
      createTipoChart(); const ctx = canvas.getContext("2d");
      if (touchX >= padding.left + offset && touchX <= rect.width - padding.right && touchY >= padding.top && touchY <= padding.top + chartHeight) {
        drawElegantVerticalLine(canvas, ctx, touchX, padding, chartHeight);
        const year = getYearFromMousePosition(touchX, padding, chartWidth, 2007, 2024);
        if (year && year >= 2007 && year <= 2024) {
          const dataPoint = dataTipo.find(d => d.año === year);
          if (dataPoint) {
            const tooltipData = [];
            const tipoColors = { Pregrado: "#3b82f6", Posgrado: "#ef4444", Postítulo: "#10b981" };
            Object.keys(tipoVisibility).forEach(tipo => { if (tipoVisibility[tipo] && dataPoint[tipo]) { tooltipData.push({ label: tipo, value: dataPoint[tipo].toLocaleString(), color: tipoColors[tipo] }); } });
            if (tooltipData.length > 0) { showMobileLegendTooltip(touch.clientX, touch.clientY, year, tooltipData); }
          }
        }
      }
      let nearPoint = null; let nearTipo = null; let minDistance = Infinity;
      function yearToX(year) { return padding.left + offset + ((year - 2007) / yearRange) * (chartWidth - offset); }
      function valueToY(value) { const maxValue = 5200; return padding.top + (1 - value / maxValue) * chartHeight; }
      tipos.forEach((tipo) => { if (!tipoVisibility[tipo]) return; dataTipo.forEach((point) => { const x = yearToX(point.año); const y = valueToY(point[tipo]); const distance = Math.hypot(touchX - x, touchY - y); if (distance <= 25 && distance < minDistance) { minDistance = distance; nearPoint = point; nearTipo = tipo; } }); });
      if (!(nearPoint && nearTipo)) { /* mantener tooltip leyenda */ } else { /* noop */ }
    }
    function handleTipoTouchEnd(e) { e.preventDefault(); setTimeout(() => { hideTooltip(); createTipoChart(); }, 3000); }
    function handleTipoMouseMove(e) {
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left; const mouseY = e.clientY - rect.top;
      const padding = getResponsivePadding(120, 40, 100, 100);
      const chartWidth = rect.width - padding.left - padding.right; const chartHeight = rect.height - padding.top - padding.bottom; const yearRange = 2024 - 2007; const offset = 15;
      createTipoChart(); const ctx = canvas.getContext("2d");
      if (mouseX >= padding.left + offset && mouseX <= rect.width - padding.right && mouseY >= padding.top && mouseY <= padding.top + chartHeight) {
        drawElegantVerticalLine(canvas, ctx, mouseX, padding, chartHeight);
        const year = getYearFromMousePosition(mouseX, padding, chartWidth, 2007, 2024);
        if (year && year >= 2007 && year <= 2024) {
          const dataPoint = dataTipo.find(d => d.año === year);
          if (dataPoint) {
            const tooltipData = [];
            const tipoColors = { Pregrado: "#3b82f6", Posgrado: "#ef4444", Postítulo: "#10b981" };
            Object.keys(tipoVisibility).forEach(tipo => { if (tipoVisibility[tipo] && dataPoint[tipo]) { tooltipData.push({ label: tipo, value: dataPoint[tipo].toLocaleString(), color: tipoColors[tipo] }); } });
            if (tooltipData.length > 0) showMinimalistTooltip(e, year, tooltipData);
          }
        }
      } else { hideTooltip(); }
      function yearToX(year) { return padding.left + offset + ((year - 2007) / yearRange) * (chartWidth - offset); }
      function valueToY(value) { const maxValue = 5200; return padding.top + (1 - value / maxValue) * chartHeight; }
      const tipos = ["Pregrado", "Posgrado", "Postítulo"]; let foundPointHover = false;
      tipos.forEach((tipo) => { if (!tipoVisibility[tipo]) return; dataTipo.forEach((point) => { const x = yearToX(point.año); const y = valueToY(point[tipo]); const distance = Math.hypot(mouseX - x, mouseY - y); if (distance <= 15) { foundPointHover = true; } }); });
      if (window.legendPositions) {
        tipos.forEach((tipo) => {
          const pos = window.legendPositions[tipo];
          if (mouseX >= pos.x && mouseX <= pos.x + pos.width && mouseY >= pos.y && mouseY <= pos.y + pos.height) {
            foundPointHover = true; showTooltip(e, `Click para ${tipoVisibility[tipo] ? "ocultar" : "mostrar"} ${tipo}`);
          }
        });
      }
      canvas.style.cursor = (mouseX >= padding.left + offset && mouseX <= rect.width - padding.right && mouseY >= padding.top && mouseY <= padding.top + chartHeight) ? (foundPointHover ? "pointer" : "crosshair") : "default";
    }
    function handleTipoMouseLeave() { hideTooltip(); const c = document.getElementById("tipoChart"); if (c) c.style.cursor = "default"; createTipoChart(); }
    function handleTipoTouchEndClick(event) {
      if (event.touches && event.touches.length > 0) return;
      const rect = canvas.getBoundingClientRect();
      const touch = event.changedTouches[0]; const touchX = touch.clientX - rect.left; const touchY = touch.clientY - rect.top;
      if (window.legendPositions) {
        ["Pregrado", "Posgrado", "Postítulo"].forEach((tipo) => {
          const pos = window.legendPositions[tipo];
          if (touchX >= pos.x && touchX <= pos.x + pos.width && touchY >= pos.y && touchY <= pos.y + pos.height) {
            tipoVisibility[tipo] = !tipoVisibility[tipo]; createTipoChart(); hideTooltip();
          }
        });
      }
    }
    function handleTipoClick(e) {
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left; const mouseY = e.clientY - rect.top;
      if (window.legendPositions) {
        ["Pregrado", "Posgrado", "Postítulo"].forEach((tipo) => {
          const pos = window.legendPositions[tipo];
          if (mouseX >= pos.x && mouseX <= pos.x + pos.width && mouseY >= pos.y && mouseY <= pos.y + pos.height) {
            tipoVisibility[tipo] = !tipoVisibility[tipo]; createTipoChart(); hideTooltip();
          }
        });
      }
    }
  }

  // ============================ CANVAS: POR SEXO ============================
  function createSexoChart() {
    const canvas = document.getElementById("sexoChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const container = canvas.parentElement;
    const dpr = window.devicePixelRatio || 1;
    const displayWidth = container.offsetWidth; const displayHeight = container.offsetHeight;
    canvas.width = displayWidth * dpr; canvas.height = displayHeight * dpr; canvas.style.width = displayWidth + "px"; canvas.style.height = displayHeight + "px"; ctx.scale(dpr, dpr);
    const padding = getResponsivePadding(120, 40, 60, 100);
    const chartWidth = displayWidth - padding.left - padding.right; const chartHeight = displayHeight - padding.top - padding.bottom;
    const minYear = 2007, maxYear = 2024, yearRange = maxYear - minYear; const maxValue = 3200;
    function yearToX(year) { const offset = 15; return padding.left + offset + ((year - minYear) / yearRange) * (chartWidth - offset); }
    function valueToY(value) { return padding.top + (1 - value / maxValue) * chartHeight; }
    ctx.clearRect(0, 0, displayWidth, displayHeight);
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high"; ctx.lineJoin = "round"; ctx.lineCap = "round";
    ctx.strokeStyle = "#f3f4f6"; ctx.lineWidth = 1; for (let i = 0; i <= 3; i++) { const y = valueToY(i * 1000); ctx.beginPath(); ctx.moveTo(padding.left, y); ctx.lineTo(displayWidth - padding.right - 1, y); ctx.stroke(); }
    ctx.strokeStyle = "#d1d5db"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(padding.left, padding.top + chartHeight); ctx.lineTo(displayWidth - padding.right - 1, padding.top + chartHeight); ctx.stroke(); ctx.beginPath(); ctx.moveTo(padding.left, padding.top); ctx.lineTo(padding.left, padding.top + chartHeight); ctx.stroke();
    ctx.fillStyle = "#1e293b"; ctx.font = "12px Georgia, serif"; ctx.textAlign = "center";
    if (isMobileDevice()) { [2007, 2010, 2013, 2016, 2019, 2022, 2024].forEach(year => { if (year >= minYear && year <= maxYear) { const x = yearToX(year); ctx.fillText(year, x, padding.top + chartHeight + 20); ctx.strokeStyle = "#d1d5db"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x, padding.top + chartHeight); ctx.lineTo(x, padding.top + chartHeight + 5); ctx.stroke(); } }); } else { for (let year = minYear; year <= maxYear; year++) { const x = yearToX(year); ctx.fillText(year, x, padding.top + chartHeight + 20); ctx.strokeStyle = "#d1d5db"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x, padding.top + chartHeight); ctx.lineTo(x, padding.top + chartHeight + 5); ctx.stroke(); } }
    ctx.textAlign = "right"; for (let i = 0; i <= 3; i++) { const value = i * 1000; const y = valueToY(value); ctx.fillText(value.toLocaleString(), padding.left - 15, y + 5); }
    const sexos = ["Hombre", "Mujer"]; const hombreAbajo = [2007, 2010, 2012, 2016, 2020];
    sexos.forEach((sexo) => { if (!sexoVisibility[sexo]) return; const color = coloresSexo[sexo]; ctx.strokeStyle = color; ctx.lineWidth = 3; ctx.beginPath(); dataSexo.forEach((point, index) => { const x = yearToX(point.año); const y = valueToY(point[sexo]); if (index === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }); ctx.stroke(); dataSexo.forEach((point) => { const x = yearToX(point.año); const y = valueToY(point[sexo]); ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, 3, 0, 2 * Math.PI); ctx.fill(); ctx.strokeStyle = color; ctx.lineWidth = 1; ctx.stroke(); if (!isMobileDevice()) { ctx.fillStyle = color; ctx.font = "9px Georgia, serif"; ctx.textAlign = "center"; let textY; if (sexo === "Hombre" && hombreAbajo.includes(point.año)) textY = y + 20; else if (sexo === "Mujer" && point.año === 2020) textY = y + 20; else textY = y - 10; ctx.shadowColor = "rgba(255,255,255,0.8)"; ctx.shadowBlur = 2; ctx.fillText(point[sexo].toLocaleString(), x, textY); ctx.shadowBlur = 0; } }); });
    ctx.fillStyle = "#1e293b"; ctx.font = "bold 20px Georgia, serif"; ctx.textAlign = "left"; ctx.fillText("Evolución de Titulaciones por Sexo en Los Ríos (2007-2024)", padding.left, 30);
    const legendY = 70; const legendSpacing = 120; let legendX = padding.left;
    sexos.forEach((sexo) => { const color = coloresSexo[sexo]; const isVisible = sexoVisibility[sexo]; if (isVisible) { ctx.fillStyle = color; ctx.beginPath(); ctx.arc(legendX, legendY, 6, 0, 2 * Math.PI); ctx.fill(); } else { ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(legendX, legendY, 6, 0, 2 * Math.PI); ctx.stroke(); } ctx.fillStyle = isVisible ? "#1e293b" : "#999"; ctx.font = "12px Georgia, serif"; ctx.textAlign = "left"; ctx.fillText(sexo, legendX + 15, legendY + 5); if (!window.sexoLegendPositions) window.sexoLegendPositions = {}; window.sexoLegendPositions[sexo] = { x: legendX - 10, y: legendY - 10, width: ctx.measureText(sexo).width + 35, height: 20 }; legendX += legendSpacing; });
    const covidYear = 2020; const covidX = yearToX(covidYear); ctx.strokeStyle = "#999999"; ctx.lineWidth = 1.5; ctx.setLineDash([8, 6]); ctx.beginPath(); ctx.moveTo(covidX, padding.top + 20); ctx.lineTo(covidX, padding.top + chartHeight - 20); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = "rgba(255,255,255,0.9)"; const textWidth = ctx.measureText("Inicio de COVID-19").width; const labelX = covidX + 8; const labelY = padding.top + 40; ctx.fillRect(labelX - 4, labelY - 14, textWidth + 8, 18); ctx.fillStyle = "#666666"; ctx.font = "11px Georgia, serif"; ctx.textAlign = "left"; ctx.fillText("Inicio de COVID-19", labelX, labelY);
  }

  function setupSexoChartInteractivity() {
    const canvas = document.getElementById("sexoChart");
    if (!canvas) return;
    canvas.addEventListener("click", handleSexoClick);
    canvas.addEventListener("touchend", handleSexoTouchEndClick, { passive: false });
    if (isMobileDevice()) { canvas.addEventListener("touchstart", handleSexoTouchStart, { passive: false }); canvas.addEventListener("touchmove", handleSexoTouchMove, { passive: false }); canvas.addEventListener("touchend", handleSexoTouchEnd, { passive: false }); } else { canvas.addEventListener("mousemove", handleSexoMouseMove); canvas.addEventListener("mouseleave", handleSexoMouseLeave); }
    function handleSexoTouchStart(e) { e.preventDefault(); handleSexoTouch(e); }
    function handleSexoTouchMove(e) { e.preventDefault(); handleSexoTouch(e); }
    function handleSexoTouch(e) {
      const rect = canvas.getBoundingClientRect(); const touch = e.touches[0]; const touchX = touch.clientX - rect.left; const touchY = touch.clientY - rect.top;
      const padding = getResponsivePadding(120, 40, 60, 100); const chartWidth = rect.width - padding.left - padding.right; const chartHeight = rect.height - padding.top - padding.bottom; const yearRange = 2024 - 2007; const offset = 15; const sexos = ["Hombre", "Mujer"];
      createSexoChart(); const ctx = canvas.getContext("2d");
      if (touchX >= padding.left + offset && touchX <= rect.width - padding.right && touchY >= padding.top && touchY <= padding.top + chartHeight) {
        drawElegantVerticalLine(canvas, ctx, touchX, padding, chartHeight);
        const year = getYearFromMousePosition(touchX, padding, chartWidth, 2007, 2024);
        if (year && year >= 2007 && year <= 2024) {
          const dataPoint = dataSexo.find(d => d.año === year);
          if (dataPoint) {
            const tooltipData = []; const sexoColors = { Hombre: "#3b82f6", Mujer: "#ef4444" };
            Object.keys(sexoVisibility).forEach(sexo => { if (sexoVisibility[sexo] && dataPoint[sexo]) { tooltipData.push({ label: sexo, value: dataPoint[sexo].toLocaleString(), color: sexoColors[sexo] }); } });
            if (tooltipData.length > 0) showMobileLegendTooltip(touch.clientX, touch.clientY, year, tooltipData);
          }
        }
      }
      let nearPoint = null; let nearSexo = null; let minDistance = Infinity;
      function yearToX(year) { return padding.left + offset + ((year - 2007) / yearRange) * (chartWidth - offset); }
      function valueToY(value) { const maxValue = 3200; return padding.top + (1 - value / maxValue) * chartHeight; }
      sexos.forEach((sexo) => { if (!sexoVisibility[sexo]) return; dataSexo.forEach((point) => { const x = yearToX(point.año); const y = valueToY(point[sexo]); const distance = Math.hypot(touchX - x, touchY - y); if (distance <= 25 && distance < minDistance) { minDistance = distance; nearPoint = point; nearSexo = sexo; } }); });
      if (!(nearPoint && nearSexo)) { /* mantener tooltip leyenda */ }
    }
    function handleSexoTouchEnd(e) { e.preventDefault(); setTimeout(() => { hideTooltip(); createSexoChart(); }, 3000); }
    function handleSexoMouseMove(event) {
      const canvasRect = canvas.getBoundingClientRect(); const mouseX = event.clientX - canvasRect.left; const mouseY = event.clientY - canvasRect.top;
      const padding = getResponsivePadding(120, 40, 60, 100); const chartWidth = canvasRect.width - padding.left - padding.right; const chartHeight = canvasRect.height - padding.top - padding.bottom; const yearRange = 2024 - 2007; const offset = 15;
      createSexoChart(); const ctx = canvas.getContext("2d");
      if (mouseX >= padding.left + offset && mouseX <= canvasRect.width - padding.right && mouseY >= padding.top && mouseY <= padding.top + chartHeight) {
        drawElegantVerticalLine(canvas, ctx, mouseX, padding, chartHeight);
        const year = getYearFromMousePosition(mouseX, padding, chartWidth, 2007, 2024);
        if (year && year >= 2007 && year <= 2024) {
          const dataPoint = dataSexo.find(d => d.año === year);
          if (dataPoint) {
            const tooltipData = []; const sexoColors = { Hombre: "#3b82f6", Mujer: "#ef4444" };
            Object.keys(sexoVisibility).forEach(sexo => { if (sexoVisibility[sexo] && dataPoint[sexo]) { tooltipData.push({ label: sexo, value: dataPoint[sexo].toLocaleString(), color: sexoColors[sexo] }); } });
            if (tooltipData.length > 0) showMinimalistTooltip(event, year, tooltipData);
          }
        }
      } else { hideTooltip(); }
      function yearToX(year) { return padding.left + offset + ((year - 2007) / yearRange) * (chartWidth - offset); }
      function valueToY(value) { const maxValue = 3200; return padding.top + (1 - value / maxValue) * chartHeight; }
      const sexos = ["Hombre", "Mujer"]; let foundHover = false;
      sexos.forEach((sexo) => { if (!sexoVisibility[sexo]) return; dataSexo.forEach((point) => { const x = yearToX(point.año); const y = valueToY(point[sexo]); const distance = Math.hypot(mouseX - x, mouseY - y); if (distance <= 15) { foundHover = true; canvas.style.cursor = "pointer"; } }); });
      if (window.sexoLegendPositions) {
        sexos.forEach((sexo) => {
          const pos = window.sexoLegendPositions[sexo];
          if (mouseX >= pos.x && mouseX <= pos.x + pos.width && mouseY >= pos.y && mouseY <= pos.y + pos.height) {
            foundHover = true; showTooltip(event, `Click para ${sexoVisibility[sexo] ? "ocultar" : "mostrar"} ${sexo}`);
          }
        });
      }
      if (mouseX >= padding.left + offset && mouseX <= canvasRect.width - padding.right && mouseY >= padding.top && mouseY <= padding.top + chartHeight) {
        canvas.style.cursor = foundHover ? "pointer" : "crosshair";
      } else { canvas.style.cursor = "default"; }
    }
    function handleSexoMouseLeave() { hideTooltip(); canvas.style.cursor = "default"; createSexoChart(); }
    function handleSexoTouchEndClick(event) {
      if (event.touches && event.touches.length > 0) return;
      const rect = canvas.getBoundingClientRect(); const touch = event.changedTouches[0]; const touchX = touch.clientX - rect.left; const touchY = touch.clientY - rect.top;
      if (window.sexoLegendPositions) {
        ["Hombre", "Mujer"].forEach((sexo) => { const pos = window.sexoLegendPositions[sexo]; if (touchX >= pos.x && touchX <= pos.x + pos.width && touchY >= pos.y && touchY <= pos.y + pos.height) { sexoVisibility[sexo] = !sexoVisibility[sexo]; createSexoChart(); hideTooltip(); } });
      }
    }
    function handleSexoClick(event) {
      const rect = canvas.getBoundingClientRect(); const mouseX = event.clientX - rect.left; const mouseY = event.clientY - rect.top;
      if (window.sexoLegendPositions) { ["Hombre", "Mujer"].forEach((sexo) => { const pos = window.sexoLegendPositions[sexo]; if (mouseX >= pos.x && mouseX <= pos.x + pos.width && mouseY >= pos.y && mouseY <= pos.y + pos.height) { sexoVisibility[sexo] = !sexoVisibility[sexo]; createSexoChart(); hideTooltip(); } }); }
    }
  }

  // ============================ NAVEGACIÓN & RESPONSIVE ============================
  function setupNavigation() {
    const navLinks = document.querySelectorAll(".nav-link");
    const sections = document.querySelectorAll(".section");
    navLinks.forEach(link => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        navLinks.forEach(l => l.classList.remove("active"));
        sections.forEach(s => s.classList.remove("active"));
        link.classList.add("active");
        const sectionId = link.getAttribute("data-section");
        const section = document.getElementById(sectionId);
        if (section) section.classList.add("active");
        setTimeout(() => {
          if (sectionId === "seccion1") createTitulacionPlotlyChart();
          else if (sectionId === "seccion2") { createTipoChart(); setupTipoChartInteractivity(); }
          else if (sectionId === "seccion3") { createSexoChart(); setupSexoChartInteractivity(); }
        }, 150);
      });
    });
  }

  function handleResize() {
    clearTimeout(window.resizeTimeout);
    window.resizeTimeout = setTimeout(() => {
      const activeSection = document.querySelector(".section.active");
      if (!activeSection) return;
      const sectionId = activeSection.id;
      if (sectionId === "seccion1") {
        const plot = document.getElementById("titulacionPlot");
        if (plot) {
          if (plot.data && plot.data.length) Plotly.Plots.resize(plot);
          else createTitulacionPlotlyChart();
        }
      } else if (sectionId === "seccion2") {
        const tipoCanvas = document.getElementById("tipoChart");
        if (tipoCanvas) { createTipoChart(); setupTipoChartInteractivity(); }
      } else if (sectionId === "seccion3") {
        const sexoCanvas = document.getElementById("sexoChart");
        if (sexoCanvas) { createSexoChart(); setupSexoChartInteractivity(); }
      }
    }, 100);
  }

  // ============================ INIT ============================
  document.addEventListener("DOMContentLoaded", () => {
    setupNavigation();
    // Activar sección 1 al iniciar
    const firstSection = document.getElementById("seccion1");
    const firstNavLink = document.querySelector('.nav-link[data-section="seccion1"]');
    if (firstSection && firstNavLink) {
      firstSection.classList.add("active");
      firstNavLink.classList.add("active");
    }
    setTimeout(() => {
      createTitulacionPlotlyChart();
      createTipoChart();
      setupTipoChartInteractivity();
      createSexoChart();
      setupSexoChartInteractivity();
    }, 100);
    window.addEventListener("resize", handleResize);
  });
})();
