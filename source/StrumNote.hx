package;

import flixel.FlxSprite;
import flixel.graphics.frames.FlxAtlasFrames;

using StringTools;

class StrumNote extends FlxSprite
{
	private var colorSwap:ColorSwap;
	public var resetAnim:Float = 0;
	private var noteData:Int = 0;
	public var laneScale:Float = 0.7;

	public function new(x:Float, y:Float, leData:Int, ?scaleOverride:Float = -1) {
		colorSwap = new ColorSwap();
		shader = colorSwap.shader;
		noteData = leData;
		laneScale = scaleOverride > 0 ? scaleOverride : Note.scales[PlayState.SONG.mania];
		super(x, y);
	}

	override function update(elapsed:Float) {
		if(resetAnim > 0) {
			resetAnim -= elapsed;
			if(resetAnim <= 0) {
				playAnim('static');
				resetAnim = 0;
			}
		}

		super.update(elapsed);
	}

	public function playAnim(anim:String, ?force:Bool = false) {
		animation.play(anim, force);
		updateHitbox();
		offset.x = frameWidth / 2;
		offset.y = frameHeight / 2;

		offset.x -= 156 * laneScale / 2;
		offset.y -= 156 * laneScale / 2;
		//centerOffsets();
		/*
		if(animation.curAnim.name == 'static') {
			colorSwap.hue = 0;
			colorSwap.saturation = 0;
			colorSwap.brightness = 0;
		} else {
			colorSwap.hue = ClientPrefs.arrowHSV[noteData % 4][0] / 360;
			colorSwap.saturation = ClientPrefs.arrowHSV[noteData % 4][1] / 100;
			colorSwap.brightness = ClientPrefs.arrowHSV[noteData % 4][2] / 100;

			if(animation.curAnim.name == 'confirm' && !PlayState.curStage.startsWith('school')) {
				offset.x -= 13;
				offset.y -= 13;
			}
		}
		*/
	}
}
