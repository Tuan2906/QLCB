
$(document).ready(function(){
        // Số lượng người
      var adultNumber = parseInt($(".adult input").val())
      var childrenNumber = parseInt($(".children input").val())
      console.log(adultNumber)
        $(".adult .fa-minus").click(() => {
            if (adultNumber == 1) {

                return 0;
            }
            adultNumber = adultNumber - 1
            $(".adult input").val(adultNumber.toString())
        });
        $(".adult .fa-plus").click(() => {
            if (adultNumber + childrenNumber  == 9) {
                alert('Quá số lượng người đi')
                return 0;
            }
            adultNumber = adultNumber + 1
            $(".adult input").val(adultNumber.toString())
        });
        $(".children .fa-minus").click(() => {
            if (childrenNumber == 0) {
                return 0;
            }
            childrenNumber = childrenNumber - 1
            $(".children input").val(childrenNumber.toString())
        })
        $(".children .fa-plus").click(() => {
            if (adultNumber + childrenNumber == 9) {
                alert('Quá số lượng người đi')
                return 0
            }
            childrenNumber = childrenNumber + 1
            $(".children input").val(childrenNumber.toString())
        })

        // lịch
        $("#one-way").click(() => {
            if ($("#one-way").prop('checked') == true) {
                $("#EndDate").prop('disabled', true)
                $("#round-trip").prop('checked', false)
            } else {
                $("#one-way").prop('checked', true)
            }
        })
        $("#round-trip").click(() => {
        if ($("#round-trip").prop('checked') == true) {
            $("#EndDate").prop('disabled', false)
            $("#one-way").prop('checked', false)
        } else {
            $("#round-trip").prop('checked', true)
        }
    })
      var DateObject = new Date()
      DayofMonth = DateObject.getDate()
      Month = DateObject.getMonth();
       if (DayofMonth < 10) {
           DayofMonth = "0" + DayofMonth
       }
       Month = Month +1
       if (Month < 10) {
           Month = "0" + Month
       }
      var CurrentDate = DateObject.getFullYear() + "-" + Month + "-" + DayofMonth
  var SearchInfo = {}
$("#StartDate").val(CurrentDate)
$("#StartDate").attr('min', CurrentDate)
$("#SearchButton").click((e) => {
//    e.preventDefault()
    SearchInfo = {
        StartAirport: $("#StartAirport").val(),
        EndAirport: $("#EndAirport").val(),
        StartDate: $("#StartDate").val(),
        EndDate: $("#EndDate").val(),
        EndDate: $("#EndDate").val(),
        Adult: $(".adult span").text(),
        Children: $(".children span").text(),
        Level : $('#level').val()
    }
    if (SearchInfo.StartAirport == null || SearchInfo.EndAirport == null) {
        alert("Vui lòng nhập sân bay đi và sân bay đến")
         e.preventDefault()
    } else if ($("#round-trip").prop("checked") == true && SearchInfo.EndDate == '') {
        alert("Vui lòng chọn ngày về")
                 e.preventDefault()
    }else if(SearchInfo.Level == null){
        alert("Vui lòng chọn loại hạng")
                 e.preventDefault()
    }
//    else {
//        localStorage.setItem("SearchInfo", JSON.stringify(SearchInfo))
//        window.location.href = "flight-result.html" // chyuen sang trang khác
//    }
})
$("#round-trip").click(function () {
    $("#EndDate").val(CurrentDate)
    $("#EndDate").attr('min', CurrentDate)
})
$("#one-way").click(function () {
    $("#EndDate").val('')
})

});
function load_diadiem(){
    fetch('/api/diadiem').then(res => res.json()).then(data =>{
        selectDestinations = document.getElementsByClassName('Start');
        for(i = 0; i< selectDestinations.length ; i++){
            data.forEach(dt =>{
                selectDestinations[i].innerHTML +='<option value="' + dt.address +'">' + dt.address +'</option>';

            })
            selectDestinations[i].selectedIndex = -1;
        }
    })
}
function load_hangve(){
    fetch('/api/hangve').then(res => res.json()).then(data =>{
        selectTicketLevel = document.getElementById('level');
        console.log(selectTicketLevel)
        data.forEach(dt =>{
            selectTicketLevel.innerHTML +='<option value="' + dt.level +'">' + dt.level +'</option>';

        })
        selectTicketLevel.selectedIndex = -1;
    })
}
var selectStart = document.getElementById('StartAirport');
var selectEnd = document.getElementById('EndAirport');
selectEnd.addEventListener('change', function() {
    if(selectStart.value == selectEnd.value){
        alert("Vui lòng chọn điểm đến khác điểm đi")
        selectEnd.value = ""
    }

});
selectStart.addEventListener('change', function() {
    if(selectStart.value == selectEnd.value){
        alert("Vui lòng chọn điểm đến khác điểm đi")
        selectStart.value = ""
    }
});
