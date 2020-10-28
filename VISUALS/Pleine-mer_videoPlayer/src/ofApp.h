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
		//
		string		fileName;
		int			numLoop;
		float		videoScale;
		string		fileType;
		int			windowPosX;
		int			windowPosY;

		// video folder
		string		fileFolder;

		// video player
		ofVideoPlayer		videoPlayer;
		int					videoWidth, videoHeight, prevFrame, loopCount, borderWindowX, borderWindowY;

		// progress bar
		float				progressBarSize, progressBarOffset, progressBarRoundRadius;
};
