for pol in T E B
do
    papermill plot_cl.ipynb out_plot_cl_${pol}.ipynb -p pol $pol
    URL=$(gh gist create --public "out_plot_cl_${pol}.ipynb")
    echo "* [${pol}](${URL/gist.github.com/nbviewer.org\/gist})" >> README.md
done
