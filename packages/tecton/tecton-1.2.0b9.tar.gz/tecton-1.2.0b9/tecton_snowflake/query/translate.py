import typing
from typing import Union

import attrs
import pandas

from tecton_core.query import node_interface
from tecton_core.query import nodes
from tecton_core.query.pandas import node
from tecton_core.query.pandas import nodes as pandas_nodes
from tecton_core.query.pandas import sql
from tecton_snowflake.query import nodes as snowflake_nodes


if typing.TYPE_CHECKING:
    import snowflake.snowpark


@attrs.frozen
class SnowparkExecutor(sql.SqlExecutor):
    session: "snowflake.snowpark.Session"

    def read_sql(self, sql_string: str) -> pandas.DataFrame:
        pandas_df = self.session.sql(sql_string).toPandas()
        return pandas_df

    def sql_to_snowpark(self, sql_string: str) -> "snowflake.snowpark.DataFrame":
        return self.session.sql(sql_string)


def _convert_to_pandas_nodes(
    tree: node_interface.NodeRef, sql_executor: SnowparkExecutor, pretty_sql: bool
) -> Union[node.ArrowExecNode, node.SqlExecNode]:
    # Recurses over RenameColsNodes and MultiOdfvPipelineNode at the top of the tree and converts them to
    # PandasExecNodes and converts only the node immediately below these nodes to a SqlExecNode
    logical_tree_node = tree.node
    node_mapping = {
        nodes.MultiOdfvPipelineNode: pandas_nodes.PandasMultiOdfvPipelineNode,
        nodes.RenameColsNode: pandas_nodes.PandasRenameColsNode,
    }
    if logical_tree_node.__class__ in node_mapping:
        input_node = _convert_to_pandas_nodes(logical_tree_node.input_node, sql_executor, pretty_sql)
        return node_mapping[logical_tree_node.__class__].from_node_inputs(
            logical_tree_node, input_node, column_name_updater=lambda x: x.upper()
        )
    else:
        return node.SqlExecNode.from_sql_inputs(logical_tree_node, sql_executor, pretty_sql)


def _convert_to_snowpark_nodes(
    tree: node_interface.NodeRef, sql_executor: SnowparkExecutor, pretty_sql: bool
) -> [node.SqlExecNode, snowflake_nodes.SnowparkExecNode]:
    # Recurses over RenameColsNodes and MultiOdfvPipelineNode at the top of the tree and converts them to
    # SnowparkExecNodes and converts only the node immediately below these nodes to a SqlExecNode
    logical_tree_node = tree.node
    node_mapping = {
        nodes.MultiOdfvPipelineNode: snowflake_nodes.SnowparkMultiOdfvPipelineNode,
        nodes.RenameColsNode: snowflake_nodes.SnowparkRenameColsNode,
    }
    if logical_tree_node.__class__ in node_mapping:
        input_node = _convert_to_snowpark_nodes(logical_tree_node.input_node, sql_executor, pretty_sql)
        return node_mapping[logical_tree_node.__class__].from_node_inputs(
            logical_tree_node, input_node, column_name_updater=lambda x: x.upper(), session=sql_executor.session
        )
    else:
        return node.SqlExecNode.from_sql_inputs(logical_tree_node, sql_executor, pretty_sql)
