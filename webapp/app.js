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
  
  // Clear previous results
  resultsEl.innerHTML = "";
  
  // Create cards with animation delay
  results.forEach((r, index) => {
    const card = document.createElement("div");
    card.className = `card rarity-${r.rarity} card-animate`;
    card.style.animationDelay = `${index * 0.1}s`;
    card.innerHTML = `
      <div class="name">${r.name}</div>
      <div class="rarity">${"★".repeat(r.rarity)}</div>
    `;
    resultsEl.appendChild(card);
  });
  
  // Update summary with delay
  setTimeout(() => {
    summaryEl.textContent = `3★: ${summary.pulled3} | 4★: ${summary.pulled4} | 5★: ${summary.pulled5}`;
  }, results.length * 100 + 200);
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


