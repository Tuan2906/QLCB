

function toggleVisibilityInfomationFlight() {
    var maDatCho = document.getElementById("txt-madatcho").value;
    if (maDatCho) {
        var InforFlight = document.getElementById("InformationFlight");
        if (InforFlight.style.display === "block") {
            InforFlight.style.display = "none";
            showInputValue();
        } else {
            InforFlight.style.display = "block";
        }
    }
    else {
        alert("Vui lòng nhập đủ thông tin.");
    }
}

function showInputValue() {
    // Lấy giá trị từ input
    var lastName = document.getElementById("txt-lastname").value;
    var firstName = document.getElementById("txt-firstname").value;
    document.getElementById("fullname").innerHTML = lastName + ", " + firstName;

    var maDatCho = document.getElementById("txt-madatcho").value;
    document.getElementById("show-madatcho").innerHTML = maDatCho;
}


function get_id_MB(id_lb,id_mb, macb, noidi, noiden, NgayKhoiHanh, ThoiGianBay) {
    fetch('/api/MayBay', {
        method: "POST", // Sửa thành phương thức POST
        body: JSON.stringify({
            "MaLB":id_lb,
            "MaMB": id_mb,
            "MaCB": macb,
            "noidi":noidi,
            "noiden":noiden,
            "NgayKhoiHanh": NgayKhoiHanh,
            "ThoiGianBay": ThoiGianBay
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        console.info(data)
    })
}

