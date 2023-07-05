for telescope in SAT LAT
do
    for pol in T E B
    do
        URL=$(gh gist create --public "out_plot_cl/plot_cl_${telescope}_${pol}.ipynb")
        echo "* [${telescope} ${pol}](${URL/gist.github.com/nbviewer.org\/gist})" >> README.md
    done
done
