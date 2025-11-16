from django.contrib import admin
from .models import Item, Solicitacao
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'link_para_edicao', 'descricao', 'categoria', 'local_encontrado',
                    'responsavel', 'status', 'data_encontrado', 'mostrar_foto')
    list_filter = ('status', "categoria")
    search_fields = ['descricao']

    @admin.display(description="Miniatura")
    def mostrar_foto(self, obj):
        if obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" width="50" height="50" />')
        else:
            return "Sem Foto"

    @admin.display(description="Editar")
    def link_para_edicao(self, obj):
        link = f"/admin/sistema/item/{obj.pk}/change/"

        return format_html(
            '<a href="{}"><img src="/static/images/lapis.png" width="20" height="20" style="margin-left: 8px; margin-right: 10px; "></a>',
            link
        )


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('id_solicitacao', 'link_para_edicao2', 'nome_solicitante', 'descricao_item_perdido',
                    'data_solicitacao', 'status', 'item_encontrado', 'mostrar_foto')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('nome_solicitante', 'descricao_item_perdido')
    raw_id_fields = ('item_encontrado',)

    @admin.display(description="Editar")
    def link_para_edicao2(self, obj):
        link = f"/admin/sistema/solicitacao/{obj.pk}/change/"

        return format_html(
            '<a href="{}"><img src="/static/images/lapis.png" width="20" height="20" style="margin-left: 8px; margin-right: 10px; "></a>',
            link
        )
    
    @admin.display(description="Foto do Item")
    def mostrar_foto(self, obj):
        if obj.foto:
            return mark_safe(f'<img src="{obj.foto.url}" width="50" height="50" />')
        else:
            return "Sem Foto"


# Register your models here.
admin.site.register(Item, ItemAdmin)
