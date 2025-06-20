/* ----------- PARÁMETROS ----------- */
const UPDATE_INTERVAL = 2000;     // ms entre refrescos del gráfico
const MAX_TITLES      = 10;       // cuántos títulos mostrar
let activeChart = null; // ← No hay gráfico activo al inicio


/* ----------- VARIABLES GLOBALES ----------- */
let titleFrequency = {};
let pendingUpdate  = false;

/* ----------- SETUP SVG ----------- */
let svg, g, x, y;
const width = 800, height = 400;

function setChart(type) {
    const desc = document.getElementById("chart-description");
    const stream = document.getElementById("stream-container");
    activeChart = type;

    // Mostrar descripción
    if (type === "titles") {
        desc.innerText = "Shows the most frequently edited article titles in real-time.";
    } else if (type === "bytes") {
        desc.innerText = "Displays the distribution of byte changes per edit (e.g. minor or major changes).";
    } else if (type === "wikis") {
        desc.innerText = "Represents the volume of edits per wiki (e.g. enwiki, eswiki, wikidata).";
    }

    // Mostrar/ocultar stream de texto solo para "wikis"
    if (type === "wikis") {
        stream.style.display = "block";
    } else {
        stream.style.display = "none";
    }

    // Dibujar gráfico activo (si hay datos)
    if (type === "titles") drawTitlesChart();
    // else if (type === "bytes") drawBytesChart();
    // else if (type === "wikis") drawWikiChart();
}



/* ----------- FUNCIÓN DE DIBUJO ----------- */
function drawTitlesChart() {
    setupChartArea();

    const data = Object.entries(titleFrequency)
        .map(([title, count]) => ({ title, count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, MAX_TITLES);

    x.domain([0, d3.max(data, d => d.count) || 1]);
    y.domain(data.map(d => d.title));

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


/* ----------- LOG TEXTO ----------- */
function logEvent(change) {
    const log   = document.getElementById("log");
    const bytes = (change.length.new || 0) - (change.length.old || 0);
    const entry = `[${new Date(change.timestamp * 1000).toLocaleTimeString()}] `
                + `(${change.wiki}) "${change.title}" by ${change.user} (${bytes} bytes)`;
    const div   = document.createElement("div");
    div.textContent = entry;
    log.prepend(div);
}

/* ----------- STREAM  ----------- */
const eventSource = new EventSource('https://stream.wikimedia.org/v2/stream/recentchange');

eventSource.onmessage = (e) => {
    try {
        const change = JSON.parse(e.data);
        if (change.type === 'edit') {
            logEvent(change);

            // Solo procesar datos si ya hay gráfico activo
            if (activeChart === "titles") {
                titleFrequency[change.title] = (titleFrequency[change.title] || 0) + 1;
                pendingUpdate = true;
            }

            // Agregar aquí lógica condicional para bytes y wikis
        }
    } catch (err) { console.error('Parse error:', err); }
};


/* ----------- ACTUALIZADOR PERIÓDICO ----------- */
setInterval(() => {
    if (!activeChart || !pendingUpdate) return;

    if (activeChart === "titles") drawTitlesChart();
    // Agrega aquí: else if (...) drawBytesChart(), etc.

    pendingUpdate = false;
}, UPDATE_INTERVAL);

