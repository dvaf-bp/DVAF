<> no-automatic-copyright-generation
# Chart.PolarExtra.js

## Build
`gulp build`

## Configuration
```javascript
"data": {
    "labels": ["Red", "Green", "Yellow", "Grey", "Blue"],
    "datasets": [{
        "length": [11, 16, 7, 6, 14],
        "width": [7, 5, 2, 3, 10],
        "color": [7, 5, 2, 3, 10], // Replaces backgroundColor, calculates color based on percentage (color[i] / colorBase), 0=green - 1=red
    }]
},
"options": {
    "text": "96%", // Text in center of graph
    "widthBase": 10, // Maximum value of width
    "colorBase": 10, // Maximum value of color
    "alwaysShowLabel": true, // Show lables in slices. Default: false
    "toFixed": 1, // Round in label. Default: 2
    "lengthLabel": "Length", // Label for data
    "widthLabel": "Width", // Label for width
    "colorLabel": "Color", // Label for color
    "opacity": 0.5, // Default: 0.5
}
```