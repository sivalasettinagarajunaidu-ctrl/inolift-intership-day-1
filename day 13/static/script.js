// ==================== Form Validation ====================
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateForm(formElement) {
    const name = formElement.querySelector('[name="name"]');
    const email = formElement.querySelector('[name="email"]');

    if (!name || !name.value.trim()) {
        alert('Please enter your name');
        return false;
    }

    if (!email || !email.value.trim()) {
        alert('Please enter your email');
        return false;
    }

    if (!validateEmail(email.value)) {
        alert('Please enter a valid email address');
        return false;
    }

    return true;
}

// ==================== Alert Handlers ====================
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Add form validation to health form
    const healthForm = document.getElementById('healthForm');
    if (healthForm) {
        healthForm.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    }
});

// ==================== Delete Confirmation ====================
function confirmDelete(recordName) {
    return confirm(`Are you sure you want to delete the record for ${recordName}?`);
}

// ==================== Table Sorting ====================
function sortTable(columnIndex, tableElement) {
    const table = tableElement || document.querySelector('.records-table');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aValue = a.children[columnIndex].textContent.trim();
        const bValue = b.children[columnIndex].textContent.trim();

        // Try to sort numerically if possible
        if (!isNaN(aValue) && !isNaN(bValue)) {
            return parseInt(aValue) - parseInt(bValue);
        }

        // Otherwise sort alphabetically
        return aValue.localeCompare(bValue);
    });

    rows.forEach(row => tbody.appendChild(row));
}

// ==================== Export Data ====================
function exportTableToCSV(filename, tableElement) {
    const table = tableElement || document.querySelector('.records-table');
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.textContent.replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });

    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename || 'export.csv';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// ==================== Search Functionality ====================
function searchTable(inputElement, tableElement) {
    const searchTerm = inputElement.value.toLowerCase();
    const table = tableElement || document.querySelector('.records-table');
    if (!table) return;

    const rows = table.querySelectorAll('tbody tr');
    let visibleRows = 0;

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
            visibleRows++;
        } else {
            row.style.display = 'none';
        }
    });

    // Update record count
    const recordCount = document.querySelector('.record-count');
    if (recordCount) {
        recordCount.textContent = `Showing ${visibleRows} record(s)`;
    }
}

// ==================== Print Functionality ====================
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write('<pre>');
    printWindow.document.write(element.innerHTML);
    printWindow.document.write('</pre>');
    printWindow.document.close();
    printWindow.print();
}

// ==================== Format Date ====================
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// ==================== Show Loading Spinner ====================
function showLoading(message = 'Loading...') {
    const loader = document.createElement('div');
    loader.className = 'loader';
    loader.innerHTML = `<p>${message}</p>`;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.remove();
    }
}

// ==================== Keyboard Shortcuts ====================
document.addEventListener('keydown', function(event) {
    // Alt + H: Go to Home
    if (event.altKey && event.key === 'h') {
        window.location.href = '/';
    }
    // Alt + R: Go to Register
    if (event.altKey && event.key === 'r') {
        window.location.href = '/register';
    }
    // Alt + L: Go to Records/List
    if (event.altKey && event.key === 'l') {
        window.location.href = '/records';
    }
    // Alt + S: Go to Statistics
    if (event.altKey && event.key === 's') {
        window.location.href = '/statistics';
    }
});

console.log('Diabetes Risk Predictor - Application Loaded');
