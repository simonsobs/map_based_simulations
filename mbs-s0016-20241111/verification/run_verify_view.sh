#!/bin/bash

components=(
"galactic_foregrounds_lowcomplexity_websky"
"galactic_foregrounds_mediumcomplexity_websky"
"galactic_foregrounds_highcomplexity_websky"
)

echo "# Visual inspection of maps - Websky" >> README.md
echo "" >> README.md

for component in "${components[@]}"
do
        papermill verify_map_view.ipynb verify_map_view_$component.ipynb -p component $component
        URL=$(gh gist create --public "verify_map_view_$component.ipynb")
        echo "* [${component}](${URL/gist.github.com/nbviewer.org\/gist})" >> README.md
done
