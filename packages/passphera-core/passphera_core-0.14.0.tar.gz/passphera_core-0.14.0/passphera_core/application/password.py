from datetime import datetime, timezone

from passphera_core.entities import Password, Generator
from passphera_core.exceptions import DuplicatePasswordException, PasswordNotFoundException
from passphera_core.interfaces import PasswordRepository, GeneratorRepository


class GeneratePasswordUseCase:
    def __init__(
            self,
            password_repository: PasswordRepository,
            generator_repository: GeneratorRepository,
    ):
        self.password_repository: PasswordRepository = password_repository
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, context: str, text: str) -> Password:
        password_entity: Password = self.password_repository.get_by_context(context)
        if password_entity and password_entity.deleted_at is not None:
            raise DuplicatePasswordException(password_entity)
        generator_entity: Generator = self.generator_repository.get()
        password: str = generator_entity.generate_password(text)
        password_entity: Password = Password(context=context, text=text, password=password)
        password_entity.encrypt()
        self.password_repository.save(password_entity)
        return password_entity


class GetPasswordByContextUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self, context: str) -> Password:
        password_entity: Password = self.password_repository.get_by_context(context)
        if not password_entity or password_entity.deleted_at is not None:
            raise PasswordNotFoundException()
        return password_entity


class UpdatePasswordUseCase:
    def __init__(
            self,
            password_repository: PasswordRepository,
            generator_repository: GeneratorRepository,
    ):
        self.password_repository: PasswordRepository = password_repository
        self.generator_repository: GeneratorRepository = generator_repository

    def execute(self, context: str, text: str) -> Password:
        password_entity: Password = self.password_repository.get_by_context(context)
        if not password_entity or password_entity.deleted_at is not None:
            raise PasswordNotFoundException()
        generator_entity: Generator = self.generator_repository.get()
        password: str = generator_entity.generate_password(text)
        password_entity.text = text
        password_entity.password = password
        password_entity.updated_at = datetime.now(timezone.utc)
        password_entity.encrypt()
        self.password_repository.update(password_entity)
        return password_entity


class DeletePasswordUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self, context: str) -> None:
        password_entity: Password = self.password_repository.get_by_context(context)
        if not password_entity or password_entity.deleted_at is not None:
            raise PasswordNotFoundException()
        password_entity.deleted_at = datetime.now(timezone.utc)
        self.password_repository.delete(password_entity)


class GetAllPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self) -> list[Password]:
        return self.password_repository.list()


class DeleteAllPasswordsUseCase:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository: PasswordRepository = password_repository

    def execute(self) -> None:
        self.password_repository.flush()
