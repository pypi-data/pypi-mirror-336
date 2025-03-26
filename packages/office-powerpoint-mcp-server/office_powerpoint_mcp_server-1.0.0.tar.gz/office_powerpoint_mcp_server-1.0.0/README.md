# Office-PowerPoint-MCP-Server

An MCP (Model Context Protocol) server for PowerPoint manipulation using python-pptx. This server provides tools for creating, editing, and manipulating PowerPoint presentations through the MCP protocol.

## Features

- Round-trip any Open XML presentation (.pptx file) including all its elements
- Add slides
- Populate text placeholders, for example to create a bullet slide
- Add image to slide at arbitrary position and size
- Add textbox to a slide; manipulate text font size and bold
- Add table to a slide
- Add auto shapes (e.g. polygons, flowchart shapes, etc.) to a slide
- Add and manipulate column, bar, line, and pie charts
- Access and change core document properties such as title and subject

## Installation

### Prerequisites

- Python 3.6 or higher
- python-pptx
- mcp[cli] (MCP's Python SDK)

### Setup

1. Install the required packages:

```bash
pip install python-pptx mcp[cli]
```

2. Clone or download this repository:

```bash
git clone https://github.com/GongRzhe/Office-PowerPoint-MCP-Server.git
cd Office-PowerPoint-MCP-Server
```

3. Make the server executable:

```bash
chmod +x ppt_mcp_server.py
```

## Usage

### Starting the Server

Run the server:

```bash
python ppt_mcp_server.py
```

### MCP Configuration

Add the server to your MCP settings configuration file:

```json
{
  "mcpServers": {
    "ppt": {
      "command": "python",
      "args": ["/path/to/ppt_mcp_server.py"],
      "env": {}
    }
  }
}
```

## Available Tools

### Presentation Tools

- **create_presentation**: Create a new PowerPoint presentation
- **open_presentation**: Open an existing PowerPoint presentation from a file
- **save_presentation**: Save the current presentation to a file
- **get_presentation_info**: Get information about the current presentation
- **set_core_properties**: Set core document properties of the current presentation

### Slide Tools

- **add_slide**: Add a new slide to the current presentation
- **get_slide_info**: Get information about a specific slide
- **populate_placeholder**: Populate a placeholder with text
- **add_bullet_points**: Add bullet points to a placeholder

### Text Tools

- **add_textbox**: Add a textbox to a slide

### Image Tools

- **add_image**: Add an image to a slide
- **add_image_from_base64**: Add an image from a base64 encoded string to a slide

### Table Tools

- **add_table**: Add a table to a slide
- **format_table_cell**: Format a table cell

### Shape Tools

- **add_shape**: Add an auto shape to a slide

### Chart Tools

- **add_chart**: Add a chart to a slide

## Examples

### Creating a New Presentation

```python
# Create a new presentation
result = use_mcp_tool(
    server_name="ppt",
    tool_name="create_presentation",
    arguments={}
)
presentation_id = result["presentation_id"]

# Add a title slide
result = use_mcp_tool(
    server_name="ppt",
    tool_name="add_slide",
    arguments={
        "layout_index": 0,  # Title slide layout
        "title": "My Presentation",
        "presentation_id": presentation_id
    }
)
slide_index = result["slide_index"]

# Populate subtitle placeholder
result = use_mcp_tool(
    server_name="ppt",
    tool_name="populate_placeholder",
    arguments={
        "slide_index": slide_index,
        "placeholder_idx": 1,  # Subtitle placeholder
        "text": "Created with PowerPoint MCP Server",
        "presentation_id": presentation_id
    }
)

# Save the presentation
result = use_mcp_tool(
    server_name="ppt",
    tool_name="save_presentation",
    arguments={
        "file_path": "my_presentation.pptx",
        "presentation_id": presentation_id
    }
)
```

### Adding a Chart

```python
# Add a chart slide
result = use_mcp_tool(
    server_name="ppt",
    tool_name="add_slide",
    arguments={
        "layout_index": 1,  # Content slide layout
        "title": "Sales Data",
        "presentation_id": presentation_id
    }
)
slide_index = result["slide_index"]

# Add a column chart
result = use_mcp_tool(
    server_name="ppt",
    tool_name="add_chart",
    arguments={
        "slide_index": slide_index,
        "chart_type": "column",
        "left": 1.0,
        "top": 2.0,
        "width": 8.0,
        "height": 4.5,
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series_names": ["2023", "2024"],
        "series_values": [
            [100, 120, 140, 160],
            [110, 130, 150, 170]
        ],
        "has_legend": True,
        "legend_position": "bottom",
        "has_data_labels": True,
        "title": "Quarterly Sales",
        "presentation_id": presentation_id
    }
)
```

## License

MIT
