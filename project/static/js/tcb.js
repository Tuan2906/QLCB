const departureList = ["Hà Nội", "Đà Nẵng", "Thành phố Hồ Chí Minh", "Đà Lạt", "Hải Phòng", "Huế", "Hạ Long", "Vinh"];
var ticketTypes = ["Phổ thông", "Phổ thông đặc biệt", "Thương gia", "Hạng nhất"];


document.addEventListener("DOMContentLoaded", function () {
    findPlaces(departureList);
    ticketType(ticketTypes);
  });

// DS điểm đi
function findPlaces(departureList) {
  const destinationSearchInputs = document.querySelectorAll(".destination-search");
  const destinationLists = document.querySelectorAll(".destination-list");

  destinationSearchInputs.forEach((input, index) => {
      input.addEventListener("input", function () {
          const searchTerm = input.value.toLowerCase();
          displayDestination(searchTerm, index);
      });

      input.addEventListener("focus", function () {
          const searchTerm = input.value.toLowerCase();
          displayDestination(searchTerm, index);
      });
  });

  function displayDestination(searchTerm, index) {
      const filteredDestination = departureList.filter(country => country.toLowerCase().includes(searchTerm));
      const destinationList = destinationLists[index];
      destinationList.innerHTML = "";
      filteredDestination.forEach(country => {
          const listItem = document.createElement("li");
          listItem.textContent = country;
          listItem.addEventListener("click", function () {
              destinationSearchInputs[index].value = country;
              destinationList.style.display = "none";
          });
          destinationList.appendChild(listItem);
      });
      if (filteredDestination.length > 0) {
          destinationList.style.display = "block";
      } else {
          destinationList.style.display = "none";
      }
  }
};
// end danh sách điểm đi

// JS Loại vé
function ticketType(ticketTypes){
    const selectElement = document.querySelector(".form-select");
    ticketTypes.forEach((type) => {
    const option = document.createElement("option");
    option.textContent = type;
    selectElement.appendChild(option);
});
}

//function addFlight(id, name, price) {
//    fetch('/api/flight', {
//        method: "post",
//        body: JSON.stringify({
//            "id": id,
//            "name": name,
//            "price": price
//        }),
//        headers: {
//            'Content-Type': 'application/json'
//        }
//    }).then(function(res) {
//        return res.json();
//    }).then(function(data) {
//        console.info(data)
//    })
//}
// end js loại vé







