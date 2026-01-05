(async () => {
  const links = [
    "https://www.mercadolivre.com.br/raco-seca-golden-formula-ces-adultos-racas-pequenas-peru-e-arroz-101kg/p/MLB14871070#polycard_client=search-nordic&search_layout=grid&position=33&type=product&tracking_id=3e70b137-8822-43bb-ab50-187c34861410&wid=MLB3138086934&sid=search"
  ];

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  const input = document.querySelector("#url-0");
  const outputSelector = "#textfield-copyLink-1";
  const buttonSelector = ".button_generate-links:not(.andes-button--disabled)";

  if (!input) {
    console.error("Textarea não encontrado");
    return;
  }

  const setNativeValue = (element, value) => {
    const setter = Object.getOwnPropertyDescriptor(
      Object.getPrototypeOf(element),
      "value"
    ).set;
    setter.call(element, value);
    element.dispatchEvent(new Event("input", { bubbles: true }));
  };

  const results = [];

  for (const link of links) {
    setNativeValue(input, "");
    await sleep(300);

    setNativeValue(input, link);
    await sleep(800);

    const button = document.querySelector(buttonSelector);
    if (!button) {
      console.warn("Botão ainda desabilitado para:", link);
      continue;
    }

    button.click();

    let generated = "";
    for (let i = 0; i < 30; i++) {
      const output = document.querySelector(outputSelector);
      if (output && output.value && output.value.startsWith("http")) {
        generated = output.value;
        break;
      }
      await sleep(500);
    }

    if (generated) {
      results.push({ original: link, affiliate: generated });
      console.log("OK:", generated);
    } else {
      console.warn("Falhou:", link);
    }

    await sleep(1000);
  }

  console.table(results);
})();
