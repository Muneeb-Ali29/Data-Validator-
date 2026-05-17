document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const totalCount = document.getElementById('totalCount');
    const validCount = document.getElementById('validCount');
    const invalidCount = document.getElementById('invalidCount');
    const errorContainer = document.getElementById('errorContainer');
    const errorList = document.getElementById('errorList');

    // Handle click to browse
    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Handle drag and drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            if (file.name.endsWith('.json')) {
                handleFile(file);
            } else {
                alert('Please upload a valid JSON file.');
            }
        }
    });

    function handleFile(file) {
        // Show loading, hide results
        uploadZone.style.display = 'none';
        loading.classList.remove('hidden');
        results.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', file);

        fetch('/api/validate', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.detail || 'Validation failed') });
            }
            return response.json();
        })
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            alert(`Error: ${error.message}`);
            uploadZone.style.display = 'block';
            loading.classList.add('hidden');
        });
    }

    function displayResults(data) {
        loading.classList.add('hidden');
        results.classList.remove('hidden');
        uploadZone.style.display = 'block'; // Allow another upload

        // Animate counts
        animateValue(totalCount, 0, data.total, 1000);
        animateValue(validCount, 0, data.valid_count, 1000);
        animateValue(invalidCount, 0, data.invalid_count, 1000);

        if (data.invalid_count > 0) {
            errorContainer.classList.remove('hidden');
            errorList.innerHTML = '';
            
            data.errors.forEach(err => {
                const li = document.createElement('li');
                li.className = 'error-item';
                
                let detailsHtml = '';
                err.errors.forEach(detail => {
                    const fieldName = detail.loc.join('.');
                    detailsHtml += `<div class="error-details">• Field '<b>${fieldName}</b>': ${detail.msg}</div>`;
                });

                li.innerHTML = `
                    <div class="error-index">Product at Index ${err.index}</div>
                    ${detailsHtml}
                `;
                errorList.appendChild(li);
            });
        } else {
            errorContainer.classList.add('hidden');
        }
    }

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
});
