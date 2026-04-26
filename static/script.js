document.addEventListener("DOMContentLoaded", function () {

    let nipt = parseFloat(document.getElementById("niptVal")?.innerText || 0);
    let cvs = parseFloat(document.getElementById("cvsVal")?.innerText || 0);
    let img = parseFloat(document.getElementById("imgVal")?.innerText || 0);

    if (nipt || cvs || img) {
        const ctx = document.getElementById('chart');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['NIPT', 'CVS', 'Imaging'],
                datasets: [{
                    label: 'Values',
                    data: [nipt, cvs, img]
                }]
            }
        });
    }
});
