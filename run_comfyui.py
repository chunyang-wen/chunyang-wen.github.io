import json
import urllib.request
import urllib.parse
import time
import os

SERVER_ADDRESS = "127.0.0.1:8000"

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
    # Load workflow
    workflow_path = "/Users/chunyangwen/Documents/opensource/chunyang-wen.github.io/workflows/image-gen.json"
    if not os.path.exists(workflow_path):
        print(f"Workflow file not found at {workflow_path}")
        return

    with open(workflow_path, "r", encoding="utf-8") as f:
        prompt_workflow = json.load(f)

    print("Queueing workflow...")
    q_res = queue_prompt(prompt_workflow)
    if not q_res or 'prompt_id' not in q_res:
        print("Could not get prompt_id from server. Make sure ComfyUI is running at 127.0.0.1:8188")
        return

    prompt_id = q_res['prompt_id']
    print(f"Workflow queued. ID: {prompt_id}")

    print("Waiting for generation to complete (this might take a while)...")
    last_status_print = time.time()
    while True:
        history = get_history(prompt_id)
        if history and prompt_id in history:
            print("Generation finished!")
            break
        
        # print a dot every 2 seconds to show progress
        if time.time() - last_status_print > 2:
            print(".", end="", flush=True)
            last_status_print = time.time()
        time.sleep(0.5)
    
    print() # New line after dots

    history_data = history[prompt_id]
    outputs = history_data.get('outputs', {})
    
    images_saved = 0
    for node_id, node_output in outputs.items():
        if 'images' in node_output:
            for i, image in enumerate(node_output['images']):
                print(f"Downloading image {image['filename']}...")
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                if image_data:
                    out_path = f"/Users/chunyangwen/Documents/opensource/chunyang-wen.github.io/output_{node_id}_{i}_{image['filename']}"
                    with open(out_path, "wb") as f:
                        f.write(image_data)
                    print(f"Saved generated image to: {out_path}")
                    images_saved += 1
    
    if images_saved == 0:
        print("No images were found in the output.")

if __name__ == "__main__":
    main()
