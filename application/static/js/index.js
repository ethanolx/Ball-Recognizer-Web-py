/**@type {number} */
const DEFAULT_BRUSH_WIDTH = 20;

/**@type {string} */
const DEFAULT_BRUSH_COLOUR = '#000000';

/**@type {HTMLCanvasElement} */
let CANVAS = document.getElementById('canvas');

/**@type {CanvasRenderingContext2D} */
let CANVAS_CONTEXT = CANVAS.getContext('2d');

let BRUSH_WIDTH_SELECTOR = document.getElementById('brush-width');
let BRUSH_CURRENT_WIDTH = document.getElementById('current-width');
let BRUSH_COLOUR_SELECTOR = document.getElementById('brush-colour');
let BRUSH_PREVIEW = document.getElementById('brush-preview');
CANVAS_CONTEXT.lineCap = CANVAS_CONTEXT.lineJoin = 'round';

/**
 * @typedef Coordinates
 * @property {number} x
 * @property {number} y
 */

/**@type {Coordinates} */
let ORIGIN_COORDS = { x: 0, y: 0 };

/**@type {Coordinates} */
let DESTINATION_COORDS = { x: 0, y: 0 };


function load_defaults() {
    BRUSH_WIDTH_SELECTOR.value = DEFAULT_BRUSH_WIDTH;
    BRUSH_COLOUR_SELECTOR.value = DEFAULT_BRUSH_COLOUR;
}

function load_canvas() {
    CANVAS_CONTEXT.fillStyle = 'white';
    CANVAS_CONTEXT.fillRect(0, 0, CANVAS.width, CANVAS.height);
}

function load_page() {
    load_defaults();
    load_canvas();
    updatePreview();
    load_event_listeners();
}

function update_brush_parameters() {
    CANVAS_CONTEXT.lineWidth = parseInt(BRUSH_WIDTH_SELECTOR.value);
    CANVAS_CONTEXT.strokeStyle = BRUSH_COLOUR_SELECTOR.value;
}

function paint() {
    CANVAS_CONTEXT.beginPath();
    CANVAS_CONTEXT.moveTo(ORIGIN_COORDS.x, ORIGIN_COORDS.y);
    CANVAS_CONTEXT.lineTo(DESTINATION_COORDS.x, DESTINATION_COORDS.y);
    CANVAS_CONTEXT.closePath();
    CANVAS_CONTEXT.stroke();
}

function update_mouse_position(ev) {
    const RECT = CANVAS.getBoundingClientRect();
    DESTINATION_COORDS.x = ev.clientX - RECT.left;
    DESTINATION_COORDS.y = ev.clientY - RECT.top;

    ORIGIN_COORDS.x = DESTINATION_COORDS.x;
    ORIGIN_COORDS.y = DESTINATION_COORDS.y;
}

function updatePreview() {
    let BRUSH_PREVIEW_CONTEXT = BRUSH_PREVIEW.getContext('2d');
    BRUSH_PREVIEW.width = parseInt(BRUSH_WIDTH_SELECTOR.value);
    BRUSH_PREVIEW.height = parseInt(BRUSH_WIDTH_SELECTOR.value);
    BRUSH_PREVIEW_CONTEXT.fillStyle = BRUSH_COLOUR_SELECTOR.value;
    BRUSH_PREVIEW_CONTEXT.fillRect(0, 0, BRUSH_PREVIEW.width, BRUSH_PREVIEW.height);
    BRUSH_CURRENT_WIDTH.value = BRUSH_WIDTH_SELECTOR.value;

    update_brush_parameters();
}

function load_event_listeners() {
    CANVAS.addEventListener("mousemove", update_mouse_position, false);

    CANVAS.addEventListener("mousedown", function (e) {
        CANVAS.addEventListener("mousemove", paint, false);
    }, false);

    CANVAS.addEventListener("mouseup", function (e) {
        CANVAS.removeEventListener("mousemove", paint, false);
    }, false);
};


function clear_canvas() {
    CANVAS_CONTEXT.clearRect(0, 0, 224, 224);
    CANVAS_CONTEXT.fillStyle = "white";
    CANVAS_CONTEXT.fillRect(0, 0, CANVAS.width, CANVAS.height);
}

async function predict_drawing() {
    document.getElementById('result').innerText = 'Fetching prediction from server...';
    let img_form = new FormData();
    img_form.append(
        name = 'image',
        value = await new Promise(res => CANVAS.toBlob(res, 'image/png')),
        fileName = 'ball.png'
    );

    let response = await fetch('/predict', {
        method: 'POST',
        body: img_form
    });
    let result = await response.json();
    document.getElementById('result').innerText = `I think it\'s a ${ result }`;
}

const webcamElement = document.getElementById('webcam');
const canvasElement = document.getElementById('cam-canvas');
const webcam = new Webcam(webcamElement, 'user', canvasElement);


async function predict_cam() {
    let picture = webcam.snap();
    webcam.stop();

    document.getElementById('result').innerText = 'Fetching prediction from server...';
    let img_form = new FormData();
    img_form.append(
        name = 'image',
        value = await new Promise(res => canvasElement.toBlob(res, 'image/png')),
        fileName = 'ball.png'
    );

    let response = await fetch('/predict', {
        method: 'POST',
        body: img_form
    });
    let result = await response.json();
    document.getElementById('result').innerText = `I think it\'s a ${ result }`;
}


load_page();

// document.getElementById("predictBtn").click(function () {
//     document.getElementById('result').text('Fetching prediction from server...');
//     var CANVAS = document.getElementById("CANVAS").get(0);
//     var context = CANVAS.getContext("2d");
//     var img = CANVAS.toDataURL('image/png');
//     document.getElementById.aax({
//         type: "POST",
//         url: "https://digit-recognizer-2085.herokuapp.com/predict",
//         data: img,
//         success: function (data) {
//             document.getElementById('result').text('Predicted Output: ' + data);
//         }
//     });
// });

