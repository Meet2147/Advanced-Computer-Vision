_________________________________________________________________________________________
Panel DATA
__________________________________________________________________________________________

xtset c y
## normal OLS
regress  roa c y ta de lq nexp nimp iipcg intr
estimates store OLS

## xi ? means repeat   creates 100 dummy variables
## Least Square Dummy Variable
xi: regress  roa  ta de lq nexp nimp iipcg intr i.c
estimates store LSDV

##areg — Linear regression with a large dummy-variable set
areg  roa  ta de lq nexp nimp iipcg intr, absorb(c)
estimates store AREG

## Comparison
estimates table OLS LSDV AREG,star stats(N r2 r2_a)

xtreg  roa  ta  de lq nexp nimp iipcg intr, fe
estimates store fe
xtreg  roa  ta  de lq nexp nimp iipcg intr, re
estimates store re

#hausman test
hausman fe re
## prob less than 0.05 then use fe model

##post estimation test for re model
xtreg  roa  ta  de lq nexp nimp iipcg intr, re
xttest0
##prob<0.05 then random effects are present


______________________________________________________________________________________
Quantile regression
______________________________________________________________________________________

##Quantile Regression
##Copy the panel data in the Data Editor.
##1.Rename all the variables.
rename var1 c
rename var2 y
rename var3 roa
rename var4 ta
rename var5 de
rename var6 lq
rename var7 nexp
rename var8 nimp
rename var9 iipcg
rename var10 intr

##2.Set the time series to panel data
xtset c y, yearly

##3.
	reg roa ta de lq nexp nimp iipcg intr
 
##4.
	xtreg roa ta de lq nexp nimp iipcg intr
 
##Sigma_u is between class error.  Sigma_e is error within groups.
##Rho = 15% profitability is captured(correlation between the classes)

##5.
xtreg roa ta de lq nexp nimp iipcg intr, fe
 

##Rho = 25% profitability due to no inclusion of time invariant features

##6.	
estimates store fe

##7.	
xtreg roa ta de lq nexp nimp iipcg intr, re
 
##Rho = 15.4%

##8.	
estimates store re

##9.	
hausman fe re
 
##If prob<0.05, then it is following fixed effects. Else it is random effects.
##10.	
qreg  roa ta de lq nexp nimp iipcg intr

##Quantiles are for the whole dataset and not created separately for every country.100% quantile regression.
##11.	 
quantile roa, recast(scatter)

##Plot roa on quantile chart. 
##12.	
qreg roa ta de lq nexp nimp iipcg intr, q(.5)

##50% quantiles are taken and similar to regression output where every variable is evaluated and its significance is given.
##13.	
grqreg, cons ci ols olsci reps(40)

##Reps are iterations. Graphical interpretation of qreg.
##14.	
summarize roa ta de lq nexp nimp iipcg intr

##15.	
 estat hettest
 
##Prob is lesser than 0.0001.if prob<0.05, alternate hypothesis is accepted where it is heteroskedastic. else null hypothesis is accepted and there is constant variance,homoskedasticity.Homoskedasticity means that the error values are evenly distributed across the best fit line while heteroskesdasticity means that the error values are not evenly distributed.

##16.	
estat imtest

##If total P<0.05 then it is heteroskedastic else homoscedastic. 
##17.	

vif

##Variance Inflation factor. – used for testing multicollinearity. If value < 10 then no multicollinearity but if greater then there is a presence of multicollinearity.
##18.	
predict resid, residuals

##19.	
histogram resid, kdensity normal

##20.	
sqreg roa ta de lq nexp nimp iipcg intr, q(0.10) reps(50)
##simultaneous quantile regression – regresses variables on the top 10 % of the data



______________________________________________________________________________________
VAR
______________________________________________________________________________________

tsset date, weekly

## check for stationarity. T-stats should be lesser than the critical values then the series is stationary
dfuller brazil, lags(0)
dfuller brazil
dfuller  rbrazil
dfuller  rbrazil, lags(0)
dfuller   rchile, lags(0)
dfuller  rcolombia,lags(0)
dfuller  rcostarica,lags(0)
dfuller  rperu,lags(0)
dfuller   rvenezuela,lags(0)

### If not stationary then differentiate using D.brazil
dfuller D.brazil
## Series stationary at the first difference

## Graphical representation of ACF and PACF
corrgram brazil
corrgram rbrazil
pac brazil, lags(10)
pac rbrazil,lags(10)

## Another test for checking stationarity
pperron  brazil, lags(5)
pperron  rbrazil


## Basic VAR model
varbasic rbrazil rchile rcolombia rcostarica rperu rvenezuela, lags(1/2) step(8) 
If prob < 0.05 then rbrazil is significant. Hence we conclude brazil affects itself in Week1 . Brazil affects Columbia in Week 2  and peru in week 1. Do the same analysis for the entire output
(USED FOR STOCK MARKET ANALYSIS)

varsoc rbrazil rchile rcolombia rcostarica rperu rvenezuela, maxlag(7)

 
## To select the optimal lag length for the VAR model choose the lag in which me have max no.of *’s with AIC being most important. So in this case lag is 1

var rbrazil rchile rcolombia rcostarica rperu rvenezuela, lags(1/1)
## Same interpretation as above

## Impulse response Graphs
irf graph irf, irf(varbasic) impulse(rbrazil) response(rcolombia)
irf graph irf, irf(varbasic) impulse(rbrazil) response(rchile rcolombia rcostarica)


GRANGER CASUALITY

Vargranger
## helps us know if one time series helps estimating another time series
 
Brazil is causally related to peru and ALL. It means rbrazil and lags of rbrazil are used to predict rperu and ALL

POST ESTIMATION TEST (VAR)

Varlmar
## Explain the o/p given below the table 
Varstable
## Explain the o/p given below the table
 

Varnorm
H0 : All variables are normally distributed in VAR
Hence as all prob values are less than 0.05 we reject H0.
So the variables are not normally distributed.


_____________________________________________________________________________________
ARCH and Garch
_____________________________________________________________________________________


1.	 tsset date, yearly
        time variable:  date, 1 to 1060
                delta:  1 year
2.	ac rbrazil
 
Hence taking the MA(2)
3.	pac rbrazil
 
Hence take the AR(2)

4.	arima rbrazil,arima(2,0,2)
Estat ic – make a note of all aics. For all combinations. If that model has lowest aic , finalize that one. Predict res,residual, plot pac of that res – if the lines lie in the grey area(confidence interval then it should be fine)
5.	regress rbrazil
 
6.	predict res,residuals
7.	predict res2, residuals
8.	twoway(tsline res2)
 
Rbrazil – stationary or not? Mean reverting or not? 
Mean across the horizontal line is uniform, and vertical distance is to be considered.
This graph is mean reverting.
9.	regress res2
 
Res2 not significant
10.	estat archlm, lag(1/10)
 
11.	display 42.715 - 26.491
12.	display chi2tail(1,16.224)
13.	 
display 85.588-70.375
15.
display chi2tail(1,15.213)
14.	arch res2, ar(1/2) arch(1)
15.
arch res2, ar(1/2) arch(1/2) garch(1/1)


_________________________________________________________________________________________
SIMULTANEOUS EQUATION MODEL
_________________________________________________________________________________________

## Declaring time series variable
tsset year, yearly

## Regress pdi
regress  pdi  mcap  gdp  m3  gdcf  fii  nds  gds
## gdp m3 nds gds are significant

## Take any one of the significant variable
regress gds  mcap  gdp  m3  gdcf  fii  nds

##Predict hat value
predict gds_hat,xb

## regress pdi with the predicted value
regress  pdi  mcap  gdp  m3  gdcf  fii  nds  gds_hat
## If the predicted value is significant then GDS is ENDOGENOUS.

## Proving endoginity of gds – 2SLS
## Instrumental variable – currently not significant but may be significant in future (nds)
ivregress 2sls pdi mcap m3 gdp gdcf fii (gds = nds)
## gds is still significant hence ENDOGENOUS

## Proving endoginity of gds – 3SLS
reg3 (pdi = mcap gdp m3 gdcf fii gds), exog(mcap gdp m3 fii gdcf) endog(gds) allexog
## gds is significant hence it is endogenous


_________________________________________________________________________________________
VECM
_________________________________________________________________________________________

vecrank rbrazil rchile rcolombia rcostarica rperu rvenezuela, trend(constant)
 

## No *’s so no cointegrating vectors

vecrank brazil chile  colombia costarica peru venezuela, trend(constant)
 
vecrank brazil chile  colombia costarica peru venezuela, trend(constant) lags(4)
 
(SIR’s Notes -  Take lag as 4 or 8)

vec brazil chile colombia costarica  peru venezuela, trend(constant) lags(4)
 
## Brazil will cointegrate with itself at lag 1, with peru at lag 1 and with Columbia at lag 2
(If u put lag as 4 o/p will have -1 lags)

test(LD.peru LD.brazil)
 
## Another way to test cointegration. If prob <0.05 cointegrated

POST ESTIMATION TEST (VECM)

veclmar, mlag(5)
vecnorm, jbera skewness kurtosis


________________________________________________________________________________________
Autoregressive Distributing-Lag Model (ARDL)
________________________________________________________________________________________


_________________________________________________________________________________________
ARIMA
_________________________________________________________________________________________

1.	 tsset date, yearly
        time variable:  date, 1 to 1060
                delta:  1 year
2.	## check for stationarity. T-stats should be lesser than the critical values then the series is stationary
dfuller brazil, lags(0)
dfuller brazil

### If not stationary then differentiate using D.brazil
dfuller D.brazil
## Series stationary at the first difference

## Graphical representation of ACF and PACF
corrgram brazil
corrgram rbrazil

2. ac rbrazil
 
Hence taking the MA(2)
3.	pac rbrazil
 
Hence take the AR(2)

4.	arima rbrazil,arima(2,0,2)
Estat ic – make a note of all aics. For all combinations. If that model has lowest aic , finalize that one. Predict res,residual, plot pac of that res – if the lines lie in the grey area(confidence interval then it should be fine)
