from django.shortcuts import render

# Create your views here.
# pages/views.py
from django.template import loader
from django.forms.fields import CharField, ImageField
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import UploadImageForm
from .models import UploadImage

import openai
from time import sleep
import base64
import requests
from PIL import Image
from io import BytesIO

API_KEY = "nzUrLgEmMb9zOX6GFHgfPzRIFLyqfc3MHXwz8A92ANwYHPQgoO" #Paste your own Plant Detection API Key
openai.api_key = #paste your own Open AI api key here (https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key)
result = ''
result2 = ''
name = ''
form = 0
def test(request):
    global result
    global result2
    global name
    global form
    print('Form Submission Detected...')
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            location = form.cleaned_data['location']
            img_file = request.FILES['image']
            print(location)

            dict1 = identify_plant([img_file])

            name = dict1["suggestions"][0]["plant_name"]
            print(name)

            string = "Is " + name + " an invasive species in " + location + "?"  # get the location from frontend
            string2 = "Briefly explain and describe the history of" + name + ". If this plant is invasive, explain why it's harmful to the ecosystem."

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a chatbot"},
                    {"role": "user", "content": string},
                ]
            )

            result = ''
            for choice in response.choices:
                result += choice.message.content

            print(result)

            response2 = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a chatbot"},
                    {"role": "user", "content": string2},
                ]
            )

            result2 = ''
            for choice in response2.choices:
                result2 += choice.message.content

            print(result2)
            print(name)
            return redirect("success")
    else:
        form = UploadImageForm





    return render(request, 'home.html', {'form': form})

def success(request):
    global result
    global result2
    global name
    global form # this is the upload image form, idk how to get the image from it
    return render(request, 'success.html', {'name': name, 'result':result, 'result2': result2, 'image':form}) # need to pass the image as a variable here

def encode_file(file_name):
    #with open(file_name, "rb") as file:
        return base64.b64encode(file_name.read()).decode("ascii")


def identify_plant(file_names):
    params = {
        "images": [encode_file(img) for img in file_names],

        "latitude": 49.1951239,
        "longitude": 16.6077111,
        "datetime": 1582830233,
        # Modifiers docs: https://github.com/flowerchecker/Plant-id-API/wiki/Modifiers
        "modifiers": ["crops_fast", "similar_images"],
    }

    headers = {
        "Content-Type": "application/json",
        "Api-Key": API_KEY,
    }

    response = requests.post("https://api.plant.id/v2/enqueue_identification",
                             json=params,
                             headers=headers).json()

    return get_result(response["id"])


def get_result(identification_id):
    params = {
        "plant_language": "en",
        # Plant details docs: https://github.com/flowerchecker/Plant-id-API/wiki/Plant-details
        "plant_details": ["common_names",
                          "edible_parts",
                          "gbif_id",
                          "name_authority",
                          "propagation_methods",
                          "synonyms",
                          "taxonomy",
                          "url",
                          "wiki_description",
                          "wiki_image",
                          ],
    }

    headers = {
        "Content-Type": "application/json",
        "Api-Key": API_KEY,
    }

    endpoint = "https://api.plant.id/v2/get_identification_result/"

    while True:
        sleep(0.5)
        response = requests.post(endpoint + str(identification_id),
                                 json=params,
                                 headers=headers).json()
        if response["suggestions"] is not None:
            return response



