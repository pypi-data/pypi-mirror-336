from dotenv import load_dotenv
import os
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN","")
s3_bucket = "ft-vaia"
def process_image_with_pixtral(image_url: str, pixtral_api_key: str='') -> str:
    from huggingface_hub import InferenceClient
    client = InferenceClient(api_key=HF_TOKEN)
    # text = f"Image URL: {image_url} "
    text = ""
    for message in client.chat_completion(
	model="meta-llama/Llama-3.2-11B-Vision-Instruct",
	messages=[
		{
			"role": "user",
			"content": [
				{"type": "image_url", "image_url": {"url": image_url}},
				{"type": "text", "text": "Provide a clear, detailed description of the content in 100-200 words. Focus on summarizing the key elements, features, and context in an informative way, without referring to any specific source or using phrases like 'this image.'"},
			],
		}
        ],
        max_tokens=500,
        stream=True,
    ):
        text += message.choices[0].delta.content
    return text

def process_image_with_dedicated_llama(image_url : str) -> str:
    from openai import OpenAI
    VAIA_IMAGE_TO_TEXT_URL=os.getenv("VAIA_IMAGE_TO_TEXT_URL","")
    client_llama = OpenAI(
        base_url=VAIA_IMAGE_TO_TEXT_URL, 
        api_key=HF_TOKEN 
    )
    text = ""
    chat_completion = client_llama.chat.completions.create(
        model="tgi",
        messages=[
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            },
            {
                "type": "text",
                "text": "Provide a clear, detailed description of the content in 100-200 words. Focus on summarizing the key elements, features, and context in an informative way, without referring to any specific source or using phrases like 'this image.'."
            }
        ]
    }
],
	top_p=None,
	temperature=None,
	max_tokens=150,
	stream=True,
	seed=None,
	frequency_penalty=None,
	presence_penalty=None
)

    for message in chat_completion:
        text += message.choices[0].delta.content
    return text
