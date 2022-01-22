const webcamElement = document.getElementById('webcam');
const canvasElement = document.getElementById('cam-canvas');
const webcam = new Webcam(webcamElement, 'user', canvasElement);

async function predict_cam() {
    let picture = webcam.snap();
    webcam.stop()
    webcamElement.style.display = 'none';
    canvasElement.hidden = false;

    fetch(picture).then(async res => {
        document.getElementById('result').innerText = 'Fetching prediction from server...';
        let img_form = new FormData();
        img_form.append(name = 'image', value = await res.blob());
        let response = await fetch('/predict', {
            method: 'POST',
            body: img_form
        });
        let result = await response.json();
        document.getElementById('result').innerText = `I think it\'s a ${ result['prediction'] }`;
    });
}

async function clear_cam() {
    webcamElement.style.display = 'block';
    canvasElement.hidden = true;
    webcam.start();
}