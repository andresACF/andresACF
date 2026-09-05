(() => {
  const garmentEl = document.getElementById("garment");
  const foldedItem = document.getElementById("folded-item");
  const stack = document.getElementById("stack");
  const basket = document.getElementById("basket");
  const foldBtn = document.getElementById("fold-btn");
  const resetBtn = document.getElementById("reset-btn");
  const status = document.getElementById("status");
  const countEl = document.getElementById("count");
  const garmentInputs = document.querySelectorAll('input[name="garment"]');

  const labels = {
    camiseta: "Camiseta",
    pantalon: "Pantalón",
    toalla: "Toalla",
  };

  let busy = false;
  let count = 0;

  function selectedType() {
    const checked = document.querySelector('input[name="garment"]:checked');
    return checked ? checked.value : "camiseta";
  }

  function setStatus(message) {
    status.textContent = message;
  }

  function syncGarmentPreview() {
    if (busy) return;
    const type = selectedType();
    garmentEl.dataset.type = type;
    garmentEl.classList.remove("folding", "folded");
    foldedItem.classList.remove("visible", "flying");
    foldedItem.dataset.type = type;
    setStatus(`${labels[type]} lista sobre la tabla.`);
  }

  function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function foldAndStore() {
    if (busy) return;
    busy = true;
    foldBtn.disabled = true;
    garmentInputs.forEach((input) => {
      input.disabled = true;
    });

    const type = selectedType();
    garmentEl.dataset.type = type;
    foldedItem.dataset.type = type;

    setStatus(`Doblando ${labels[type].toLowerCase()}…`);
    garmentEl.classList.remove("folded");
    garmentEl.classList.add("folding");

    await wait(700);

    garmentEl.classList.add("folded");
    foldedItem.classList.add("visible");
    setStatus("Enviando a la canasta…");

    await wait(120);
    foldedItem.classList.add("flying");

    await wait(820);

    const item = document.createElement("div");
    item.className = `stack-item ${type}`;
    item.title = labels[type];
    stack.appendChild(item);

    basket.classList.remove("catch");
    void basket.offsetWidth;
    basket.classList.add("catch");

    count += 1;
    countEl.textContent = String(count);

    foldedItem.classList.remove("visible", "flying");
    garmentEl.classList.remove("folding", "folded");

    setStatus(
      count === 1
        ? "Primera prenda en la canasta."
        : `${count} prendas listas en la canasta.`
    );

    busy = false;
    foldBtn.disabled = false;
    garmentInputs.forEach((input) => {
      input.disabled = false;
    });
  }

  function resetBasket() {
    if (busy) return;
    stack.innerHTML = "";
    count = 0;
    countEl.textContent = "0";
    setStatus("Canasta vacía. Elige una prenda y vuelve a doblar.");
    syncGarmentPreview();
  }

  garmentInputs.forEach((input) => {
    input.addEventListener("change", syncGarmentPreview);
  });

  foldBtn.addEventListener("click", () => {
    foldAndStore().catch(() => {
      busy = false;
      foldBtn.disabled = false;
      garmentInputs.forEach((input) => {
        input.disabled = false;
      });
      setStatus("Hubo un problema al doblar. Inténtalo de nuevo.");
    });
  });

  resetBtn.addEventListener("click", resetBasket);

  syncGarmentPreview();
})();
