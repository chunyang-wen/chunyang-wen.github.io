import json
import urllib.request
import urllib.parse
import time
import os
import argparse
import random

SERVER_ADDRESS = "127.0.0.1:8000"
WORKFLOW_PATH = "/Users/chunyangwen/Documents/opensource/chunyang-wen.github.io/workflows/flux_dev_full_text_to_image.json"

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except Exception as e:
        print(f"Failed to queue prompt: {e}. Is ComfyUI running?")
        return None

def get_history(prompt_id):
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Failed to get history: {e}")
        return None

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/view?{url_values}") as response:
            return response.read()
    except Exception as e:
        print(f"Failed to get image: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate 600x600 image via ComfyUI (Flux).")
    parser.add_argument("--prompt", type=str, required=True, help="The positive text prompt.")
    parser.add_argument("--negative_prompt", type=str, default="text, watermark, ugly, low quality", help="The negative text prompt.")
    parser.add_argument("--out_path", type=str, required=True, help="The output path for the image.")
    args = parser.parse_args()

    if not os.path.exists(WORKFLOW_PATH):
        print(f"Workflow file not found at {WORKFLOW_PATH}")
        return

    with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
        prompt_workflow = json.load(f)

    # Node 41 is positive text prompt (Flux)
    if "41" in prompt_workflow:
        prompt_workflow["41"]["inputs"]["clip_l"] = args.prompt
        prompt_workflow["41"]["inputs"]["t5xxl"] = args.prompt
    
    # Node 27 defines latent size
    if "27" in prompt_workflow:
        prompt_workflow["27"]["inputs"]["width"] = 600
        prompt_workflow["27"]["inputs"]["height"] = 600
    
    # Node 31 is KSampler, randomize seed
    if "31" in prompt_workflow:
        prompt_workflow["31"]["inputs"]["seed"] = random.randint(1, 1000000000000000)

    print("Queueing workflow...")
    q_res = queue_prompt(prompt_workflow)
    if not q_res or 'prompt_id' not in q_res:
        print("Could not get prompt_id from server. Make sure ComfyUI is running at 127.0.0.1:8000")
        return

    prompt_id = q_res['prompt_id']
    print(f"Workflow queued. ID: {prompt_id}")

    print("Waiting for generation to complete...")
    while True:
        history = get_history(prompt_id)
        if history and prompt_id in history:
            print("Generation finished!")
            break
        time.sleep(1)

    history_data = history[prompt_id]
    outputs = history_data.get('outputs', {})
    
    images_saved = False
    for node_id, node_output in outputs.items():
        if 'images' in node_output:
            for image in node_output['images']:
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                if image_data:
                    os.makedirs(os.path.dirname(args.out_path), exist_ok=True)
                    with open(args.out_path, "wb") as f:
                        f.write(image_data)
                    print(f"Saved generated image to: {args.out_path}")
                    images_saved = True
                    break
        if images_saved:
            break
    
    if not images_saved:
        print("No images were found in the output. Please check the workflow or ComfyUI logs.")

if __name__ == "__main__":
    main()
