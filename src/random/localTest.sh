#for f in ./test/*.cnf
for f in ~/../../media/andre/LinUXB/research-project/test02/*.cnf
do 
    $f >> numberOfSolutions.txt
    (./../sharpSAT/build/Release/sharpSAT $f ) >> numberOfSolutions.txt
done
