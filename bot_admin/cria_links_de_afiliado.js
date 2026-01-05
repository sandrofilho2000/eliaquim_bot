(async () => {
  const links = [
    "https://www.mercadolivre.com.br/jipe-infantil-eletrico-12v-carrinho-controle-remoto-musica-cor-vermelho-voltagem-do-carregador-110v220v-brinqkids/p/MLB40342995",
    "https://www.mercadolivre.com.br/air-fryer-britnia-55l-1500w-antiaderente-redstone-bfr50-127v/p/MLB34733595?pdp_filters=item_id%3AMLB4689906140#polycard_client=affiliates&wid=MLB4689906140&sid=affiliates"
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
