(() => {
  const garmentEl = document.getElementById("garment");
  const foldedItem = document.getElementById("folded-item");
  const stack = document.getElementById("stack");
  const basket = document.getElementById("basket");
  const foldBtn = document.getElementById("fold-btn");
  const resetBtn = document.getElementById("reset-btn");
  const statusEl = document.getElementById("status");
  const countEl = document.getElementById("count");
  const garmentInputs = document.querySelectorAll('input[name="garment"]');
  const connectBtn = document.getElementById("connect-btn");
  const hwFoldBtn = document.getElementById("hw-fold-btn");
  const hwHomeBtn = document.getElementById("hw-home-btn");
  const hwSupport = document.getElementById("hw-support");

  const labels = {
    camiseta: "Camiseta",
    pantalon: "Pantalón",
    toalla: "Toalla",
  };

  let busy = false;
  let count = 0;
  let port = null;
  let reader = null;
  let readBuffer = "";
  let keepReading = false;
  let foldTimeout = null;

  function selectedType() {
    const checked = document.querySelector('input[name="garment"]:checked');
    return checked ? checked.value : "camiseta";
  }

  function setStatus(message) {
    statusEl.textContent = message;
  }

  function setHwConnected(connected) {
    if (hwFoldBtn) hwFoldBtn.disabled = !connected || busy;
    if (hwHomeBtn) hwHomeBtn.disabled = !connected || busy;
    if (connectBtn) {
      connectBtn.textContent = connected ? "Desconectar" : "Conectar ESP32";
    }
    if (hwSupport) {
      hwSupport.textContent = connected
        ? "ESP32 conectado. Coloca la prenda y pulsa Doblar en hardware."
        : "Conecta tu Dobla por USB (Chrome / Edge).";
    }
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

  function addToBasket(type) {
    const item = document.createElement("div");
    item.className = `stack-item ${type}`;
    item.title = labels[type];
    stack.appendChild(item);

    basket.classList.remove("catch");
    void basket.offsetWidth;
    basket.classList.add("catch");

    count += 1;
    countEl.textContent = String(count);
  }

  async function playSimAnimation(type) {
    garmentEl.dataset.type = type;
    foldedItem.dataset.type = type;
    garmentEl.classList.remove("folded");
    garmentEl.classList.add("folding");
    await wait(700);
    garmentEl.classList.add("folded");
    foldedItem.classList.add("visible");
    await wait(120);
    foldedItem.classList.add("flying");
    await wait(820);
    foldedItem.classList.remove("visible", "flying");
    garmentEl.classList.remove("folding", "folded");
  }

  function setBusy(next) {
    busy = next;
    foldBtn.disabled = next;
    garmentInputs.forEach((input) => {
      input.disabled = next;
    });
    setHwConnected(!!port);
  }

  function clearFoldTimeout() {
    if (foldTimeout) {
      clearTimeout(foldTimeout);
      foldTimeout = null;
    }
  }

  async function foldAndStore() {
    if (busy) return;
    setBusy(true);
    const type = selectedType();
    setStatus(`Doblando ${labels[type].toLowerCase()}…`);
    try {
      await playSimAnimation(type);
      addToBasket(type);
      setStatus(
        count === 1
          ? "Primera prenda en la canasta."
          : `${count} prendas listas en la canasta.`
      );
    } finally {
      setBusy(false);
    }
  }

  function resetBasket() {
    if (busy) return;
    stack.innerHTML = "";
    count = 0;
    countEl.textContent = "0";
    setStatus("Canasta vacía. Elige una prenda y vuelve a doblar.");
    syncGarmentPreview();
  }

  async function writeSerial(line) {
    if (!port || !port.writable) throw new Error("Sin puerto");
    const writer = port.writable.getWriter();
    try {
      await writer.write(new TextEncoder().encode(`${line}\n`));
    } finally {
      writer.releaseLock();
    }
  }

  async function readLoop() {
    if (!port || !port.readable) return;
    keepReading = true;
    const decoder = new TextDecoder();
    reader = port.readable.getReader();
    try {
      while (keepReading) {
        const { value, done } = await reader.read();
        if (done) break;
        readBuffer += decoder.decode(value, { stream: true });
        let idx;
        while ((idx = readBuffer.search(/\r?\n/)) >= 0) {
          const line = readBuffer.slice(0, idx).trim();
          readBuffer = readBuffer.slice(idx).replace(/^\r?\n/, "");
          if (line) handleHwLine(line);
        }
      }
    } catch (err) {
      if (keepReading) {
        setStatus(`Serie: ${err.message || "lectura interrumpida"}`);
      }
    } finally {
      try {
        reader.releaseLock();
      } catch (_) {
        /* ignore */
      }
      reader = null;
    }
  }

  function finishHwFoldOk() {
    clearFoldTimeout();
    const type = selectedType();
    playSimAnimation(type)
      .then(() => {
        addToBasket(type);
        setStatus(
          count === 1
            ? "Hardware listo. Primera prenda en la canasta."
            : `Hardware listo. ${count} prendas en la canasta.`
        );
      })
      .finally(() => {
        setBusy(false);
      });
  }

  function handleHwLine(line) {
    if (line === "FOLD_START") {
      setStatus("Hardware: doblando…");
    } else if (line === "FOLD_DONE") {
      finishHwFoldOk();
    } else if (line === "HOME_DONE") {
      clearFoldTimeout();
      setStatus("Hardware en posición home.");
      setBusy(false);
    } else if (line === "BUSY") {
      setStatus("Hardware ocupado. Espera a que termine.");
    } else if (line === "DOBLA_READY") {
      setStatus("ESP32 listo.");
    }
  }

  async function disconnectSerial() {
    keepReading = false;
    clearFoldTimeout();
    try {
      if (reader) await reader.cancel();
    } catch (_) {
      /* ignore */
    }
    try {
      if (port) await port.close();
    } catch (_) {
      /* ignore */
    }
    port = null;
    setBusy(false);
    setHwConnected(false);
    setStatus("ESP32 desconectado.");
  }

  async function connectSerial() {
    if (port) {
      await disconnectSerial();
      return;
    }
    if (!("serial" in navigator)) {
      setStatus("Este navegador no soporta Web Serial. Usa Chrome o Edge.");
      return;
    }
    try {
      port = await navigator.serial.requestPort();
      await port.open({ baudRate: 115200 });
      setHwConnected(true);
      setStatus("ESP32 conectado.");
      readLoop();
    } catch (err) {
      port = null;
      setHwConnected(false);
      if (err && err.name === "NotFoundError") {
        setStatus("No se eligió ningún puerto.");
      } else {
        setStatus(`No se pudo conectar: ${err.message || err}`);
      }
    }
  }

  async function hwFold() {
    if (!port || busy) return;
    setBusy(true);
    try {
      await writeSerial("FOLD");
      setStatus("Comando FOLD enviado al ESP32…");
      clearFoldTimeout();
      foldTimeout = setTimeout(() => {
        setStatus(
          "Sin respuesta del ESP32. Revisa alimentación, USB y el Monitor Serial."
        );
        setBusy(false);
      }, 20000);
    } catch (err) {
      setBusy(false);
      setStatus(`Error al enviar FOLD: ${err.message || err}`);
    }
  }

  async function hwHome() {
    if (!port || busy) return;
    try {
      await writeSerial("HOME");
      setStatus("Comando HOME enviado…");
    } catch (err) {
      setStatus(`Error al enviar HOME: ${err.message || err}`);
    }
  }

  garmentInputs.forEach((input) => {
    input.addEventListener("change", syncGarmentPreview);
  });

  foldBtn.addEventListener("click", () => {
    foldAndStore().catch(() => {
      setBusy(false);
      setStatus("Hubo un problema al doblar. Inténtalo de nuevo.");
    });
  });

  resetBtn.addEventListener("click", resetBasket);

  if (connectBtn) connectBtn.addEventListener("click", () => connectSerial());
  if (hwFoldBtn) hwFoldBtn.addEventListener("click", () => hwFold());
  if (hwHomeBtn) hwHomeBtn.addEventListener("click", () => hwHome());

  if (hwSupport && !("serial" in navigator)) {
    hwSupport.textContent =
      "Web Serial no disponible aquí. Usa Chrome/Edge en escritorio, o el botón físico del ESP32.";
    if (connectBtn) connectBtn.disabled = true;
  }

  setHwConnected(false);
  syncGarmentPreview();
})();
