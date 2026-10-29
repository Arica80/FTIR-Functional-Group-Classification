# FTIR Spectral Image Classification
## Experimental HOG + Linear SVM Baseline

### Dataset
- Total FTIR images: 498
- Training images: 306
- Validation images: 71
- Test images: 71
- Images excluded pending review: 50
- Original categories: alcohol, amine, ketone

### Model
- Feature extraction: Histogram of Oriented Gradients (HOG)
- Classifier: Linear Support Vector Machine
- Input: 256 x 256 grayscale spectral images
- Evaluation: historical train/validation/test partitions

### Results
| Metric | Validation | Test |
|---|---:|---:|
| Accuracy | 0.9155 | 0.8732 |
| Macro F1 | 0.9123 | 0.8709 |

### Error Analysis
- Correct test classifications: 62/71
- Incorrect test classifications: 9/71
- Errors involving multifunctional compounds: 5
- Other misclassifications: 4

Five errors involved compounds possessing multiple
functional groups, highlighting limitations of the
original single-label classification scheme.

### Limitations
The original dataset labels represent folder categories,
not fully verified molecular functional-group annotations.

Molecular identity equivalence across dataset partitions
has not yet been exhaustively audited.

Differences in sample preparation, including KBr and
Nujol, have not yet been systematically characterized.

Therefore, these results represent a preliminary
three-category classification baseline, not validated
multi-label chemical identification.

### Future Work
- Structural validation and molecular identity auditing
- Multi-label functional-group annotation
- Evaluation of sample preparation effects
- Multi-label SVM and CNN development
