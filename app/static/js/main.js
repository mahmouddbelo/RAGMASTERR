document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const urlForm = document.getElementById('urlForm');
    const queryForm = document.getElementById('queryForm');
    const answerDiv = document.getElementById('answer');
    const answerText = document.getElementById('answerText');

    function showAlert(message, type = 'success') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.row'));
        setTimeout(() => alertDiv.remove(), 5000);
    }

    function setLoading(form, isLoading) {
        const button = form.querySelector('button[type="submit"]');
        if (isLoading) {
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            form.classList.add('loading');
        } else {
            button.disabled = false;
            button.innerHTML = button.getAttribute('data-original-text');
            form.classList.remove('loading');
        }
    }

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData();
        const file = document.getElementById('file').files[0];
        
        if (!file) {
            showAlert('Please select a file to upload', 'warning');
            return;
        }
        
        formData.append('file', file);
        setLoading(this, true);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showAlert('File processed successfully! You can now ask questions.');
                document.getElementById('question').focus();
            } else {
                showAlert(data.error || 'Error processing file', 'danger');
            }
        } catch (error) {
            showAlert('Error processing file: ' + error.message, 'danger');
        } finally {
            setLoading(this, false);
        }
    });

    urlForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const url = document.getElementById('url').value;
        
        if (!url) {
            showAlert('Please enter a URL', 'warning');
            return;
        }
        
        setLoading(this, true);

        try {
            const response = await fetch('/process_url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (response.ok) {
                showAlert('URL processed successfully! You can now ask questions.');
                document.getElementById('question').focus();
            } else {
                showAlert(data.error || 'Error processing URL', 'danger');
            }
        } catch (error) {
            showAlert('Error processing URL: ' + error.message, 'danger');
        } finally {
            setLoading(this, false);
        }
    });

    queryForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const question = document.getElementById('question').value;
        
        if (!question) {
            showAlert('Please enter a question', 'warning');
            return;
        }
        
        setLoading(this, true);
        answerDiv.style.display = 'none';

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });

            const data = await response.json();

            if (response.ok) {
                answerText.textContent = data.answer;
                answerDiv.style.display = 'block';
            } else {
                showAlert(data.error || 'Error getting answer', 'danger');
            }
        } catch (error) {
            showAlert('Error getting answer: ' + error.message, 'danger');
        } finally {
            setLoading(this, false);
        }
    });

    // Store original button text
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.setAttribute('data-original-text', button.innerHTML);
    });
}); 