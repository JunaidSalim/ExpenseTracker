const renderdouChart = (data, labels,value) => {
  var ctx = document.getElementById("douChart").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: `${value} Expenses`,
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 3,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expenses per category",
      },
    },
  });
};

const renderbarChart = (data, labels,value) => {

  var ctx = document.getElementById("barChart").getContext("2d");
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: `${value} Expenses`,
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      title: {
        display: true,
        text: "Expense per Category",
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true,
          },
        }],
      },
    },
  });
};

const getChartData = (value) => {
  fetch(`/expense-summary?value=${value}`)
    .then((res) => res.json())
    .then((results) => {
      const category_data = results.expense_category_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];

      data_key = {
        "all" : "All",
        "last_month": "Last Month",
        "last_30_days": "Last 30 Days"
      }

      renderbarChart(data, labels, data_key[value]);
      renderdouChart(data, labels, data_key[value]);

    });
};

let filterbutton = document.getElementById('options')
let filterOption = filterbutton.value

filterbutton.addEventListener('change', (e) => {
   window.location.reload()
});


document.onload = getChartData(value = filterOption);