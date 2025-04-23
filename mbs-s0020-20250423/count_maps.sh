for f in output/SAT_4096/*
do
    echo $f, $(ls $f | wc -l)
done
