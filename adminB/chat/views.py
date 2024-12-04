from django.views.generic import View
from django.shortcuts import render


class LobbyView(View):
    def get(self, request):
        return render(request, '')