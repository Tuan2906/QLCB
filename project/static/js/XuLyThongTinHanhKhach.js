var dem=0
function layid(obj){
         value = obj.value;
         if(value!==null)
         {


                 var option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                var select = document.getElementById('nglondicung');
                if(select !== null)
                {
                   select.appendChild(option);
                   dem++;
                }
         }
        // Lấy giá trị của ô text box

        // Tạo một tùy chọn mới

 }



var check_cccd=flag_CCDD=flag_NgsinhNgl=flag_ngsinhTreEm=flag_email=flag_sdt=true
function check_TT() {
    // Nếu dữ liệu hợp lệ, thì cho phép gửi biểu mẫu

    if (check_cccd == true && flag_CCDD == true && flag_ngsinhTreEm == true && flag_NgsinhNgl==true && flag_email==true && flag_sdt==true) {
      checktrung_CCCD()
      return true;
     } else {
          if (check_cccd==false)
          {
            checktrung_CCCD();
          }
       alert("Vui lòng kiểm tra lại thông tin nãy thông báo trước và sửa lại")
       event.preventDefault();
      return false;
    }

 }
function checktrung_CCCD() {
  const inputs = document.querySelectorAll(".CCCD");
   for ( i = 0; i< inputs.length; i++) {
           if (inputs[i].value === inputs[i+1].value)
           {

               alert("CCCD không đươc trùng nhau")
                check_cccd=false
                event.preventDefault();


           }
           else
           {
             check_cccd=true
           }
     }
}
function check_CCCD(obj)
{
  var so = /^[0-9]+$/
   if(obj.value.length <12)
   {
     alert("Vui lòng nhập CCCD đủ 12 số ")
       flag_CCDD=false
   }
   else if(obj.value.length > 12)
   {
      alert("Vui lòng kiểm tra lại CCCD")
      flag_CCDD= false
   }
   else if(so.test(obj.value)==false)
   {
      alert("Vui lòng kiểm tra lại CCCD không phải là chữ")
      flag_CCDD= false
   }
   else
   {
    flag_CCDD=true
   }
}

 var today = new Date();
 var namHienTai = today.getFullYear();
function checkNgaySinhNguoiLon(obj){
    var namsinh = obj.value.split("-")[0];
    var tuoi = namHienTai - namsinh
      if (tuoi < 6){
        alert("Người lớn phải trên 6 tuổi!");
         flag_NgsinhNgl=false
      }
      else{
        flag_NgsinhNgl=true
      }
}
function checkNgaySinhTreEm(obj)
{
      var namsinh = obj.value.split("-")[0];
      var tuoi = namHienTai - namsinh
      if (tuoi > 6){
        alert(" Trẻ em phải dưới 6 tuổi!");
        flag_ngsinhTreEm= false
      }
      else{
        flag_ngsinhTreEm=true
      }
}
function checkEmail(obj)
{
  // Biểu thức chính quy để xác định định dạng email
  var mail = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/;
  // Kiểm tra email có khớp với biểu thức chính quy hay không
  if(mail.test(obj.value)==false)
  {
    alert("Vui lòng nhập email cho đúng")
    flag_email=false
  }
  else{
    flag_email=true
  }
}
function checkSDT(obj)
{
  var so = /^[0-9]+$/
   if(obj.value.length <10)
   {
     alert("Vui lòng nhập SĐT đủ 10 số ")
       flag_sdt=false
   }
   else if(obj.value.length > 11)
   {
      alert("Vui lòng kiểm tra lại SĐT")
      flag_sdt= false
   }
   else if(so.test(obj.value)==false)
   {
      alert("Vui lòng kiểm tra lại SĐT không phải là chữ")
      flag_sdt= false
   }
   else
   {
    flag_sdt=true
   }
}