from django.shortcuts import render
from django.http import HttpResponse

from .models import BillBoard


def index(request) -> HttpResponse:
    billboards = BillBoard.objects.all()

    context = {
        'billboards': billboards
    }

    return render(
        request,
        'billboard/index.html',
        context,
    )
