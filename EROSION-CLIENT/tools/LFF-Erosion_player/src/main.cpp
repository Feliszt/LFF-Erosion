#include "ofMain.h"
#include "ofApp.h"
#include "ofAppGLFWWindow.h"

//========================================================================
int main(int argc, char **argv) {
	ofGLFWWindowSettings settings;

	// main window
	settings.setSize(800, 800);
	settings.setGLVersion(4, 5);
	settings.setPosition(ofVec2f(100, 100));
	settings.decorated = false;
	settings.resizable = false;
	shared_ptr<ofAppBaseWindow> mainWindow = ofCreateWindow(settings);

	// create and run app
	ofApp *app = new ofApp();
	app->argc = argc;
	app->argv = argv;

	// run the app
	shared_ptr<ofApp> mainApp(app);
	ofRunApp(mainWindow, mainApp);
	ofRunMainLoop();
}
