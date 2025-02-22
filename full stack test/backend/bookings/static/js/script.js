
let selectedTime = null;

async function fetchSlots() {
    const date = document.getElementById('booking-date').value;
    try {
        const response = await fetch(`/api/slots/?date=${date}`);
        const data = await response.json();
        displaySlots(data.slots);
    } catch (error) {
        showMessage("Error fetching slots", "red");
    }
}

function displaySlots(slots) {
    const container = document.getElementById('slots-container');
    container.innerHTML = slots.map(slot => 
        `<button class="slot" onclick="selectSlot('${slot}')">${slot}</button>`
    ).join('');
}

function selectSlot(time) {
    selectedTime = time;
    document.getElementById('booking-form').style.display = 'block';
}

async function bookSlot() {
    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value;
    const date = document.getElementById('booking-date').value;

    try {
        const response = await fetch('/api/book/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone, date, time: selectedTime }),
        });
        const result = await response.json();
        showMessage(result.status === 'success' ? '✅ Booking successful!' : '❌ Slot already booked!', 
                    result.status === 'success' ? 'green' : 'red');
    } catch (error) {
        showMessage("❌ Booking failed", "red");
    }
}

function showMessage(text, color) {
    const msgEl = document.getElementById('message');
    msgEl.textContent = text;
    msgEl.style.color = color;
}