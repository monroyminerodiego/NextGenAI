/* ---------- PARÁMETROS GENERALES ---------- */
const UPDATE_INTERVAL = 2000;      // ms entre refrescos
const MAX_TITLES      = 10;        // Top N titles
const MAX_POINTS      = 300;       // Últimos eventos para el histograma

/* ---------- ESTADO GLOBAL ---------- */
let activeChart   = null;          // gráfico actual
let pendingUpdate = false;         // marcar redibujo

/* contenedores de datos */
const titleFrequency = {};         // {title: count}
const byteChanges    = [];         // lista de difs de bytes

/* ---------- ÁREA DE DIBUJO ---------- */
let svg, g, x, y;
const width  = 800,
      height = 400;

function setupChartArea() {
  d3.select("#chart").selectAll("*").remove();

  svg = d3.select("#chart")
          .append("svg")
          .attr("width", width)
          .attr("height", height);

  g  = svg.append("g").attr("transform", "translate(40,20)");
}

/* ---------- CHART #1 – Top Edited Articles ---------- */
function drawTitlesChart() {
  setupChartArea();

  const data = Object.entries(titleFrequency)
                     .map(([title, count]) => ({ title, count }))
                     .sort((a, b) => b.count - a.count)
                     .slice(0, MAX_TITLES);

  x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.count) || 1])
        .range([0, width - 100]);

  y = d3.scaleBand()
        .domain(data.map(d => d.title))
        .range([0, height - 50])
        .padding(0.2);

  g.append("g").call(d3.axisLeft(y));

  g.selectAll("rect")
    .data(data)
    .enter().append("rect")
      .attr("y", d => y(d.title))
      .attr("width", d => x(d.count))
      .attr("height", y.bandwidth())
      .attr("fill", "#4a90e2");

  g.selectAll("text.label")
    .data(data)
    .enter().append("text")
      .attr("class", "label")
      .attr("x", d => x(d.count) + 5)
      .attr("y", d => y(d.title) + y.bandwidth() / 2 + 5)
      .text(d => d.count);
}

/* ---------- CHART #2 – Byte Change Histogram ---------- */
function drawBytesChart() {
  setupChartArea();

  const values = byteChanges.slice(-MAX_POINTS);

  const binGen = d3.bin().thresholds(20);
  const bins   = binGen(values);

  x = d3.scaleLinear()
        .domain([d3.min(values) || 0, d3.max(values) || 1])
        .nice()
        .range([0, width - 60]);

  y = d3.scaleLinear()
        .domain([0, d3.max(bins, d => d.length) || 1])
        .nice()
        .range([height - 50, 0]);

  g.append("g")
   .attr("transform", `translate(0,${height - 50})`)
   .call(d3.axisBottom(x));

  g.append("g").call(d3.axisLeft(y));

  g.selectAll("rect")
    .data(bins)
    .enter().append("rect")
      .attr("x", d => x(d.x0))
      .attr("y", d => y(d.length))
      .attr("width", d => x(d.x1) - x(d.x0) - 1)
      .attr("height", d => y(0) - y(d.length))
      .attr("fill", "#ff7f0e");
}

/* ---------- DESCRIPCIÓN Y SELECCIÓN DE GRÁFICO ---------- */
function setChart(type) {
    const desc      = document.getElementById("chart-description");
    const streamBox = document.getElementById("stream-container");
    const chartBox  = document.getElementById("chart");
    activeChart     = type;

    if (type === "wikis") {
        desc.innerHTML = `
            <strong>Live stream of every edit (raw text log).</strong><br>
            This view shows a real-time feed of all edit events coming from Wikimedia projects. 
            Each line includes the wiki (e.g., enwiki), the article title, the user who made the edit, 
            and the size difference in bytes. It's ideal for monitoring activity as it happens.
        `;
        streamBox.style.display = "block";
        chartBox.style.display = "none";
    } else if (type === "titles") {
        desc.innerHTML = `
            <strong>Shows the most frequently edited article titles in real-time.</strong><br>
            This bar chart ranks the top 10 articles that are currently receiving the most edits. 
            It helps identify trending topics or heavily edited content in real time.
        `;
        streamBox.style.display = "none";
        chartBox.style.display = "block";
    } else if (type === "bytes") {
        desc.innerHTML = `
            <strong>Displays the distribution of byte changes per edit (minor vs. major).</strong><br>
            This histogram groups recent edits by how many bytes were added or removed. Where added bytes are positive values and removed bytes are negative values
            It reveals whether most edits are small tweaks or large structural changes.
        `;
        streamBox.style.display = "none";
        chartBox.style.display = "block";
    }

    pendingUpdate = true;
}


/* ---------- LOG DE TEXTO ---------- */
function logEvent(change, diff) {
  const log  = document.getElementById("log");
  const line = `[${new Date(change.timestamp * 1000).toLocaleTimeString()}] `
             + `(${change.wiki}) "${change.title}" by ${change.user} (${diff} bytes)`;
  const div  = document.createElement("div");
  div.textContent = line;
  log.prepend(div);
}

/* ---------- STREAM SSE ---------- */
const eventSource = new EventSource(
  "https://stream.wikimedia.org/v2/stream/recentchange"
);

eventSource.onmessage = (e) => {
  try {
    const change = JSON.parse(e.data);
    if (change.type !== "edit") return;

    const diff = (change.length.new || 0) - (change.length.old || 0);

    /* acumular para títulos y bytes */
    titleFrequency[change.title] = (titleFrequency[change.title] || 0) + 1;
    byteChanges.push(diff);
    if (byteChanges.length > MAX_POINTS * 4) byteChanges.shift();

    /* mostrar en log si estamos en modo “stream” */
    if (activeChart === "wikis") logEvent(change, diff);

    pendingUpdate = true;
  } catch (err) {
    console.error("Parse error:", err);
  }
};

/* ---------- REFRESCO PERIÓDICO ---------- */
setInterval(() => {
  if (!activeChart || !pendingUpdate) return;

  if (activeChart === "titles") drawTitlesChart();
  else if (activeChart === "bytes") drawBytesChart();
  /* “wikis” ya no dibuja nada: solo muestra log */

  pendingUpdate = false;
}, UPDATE_INTERVAL);
