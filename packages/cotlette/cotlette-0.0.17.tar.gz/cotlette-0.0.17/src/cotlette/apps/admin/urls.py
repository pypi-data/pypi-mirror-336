import os

from fastapi import APIRouter, Request
from cotlette.shortcuts import render

from cotlette.conf import settings

router = APIRouter()


def url_for(endpoint, **kwargs):
    """
    Функция для генерации URL на основе endpoint и дополнительных параметров.
    В данном случае endpoint игнорируется, так как мы используем только filename.
    """
    if not kwargs:
        return f"/{endpoint}"
    
    path = f"/{endpoint}"
    for key, value in kwargs.items():
        path += f"/{value}"
    
    return path


@router.get("/", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="pages/index.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test",
        "config": settings,
    })

@router.get("/accounts_login", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="accounts/login.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test",
        "config": settings,
    })

@router.get("/accounts_register", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="accounts/register.html", context={
        "url_for": url_for,
        "parent": "home",
        "segment": "test",
        "config": settings,
    })

@router.get("/pages_tables", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="pages/tables.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": settings,
    })



@router.get("/pages_billing", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="pages/billing.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": settings,
    })

@router.get("/pages_profile", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="pages/profile.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": settings,
    })

@router.get("/accounts_password_change", response_model=None)
async def test(request: Request):    
    return render(request=request, template_name="accounts/password_change.html", context={
        "url_for": url_for,
        "parent": "/",
        "segment": "test",
        "config": settings,
    })