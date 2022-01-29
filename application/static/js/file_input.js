function update_image_preview() {
    const form = document.getElementById('image-file');
    console.log(form.files)
    if (form.files.length > 0) {
        const image_file = form.files[0];
        const image_file_url = URL.createObjectURL(image_file);
        document.getElementById('image-preview').src = image_file_url;
    }
}

function clear_image_preview() {
    document.getElementById('image-preview').src = '';
}

async function predict_file() {
    document.getElementById('result').innerText = 'Fetching prediction from server...';
    let response = await fetch('/predict', {
        method: 'POST',
        body: new FormData(document.getElementById('file-form'))
    });
    let result = await response.json();
    document.getElementById('result').innerText = `I think it\'s a ${ result['prediction'] } (${(result['probability'] * 100.0).toFixed(2)}%)`;
}