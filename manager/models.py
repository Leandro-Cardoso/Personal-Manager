from django.db import models
from django.core.exceptions import ValidationError
from month.models import MonthField

class Income(models.Model):
    name = models.CharField("Nome", max_length=200)
    description = models.TextField("Descrição", null=True, blank=True)
    started_at = MonthField("Mês de Início", null=False, blank=False)
    ended_at = MonthField("Mês de Fim", null=True, blank=True)
    is_continuous = models.BooleanField("É Contínua (Sem Fim Definido)?", default=False)

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"

    def clean(self):
        """
        Validação entre campos.
        """
        if self.is_continuous and self.ended_at is not None:
            raise ValidationError(
                {'is_continuous': "Uma receita contínua não pode ter um 'Mês de Fim' definido."},
                code='invalid_continuous_end'
            )

        if not self.is_continuous and self.ended_at is not None:
            if self.ended_at < self.started_at:
                raise ValidationError(
                    {'ended_at': "O 'Mês de Fim' não pode ser anterior ao 'Mês de Início'."},
                    code='invalid_end_date'
                )

    def save(self, *args, **kwargs):
        """
        Salvar e ajustar campos.
        """
        self.full_clean() 
        
        if self.is_continuous:
            self.ended_at = None
            
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Exibir dados.
        """
        started_str = self.started_at.strftime('%m/%Y')
        
        if self.is_continuous:
            return f"{self.name} (Desde {started_str} - Contínua)"
        
        if self.ended_at:
            ended_str = self.ended_at.strftime('%m/%Y')
            
            if self.started_at == self.ended_at:
                return f"{self.name} ({started_str})"
            else:
                return f"{self.name} ({started_str} - {ended_str})"
        
        return f"{self.name} ({started_str} - Erro de data)"

# TODO: Gastos
