const {
    app,
    BrowserWindow
} = require('electron');

const path = require('path');

let mainWindow = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,

        webPreferences: {
            contextIsolation: false,
            nodeIntegration: true,
            nodeIntegrationInWorker: true,
			preload: path.join(__dirname, 'preload.js')
        }
    });

    mainWindow.loadFile(
        `${__dirname}/src/index.html`
    );

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on(
    'ready',
    createWindow
);

app.on(
    'window-all-closed',
    () =>
        process.platform !== 'darwin' &&
        app.quit()
);

app.on(
    'activate',
    () =>
        mainWindow === null &&
        createWindow()
);