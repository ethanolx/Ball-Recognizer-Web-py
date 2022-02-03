const CHART = document.getElementById('chart');
const ALL_LABELS = CHART.data[0].labels;
console.log('All Labels: ', ALL_LABELS);


CHART.on('plotly_legendclick', data => {
    if (Object.keys(data.layout).includes('hiddenlabels')) {
        if (data.layout.hiddenlabels.includes(data.label)) {
            data.layout.hiddenlabels = data.layout.hiddenlabels.filter(ball => ball !== data.label);
        }
        else {
            data.layout.hiddenlabels = [...data.layout.hiddenlabels, data.label];
        }
    }
    else {
        data.layout.hiddenlabels = [data.label];
    }
    filter_predictions(data.layout.hiddenlabels);
});

CHART.on('plotly_legenddoubleclick', data => {
    if (!data.layout.hiddenlabels.includes(data.label) && data.layout.hiddenlabels.length === ALL_LABELS.length - 1) {
        data.layout.hiddenlabels = [];
    }
    else {
        data.layout.hiddenlabels = [...ALL_LABELS.filter(ball => ball !== data.label)];
    }
    filter_predictions(data.layout.hiddenlabels);
});

function filter_predictions(hidden_labels) {
    for (let n of document.querySelectorAll('.ball-card')) {
        let el_classes = n.className.split(' ');
        let ball_type = el_classes[2].replace(/[_]/g, ' ');
        n.hidden = hidden_labels.includes(ball_type);
    }
}