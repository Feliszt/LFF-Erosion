#pragma once

#include "ofMain.h"
#include "ofxAudioFile.h"

class ofApp : public ofBaseApp {

public:
	void setup();
	void update();
	void draw();
	void audioOut(ofSoundBuffer & buffer);

	// app arguments
	int			argc;
	char**		argv;
	//
	string		fileName;
	int			numLoop;
	float		videoScale;
	string		fileType;
	int			windowPosX;
	int			windowPosY;
	float		volume;

	// video folder
	string		fileFolder;

	// video player
	ofVideoPlayer		videoPlayer;
	int					mediaWidth, mediaHeight;
	float				soundPrevPosition;
	int					prevFrame, loopCount, borderWindowX, borderWindowY;

	// audio player
	ofxAudioFile	audioFile;
	int				audioStreamPos;
	int				bufferSize;

	// progress bar
	float				progressBarSize, progressBarOffset, progressBarRoundRadius;
};
