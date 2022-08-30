var data = {
    labels: field_labels,

    datasets: [{
      label: 'New Label',
      data: field_data,
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
                ],
      hoverOffset: 6
    }]
  };
 
  var config = {
    type: 'doughnut',
    data: data,
    options:{
      maintainAspectRatio: false,
      plugins:{
        legend:{
          display:true,
          position:'top',
          labels:{
            font:{
              size:15
            }
          }
        },
        tooltip:{
          bodyFont:{
            size:14,
          }
        }
      }
  
    }
  };

  var myChart = new Chart(
    document.getElementById('field-piechart'),
    config
  );


