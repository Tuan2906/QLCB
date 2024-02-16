var clickCount = 0;
        
var data=[]

function add(){
    data.splice(0,data.length)
    $('.expand-btn').attr('disabled', false);
    var item_tuyenbay = document.getElementById("tuyenbay").selectedOptions[0].innerText
    var item_macb = document.getElementById("macb").value
    var item_ngaygiodi = document.getElementById("ngaygiodi").value
    var item_thoigian = document.getElementById("thoigian").value
    var item_maybay= document.getElementById("maybay").selectedOptions[0].innerText
    if (clickCount !== 0){
        var item_sanbay = document.getElementById("sanbay").value
        var item_thoigiandung = document.getElementById("thoigiandung").value
        var item_ghichu = document.getElementById("ghichu").value
    }else {
        var item_sanbay = ''
        var item_thoigiandung = ''
        var item_ghichu = ''
    }
    clickCount = 0

    
    var item = {
        tuyenbay: item_tuyenbay,
        macb: item_macb,
        tenmaybay: item_maybay,
        ngaygiodi: item_ngaygiodi,
        thoigian: item_thoigian,
        sanbay: item_sanbay,
        thoigiandung: item_thoigiandung,
        ghichu: item_ghichu
    }
    data.push(item)
    render()
    //clear()
    deleteItem()
    document.querySelector('.order-table').innerHTML = ''
}
function deleteRow(obj) {
  const table = document.querySelector("#render");
    const rows = document.querySelector(`.${obj.id}`); // Sử dụng querySelector với cú pháp class
    const tbody = rows.parentNode;
    tbody.remove(rows)


}
var isTableVisible = false;
orderTable = document.querySelector('.order-table')
addBtn = document.querySelector('.expand-btn')
addBtn.addEventListener('click', () => {
    clickCount++
    console.log(clickCount)
    if(clickCount === 1) {
        orderTable.innerHTML += `<table class="order-list">
                                        <thead>
                                            <tr>
                                                <th>Sân bay</th>
                                                <th>Thời gian dừng</th>
                                                <th>Ghi chú</th>
                                            </tr>
                                        </thead>
                                        <tbody class='order-body'>
                                            <tr>
                                                <td>
                                                    <select name="sanbay" id="sanbay" class = 'sanbay'>

                                                    </select>
                                                </td>
                                                <td><input type="number" name="thoigiandung1" id="thoigiandung" placeholder="Thời gian dừng" onblur="check(this)"></td>
                                                <td><input type="text" name="ghichu" id="ghichu" placeholder="Ghi chú"  style='color:black'></td>
                                            </tr>
                                        </tbody>
                                 </table>`
    }
    else if(clickCount <= quydinh.sanBayTG_ToiDa && clickCount > 1)  {  // cho nay kiem tra quy dinh co duoc vo khong
        document.querySelector('.order-body').innerHTML += `<tr>
        <td>
            <select name="sanbay" id="sanbay" class = 'sanbay'>

            </select>
        </td>
        <td><input type="number" name="thoigiandung2" id="thoigiandung" placeholder="Thời gian dừng" onblur="check(this)" ></td>
        <td><input type="text" name="ghichu" id="ghichu" placeholder="Ghi chú"  style='color:black'></td>
    </tr>`
//    $('.expand-btn').attr('disabled', true);
    }

    var listSanBay = document.getElementsByClassName('sanbay')
    for (let i = clickCount-1; i<listSanBay.length;i++){
        listsb.forEach(sb=>{
            console.log(sb)
            listSanBay[i].innerHTML +='<option value="' + sb.masb +'" class="p-3">' + sb.masb +'</option>';
        })
    }


})
function render(){
    var table = ``
    var newRow
    const tableData = [];
     for (const row of document.querySelector(".order-table").querySelectorAll("tr:not(:has(th))")) {
                tableData.push({
                    sanbay: row.querySelector("td > #sanbay").value,
                   thoigiandung: row.querySelector("td > #thoigiandung").value,
                    ghichu:row.querySelector("td > #ghichu ").value
                });
      }

      for(let i=0;i<data.length;i++){
         if(tableData.length >=2)
        {
           const extractedDate = data[i].ngaygiodi.substring(0, 10);
            str = "a" +  extractedDate
            console.log(typeof(str))
            table +=
                `<tr class=${str}>
                    <td rowspan="2">${data[i].tuyenbay}</td>
                    <td rowspan="2">${data[i].macb}</td>
                    <td rowspan="2">${data[i].tenmaybay}</td>
                    <td rowspan="2">${data[i].ngaygiodi}</td>
                     <td rowspan="2">${data[i].thoigian}</td>
                     <td>${tableData[i].sanbay}</td>
                     <td>${tableData[i].thoigiandung}</td>
                     <td>${tableData[i].ghichu}</td>
                     <td rowspan="2"><input type="button" id=${str} value="Xóa" onclick="deleteRow(this)"/></td>
                </tr>
                <tr class=${str}>
                     <td>${tableData[i+1].sanbay}</td>
                    <td>${tableData[i+1].thoigiandung}</td>
                    <td>${tableData[i+1].ghichu}</td>
                <tr>`
                 break;
          }
          else{
               const extractedDate = data[i].ngaygiodi.substring(0, 10);
                 str = "a" +  extractedDate
               if(tableData[0] !== undefined)
               {

                  table += `<tr class=${str}>
                                 <td>${data[i].tuyenbay}</td>
                                 <td>${data[i].macb}</td>
                                <td>${data[i].tenmaybay}</td>
                                 <td>${data[i].ngaygiodi}</td>
                                 <td>${data[i].thoigian}</td>
                                 <td>${tableData[i].sanbay}</td>
                                 <td>${tableData[i].thoigiandung}</td> <td>${tableData[i].ghichu}</td>
                                <td><input type="button" id=${str} value="Xóa" onclick="deleteRow(this)"/></td>
                              <tr>`
                           break;
               }
                else
                {
                   table += `<tr class=${str}>
                                <td>${data[i].tuyenbay}</td>
                                <td>${data[i].macb}</td>
                               <td>${data[i].tenmaybay}</td>
                                <td>${data[i].ngaygiodi}</td>
                                 <td style="width: 200px; white-space: nowrap;">${data[i].thoigian}</td>
                                 <td><td>
                                 <td></td>
                                 <td><input type="button" id=${str}  value="Xóa" onclick="deleteRow(this)"/></td>

                             <tr>`
                             break;
                }
             }
     }

       document.getElementById("render").innerHTML += table
       document.getElementById("xacnhan").style.display="block"

        // Reset bảng
         if(document.querySelector(".order-list") !== null)
         {
              document.querySelector(".order-list").remove()
          }
}
 function clear(){
     document.getElementById("tuyenbay").value="";
     document.getElementById("macb").value="";
     document.getElementById("ngaygiodi").value="";
     document.getElementById("thoigian").value="";

 }
 function addlaplich() {
     const tableData = [];
     var i=0;
     for (const rows of document.querySelectorAll(".table > tbody")) {
       for(const row of rows.querySelectorAll("tbody > tr:not(:has(th))"))
        {
             if( row.querySelector("td") != null)
             {
                   if(row.querySelectorAll("td").length !=3 || i ==0 )
                    {  tableData.push({
                            id_chuyenbay: row.querySelector("td").nextElementSibling.textContent,
                            maybay: row.querySelector("td").nextElementSibling.nextElementSibling.textContent,
                            ngaygiodi:row.querySelector("td").nextElementSibling.nextElementSibling.nextElementSibling.textContent,
                            thoigianbay: row.querySelector("td").nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.textContent,
                            sanbaybaytrunggian: row.querySelector("td").nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.textContent,
                            thoigiandung:row.querySelector("td").nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.textContent
                        });
                    }
                    else
                    {
                        tableData.push({
                           sanbaybaytrunggian: row.querySelector("td").textContent,
                            thoigiandung:row.querySelector("td").nextElementSibling.textContent
                        });
                    }
                 i++;
             }
         }
      }

    fetch('/api/laplich', {
        method: "post",
        body: JSON.stringify(tableData),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        console.info(data)
    })
}


var selectTuyen = document.getElementById('tuyenbay')
function load_Tuyen(){
    console.log('anc')
    fetch('/api/diadiem').then(res => res.json()).then(data =>{
        i = 0
        data.forEach(dt1 =>{
            data.forEach(dt2 =>{
                if (dt1 != dt2){
                    i++
                    selectTuyen.innerHTML +='<option value="' + i +'" class="p-3">' + dt1.address + '-' +dt2.address +'</option>';
                }

            })
        })
        selectTuyen.selectedIndex = -1;
    })
}

selectMaCB = document.getElementById('macb')
selectTuyen.addEventListener('change', function() {
      fetch('/api/timcb', {
            method: "POST",
            body: JSON.stringify({
                'tuyen': selectTuyen.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
            selectMaCB.options.length = 0;
            data.forEach(dt =>{
                selectMaCB.innerHTML +='<option value="' + dt.macb +'" class="p-3">' + dt.macb + '</option>';
            })
            selectMaCB.disabled = false;
        })
});

var selectMB = document.getElementById('maybay')
function load_maybay(){
    fetch('/api/maybay').then(res => res.json()).then(data =>{
        data.forEach(dt =>{
            selectMB.innerHTML +='<option value="' + dt.mamb +'">' + dt.tenmb +'</option>';
        })
        selectMB.selectedIndex = -1;
    })
}

var ghe1 = document.getElementById('soluongve1')
var ghe2 = document.getElementById('soluongve2')
selectMB.addEventListener('change', function() {
      fetch('/api/countghe', {
            method: "POST",
            body: JSON.stringify({
                'idmb': selectMB.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
            ghe1.value = data.hang1
            ghe2.value  = data.hang2
        })
});


var listsb = []
function load_sb(){
    fetch('/api/sanbay').then(res => res.json()).then(data =>{
        data.forEach(dt =>{
            listsb.push(dt)
        })
    })
}
var quydinh=''
function load_quydinh(){
    fetch('/api/quydinh').then(res => res.json()).then(data =>{
        quydinh = data
    })
}

function check (obj){
    if(obj.id == 'thoigiandung'){
        if(obj.value < quydinh.thoiGianDungToiThieu ||  obj.value > quydinh.thoiGianDungToiDa){
            alert('vui lòng nhập thời gian dừng từ '+  quydinh.thoiGianDungToiThieu + ' phút đến ' +  quydinh.thoiGianDungToiDa + ' phút')
            obj.value = quydinh.thoiGianDungToiThieu
        }

    }
    if(obj.id == 'thoigian'){
        if(obj.value < quydinh.thoiGianBayToiThieu){
           alert('vui lòng nhập thời gian bay từ ' + quydinh.thoiGianBayToiThieu + ' phút trở lên')
           obj.value = quydinh.thoiGianBayToiThieu
        }
    }
}

