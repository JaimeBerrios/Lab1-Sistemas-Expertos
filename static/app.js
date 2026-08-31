const form = document.querySelector("#expert-form");
const clearButton = document.querySelector("#clear-btn");
const submitButton = form.querySelector('button[type="submit"]');
const statusBox = document.querySelector("#status-box");
const resultsGrid = document.querySelector("#results-grid");
const resultsTitle = document.querySelector("#results-title");
const resultsSubtitle = document.querySelector("#results-subtitle");
const recipeCount = document.querySelector("#recipe-count");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setStatus(message, type = "info") {
  statusBox.className = `alert alert-${type} mb-4`;
  statusBox.textContent = message;
}

function selectedIngredients() {
  return Array.from(form.querySelectorAll('input[name="ingredientes"]:checked'))
    .map((input) => input.value);
}

function renderIngredientChips(ingredients, className = "") {
  return ingredients
    .map((ingredient) => (
      `<span class="ingredient-chip ${className}">${escapeHtml(ingredient.nombre)}</span>`
    ))
    .join("");
}

function renderRecipes(data) {
  const recipes = data.recetas || [];
  recipeCount.textContent = recipes.length;
  resultsTitle.textContent = `${recipes.length} receta(s) recomendada(s)`;
  resultsSubtitle.textContent = (
    `${data.objetivo.nombre} · ${data.tipo_comida.nombre} · ` +
    `${data.totales.reglas_activadas} regla(s) activada(s)`
  );
  resultsGrid.innerHTML = "";

  if (recipes.length === 0) {
    setStatus(
      `No hay recetas que superen el ${data.umbral_coincidencia}% de coincidencia.`,
      "warning"
    );
    return;
  }

  setStatus(
    `Resultados ordenados por coincidencia y puntuación nutricional. ${data.objetivo.criterio}`,
    "success"
  );

  resultsGrid.innerHTML = recipes.map((recipe) => {
    const ingredients = renderIngredientChips(recipe.ingredientes);
    const missing = renderIngredientChips(
      recipe.coincidencia.ingredientes_faltantes,
      "ingredient-chip-missing"
    );
    const nutrition = recipe.nutricion;

    return `
      <article class="recipe-card">
        <div class="recipe-card-header">
          <div>
            <span class="recipe-kicker">
              ${escapeHtml(recipe.regla_activada.id)} ·
              ${escapeHtml(recipe.tipo_comida.nombre)} ·
              ${escapeHtml(recipe.tiempo_preparacion_min)} min
            </span>
            <h3>${escapeHtml(recipe.nombre)}</h3>
          </div>
          <div class="badge-stack">
            <span class="confidence-badge">
              ${escapeHtml(recipe.coincidencia.porcentaje.toFixed(2))}% coincidencia
            </span>
            <span class="fit-badge">
              ${escapeHtml(recipe.adecuacion)} ·
              ${escapeHtml(recipe.puntuacion_objetivo.toFixed(2))} pts
            </span>
          </div>
        </div>
        <p class="mb-2">${escapeHtml(recipe.descripcion)}</p>
        <div class="metric-row" aria-label="Información nutricional estimada">
          <span class="metric-pill">${escapeHtml(nutrition.calorias)} kcal</span>
          <span class="metric-pill">${escapeHtml(nutrition.proteinas)} g proteína</span>
          <span class="metric-pill metric-pill-secondary">${escapeHtml(nutrition.carbohidratos)} g carbohidratos</span>
          <span class="metric-pill metric-pill-secondary">${escapeHtml(nutrition.grasas)} g grasas</span>
        </div>
        <div aria-label="Ingredientes de ${escapeHtml(recipe.nombre)}">
          ${ingredients}
        </div>
        ${missing ? `
          <div class="missing-ingredients">
            <strong>Ingredientes faltantes</strong>
            <div>${missing}</div>
          </div>
        ` : ""}
        <div class="inference-box">
          <strong>Inferencia aplicada</strong>
          <p>${escapeHtml(recipe.explicacion)}</p>
        </div>
      </article>
    `;
  }).join("");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const ingredientes = selectedIngredients();

  if (ingredientes.length === 0) {
    recipeCount.textContent = "0";
    resultsGrid.innerHTML = "";
    resultsTitle.textContent = "Resultados";
    resultsSubtitle.textContent = "Selecciona al menos un ingrediente disponible.";
    setStatus(
      "Debes seleccionar al menos un ingrediente para ejecutar el sistema.",
      "warning"
    );
    return;
  }

  submitButton.disabled = true;
  setStatus("Evaluando reglas, coincidencia y objetivo nutricional...", "info");

  try {
    const response = await fetch(form.dataset.apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        objetivo: form.objetivo.value,
        tipo_comida: form.tipo_comida.value,
        ingredientes,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      const details = Array.isArray(data.detalles) ? data.detalles.join(" ") : "";
      throw new Error(details || data.error || "No se pudo procesar la solicitud.");
    }
    renderRecipes(data);
  } catch (error) {
    recipeCount.textContent = "0";
    resultsGrid.innerHTML = "";
    resultsTitle.textContent = "Error";
    resultsSubtitle.textContent = "No fue posible completar la consulta.";
    setStatus(error.message, "danger");
  } finally {
    submitButton.disabled = false;
  }
});

clearButton.addEventListener("click", () => {
  form.querySelectorAll('input[name="ingredientes"]').forEach((input) => {
    input.checked = false;
  });
  form.objetivo.value = "mantener_peso";
  form.tipo_comida.value = "todos";
  recipeCount.textContent = "0";
  resultsGrid.innerHTML = "";
  resultsTitle.textContent = "Resultados";
  resultsSubtitle.textContent = "Los resultados aparecerán aquí sin recargar la página.";
  setStatus("Marca ingredientes y ejecuta el sistema experto.", "info");
});
