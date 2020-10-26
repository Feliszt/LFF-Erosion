#pragma once

#include "ofMain.h"

class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();	

		// app arguments
		int			argc;
		char**		argv;

		// file path
		string		fileFolder, fileName;
		int			fileLength;

		// video player
		ofVideoPlayer		videoPlayer;
		int					videoWidth, videoHeight, prevFrame, loopCount, numLoopTotal, borderWindow;

		// progress bar
		float				progressBarSize, progressBarOffset;
};
