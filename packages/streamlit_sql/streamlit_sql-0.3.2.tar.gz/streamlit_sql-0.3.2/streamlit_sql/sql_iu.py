from collections.abc import Callable

import pandas as pd
import streamlit as st
from sqlalchemy import CTE, Select, select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import Enum as SQLEnum
from streamlit import session_state as ss
from streamlit.connections import SQLConnection
from streamlit.elements.arrow import DataframeState

from streamlit_sql import create_delete_model, lib, read_cte, update_model

OPTS_ITEMS_PAGE = (50, 100, 200, 500, 1000)


class SqlUi:
    """Show A CRUD interface in a Streamlit Page

    See in __init__ method detailed descriptions of arguments and properties

    It also offers the following properties:


    """

    def __init__(
        self,
        conn: SQLConnection,
        read_instance,
        edit_create_model: type[DeclarativeBase],
        available_filter: list[str] | None = None,
        edit_create_default_values: dict | None = None,
        rolling_total_column: str | None = None,
        rolling_orderby_colsname: list[str] | None = None,
        df_style_formatter: dict[str, str] | None = None,
        read_use_container_width: bool = False,
        hide_id: bool = True,
        base_key: str = "",
        style_fn: Callable[[pd.Series], list[str]] | None = None,
        update_show_many: bool = False,
        disable_log: bool = False,
    ):
        """The CRUD interface will be displayes just by initializing the class

        Arguments:
            conn (SQLConnection): A sqlalchemy connection created with st.connection(\"sql\", url=\"<sqlalchemy url>\")
            read_instance (Select | CTE | Model): The sqlalchemy select statement to display or a CTE. Choose columns to display , join, query or order.If selecting columns, you need to add the id column. If a Model, it will select all columns.
            edit_create_default_values (dict, optional): A dict with column name as keys and values to be default. When the user clicks to create a row, those columns will not show on the form and its value will be added to the Model object
            available_filter (list[str], optional): Define wich columns the user will be able to filter in the top expander. Defaults to all
            rolling_total_column (str, optional): A numeric column name of the read_instance. A new column will be displayed with the rolling sum of these column
            rolling_orderby_colsname (list[str], optional): A list of columns name of the read_instance. It should contain a group of columns that ensures uniqueness of the rows and the order to calculate rolling sum. Usually, it should a date and id column. If not informed, rows will be sorted by id only. Defaults to None
            df_style_formatter (dict[str,str]): a dictionary where each key is a column name and the associated value is the formatter arg of df.style.format method. See pandas docs for details.
            read_use_container_width (bool, optional): add use_container_width to st.dataframe args. Default to False
            hide_id (bool, optional): The id column will not be displayed if set to True. Defaults to True
            base_key (str, optional): A prefix to add to widget's key argument. This is needed when creating more than one instance of this class in the same page. Defaults to empty str
            style_fn (Callable[[pd.Series], list[str]], optional): A function that goes into the *func* argument of *df.style.apply*. The apply method also receives *axis=1*, so it works on rows. It can be used to apply conditional css formatting on each column of the row. See Styler.apply info on pandas docs. Defaults to None
            update_show_many (bool, optional): Show a st.expander of one-to-many relations in edit or create dialog
            disable_log (bool): Every change in the database (READ, UPDATE, DELETE) is logged to stderr by default. If this is *true*, nothing is logged. To customize the logging format and where it logs to, use loguru as add a new sink to logger. See loguru docs for more information. Dafaults to False

        Attributes:
            df (pd.Dataframe): The Dataframe displayed in the screen
            selected_rows (list[int]): The position of selected rows. This is not the row id.
            qtty_rows (int): The quantity of all rows after filtering


        Examples:
            ```python
            def style_fn(row):
                if row.amount > 0:
                    bg = "background-color: rgba(0, 255, 0, 0.1)"
                else:
                    bg = "background-color: rgba(255, 0, 0, 0.2)"

                result = [bg] * len(row)
                return result


            db_url = "sqlite:///data.db"
            conn = st.connection("sql", db_url)

            stmt = (
                select(
                    db.Invoice.id,
                    db.Invoice.date,
                    db.Invoice.amount,
                    db.Client.name,
                )
                .join(db.Client)
                .where(db.Invoice.amount > 1000)
                .order_by(db.Invoice.date)
            )

            sql_ui = SqlUi(
                conn=conn,
                read_instance=stmt,
                edit_create_model=db.Invoice,
                available_filter=["name"],
                rolling_total_column="amount",
                rolling_orderby_colsname=["date", "id"],
                df_style_formatter={"amount": "{:,.2f}"},
                read_use_container_width=True,
                hide_id=True,
                base_key="my_base_sql_ui",
                style_fn=style_fn,
                update_show_many=True,
                disable_log=False,
            )

            ```

        """
        self.conn = conn
        self.read_instance = read_instance
        self.edit_create_model = edit_create_model
        self.available_filter = available_filter or []
        self.edit_create_default_values = edit_create_default_values or {}
        self.rolling_total_column = rolling_total_column
        self.rolling_orderby_colsname = rolling_orderby_colsname or ["id"]
        self.df_style_formatter = df_style_formatter or {}
        self.read_use_container_width = read_use_container_width
        self.hide_id = hide_id
        self.base_key = base_key
        self.style_fn = style_fn
        self.update_show_many = update_show_many
        self.disable_log = disable_log

        self.cte = self.get_cte()
        self.rolling_pretty_name = lib.get_pretty_name(self.rolling_total_column or "")

        # Bootstrap
        self.set_initial_state()
        self.set_structure()
        self.notification()
        lib.set_logging(self.disable_log)

        # Create UI
        col_filter = self.filter()
        stmt_no_pag = read_cte.get_stmt_no_pag(self.cte, col_filter)
        qtty_rows = read_cte.get_qtty_rows(self.conn, stmt_no_pag)
        items_per_page, page = self.pagination(qtty_rows, col_filter)
        stmt_pag = read_cte.get_stmt_pag(stmt_no_pag, items_per_page, page)
        initial_balance = self.get_initial_balance(
            self.cte,
            stmt_pag,
            col_filter.no_dt_filters,
            rolling_total_column,
            self.rolling_orderby_colsname,
        )
        df = self.get_df(stmt_pag, initial_balance)
        selection_state = self.show_df(df)
        rows_selected = self.get_rows_selected(selection_state)

        # CRUD
        self.crud(df, rows_selected)
        ss.stsql_opened = False

        # Returns
        self.df = df
        self.rows_selected = rows_selected
        self.qtty_rows = qtty_rows

    def set_initial_state(self):
        lib.set_state("stsql_updated", 1)
        lib.set_state("stsql_update_ok", None)
        lib.set_state("stsql_update_message", None)
        lib.set_state("stsql_opened", False)
        lib.set_state("stsql_filters", {})

    def set_structure(self):
        self.header_container = st.container()
        self.data_container = st.container()
        self.pag_container = st.container()

        table_name = lib.get_pretty_name(self.edit_create_model.__tablename__)
        self.header_container.header(table_name, divider="orange")

        self.expander_container = self.header_container.expander(
            "Filter",
            icon=":material/search:",
        )

        self.filter_container = self.header_container.container()

        if self.rolling_total_column:
            self.saldo_toggle_col, self.saldo_value_col = self.header_container.columns(
                2
            )

        self.btns_container = self.header_container.container()

    def notification(self):
        if ss.stsql_update_ok is True:
            self.header_container.success(
                ss.stsql_update_message, icon=":material/thumb_up:"
            )
        if ss.stsql_update_ok is False:
            self.header_container.error(
                ss.stsql_update_message, icon=":material/thumb_down:"
            )

    def get_cte(self):
        if isinstance(self.read_instance, Select):
            cte = self.read_instance.cte()
        elif isinstance(self.read_instance, CTE):
            cte = self.read_instance
        else:
            cte = select(self.read_instance).cte()

        if self.rolling_total_column:
            orderby_cols = [
                cte.columns.get(colname) for colname in self.rolling_orderby_colsname
            ]
            orderby_cols = [col for col in orderby_cols if col is not None]
            cte = select(cte).order_by(*orderby_cols).cte()

        return cte

    def filter(self):
        filter_colsname = self.available_filter
        if len(filter_colsname) == 0:
            filter_colsname = [
                col.description for col in self.cte.columns if col.description
            ]

        with self.conn.session as s:
            existing = read_cte.get_existing_values(
                _session=s,
                cte=self.cte,
                updated=ss.stsql_updated,
                available_col_filter=filter_colsname,
            )

        col_filter = read_cte.ColFilter(
            self.expander_container,
            self.cte,
            existing,
            filter_colsname,
            self.base_key,
        )
        if str(col_filter) != "":
            self.filter_container.write(col_filter)

        return col_filter

    def pagination(self, qtty_rows: int, col_filter: read_cte.ColFilter):
        with self.pag_container:
            items_per_page, page = read_cte.show_pagination(
                qtty_rows,
                OPTS_ITEMS_PAGE,
                self.base_key,
            )

        filters = {**col_filter.no_dt_filters, **col_filter.dt_filters}
        if filters != ss.stsql_filters:
            page = 1
            ss.stsql_filters = filters

        return items_per_page, page

    def get_initial_balance(
        self,
        base_cte: CTE,
        stmt_pag: Select,
        no_dt_filters: dict,
        rolling_total_column: str | None,
        rolling_orderby_colsname: list[str],
    ):
        if rolling_total_column is None:
            return 0

        saldo_toogle = self.saldo_toggle_col.toggle(
            f"Adiciona Saldo Anterior em {self.rolling_pretty_name}",
            value=True,
            key=f"{self.base_key}_saldo_toggle_sql_ui",
        )

        if not saldo_toogle:
            return 0

        stmt_no_pag_dt = read_cte.get_stmt_no_pag_dt(base_cte, no_dt_filters)

        orderby_cols = [
            base_cte.columns.get(colname) for colname in rolling_orderby_colsname
        ]
        orderby_cols = [col for col in orderby_cols if col is not None]
        with self.conn.session as s:
            initial_balance = read_cte.initial_balance(
                _session=s,
                stmt_no_pag_dt=stmt_no_pag_dt,
                stmt_pag=stmt_pag,
                rolling_total_column=rolling_total_column,
                orderby_cols=orderby_cols,
            )

        self.saldo_value_col.subheader(
            f"Saldo Anterior {self.rolling_pretty_name}: {initial_balance:,.2f}"
        )

        return initial_balance

    def convert_arrow(self, df: pd.DataFrame):
        cols = self.cte.columns
        for col in cols:
            if isinstance(col.type, SQLEnum):
                col_name = col.name
                df[col_name] = df[col_name].map(lambda v: v.value)

        return df

    def get_df(
        self,
        stmt_pag: Select,
        initial_balance: float,
    ):
        with self.conn.connect() as c:
            df = pd.read_sql(stmt_pag, c)

        df = self.convert_arrow(df)
        if self.rolling_total_column is None:
            return df

        rolling_col_name = f"Balance {self.rolling_pretty_name}"
        df[rolling_col_name] = df[self.rolling_total_column].cumsum() + initial_balance

        return df

    def add_balance_formatter(self, df_style_formatter: dict[str, str]):
        formatter = {}
        for k, v in df_style_formatter.items():
            formatter[k] = v
            if k == self.rolling_total_column:
                rolling_col_name = f"Balance {self.rolling_pretty_name}"
                formatter[rolling_col_name] = v

        return formatter

    def show_df(self, df: pd.DataFrame):
        if df.empty:
            st.header(":red[Tabela Vazia]")
            return None

        column_order = None
        if self.hide_id:
            column_order = [colname for colname in df.columns if colname != "id"]

        df_style = df.style
        formatter = self.add_balance_formatter(self.df_style_formatter)
        df_style = df_style.format(formatter)  # pyright: ignore
        if self.style_fn is not None:
            df_style = df_style.apply(self.style_fn, axis=1)

        selection_state = self.data_container.dataframe(
            df_style,
            use_container_width=self.read_use_container_width,
            height=650,
            hide_index=True,
            column_order=column_order,
            on_select="rerun",
            selection_mode="multi-row",
            key=f"{self.base_key}_df_sql_ui",
        )
        return selection_state

    def get_rows_selected(self, selection_state: DataframeState | None):
        rows_pos = []
        if (
            selection_state
            and "selection" in selection_state
            and "rows" in selection_state["selection"]
        ):
            rows_pos = selection_state["selection"]["rows"]

        return rows_pos

    def crud(self, df: pd.DataFrame, rows_selected: list[int]):
        qtty_rows = len(rows_selected)
        action = update_model.action_btns(
            self.btns_container,
            qtty_rows,
            ss.stsql_opened,
        )

        if action == "add":
            create_row = create_delete_model.CreateRow(
                conn=self.conn,
                Model=self.edit_create_model,
                default_values=self.edit_create_default_values,
            )
            create_row.show_dialog()
        elif action == "edit":
            selected_pos = rows_selected[0]
            row_id = int(df.iloc[selected_pos]["id"])
            update_row = update_model.UpdateRow(
                conn=self.conn,
                Model=self.edit_create_model,
                row_id=row_id,
                default_values=self.edit_create_default_values,
                update_show_many=self.update_show_many,
            )
            update_row.show_dialog()
        elif action == "delete":
            rows_id = df.iloc[rows_selected].id.astype(int).to_list()
            delete_rows = create_delete_model.DeleteRows(
                conn=self.conn,
                Model=self.edit_create_model,
                rows_id=rows_id,
            )
            delete_rows.show_dialog()


def show_sql_ui(
    conn: SQLConnection,
    read_instance,
    edit_create_model: type[DeclarativeBase],
    available_filter: list[str] | None = None,
    edit_create_default_values: dict | None = None,
    rolling_total_column: str | None = None,
    rolling_orderby_colsname: list[str] | None = None,
    df_style_formatter: dict[str, str] | None = None,
    read_use_container_width: bool = False,
    hide_id: bool = True,
    base_key: str = "",
    style_fn: Callable[[pd.Series], list[str]] | None = None,
    update_show_many: bool = False,
) -> tuple[pd.DataFrame, list[int]] | None:
    """Show A CRUD interface in a Streamlit Page

    This function is deprecated and will be removed in future versions. See SqlUi class docs for details on each argument.

     Returns:
         tuple[pd.DataFrame, list[int]]: A Tuple with the DataFrame displayed as first item and a list of rows numbers selected as second item.

    Example:
        See SqlUi class for an example.

    """
    ui = SqlUi(
        conn=conn,
        read_instance=read_instance,
        edit_create_model=edit_create_model,
        available_filter=available_filter,
        edit_create_default_values=edit_create_default_values,
        rolling_total_column=rolling_total_column,
        rolling_orderby_colsname=rolling_orderby_colsname,
        df_style_formatter=df_style_formatter,
        read_use_container_width=read_use_container_width,
        hide_id=hide_id,
        base_key=base_key,
        style_fn=style_fn,
        update_show_many=update_show_many,
    )

    return ui.df, ui.rows_selected
