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
        fetch("/search-expense/", {
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
                        tablebody.innerHTML += `<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                  <td class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">${item.amount}</td>
                  <td class="px-6 py-4">${item.category}</td>
                  <td class="px-6 py-4">${item.description}</td>
                  <td class="px-6 py-4">${item.date}</td>
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