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
	if (argc != 5 && argc != 1) {
		ofLog() << "[Pleine-mer_videoPlayer] RECEIVED " << argc << " ARGUMENTS. NEEDS 5.";
		ofExit();
	}

	// allow an option for 0 arguments
	if (argc == 1) {
		fileName		= "video_ble_65_01-05-2019_16h19.mp4";
		numLoop			= 3;
		videoScale		= 0.65;
		fileType		= "video";
	}
	else {
		fileName	= argv[1];
		numLoop		= stoi(argv[2]);
		videoScale	= stof(argv[3]);
		fileType	= argv[4];

		// rewrite video scale if audioclip
		// we display audio clips at the center with normal scale
		if (strcmp(fileType.c_str(), "audioclip") == 0) {
			videoScale = 1.0;
		}
	}

	// read json config file and store variables
	ofJson configFile = ofLoadJson("D:/PERSO/_CREA/Pleine-mer/_DEV/DATA/installationData/config.json");
	fileFolder = configFile["media_folder"].get<std::string>();
	borderWindowX = configFile["border_window_x"].get<std::int16_t>();
	borderWindowY = configFile["border_window_x"].get<std::int16_t>();	

	// init video player
	videoPlayer.load(fileFolder + fileName);
	videoWidth			= int(videoPlayer.getWidth() * videoScale);
	videoHeight			= int(videoPlayer.getHeight() * videoScale);
	loopCount			= 0;

	// get screen size
	int screenWidth		= ofGetScreenWidth();
	int screenHeight	= ofGetScreenHeight();

	// set window position
	int windowX = (videoWidth >= screenWidth) ? borderWindowX : ofRandom(borderWindowX, screenWidth - videoWidth - borderWindowX);
	int windowY = (videoHeight >= screenHeight) ? borderWindowY : ofRandom(borderWindowY, screenHeight - videoHeight - borderWindowX);

	// we display audio clips at the center with normal scale
	if (strcmp(fileType.c_str(), "audioclip") == 0) {
		windowX = int((screenWidth - videoWidth) * 0.5);
		windowY = int((screenHeight - videoHeight) * 0.5);
	}

	// resize window and position window
	ofSetWindowShape(videoWidth, videoHeight);
	ofSetWindowPosition(int(windowX), int(windowY));

	// progress bar settings
	progressBarSize			= 15;
	progressBarOffset		= 4;
	progressBarRoundRadius	= 10;

	// play video
	videoPlayer.play();
	//videoPlayer.setVolume(0.0);

	// debug
	cout << "[inst_videoPlayer]\t[" << fileName << "]\tStart." << endl;
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