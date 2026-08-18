const form = document.querySelector("#expert-form");
const clearButton = document.querySelector("#clear-btn");
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

function renderRecipes(data) {
  const recipes = data.recetas || [];
  recipeCount.textContent = recipes.length;
  resultsTitle.textContent = `${recipes.length} receta(s) recomendada(s)`;
  resultsSubtitle.textContent = `${data.objetivo_nombre} · ${data.totales.reglas_activadas} regla(s) activada(s).`;
  resultsGrid.innerHTML = "";

  if (recipes.length === 0) {
    setStatus("No se encontraron recetas para esa combinación de ingredientes.", "warning");
    return;
  }

  setStatus(
    `El motor de inferencia aplicó el criterio: ${data.criterio_objetivo.nombre}.`,
    "success"
  );

  resultsGrid.innerHTML = recipes.map((recipe) => {
    const chips = recipe.ingredientes
      .map((ingredient) => `<span class="ingredient-chip">${escapeHtml(ingredient.nombre)}</span>`)
      .join("");

    return `
      <article class="recipe-card">
        <div class="recipe-card-header">
          <div>
            <span class="recipe-kicker">Regla ${escapeHtml(recipe.regla_activada.numero)}</span>
            <h3>${escapeHtml(recipe.nombre)}</h3>
          </div>
          <span class="fit-badge">${escapeHtml(recipe.adecuacion)}</span>
        </div>
        <p class="mb-2">${escapeHtml(recipe.descripcion)}</p>
        <div class="metric-row">
          <span class="metric-pill">${escapeHtml(recipe.calorias)} kcal</span>
          <span class="metric-pill">${escapeHtml(recipe.proteinas)} g proteína</span>
        </div>
        <div aria-label="Ingredientes de ${escapeHtml(recipe.nombre)}">
          ${chips}
        </div>
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
    setStatus("Debes seleccionar al menos un ingrediente para ejecutar el sistema.", "warning");
    return;
  }

  setStatus("Analizando reglas del sistema experto...", "info");

  try {
    const response = await fetch(form.dataset.apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        objetivo: form.objetivo.value,
        ingredientes,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "No se pudo procesar la solicitud.");
    }

    renderRecipes(data);
  } catch (error) {
    recipeCount.textContent = "0";
    resultsGrid.innerHTML = "";
    resultsTitle.textContent = "Error";
    resultsSubtitle.textContent = "Revisa la conexión con el servidor Flask.";
    setStatus(error.message, "danger");
  }
});

clearButton.addEventListener("click", () => {
  form.querySelectorAll('input[name="ingredientes"]').forEach((input) => {
    input.checked = false;
  });

  recipeCount.textContent = "0";
  resultsGrid.innerHTML = "";
  resultsTitle.textContent = "Resultados";
  resultsSubtitle.textContent = "Los resultados aparecerán aquí sin recargar la página.";
  setStatus("Marca ingredientes y ejecuta el sistema experto.", "info");
});
