const form = document.querySelector("#expert-form");
const clearButton = document.querySelector("#clear-btn");
const selectAllButton = document.querySelector("#select-all-btn");
const demoButton = document.querySelector("#demo-btn");
const submitButton = form.querySelector('button[type="submit"]');
const ingredientInputs = Array.from(
  form.querySelectorAll('input[name="ingredientes"]')
);
const selectedCount = document.querySelector("#selected-count");
const statusBox = document.querySelector("#status-box");
const resultsGrid = document.querySelector("#results-grid");
const resultsTitle = document.querySelector("#results-title");
const resultsSubtitle = document.querySelector("#results-subtitle");
const recipeCount = document.querySelector("#recipe-count");

const DEMO_CASE = {
  objetivo: "aumentar_masa_muscular",
  tipoComida: "desayuno",
  ingredientes: ["semillas_chia", "yogur_griego", "banana"],
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatNumber(value, decimals = 2) {
  const number = Number(value);
  return Number.isInteger(number) ? String(number) : number.toFixed(decimals);
}

function setStatus(message, type = "info") {
  const icons = {
    info: "bi-info-circle",
    success: "bi-check-circle",
    warning: "bi-exclamation-triangle",
    danger: "bi-x-circle",
  };
  statusBox.className = `status-message status-${type}`;
  statusBox.innerHTML = `
    <i class="bi ${icons[type] || icons.info}" aria-hidden="true"></i>
    <span>${escapeHtml(message)}</span>
  `;
}

function selectedIngredients() {
  return ingredientInputs.filter((input) => input.checked).map((input) => input.value);
}

function updateSelectionCount() {
  const count = selectedIngredients().length;
  selectedCount.textContent = count;
  document.querySelector(".selection-summary").classList.toggle("has-selection", count > 0);
}

function applyIngredientSelection(ids) {
  const selected = new Set(ids);
  ingredientInputs.forEach((input) => {
    input.checked = selected.has(input.value);
  });
  updateSelectionCount();
}

function selectRadio(name, value) {
  const input = form.querySelector(`input[name="${name}"][value="${value}"]`);
  if (input) {
    input.checked = true;
  }
}

function confidenceTier(value) {
  if (value >= 100) {
    return { className: "confidence-complete", label: "Coincidencia completa" };
  }
  if (value >= 75) {
    return { className: "confidence-high", label: "Coincidencia alta" };
  }
  return { className: "confidence-partial", label: "Coincidencia parcial" };
}

function renderAvailabilityChips(ingredients, type) {
  const icon = type === "matched" ? "bi-check-circle-fill" : "bi-exclamation-circle";
  return ingredients
    .map((ingredient) => `
      <span class="availability-chip ${type}">
        <i class="bi ${icon}" aria-hidden="true"></i>
        ${escapeHtml(ingredient.nombre)}
      </span>
    `)
    .join("");
}

function renderRecipe(recipe) {
  const nutrition = recipe.nutricion;
  const confidence = Number(recipe.coincidencia.porcentaje);
  const tier = confidenceTier(confidence);
  const matched = renderAvailabilityChips(
    recipe.coincidencia.ingredientes_disponibles,
    "matched"
  );
  const missing = renderAvailabilityChips(
    recipe.coincidencia.ingredientes_faltantes,
    "missing"
  );

  return `
    <article class="recipe-card ${tier.className}">
      <div class="recipe-card-header">
        <div>
          <span class="recipe-kicker">
            ${escapeHtml(recipe.tipo_comida.nombre)} ·
            ${escapeHtml(recipe.tiempo_preparacion_min)} min ·
            ${escapeHtml(recipe.dificultad)}
          </span>
          <h3>${escapeHtml(recipe.nombre)}</h3>
          <p>${escapeHtml(recipe.descripcion)}</p>
        </div>
        <div class="confidence-score">
          <strong>${formatNumber(confidence)}%</strong>
          <span>${tier.label}</span>
        </div>
      </div>

      <div
        class="confidence-progress"
        role="progressbar"
        aria-label="Porcentaje de certeza"
        aria-valuemin="0"
        aria-valuemax="100"
        aria-valuenow="${escapeHtml(confidence)}"
      >
        <span style="width: ${Math.min(100, Math.max(0, confidence))}%"></span>
      </div>

      <div class="nutrition-grid" aria-label="Información nutricional estimada">
        <div class="calorie-metric">
          <span>Calorías</span>
          <strong>${escapeHtml(nutrition.calorias)}</strong>
          <small>kcal</small>
        </div>
        <div class="macro-metric protein">
          <span>Proteína</span>
          <strong>${escapeHtml(nutrition.proteinas)} g</strong>
        </div>
        <div class="macro-metric carbs">
          <span>Carbohidratos</span>
          <strong>${escapeHtml(nutrition.carbohidratos)} g</strong>
        </div>
        <div class="macro-metric fats">
          <span>Grasas</span>
          <strong>${escapeHtml(nutrition.grasas)} g</strong>
        </div>
      </div>

      <div class="availability-grid">
        <section class="availability-block matched-block">
          <h4>
            <i class="bi bi-check2-circle" aria-hidden="true"></i>
            Coincidentes
            <span>${recipe.coincidencia.cantidad_disponible}/${recipe.coincidencia.cantidad_requerida}</span>
          </h4>
          <div>${matched}</div>
        </section>
        <section class="availability-block missing-block">
          <h4>
            <i class="bi bi-bag-plus" aria-hidden="true"></i>
            Faltantes
          </h4>
          <div>
            ${missing || '<span class="complete-message"><i class="bi bi-stars"></i> Receta completa</span>'}
          </div>
        </section>
      </div>

      <details class="explanation-panel">
        <summary>
          <span>
            <i class="bi bi-diagram-3" aria-hidden="true"></i>
            ¿Por qué el sistema experto recomienda esto?
          </span>
          <i class="bi bi-chevron-down detail-chevron" aria-hidden="true"></i>
        </summary>
        <div class="explanation-content">
          <div class="rule-badge">
            Regla activada: ${escapeHtml(recipe.regla_activada.id)}
          </div>
          <p>${escapeHtml(recipe.explicacion)}</p>
          <small>
            Scoring para el objetivo:
            <strong>${formatNumber(recipe.puntuacion_objetivo)} puntos</strong>
            · ${escapeHtml(recipe.adecuacion)}
          </small>
        </div>
      </details>
    </article>
  `;
}

function renderEmptyState(title, message, icon = "bi-sliders") {
  resultsGrid.innerHTML = `
    <div class="empty-state">
      <i class="bi ${icon}" aria-hidden="true"></i>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(message)}</p>
    </div>
  `;
}

function renderLoading() {
  resultsGrid.innerHTML = `
    <div class="loading-card" aria-hidden="true">
      <span></span><span></span><span></span><span></span>
    </div>
    <div class="loading-card" aria-hidden="true">
      <span></span><span></span><span></span><span></span>
    </div>
  `;
}

function renderRecipes(data) {
  const recipes = data.recetas || [];
  recipeCount.textContent = recipes.length;
  resultsTitle.textContent = recipes.length
    ? "Recomendaciones del motor"
    : "Sin recomendaciones";
  resultsSubtitle.textContent = (
    `${data.objetivo.nombre} · ${data.tipo_comida.nombre} · ` +
    `${data.totales.reglas_activadas} regla(s) activada(s)`
  );

  if (recipes.length === 0) {
    setStatus(
      "Ninguna receta superó el umbral estricto de coincidencia mayor al 50%.",
      "warning"
    );
    renderEmptyState(
      "Umbral no alcanzado",
      "Agrega más ingredientes o cambia el tipo de comida para activar una regla con más del 50% de certeza.",
      "bi-shield-exclamation"
    );
    return;
  }

  setStatus(
    `${recipes.length} recomendación(es) ordenadas por certeza y scoring nutricional.`,
    "success"
  );
  resultsGrid.innerHTML = recipes.map(renderRecipe).join("");
}

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  submitButton.classList.toggle("is-loading", isLoading);
  form.setAttribute("aria-busy", String(isLoading));
}

ingredientInputs.forEach((input) => {
  input.addEventListener("change", updateSelectionCount);
});

selectAllButton.addEventListener("click", () => {
  applyIngredientSelection(ingredientInputs.map((input) => input.value));
  setStatus("Todos los ingredientes están seleccionados.", "info");
});

clearButton.addEventListener("click", () => {
  applyIngredientSelection([]);
  recipeCount.textContent = "0";
  resultsTitle.textContent = "Resultados del motor";
  resultsSubtitle.textContent = "Las recomendaciones aparecerán ordenadas por certeza.";
  setStatus("Selección limpia. Elige al menos un ingrediente.", "info");
  renderEmptyState(
    "Comienza una nueva consulta",
    "Selecciona ingredientes disponibles para construir la memoria de trabajo.",
    "bi-arrow-left-circle"
  );
});

demoButton.addEventListener("click", () => {
  selectRadio("objetivo", DEMO_CASE.objetivo);
  selectRadio("tipo_comida", DEMO_CASE.tipoComida);
  applyIngredientSelection(DEMO_CASE.ingredientes);
  setStatus(
    "Caso demo cargado: desayuno para aumentar masa muscular. Ejecuta el motor.",
    "info"
  );
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const ingredientes = selectedIngredients();

  if (ingredientes.length === 0) {
    recipeCount.textContent = "0";
    resultsTitle.textContent = "Faltan hechos iniciales";
    resultsSubtitle.textContent = "El motor necesita al menos un ingrediente.";
    setStatus("Selecciona al menos un ingrediente antes de ejecutar.", "warning");
    renderEmptyState(
      "Selecciona ingredientes",
      "Los ingredientes son los hechos que permiten evaluar las reglas de producción.",
      "bi-hand-index-thumb"
    );
    return;
  }

  setLoading(true);
  setStatus("Evaluando categorías, reglas y porcentajes de coincidencia...", "info");
  renderLoading();

  try {
    const response = await fetch(form.dataset.apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        objetivo: form.elements.objetivo.value,
        tipo_comida: form.elements.tipo_comida.value,
        ingredientes,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      const details = Array.isArray(data.detalles) ? data.detalles.join(" ") : "";
      throw new Error(details || data.error || "No se pudo procesar la solicitud.");
    }

    renderRecipes(data);
    if (window.matchMedia("(max-width: 991px)").matches) {
      document.querySelector(".results-panel").scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  } catch (error) {
    recipeCount.textContent = "0";
    resultsTitle.textContent = "No fue posible completar la consulta";
    resultsSubtitle.textContent = "Revisa el servidor e intenta nuevamente.";
    setStatus(error.message, "danger");
    renderEmptyState(
      "Error de conexión",
      "El motor no devolvió una respuesta válida.",
      "bi-wifi-off"
    );
  } finally {
    setLoading(false);
  }
});

updateSelectionCount();
