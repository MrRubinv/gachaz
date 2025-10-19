const tg = window.Telegram ? window.Telegram.WebApp : null;
if (tg) {
  tg.expand();
}

let currentBanner = "standard";
const BANNERS = {
  "standard": {
    title: "Стандартный баннер",
    image: "https://admin.esports.gg/wp-content/uploads/2024/08/Jane-Doe-Upcoming-ZZZ-banner-1024x576.jpg",
  },
  "featured-ellen": {
    title: "Выделенный: Эллен",
    image: "https://i.imgur.com/Rnbjskv.jpeg"
  },
  "featured-lycaon": {
    title: "Выделенный: Ликаон",
    image: "https://i.imgur.com/J0D8Lls.jpeg"
  },
  "amplify-core": {
    title: "Амплификация: Ядро",
    image: "https://i.imgur.com/0hQ3xFY.jpeg"
  },
  "gang-channel": {
    title: "Канал банду",
    image: "https://i.imgur.com/0bF3n8Z.jpeg"
  }
};

function applyBanner(bannerKey) {
  currentBanner = bannerKey in BANNERS ? bannerKey : "standard";
  const meta = BANNERS[currentBanner];
  const imgEl = document.getElementById("bannerImage");
  const titleEl = document.getElementById("bannerTitle");
  if (imgEl) imgEl.src = meta.image;
  if (titleEl) titleEl.textContent = meta.title;
  // update selection state
  document.querySelectorAll('.banner-item').forEach(btn => {
    if (btn.getAttribute('data-banner') === currentBanner) {
      btn.classList.add('selected');
    } else {
      btn.classList.remove('selected');
    }
  });
}

async function doPull(count) {
  const payload = { count, banner: currentBanner };
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

// Banner item clicks
const switcher = document.getElementById("bannerSwitcher");
if (switcher) {
  switcher.querySelectorAll('.banner-item').forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.getAttribute('data-banner');
      applyBanner(key);
    });
  });
}

// Initialize banner state on load
applyBanner(currentBanner);

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

// Menu functionality
const menuButton = document.getElementById("menuButton");
const menuDropdown = document.getElementById("menuDropdown");

menuButton.addEventListener("click", (e) => {
  e.stopPropagation();
  menuDropdown.classList.toggle("show");
});

// Close menu when clicking outside
document.addEventListener("click", (e) => {
  if (!menuButton.contains(e.target) && !menuDropdown.contains(e.target)) {
    menuDropdown.classList.remove("show");
  }
});

// Menu item click handlers
document.querySelectorAll(".menu-item").forEach(item => {
  item.addEventListener("click", (e) => {
    e.preventDefault();
    const section = e.target.getAttribute("data-section");
    handleMenuClick(section);
    menuDropdown.classList.remove("show");
  });
});

function handleMenuClick(section) {
  switch(section) {
    case "profile":
      alert("👤 Профиль\n\nЗдесь будет информация о вашем профиле:\n• Уровень\n• Статистика круток\n• Достижения");
      break;
    case "characters":
      alert("🎭 Персонажи\n\nЗдесь будет коллекция ваших персонажей:\n• Полученные персонажи\n• Уровни и характеристики\n• Сортировка по редкости");
      break;
    case "settings":
      alert("⚙️ Настройки\n\nЗдесь будут настройки приложения:\n• Язык\n• Звуки\n• Анимации\n• Тема");
      break;
  }
}


