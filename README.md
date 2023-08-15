# Codon optimization tool

_This tool was developed as part of MIT's 2023 iGEM team software. For more information, see our [wiki](https://2023.igem.wiki/mit/)._

Prior to ordering custom DNA sequences intended for transfection, it is imperative for researchers to optimize codons for the host organism. Specifically, codon optimization refers to the process of changing codons without changing their encoded amino acids in order to accommodate the codon bias inherent to the host organism. This increases both gene expression and translational efficiency of the gene of interest.

Though some online tools exist to aid in codon optimization, our team faced significant uncertainty and confusion while trying to utilize them, and results were frequently irreproducible and did not reflect expectations based on codon frequency charts. Thus, we decided to create software that accurately optimizes sequences with consistent results. We have implemented optimization for many frequently used host organisms, including homo sapiens, mus musculus, and cricetulus griseus. We hope that our tool will provide a straightforward method for future iGEM teams and other researchers to optimize their codons.
