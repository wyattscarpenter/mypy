"""Classification of possible errors mypy can detect.

These can be used for filtering specific errors.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Final

from mypy_extensions import mypyc_attr

error_codes: dict[str, ErrorCode] = {}
sub_code_map: dict[str, set[str]] = defaultdict(set)


@mypyc_attr(allow_interpreted_subclasses=True)
class ErrorCode:
    def __init__(
        self,
        code: str,
        description: str,
        default_enabled: bool = True,
        sub_code_of: ErrorCode | None = None,
    ) -> None:
        self.code = code
        self.description = description
        self.default_enabled = default_enabled
        self.sub_code_of = sub_code_of
        if sub_code_of is not None:
            assert sub_code_of.sub_code_of is None, "Nested subcategories are not supported"
            sub_code_map[sub_code_of.code].add(code)
        error_codes[code] = self

    def __str__(self) -> str:
        return f"<ErrorCode {self.code}>"

    def __repr__(self) -> str:
        """This doesn't fulfill the goals of repr but it's better than the default view."""
        return f"<ErrorCode {self.code}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ErrorCode):
            return False
        return self.code == other.code

    def __hash__(self) -> int:
        return hash((self.code,))


ATTR_DEFINED: Final = ErrorCode("attr-defined", "Check that attribute exists")
NAME_DEFINED: Final = ErrorCode("name-defined", "Check that name is defined")
CALL_ARG: Final = ErrorCode(
    "call-arg", "Check number, names and kinds of arguments in calls"
)
ARG_TYPE: Final = ErrorCode("arg-type", "Check argument types in calls")
CALL_OVERLOAD: Final = ErrorCode(
    "call-overload", "Check that an overload variant matches arguments"
)
VALID_TYPE: Final = ErrorCode("valid-type", "Check that type (annotation) is valid")
VAR_ANNOTATED: Final = ErrorCode(
    "var-annotated", "Require variable annotation if type can't be inferred"
)
OVERRIDE: Final = ErrorCode(
    "override", "Check that method override is compatible with base class"
)
RETURN: Final = ErrorCode("return", "Check that function always returns a value")
RETURN_VALUE: Final = ErrorCode(
    "return-value", "Check that return value is compatible with signature"
)
ASSIGNMENT: Final = ErrorCode(
    "assignment", "Check that assigned value is compatible with target"
)
METHOD_ASSIGN: Final = ErrorCode(
    "method-assign",
    "Check that assignment target is not a method",
    sub_code_of=ASSIGNMENT,
)
TYPE_ARG: Final = ErrorCode("type-arg", "Check that generic type arguments are present")
TYPE_VAR: Final = ErrorCode("type-var", "Check that type variable values are valid")
UNION_ATTR: Final = ErrorCode(
    "union-attr", "Check that attribute exists in each item of a union"
)
INDEX: Final = ErrorCode("index", "Check indexing operations")
OPERATOR: Final = ErrorCode("operator", "Check that operator is valid for operands")
LIST_ITEM: Final = ErrorCode(
    "list-item", "Check list items in a list expression [item, ...]"
)
DICT_ITEM: Final = ErrorCode(
    "dict-item", "Check dict items in a dict expression {key: value, ...}"
)
TYPEDDICT_ITEM: Final = ErrorCode(
    "typeddict-item", "Check items when constructing TypedDict"
)
TYPEDDICT_UNKNOWN_KEY: Final = ErrorCode(
    "typeddict-unknown-key",
    "Check unknown keys when constructing TypedDict",
    sub_code_of=TYPEDDICT_ITEM,
)
HAS_TYPE: Final = ErrorCode(
    "has-type", "Check that type of reference can be determined"
)
IMPORT: Final = ErrorCode(
    "import", "Require that imported module can be found or has stubs"
)
IMPORT_NOT_FOUND: Final = ErrorCode(
    "import-not-found", "Require that imported module can be found", sub_code_of=IMPORT
)
IMPORT_UNTYPED: Final = ErrorCode(
    "import-untyped", "Require that imported module has stubs", sub_code_of=IMPORT
)
NO_REDEF: Final = ErrorCode("no-redef", "Check that each name is defined once")
FUNC_RETURNS_VALUE: Final = ErrorCode(
    "func-returns-value", "Check that called function returns a value in value context"
)
ABSTRACT: Final = ErrorCode(
    "abstract", "Prevent instantiation of classes with abstract attributes"
)
TYPE_ABSTRACT: Final = ErrorCode(
    "type-abstract", "Require only concrete classes where Type[...] is expected"
)
VALID_NEWTYPE: Final = ErrorCode(
    "valid-newtype", "Check that argument 2 to NewType is valid"
)
STRING_FORMATTING: Final = ErrorCode(
    "str-format", "Check that string formatting/interpolation is type-safe"
)
STR_BYTES_PY3: Final = ErrorCode(
    "str-bytes-safe", "Warn about implicit coercions related to bytes and string types"
)
EXIT_RETURN: Final = ErrorCode(
    "exit-return", "Warn about too general return type for '__exit__'"
)
LITERAL_REQ: Final = ErrorCode("literal-required", "Check that value is a literal")
UNUSED_COROUTINE: Final = ErrorCode(
    "unused-coroutine", "Ensure that all coroutines are used"
)
EMPTY_BODY: Final = ErrorCode(
    "empty-body",
    "A dedicated error code to opt out return errors for empty/trivial bodies",
)
SAFE_SUPER: Final = ErrorCode(
    "safe-super", "Warn about calls to abstract methods with empty/trivial bodies"
)
TOP_LEVEL_AWAIT: Final = ErrorCode(
    "top-level-await", "Warn about top level await expressions"
)
AWAIT_NOT_ASYNC: Final = ErrorCode(
    "await-not-async", 'Warn about "await" outside coroutine ("async def")'
)
# These error codes aren't enabled by default.
NO_UNTYPED_DEF: Final = ErrorCode(
    "no-untyped-def", "Check that every function has an annotation"
)
NO_UNTYPED_CALL: Final = ErrorCode(
    "no-untyped-call",
    "Disallow calling functions without type annotations from annotated functions",
)
REDUNDANT_CAST: Final = ErrorCode(
    "redundant-cast", "Check that cast changes type of expression"
)
ASSERT_TYPE: Final = ErrorCode("assert-type", "Check that assert_type() call succeeds")
COMPARISON_OVERLAP: Final = ErrorCode(
    "comparison-overlap", "Check that types in comparisons and 'in' expressions overlap"
)
NO_ANY_UNIMPORTED: Final = ErrorCode(
    "no-any-unimported", 'Reject "Any" types from unfollowed imports'
)
NO_ANY_RETURN: Final = ErrorCode(
    "no-any-return",
    'Reject returning value with "Any" type if return type is not "Any"',
)
UNREACHABLE: Final = ErrorCode(
    "unreachable", "Warn about unreachable statements or expressions"
)
ANNOTATION_UNCHECKED: Final = ErrorCode(
    "annotation-unchecked", "Notify about type annotations in unchecked functions"
)
TYPEDDICT_READONLY_MUTATED: Final = ErrorCode(
    "typeddict-readonly-mutated", "TypedDict's ReadOnly key is mutated"
)
POSSIBLY_UNDEFINED: Final = ErrorCode(
    "possibly-undefined",
    "Warn about variables that are defined only in some execution paths",
    default_enabled=False,
)
REDUNDANT_EXPR: Final = ErrorCode(
    "redundant-expr", "Warn about redundant expressions", default_enabled=False
)
TRUTHY_BOOL: Final = ErrorCode(
    "truthy-bool",
    "Warn about expressions that could always evaluate to true in boolean contexts",
    default_enabled=False,
)
TRUTHY_FUNCTION: Final = ErrorCode(
    "truthy-function",
    "Warn about function that always evaluate to true in boolean contexts",
)
TRUTHY_ITERABLE: Final = ErrorCode(
    "truthy-iterable",
    "Warn about Iterable expressions that could always evaluate to true in boolean contexts",
    default_enabled=False,
)
NAME_MATCH: Final = ErrorCode(
    "name-match", "Check that type definition has consistent naming"
)
NO_OVERLOAD_IMPL: Final = ErrorCode(
    "no-overload-impl",
    "Check that overloaded functions outside stub files have an implementation",
)
IGNORE_WITHOUT_CODE: Final = ErrorCode(
    "ignore-without-code",
    "Warn about '# type: ignore' comments which do not have error codes",
    default_enabled=False,
)
UNUSED_AWAITABLE: Final = ErrorCode(
    "unused-awaitable",
    "Ensure that all awaitable values are used",
    default_enabled=False,
)
REDUNDANT_SELF_TYPE: Final = ErrorCode(
    "redundant-self",
    "Warn about redundant Self type annotations on method first argument",
    default_enabled=False,
)
USED_BEFORE_DEF: Final = ErrorCode(
    "used-before-def", "Warn about variables that are used before they are defined"
)
UNUSED_IGNORE: Final = ErrorCode(
    "unused-ignore", "Ensure that all type ignores are used", default_enabled=False
)
EXPLICIT_OVERRIDE_REQUIRED: Final = ErrorCode(
    "explicit-override",
    "Require @override decorator if method is overriding a base class method",
    default_enabled=False,
)
UNIMPORTED_REVEAL: Final = ErrorCode(
    "unimported-reveal",
    "Require explicit import from typing or typing_extensions for reveal_type",
    default_enabled=False,
)
MUTABLE_OVERRIDE: Final = ErrorCode(
    "mutable-override",
    "Reject covariant overrides for mutable attributes",
    default_enabled=False,
)
EXHAUSTIVE_MATCH: Final = ErrorCode(
    "exhaustive-match",
    "Reject match statements that are not exhaustive",
    default_enabled=False,
)
METACLASS: Final = ErrorCode("metaclass", "Ensure that metaclass is valid")

# Syntax errors are often blocking.
SYNTAX: Final = ErrorCode("syntax", "Report syntax errors")

# This is an internal marker code for a whole-file ignore. It is not intended to
# be user-visible.
FILE: Final = ErrorCode("file", "Internal marker for a whole file being ignored")
del error_codes[FILE.code]

# This is a catch-all for remaining uncategorized errors.
MISC: Final = ErrorCode("misc", "Miscellaneous other checks")

OVERLOAD_CANNOT_MATCH: Final = ErrorCode(
    "overload-cannot-match",
    "Warn if an @overload signature can never be matched",
    sub_code_of=MISC,
)

OVERLOAD_OVERLAP: Final = ErrorCode(
    "overload-overlap",
    "Warn if multiple @overload variants overlap in unsafe ways",
    sub_code_of=MISC,
)

PROPERTY_DECORATOR: Final = ErrorCode(
    "prop-decorator",
    "Decorators on top of @property are not supported",
    sub_code_of=MISC,
)

NARROWED_TYPE_NOT_SUBTYPE: Final = ErrorCode(
    "narrowed-type-not-subtype",
    "Warn if a TypeIs function's narrowed type is not a subtype of the original type",
)

EXPLICIT_ANY: Final = ErrorCode(
    "explicit-any", "Warn about explicit Any type annotations"
)

DEPRECATED: Final = ErrorCode(
    "deprecated",
    "Warn when importing or using deprecated (overloaded) functions, methods or classes",
    default_enabled=False,
)

# This copy will not include any error codes defined later in the plugins.
mypy_error_codes = error_codes.copy()
