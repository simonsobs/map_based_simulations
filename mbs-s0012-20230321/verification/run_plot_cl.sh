for telescope in SAT LAT
do
    for pol in T E B
    do
        papermill --prepare-only plot_cl.ipynb out_plot_cl/plot_cl_${telescope}_${pol}.ipynb -p input_telescope $telescope -p pol $pol
    done
done
