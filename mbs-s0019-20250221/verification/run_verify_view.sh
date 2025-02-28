#!/bin/bash

components=(
"galactic_foregrounds_d1s1"
"galactic_foregrounds_lowcomplexity"
"galactic_foregrounds_mediumcomplexity"
"galactic_foregrounds_highcomplexity"
)

echo "# Visual inspection of maps" >> README.md
echo "" >> README.md

for component in "${components[@]}"
do
        papermill verify_map_view.ipynb verify_map_view_$component.ipynb -p component $component
        URL=$(gh gist create --public "verify_map_view_$component.ipynb")
        echo "* [${component}](${URL/gist.github.com/nbviewer.org\/gist})" >> README.md
done
