import gradio as gr
import asyncio
import websockets
import json
import time
from threading import Thread

# WebSocket URL for backend inference
WS_URL = "ws://localhost:8000/ws/infer"

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.loop = asyncio.new_event_loop()
        self.connected = False
        self.response = None
        self.error = None

    async def connect(self):
        self.ws = await websockets.connect(self.url)
        self.connected = True

    async def send(self, message):
        if not self.connected:
            await self.connect()
        await self.ws.send(message)

    async def receive(self):
        try:
            response = await self.ws.recv()
            return response
        except Exception as e:
            self.error = str(e)
            return None

    async def close(self):
        if self.ws:
            await self.ws.close()
            self.connected = False

    def run_inference(self, prompt, settings):
        async def _run():
            try:
                await self.connect()
                request = json.dumps({"prompt": prompt, "settings": settings})
                await self.send(request)
                response = await self.receive()
                return response
            except Exception as e:
                return json.dumps({"error": str(e)})
            finally:
                await self.close()
        return self.loop.run_until_complete(_run())

ws_client = WebSocketClient(WS_URL)

def generate_response(prompt, temperature, max_tokens):
    settings = {
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    start_time = time.time()
    response_json = ws_client.run_inference(prompt, settings)
    response = json.loads(response_json)
    if "error" in response:
        return f"Error: {response['error']}", "", ""
    result = response.get("result", {})
    output = result.get("output", "")
    inference_time = result.get("inference_time", 0)
    resource_usage = result.get("resource_usage", {})
    mem_rss = resource_usage.get("memory_rss_mb", 0)
    cpu_percent = resource_usage.get("cpu_percent", 0)
    metrics = f"Inference time: {inference_time:.2f}s | Memory RSS: {mem_rss:.2f} MB | CPU usage: {cpu_percent:.2f}%"
    return output, metrics, "You can save or export the results from here."

with gr.Blocks() as demo:
    gr.Markdown("# Model Inference Interface")
    with gr.Row():
        with gr.Column(scale=3):
            prompt_input = gr.Textbox(label="Input Prompt", lines=4, placeholder="Enter your prompt here...")
            model_select = gr.Dropdown(label="Select Model", choices=["flux1-k-dev-q2_k.gguf"], value="flux1-k-dev-q2_k.gguf")
            with gr.Accordion("Inference Settings", open=True):
                temperature = gr.Slider(minimum=0.0, maximum=1.0, value=0.7, label="Temperature")
                max_tokens = gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max Tokens")
            generate_btn = gr.Button("Generate")
        with gr.Column(scale=4):
            output_text = gr.Textbox(label="Output", lines=10, interactive=False)
            metrics_text = gr.Textbox(label="Inference Metrics", interactive=False)
            save_export_info = gr.Textbox(label="Save/Export Info", interactive=False)

    def on_generate_click(prompt, temperature, max_tokens):
        return generate_response(prompt, temperature, max_tokens)

    generate_btn.click(on_generate_click, inputs=[prompt_input, temperature, max_tokens], outputs=[output_text, metrics_text, save_export_info])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
