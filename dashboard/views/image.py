from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dashboard.helpers import list_image, delete_image


def redirect_view(request):
    return HttpResponseRedirect('/images')


def image_list(request):
    resp = list_image()
    if not resp:
        return render(request, 'dashboard/image_list.html', {})

    images = []
    print(resp)
    for res in resp:
        for r in res['RepoTags']:
            name, tag = r.split(':')
            img_id = res['Id'].split(':')
            image = {
                'repo': name,
                'tag': tag,
                'id': img_id[1][:12]
            }
            images.append(image)
    return render(request, 'dashboard/image_list.html', {'images': images})


class DeleteImage(APIView):

    def post(self, request):
        try:
            image = request.data['name']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        resp = delete_image(image)
        if resp:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
