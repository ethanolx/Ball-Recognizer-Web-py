const webcamElement = document.getElementById('webcam');
const canvasElement = document.getElementById('cam-canvas');
const canvasContext = canvasElement.getContext('2d');
const hiddenCanvas = document.getElementById('hidden-canvas');
const webcam = new Webcam(webcamElement, 'user', hiddenCanvas);
const webcamElement2 = document.getElementById('webcamhidden');
const webcamhidden = new Webcam(webcamElement2, 'user')
const hiddenImage = document.getElementById('hidden_img');

async function predict_cam() {
    let picture = webcam.snap();
    webcam.stop();
    webcamElement.style.display = 'none';

    hiddenImage.src = picture;

    hiddenImage.onload = ev => {
        const SOURCE_DIMS = Math.max(webcamElement2.width, webcamElement2.height)
        const SOURCE_WIDTH = webcamElement2.height / SOURCE_DIMS * 220;
        const SOURCE_HEIGHT = webcamElement2.width / SOURCE_DIMS * 220;

        const CROP_LEFT = (220 - SOURCE_WIDTH) / 2;
        const CROP_RIGHT = (220 - SOURCE_HEIGHT) / 2;

        canvasContext.drawImage(hiddenImage, CROP_LEFT, CROP_RIGHT, SOURCE_WIDTH, SOURCE_HEIGHT, 0, 0, 220, 220);
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
            document.getElementById('result').innerText = `I think it\'s a ${ result['prediction'] } (${(result['probability'] * 100.0).toFixed(2)}%)`;
        });
    };
}

async function clear_cam() {
    webcamElement.style.display = 'block';
    canvasElement.hidden = true;
    webcam.start();
}

