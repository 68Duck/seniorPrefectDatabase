function exportTableToExcel(tableID, filename = '') {
    var downloadLink;
    var dataType = 'application/vnd.ms-excel';
    var tableSelect = document.getElementById(tableID);
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

    // Specify file name
    filename = filename ? filename + '.xls' : 'excel_data.xls';

    // Create download link element
    downloadLink = document.createElement("a");

    document.body.appendChild(downloadLink);

    if (navigator.msSaveOrOpenBlob) {
        var blob = new Blob(['\ufeff', tableHTML], {
            type: dataType
        });
        navigator.msSaveOrOpenBlob(blob, filename);
    } else {
        // Create a link to the file
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;
        // Setting the file name
        downloadLink.download = filename;

        //triggering the function
        downloadLink.click();
    }
}


var tableToExcel = (function() {
  var uri = 'data:application/vnd.ms-excel;base64,'
    , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>'
    , base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }
    , format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }
  return function(table, name) {
    if (!table.nodeType) table = document.getElementById(table)
    var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
    window.location.href = uri + base64(format(template, ctx))
  }
})()

//
// function tableItemClicked() {
//
// }
// $(function(){
//   $("td").click(function(event){
//     if($(this).children("input").length > 0)
//           return false;
//
//     var tdObj = $(this);
//     var preText = tdObj.html();
//     var inputObj = $("<input type='text' />");
//     tdObj.html("");
//
//     inputObj.width(tdObj.width())
//             .height(tdObj.height())
//             .css({border:"0px",fontSize:"17px"})
//             .val(preText)
//             .appendTo(tdObj)
//             .trigger("focus")
//             .trigger("select");
//
//     inputObj.keyup(function(event){
//       if(13 == event.which) { // press ENTER-key
//         var text = $(this).val();
//         tdObj.html(text);
//       }
//       else if(27 == event.which) {  // press ESC-key
//         tdObj.html(preText);
//       }
//     });
//
//     inputObj.click(function(){
//       return false;
//     });
//   });
// });

// getTableInformation();
// fetch("/")
//   .then(function getTableInformation () {
//     var table = document.getElementById("table")
//     var tableHTML = table.outerHTML
//     var rows = new Array()
//     // console.log(table)
//     table.querySelectorAll("tbody").forEach(tbody =>{
//       tbody.querySelectorAll("tr").forEach(tr =>{
//         var row = new Array()
//         tr.querySelectorAll("td").forEach(item =>{
//           row.push(item.innerHTML)
//           // console.log(item.innerHTML)
//         })
//         rows.push(row)
//       })
//     })
//     console.log(rows)
//     return rows
//   }).then(function (text) {
//           console.log('GET response:');
//           console.log(text);
//           return text
//       });

function addTableRow(){
  var table = document.getElementById("table")
  var tbody = table.querySelector("tbody")
  var count = 0
  var rowsCount = 1   // as the id starts at one
  var tr = tbody.querySelector("tr")
  tbody.querySelectorAll("tr").forEach(tr =>{
    rowsCount++
  })
  tr.querySelectorAll("td").forEach(td =>{
    count++
  })
  newRow = document.createElement("tr")
  for (var i=0;i<count;i++){
    newElement = document.createElement("td")
    if (i==0){
      newElement.innerHTML = rowsCount
    }
    newElement.setAttribute("contenteditable","true")
    newElement.setAttribute("name","tableItem")
    newElement.setAttribute("class",".tableItem")
    newRow.appendChild(newElement)
  }
  tbody.appendChild(newRow)
  sendPost()
}

const sendPost = async () => {
   const url = '/tableUpdate'; // the URL to send the HTTP request to
   const body = JSON.stringify(getTableInformation()); // whatever you want to send in the body of the HTTP request
   const headers = {'Content-Type': 'application/json'}; // if you're sending JSON to the server
   const method = 'POST';
   const response = await fetch(url, { method, body, headers });
   const data = await response.text(); // or response.json() if your server returns JSON
   // console.log(data);
}



function getTableInformation (){
  var table = document.getElementById("table")
  var tableHTML = table.outerHTML
  var rows = new Array()
  // console.log(table)
  table.querySelectorAll("tbody").forEach(tbody =>{
    tbody.querySelectorAll("tr").forEach(tr =>{
      var row = new Array()
      tr.querySelectorAll("td").forEach(item =>{
        row.push(item.innerHTML)
        // console.log(item.innerHTML)
      })
      rows.push(row)
    })
  })
  // console.log(rows)
  return rows
}


$(document).on('input','#table > tbody > tr > td',function(){
  sendPost()
})

function logTest(){
  console.log("test")
}



// addTableRow()
