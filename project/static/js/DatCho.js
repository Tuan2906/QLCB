var clickCount = 0;

function rgbToHex(rgb) {
  // Chia chuỗi RGB thành các giá trị màu đỏ, xanh lá, và xanh lam
  let [r, g, b] = rgb.match(/\d+/g);

  // Chuyển đổi các giá trị màu từ dạng chuỗi sang số nguyên
  r = parseInt(r);
  g = parseInt(g);
  b = parseInt(b);

  // Chuyển đổi thành mã màu hex và viết thường
  let hex = "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toLowerCase();

  return hex; // Trả về mã màu hex viết thường
}


function changeColor(button,soluongkh, hangve) {
    if (button.classList.contains('selected')) {
        button.classList.remove('selected'); // Nếu có rồi, xóa lớp 'selected'
        clickCount--;
    } else {
        backColor =  button.style.backgroundColor
        if(backColor == 'rgb(108, 92, 231)' && hangve == 2) {
            alert('Bạn không thể chọn ghế này')
            return
        }
        if (clickCount < soluongkh) {
            button.classList.add('selected'); // Nếu chưa có, thêm lớp 'selected'
            clickCount++;
        } else {
            alert('Bạn đã chọn quá '+soluongkh+' chỗ ngồi.');
        }
    }
}
function checkAndPay(button,soluongkh) {
    // Thêm các nút có class "selected" vào mảng và áp dụng màu đỏ
    var selectedButtons = document.querySelectorAll('.common.selected');
 var selectedChairs = document.querySelectorAll('.table > tbody > tr > td:nth-child(4) >input');// tra ve mang ghe da chon
    if (selectedButtons.length == soluongkh) {
        var confirmed = confirm('Bạn có thực sự không muốn thay đổi vị trí?');
        var i = 0;
        if (confirmed) {
            // Thực hiện thanh toán
            selectedButtons.forEach(button => {
                button.style.setProperty('background', 'red', 'important');
                    console.log ("buton dc chon" + button.id)
                   if(button.id.length ==4){
                        console.log('vo if')
                       selectedChairs[i].value = button.id.slice(1,3);
                   }
                   else {
                         console.log('vo else')

                       selectedChairs[i].value = button.id.slice(1,4);
                   }
                i++;
                button.disabled = true;
            });
            var confirmFlight = document.getElementById('conf');
            confirmFlight.style.display =  'block';
        }
    } else {
        alert('Vui lòng chọn ' + soluongkh +  ' chỗ ngồi trước khi xác nhận chổ ngồi.');
    }
};
function ChuyenMauGhe() {
    fetch('/api/ghe').then(res => res.json()).then(data => {
        var ghe_btns =  document.querySelectorAll('.common');
        for (let dt of data){
            ghe_btns.forEach(ghe_btn => {
                console.log(ghe_btn.id)
                console.log(ghe_btn.id.length)

                if(dt.soghe == ghe_btn.id.slice(1,3) && ghe_btn.id.length==4){
                    ghe_btn.style.backgroundColor = 'red';
                    ghe_btn.disabled = true;
                }
                if(dt.soghe == ghe_btn.id.slice(1,4) && ghe_btn.id.length>4){
                    ghe_btn.style.backgroundColor = 'red';
                    ghe_btn.disabled = true;
                }
            });
        }
    });
}
//     // Lưu trạng thái (màu đỏ) vào localStorage để giữ nguyên khi load lại trang
//     localStorage.setItem('confirmedSeats', JSON.stringify(selectedSeats));
//     // Kiểm tra xem có dữ liệu đã lưu trước đó hay không
// var storedSeats = localStorage.getItem('confirmedSeats');
// if (storedSeats) {
//     // Parse dữ liệu từ JSON
//     selectedSeats = JSON.parse(storedSeats);

//     // Áp dụng màu đỏ cho các nút trong mảng khi load lại trang
//     selectedSeats.forEach(seat => {
//         var seatButton = document.querySelector('.common:contains("' + seat + '")');
//         if (seatButton) {
//             // Áp dụng màu đỏ trực tiếp
//             seatButton.style.backgroundColor = 'red';
//         }
//     });
// }

function Load_ghe(id_mb){
     fetch('/api/DatCho', {
            method: "post",
            body: JSON.stringify({
                "MaMB": id_mb
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json();
        }).then(function(data) {


        })
}

function ChuyenMauGhe_ThuongGia(){
    fetch('/api/thuonggia').then(res => res.json()).then(data => {
        var ghe_btns =  document.querySelectorAll('.ghe');
        for (let dt of data){
            ghe_btns.forEach(ghe_btn => {

                if(dt.Day + dt.Ghe == ghe_btn.id.slice(1,3) && ghe_btn.id.length==4){

                        ghe_btn.style.backgroundColor = '#6c5ce7';
                }
            });
        }
    });
}