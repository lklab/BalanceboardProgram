#!/usr/bin/env python3

STIMULATION_MODE_VISION = "v"
STIMULATION_MODE_HEARING = "h"
STIMULATION_MODE_BOTH = "b"

INPUT_TYPE_LEFT_HAND = "lh"
INPUT_TYPE_RIGHT_HAND = "rh"
INPUT_TYPE_LEFT_FOOT = "lf"
INPUT_TYPE_RIGHT_FOOT = "rf"

motionSetting = {}
motionSetting[1] = {
	"perfectDuration" : 150,
	"stimulations" : [
		STIMULATION_MODE_BOTH,
		STIMULATION_MODE_HEARING,
		STIMULATION_MODE_VISION,
		STIMULATION_MODE_BOTH,
		STIMULATION_MODE_HEARING,
		STIMULATION_MODE_VISION,
		STIMULATION_MODE_BOTH,
		STIMULATION_MODE_HEARING,
		STIMULATION_MODE_VISION,
		STIMULATION_MODE_BOTH,
		STIMULATION_MODE_HEARING,
		STIMULATION_MODE_VISION,
	],
	"inputs" : [
		[INPUT_TYPE_RIGHT_HAND],
		[INPUT_TYPE_RIGHT_HAND],
		[INPUT_TYPE_RIGHT_HAND],
		[INPUT_TYPE_LEFT_HAND],
		[INPUT_TYPE_LEFT_HAND],
		[INPUT_TYPE_LEFT_HAND],
		[INPUT_TYPE_RIGHT_FOOT],
		[INPUT_TYPE_RIGHT_FOOT],
		[INPUT_TYPE_RIGHT_FOOT],
		[INPUT_TYPE_LEFT_FOOT],
		[INPUT_TYPE_LEFT_FOOT],
		[INPUT_TYPE_LEFT_FOOT],
	]
}
motionSetting[2] = {
	"perfectDuration" : 150,
	"stimulations" : [
		STIMULATION_MODE_BOTH,
		STIMULATION_MODE_HEARING,
		STIMULATION_MODE_VISION,
		STIMULATION_MODE_BOTH,
		STIMULATION_MODE_HEARING,
		STIMULATION_MODE_VISION,
	],
	"inputs" : [
		[INPUT_TYPE_RIGHT_HAND, INPUT_TYPE_LEFT_HAND],
		[INPUT_TYPE_RIGHT_HAND, INPUT_TYPE_LEFT_HAND],
		[INPUT_TYPE_RIGHT_HAND, INPUT_TYPE_LEFT_HAND],
		[INPUT_TYPE_RIGHT_FOOT, INPUT_TYPE_LEFT_FOOT],
		[INPUT_TYPE_RIGHT_FOOT, INPUT_TYPE_LEFT_FOOT],
		[INPUT_TYPE_RIGHT_FOOT, INPUT_TYPE_LEFT_FOOT],
	]
}
motionSetting[3] = {
	"perfectDuration" : 150,
	"stimulations" : [
		STIMULATION_MODE_BOTH,
		STIMULATION_MODE_HEARING,
		STIMULATION_MODE_VISION,
		STIMULATION_MODE_BOTH,
		STIMULATION_MODE_HEARING,
		STIMULATION_MODE_VISION,
	],
	"inputs" : [
		[INPUT_TYPE_RIGHT_HAND, INPUT_TYPE_LEFT_FOOT],
		[INPUT_TYPE_RIGHT_HAND, INPUT_TYPE_LEFT_FOOT],
		[INPUT_TYPE_RIGHT_HAND, INPUT_TYPE_LEFT_FOOT],
		[INPUT_TYPE_LEFT_HAND, INPUT_TYPE_RIGHT_FOOT],
		[INPUT_TYPE_LEFT_HAND, INPUT_TYPE_RIGHT_FOOT],
		[INPUT_TYPE_LEFT_HAND, INPUT_TYPE_RIGHT_FOOT],
	]
}

motionSetting[4] = motionSetting[1].copy()
motionSetting[4]["perfectDuration"] = 100
motionSetting[5] = motionSetting[2].copy()
motionSetting[5]["perfectDuration"] = 100
motionSetting[6] = motionSetting[3].copy()
motionSetting[6]["perfectDuration"] = 100

motionSetting[7] = motionSetting[1].copy()
motionSetting[7]["perfectDuration"] = 50
motionSetting[8] = motionSetting[2].copy()
motionSetting[8]["perfectDuration"] = 50
motionSetting[9] = motionSetting[3].copy()
motionSetting[9]["perfectDuration"] = 50

motionSetting[10] = motionSetting[1].copy()
motionSetting[10]["perfectDuration"] = 30
motionSetting[11] = motionSetting[2].copy()
motionSetting[11]["perfectDuration"] = 30
motionSetting[12] = motionSetting[3].copy()
motionSetting[12]["perfectDuration"] = 30

motionSetting[13] = motionSetting[1].copy()
motionSetting[13]["perfectDuration"] = 15
motionSetting[14] = motionSetting[2].copy()
motionSetting[14]["perfectDuration"] = 15
motionSetting[15] = motionSetting[3].copy()
motionSetting[15]["perfectDuration"] = 15

import json
file = open("exercise_bi_setting.json", "w")
file.write(json.dumps(motionSetting, indent=4))
file.close()
