from .span import Span as span
from .label import Label as label
from .paragraph import Paragraph as paragraph
from .input import Input as input
from .number import Number as number
from .button import Button as button
from .checkbox import Checkbox as checkbox
from .form import Form as form
from .select import Select as select
from .ul import Ul as ul
from .li import Li as li
from .div import Div as div
from .range import Range as range
from .date import Date as date
from .link import Link as link

option = select.Option

__all__ = [
    "span",
    "label",
    "paragraph",
    "input",
    "number",
    "button",
    "checkbox",
    "form",
    "select",
    "option",
    "ul",
    "li",
    "div",
    "range",
    "date",
    "link",
]
