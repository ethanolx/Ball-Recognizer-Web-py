const webcamElement = document.getElementById('webcam');
const canvasElement = document.getElementById('cam-canvas');
const canvasContext = canvasElement.getContext('2d');
const hiddenCanvas = document.getElementById('hidden-canvas');
const webcam = new Webcam(webcamElement, 'user', hiddenCanvas);
const hiddenImage = document.getElementById('hidden_img');

async function predict_cam() {
    let picture = webcam.snap();
    webcam.stop();
    webcamElement.style.display = 'none';

    hiddenImage.src = picture;

    hiddenImage.onload = ev => {
        let new_dimensions = Math.min(hiddenCanvas.width, hiddenCanvas.height);
        let crop_left = (hiddenCanvas.width - new_dimensions) / 2;
        let crop_top = (hiddenCanvas.height - new_dimensions) / 2;
        console.log(hiddenCanvas.width, hiddenCanvas.height, crop_left, crop_top);
        console.log(crop_left, crop_top, new_dimensions, new_dimensions, 0, 0, 220, 220);

        canvasContext.drawImage(hiddenImage, crop_left, crop_top, new_dimensions, new_dimensions, 0, 0, 220, 220);
        canvasElement.hidden = false;

        fetch(canvasElement.toDataURL('image/png')).then(async res => {
            document.getElementById('result').innerText = 'Fetching prediction from server...';
            let img_form = new FormData();
            img_form.append(name = 'image', value = await res.blob());
            let response = await fetch('/predict', {
                method: 'POST',
                body: img_form
            });
            let result = await response.json();
            document.getElementById('result').innerText = `I think it\'s a ${ result['prediction'] }`;
        })
    };
}

async function clear_cam() {
    webcamElement.style.display = 'block';
    canvasElement.hidden = true;
    webcam.start();
}

