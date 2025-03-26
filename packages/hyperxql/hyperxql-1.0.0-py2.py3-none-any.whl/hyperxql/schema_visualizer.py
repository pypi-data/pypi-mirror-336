"""
Schema visualization module for HyperXQL.
Generates visual representations of database schemas.
"""

import os
import tempfile
from typing import Dict, Any, List, Optional, Tuple
import logging
import base64

# Configure logging
logger = logging.getLogger(__name__)

# Try to import pydot for visualization
PYDOT_AVAILABLE = False
try:
    import pydot
    PYDOT_AVAILABLE = True
except ImportError:
    logger.warning("pydot not available. Schema visualization will be disabled.")
    # Create a minimal pydot stub for type checking
    class DummyPydot:
        class Dot:
            def __init__(self, *args, **kwargs):
                pass
            def add_node(self, *args, **kwargs):
                pass
            def add_edge(self, *args, **kwargs):
                pass
            def get_nodes(self):
                return []
            def write_svg(self, *args, **kwargs):
                pass
            def write_png(self, *args, **kwargs):
                pass
        class Node:
            def __init__(self, *args, **kwargs):
                pass
            def get_name(self):
                return ""
            def get_attributes(self):
                return {}
        class Edge:
            def __init__(self, *args, **kwargs):
                pass
    pydot = DummyPydot


class SchemaVisualizer:
    """Generator for database schema visualizations."""

    def __init__(self):
        """Initialize the schema visualizer."""
        self.graph = None
        self.node_styles = {
            'table': {
                'shape': 'record',
                'fontname': 'Arial',
                'fontsize': '12',
                'style': 'rounded,filled',
                'fillcolor': '#1e1e24',
                'color': '#404040',
                'fontcolor': 'white',
                'margin': '0.3',
                'penwidth': '1.5'
            }
        }
        self.edge_styles = {
            'foreign_key': {
                'fontname': 'Arial',
                'fontsize': '10',
                'color': '#555555',
                'fontcolor': '#aaaaaa',
                'arrowhead': 'crow',
                'arrowtail': 'none',
                'style': 'dashed',
                'penwidth': '1.2'
            }
        }

    def generate_schema_visualization(self, db_info: Dict[str, Any], output_format: str = 'svg') -> str:
        """
        Generate visualization of database schema.

        Args:
            db_info: Database information dictionary
            output_format: Output format ('svg', 'png', etc.)

        Returns:
            Path to generated visualization or base64 encoded string
        """
        # Check if pydot is available
        if not PYDOT_AVAILABLE:
            logger.error("Cannot generate schema visualization: pydot is not available")
            return ""

        try:
            # Create a new directed graph
            self.graph = pydot.Dot('database_schema', graph_type='digraph', bgcolor='transparent')

            # Add tables as nodes
            if db_info.get('tables'):
                for table in db_info['tables']:
                    self._add_table_node(table)

                # Add foreign key relationships as edges
                for table in db_info['tables']:
                    if table.get('foreign_keys'):
                        for fk in table['foreign_keys']:
                            self._add_foreign_key_edge(table['name'], fk)

            # Generate output in the specified format
            if output_format == 'svg':
                return self._generate_svg()
            elif output_format == 'png':
                return self._generate_png()
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
        except Exception as e:
            logger.error(f"Error generating schema visualization: {e}")
            return ""

    def _add_table_node(self, table: Dict[str, Any]):
        """Add a table as a node to the graph."""
        if not self.graph:
            return
            
        # Header with table name
        label = f"{{<f0> {table['name']} |"

        # Add columns
        for i, column in enumerate(table['columns']):
            port = f"f{i+1}"
            
            # Create column icon based on column properties
            if column.get('primary_key'):
                icon = "PK "  # Primary key indicator
            elif column.get('foreign_key'):
                icon = "FK "  # Foreign key indicator
            else:
                icon = "   "  # Regular column
                
            column_str = f"<{port}> {icon}{column['name']}"
            
            # Add data type without HTML formatting
            column_str += f" : {column['type']}"
            
            # Add separator if not the last column
            if i < len(table['columns']) - 1:
                column_str += "|"
                
            label += column_str

        label += "}"

        # Create node
        node = pydot.Node(table['name'], label=label, **self.node_styles['table'])
        self.graph.add_node(node)

    def _add_foreign_key_edge(self, table_name: str, foreign_key: Dict[str, Any]):
        """Add a foreign key relationship as an edge to the graph."""
        if not self.graph:
            return
            
        source = f"{table_name}:f{self._get_column_index(table_name, foreign_key['column']) + 1}"
        target = f"{foreign_key['referred_table']}:f{self._get_column_index(foreign_key['referred_table'], foreign_key['referred_column']) + 1}"
        
        # Create edge
        edge = pydot.Edge(source, target, **self.edge_styles['foreign_key'])
        self.graph.add_edge(edge)

    def _get_column_index(self, table_name: str, column_name: str) -> int:
        """Get the index of a column in a table."""
        if not self.graph:
            return 0
            
        nodes = self.graph.get_nodes()
        for node in nodes:
            if node.get_name().strip('"') == table_name:
                attributes = node.get_attributes()
                if 'label' in attributes:
                    label = attributes['label']
                    parts = label.split('|')
                    
                    if len(parts) > 1:  # Has columns
                        columns_part = '|'.join(parts[1:])
                        columns_part = columns_part.strip('{').strip('}')
                        column_parts = columns_part.split('|')
                        
                        for i, col_part in enumerate(column_parts):
                            if column_name in col_part:
                                return i
                                
        return 0

    def _generate_svg(self) -> str:
        """Generate SVG visualization and return as base64."""
        if not self.graph:
            return ""
            
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            tmp_path = tmp.name
            
        # Generate SVG
        self.graph.write_svg(tmp_path)
        
        # Read SVG content
        with open(tmp_path, 'rb') as f:
            svg_content = f.read()
            
        # Remove temporary file
        os.unlink(tmp_path)
        
        # Return SVG as base64
        return base64.b64encode(svg_content).decode('utf-8')

    def _generate_png(self) -> str:
        """Generate PNG visualization and return as base64."""
        if not self.graph:
            return ""
            
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
            
        # Generate PNG
        self.graph.write_png(tmp_path)
        
        # Read PNG content
        with open(tmp_path, 'rb') as f:
            png_content = f.read()
            
        # Remove temporary file
        os.unlink(tmp_path)
        
        # Return PNG as base64
        return base64.b64encode(png_content).decode('utf-8')