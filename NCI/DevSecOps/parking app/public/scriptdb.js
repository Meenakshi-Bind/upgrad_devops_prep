let pay = document.querySelector(".PaymentDone");
let btn = document.querySelector("button.addContent");
let block = document.querySelector(".block");
let submit = document.querySelector(".submit");
let aftercheckout = document.querySelector(".afterCheckOut");
let popup = document.querySelector(".popCheckIn");
let currentCheckoutId = null;

const API_BASE = 'http://localhost:3010/api';

btn.addEventListener("click", function() {
    block.style.display = "none";
    popup.style.removeProperty("display");
});

submit.addEventListener("click", function() {
    let VehicleType = document.querySelector("select#cars").value;
    let VehicleNo = document.querySelector("input#VehicleNo").value;
    let phone = document.querySelector("input#Phoneno").value;
    let VehicleModel = document.querySelector("input#VehicleModel").value;
    let customer = document.querySelector("input#CustomerName").value;

    if (!VehicleNo || !VehicleType || !VehicleModel || !phone || !customer) {
        alert("Please fill all fields");
        return;
    }

    checkInVehicle(VehicleType, VehicleNo, customer, phone, VehicleModel);
});

function checkInVehicle(vehicleType, vehicleNo, customer, phone, vehicleModel) {
    fetch(`${API_BASE}/vehicles/checkin`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            vehicleNumber: vehicleNo,
            vehicleType: vehicleType,
            vehicleModel: vehicleModel,
            customerName: customer,
            phoneNumber: phone
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Vehicle checked in successfully!');
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error checking in vehicle');
    });
}

function fetchVehicles() {
    fetch(`${API_BASE}/vehicles`)
    .then(response => response.json())
    .then(data => {
        const vehicles = data.data || [];
        displayVehicles(vehicles);
    })
    .catch(error => {
        console.error('Error fetching vehicles:', error);
    });
}

function displayVehicles(vehicles) {
    let table = document.querySelector(".table");
    table.innerHTML = `
        <tr>
            <th>Vehicle No</th>
            <th>Vehicle Model</th>
            <th>Vehicle Type</th>
            <th>Phone</th>
            <th>Check-in</th>
            <th></th>
        </tr>
    `;

    vehicles.forEach(vehicle => {
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${vehicle.vehicle_number}</td>
            <td>${vehicle.vehicle_model}</td>
            <td>${vehicle.vehicle_type}</td>
            <td>${vehicle.phone_number}</td>
            <td>${new Date(vehicle.checkin_time).toLocaleString()}</td>
            <td><button class="buttonOut" data-id="${vehicle.id}"><i class="fas fa-minus"></i>Check-Out</button></td>
        `;
        table.appendChild(row);
    });

    attachCheckoutListeners();
}

function attachCheckoutListeners() {
    let checkoutButtons = document.querySelectorAll("button.buttonOut");
    checkoutButtons.forEach(button => {
        button.addEventListener("click", function(e) {
            const vehicleId = this.getAttribute('data-id');
            showCheckoutPopup(vehicleId);
        });
    });
}

function showCheckoutPopup(vehicleId) {
    currentCheckoutId = vehicleId;
    aftercheckout.style.removeProperty("display");
    block.style.display = "none";
    
    fetch(`${API_BASE}/vehicles`)
        .then(response => response.json())
        .then(data => {
            const vehicle = data.data.find(v => v.id == vehicleId);
            if (vehicle) {
                updateCheckoutDisplay(vehicle);
            }
        });
}

function updateCheckoutDisplay(vehicle) {
    let table2 = document.querySelector(".popCheckOut");
    let table3 = document.querySelector(".popCheckOut2");
    
    table2.innerHTML = `
        <th>Customer Name</th>
        <th>Phone Number</th>
        <th>Vehicle Number</th>
        <th>Vehicle Model</th>
    `;
    
    table3.innerHTML = `
        <th>Vehicle Type</th>
        <th>Check-in Time</th>
        <th>Check-out Time</th>
        <th>Duration</th>
    `;
    
    let row2 = document.createElement("tr");
    row2.innerHTML = `
        <td>${vehicle.customer_name}</td>
        <td>${vehicle.phone_number}</td>
        <td>${vehicle.vehicle_number}</td>
        <td>${vehicle.vehicle_model}</td>
    `;
    
    let row3 = document.createElement("tr");
    const checkoutTime = new Date().toLocaleString();
    const duration = Math.round((new Date() - new Date(vehicle.checkin_time)) / (1000 * 60 * 60));
    
    row3.innerHTML = `
        <td>${vehicle.vehicle_type}</td>
        <td>${new Date(vehicle.checkin_time).toLocaleString()}</td>
        <td>${checkoutTime}</td>
        <td>${duration} hrs</td>
    `;
    
    table2.appendChild(row2);
    table3.appendChild(row3);
}

let close = document.querySelector(".closeButton");
close.addEventListener("click", function() {
    pay.style.display = "none";
    block.style.removeProperty("display");
});

let buttonPro = document.querySelector("button.Pro");
buttonPro.addEventListener("click", function() {
    if (currentCheckoutId) {
        checkoutVehicle(currentCheckoutId);
    }
});

function checkoutVehicle(vehicleId) {
    fetch(`${API_BASE}/vehicles/checkout/${vehicleId}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(data => {
        aftercheckout.style.display = "none";
        pay.style.display = "";
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error during checkout');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fetchVehicles();
});