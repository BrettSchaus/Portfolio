const button = document.getElementById("stock-button");
const symbol = document.getElementById("stock-symbol");
const value = document.getElementById("stock-value");

button.addEventListener("click", async function () {
    value.textContent = "Loading...";

    try {
        const response = await fetch("/api/stock");
        const data = await response.json();

        symbol.textContent = data.symbol;
        value.textContent = `$${Number(data.price).toFixed(2)}`;

    } catch (error) {
        symbol.textContent = "ERROR";
        value.textContent = "Unable to load price";
        console.error(error);
    }
});
