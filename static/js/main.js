function copyToClipboard() {
    const inputElement = document.getElementById("shortUrlText");
    const btn = document.querySelector('.copy-btn');
    const copyText = btn.querySelector('.copy-text');
    const copyIcon = btn.querySelector('.copy-icon');
    
    if (!inputElement) {
        console.error('Short URL input not found');
        return;
    }

    inputElement.select();
    inputElement.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(inputElement.value).then(() => {
        const originalText = copyText ? copyText.innerText : 'Copy';

        btn.classList.add('copied');
        
        if (copyText) {
            copyText.innerText = "Copiado!";
        }

        if (copyIcon) {
            copyIcon.innerHTML = '<polyline points="20 6 9 17 4 12"></polyline>';
        }
        
        setTimeout(() => {
            btn.classList.remove('copied');
            
            if (copyText) {
                copyText.innerText = originalText;
            }
            
            if (copyIcon) {
                copyIcon.innerHTML = '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>';
            }
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        
        try {
            document.execCommand('copy');
            
            if (copyText) {
                copyText.innerText = "Copied!";
            }
            
            setTimeout(() => {
                if (copyText) {
                    copyText.innerText = "Copy";
                }
            }, 2000);
        } catch (fallbackErr) {
            console.error('Fallback copy failed: ', fallbackErr);
            alert('Failed to copy URL. Please copy manually.');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const shortUrlInput = document.getElementById('shortUrlText');
    
    if (shortUrlInput) {

        shortUrlInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                copyToClipboard();
            }
        });
        
        shortUrlInput.addEventListener('click', function() {
            this.select();
        });

        shortUrlInput.focus();
        shortUrlInput.select();
    }
});
