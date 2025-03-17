from sys import meta_path

from gradio_client import Client
from watchfiles import awatch
import requests
import asyncio
from gradio_client import Client, file
import shutil
from cfg import hf_token


async def generate3d(photo):
	client = Client("TencentARC/InstantMesh", hf_token=hf_token)
	result = client.predict(
			input_image=file(photo), #input photo
			sample_steps=75,
			sample_seed=42,
			api_name="/generate_mvs")

	model = client.predict(
			api_name="/make3d")

	print(model[1])

	directory = 'FastApi/app/model'

	shutil.copy(model[1], directory)

	return model[1]

