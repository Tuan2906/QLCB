
function baoLoi(){
    var a=document.getElementById("email");
    var loi1="",loi2="";
    if(a.value==""){
        loi1="ban can nhap email";
    }
    else if (a.value.slice(-10)!="@gmail.com"){ // cắt từ vị trí -10 trong a.value
        loi1="vui long nhap dung dinh dang email"
    }
    var b=document.getElementById("Password");
    if(b.value==""){
        loi2="ban can nhap password";
    }
    else if (b.value.length > 7){
        loi2="quá số kí tự, vui lòng nhập < 7";
    }
    if(loi1=="" && loi2==""){
       var load=document.getElementById("load"); // hinh load
       load.style.display="block"; // hình load xuất hiện
       var around= document.getElementById("around") // nền 
       around.style.display="block" // nền hiện 
       around.style.backgroundColor="rgba(0,0,0,.5)" // thiết lập nền đen
        return true; 
    }
    if(loi1!=""){
        var c=document.getElementById("baoloi1");
        c.value=loi1;
        c.style.color="red";
    }
    if(loi2!=""){
        var d=document.getElementById("baoloi2");
        d.value=loi2;
        d.style.color="red"; 
    }
}
function timeOut(){
    if(baoLoi()==true){
        setTimeout(function(){
            alert("đăng nhập thành công");
            window.location.assign("http://127.0.0.1:5501/html/trang2.html"); // chuyển đến trang đăng nhập
        },3000)
    }
}
function showPass (obj){
    var icon=document.getElementById("icon");
    var pass=document.getElementById("Password");
    var a=icon.getAttribute("class"); 
    if(a=="fa-solid fa-eye-slash"){ // neu mat ẩn
        icon.className="fa-solid fa-eye"
        pass.setAttribute("type","text");
        pass.setAttribute("placeholder","Password");
        // -> mat thấy
    }
    else{
        icon.className="fa-solid fa-eye-slash"
        pass.setAttribute("type","PASSWORD"); // đổi loại
        pass.setAttribute("placeholder","Password");
    }
}
//window.onpopstate = function(event) {
//    // Kiểm tra xem người dùng có thực hiện hành động "Go back" hay không
//    alert('le')
//    if (event){
//        // Gửi yêu cầu đến server để đăng xuất người dùng
//        var xhr = new XMLHttpRequest();
//        xhr.open('GET', '/logout', true); // Thay đổi đường dẫn và phương thức tùy theo cấu hình logout của Flask
//        xhr.send();
////
////        xhr.onreadystatechange = function() {
////            if (xhr.readyState === XMLHttpRequest.DONE) {
////                if (xhr.status === 200) {
////                    console.log('Đã đăng xuất');
////                    // Xử lý các hành động khác sau khi đăng xuất thành công
////                } else {
////                    console.error('Lỗi khi đăng xuất');
////                }
////            }
////        };
//    }
//    // Sau khi xử lý đăng xuất, bạn có thể chuyển người dùng đến trang nào đó
//    // window.location.href = '/somepage';
//};