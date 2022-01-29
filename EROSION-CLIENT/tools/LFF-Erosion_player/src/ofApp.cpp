#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup() {
	// arg debug
	/*
	for (int i = 0; i < argc; i++) {
		cout << "[Pleine-mer_videoPlayer]\targ #" << i << "\t[" << argv[i] << "]" << endl;
	}
	//ofExit();*/

	// get arguments
	if (argc != 8 && argc != 1) {
		cout << "[LFF-Erosion_player] RECEIVED " << argc << " ARGUMENTS. NEEDS 8." << endl;
		ofExit();
	}

	// get config
	ofJson client_config = ofLoadJson("../../../../data/config.json");
	string media_folder = "";
	if (client_config["video_folder"].is_null()) {
		ofLog() << "[LFF - Erosion_player]\t" << "no video folder specified in config file. exit.";
	}
	if (client_config["audio_folder"].is_null()) {
		ofLog() << "[LFF - Erosion_player]\t" << "no audio folder specified in config file. exit.";
	}

	// allow an option for 0 arguments
	if (argc == 1) {
		fileName = "feuilles02_400x400.mp4";
		numLoop = 3;
		videoScale = 0.65;
		windowPosX = 20;
		windowPosY = 20;
		volume = 1.0;
		fileType = "video";
	}
	else {
		fileName = argv[1];
		numLoop = stoi(argv[2]);
		videoScale = stof(argv[3]);
		windowPosX = stoi(argv[4]);
		windowPosY = stoi(argv[5]);
		volume = stoi(argv[6]);
		fileType = argv[7];
		media_folder = "../../../../data/";
	}

	// init video player
	if (fileType == "video") {
		string video_path = media_folder + fileName;
		videoPlayer.load(video_path);
		videoPlayer.play();
		videoPlayer.setVolume(volume);
		mediaWidth = int(videoPlayer.getWidth() * videoScale);
		mediaHeight = int(videoPlayer.getHeight() * videoScale);
		loopCount = 0;
	}
	else if (fileType == "audioclip") {
		string audio_path = media_folder + fileName;
		loopCount = 0;
		mediaWidth = 400;
		mediaHeight = 200;
		bufferSize = 512;
		audioFile.load(audio_path);
		float sampleRate = 44100.0;
		ofSoundStreamSettings settings;
		settings.setOutListener(this);
		settings.sampleRate = sampleRate;
		settings.numOutputChannels = 2;
		settings.numInputChannels = 0;
		settings.bufferSize = bufferSize;
		ofSoundStreamSetup(settings);
		audioStreamPos = 0;
		ofSetFrameRate(sampleRate / 1000);
	}

	// resize window and position window
	ofSetWindowShape(mediaWidth, mediaHeight);
	ofSetWindowPosition(windowPosX, windowPosY);

	// progress bar settings
	progressBarSize = 15;
	progressBarOffset = 4;
	progressBarRoundRadius = 10;

	// debug
	//cout << "[inst_videoPlayer]\t[" << fileName << "]\tStart." << endl;
}

//--------------------------------------------------------------
void ofApp::update() {
	// update video
	if (fileType == "video") {
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
}

//--------------------------------------------------------------
void ofApp::draw() {
	// bg
	ofBackground(255);

	// play video
	if (fileType == "video") {
		ofSetColor(255);
		ofPushMatrix();
		ofScale(videoScale);
		videoPlayer.draw(0, 0);
		ofPopMatrix();
	}

	// compute progress bar
	int progressBarX = 0;
	if (fileType == "video") {
		progressBarX = ofMap(videoPlayer.getCurrentFrame(), 0, videoPlayer.getTotalNumFrames(), progressBarOffset, mediaWidth - 2 * progressBarOffset);
	}
	else {
		progressBarX = ofMap(audioStreamPos, 0, audioFile.length(), progressBarOffset, mediaWidth - 2 * progressBarOffset);
	}

	if (fileType == "audioclip") {
		ofSetColor(0);
		ofNoFill();
		ofSetLineWidth(5);
		ofBeginShape();
		for (int i = 0; i < bufferSize; i += 2) {
			float val = audioFile.sample(audioStreamPos + i, 1) * 10.0;
			float y = ofMap(val, -1.0, 1.0, ofGetHeight() * 0.9, ofGetHeight() * 0.1);
			float x = ofMap(i, 0, bufferSize, ofGetWidth() * 0.05, ofGetWidth() * 0.95);
			ofVertex(x, y);
		}
		ofEndShape();
		ofSetLineWidth(1);
		ofFill();
	}

	// draw background of progress bar
	ofSetColor(240);
	ofDrawRectangle(0, mediaHeight - progressBarSize, mediaWidth, progressBarSize);

	// draw grey middleground of progress bar
	ofSetColor(210);
	ofDrawRectRounded(progressBarOffset, mediaHeight - progressBarSize + progressBarOffset, mediaWidth - 2 * progressBarOffset, progressBarSize - 2 * progressBarOffset, progressBarRoundRadius);

	// draw white foreground of progress bar
	ofSetColor(50);
	ofDrawRectRounded(progressBarOffset, mediaHeight - progressBarSize + progressBarOffset, progressBarX, progressBarSize - 2 * progressBarOffset, progressBarRoundRadius);
}

//--------------------------------------------------------------
void ofApp::audioOut(ofSoundBuffer & buffer) {
	for (int i = 0; i < buffer.getNumFrames(); i++) {
		if ((audioStreamPos + i) > audioFile.length()) {
			ofExit();
		}
		for (int k = 0; k < buffer.getNumChannels(); k++) {
			buffer[i * buffer.getNumChannels() + k] = audioFile.sample(audioStreamPos + i, 1) * volume;
		}
	}
	audioStreamPos += buffer.getNumFrames();
}