from django.forms.utils import flatatt
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from sentirsebien.models import Perfil, ItemsTopicos, ComponenteBienestar, RespuestasPuente, ResultadoPerfil
from django.http import JsonResponse
import random

def primer_item(request):
    topico = request.GET.get('topico', None)
   
    if topico == 'ae_depresion':
        ae_depresion = ['das_ansiedad', 'das_estres', 'das_depresion']
        item_lista = random.sample(ae_depresion,1)
        sub_topico = item_lista[0]
        item = ItemsTopicos.objects.filter(topico = sub_topico).order_by('?').first()
    else:
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
    
    if topico == 'ae_depresion':
        ae_depresion = ['das_ansiedad', 'das_estres', 'das_depresion']
        for respuesta in RespuestasPuente.objects.filter(perfil=perfil, item__topico__in = ae_depresion):
            items_respondidos.append(respuesta.item) 
        items_total = get_list_or_404(ItemsTopicos, topico__in = ae_depresion)
        items_disponibles = list(set(items_total) - set(items_respondidos))
    else:
        for respuesta in RespuestasPuente.objects.filter(perfil=perfil, item__topico = topico):
            items_respondidos.append(respuesta.item) 
        items_total = get_list_or_404(ItemsTopicos, topico = topico)
        items_disponibles = list(set(items_total) - set(items_respondidos))

    if len(items_disponibles) <=0:
        resultado_process(perfil, topico)
        RespuestasPuente.objects.filter(perfil=perfil).delete()
        data = {
            'estado': False,
            'id': 12,
            'item': 'Finalizo',
            'topico': topico
        }
        return JsonResponse(data)

    item_lista = random.sample(items_disponibles,1)
    item_new = item_lista[0]

    data = {
        'estado': True,
        'id': item_new.id,
        'item': item_new.item,
        'topico': topico
    }
    return JsonResponse(data)


def resultado_process(perfil, topico):
    if topico == 'ae_depresion':
        ae_depresion = ['das_ansiedad', 'das_estres', 'das_depresion']
        resultado = ''
        for das_component in ae_depresion:
            contador = 0
            for respuesta_item in RespuestasPuente.objects.filter(perfil=perfil, item__topico = das_component):
                contador += respuesta_item.respuesta
            if das_component == 'das_estres':
                if contador <= 12:
                    resultado = 'low'
                elif contador <= 18:
                    resultado = 'medium'
                else:
                    resultado = 'high'
            else:
                if contador <= 9:
                    resultado = 'low'
                elif contador <= 16:
                    resultado = 'medium'
                else:
                    resultado = 'high'
            ResultadoPerfil.objects.create(
                perfil = perfil,
                topico = das_component,
                puntaje = contador,
                resultado = resultado
            )
    else:       
        contador = 0
        resultado = ''
        for respuesta_item in RespuestasPuente.objects.filter(perfil=perfil, item__topico = topico):
            if respuesta_item.item.inverso:
                contador += (-1)*respuesta_item.respuesta
            else:
                contador += respuesta_item.respuesta
    
        if topico == 'sa_mental':
            if contador <= 46:
                resultado = 'low'
            elif contador <= 66:
                resultado = 'medium'
            else:
                resultado = 'high'

        if topico == 'asertividad':
            if contador <= 32:
                resultado = 'low'
            elif contador <= 46:
                    resultado = 'medium'
            else:
                resultado = 'high'
        
        if topico == 'ap_social':
            if contador <= 17:
                resultado = 'low'
            elif contador <= 21:
                    resultado = 'medium'
            else:
                resultado = 'high'

        if topico == 'vi_pareja':
            if contador <= 10:
                resultado = 'low'
            elif contador <= 23:
                    resultado = 'medium'
            else:
                resultado = 'high'

        ResultadoPerfil.objects.create(
                perfil = perfil,
                topico = topico,
                puntaje = contador,
                resultado = resultado
            )