from django.shortcuts import redirect, render
from perfis.models import Perfil, Convite

from django.contrib.auth.decorators import login_required, permission_required


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


@login_required
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
