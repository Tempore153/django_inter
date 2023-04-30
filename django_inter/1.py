from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


@csrf_exempt
@require_GET
def paraphrase(request):

    if request.method == "GET":

        input_tree = request.GET.get('tree', None)
        limit = int(request.GET.get('limit', 20))


        paraphrased_trees = func.permute_nouns(input_tree)
        response_data = {


                'input_tree': input_tree,
                'paraphrased_tree': paraphrased_trees,

        }


        # Повернення відповіді в JSON-форматі
    return JsonResponse(response_data)