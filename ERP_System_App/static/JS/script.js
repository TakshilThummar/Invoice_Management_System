/*  ========================================================  Password Show and Hide Start  ========================================================  */

document.getElementById('toggle_password').addEventListener('click', function() {
    const passwordField = document.getElementById('password');
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);

    this.src = type === 'password' ?
        'https://img.icons8.com/material-outlined/24/000000/visible.png' :
        'https://img.icons8.com/material-outlined/24/000000/invisible.png';
});

document.getElementById('toggle_confirm_password').addEventListener('click', function() {
    const confirmPasswordField = document.getElementById('confirm_password');
    const type = confirmPasswordField.getAttribute('type') === 'password' ? 'text' : 'password';
    confirmPasswordField.setAttribute('type', type);

    this.src = type === 'password' ?
        'https://img.icons8.com/material-outlined/24/000000/visible.png' :
        'https://img.icons8.com/material-outlined/24/000000/invisible.png';
});

/*  ========================================================  Password Show and Hide End  ========================================================  */

/*  ========================================================  Alert Message Start  ========================================================  */

document.addEventListener('DOMContentLoaded', function() {
    var messagesElement = document.getElementById('messages');

    if (messagesElement) {
        var messages = messagesElement.getAttribute('data-messages');

        if (messages) {
            var messageArray = messages.split('|');

            messageArray.forEach(function(message) {
                alert(message); // Display each message as an alert box
            });
        }
    }
});

/*  ========================================================  Alert Message End  ========================================================  */

/*  ========================================================  Search Method Start  ========================================================  */

function filterTable() {
    let billNumberInput = document.getElementById("search_bill_number").value.toUpperCase();
    let customerNameInput = document.getElementById("search_customer_name").value.toUpperCase();
    let dateInput = document.getElementById("search_date").value;
    let productNameInput = document.getElementById("search_product_name").value.toUpperCase();

    let table = document.getElementById("billTable");
    let rows = table.getElementsByClassName("bill-search-table-raw-details");

    for (let i = 0; i < rows.length; i++) {
        let tdBillNumber = rows[i].getElementsByTagName("h5")[1];
        let tdCustomerName = rows[i].getElementsByTagName("h5")[2];
        let tdDate = rows[i].getElementsByTagName("h5")[4];
        let tdProductName = rows[i].getElementsByTagName("h5")[5];

        if (tdBillNumber && tdCustomerName && tdDate && tdProductName) {
            let billNumberValue = tdBillNumber.textContent || tdBillNumber.innerText;
            let customerNameValue = tdCustomerName.textContent || tdCustomerName.innerText;
            let dateValue = tdDate.textContent || tdDate.innerText;
            let productNameValue = tdProductName.textContent || tdProductName.innerText;

            let parsedDateValue = new Date(dateValue);
            let parsedDateInput = new Date(dateInput);

            // Ensure the date is valid
            if (isNaN(parsedDateValue.getTime())) {
                rows[i].style.display = "none";
                continue;
            }

            if (
                billNumberValue.toUpperCase().indexOf(billNumberInput) > -1 &&
                customerNameValue.toUpperCase().indexOf(customerNameInput) > -1 &&
                (!dateInput || parsedDateValue.toDateString() === parsedDateInput.toDateString()) &&
                productNameValue.toUpperCase().indexOf(productNameInput) > -1
            ) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}

/*  ========================================================  Search Method End  ========================================================  */

/*  ========================================================  Auto Fill Amount Start  ========================================================  */

/*document.getElementById('billForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    // Gather form data
    const formData = new FormData(this);

    // Simulate form submission
    fetch('/generate/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('message').innerText = 'Bill generated successfully!';
                document.getElementById('error').style.display = 'none';
            } else {
                document.getElementById('error').innerText = 'Error generating bill: ' + data.error;
                document.getElementById('error').style.display = 'block';
                document.getElementById('message').style.display = 'none';
            }
        })
        .catch(error => {
            document.getElementById('error').innerText = 'Network error: ' + error;
            document.getElementById('error').style.display = 'block';
            document.getElementById('message').style.display = 'none';
        });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}*/

/*  ========================================================  Auto Fill Amount End  ========================================================  */

/*  ========================================================  Validater Start  ========================================================  */

function validateNumber(field) {
    const errorElement = document.getElementById(field.id + '_error');
    if (/[^0-9]/.test(field.value)) {
        errorElement.textContent = "Only Numbers Are Allowed...";
        errorElement.style.display = 'block';
    } else {
        errorElement.style.display = 'none';
    }
}

function validateCharacterWithSpaces(field) {
    const errorElement = document.getElementById(field.id + '_error');
    if (/[^a-zA-Z\s]/.test(field.value)) {
        errorElement.textContent = "Only Characters Are Allow...";
        errorElement.style.display = 'block';
    } else {
        errorElement.style.display = 'none';
    }
}

function validateProduct(field) {
    const errorElement = document.getElementById(field.id + '_error');
    errorElement.style.display = 'none'; // All values are allowed for product name
}

function updateFlag(selectElement) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const flagUrl = selectedOption.getAttribute('data-flag');
    document.getElementById('country_flag').src = flagUrl;
}

function validatePhoneNumber(field) {
    const errorElement = document.getElementById(field.id + '_error');
    const countryCode = document.getElementById('country_code').value;
    let regex;

    if (countryCode === '+91') {
        regex = /^[0-9]{10}$/;
    } else if (countryCode === '+1') {
        regex = /^[0-9]{10}$/;
    } else if (countryCode === '+100') {
        regex = /^[0-9]{7,10}$/; // Example for custom country
    }

    if (!regex.test(field.value)) {
        errorElement.textContent = "Invalid Phone Number For The Selected Country...";
        errorElement.style.display = 'block';
    } else {
        errorElement.style.display = 'none';
    }
}

function validateForm() {
    const fields = ['bill_number', 'customer_name', 'customer_number', 'quantity', 'price', 'tax', 'total'];
    let valid = true;

    fields.forEach(function(field) {
        const element = document.getElementById(field);
        const errorElement = document.getElementById(field + '_error');

        if (element.value.trim() === "") {
            errorElement.textContent = "Blank Space is Not Allowed...";
            errorElement.style.display = 'block';
            valid = false;
        } else if (errorElement.style.display === 'block') {
            valid = false;
        } else {
            errorElement.style.display = 'none';
        }
    });

    if (valid) {
        alert('Form submitted successfully!');
    } else {
        alert('Please fix the errors in the form.');
    }
}

function submitForm() {
    var billNumber = document.getElementById('bill_number').value;
    var customerName = document.getElementById('customer_name').value;
    var customerNumber = document.getElementById('customer_number').value;
    var product = document.getElementById('product').value;
    var quantity = document.getElementById('quantity').value;
    var price = document.getElementById('price').value;

    var valid = true;

    valid &= validateField('bill_number', billNumber, true, false);
    valid &= validateField('customer_name', customerName, false, true);
    valid &= validateField('customer_number', customerNumber, true, false);
    valid &= validateField('product', product, false, true);
    valid &= validateField('quantity', quantity, true, false);
    valid &= validateField('price', price, true, false);

    if (valid) {
        calculate();
        var speech = new SpeechSynthesisUtterance("Bill Generated Successfully..., Thank You.");
        window.speechSynthesis.speak(speech);
        alert("Bill Generated Successfully..., Thank You.");
    }
}

// Default today's date for bill_date
document.getElementById('bill_date').valueAsDate = new Date();

/*  ========================================================  Validater End  ========================================================  */

function speakMessage(message) {
    const msg = new SpeechSynthesisUtterance(message);
    // Optionally, you can set the voice to a female voice if available
    const voices = window.speechSynthesis.getVoices();
    const femaleVoice = voices.find(voice => voice.name.includes('Female')) || voices[0];
    msg.voice = femaleVoice;
    window.speechSynthesis.speak(msg);
}

function validateNumber(field) {
    const errorElement = document.getElementById(field.id + '_error');
    const value = field.value.trim();

    if (/[^0-9]/.test(field.value)) {
        errorElement.textContent = "Only Numbers Are Allowed...";
        errorElement.style.display = 'block';
    } else if (field.id === 'quantity' || field.id === 'price') {
        // For quantity and price, check for 0
        if (value == 0 || value === '') {
            errorElement.textContent = "0 Or Blank Space are not allowed.";
            errorElement.style.display = 'block';
        } else {
            errorElement.style.display = 'none';
        }
    } else {
        errorElement.style.display = 'none';
    }
}

function validateCharacterWithSpaces(field) {
    const errorElement = document.getElementById(field.id + '_error');
    if (/[^a-zA-Z\s]/.test(field.value)) {
        errorElement.textContent = "Only Characters Are Allow...";
        errorElement.style.display = 'block';
    } else {
        errorElement.style.display = 'none';
    }
}

function validateProduct(field) {
    const errorElement = document.getElementById(field.id + '_error');
    errorElement.style.display = 'none'; // All values are allowed for product name
}

function updateFlag(selectElement) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const flagUrl = selectedOption.getAttribute('data-flag');
    document.getElementById('country_flag').src = flagUrl;
}

function validatePhoneNumber(field) {
    const errorElement = document.getElementById(field.id + '_error');
    const countryCode = document.getElementById('country_code').value;
    let regex;

    if (countryCode === '+91') {
        regex = /^[0-9]{10}$/;
    } else if (countryCode === '+1') {
        regex = /^[0-9]{10}$/;
    } else if (countryCode === '+100') {
        regex = /^[0-9]{7,10}$/; // Example for custom country
    }

    if (!regex.test(field.value)) {
        errorElement.textContent = "Invalid Phone Number For The Selected Country...";
        errorElement.style.display = 'block';
    } else {
        errorElement.style.display = 'none';
    }
}

function validateForm() {
    const fields = ['bill_number', 'customer_name', 'customer_number', 'quantity', 'price', 'tax', 'total'];
    let valid = true;

    fields.forEach(function(field) {
        const element = document.getElementById(field);
        const errorElement = document.getElementById(field + '_error');

        if (element.value.trim() === "") {
            errorElement.textContent = "Blank Space is Not Allowed...";
            errorElement.style.display = 'block';
            valid = false;
        } else if (errorElement.style.display === 'block') {
            valid = false;
        } else {
            errorElement.style.display = 'none';
        }
    });

    if (valid) {
        //alert("Form submitted successfully!");
        speakMessage("Bill Generated Successfully! Thank You...")
            // Optionally, submit the form data here.
    } else {
        //alert("Please correct the errors and try again.");
        speakMessage("Please Correct The Errors And Try Again.")
    }
}

function calculateTotals() {

    const quantity = parseFloat(document.getElementById('quantity').value) || 0;
    const price = parseFloat(document.getElementById('price').value) || 0;
    const taxRate = 0.18;
    const totalElement = document.getElementById('total');
    const taxElement = document.getElementById('tax');

    if (quantity > 0 && price > 0) {
        const tax = quantity * price * taxRate;
        const total = (quantity * price) + tax;

        taxElement.value = tax.toFixed(2);
        totalElement.value = total.toFixed(2);
    } else {
        taxElement.value = '';
        totalElement.value = '';
    }
}

/*function submitForm() {
    var billNumber = document.getElementById('bill_number').value;
    var customerName = document.getElementById('customer_name').value;
    var customerNumber = document.getElementById('customer_number').value;
    var product = document.getElementById('product').value;
    var quantity = document.getElementById('quantity').value;
    var price = document.getElementById('price').value;

    var valid = true;

    valid &= validateField('bill_number', billNumber, true, false);
    valid &= validateField('customer_name', customerName, false, true);
    valid &= validateField('customer_number', customerNumber, true, false);
    valid &= validateField('product', product, false, true);
    valid &= validateField('quantity', quantity, true, false);
    valid &= validateField('price', price, true, false);

    if (valid) {
        calculate();
        var speech = new SpeechSynthesisUtterance("Bill Generated Successfully..., Thank You.");
        window.speechSynthesis.speak(speech);
        alert("Bill Generated Successfully..., Thank You.");
    }
}*/

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast show';
    setTimeout(() => {
        toast.className = toast.className.replace('show', '');
    }, 3000);
}

// Default today's date for bill_date
document.getElementById('bill_date').valueAsDate = new Date();