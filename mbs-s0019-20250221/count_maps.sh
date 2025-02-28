for f in output/*
do
    echo $f, $(ls $f | wc -l)
done
