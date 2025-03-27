"""
    Intermediate Representation of RelationalAI programs.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from io import StringIO
from itertools import count
from typing import Any, IO, Optional, Tuple, TypeVar, Union as PyUnion

from .util import FrozenOrderedSet

import json

#--------------------------------------------------
# IR Nodes
#--------------------------------------------------

_global_id = count(0)
def next_id():
    return next(_global_id)

@dataclass(frozen=True)
class Node:
    # A generated id that is not used on comparisons and hashes
    id: int = field(default_factory=next_id, init=False, compare=False, hash=False)

    @property
    def kind(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        return node_to_string(self)

#-------------------------------------------------
# Public Types - Model
#-------------------------------------------------

@dataclass(frozen=True)
class Model(Node):
    """Represents the whole universe of elements that make up a program."""
    engines: FrozenOrderedSet["Engine"]
    relations: FrozenOrderedSet["Relation"]
    types: FrozenOrderedSet["Type"]
    root: Task


#-------------------------------------------------
# Public Types - Engine
#-------------------------------------------------

@dataclass(frozen=True)
class Capability(Node):
    """Engine capabilities, such as 'graph algorithms', 'solver', 'constant time count', etc"""
    name: str

@dataclass(frozen=True)
class Engine(Node):
    """The entity that owns a Task and provides access to certain relations."""
    name: str
    platform: str # SQL, Rel, JS, OpenAI, etc
    info: Any
    capabilities: FrozenOrderedSet[Capability]
    relations: FrozenOrderedSet["Relation"]


#-------------------------------------------------
# Public Types - Data Model
#-------------------------------------------------

@dataclass(frozen=True)
class ScalarType(Node):
    """The named type."""
    name: str

@dataclass(frozen=True)
class ListType(Node):
    """A type that represents a list of elements of some other type."""
    element_type: Type

@dataclass(frozen=True)
class SetType(Node):
    """A type that represents a set of elements of some other type."""
    element_type: Type

@dataclass(frozen=True)
class UnionType(Node):
    """A type that represents either one of a set of types."""
    types: FrozenOrderedSet[Type]

# The type of a field in a relation
Type = PyUnion[ScalarType, ListType, SetType, UnionType]

@dataclass(frozen=True)
class Field(Node):
    """A named field in a relation."""
    name: str
    type: Type
    input: bool # must be grounded as the relation cannot compute it


@dataclass(frozen=True)
class Relation(Node):
    """A relation represents the schema of a set of tuples."""
    name: str
    fields: Tuple[Field, ...]
    requires: FrozenOrderedSet[Capability]


#-------------------------------------------------
# Public Types - Tasks
#-------------------------------------------------

@dataclass(frozen=True)
class Task(Node):
    engine: Optional[Engine]

#
# Task composition
#

@dataclass(frozen=True)
class Logical(Task):
    """Execute sub-tasks up to fix-point."""
    # Executes tasks concurrently. Succeeds if every task succeeds.
    hoisted: Tuple[VarOrElse, ...]
    body: Tuple[Task, ...]

@dataclass(frozen=True)
class Union(Task):
    """Execute sub-tasks in any order."""
    # Executes tasks concurrently. Succeeds if at least one task succeeds.
    hoisted: Tuple[VarOrElse, ...]
    tasks: Tuple[Task, ...]

@dataclass(frozen=True)
class Sequence(Task):
    """Execute sub-tasks one at a time, in this order."""
    # Executes tasks in order. Stops when a task fails. Succeeds if all tasks succeed.
    hoisted: Tuple[VarOrElse, ...]
    tasks: Tuple[Task, ...]

@dataclass(frozen=True)
class Match(Task):
    """Execute sub-tasks in order until the first succeeds."""
    # Executes tasks in order. Stops when a task succeeds. Succeeds if some task succeeds.
    hoisted: Tuple[VarOrElse, ...]
    tasks: Tuple[Task, ...]

@dataclass(frozen=True)
class Until(Task):
    """Execute both `check` and `body` concurrently, until check succeeds."""
    hoisted: Tuple[VarOrElse, ...]
    check: Task
    body: Task

@dataclass(frozen=True)
class Wait(Task):
    hoisted: Tuple[VarOrElse, ...]
    check: Task

# TODO: DynamicLookup


#
# Logical Quantifiers
#

@dataclass(frozen=True)
class Not(Task):
    """Logical negation of the sub-task."""
    task: Task

@dataclass(frozen=True)
class Exists(Task):
    """Existential quantification over the sub-task."""
    vars: Tuple[Var, ...]
    task: Task

@dataclass(frozen=True)
class ForAll(Task):
    """Universal quantification over the sub-task."""
    vars: Tuple[Var, ...]
    task: Task


#
# Iteration (Loops)
#

# loops body until a break condition is met
@dataclass(frozen=True)
class Loop(Task):
    """Execute the body in a loop, incrementing the iter variable, until a break sub-task in
    the body succeeds."""
    hoisted: Tuple[VarOrElse, ...]
    iter: Var
    body: Task

@dataclass(frozen=True)
class Break(Task):
    """Break a surrounding Loop if the `check` succeeds."""
    check: Task


#
# Relational Operations
#

@dataclass(frozen=True)
class Var(Node):
    """A named variable that can point to objects of this type."""
    type: Type
    name: str

@dataclass(frozen=True)
class Else(Node):
    """A variable with a default value. This can be used in 'hoisted' attributes to
    represent the value to assign a variable if the underlying task fails."""
    var: Var
    value: Value

VarOrElse = PyUnion[Var, Else]

@dataclass(frozen=True)
class Literal(Node):
    """A literal value with a specific type."""
    type: Type
    value: Any

Value = PyUnion[str, int, float, bool, None, Var, Else, Literal, Type, Relation, Tuple["Value", ...], FrozenOrderedSet["Value"]]

@dataclass(frozen=True)
class Annotation(Node):
    """Meta information that can be attached to Updates."""
    relation: Relation
    args: Tuple[Value, ...]

class Effect(Enum):
    """Possible effects of an Update."""
    derive = "derive"
    insert = "insert"
    delete = "delete"

@dataclass(frozen=True)
class Update(Task):
    """Updates the relation with these arguments. The update can derive new tuples
    temporarily, can insert new tuples persistently, or delete previously persisted tuples."""
    relation: Relation
    args: Tuple[Value, ...]
    effect: Effect
    annotations: FrozenOrderedSet[Annotation]

@dataclass(frozen=True)
class Lookup(Task):
    """Lookup tuples from this relation, filtering with these arguments."""
    relation: Relation
    args: Tuple[Value, ...]

@dataclass(frozen=True)
class Output(Task):
    """Output the value of these vars, giving them these column names."""
    aliases: FrozenOrderedSet[Tuple[str, Var]]

@dataclass(frozen=True)
class Construct(Task):
    """Construct an id from these values, and bind the id to this var."""
    values: Tuple[Value, ...]
    id_var: Var

@dataclass(frozen=True)
class Aggregate(Task):
    """Perform an aggregation with these arguments."""
    aggregation: Relation
    projection: Tuple[Var, ...]
    group: Tuple[Var, ...]
    args: Tuple[Value, ...]


#--------------------------------------------------
# Printer
#--------------------------------------------------

infix = ["+", "-", "*", "/", "%", "=", "!=", "<", "<=", ">", ">="]

T = TypeVar('T', bound=Node)
def node_to_string(node:Node|Tuple[T, ...]|FrozenOrderedSet[T]) -> str:
    io = StringIO()
    printer = Printer(io)
    printer.pprint(node)
    return io.getvalue()

def value_to_string(value:PyUnion[Value, Tuple[Value, ...]]) -> str:
    return Printer().value_to_string(value)

@dataclass(frozen=True)
class Printer():
    io: Optional[IO[str]] = None

    # count of vars with this name, to generate names with ids when there's collision
    var_count: dict[str, int] = field(default_factory=dict)
    # cache of precomputed names for the var with this id
    var_name_cache: dict[int, str] =  field(default_factory=dict)

    def indent_print(self, depth, *args) -> None:
        """ Helper to print the arguments into the io with indented based on depth. """
        if self.io is None:
            print("    " * depth + " ".join(map(str, args)))
        else:
            self.io.write("    " * depth + " ".join(map(str, args)) + "\n")

    def print_hoisted(self, depth, name, hoisted: Tuple[VarOrElse, ...]):
        if hoisted:
            self.indent_print(depth, f"{name} ⇑[{', '.join([self.value_to_string(h) for h in hoisted])}]")
        else:
            self.indent_print(depth, name)

    def var_to_string(self, var: Var) -> str:
        if var.id in self.var_name_cache:
            return self.var_name_cache[var.id]

        if var.name in self.var_count:
            c = self.var_count[var.name]
            self.var_count[var.name] = c + 1
            name = f"{var.name}_{c}"
        else:
            self.var_count[var.name] = 2
            name = f"{var.name}"

        self.var_name_cache[var.id] = name
        return name

    def value_to_string(self, value:PyUnion[Value, Tuple[Value, ...]]) -> str:
        """ Return a string representation of the value. """
        if isinstance(value, (int, str, float, bool)):
            return json.dumps(value)
        elif value is None:
            return "None"
        elif isinstance(value, Var):
            return self.var_to_string(value)
        elif isinstance(value, Else):
            return f"{self.var_to_string(value.var)}={value.value}"
        elif isinstance(value, Literal):
            return f"{json.dumps(value.value)}"
        elif isinstance(value, ListType):
            return f"[{self.value_to_string(value.element_type)}]"
        elif isinstance(value, SetType):
            return f"{{{self.value_to_string(value.element_type)}}}"
        elif isinstance(value, UnionType):
            return f"{{{'; '.join(map(self.value_to_string, value.types))}}}"
        elif isinstance(value, ScalarType):
            return f"{value.name}"
        elif isinstance(value, Relation):
            return value.name
        elif isinstance(value, Tuple):
            return f"({', '.join(map(self.value_to_string, value))})"
        elif isinstance(value, FrozenOrderedSet):
            return f"{{{', '.join(map(self.value_to_string, value))}}}"
        else:
            raise NotImplementedError(f"value_to_string not implemented for {type(value)}")

    T = TypeVar('T', bound=Node)
    def pprint(self, node:Node|Tuple[T, ...]|FrozenOrderedSet[T], depth=0) -> None:
        """ Pretty print the node into the io, starting with indentation based on depth. If io is None,
        print into the standard output. """

        if isinstance(node, Tuple) or isinstance(node, FrozenOrderedSet):
            for n in node:
                self.pprint(n, depth)
        # model
        elif isinstance(node, Model):
            self.indent_print(depth, "Model")
            if len(node.engines) > 0:
                self.indent_print(depth + 1, "engines:")
            self.pprint(node.engines, depth + 2)
            if len(node.relations) > 0:
                self.indent_print(depth + 1, "relations:")
            self.pprint(node.relations, depth + 2)
            if len(node.types) > 0:
                self.indent_print(depth + 1, "types:")
            self.pprint(node.types, depth + 2)
            self.indent_print(depth + 1, "root:")
            self.pprint(node.root, depth + 2)

        # engine
        elif isinstance(node, Capability):
            self.indent_print(depth, node.name)
        elif isinstance(node, Engine):
            self.indent_print(depth, f"Engine ({node.name}, {node.platform})")
            self.indent_print(depth + 1, node.info)
            self.indent_print(depth + 1, ', '.join([c.name for c in node.capabilities]))
            self.pprint(node.relations, depth + 1)

        # data model
        elif isinstance(node, (ScalarType, ListType, SetType, UnionType)):
            self.indent_print(depth, self.value_to_string(node))
        elif isinstance(node, Field):
            s = f"{node.name}: {self.value_to_string(node.type)} {'(input)' if node.input else ''}"
            self.indent_print(depth, s)
        elif isinstance(node, Relation):
            self.indent_print(depth, node.name)
            self.pprint(node.fields, depth + 1)
            if len(node.requires) > 0:
                self.indent_print(depth + 1, "requires:")
                self.pprint(node.requires, depth + 2)

        # tasks

        # Task composition
        elif isinstance(node, Logical):
            self.print_hoisted(depth, "Logical", node.hoisted)
            self.pprint(node.body, depth + 1)
        elif isinstance(node, Sequence):
            self.print_hoisted(depth, "Sequence", node.hoisted)
            self.pprint(node.tasks, depth + 1)
        elif isinstance(node, Union):
            self.print_hoisted(depth, "Union", node.hoisted)
            self.pprint(node.tasks, depth + 1)
        elif isinstance(node, Match):
            self.print_hoisted(depth, "Match", node.hoisted)
            self.pprint(node.tasks, depth + 1)
        elif isinstance(node, Until):
            self.print_hoisted(depth, "Until", node.hoisted)
            self.pprint(node.check, depth + 1)
            self.pprint(node.body, depth + 1)
        elif isinstance(node, Wait):
            self.print_hoisted(depth, "Match", node.hoisted)
            self.pprint(node.check, depth + 1)

        # Relational Operations
        elif isinstance(node, Var):
            self.indent_print(0, self.value_to_string(node))
        elif isinstance(node, Literal):
            self.indent_print(0, self.value_to_string(node))
        elif isinstance(node, Annotation):
            if node.args:
                self.indent_print(depth, f"@{node.relation.name}{self.value_to_string(node.args)}")
            else:
                self.indent_print(depth, f"@{node.relation.name}")
        elif isinstance(node, Update):
            rel_name = node.relation.name
            annos = "" if not node.annotations else f" {' '.join(str(a) for a in node.annotations)}"
            self.indent_print(depth, f"→ {node.effect.value} {rel_name}{self.value_to_string(node.args)}{annos}")
        elif isinstance(node, Lookup):
            rel_name = node.relation.name
            if rel_name in infix:
                args = [self.value_to_string(arg) for arg in node.args]
                if len(node.args) == 2:
                    self.indent_print(depth, f"{args[0]} {rel_name} {args[1]}")
                elif len(node.args) == 1:
                    self.indent_print(depth, f"{rel_name}{args[0]}")
                elif len(node.args) == 3:
                    self.indent_print(depth, f"{args[2]} = {args[0]} {rel_name} {args[1]}")
            else:
                self.indent_print(depth, f"{rel_name}{self.value_to_string(node.args)}")
        elif isinstance(node, Output):
            args = []
            for k, v in node.aliases:
                ppv = self.value_to_string(v)
                if k != ppv:
                    args.append(f"{ppv} as '{k}'")
                else:
                    args.append(ppv)
            self.indent_print(depth, f"→ output({', '.join(args)})")
        elif isinstance(node, Construct):
            values = [self.value_to_string(v) for v in node.values]
            self.indent_print(depth, f"construct({', '.join(values)}, {self.value_to_string(node.id_var)})")
        elif isinstance(node, Aggregate):
            self.indent_print(depth, f"{node.aggregation.name}([{self.value_to_string(node.projection)}], [{self.value_to_string(node.group)}], [{self.value_to_string(node.args)}])")

        # Logical Quantifiers
        elif isinstance(node, Not):
            self.indent_print(depth, "Not")
            self.pprint(node.task, depth + 1)
        elif isinstance(node, Exists):
            self.indent_print(depth, f"Exists({', '.join([self.value_to_string(v) for v in node.vars])})")
            self.pprint(node.task, depth + 1)
        elif isinstance(node, ForAll):
            self.indent_print(depth, f"ForAll({', '.join([self.value_to_string(v) for v in node.vars])})")
            self.pprint(node.task, depth + 1)

        # Iteration (Loops)
        elif isinstance(node, Loop):
            self.print_hoisted(depth, f"Loop ⇓[{self.value_to_string(node.iter)}]", node.hoisted)
            self.pprint(node.body, depth + 1)

        elif isinstance(node, Break):
            self.indent_print(depth, "Break")
            self.pprint(node.check, depth + 1)

        elif isinstance(node, Task):
            # empty task represents success
            self.indent_print(depth, "Success")

        else:
            # return
            raise NotImplementedError(f"pprint not implemented for {type(node)}")
