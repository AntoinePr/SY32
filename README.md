# SY32
## Context of the project
Machine learning based program able to detect bodies on pictures.
* Read [training images](https://github.com/AntoinePr/SY32/tree/master/projetpers/train) and the [bodies locations](https://github.com/AntoinePr/SY32/tree/master/projetpers/train) inside them
* Randomly generates negative samples from files
* Transforms pictures into normalized vectors
* Learn from vectors with sklearn.SVM
* Run the body detection on the input images while saving all false negatives and false positives
* Relearn with initial images plus the false negatives and false positives
* Detects the bodies from [input pictures](https://github.com/AntoinePr/SY32/tree/master/projetpers/test)
## How to launch
Run the [main.py](https://github.com/AntoinePr/SY32/tree/master/main.py) file as below
```
python main.py
```
The results will be stored in the results.txt file

