from __future__ import annotations

from typing import Sequence

from codegen.models import DeferredVar, PredefinedFn, Program, expr, stmt
from loguru import logger
from sera.misc import to_snake_case
from sera.models import App, DataCollection, Module, Package


def make_python_api(app: App, collections: Sequence[DataCollection]):
    """Make the basic structure for the API."""
    app.api.ensure_exists()
    app.api.pkg("routes").ensure_exists()

    dep_pkg = app.api.pkg("dependencies")
    for collection in collections:
        make_dependency(collection, dep_pkg)
        route = app.api.pkg("routes").pkg(collection.get_pymodule_name())

        get_route, get_route_fn = make_python_get_api(collection, route)

        program = Program()
        program.import_("__future__.annotations", True)
        program.import_("litestar.Router", True)
        program.import_(get_route.path + "." + get_route_fn, True)

        program.root(
            stmt.LineBreak(),
            lambda ast: ast.assign(
                DeferredVar.simple("router"),
                expr.ExprFuncCall(
                    expr.ExprIdent("Router"),
                    [
                        PredefinedFn.keyword_assignment(
                            "path",
                            expr.ExprConstant(
                                f"/{to_snake_case(collection.name).replace('_', '-')}"
                            ),
                        ),
                        PredefinedFn.keyword_assignment(
                            "route_handlers",
                            PredefinedFn.list(
                                [
                                    expr.ExprIdent(get_route_fn),
                                ]
                            ),
                        ),
                    ],
                ),
            ),
        )

        route.module("route").write(program)


def make_dependency(collection: DataCollection, target_pkg: Package):
    """Generate dependency injection for the service."""
    app = target_pkg.app

    outmod = target_pkg.module(collection.get_pymodule_name())
    if outmod.exists():
        logger.info("`{}` already exists. Skip generation.", outmod.path)
        return

    ServiceNameDep = to_snake_case(f"{collection.name}ServiceDependency")

    program = Program()
    program.import_("__future__.annotations", True)
    program.import_(
        app.services.path
        + f".{collection.get_pymodule_name()}.{collection.get_service_name()}",
        True,
    )

    program.root(
        stmt.LineBreak(),
        lambda ast: ast.func(
            ServiceNameDep, [], expr.ExprIdent(collection.get_service_name())
        )(
            lambda ast01: ast01.return_(
                expr.ExprFuncCall(expr.ExprIdent(collection.get_service_name()), [])
            )
        ),
    )
    outmod.write(program)


def make_python_get_api(
    collection: DataCollection, target_pkg: Package
) -> tuple[Module, str]:
    """Make an endpoint for querying resources"""
    app = target_pkg.app

    ServiceNameDep = to_snake_case(f"{collection.name}ServiceDependency")

    program = Program()
    program.import_("__future__.annotations", True)
    program.import_("typing.Annotated", True)
    program.import_("litestar.get", True)
    program.import_("litestar.Request", True)
    program.import_("litestar.params.Parameter", True)
    program.import_("litestar.di.Provide", True)
    program.import_(app.config.path + ".ROUTER_DEBUG", True)
    program.import_(
        f"{app.api.path}.dependencies.{collection.get_pymodule_name()}.{ServiceNameDep}",
        True,
    )
    program.import_(
        app.services.path
        + f".{collection.get_pymodule_name()}.{collection.get_service_name()}",
        True,
    )
    program.import_("sera.libs.api_helper.parse_query", True)

    func_name = "get_"

    program.root(
        stmt.LineBreak(),
        lambda ast00: ast00.assign(
            DeferredVar.simple("QUERYABLE_FIELDS"),
            expr.ExprConstant(collection.get_queryable_fields()),
        ),
        stmt.PythonDecoratorStatement(
            expr.ExprFuncCall(
                expr.ExprIdent("get"),
                [
                    expr.ExprConstant("/"),
                    PredefinedFn.keyword_assignment(
                        "dependencies",
                        PredefinedFn.dict(
                            [
                                (
                                    expr.ExprConstant("service"),
                                    expr.ExprIdent(f"Provide({ServiceNameDep})"),
                                )
                            ]
                        ),
                    ),
                ],
            )
        ),
        lambda ast10: ast10.func(
            func_name,
            [
                DeferredVar.simple(
                    "limit",
                    expr.ExprIdent(
                        'Annotated[int, Parameter(default=10, description="The maximum number of records to return")]'
                    ),
                ),
                DeferredVar.simple(
                    "offset",
                    type=expr.ExprIdent(
                        'Annotated[int, Parameter(default=0, description="The number of records to skip before returning results")]'
                    ),
                ),
                DeferredVar.simple(
                    "unique",
                    expr.ExprIdent(
                        'Annotated[bool, Parameter(default=False, description="Whether to return unique results only")]'
                    ),
                ),
                DeferredVar.simple(
                    "sorted_by",
                    expr.ExprIdent(
                        "Annotated[list[str], Parameter(description=\"list of field names to sort by, prefix a field with '-' to sort that field in descending order\")]"
                    ),
                ),
                DeferredVar.simple(
                    "group_by",
                    expr.ExprIdent(
                        'Annotated[list[str], Parameter(description="list of field names to group by")]'
                    ),
                ),
                DeferredVar.simple(
                    "fields",
                    expr.ExprIdent(
                        'Annotated[list[str], Parameter(description="list of field names to include in the results")]'
                    ),
                ),
                DeferredVar.simple(
                    "request",
                    expr.ExprIdent("Request"),
                ),
                DeferredVar.simple(
                    "service",
                    expr.ExprIdent(collection.get_service_name()),
                ),
            ],
            is_async=True,
        )(
            stmt.SingleExprStatement(
                expr.ExprConstant("Retrieving records matched a query")
            ),
            lambda ast11: ast11.assign(
                DeferredVar.simple("query", expr.ExprIdent("ServiceQuery")),
                expr.ExprFuncCall(
                    expr.ExprIdent("parse_query"),
                    [
                        expr.ExprIdent("request"),
                        expr.ExprIdent("QUERYABLE_FIELDS"),
                        PredefinedFn.keyword_assignment(
                            "debug",
                            expr.ExprIdent("ROUTER_DEBUG"),
                        ),
                    ],
                ),
            ),
            lambda ast12: ast12.return_(
                expr.ExprFuncCall(
                    expr.ExprIdent("service.get"),
                    [
                        expr.ExprIdent("query"),
                        PredefinedFn.keyword_assignment(
                            "limit", expr.ExprIdent("limit")
                        ),
                        PredefinedFn.keyword_assignment(
                            "offset", expr.ExprIdent("offset")
                        ),
                        PredefinedFn.keyword_assignment(
                            "unique", expr.ExprIdent("unique")
                        ),
                        PredefinedFn.keyword_assignment(
                            "sorted_by", expr.ExprIdent("sorted_by")
                        ),
                        PredefinedFn.keyword_assignment(
                            "group_by", expr.ExprIdent("group_by")
                        ),
                        PredefinedFn.keyword_assignment(
                            "fields", expr.ExprIdent("fields")
                        ),
                    ],
                )
            ),
        ),
    )

    outmod = target_pkg.module("get")
    outmod.write(program)

    return outmod, func_name
