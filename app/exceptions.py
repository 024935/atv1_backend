"""Exceções de domínio usadas pelas services/controllers para sinalizar erros HTTP."""

from __future__ import annotations


class BadRequestException(Exception):
    """Erro de negócio equivalente a um HTTP 400 (ex.: referência inexistente)."""


class ConflictException(Exception):
    """Erro de negócio equivalente a um HTTP 409 (ex.: violação de unicidade)."""


class NotFoundException(Exception):
    """Erro de negócio equivalente a um HTTP 404 (recurso não encontrado)."""


class ValidationException(Exception):
    """Carrega a lista de mensagens de erro de cada campo inválido do DTO de entrada."""

    def __init__(self, errors: list[str]) -> None:
        super().__init__("Erro de validação.")
        self.errors = errors
