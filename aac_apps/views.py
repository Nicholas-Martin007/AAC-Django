from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aac_apps.models import Kartu, KisahSosial, KartuKisah


@csrf_exempt
def ls_kartu(request):
    if request.method == "GET":
        ls_kartu = Kartu.objects.filter(flag=False)
        return JsonResponse([k.to_json() for k in ls_kartu], safe=False)

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

        elif request.method == "PUT":
            data = json.loads(request.body)
            kartu.label = data.get("label", kartu.label)
            kartu.gambar = data.get("gambar", kartu.gambar)
            kartu.kategori = data.get("kategori", kartu.kategori)
            kartu.flag = data.get("flag", kartu.flag)
            kartu.save()
            return JsonResponse(kartu.to_json())

        elif request.method == "DELETE":
            kartu.flag = True
            kartu.save()
            return JsonResponse({"message": "Kartu telah dihapus",})

        else:
            return JsonResponse({"error": "Error, tidak bisa"}, status=405)

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Kartu tidak ada"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def ls_kisah(request):

    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        kisah_list = KisahSosial.objects.all().order_by("-created_at") # - karena descending
        response = []
        for kisah in kisah_list:
            print("Ini kisahnya")
            print(kisah)
            kartu_ids = kisah.kartu.all().values_list("kartu_id", flat=True)
            response.append({
                "kisah_id": kisah.kisah_id,
                "input_text": kisah.input_text,
                "output_text": kisah.output_text,
                "created_at": kisah.created_at.isoformat(),
                "kartu_ids": list(kartu_ids),
                "score_human": kisah.score_human,
                "score_perplexity": kisah.score_perplexity,
            })
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def detail_kisah(request, kisah_id):
    try:
        kisah = KisahSosial.objects.get(kisah_id=kisah_id)

        if request.method == "GET":
            kartu_ids = kisah.kartu.all().values_list("kartu_id", flat=True)
            return JsonResponse({
                "kisah_id": kisah.kisah_id,
                "input_text": kisah.input_text,
                "output_text": kisah.output_text,
                "created_at": kisah.created_at.isoformat(),
                "kartu_ids": list(kartu_ids),
                "score_human": kisah.score_human,
                "score_perplexity": kisah.score_perplexity,
            })

        elif request.method == "PUT":
            data = json.loads(request.body)
            if "ratings" in data:
                kisah.score_human = data["ratings"]
                kisah.save()
                return JsonResponse({"message": "Ratings telah diupdate"})
            return JsonResponse({"error": "Tidak ada rating"}, status=400)

        else:
            return JsonResponse({"error": "Error 405"}, status=405)

    except KisahSosial.DoesNotExist:
        return JsonResponse({"error": "Error 404"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["POST"])
def generate_story(request):
    try:
        data = request.data
        kartu_ids = data.get("kartu_ids", [])
        if not kartu_ids:
            return Response({"error": "Kartu diperlukan"}, status=400)

        kartus = []
        for k_id in kartu_ids:
            try:
                k = Kartu.objects.get(kartu_id=k_id)
                kartus.append(k)
            except Kartu.DoesNotExist:
                return Response({"error": f"Kartu with id {k_id} not found"}, status=404)

        input_labels = [k.label for k in kartus]
        input_text = ", ".join(input_labels)
        generated_story = f"Cerita berdasarkan kartu: {input_text}"

        kisah = KisahSosial.objects.create(
            input_text=input_text,
            output_text=generated_story,
            score_human=0.0,
            score_perplexity=0.0,
        )

        for idx, k in enumerate(kartus):
            KartuKisah.objects.create(kartu=k, kisah=kisah, order=idx)

        response_data = {
            "kisah_id": kisah.kisah_id,
            "input_text": kisah.input_text,
            "output_text": kisah.output_text,
            "created_at": kisah.created_at.isoformat(),
            "kartu_ids": kartu_ids,
        }

        return Response(response_data, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@csrf_exempt
def all_kartu(request):
    if request.method == "GET":
        ls_kartu = Kartu.objects.all()
        return JsonResponse([k.to_json() for k in ls_kartu], safe=False)



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
