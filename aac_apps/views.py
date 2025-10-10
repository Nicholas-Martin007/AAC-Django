from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
# import torch
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from transformers import AutoModelForCausalLM
# from peft import PeftModelForCausalLM
from aac_apps.models import Kartu
# from .tokenizer import FinetuneTokenizer


@csrf_exempt
def ls_kartu(request):
    if request.method == "GET":
        ls_kartu = Kartu.objects.all()
        return JsonResponse([kartu.to_json() for kartu in ls_kartu], safe=False)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            kartu = Kartu.from_json(data)
            kartu.save()
            return JsonResponse(kartu.to_json(), status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)  


@csrf_exempt
def detail_kartu(request, kartu_id):
    try:
        kartu = Kartu.objects.get(kartu_id=kartu_id)
        if request.method == "GET":
            return JsonResponse(kartu.to_json())

        elif request.method == "DELETE":
            kartu.delete()
            return JsonResponse({"message": "Kartu deleted successfully"})

        elif request.method == "PUT":
            data = json.loads(request.body)
            kartu.label = data.get("label", kartu.label)
            kartu.gambar = data.get("gambar", kartu.gambar)
            kartu.kategori = data.get("kategori", kartu.kategori)
            kartu.save()
            return JsonResponse(kartu.to_json())

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Kartu not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# MODEL_PATH = "/Users/Nicmar/Downloads/_QLoRA_proof/"
# BASE_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# tokenizer = FinetuneTokenizer(BASE_MODEL).get_tokenizer()
# base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)
# base_model.resize_token_embeddings(len(tokenizer))
# qlora_model = PeftModelForCausalLM.from_pretrained(base_model, MODEL_PATH)
# model = qlora_model.merge_and_unload().to(DEVICE)


# @api_view(["POST"])
# def generate_story(request):
#     data = request.data
#     input_list = data.get("input", [])  # ["kelas", "meja", "pensil"]

#     print("Input List:", input_list)
#     prompt = tokenizer.apply_chat_template(
#         [{"role": "user", "content": json.dumps(input_list)}],
#         tokenize=False,
#         add_generation_prompt=True,
#     )
#     input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(DEVICE)

#     output = model.generate(
#         input_ids=input_ids,
#         max_new_tokens=200,
#         temperature=0.8,
#         top_p=0.9,
#         do_sample=True,
#         eos_token_id=tokenizer.eos_token_id,
#         pad_token_id=tokenizer.pad_token_id,
#     )

#     story = tokenizer.decode(output[0], skip_special_tokens=True)
#     return Response({"story": story})
