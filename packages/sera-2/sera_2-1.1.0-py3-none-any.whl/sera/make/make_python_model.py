from __future__ import annotations

from typing import Sequence

from codegen.models import DeferredVar, PredefinedFn, Program, expr, stmt
from sera.misc import assert_isinstance, filter_duplication
from sera.models import DataProperty, ObjectProperty, Package, Schema


def make_python_data_model(schema: Schema, target_pkg: Package):
    """Generate public classes for the API from the schema."""
    for cls in schema.topological_sort():
        program = Program()
        program.import_("__future__.annotations", True)
        program.import_("msgspec", False)
        # program.import_("dataclasses.dataclass", True)

        # program.root(stmt.PythonStatement("@dataclass"))
        cls_ast = program.root.class_(cls.name, [expr.ExprIdent("msgspec.Struct")])
        for prop in cls.properties.values():
            if prop.is_private:
                # skip private fields as this is for APIs exchange
                continue

            if isinstance(prop, DataProperty):
                pytype = prop.datatype.get_python_type()
                if pytype.dep is not None:
                    program.import_(pytype.dep, True)
                cls_ast(stmt.DefClassVarStatement(prop.name, pytype.type))
            elif isinstance(prop, ObjectProperty):
                program.import_(
                    f"{target_pkg.module(prop.target.get_pymodule_name()).path}.{prop.target.name}",
                    is_import_attr=True,
                )
                pytype = prop.target.name
                cls_ast(stmt.DefClassVarStatement(prop.name, pytype))

        target_pkg.module(cls.get_pymodule_name()).write(program)


def make_python_relational_model(
    schema: Schema, target_pkg: Package, target_data_pkg: Package
):
    """Make python classes for relational database using SQLAlchemy.

    The new classes is going be compatible with SQLAlchemy 2.
    """
    app = target_pkg.app

    def make_base(custom_types: Sequence[ObjectProperty]):
        """Make a base class for our database."""
        program = Program()
        program.import_("__future__.annotations", True)
        program.import_("sera.libs.base_orm.BaseORM", True)
        program.import_("sera.libs.base_orm.create_engine", True)
        program.import_("contextlib.contextmanager", True)
        program.import_("sqlalchemy.orm.Session", True)

        # assume configuration for the app at the top level
        program.import_(f"{app.config.path}.DB_CONNECTION", True)
        program.import_(f"{app.config.path}.DB_DEBUG", True)

        program.root.linebreak()

        type_map = []
        for custom_type in custom_types:
            program.import_(
                f"{target_data_pkg.module(custom_type.target.get_pymodule_name()).path}.{custom_type.target.name}",
                is_import_attr=True,
            )

            if custom_type.cardinality.is_star_to_many():
                if custom_type.is_map:
                    program.import_("typing.Mapping", True)
                    program.import_("sera.libs.baseorm.DictDataClassType", True)
                    type = f"Mapping[str, {custom_type.target.name}]"
                    maptype = f"DictDataClassType({custom_type.target.name})"
                else:
                    program.import_("typing.Sequence", True)
                    program.import_("sera.libs.baseorm.ListDataClassType", True)
                    type = f"Sequence[str, {custom_type.target.name}]"
                    maptype = f"ListDataClassType({custom_type.target.name})"
            else:
                program.import_("sera.libs.baseorm.DataClassType", True)
                type = custom_type.target.name
                maptype = f"DataClassType({custom_type.target.name})"

            if custom_type.is_optional:
                program.import_("typing.Optional", True)
                type = f"Optional[{type}]"

            type_map.append((expr.ExprIdent(type), expr.ExprIdent(maptype)))

        cls_ast = program.root.class_("Base", [expr.ExprIdent("BaseORM")])(
            stmt.DefClassVarStatement(
                "type_annotation_map", "dict", PredefinedFn.dict(type_map)
            ),
            return_self=True,
        )

        program.root.linebreak()
        program.root.assign(
            DeferredVar("engine", force_name="engine"),
            expr.ExprFuncCall(
                expr.ExprIdent("create_engine"),
                [
                    expr.ExprIdent("DB_CONNECTION"),
                    PredefinedFn.keyword_assignment(
                        "debug", expr.ExprIdent("DB_DEBUG")
                    ),
                ],
            ),
        )

        program.root.linebreak()
        program.root.func("create_db_and_tables", [])(
            stmt.PythonStatement("Base.metadata.create_all(engine)"),
        )

        program.root.linebreak()
        program.root.python_stmt("@contextmanager")
        program.root.func("get_session", [])(
            lambda ast00: ast00.python_stmt("with Session(engine) as session:")(
                lambda ast01: ast01.python_stmt("yield session")
            )
        )

        target_pkg.module("base").write(program)

    custom_types: list[ObjectProperty] = []

    for cls in schema.topological_sort():
        if cls.db is None:
            # skip classes that are not stored in the database
            continue

        program = Program()
        program.import_("__future__.annotations", True)
        program.import_("sqlalchemy.orm.MappedAsDataclass", True)
        program.import_("sqlalchemy.orm.mapped_column", True)
        program.import_("sqlalchemy.orm.Mapped", True)
        program.import_("typing.ClassVar", True)
        program.import_(f"{target_pkg.path}.base.Base", True)

        cls_ast = program.root.class_(
            cls.name, [expr.ExprIdent("MappedAsDataclass"), expr.ExprIdent("Base")]
        )
        cls_ast(
            stmt.DefClassVarStatement(
                "__tablename__",
                type="ClassVar[str]",
                value=expr.ExprConstant(cls.db.table_name),
            ),
            stmt.LineBreak(),
        )

        for prop in cls.properties.values():
            if prop.db is None:
                # skip properties that are not stored in the database
                continue

            if isinstance(prop, DataProperty):
                pytype = prop.datatype.get_sqlalchemy_type()
                if pytype.dep is not None:
                    program.import_(pytype.dep, True)

                propname = prop.name
                proptype = f"Mapped[{pytype.type}]"

                propvalargs = []
                if prop.db.is_primary_key:
                    propvalargs.append(
                        PredefinedFn.keyword_assignment(
                            "primary_key", expr.ExprConstant(True)
                        )
                    )
                    if prop.db.is_auto_increment:
                        propvalargs.append(
                            PredefinedFn.keyword_assignment(
                                "autoincrement", expr.ExprConstant("auto")
                            )
                        )
                    if prop.db.is_unique:
                        propvalargs.append(
                            PredefinedFn.keyword_assignment(
                                "unique", expr.ExprConstant(True)
                            )
                        )
                propval = expr.ExprFuncCall(
                    expr.ExprIdent("mapped_column"), propvalargs
                )
            else:
                assert isinstance(prop, ObjectProperty)
                if prop.target.db is not None:
                    # if the target class is in the database, we generate a foreign key for it.
                    program.import_("sqlalchemy.ForeignKey", True)

                    # we store this class in the database
                    propname = f"{prop.name}_id"
                    idprop = prop.target.get_id_property()
                    assert idprop is not None
                    idprop_pytype = idprop.datatype.get_sqlalchemy_type()
                    if idprop_pytype.dep is not None:
                        program.import_(idprop_pytype.dep, True)

                    proptype = f"Mapped[{idprop_pytype.type}]"

                    propvalargs: list[expr.Expr] = [
                        expr.ExprConstant(f"{prop.target.db.table_name}.{idprop.name}")
                    ]
                    propvalargs.append(
                        PredefinedFn.keyword_assignment(
                            "ondelete",
                            expr.ExprConstant(prop.db.on_delete.to_sqlalchemy()),
                        )
                    )
                    propvalargs.append(
                        PredefinedFn.keyword_assignment(
                            "onupdate",
                            expr.ExprConstant(prop.db.on_update.to_sqlalchemy()),
                        )
                    )

                    propval = expr.ExprFuncCall(
                        expr.ExprIdent("mapped_column"),
                        [
                            expr.ExprFuncCall(
                                expr.ExprIdent("ForeignKey"),
                                propvalargs,
                            ),
                        ],
                    )
                else:
                    # if the target class is not in the database,
                    program.import_(
                        f"{target_pkg.module(prop.target.get_pymodule_name()).path}.{prop.target.name}",
                        is_import_attr=True,
                    )
                    propname = prop.name
                    proptype = f"Mapped[{prop.target.name}]"

                    # we have two choices, one is to create a composite class, one is to create a custom field
                    if prop.db.is_embedded == "composite":
                        # for a class to be composite, it must have only data properties
                        program.import_("sqlalchemy.orm.composite", True)
                        propvalargs = [expr.ExprIdent(prop.target.name)]
                        for p in prop.target.properties.values():
                            propvalargs.append(
                                expr.ExprFuncCall(
                                    expr.ExprIdent("mapped_column"),
                                    [
                                        expr.ExprIdent(f"{prop.name}_{p.name}"),
                                        expr.ExprIdent(
                                            assert_isinstance(p, DataProperty)
                                            .datatype.get_sqlalchemy_type()
                                            .type
                                        ),
                                        expr.PredefinedFn.keyword_assignment(
                                            "nullable",
                                            expr.ExprConstant(prop.is_optional),
                                        ),
                                    ],
                                )
                            )
                        propval = expr.ExprFuncCall(
                            expr.ExprIdent("composite"),
                            propvalargs,
                        )
                    else:
                        # we create a custom field, the custom field mapping need to be defined in the base
                        propval = expr.ExprFuncCall(expr.ExprIdent("mapped_column"), [])
                        custom_types.append(prop)

            cls_ast(stmt.DefClassVarStatement(propname, proptype, propval))

        target_pkg.module(cls.get_pymodule_name()).write(program)

    # make a base class that implements the mapping for custom types
    custom_types = filter_duplication(
        custom_types, lambda p: (p.target.name, p.cardinality, p.is_optional, p.is_map)
    )
    make_base(custom_types)
