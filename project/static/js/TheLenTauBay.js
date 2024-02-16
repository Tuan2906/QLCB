function generateQR(soluong) {
    // Lấy giá trị từ các thẻ HTML\
    console.log(1)
    var txtName = document.getElementsByClassName("txtName");
    var txtDate = document.getElementById("txtDate");
    var txtFlight = document.getElementById("txtFlight");
    var txtBookingCode = document.getElementById("txtBookingCode");
    var txtHours = document.getElementById("txtHours");
    var txtChair = document.getElementsByClassName("txtChair");
    var txtSEQ = document.getElementsByClassName("txtSEQ");
    var txtRequest = document.getElementById("txtRequest");
    var txtSSR = document.getElementById("txtSSR");
    arrFullCode = []
    // Ghép chuỗi để tạo fullCode
    for (let i = 0; i<soluong;i++){
        arrFullCode[i] = "Họ và Tên: "+ txtName[i].innerText + ' \n' + "Ngày bay: "+ txtDate.innerText + ' \n' + "Số hiệu chuyến bay: "+txtFlight.innerText + ' \n' +"Mã đặt chỗ: "+ txtBookingCode.innerText + ' \n'
         +"Giờ đi : "+ txtHours.innerText + ' \n' +"Số ghế: "+ txtChair[i].innerText + ' \n' + "Mã vé: "+txtSEQ[i].innerText + ' \n' +"Hạng vé: "+ txtRequest.innerText + ' \n' +"Mã SSR: "+ txtSSR.innerText +'\n';
         console.log(arrFullCode[i])
    }


    // Sử dụng encodeURIComponent để chắc chắn các ký tự đặc biệt không làm hỏng URL
    var encodedData = encodeURIComponent(arrFullCode);

    // Đặt src cho thẻ img
    document.getElementById("qrCodeImage").src = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + encodedData;
}


function downloadConfirmationPage(soluong) {
      generateQR(soluong);
      window.print();
//    var htmlContent = document.documentElement.outerHTML;
//    var blob = new Blob([htmlContent], { type: 'text/html' });
//    var url = URL.createObjectURL(blob);
//
//    var a = document.createElement('a');
//    a.href = url;
//    a.download = 'TheLenTauBay.html';
//
//    document.body.appendChild(a);
//    a.click();
//
//    document.body.removeChild(a);
//
//    setTimeout(function() {
//    // Đóng trang web sau khi tải về
//    window.open('', '_self').close();
//    }, 0);

//    var element = document.documentElement;
//
//    // Sử dụng html2pdf để chuyển đổi và tải về dưới dạng PDF
//    html2pdf(element, {
//        margin: 10,
//        filename: 'TheLenTauBay.pdf',
//        image: { type: 'jpeg', quality: 0.98 },
//        html2canvas: { scale: 2 },
//        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
//    });


}