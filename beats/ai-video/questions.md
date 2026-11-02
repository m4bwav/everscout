# Question bank: AI video generation

Seeds for everscout-engage (format: `beats/_template/questions.md`). Tag `ai` marks seeds that name models or generation; drop them where a community is hostile. Rephrase each for the post and tie it to a shot or moment the maker showed.

## How to use this file

Two or three seeds from different categories. Name the shot you mean ("the rooftop shot at 0:40"). In model subreddits asking which model is normal; elsewhere start with craft.

## Models and settings

- [models, ai] Which model did each shot come from? Did you mix models?
- [models, ai] Did you go image-to-video or text-to-video, and what made the keyframes?
- [models, ai] Roughly how many generations did you roll per usable shot?
- [models, ai] Local or cloud? If local, which GPU, and how long per clip?
- [lora, ai] Did you rebuild the trainer's latent cache after changing clips or captions?
- [wan, ai] Did you put the LoRA on both Wan 2.2 experts or only one?

## Consistency

- [consistency, ai] How did you keep the character consistent: a LoRA, reference images, something else?
- [consistency] How did you deal with wardrobe and props drifting between shots?
- [consistency, ai] Did you chain first and last frames to keep continuity?

## Pipeline

- [pipeline, ai] Would you share the ComfyUI workflow, or name the key nodes?
- [pipeline] Did you storyboard first, and with what?
- [pipeline] What did you use for upscaling or interpolation on the final?
- [pipeline, ai] Which sampler, steps and shift, and can you re-render the same take from its seed?
- [pipeline, ai] Are interactive world models usable for game prototyping yet?

## Editing and craft

- [craft] Which editor did you cut it in, and how much did you fix in the edit instead of regenerating?
- [craft] How did you handle pacing with the clip-length limits?
- [craft] Is there any real footage or compositing in there?
- [craft] What was the hardest shot to get, and why?
- [craft] Where do your cuts fall: on a look, a reaction or the action? Did the generated motion match across them? (Murch)
- [craft] Did you check the rhythm with a picture-only cut before adding sound? (Murch)
- [craft] Whose point of view does each scene follow, and did that change how you prompted the shots? (Katz)
- [craft] How did you hide the seam between two generated clips: a cleared frame, a foreground wipe, a short dissolve? (Katz)

## Sound

- [sound, ai] Is the audio native to the model or added after? What for voice, music and effects?
- [sound] How did you get the lip-sync to line up?

## Cost and time

- [cost] Roughly what did it cost in credits or GPU hours?
- [cost] How long from idea to final cut?

## Reception

- [reception] Where has it been shown, and how did people react?
- [reception] What would you do differently with the models available now?

## Camera recipes (Master Shots, 2026-11-01)

- [craft] Can your model hold a fixed-distance lead or follow on a runner for a whole 5-10 s clip without drifting?
- [craft] Does "telephoto, fist passes behind his head, he snaps back" give a believable faked hit, or do you cut the contact in the edit?
- [craft] In a chase, does pairing a handheld card on the hero with a smooth card on the pursuer read as the pursuer gaining?

## Light and material (Color & Light, 2026-11-01)

- [craft] Does your model tint a subject's edges with the surrounding colour, or do characters look pasted onto the plate? What fixes it: prompt, relight pass or comp?
- [craft] Does "backlit" skin give red subsurface glow at the ears and fingers, or an orange cast over the whole face?
- [craft] In a high-contrast shot, which end do you expose for, and does the model respect "blown window" or "silhouetted foreground"?

## Visual structure (The Visual Story, 2026-11-01)

- [craft] Does your model keep flat staging (frontal planes, parallel movement) or deep staging (figures near and far, movement toward the lens) when the prompt asks for it, and does a pan read flatter than a dolly in its output?
- [craft] Did you plan the intensity of a sequence (where contrast peaks, where it calms) before generating the shots, and how did you carry that plan into the prompts?
