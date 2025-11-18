NOTE: MB the next batch should be more inspired by dr seuss

# Step 1: character design sheet
draw me a character design reference sheet for a handdrawn children book character hero: it's a big tick (the insect), but it has some facial traits resembling slovenian philosopher Alenka Zupančič (rather long oval face, small eyes, glasses, hazelnut long hair, wrinkles, smart and witty air). Make sure it’s a tick with a tick body and an insect face, not some weird humanoid faced freak nightmare fuel.


# Step 2: same thread, page by page
Let’s draw the first page. It’s zoomed it on zupancic the tick, she is visibly sad.


# Step 3: apply a style to each page, can be separate threads but keeping the same gives better consistency

Keep the style consistent with the ethereal/poetic/abstract/ultra stylized vibe we’ve been developing, rather than sticking to the original picture. Do not use precise traits, do not keep details, make it blurry and abstract. The reference image is just a vague guide.
A poetic, abstract digital illustration with a soft, expressive aesthetic. Composed using flat color fields with smooth, blended transitions—colors are vivid yet gentle, like watercolors translated into digital form. No texture. Use a heavily stylized, abstract, whimsical, painterly style characterized by vibrant, bold, saturated colors and soft, blended gradients. Shapes are simplified and fluid, with no hard edges, no outlines, and no visible texture. The aesthetic should feel dreamy and surreal, with a mix of warm and cool tones used expressively rather than realistically. Use stylized, simplified shapes with smooth contours and minimal hard edges. Objects and characters are more silhouettes, abstract geometric shapes, than clear representations. The composition avoids cartoonish features, vector-style graphics, and infographic aesthetics. Lighting is diffuse and atmospheric, with glowing highlights and soft shadows. The overall mood is dreamy, emotional, and imaginative, evoking a sense of quiet magic and visual poetry.
Very colorful, dominating 

## below is what changes
palette is brown and green.
The page is square, 768*768.
As much as you can, keep the likeness to Alenka Zupančič (rather long oval face, small eyes, glasses, hazelnut long hair, wrinkles, smart and witty air)

# Step 4: fix images, outpainting, combination

do some outpainting on this image towards its right, going from a 512*512 square to a 1024*512 rectangle. Keep the original picture on the left just complete it on its right

OR

do some outpainting on this image towards its left, going from a 512*512 square to a 1024*512 rectangle. Keep the original picture on the right just complete it on its left


A poetic, abstract digital illustration with a soft, expressive aesthetic. Composed using flat color fields with smooth, blended transitions—colors are vivid yet gentle, like watercolors translated into digital form. No texture. Use a heavily stylized, abstract, whimsical, painterly style characterized by vibrant, bold, saturated colors and soft, blended gradients. Shapes are simplified and fluid, with no hard edges, no outlines, and no visible texture. The aesthetic should feel dreamy and surreal, with a mix of warm and cool tones used expressively rather than realistically. Use stylized, simplified shapes with smooth contours and minimal hard edges. Objects and characters are more silhouettes, abstract geometric shapes, than clear representations. The composition avoids cartoonish features, vector-style graphics, and infographic aesthetics. Lighting is diffuse and atmospheric, with glowing highlights and soft shadows. The overall mood is dreamy, emotional, and imaginative, evoking a sense of quiet magic and visual poetry.

Very colorful, dominating palette is sky blue and orange. 

# Step 5: img2img to enforce style and dimensions

## positive prompt
stylized abstract crayon drawing of a (fennec:1.3)

stylized abstract crayon drawing, (stylized), (line art), (sketch), symbolic, (abstract:1.2), pencil, (children book), crayon, (colorful), (bright colors), (vivid colors), (vibrant colors), flat colors, child drawing, doodle, messy, crayons, scribble, 4k, high quality, masterpiece, award winning, trending, ultra clear,

blue tones, yellow tones,

<lora:dave2d_lora:.8> dave2d style
<lora:childbook_20230601211222:.7> childbook
<lora:EmoteMakerLora:.3> twitchemote
<lora:18.37:.3> hau_fneg

## negative prompt
(cartoon:1.2), (pixar:1.2), (disney:1.2), (cgi:1.2), (ai:1.2)
deformed, wrong limbs, amputee, duplicate, disfigured, dead, cross eyed, bad anatomy, anorexic, bad proportions, disconnected, missing, extra, missing limbs, too many fingers, disjointed, out of frame, wrinkles, contortionist, contorted limbs, gross, missing arms, missing legs, extra arms, extra legs, fused fingers, malformed, mutation, morbid, mutilated, decomposition, abnormal, mutated, n_bad_prompt_version2, n_badhandsv5-neg, by n_bad-artist, ugly, wrong, bad, artifacts, incomplete, incorrect, censored, amateur, watermark, error, unfinished, signature, lowres, text, cropped, worst quality, low quality, poorly drawn, lousy, blurry, unclear

## settings
STRENGTH 0.35
OUTPUT 1024*512


# Step 6: upscale
# Step 7: publish