# Merge two ComfyUI workflow .json files

I am aware you can basically accomplish this by copy/pasting, but I was struggling with losing work when I restarted RunDiffusion due to a weird bug with the manager disappearing, and wanted something I had a bit more control over. This is tested on a moderately complex workflow, but nothing too crazy so there are bound to be bugs.

The y offset is so the two workflows don't load on top of each other. It defaults to 1000 px, but I tend to require more, but either way I made it an optional parameter.

## Usage 
merge_comfy_workflows.py [-h] [--y_offset Y_OFFSET] file1 file2 output_file

e.g.:
> python merge_comfy_workflows.py ./workflows/rundiffusion-CogVideoX5b-I2V-with-faceswap.json ./workflows/rundiffusion-flux-image-upscaler.json ./workflows/merged.json 
