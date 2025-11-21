const { app, BrowserWindow } = require('electron');
const path = require('path');
const { pathToFileURL } = require('url');

function createWindow() {
    const win = new BrowserWindow({
        width: 1000,
        height: 700,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    const startPage = path.join(__dirname, 'renderer', 'index.html');
    win.loadURL(pathToFileURL(startPage).href);
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
