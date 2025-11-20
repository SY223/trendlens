const API_BASE = "http://127.0.0.1:8000";

const fetchBtn = document.getElementById("fetchBtn");
const queryInput = document.getElementById("query");
const statusSpan = document.getElementById("status");
const resultsBody = document.getElementById("resultsBody");
const ctx = document.getElementById("sentimentChart");

let chart;

async function fetchHeadlines(query) {
  const payload = { query: query || null, page_size: 20 };
  const res = await fetch(`${API_BASE}/headlines`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function analyzeBatch(headlines) {
  const payload = { headlines };
  const res = await fetch(`${API_BASE}/sentiment/batch`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function sentimentBadge(sentiment) {
  const cls = `badge ${sentiment}`;
  return `<span class="${cls}">${sentiment}</span>`;
}

function renderTable(items, analysis) {
  resultsBody.innerHTML = "";
  for (let i = 0; i < items.length; i++) {
    const a = items[i];
    const s = analysis.results[i];
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${sentimentBadge(s.sentiment)}</td>
      <td>${(s.confidence * 100).toFixed(1)}%</td>
      <td><a href="${a.url}" target="_blank" rel="noopener">${a.title}</a></td>
      <td>${a.source}</td>
      <td>${new Date(a.published_at).toLocaleString()}</td>
    `;
    resultsBody.appendChild(tr);
  }
}

function renderChart(analysis) {
  const counts = { positive: 0, neutral: 0, negative: 0 };
  for (const r of analysis.results) counts[r.sentiment]++;

  const data = {
    labels: ["Positive", "Neutral", "Negative"],
    datasets: [
      {
        label: "Headlines",
        data: [counts.positive, counts.neutral, counts.negative],
        backgroundColor: ["#10b981", "#6b7280", "#ef4444"],
      },
    ],
  };

  if (chart) chart.destroy();
  chart = new Chart(ctx, { type: "bar", data, options: { responsive: true } });
}

fetchBtn.addEventListener("click", async () => {
  const query = queryInput.value.trim();
  statusSpan.textContent = "Fetching headlines...";
  try {
    const headlines = await fetchHeadlines(query);
    statusSpan.textContent = `Analyzing ${headlines.count} headlines...`;
    const titles = headlines.items.map((i) => i.title);
    const analysis = await analyzeBatch(titles);
    renderTable(headlines.items, analysis);
    renderChart(analysis);
    statusSpan.textContent = "Done.";
  } catch (e) {
    console.error(e);
    statusSpan.textContent = "Error: " + (e.message || e);
  }
});

// // Initial load
// (async () => {
//   try {
//     statusSpan.textContent = "Loading default fintech headlines...";
//     const headlines = await fetchHeadlines(null);
//     const titles = headlines.items.map(i => i.title);
//     const analysis = await analyzeBatch(titles);
//     renderTable(headlines.items, analysis);
//     renderChart(analysis);
//     statusSpan.textContent = "Ready.";
//   } catch (e) {
//     statusSpan.textContent = "Startup error: " + (e.message || e);
//   }
// })();
