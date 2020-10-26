#include "ofMain.h"
#include "ofApp.h"

//========================================================================
int main(int argc, char **argv){
	// set window size
	ofSetupOpenGL(800, 800, OF_WINDOW);

	// create and run app
	ofApp *app = new ofApp();
	app->argc = argc;
	app->argv = argv;

	// run the app
	ofRunApp(app);
}
