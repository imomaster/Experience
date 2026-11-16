// Descarrega vários PDF do Diário da República de uma só vez, pelo browser.
//
// Para quando o `curl` é recusado (403) em files.diariodarepublica.pt.
// 1. Abrir num separador do Chrome uma página de https://diariodarepublica.pt/ ou um PDF de
//    https://files.diariodarepublica.pt/… (qualquer das duas origens serve).
//    O pedido tem de partir do browser: é isso que evita a recusa.
// 2. Correr este ficheiro nesse separador (ferramenta de JavaScript do browser) e chamar:
//        await descarregarPDFs(["https://files.diariodarepublica.pt/1s/…pdf", "…"])
// 3. O browser grava um único ficheiro, dre_pdfs.json (um só, porque o Chrome
//    bloqueia várias transferências automáticas seguidas no mesmo separador).
// 4. No terminal:  python3 dre_desempacotar.py ~/Downloads/dre_pdfs.json -o pdfs/
async function descarregarPDFs(urls, nome = "dre_pdfs.json") {
  const pacote = {};
  for (const u of urls) {
    try {
      const r = await fetch(u, { credentials: "omit" });
      if (!r.ok) { pacote[u] = { erro: "HTTP " + r.status }; continue; }
      const b = new Uint8Array(await r.arrayBuffer());
      let bin = "";
      for (let i = 0; i < b.length; i += 0x8000) bin += String.fromCharCode.apply(null, b.subarray(i, i + 0x8000));
      pacote[u] = { bytes: b.length, base64: btoa(bin) };
    } catch (e) {
      pacote[u] = { erro: String(e) };
    }
  }
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(pacote)], { type: "application/json" }));
  a.download = nome;
  document.body.appendChild(a);
  a.click();
  a.remove();
  return Object.fromEntries(Object.entries(pacote).map(([k, v]) => [k, v.erro || v.bytes + " bytes"]));
}
