from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

ACTIVE_CLASSES = "bg-blue-700 text-white font-semibold"
INACTIVE_CLASSES = "text-white/80 hover:text-white hover:bg-blue-700/50"

@register.simple_tag(takes_context=True)
def nav_active(context, urlname, *args, **kwargs):
    """
    Retorna classes CSS para destacar item ativo no menu lateral.
    Exemplo de uso no template:
    <a href="{% url 'accounts:dashboard' %}" class="{% nav_active 'accounts:dashboard' %}">Dashboard</a>
    """
    request = context["request"]
    path = request.path

    try:
        base_url = reverse(urlname, args=args, kwargs=kwargs)
    except NoReverseMatch:
        return INACTIVE_CLASSES

    # Para URLs exatas como dashboard
    if path == base_url:
        return ACTIVE_CLASSES
    
    # Para seções (como alunos, financeiro, etc.), verifica se a URL atual pertence à seção
    if urlname.startswith(('alunos:', 'financeiro:', 'frequencia:', 'relatorios:', 'treinos:')):
        app_name = urlname.split(':')[0]
        if path.startswith(f'/{app_name}/'):
            return ACTIVE_CLASSES
    
    # Para outras URLs, verifica se começa com a base URL
    if path.startswith(base_url) and base_url != '/':
        return ACTIVE_CLASSES
        
    return INACTIVE_CLASSES
