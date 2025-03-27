"""
A simple metamodel for Rel.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from io import StringIO
from typing import IO, Optional, Tuple, Union as PyUnion



@dataclass(frozen=True)
class Node:
    def __str__(self):
        return to_string(self)

    @property
    def kind(self):
        return self.__class__.__name__.lower()

#--------------------------------------------------
# Top level program and declarations
#--------------------------------------------------

@dataclass(frozen=True)
class Program(Node):
    # top-level declarations
    declarations: Tuple[PyUnion[Declare, Def], ...]

@dataclass(frozen=True)
class Declare(Node):
    """ declare $premise [requires $requires] """
    premise: Expr
    requires: Optional[Expr]
    annotations: Tuple[Annotation, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class Def(Node):
    """ def $name($params) { $body } """
    name: str
    params: Tuple[PyUnion[Var, Primitive, MetaValue], ...]
    body: Expr
    annotations: Tuple[Annotation, ...] = field(default_factory=tuple)

#--------------------------------------------------
# Primitives, Annotations
#--------------------------------------------------

Primitive = PyUnion[str, int, float]

@dataclass(frozen=True)
class Annotation(Node):
    """ @$name($args) """
    name: str
    args: Tuple[PyUnion[Primitive, MetaValue], ...]


#--------------------------------------------------
# Expr
#--------------------------------------------------

@dataclass(frozen=True)
class CompositeExpr(Node):
    pass

Expr = PyUnion[Primitive, CompositeExpr]

@dataclass(frozen=True)
class MetaValue(CompositeExpr):
    """ #$value """
    value: Primitive

@dataclass(frozen=True)
class Var(CompositeExpr):
    """ $name[...] [in $type] """
    name: str
    varargs: bool = False
    type: Optional[str] = None

@dataclass(frozen=True)
class Identifier(CompositeExpr):
    """ $name

    Used to declare a relation by name or to refer to a relation (e.g. Int, String)
    """
    name: str

@dataclass(frozen=True)
class Atom(CompositeExpr):
    """ $expr($args)

    Represents atoms like identifier($name)($args) as well as literal relations
    relations like {(:a, Int, 1)}(x...)
    """
    expr: Expr
    args: Tuple[Expr, ...]

def atom(name: str, args: Tuple[Expr, ...]):
    """ Helper to create a Atom where expression is an identifier. """
    return Atom(Identifier(name), args)

@dataclass(frozen=True)
class RelationalAbstraction(CompositeExpr):
    """ ($vars): $body """
    vars: Tuple[Var, ...]
    body: Expr

@dataclass(frozen=True)
class And(CompositeExpr):
    """ $body[0] and $body[1] ... and $body[n] """
    body: Tuple[Expr, ...]

@dataclass(frozen=True)
class Or(CompositeExpr):
    """ $body[0] or $body[1] ... or $body[n] """
    body: Tuple[Expr, ...]

@dataclass(frozen=True)
class Exists(CompositeExpr):
    """ exists(($vars) | $body ) """
    vars: Tuple[Var, ...]
    body: Expr

@dataclass(frozen=True)
class ForAll(CompositeExpr):
    """ forall(($vars) | $body ) """
    vars: Tuple[Var, ...]
    body: Expr

@dataclass(frozen=True)
class Not(CompositeExpr):
    """ not ( $body ) """
    body: Expr

@dataclass(frozen=True)
class BinaryExpr(CompositeExpr):
    """ $lhs $op $rhs """
    lhs: Expr
    op: str
    rhs: Expr

@dataclass(frozen=True)
class Product(CompositeExpr):
    """ ($body[0] , $body[1] ... , $body[n]) """
    body: Tuple[Expr, ...]

@dataclass(frozen=True)
class Union(CompositeExpr):
    """ {$body[0] ; $body[1] ... ; $body[n]} """
    body: Tuple[Expr, ...]



#--------------------------------------------------
# Printer
#--------------------------------------------------

infix = ["+", "-", "*", "/", "%", "=", "!=", "<", "<=", ">", ">="]

def to_string(node) -> str:
    io = StringIO()
    Printer(io).print(node, 0)
    return io.getvalue()

@dataclass(frozen=True)
class Printer():
    io: Optional[IO[str]] = None

    def _join(self, args, sep=', ', indent=0):
        for i, s in enumerate(args):
            if i != 0:
                if indent != 0:
                    self._indent_print(sep.rstrip())
                    self._nl()
                else:
                    self._indent_print(sep)
            self.print(s, indent)

    def _indent_print(self, arg, indent=0):
        print("    " * indent + str(arg), file=self.io, end='')

    def _nl(self):
        self._indent_print("\n")

    def _print_value(self, value):
        if isinstance(value, tuple):
            for i, v in enumerate(value):
                if i != 0:
                    self._indent_print(", ")
                self._print_value(v)
        elif isinstance(value, str):
            self._indent_print(f"\"{value}\"")
        else:
            self._indent_print(value)

    def print(self, node, indent=0) -> None:
        #--------------------------------------------------
        # Top level program and declarations
        #--------------------------------------------------
        if isinstance(node, Program):
            for d in node.declarations:
                self.print(d, indent)
                self._nl()

        elif isinstance(node, Declare):
            for anno in node.annotations:
                self.print(anno, indent)
                self._nl()
            self._indent_print(f"declare {node.premise}", indent)
            if node.requires:
                self._indent_print(" requires ")
                self.print(node.requires, 0)
            self._nl()

        elif isinstance(node, Def):
            for anno in node.annotations:
                self.print(anno, indent)
                self._nl()
            self._indent_print(f"def {node.name}", indent)
            if node.params:
                self._indent_print("(")
                self._join(node.params)
                self._indent_print("):")
                self._nl()
            self.print(node.body, indent+1)
            self._nl()

        #--------------------------------------------------
        # Primitives, Annotations
        #--------------------------------------------------
        elif isinstance(node, (str, int, float, tuple)):
            self._print_value(node)

        elif isinstance(node, Annotation):
            self._indent_print(f"@{node.name}", indent)
            if node.args:
                self._indent_print("(")
                self._join(node.args)
                self._indent_print(")")


        #--------------------------------------------------
        # Expr
        #--------------------------------------------------

        elif isinstance(node, MetaValue):
            self._indent_print("#")
            self._print_value(node.value)

        elif isinstance(node, Var):
            self._indent_print(f"{node.name}", indent)
            if node.varargs:
                self._indent_print("...")
            if node.type:
                self._indent_print(f" in {node.type}")

        elif isinstance(node, Identifier):
            self._indent_print(f"{node.name}", indent)

        elif isinstance(node, Atom):
            if isinstance(node.expr, Identifier) and node.expr.name in infix:
                # deal with the 3 kinds of infix operators
                if len(node.args) == 1:
                    self.print(node.expr, indent)
                    self.print(node.args[0])
                elif len(node.args) == 2:
                    self.print(node.args[0], indent)
                    self._indent_print(" ")
                    self.print(node.expr)
                    self._indent_print(" ")
                    self.print(node.args[1])
                elif len(node.args) == 3:
                    self.print(node.args[2], indent)
                    self._indent_print(" = ")
                    self.print(node.args[0])
                    self._indent_print(" ")
                    self.print(node.expr)
                    self._indent_print(" ")
                    self.print(node.args[1])
                else:
                    raise NotImplementedError(f"emit_action: {node}")
            else:
                if isinstance(node.expr, Identifier):
                    self.print(node.expr, indent)
                else:
                    self._indent_print("{", indent)
                    self.print(node.expr, indent)
                    self._indent_print("}")
                self._indent_print("(")
                self._join(node.args)
                self._indent_print(")")

        elif isinstance(node, RelationalAbstraction):
            if node.vars:
                self._indent_print("{[")
                self._join(node.vars)
                self._indent_print("]: ")
                self.print(node.body)
                self._indent_print("}", indent)
            else:
                self.print(node.body, indent)

        elif isinstance(node, And):
            self._join(node.body, " and ", indent)

        elif isinstance(node, Or):
            self._join(node.body, " or ", indent)

        elif isinstance(node, Exists):
            self._indent_print("exists((", indent)
            self._join(node.vars)
            self._indent_print(") |")
            self._nl()
            self.print(node.body, indent+1)
            self._nl()
            self._indent_print(")", indent)

        elif isinstance(node, ForAll):
            self._indent_print("forall((", indent)
            self._join(node.vars)
            self._indent_print(")| ")
            self.print(node.body)
            self._indent_print(")")

        elif isinstance(node, Not):
            self._indent_print("not (", indent)
            self.print(node.body)
            self._indent_print(")")

        elif isinstance(node, BinaryExpr):
            self.print(node.lhs, indent)
            self._indent_print(f" {node.op} ")
            self.print(node.rhs)

        elif isinstance(node, Product):
            self._indent_print("(", indent)
            self._join(node.body, ", ")
            self._indent_print(")")

        elif isinstance(node, Union):
            self._indent_print("{", indent)
            self._join(node.body, " ; ")
            self._indent_print("}")

        else:
            raise Exception(f"Missing implementation in Rel printer: {type(node)}")
