from .services_dependencies import ORMSessionDependency


def get_client_session(orm_session: ORMSessionDependency): ...
