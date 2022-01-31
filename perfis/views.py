from django.shortcuts import redirect, render
from perfis.models import Perfil, Convite
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework import viewsets, response, status, exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, rendered_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return None
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method == 'POST':
            return (AllowAny(),)


@api_view(['GET'])
@rendered_classes((JSONRenderer, BrowsableAPIRenderer))
def convites(request, *args, **kwargs):
    perfil_logado = get_perfil_logado(request)
    convites = Convite.objects.filter(convidado=perfil_logado)
    serializer = None
    return response.Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@rendered_classes((JSONRenderer, BrowsableAPIRenderer))
def convidar(request, *args, **kwargs):
    try:
        perfil_a_convidar = Perfil.objects.get(id=kwargs['perfil_id'])
    except:
        raise exceptions.NotFound('Perfil não encontrado.')
    perfil_logado = get_perfil_logado(request)
    if perfil_a_convidar != perfil_logado:
        perfil_logado.convidar(perfil_a_convidar)
        return response.Response({'mensagem': f'Convite enviado com sucesso para {perfil_a_convidar.email}.'}, status=status.HTTP_201_CREATED)
    raise exceptions.ParseError(
        'Impossível realizar convite com o id informado.')


@api_view(['POST'])
@rendered_classes((JSONRenderer, BrowsableAPIRenderer))
def aceitar(request, *args, **kwargs):
    perfil_logado = get_perfil_logado(request)
    try:
        convite = Convite.objects.filter(
            convidado=perfil_logado).get(id=kwargs['convite_id'])
    except:
        raise exceptions.NotFound(
            'Perfil com o referido id não foi encontrado.')
    convite.aceitar()
    return response.Response({'mensagem': 'Convite aceito.'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@rendered_classes((JSONRenderer, BrowsableAPIRenderer))
def get_meu_perfil(request, *args, **kwargs):
    perfil_logado = get_perfil_logado(request)
    serializer = None
    return response.Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def index(request):
    return render(request, 'index.html', {'perfis': Perfil.objects.all(), 'perfil_logado': get_perfil_logado(request)})


@login_required
def exibir(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_e_contato = perfil in perfil_logado.contatos.all()
    return render(request, 'perfil.html', {'perfil': perfil, 'perfil_logado': get_perfil_logado(request), 'ja_e_contato': ja_e_contato})


@permission_required('perfis.add_convite', raise_exception=True)
@login_required
def convidar(request, perfil_id):
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.convidar(perfil_a_convidar)

    return redirect('index')


def get_perfil_logado(request):
    return request.user.perfil


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')

    # if perfil_id == 1:
    #    perfil = Perfil('Fábio Henrique', 'fabio@ifb.edu.br', '222222', 'IFB')
    # if perfil_id == 2:
    #    perfil = Perfil('Elon Musk', 'elon.musk@tesla.com', '333333', 'Tesla')
    # print('ID do Perfil:{}'.format(perfil_id))


# print('Hello world')
# Create your views here
