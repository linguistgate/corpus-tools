## The functions contained in the file are:

## c.(x) : center a predictor
## z.(x) : standardize (z-transform) a predictor
## r.(formula, ...) : return standardized residuals from regressing a predictor against at least one other predictor
## s.(x) : apply a transformation from Seber 1977 that puts the data in the range [-1,1]
## p.(x, ...) : polynomial terms around x (uses orthogonal polynomials by default, see ?poly)


c. <- function (x) scale(x, scale = FALSE)
z. <- function (x) scale(x)
r. <- function (formula, ...) rstandard(lm(formula, ...))
l. <- function (x) log(x)
s. <- function (x) {
    ## Seber 1977 page 216, from http://dx.doi.org/10.1021/ie970236k
    ## Transforms continuous variable to the range [-1, 1]
    ## In linked paper, recommended before computing orthogonal
    ## polynomials
    (2 * x - max(x) - min(x)) / (max(x) - min(x))
}
p. <- function (x, ...) poly(x, ...)
