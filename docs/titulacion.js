"use strict";

// Titulación Los Ríos – visualizaciones en Highcharts
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

  // Colores (mantener los que ya estaban antes)
  const colorTotal = "#d62728";
  const coloresTipo = { Pregrado: "#0072B2", Posgrado: "#D55E00", Postítulo: "#009E73" };
  const coloresSexo = { Hombre: "#0072B2", Mujer: "#D55E00" };

  // ============================ HIGHCHARTS: PLANTILLA ============================
  const chartInstances = {
    total: null,
    tipo: null,
    sexo: null
  };

  function ensureHighcharts() {
    if (typeof window.Highcharts === "undefined") {
      // eslint-disable-next-line no-console
      console.error("Highcharts no está cargado. Revisa los <script> en docs/index.html");
      return false;
    }
    return true;
  }

  function getExportMenuItems() {
    return [
      "viewFullscreen",
      "printChart",
      "separator",
      "downloadPNG",
      "downloadJPEG",
      "downloadSVG",
      "separator",
      "downloadCSV",
      "downloadXLS",
      "viewData"
    ];
  }

  function getCommonChartOptions({ title, subtitle, yAxisTitle }) {
    return {
      chart: {
        backgroundColor: "#ffffff",
        style: { fontFamily: "Georgia, serif" },
        spacingTop: 20,
        spacingLeft: 10,
        spacingRight: 10
      },
      title: {
        text: title,
        align: "left"
      },
      subtitle: {
        text: subtitle,
        align: "left",
        useHTML: true
      },
      xAxis: {
        tickInterval: 1,
        crosshair: { color: "rgba(100,100,100,0.15)", width: 1 },
        accessibility: { rangeDescription: "Range: 2007 to 2024" }
      },
      yAxis: {
        title: { text: yAxisTitle }
      },
      legend: {
        layout: "vertical",
        align: "right",
        verticalAlign: "middle"
      },
      plotOptions: {
        series: {
          label: { connectorAllowed: false },
          pointStart: 2007,
          marker: { enabled: true }
        }
      },
      tooltip: {
        shared: true
      },
      exporting: {
        enabled: true,
        buttons: {
          contextButton: {
            menuItems: getExportMenuItems()
          }
        }
      },
      credits: { enabled: false },
      responsive: {
        rules: [{
          condition: { maxWidth: 500 },
          chartOptions: {
            legend: {
              layout: "horizontal",
              align: "center",
              verticalAlign: "bottom"
            }
          }
        }]
      }
    };
  }

  function destroyChart(key) {
    const existing = chartInstances[key];
    if (existing && typeof existing.destroy === "function") {
      existing.destroy();
      chartInstances[key] = null;
    }
  }

  function addCovidPlotLine() {
    return {
      color: "#999999",
      width: 1.5,
      value: 2020,
      dashStyle: "Dash",
      label: {
        text: "Inicio de COVID-19",
        align: "left",
        style: { color: "#666666", fontSize: "11px" },
        rotation: 0,
        x: 8,
        y: 12
      },
      zIndex: 3
    };
  }

  // ============================ GRÁFICOS ============================
  function createTitulacionChart() {
    if (!ensureHighcharts()) return;
    const container = document.getElementById("titulacionPlot");
    if (!container) return;

    destroyChart("total");
    chartInstances.total = window.Highcharts.chart("titulacionPlot", {
      ...getCommonChartOptions({
        title: "U.S Solar Employment Growth",
        subtitle: 'By Job Category. Source: <a href="https://irecusa.org/programs/solar-jobs-census/" target="_blank">IREC</a>.',
        yAxisTitle: "Number of Employees"
      }),
      // Mantener los datos/colores del proyecto, solo se aplica la plantilla
      title: { text: "Evolución de Titulaciones en Los Ríos (2007-2024)", align: "left" },
      subtitle: { text: "Número total de profesionales titulados por año", align: "left" },
      yAxis: { title: { text: "Número de Titulados" } },
      xAxis: {
        ...getCommonChartOptions({ title: "", subtitle: "", yAxisTitle: "" }).xAxis,
        plotLines: [addCovidPlotLine()]
      },
      series: [{
        name: "Titulaciones",
        color: colorTotal,
        lineWidth: 3,
        marker: { radius: 4 },
        data: dataTitulaciones.map(d => d.total)
      }]
    });
  }

  function createTipoChart() {
    if (!ensureHighcharts()) return;
    const container = document.getElementById("tipoChart");
    if (!container) return;

    destroyChart("tipo");
    chartInstances.tipo = window.Highcharts.chart("tipoChart", {
      ...getCommonChartOptions({
        title: "Evolución de Titulaciones por Tipo en Los Ríos (2007-2024)",
        subtitle: "Pregrado, Posgrado y Postítulo",
        yAxisTitle: "Número de Titulados"
      }),
      xAxis: {
        ...getCommonChartOptions({ title: "", subtitle: "", yAxisTitle: "" }).xAxis,
        plotLines: [addCovidPlotLine()]
      },
      series: [
        {
          name: "Pregrado",
          color: coloresTipo.Pregrado,
          data: dataTipo.map(d => d.Pregrado)
        },
        {
          name: "Posgrado",
          color: coloresTipo.Posgrado,
          data: dataTipo.map(d => d.Posgrado)
        },
        {
          name: "Postítulo",
          color: coloresTipo.Postítulo,
          data: dataTipo.map(d => d["Postítulo"])
        }
      ]
    });
  }

  function createSexoChart() {
    if (!ensureHighcharts()) return;
    const container = document.getElementById("sexoChart");
    if (!container) return;

    destroyChart("sexo");
    chartInstances.sexo = window.Highcharts.chart("sexoChart", {
      ...getCommonChartOptions({
        title: "Evolución de Titulaciones por Sexo en Los Ríos (2007-2024)",
        subtitle: "Comparación entre Hombres y Mujeres",
        yAxisTitle: "Número de Titulados"
      }),
      xAxis: {
        ...getCommonChartOptions({ title: "", subtitle: "", yAxisTitle: "" }).xAxis,
        plotLines: [addCovidPlotLine()]
      },
      series: [
        {
          name: "Hombre",
          color: coloresSexo.Hombre,
          data: dataSexo.map(d => d.Hombre)
        },
        {
          name: "Mujer",
          color: coloresSexo.Mujer,
          data: dataSexo.map(d => d.Mujer)
        }
      ]
    });
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
          if (sectionId === "seccion1") createTitulacionChart();
          else if (sectionId === "seccion2") createTipoChart();
          else if (sectionId === "seccion3") createSexoChart();
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
        if (chartInstances.total) chartInstances.total.reflow();
        else createTitulacionChart();
      } else if (sectionId === "seccion2") {
        if (chartInstances.tipo) chartInstances.tipo.reflow();
        else createTipoChart();
      } else if (sectionId === "seccion3") {
        if (chartInstances.sexo) chartInstances.sexo.reflow();
        else createSexoChart();
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
      // Crear solo el gráfico visible; los otros se crean al cambiar de pestaña
      createTitulacionChart();
    }, 100);
    window.addEventListener("resize", handleResize);
  });
})();
