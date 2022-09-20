{"name": "radialbars", "function": "radial_chart", "source": "visualizations/radialbars.js", "language": "javascript", "label": "Radial", "description": "A circular bar chart", "icon": "fa-light fa-bullseye", "build": "true", "params": [{"name": "x", "label": "Label", "single": true, "description": "The column containing the labels of the charts", "value": []}, {"name": "y", "label": "Value", "single": true, "description": "the column containing the values the areas they occupy in the rectagular area should be propotional to", "value": []}, {"name": "wafflesizelabel", "label": "Size", "description": "The size of the large rectangle", "value": [{"control": "number", "value": "250"}]}, {"name": "palette", "label": "D3 Palette", "description": "the D3 Palette to determine the color scheme to use", "value": [{"control": "paletteSelect", "value": "schemeTableau10", "values": ["schemeTableau10", "schemeAccent", "schemeDark2", "schemePaired", "schemeSet1", "schemeSet2", "schemeSet3"]}]}]}