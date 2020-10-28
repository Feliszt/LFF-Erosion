#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
	/*
	// arg debug
	for (int i = 0; i < argc; i++) {
		ofLog() << "[Pleine-mer_videoPlayer]\targ #" << i << "\t[" << argv[i] << "]";
	}
	*/

	// get arguments
	if (argc != 6 && argc != 1) {
		ofLog() << "[Pleine-mer_videoPlayer] RECEIVED " << argc << " ARGUMENTS. NEEDS 6.";
		ofExit();
	}

	// allow an option for 0 arguments
	if (argc == 1) {
		fileName		= "video_ble_65_01-05-2019_16h19.mp4";
		numLoop			= 3;
		videoScale		= 0.65;
		windowPosX		= 20;
		windowPosY		= 20;
	}
	else {
		fileName	= argv[1];
		numLoop		= stoi(argv[2]);
		videoScale	= stof(argv[3]);
		windowPosX	= stoi(argv[4]);
		windowPosY	= stoi(argv[5]);
	}

	// read json config file and store variables
	ofJson configFile = ofLoadJson("D:/PERSO/_CREA/Pleine-mer/_DEV/DATA/installationData/config.json");
	fileFolder = configFile["media_folder"].get<std::string>();

	// init video player
	videoPlayer.load(fileFolder + fileName);
	videoWidth			= int(videoPlayer.getWidth() * videoScale);
	videoHeight			= int(videoPlayer.getHeight() * videoScale);
	loopCount			= 0;

	// resize window and position window
	ofSetWindowShape(videoWidth, videoHeight);
	ofSetWindowPosition(windowPosX, windowPosY);

	// progress bar settings
	progressBarSize			= 15;
	progressBarOffset		= 4;
	progressBarRoundRadius	= 10;

	// play video
	videoPlayer.play();
	//videoPlayer.setVolume(0.0);

	// debug
	//cout << "[inst_videoPlayer]\t[" << fileName << "]\tStart." << endl;
}

//--------------------------------------------------------------
void ofApp::update(){
	// update video
	videoPlayer.update();

	// debug
	//ofLog() << videoPlayer.getCurrentFrame() << " / " << videoPlayer.getTotalNumFrames();

	// check if loop
	if (videoPlayer.getCurrentFrame() == 0 && prevFrame != 0) {
		loopCount++;

		//ofLog() << "[Pleine-mer_videoPlayer]\tLoop #" << loopCount;

		// check if we looped enough
		// if so, we exit the app
		if (loopCount == numLoop) {
			//cout << "[inst_videoPlayer]\t[" << fileName << "]\tEnd." << endl;
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
	ofPushMatrix();
	ofScale(videoScale);
	videoPlayer.draw(0, 0);
	ofPopMatrix();

	// compute progress bar
	int progressBarX = ofMap(videoPlayer.getCurrentFrame(), 0, videoPlayer.getTotalNumFrames(), progressBarOffset, videoWidth - 2 * progressBarOffset);

	// draw black background of progress bar
	ofSetColor(250);
	ofDrawRectangle(0, videoHeight - progressBarSize, videoWidth, progressBarSize);

	// draw grey middleground of progress bar
	ofSetColor(210);
	ofDrawRectRounded(progressBarOffset, videoHeight - progressBarSize + progressBarOffset, videoWidth - 2 * progressBarOffset, progressBarSize - 2 * progressBarOffset, progressBarRoundRadius);

	// draw white foreground of progress bar
	ofSetColor(50);
	ofDrawRectRounded(progressBarOffset, videoHeight - progressBarSize + progressBarOffset, progressBarX, progressBarSize - 2 * progressBarOffset, progressBarRoundRadius);
}