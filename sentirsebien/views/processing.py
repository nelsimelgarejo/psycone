from django.forms.utils import flatatt
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from sentirsebien.models import Perfil, ItemsTopicos, ComponenteBienestar, RespuestasPuente, ResultadoPerfil
from django.http import JsonResponse
import random

def primer_item(request):
    topico = request.GET.get('topico', None)
    item = ItemsTopicos.objects.filter(topico = topico).order_by('?').first()
    data = {
        'id': item.id,
        'item': item.item,
        'topico': topico
    }
    return JsonResponse(data)

def respuesta_sa_mental(request):
    perfil = get_object_or_404(Perfil, usuario__username = request.user)
    topico = request.POST.get('topico', None)
    id_item_topico = request.POST.get('item_topico', None)

    item = get_object_or_404(ItemsTopicos, id=id_item_topico)

    topicos_respuesta = {
        'sa_mental':request.POST.get('sa_mental_value', None), 
        'ae_depresion': request.POST.get('ae_depresion_value', None),
        'ap_social': request.POST.get('ap_social_value', None),
        'asertividad': request.POST.get('asertividad_value', None),
        'vi_pareja': request.POST.get('vi_pareja_value', None)
        } 
    
    respuesta = topicos_respuesta[topico]

    RespuestasPuente.objects.create(
        perfil = perfil, 
        item = item,
        respuesta = respuesta
    )
    items_respondidos = []
    for respuesta in RespuestasPuente.objects.filter(perfil=perfil, item__topico = topico):
        items_respondidos.append(respuesta.item) 
    items_total = get_list_or_404(ItemsTopicos, topico = topico)
    items_disponibles = list(set(items_total) - set(items_respondidos))

    if len(items_disponibles) <=0:
        data = {
            'estado': False,
            'id': 12,
            'item': 'Finalizo',
            'topico': topico
        }
        return JsonResponse(data)

    item_lista = random.sample(items_disponibles,1)
    item_new = item = item_lista[0]

    data = {
        'estado': True,
        'id': item_new.id,
        'item': item_new.item,
        'topico': topico
    }
    return JsonResponse(data)