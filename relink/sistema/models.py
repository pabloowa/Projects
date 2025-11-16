from django.db import models
# Create your models here.

class Item(models.Model):
    
    opcoes_status = [
        ('Pendente', 'Pendente'),
        ('Devolvido', 'Devolvido'),
        ('Descartado', 'Descartado'),
    ]

    id_item = models.AutoField(primary_key=True, verbose_name="ID")
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    categoria = models.CharField(max_length=100, verbose_name="Categoria")
    local_encontrado = models.CharField(max_length=100, verbose_name="Local Encontrado")
    responsavel = models.CharField(max_length=100, verbose_name="Responsável")
    data_encontrado = models.DateField()
    status = models.CharField(max_length=20, verbose_name="Status", choices = opcoes_status, default='Pendente')
    foto = models.ImageField(upload_to='fotos_itens/', blank=True, null=True)

    def __str__(self):
        return self.descricao
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"
    
class Solicitacao(models.Model):

    opcoes_solicitacao = [
        ('Pendente', 'Pendente'),
        ('Finalizado', 'Finalizado'),
        ('Não Encontrado', 'Não Encontrado'),
    ]

    id_solicitacao = models.AutoField(primary_key=True, verbose_name="ID")
    nome_solicitante = models.CharField(max_length=200, verbose_name="Nome do Solicitante")
    contato_solicitante = models.CharField(max_length=200, verbose_name="Contato (Telefone/Email)")
    data_solicitacao = models.DateField(auto_now_add=True, verbose_name="Data da Solicitação")
    descricao_item_perdido = models.TextField(verbose_name="Descrição do Item Perdido")
    status = models.CharField(max_length=20,verbose_name="Status da Solicitação", choices=opcoes_solicitacao, default='Pendente')
    foto = models.ImageField(upload_to='fotos_itens/', blank=True, null=True)

    item_encontrado = models.ForeignKey(Item, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Item Encontrado (Linkar)",
        related_name='solicitacoes'
    )

    def __str__(self):
        return f"Solicitação de {self.nome_solicitante} ({self.descricao_item_perdido[:20]}...)"
    

    def save(self, *args, **kwargs):
        if self.item_encontrado:
            
            if self.item_encontrado.status == 'Pendente':
                item = self.item_encontrado
                item.status = 'Devolvido'
                item.save() 
        
            if self.status == 'Pendente':
                self.status = 'Finalizado'
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Solicitação"
        verbose_name_plural = "Solicitações"