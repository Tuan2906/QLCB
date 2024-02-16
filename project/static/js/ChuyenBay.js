document.getElementById("next").addEventListener("click",()=>{
    var widthSlider = document.querySelector(".swiper-slide").offsetWidth;
    document.querySelector(".mySwiper").scrollLeft+=widthSlider;
})
document.getElementById("prev").addEventListener("click",()=>{
    var widthSlider = document.querySelector(".swiper-slide").offsetWidth;
    document.querySelector(".mySwiper").scrollLeft-=widthSlider;
})

//function LookLichBay(timeLich){
//    fetch('/api/lichbay',{
//        method: "POST",
//        body: JSON.stringify({
//            'time': timeLich
//        }),
//        headers: {
//            'Content-Type': 'application/json'
//        }
//    }).then(res => res.json()).then(data => {
//        console.log(data)
//    });
//}
function addFlight(malb, macb, ngaykhoihanh, noidi,noiden, tenMayBay ,totalprice) {

        fetch('/api/flight', {
            method: "post",
            body: JSON.stringify({
                "MaLB": malb,
                "MaCB": macb,
                "noidi": noidi,
                "noiden":noiden,
                'tenMB': tenMayBay,
                "NgayKhoiHanh":ngaykhoihanh,
                "Tongtien": totalprice
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
        })
}


function move (startDay){
    var widthSlider = document.querySelector(".swiper-slide").offsetWidth
    var pArr = document.querySelectorAll(".loadFlights p")
     var arr =  startDay.split("-");
    for (var i = 0; i <= pArr.length; i++) {
      var dateArr = pArr[i].textContent.split("/")
      if(arr[2] == dateArr[0] && arr[1] == dateArr[1] && arr[0] == dateArr[2]) {
        const today = new Date();
        const day = today.getDate();
        const month = today.getMonth() + 1;
        const year = today.getFullYear();
        var date1 = new Date(year + '-' + month + '-' + day)
        var date2 = new Date (dateArr.reverse().join('-'))
        const difference = date2 - date1;
        const distance = Math.round(difference / (1000 * 60 * 60 * 24));
        document.querySelector(".mySwiper").scrollLeft+= (widthSlider*distance);
         var colorSlider = document.querySelectorAll(".swiper-slide")[distance];
         colorSlider.style.backgroundColor = 'red'
      }
    }
}