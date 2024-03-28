from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key="ulxWhbY1nxtlA240URf6"
)

result = CLIENT.infer("board.jpeg", model_id="chessboard-1hk4y/3")
print(result)

