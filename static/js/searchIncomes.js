const searchField = document.querySelector('#searchField');

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tablebody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tablebody.innerHTML = "";
        fetch("search-income/", {
            body: JSON.stringify({ search: searchValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                appTable.style.display = "none";
                tableOutput.style.display = "block";

                if (data.length === 0) {
                    noResults.style.display = "block";
                    tableOutput.style.display = "none";

                } else {
                    noResults.style.display = "none";
                    data.forEach((item) => {
                        tablebody.innerHTML += `<tr>
                  <td>${item.amount}</td>
                  <td>${item.source}</td>
                  <td>${item.description}</td>
                  <td>${item.date}</td>
                  </tr>`;
                    });
                }
            });
    } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});