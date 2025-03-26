from datetime import date
from decimal import Decimal

import streamlit as st
from sqlalchemy import Numeric
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.elements import KeyedColumnElement
from sqlalchemy.types import Enum as SQLEnum
from streamlit_datalist import stDatalist

from streamlit_sql.filters import ExistingData
from streamlit_sql.lib import get_pretty_name


class InputFields:
    def __init__(
        self,
        Model: type[DeclarativeBase],
        key_prefix: str,
        default_values: dict,
        existing_data: ExistingData,
    ) -> None:
        self.Model = Model
        self.key_prefix = key_prefix
        self.default_values = default_values
        self.existing_data = existing_data

    def input_fk(self, col_name: str, value: int | None):
        key = f"{self.key_prefix}_{col_name}"
        opts = self.existing_data.fk[col_name]

        index = next((i for i, opt in enumerate(opts) if opt.idx == value), None)
        input_value = st.selectbox(
            col_name,
            options=opts,
            format_func=lambda opt: opt.name,
            index=index,
            key=key,
        )
        if not input_value:
            return None
        return input_value.idx

    def get_col_str_opts(self, col_name: str, value: str | None):
        opts = list(self.existing_data.text[col_name])
        if value is None:
            return None, opts

        try:
            val_index = opts.index(value)
            return val_index, opts
        except ValueError:
            opts.append(value)
            val_index = len(opts) - 1
            return val_index, opts

    def input_enum(self, col_enum: SQLEnum, col_value=None):
        col_name = col_enum.name
        assert col_name is not None
        opts = col_enum.enums
        if col_value:
            index = opts.index(col_value)
        else:
            index = None
        input_value = st.selectbox(col_name, opts, index=index)
        return input_value

    def input_str(self, col_name: str, value=None):
        key = f"{self.key_prefix}_{col_name}"
        val_index, opts = self.get_col_str_opts(col_name, value)
        input_value = stDatalist(
            col_name,
            list(opts),
            index=val_index,  # pyright: ignore
            key=key,
        )
        result = str(input_value)
        return result

    def input_numeric(self, col_name, scale: int | None, value=None):
        step = None
        if scale:
            step = 10 ** (scale * -1)

        value_float = None
        if value:
            value_float = float(value)

        input_value = st.number_input(col_name, value=value_float, step=step)

        if not input_value:
            return None

        value_dec = Decimal(str(input_value))
        if step:
            value_dec = value_dec.quantize(Decimal(str(step)))

        return value_dec

    def get_input_value(self, col: KeyedColumnElement, col_value):
        col_name = col.description
        assert col_name is not None
        pretty_name = get_pretty_name(col_name)

        if col.primary_key:
            input_value = col_value
        elif len(col.foreign_keys) > 0:
            input_value = self.input_fk(col_name, col_value)
        elif col.type.python_type is str:
            input_value = self.input_str(col_name, col_value)
        elif col.type.python_type is int:
            input_value = st.number_input(pretty_name, value=col_value, step=1)
        elif col.type.python_type is float:
            input_value = st.number_input(pretty_name, value=col_value, step=0.1)
        elif isinstance(col.type, Numeric):
            scale = col.type.scale
            input_value = self.input_numeric(pretty_name, scale, col_value)
        elif col.type.python_type is date:
            input_value = st.date_input(pretty_name, value=col_value)
        elif col.type.python_type is bool:
            input_value = st.checkbox(pretty_name, value=col_value)
        elif isinstance(col.type, SQLEnum):
            input_value = self.input_enum(col.type, col_value)
        else:
            input_value = None

        return input_value
