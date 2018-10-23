from sounds import get_sounds

class ScratchProjectBase:
	def __init__(self):
		self.json = {
	"objName": "Stage",
	"sounds": [{
			"soundName": "pop",
			"soundID": 7,
			"md5": "83a9787d4cb6f3b7632b4ddfebf74367.wav",
			"sampleCount": 258,
			"rate": 11025,
			"format": ""
		}],
	"costumes": [{
			"costumeName": "backdrop1",
			"baseLayerID": 3,
			"baseLayerMD5": "739b5e2a2435f6e1ec2993791b423146.png",
			"bitmapResolution": 1,
			"rotationCenterX": 240,
			"rotationCenterY": 180
		}],
	"currentCostumeIndex": 0,
	"penLayerMD5": "5c81a336fab8be57adc039a8a2b33ca9.png",
	"penLayerID": 0,
	"tempoBPM": 60,
	"videoAlpha": 0.5,
	"children": [{
		"objName": "Sprite1",
		"sounds": get_sounds(),
		"costumes": [{
				"costumeName": "costume1",
				"baseLayerID": 1,
				"baseLayerMD5": "f9a1c175dbe2e5dee472858dd30d16bb.svg",
				"bitmapResolution": 1,
				"rotationCenterX": 47,
				"rotationCenterY": 55
			},
			{
				"costumeName": "costume2",
				"baseLayerID": 2,
				"baseLayerMD5": "6e8bd9ae68fdb02b7e1e3df656a75635.svg",
				"bitmapResolution": 1,
				"rotationCenterX": 47,
				"rotationCenterY": 55
			}],
		"currentCostumeIndex": 0,
		"scratchX": 0,
		"scratchY": 0,
		"scale": 1,
		"direction": 90,
		"rotationStyle": "normal",
		"isDraggable": False,
		"indexInLibrary": 1,
		"visible": True,
		"spriteInfo": {
		}
	}],
	"info": {
		"scriptCount": 0,
		"flashVersion": "MAC 28,0,0,126",
		"swfVersion": "v460",
		"userAgent": "Scratch 2.0 Offline Editor",
		"spriteCount": 1,
		"videoOn": False
	}
}

