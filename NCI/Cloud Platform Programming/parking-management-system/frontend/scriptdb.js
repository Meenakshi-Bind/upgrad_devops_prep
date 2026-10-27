// scriptdb.js - Updated
const API_BASE = 'http://your-domain.com/api';

// Add login functionality
async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        return await response.json();
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, message: 'Login failed' };
    }
}

// Update submit event listener
submit.addEventListener("click", async function(){
    let VehicleType = document.querySelector("select#cars");
    let VehicleNo = document.querySelector("input#VehicleNo");
    let phone = document.querySelector("input#Phoneno");
    let VehicleModel = document.querySelector("input#VehicleModel");
    let customer = document.querySelector("input#CustomerName");
    
    try {
        const response = await fetch(`${API_BASE}/check-in/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                vehicle_number: VehicleNo.value,
                vehicle_type: VehicleType.value,
                vehicle_model: VehicleModel.value,
                customer_name: customer.value,
                phone_number: phone.value
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            popup.style.display = "none";
            block.style.removeProperty("display");
            window.location.reload();
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Check-in error:', error);
        alert('Check-in failed');
    }
});