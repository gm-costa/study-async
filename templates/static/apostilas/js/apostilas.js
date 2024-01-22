const container = document.getElementById('pdf-container');

pdfjsLib.getDocument("{{apostila.arquivo.url}}").promise.then(pdf => {
    pdf.getPage(1).then(page => {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        const viewport = page.getViewport({ scale: 0.6 });

        canvas.width = viewport.width;
        canvas.height = viewport.height;

        page.render({ canvasContext: context, viewport }).promise.then(() => {
            container.appendChild(canvas);
        });
    });
});
