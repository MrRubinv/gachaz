const tg = window.Telegram ? window.Telegram.WebApp : null;
if (tg) {
  tg.expand();
}

async function doPull(count) {
  const payload = { count, banner: "standard" };
  const res = await fetch("/api/pull", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error("Не удалось выполнить крутку");
  }
  return res.json();
}

function render(results, summary) {
  const resultsEl = document.getElementById("results");
  const summaryEl = document.getElementById("summary");
  resultsEl.innerHTML = results
    .map(
      (r) => `
      <div class="card rarity-${r.rarity}">
        <div class="name">${r.name}</div>
        <div class="rarity">${"★".repeat(r.rarity)}</div>
      </div>
    `
    )
    .join("");
  summaryEl.textContent = `3★: ${summary.pulled3} | 4★: ${summary.pulled4} | 5★: ${summary.pulled5}`;
}

document.getElementById("pull1").addEventListener("click", async () => {
  try {
    const data = await doPull(1);
    render(data.results, data.summary);
  } catch (e) {
    alert(e.message);
  }
});

document.getElementById("pull10").addEventListener("click", async () => {
  try {
    const data = await doPull(10);
    render(data.results, data.summary);
  } catch (e) {
    alert(e.message);
  }
});


