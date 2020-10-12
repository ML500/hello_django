from django.http import Http404, HttpResponseNotFound


class RestrictIds:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        parts = request.path.split('/')
        for part in parts:
            try:
                pk = int(part)
                if pk and pk in range(1, 101):
                    raise Http404
            except ValueError:
                pass

        response = self.get_response(request)
        return response


class FindIds:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        parts = request.path.split('/')
        pks = []
        for part in parts:
            try:
                pks.append(int(part))
            except ValueError:
                pass
        request.pks = pks

        response = self.get_response(request)
        return response

class TextResponse:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        as_text = request.GET.get('text')
