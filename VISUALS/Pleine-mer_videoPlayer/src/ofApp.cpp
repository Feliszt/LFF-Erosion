#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
	// get arguments
	if (argc != 3 && argc != 1) {
		ofLog() << "[Pleine-mer_videoPlayer] NOT RIGHT ARGUMENTS. NEEDS 2 ARGUMENTS.";
		ofExit();
	}

	// allow an option for 0 arguments
	if (argc == 1) {
		fileName			= "video_benmzrt_32_22-01-2020_20h57_12_384-656.mp4";
		numLoopTotal		= 1;
	}
	else {
		fileName = argv[1];
		numLoopTotal = stoi(argv[2]);
	}

	// set fileName
	fileFolder		= "D:/PERSO/_CREA/Pleine-mer/_DEV/DATA/Pleine-mer_media-files/";

	// init video player
	videoPlayer.load(fileFolder + fileName);
	videoWidth			= videoPlayer.getWidth();
	videoHeight			= videoPlayer.getHeight();
	loopCount			= 0;
	borderWindow		= 10;

	// get screen size
	int screenWidth		= ofGetScreenWidth();
	int screenHeight	= ofGetScreenHeight();

	// set window position
	int windowX = (videoWidth >= screenWidth) ? borderWindow : ofRandom(borderWindow, screenWidth - videoWidth - borderWindow);
	int windowY = (videoHeight >= screenHeight) ? borderWindow : ofRandom(borderWindow, screenHeight - videoHeight - borderWindow);

	// resize window and position window
	ofSetWindowShape(videoWidth, videoHeight);
	ofSetWindowPosition(int(windowX), int(windowY));

	// progress bar settings
	progressBarSize			= 20;
	progressBarOffset		= 5;

	// play video
	videoPlayer.play();

	// debug
	ofLog() << "[Pleine-mer_videoPlayer]\tPlaying file [" << fileName << "]\tnum loop = " << numLoopTotal;
}

//--------------------------------------------------------------
void ofApp::update(){
	// update video
	videoPlayer.update();

	// debug
	//ofLog() << videoPlayer.getCurrentFrame() << " / " << videoPlayer.getTotalNumFrames();

	// check if loop
	if (videoPlayer.getCurrentFrame() == 0 && prevFrame >= videoPlayer.getTotalNumFrames() - 1) {
		loopCount++;

		ofLog() << "[Pleine-mer_videoPlayer]\tLoop #" << loopCount;

		// check if we looped enough
		// if so, we exit the app
		if (loopCount == numLoopTotal) {
			ofExit();
		}
	}

	// update frame
	prevFrame = videoPlayer.getCurrentFrame();
}

//--------------------------------------------------------------
void ofApp::draw(){
	// play video
	ofBackground(255);
	ofSetColor(255);
	videoPlayer.draw(0, 0);

	// compute progress bar
	int progressBarX = ofMap(videoPlayer.getCurrentFrame(), 0, videoPlayer.getTotalNumFrames(), progressBarOffset, videoWidth - 2 * progressBarOffset);

	// draw black background of progress bar
	ofSetColor(255);
	ofDrawRectangle(0, videoHeight - progressBarSize, videoWidth, progressBarSize);

	// draw grey middleground of progress bar
	ofSetColor(200);
	ofDrawRectangle(progressBarOffset, videoHeight - progressBarSize + progressBarOffset, videoWidth - 2 * progressBarOffset, progressBarSize - 2 * progressBarOffset);

	// draw white foreground of progress bar
	ofSetColor(0);
	ofDrawRectangle(progressBarOffset, videoHeight - progressBarSize + progressBarOffset, progressBarX, progressBarSize - 2 * progressBarOffset);
}