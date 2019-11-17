_________________________________________________________________________________________
Panel DATA
__________________________________________________________________________________________
They are Multi-Dimensional Data invloving measurnments over-time.It contains observation
 of multiple phenomena obtained over multiple time period for same individual. 
 In this session, we focus on two techniques use to analyze panel data:
 1.Fixed effects 2.Random effects

1.Fixed Effect
Fixed Effect Model: Use fixed-effects (FE) whenever you are only interested in analyzing
the impact of variables that vary over time.FE explore the relationship between 
predictor and outcome variables within an entity (country, person, company, etc.). 
Each entity has its own individual characteristics that may or may not influence 
the predictor variables (for example, being a male or female could influence the 
opinion_toward certain issue). When using FE we assume that something within the 
individual may impact or bias the predictor or outcome variables and we need to 
control for this. This is the rationale behind the assumption of the correlation
 between entity’s error term and predictor variables. FE remove the effect of those
 time-invariant characteristics so we can assess the net effect of the predictors on 
 the outcome variable. Another important assumption of the FE model is that 
 those time-invariant characteristics are unique to the individual and 
 should not be correlated with other individual characteristics.
 Each entity is different therefore the entity’s error term and the constant 
 (which captures individual characteristics) should not be correlated with the others.
 If the error terms are correlated, then FE is no suitable since inferences may not
 be correct and you need to model that relationship, this is main rationale for hausman 
 test.The equation for the fixed effects model becomes
 Yit=beta_1 Xit + alpha_i + Uit
 Where alpha_i = (i =1.... n) is the unknown intercept for each entity 
(entity-specific intercepts). 
Yit = is the dependent variable (DV) where i = entity and t = time.
Xit = represents one independent variable,
Bi = is the coefficient for that independent variable,
uit = is the error term 
The key insight of Fixed Effect Model:
1. The key insight is that if the unobserved variable does not change over time,
 then anychanges in the dependent variable must be due to influences other than these 
 fixed characteristics. 
 2.In the case of time-series cross-sectional data the interpretation of the 
 beta () coefficients would be for a given country, as X varies across time by one unit 
 and hence, Y increases or decreases by f units. 
 3.Fixed-effects will not work well with data for which within-cluster variation is 
 minimal or for slow changing variables over time.
 
 KEY NOTE ON FIXED-EFFECTS
The fixed-effects model controls for all time-invariant differences between the
individuals, so the estimated coefficients of the fixed-effects models cannot 
be biased because of omitted time- invariant characteristic like culture, religion, 
gender, working culture of the company,Management structure, ete. One side limitation
 of fixed-effects models is that it cannot be used to investigate time- invariant 
 causes of the dependent variables. Technically, time-invariant characteristics 
 of the individuals are perfectly collinear with entity dummies. Functionally, 
 fixed-effects models are designed to study the causes of changes within a person
 [or entity]. But a time-invariant characteristic cannot cause such a change, 
 because it is constant for each person.

RANDOM-EFFECTS MODEL
The rationale behind random effects (RE) model is that, unlike the fixed effects model, 
the variation across entities is assumed to be random and uncorrelated with the 
predictor or independent variables included in the model. If you have reason to
believe that differences across entities have some influence on your dependent 
variables, then you should use random effects. 
An advantage of random effects is that you can include time invariant variables
(i.e. gender). In the fixed effects model these variables are absorbed by the 
intercept. The random effects model is:
Yit=Beta Xit+ alpha + Uit + Eit ,where Uit = Between entity error Eit = Within entity error

Random effects assume that the entity’s error term is not correlated with the predictors 
which allows for time-invariant variables to play a role as explanatory variables. 
In random effect you need to specify those individual characteristics that may or 
may not influence the a variables. The problem with this is that some variables may not
be available therefore leading to omitted variable bias in the model. RE allows to 
generalize the inferences beyond the sample used in the model.
 
Hausman test is to decide between Fe and Re model is fitted the data the most, we can run
it. HO is The preferred model is Random effect
    Ha is the preferred model id Fixed effect.
It basically test whether the unique error (between entity error are correlated with 
the regressor). And hence,the null hypothesis is Ui are not correlated with X's.

Stata Panel Data

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
Standard linear regression techniques summarize the average relationship between a set
of regressors and the outcome variable based on the conditional mean function E(ylx).
This provides only a partial view of the relationship,as we might be interested in 
describing the relationship at different points in the conditional distribution of y.
Quantile regression provides that capability. Analogous to the conditional mean 
function of linear regression,we may consider the relationship between the regressors 
and outcome using the conditional median function Q_q(ylx),where the median is the 
50th percentile,or quantile q,of the empirical distribution.
The quantile qE(0,1)is that y which splits the data into proportions q below 
and l-q above. If e_i is the model prediction error,OLS minimizes summation(e_i)^2 . 
However,median regression, also known as least-absolute-deviations(LAD)regression,
that minimizes summazion_mod(e_i).Quantile regression minimizes a sum that gives 
asymmetric penalties(1-q)mod(e_i) for over prediction and qmod(e_i) for under prediction.
Although its computation requires linear programming methods,the
quantile regression estimator is asymptotically normally distributed.
Median regression is more robust to outliers than least squares regression,and is
semiparametric as it avoids assumptions about the parametric distribution of the 
error process.

Advantages of quantlle regresslon(QR):
1. QR has flexibility for modeling data with heterogeneous conditional distributions.
2. Median regression is moro robust to outliers than tho OLS regression.
3.lt has richer characterizntion and description of the data that can show different 
effects of the independent variables on tho dopendent variable depending across the 
spectrum of the dependent variable.
4.While OLS can bo inefficient if the errors are highly non-normal,QR is more robust
to non-normal errors and outliers,QR also provides a richer characterization of the
data,allowing us to consider the impoct of a covarinte on the entire distribution of
y,not merely its conditional mean.
5.Furthermore,QR is invariant to monotonic transformations such as log(.),so the
qunntiles of h(y),a monotone transform of Y,are h(Q(y)),and the inverse
transformation may be used to translate the results back to Y.This is not possible for
the mean as E[h(y)] not equal h[E(y)).
The quantile regression is described by the following equation:
Y_i = X_i(dash)*Beta_q + e_t

where Beta_q is the vector of unknown parameters associated with the q_th quantile.
While OLS minimizes sum of squares of the model prediction error (Ee),the median
regression,(called as least absolute-deviation regression)minimizes sum of absolute
error(summation(q mod(e_i)).The QR minimizes(summation(q mod(e_i))+
(summation((1-q) mod(e_i)),that is a sum that gives the asymmetric
penalty to q mod(e_i) for under prediction and(1-q)mod(e_i) for over prediction.

Stata Quantile regression

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
1.Autoregression implies pressure of lagged values of the dependent variable on the 
righthand side ofthe equation. 2.Vector implies. it is a system of equation that contains 
a vector of two or more variables. 3.VAR model is estimated or approximated to be used,
if the variables are integrals oi order one i.e. all the variables should be integrated 
at 1 st difference.4.If the variables are co-integrated, then we have the scope to 
estimate both short-run VAR and long-run Vector Error Correction Models (VECM).
5.If variables are not co-integrated, then we can maximum estimate short-run VAR models. 
6.All the variables in a VAR system are endogenous and there are no endogenou variables.
7.The stochastic error terms of the 'AR model are called impulse or innovation shocks.

A VAR model of 3 variables with kth log would look like:
Pdi_t = alpha + summation(beta_i *Pdi_(t-i))+summation(delta_i *gdcf_(t-i))
+summation(gamma_i *gdp_(t-i)) + u_t1
gdcf_t=alpha + summation(beta_i *Pdi_(t-i))+summation(delta_i *gdcf_(t-i))
+summation(gamma_i *gdp_(t-i)) + u_t2
gdp_t=alpha + summation(beta_i *Pdi_(t-i))+summation(delta_i *gdcf_(t-i))
+summation(gamma_i *gdp_(t-i)) + u_t3

Here note that RHS. constraints all the variables of its log. 
Hence a potential reason to av exogeneity.
•	In VAR, dependent variable of eq. (I) is a function of its own log and 
the log values of the other endogenous variables.
•	In VAR all the RHS variables are in equal log. This is the optimal log of the no 
Moreover, using equal log length, makes the model simple to estimate and help model specification.
•	Most importantly, in VAR all the variables must be in level, not in the 1 st differe But they must be stationary at 1 st difference.
•	A VAR model is estimated by OLS estimates
 Identification of proper log-length is very important. 
 Unnecessarily high log-length cause the models to lose degrees of freedom and may 
suffer by problems of Multi Collinearity.similarly. too few log (less than the optimum) 
may cause specification error. Hence,it is important to identify optimal log length.
VAR coefficients are explained with the assumption ofCeteris-Paribus.
 
 Need for VAR Model
•When there is no co-integration among the variables of the system, all the variables
 are assumed to be independent, then it is appropriate to use VAR.
•If we want to establish causal relationships among a group of variables are "a. 
theoretical or have no-theoretical relationships" among themselves; the VAR is more
 suitable to be estimated.
•If we want to measure the impulse to one variable and its response to whole system of
 variables, then VAR can be used.
 
 Steps to USE VAR Model
 
•	Test for unit root/stationarity.

•	Test for optimum log length.   
    Estimate VAR.
•	Estimate impulse response & variance decomposition.

Granger Causality Test

Christopher A. Sims ( 1972) has developed a practical technique of testing causality in a bi-variate model.
According to Sims, one can regress Y on past values and future values of X and if 
causality runs from X to Y only, future values of X in the regression should have 
coefficients significantly different from zero. To explain the Granger test, 
let us consider two variables GDP and exports (X). test assumes that the 
information relevant to the prediction of the respective variables. 
GDP and X is contained solely in the time series data on these variables. 
The test involves the estimation of following pair of regression:
 
GDP_t=Summation(i=1 to n)(Alpha_i * X_(t-i))+Summation(j=1 to n)(Beta_i * GDP_(t-j))+E_1t
X_t=Summation(i=1 to n)(Gamma_i * X_(t-i))+Summation(j=1 to n)(Delta_i * GDP_(t-j))+E_2t

where, it is assumed that the disturbances st, and c2, are uncorrelated.
 Equation (I) postulates that current GDP is related to the past values of itself as 
 well as that of X (exports) and equation (2) postulates a similar behavior i.e. exports
(X) is related to the past values of itself as well as with the past values of GDP.

Direction of Causality:
Causality gan be both unidirectional or bidirectional.
Case I: Unidirectional causality from X to GDP is indicated if the estimated 
coefficients on the lagged X in equation ( I ) are statistically different from zero as
 a group (i.e. summation(Alpha_i not= O)and the set of estimated coefficients on the 
 lagged GDP in equation (2) is not statistically different from zero (i.e.(summation(delta_i = O))) 
Case Il: Conversely, unidirectional causality from GDP to X exists if the set of lagged
 X coefficients in equation (I) is not statistically different from zero (i.e.summation(Alpha_i = O)
 and the set of lagged coefficients of GDP in equation (2) is statistically different
 from zero (i.e.(summation(delta_i not= O))) 
 Case Ill: When the sets of X and GDP coefficients are statistically significantly 
 different from zero in both regression, it is called bilateral causality.
 And if not then the variable ue independent or have no causality.
More generally, since the future cannot predict the past (in a two variable case X and Y)
 if X Granger causes Y, then change in X should precede changes in Y.
 Therefore, in a regression of Y on other variables (including its own past values) 
 if we include lagged values of X and it significantly improves the prediction of Y.
 then say X Granger causes Y.
 
The Granger causality test involves the following steps taking GDP and Export as variables
for illustration. First. regress current GDP on all lagged GDP terms and do not include 
lagged values Of X variable. From this obtain the restricted residual of squares(RSS_R)
 Second, run the regression including the lagged values of X. From this obtain the
unrestricted residual sum of squares (RSS_UR).The null hypothesis is Ho: summation(alpha_i)= O.
To test this hypotiiesis we apply F-test.	

F= ((RSS_R-RSS_UR)/m)/(RSS_UR/(n-k)) 
Here, m is number of lagged X terms and k is number ofvparameters estimated in unrestricted regression.
If the computed Value Exceed the critical value of F at chosen level of significance,we reject the null
hypothesis. this is what we can say X causes GDP.The assumption of stationary for GDP and X should be satisfied.
The number of lagged term should be introduced in the causality test by Akaike information Criterion(AIC).


Stata VAR and Granger Causality

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
Conditional Heteroscedastic Models of Volatility:

The prime motivation behind the development of conditional volatility models is twofold.
First, the linear time series models were inappropriate in the sense that they provide 
poor forecast intervals, and it was contended that like conditional mean, variance
 (volatility) could as well evolve over time, and hence it was important to model 
 them both simultaneously. Secondly. an assumption Of Classical Linear Regression Model 
 (CLRM) is that the variance of the error term is constant. If the errors are 
 heteroscedastic but assumed to be an important implication would be that standard error
 estimates could be wrong. It is unlikely in the context of financial time series that 
 the variance is constant over time and it makes sense to consider a model that 
 does not assume that variance is constant. An attempt in this regard was made by 
 Engel (1982) who proposed the Auto Regressive Conditional Heteroscedastic (ARCH) model.
 Another important feature of many series of financial asset returns which provides a
 motivation for the ARCH class of models is known as "volatility clustering" or 
 "volatility pooling". This volatility clustering describes the tendency of large 
 changes in asset prices (of either sign) to follow large changes, and small changes 
 (of either sign) to follow small changes. Hence the current level of volatility tends 
 to be positively correlated with its level during the immediate preceding periods.

The ARCH Model
The first model that provides a systematic framework for volatility modelling is 
the ARCH model of Engle (1982). The model shows that it is possible to simultaneously 
model the mean and variance of a series. As a preliminary step to understand Engle's
methodology. let's estimate a stationary ARMA model
yt = a0 + a1yt-1 + €t,

where E[€t] = 0, var[€t] = sigma^2 for all t and forecast yt+1

A forecast of yt+1 conditional expectation of yt+1 period t, given the value of yt,
as follows

Et[yt+1] = a0 + a1y1   
       Since E[€t+1] = 0

If we use this conditional mean to forecast yt+1, the forecast error variance is
           Et[(yt+1 – a0 – a1yt)^2] = E[€^2t+1] = sigma^2
Instead, if unconditional forecasts are used, the unconditional forecast is always the 
long run mean of the {yt} sequence is equal to a0/(1-at). The unconditional forecast
error variance is

E{ [ yt+1 – a0/(1-a1)]^2} = E[(€t+1 + a1€1 + a1^2€t-1 + a^3€t-2 + …….. )^2] = sigma^2/(1-a1^2)

Since 1/(1-a1^2)>1, the unconditional forecast has a greater variance than the
 conditional forecast. Thus, conditional forecasts are preferable. 
 Similarly. if the variance of {€t} is not constant, we can estimate any tendency 
 for sustained movements in the variance using an ARMA model. Let's {€hat t}, will
 be the estimated residuals from the yt = a0 + a1yt-1 + €t , so that the conditional 
 variance of yt+1 will be

Var(yt+1|yt) = Et[(yt+1 – a0 – a1yt)^2] = Et[€t+1 ^2]

Thus far, we have set Et€^2 t+1 equal to sigma^2. Now suppose that the conditional 
variance is not constant. One simple strategy is to model the conditional variance 
as an AR (q) process using the square of the estimated residuals:

€hat^2 t = a0 + a1€hat^2 t-1 + a2€hat^2 t-2 + … + a4€hat^2 t-1 + v        (5.4)

Where v, is a white noise process. If the values of a1, a2, …..,  aq all equal to zero, 
the estimated variance is simply the constant a0. Otherwise the conditional variance of
 yt evolves according to the autoregressive process given by (5.4). As such we can 
 use (5.4) to forecast the conditional variance at t+1 as
E1 €hat^2 t+1 = a0 + a1 €hat^2 + a2 €hat^2 t-1 + … + a4 €hat^2 t+1-q

For this reason, an equation like (5.4) is called an autoregressive conditional 
heteroscedastic (ARCH) model.

Though the ARCH model offers some advantages described above, it has some weakness too:
•      The model assumes that positive and negative shocks have the same effect in 
volatility because it depends on the square of previous shocks. In practice it is well 
known that price of the financial asset responds differently to positive and negative 
shocks.

•      The ARCH model is rather restrictive. For instance, a1^2 of an ARCH (I) model
 must be in the interval [0, 1/3) if the is to have a finite fourth nuxncn.t. The 
 constraints become complicated for higher order ARCH model.

•      The ARCH model does not provide insights for understanding the source of 
variations of a financial time series. It only provides a mechanical way to describe 
the behavior of the conditional variance. It gives no indication what causes such 
behavior to occur.

•      ARCH models are likely to over predict the volatility because they respond slowly to large isolated shocks to the return series.

Building an ARCH Model:
A way to build an ARCH model consists of three steps. Step (I) builds an econometric
 model for example an ARMA model for the return series to remove linear dependence in 
 the data and use the residual series of the model to test for ARCH effects. 
 Step (2) specifies the ARCH order and performs estimation. 
 Step (3) involves checking the fitted ARCH model carefully and refining it if necessary.

The GARCH Model
GARCH models explain variance by two distributed lags. one on past squared residuals 
to capture high frequency effects or news about volatility from the previous period 
measured as the lag of the squared residual from mean equation, and second lagged 
values of variance itself to capture long term influences. In the GARCH (I, l) model, 
the variance expected at any given data is a combination of long run variance and the 
variance expected for the last period, adjusted to take into account the size of the 
last periods observed shock. In the GARCH model estimates for financial asset returns 
data, the sum of coefficients on the lagged squared error and Jagged conditional 
variance is very close to unity. This implies that shocks to the conditional variance
 will be highly persistence and the presence of quite long memory but being less 
 than unit, it is still mean reverting.

Bollerslev (1986) proposes a useful extension of ARCH model known as the Generalized
ARCH (i.e. GARCH) model. Bollerslev extended Engle's original work by developing a 
technique that allows the conditional to be an ARMA process. Let the error process
be such that €t = vt sqrt(ht)
Where sigma^2 vt = 1 and ht = a0 + a1€^2t-1
ht = a0 + ?q i=1 ai€^2 t-I + ?p i=1 ßt ht-I                 (5.5)
Since {vt} is a white noise process that is independent of past realization of €t-i,
 the conditional and unconditional means of €t are equal to zero. By taking expected 
 values of €t-i, it is easy to verify that E€t = Evt sqrt(ht) = 0. The important point
 is that the conditional variance of €t is given by Et-1€^2t = ht. Thus, the conditional
 variance of €t is given by ht in equation (5.5).

The generalized ARCH (p. q) of equation (5.5) is called as GARCH (p, q) that allows 
for both autoregressive and moving average components in the heteroskedastic variance. 
If we set p = 0 and q = 1, it is clear that the first order ARCH model is simply a 
GARCH (0,1) model. If all the ßi equal to zero, the GARCII (p. q) model is equivalent 
to an ARCH (q) model. The benefit of GARCH model should be clear as a higher order ARCH
 model may have a more parsimonious GARCH representation which is much easier to 
 identify and estimate. This is particularly true since all coefficients in (5.5)
 must be positive.

ARCH component a (alpha) reflects the influence of random deviations in previous 
period error terms on o which is a function of random error terms and realized 
variance of previous periods. Similarly, GARCH coefficient (beta) measures the part 
of the realized variances in the previous period that is carried over in to the current 
period. The sum Of ARCH coefficient and GARCH coefficient (a + ß) determines the short 
run dynamics of the resulting volatility time series. More specifically, a large ARCH 
error coefficient (a) means that volatility reacts intensely to market movements and a 
large GARCH error coefficient (ß) indicates that shocks to conditional variance take a 
long time to die out. So volatility is persistence. Hence current volatility can be
explained by past volatility that tends to persist overtime. If a is relatively high 
and ß is relatively low, then volatility tends to be spikier.


Stata Aarch and Garch
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
- Application of a least square to a single equation assumes that
	1. Explanatory variables are truely exognenous 
	2. There is one way causation between the dependent variable Y and eplanatory variable X.
- If this is not true, if X's at the same time are determined by Y, then the OLS 
assumption E(Xu not eq 0) is violated and leads to biased and inconsistent estimates.
- If there is a 2 way causation in a function it implies that the function 
cannot be treated as a single equation and belongs to a wider eqaution where it describes 
relationship between wider variable.
- If Y=f(X) and X=f(Y), we are not allowed to use a single equation model to
 describe relationship between X and Y.
- We must use multiple equations model which would include separate equations 
in which both Y and X would appear as endogenous variables although they might appear explanatory in
other equation model.
- A system describing the joint dependencies of variable is called a System 
of Simultaneous Equations.

SIMULTANEOUS EQUATION BAISED
- As we know in any economic phenomenon any equation will be a wider system of 
simultaneous equation.
- Here we illustrate an example that will explain simultaenous relationships and violation 
of assumption of OLS which creates what is known as simultaneous equation bais.
- Example:
Suppose we want to estimate demand for food which depends upon, 
P = Price, P0 = Other Prices and Y = Income.
It can be mentioned as:
Q = b0+b1P+b2P0+b3Y+U    ----(1)
- If least squares is applied to the equation we will obtain baised estimates of b0 
and b1 because P0 and U are not independent.
- Demand for any commodity is a function of it's price but price of market is 
influenced by quantity demanded by the commodity.
- We cannot conclude only on the basis of the above equation there should be at 
least one model giving relation between P and Q.
P = C0+C1Q+C2W+V        -----(2)
Here, W is weather's index.
Substituting Q in 2,
P = C0+C1(b0+b1P+b2P0+b3Y+U)+C2W+V
We can see from the equation that P is dependent on U hence we have violation of OLS 
Assumption.E(Xu not eq 0)
P is not exogenous variable in demand function.
- The bias arising from application classical least square to an equation belonging 
to a system of simultaneous relations are called simultaneous equations bais.
- This originates from violation of OLS assumption, i.e. dependence of P and Q and E
(Xu not eq 0).
- This creates several problems like:
 1. Identification of parameters of individual relationship.
 2. Problem of estimation, OLS Yields baised and inconsistent estimates.
___________________________________________________________________________________________________________________________________________________________________
IDENTIFICATION
___________________________________________________________________________________________________________________________________________________________________
- Identification is a problem of model formulation rather then estimation.
- A model is said to be identified if it is in a unique statistical form, enabling 
unique estimates of it's parameters to be subsequently made from sample data.
-If a model is not identified then estimates of parameters of relationships between
 variables measured in samples may relate to the model in question or to another
model or a mixture of models.
- For identification of entire model it is necessary for a model to be complete and 
for each equation in it to be identified.
- To understand identification problem let us understand with an example:
EXAMPLE:
Consider theory of market equillibrium, let's assume the market mechanism for a
 certain commodity.
D = b0+b1P+U
S = a0+a1P+V
D = S
D = Quantity Demanded
S = Quantity Supplied
P = Price
The model is complete in that there are three equations and 3 endogenous variables S,D,P).
- By identfication problem we can mean whether numerical estimates of parameters of structural equation can be obtained from estimates reduced to coefficients.
If this can be done we can say that particular equation can be identified.
- If this cannot be done, then particular equation is unidentified or underidentified.
- An identified equation can be exactly identified or over identified.
For an equation to be exactly identified when it's unique numerical values of 
structural parameters can be obtained.
For an equation to be over identified if more than one numerical values can be 
obtained for some parameters of structural equations.
- In order to ease the task of identification, rank and order condition is used.
To under Rank and Order conditions, following equations are used:
M = No. of endogenous variables in a model.
m = No. of endogenous variables in a equation.
K = No. of predetermined variables in a model.
k = No. of predetermined variables in an equation.
___________________________________________________________________________________________________________________________________________________________________
ORDER CONDITION
___________________________________________________________________________________________________________________________________________________________________
- A necessary condition for identification is known as order condition.
- It can be stated in two different but equivalent ways.
A) A simultaneous equation model for an equation to be identified it must exclude at 
least M-1 variables in the model.
   A simultaneous equation model for an equation to be overidentified it must exclude 
   more than M-1 variables in the model.
B) A simultaneous equation model, for an equation to be identified the number of
 pretermined variables excluded from equation must not be less than number of 
endogenous variables included in that equation less than that of 1.
K - k >= m-1
K - k = m-1 ; INDENTIFIED
K - k > m-1 ; OVER IDENTIFIED
_________________________________________________________________________________________________________________________________________________________________
RANK CONDITION
_________________________________________________________________________________________________________________________________________________________________
- Rank condition is a necessary and a sufficient condition for an equation to be identified.
- A model containing 
M equations and m endogenous variables is identified if and only if at least one 
non-zero determinant of order (m-1)(m-1) can be constructed from coefficients of 
variables excluded from that particular equation but included in other equation.
- Principals of identifiability:
A) K-k > m-1 and rank of matrix is equal to m-1 then equation is overidentified.
B) K-k = m-1 and rank of matrix is equal to m-1 then equation is identified.
C) K-k >= m-1 and rank of matrix is <m-1 then equation is underidentified.
D) K-k < m-1 and rank of matrix is bound to be <m-1 then equation is Unidentified.

_________________________________________________________________________________________
ILS ( Indirect Least Square)
_________________________________________________________________________________________
- For just or exactly identified structural equation, the method of obtaining estimates of strutural coefficients from OLS estimates of 
reduced form coefficients is known as method of indirect least squares.
- The estimates thus obtained is known as the indirect least square estimates for ILS.
- ILS invlolves the following steps:
STEP 1) Obtain the reduced form equations. These reduced form equations are obtained from strutural equations in such a manner that the dependent variable
in each equation is the only endogenous variable and is a function of predetermined variables and stochastic error terms.
STEP 2) Then we apply OLS to the reduced form equation individually. This operation is permissible since the explanatory variables in these equation are predetermined 
and hence uncorrelated with the stochastic disturbances. These estimates thus obtained are considered.
STEP 3) We obtain estimates of the original structural coefficients from estimated reduced form coefficeints. If an equation is exactly identified there is no 1 to 1 
correspondence between structural and reduced form coefficients that is, one can derive unqiue estimates of the former from the latter.
- ILLUSTRATION
Consider the demand and supply model
Demand function: Qt = a0+a1Pt+a2Xt+U1t (a = alpha)
Supply function: Qt = B0+B1Pt+U2t (B = beta)
Here Q = Quantity, P = Price, X = Income or expenditure.
Assume that X is endogenous. The supply function is exactly identified and the demand function is unidentified. The reduced form equation corresponding to this preceeding 
structural equations are
Pt = Pi0+Pi1Xt+Wt
Qt = Pi2+P3Xt+vt
where, Pi's are reduced from coefficients and are combinations of structural combinations of structural coefficients W and v are linear combinations of structural
disturbances  U1 and U2. Now apply OLS to the reduced form equations:
(Pi1)hat = S(P1xt)/S(xt)sq.		(Pi0)hat = P(bar)-(Pi1)hat.X(bar)
(Pi3)hat = S(Q1xt)/S(xt)sq.		(Pi2)hat = Q(bar)-(Pi3)hat.X(bar)
It's parameter can be estimated uniquely from the reduced form coefficients as follows:
B(0) = (Pi2) - B1(Pi0)		B1 = (Pi3)/(Pi1)
Hence the estimates of the parameters can be obtained from estimates of the reduced form coefficient as:
B(0)hat = (Pi2)hat - (B1)hat.(Pi0)hat		B(1)hat = Pi(3)hat/Pi(t)hat
which are ILS estimators.
__________________________________________________________________________________________________________________________________________________________________
2 SLS (Stage Least Squares)
__________________________________________________________________________________________________________________________________________________________________
- The 2 stage least square had been developed independently by Henri Theil and Robert Basmann. As the name indicates, the method involves two successive application 
of OLS.
- Consider the following model
Income Function: Y1t = B(10)+B(11)Y2t+r11X1t+r12X2t+U2t
Money Function: Y2t = B(20)+B(2t)Yt
Here, Y1 = Income, Y2 = Stock of money, X1 = Investment Expenditure, X2 = Government Expenditure on goods.
In order to solve this simultaneous equation problem the process to be followed in 2SLS is as follows:
STAGE 1: To get rid of likely correlation between Y1 and U2 we regress first Y1 on all the predetermined variables in the whole system, not just that equation,
In our case, this means regressing Y1 on X1 and X2 as follows:
Y1t = Pi(0)hat+Pi(1)hat.X1t+Pi(2)hat.X2t+Uthat
Here, Uthat = OLS Residuals.
Hence,
Y1that = Pi(0)hat+Pi(1)hat.X1t+Pi(2)hat.X2t
Here, Y1that  is an estimate of the mean of Y, conditional upon the fixed X's.
Hence, Y1t = Y1that+Uthat
which shows that the stochastic Y1 consists of two parts; Y1that which is a linear combination of non stochastic X's and a random component Uthat.
Following OLS theory, Y1that and Uthat are uncorrelated.
STAGE 2: The over identified money supply equation is now written as 
Y2t = B20+B21(Y1that+Uthat)+U2t
    = B20+B21Y1that+(U2t+B21Uthat)
	= B20+B21Y1that+Ut*
where Ut* = U2t+B21Uthat.
Now we can apply OLS to estimate the parameters.
Obtaining the estimates Y1that abd replacing Y1t in the original equation by estimated Y1that, and then applying OLS to the equation thus transformed. 
The estimators thus obtained are consistent, i.e they converge to their true values as the sample size increase indefinitely.
FEATURES of 2SLS:
1. It can be applied to an individual equation in the system without directly taking into account any other equations in the system. Hence, for solving
econometrics model 2SLS offers economical model.
2. 2SLS provides only one estimate per parameter.
3. It is easy to apply because all one needs to know is the total number of endogenous variables in the system without knowing any variables in the system.
4. Although specially designed to handle over identified equation, the method can also be applied to exactly identifeid equations.
5. In 2SLS we state the standard erros of the estimated coefficients because the structural coefficients are directly estimated from 2SLS.
_________________________________________________________________________________________________________________________________________________________________
3 SLS ( Three Stage Least Squares)
_________________________________________________________________________________________________________________________________________________________________
- 3 SLS is a system applied to all equations of the model and gives estimates of all the parameters simultaneously. This method was developed by Theit and Zellmax as 
a logical extension of Theil's 2SLS. It involves the application of the method of least squares in the successive stages.
STAGE 1: In the first stage we estimate the reduced form of all the equations of the system.
y1 = f(X1,X2..........,Xk)
y2 = f(X1,X2..........,Xk)
y3 = f(X1,X2..........,Xk)
.
.
.
ya = f(X1,X2..........,Xk)
We thus obtain estimated values of the endogenous variable Y1hat,Y2hat,.....Yahat.
STAGE 2: We substitue the above calculated values of the endogenous variables in the right hand side of the structural equations and apply least sqaures to the 
transformed equations. We thus obtain the 2SLS of parameters which we use for the estimation of the error terms of the various equations. We find set of G errors
e1,e2,e3......eG
each corresponding to error terms G, of the respective structural equation. Ofcourse for each equation we have n values of error terms.
The Variance and Covariance of estimated error terms may easily be computed by usual formula of covariance.
Sigma(e12)hat = S(e1ie2i)/n
Sigma(e13)hat = S(e1ie3i)/n and so on..
The complete set of variance and co variance of error terms are as follows:
Matrix ((Sigmahat(e11)sq..........(Sigmahat(eiG))
	   ((Sigmahat(e21)sq..........(Sigmahat(e2G))
	   ((.									   ))
	   ((.									   ))
	   ((Sigmahat(eG1)sq..........(Sigmahat(eGG))
	   
Matrix ((Sigma(ei1)sq/n)......... (Sigma(eiG)sq/n))
	   ((Sigma(ei2)sq/n)......... (Sigma(eiG)sq/n))
	   ((.										 ))
	   ((.										 ))
	   ((Sigma(eiG)sq/n)......... (Sigma(e G)sq/n))
STAGE: 3 We use the above variance and covariance of the error terms in order to obtain the transformation of the error of original variables for the application
of GLS

Properties of 3SLS estimates
1. 3SLS estimates are biased but consistent.
2. They are more efficient than 2SLS , since we can use more information than 2SLS.

Stata SME
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
VECM

The Johansen Tests for Cointegration
Time series can be cointegrated in various ways, with details such as trends assuming 
some importance because asymptotic distributions depend on the presence or lack of such
terms. I will focus on the simple case of one unit root in each of the variables with no
constant terms or other deterministic terms. These notes are a quick summary of some 
results without derivations.

Cointegration and Eigenvalues
The Johansen test can be seen as a multivariate generalization of the augmented Dickey- Fuller 
test. The generalization is the examination of linear combinations of variables for unit
roots. The Johansen test and estimation strategy – maximum likelihood – makes it possible
to estimate all cointegrating vectors when there are more than two variables.1 If there are
three variables each with unit roots, there are at most two cointegrating vectors. 
More generally, if there are n variables which all have unit roots, there are at most 
n - 1 cointegrating vectors. The Johansen test provides estimates of all cointegrating 
vectors. Just as for the Dickey-Fuller test, the existence of unit roots implies that 
standard asymptotic distributions do not apply.
Slight digression for an assertion: If there are n variables and there are n 
cointegrating vectors, then the variables do not have unit roots. Why? Because 
the cointegrating vectors.Results generally go through for quasi-maximum likelihood estimation.
We can be written as scalar multiples of each of the variables alone, which implies that the variables do not have unit roots.
The vector autoregression (VAR) in levels with the constant suppressed is


xt = Sigma(i=1 to k) Aixt-i+ut

For k > 1, this VAR in the levels always can be written
Delta(xt) = Pi(xt-1)+Sigma(i=1 to k-1) Pi(i(Delta xt-i))+ut
For the simpler case k = 1, it is simply Deltaxt = Pi xt-1 + ut
The matrix Pi can be written in terms of the vector or matrix of adjustment parameters
alpha and the vector or matrix of cointegrating vectors ß as

Pi = aß'	(3)

For example, if the number of variables, n, is two and there is one cointegrating vector,
then the vector ß is 2 x 1 and the vector a is 2 x 1. The two coefficients in the 
cointegrating vector ßj multiply the variables to deliver the linear combination of 
variables that does not have a unit root, that is ßjxt-1. The two coefficients in a 
are the two adjustment coefficients, one for each of the two equations, which multiply 
the cointegrating relationship ßjxt-1 to deliver the response of the variables in the 
two equations to deviations of the cointegrating relationship from zero.
If the matrix Pi equals a matrix of zeroes, that is, Pi = 0 then the variables are
not cointegrated and the relationship reduces to the vector autoregression in the first differences
Delta(xt) = Sigma( i =1 to k-1)Pi(iDeltaxt-i)+ut
 
How can one test whether Pi = 0? One way is to test whether the rank of Pi is zero, that is whether
rank (Pi) = 0	(5)

If the variables are cointegrated, then rank (Pi) not eq  0  and  in  fact  rank (Pi)  =  the number
of cointegrating vectors. The number of cointegrating vectors is less than or equal to
the number of variables n and strictly less than n if the variables have unit roots.
If the rank of matrix is less than n, then its determinant is zero. Eigenvalues are useful for
solving this problem because the determinant of a square matrix equals the product of the eigenvalues. 
If the rank of the matrix is less than the number of rows and columns in the matrix, then one or more eigenvalues is zero and the determinant is zero.
What are eigenvalues? The set of eigenvalues for the n x n matrix A are given by the n
solutions to the polynomial equation


det (A - Lambda In) = 0	(6)

where In is an nth order identity matrix and det(.) denotes the determinant of the 
matrix A - Lamda In. Direct computation shows that equation (6) is an nth order 
polynomial, which has n not necessarily distinct roots.
The Johansen tests are based on eigenvalues of transformations of the data and 
represent linear combinations of the data that have maximum correlation 
(canonical correlations). To repeat, the eigenvalues used in Johansen’s test 
are not eigenvalues of the matrix ? directly, although the eigenvalues in the 
test also can be used to determine the rank of ? and have tractable distributions. 
The eigenvalues are guaranteed to be non-negative and real. It would take us far 
afield to go into this and would serve little purpose in the end 
(other than torturing most of the people in class, which does not seems particularly 
desirable).2
Suppose that eigenvalues for the Johansen test have been computed.

Order the n eigenvalues by size so Lamda 1 = Lamda 2 = ... = Lamda n and recall that
 Lamda i >= 0 for all i. If Lamda 1 = 0, then the rank of Pi is zero and there are no 
 cointegrating vectors. If Lamda 1 not eq 0, then the rank of Pi is greater than or
 equal to one and there is at least one cointegrating vector. If Lamda 1 = 0, stop 
 with a conclusion of no cointegrating vectors.3
If Lamda n-1 not eq 0, then continue testing by moving on to Lamda 2 <= Lamda 1. 
If Lamda 2 not eq 0, then the rank of Pi is one and there is one cointegrating vector. 
If Lamda 2 not eq 0, then the rank of Pi is at least two and there are two or more cointegrating vectors.
And so on ....
 
If Lamda n-1 not eq 0, then test whether Lamda n = 0. If Lamda n = 0, then there are n - 1 cointegrating
 vectors. If Lamda n not eq 0, the variables do not have unit roots.
In an application with two variables, the maximum number of cointegrating vectors is two. 
Two cointegrating vectors would indicate that the variables do not have unit roots. 
The eigenvalues are Lamda 1 and Lamda 2 with Lamda 1 > Lamda2. If Lamda 1 not eq 0,
then there are no cointegrating vectors. If Lamda 1 not eq 0 and Lamda 2 = 0, there 
is one cointegrating vector. If Lamda1 not eq 0 and Lamda 2 not eq variables do not have unit roots.

The  Johansen Tests
 
The Johansen tests are called the maximum eigenvalue test and the trace test.
Let r be the rank of Pi. As the discussion above indicated, this is the same as the 
number of cointegrating vectors. The Johansen tests are likelihood-ratio tests.
There are two tests: 1. the maximum eigenvalue test, and 2. the trace test.
For both test statistics, the initial Johansen test is a test of the null hypothesis 
of no coin- tegration against the alternative of cointegration. The tests differ in
 terms of the alternative hypothesis If L1 = 0 and L1 >= L2> = ... >= Ln, then L1 = 0 = L2 = ... = Ln
 
Maximum Eigenvalue Test

The maximum eigenvalue test examines whether the largest eigenvalue is zero relative to
the alternative that the next largest eigenvalue is zero. The first test is a test whether
the rank of the matrix Pi is zero. The null hypothesis is that rank (Pi) = 0 and 
the alternative hypothesis is that rank (Pi) = 1. For further tests, the null
hypothesis is that rank (Pi) = 1, 2... and the alternative hypothesis is that rank (Pi) = 2, 3, ....
In more detail, the first test is the test of rank (Pi) = 0 and the alternative hypothesis is that rank (Pi) = 1.
This is a test using the largest eigenvalue. If the rank of the matrix  is zero, the largest eigenvalue is zero,
there is no cointegration and tests are done. If the largest eigenvalue Lamda 1 is nonzero, the rank of the matrix is at least one
and there might be more cointegrating vectors. Now test whether the second largest eigenvalue Lamda 2 is zero. If this eigenvalue is zero,
the tests are done and there is exactly one cointegrating vector. If the second largest eigenvalue Lamda 2 not eq 0 and there are more than two variables, 
there might be more cointegrating vectors. Now test whether the third largest eigenvalue Lamda 3 is zero. And so on until the null hypothesis of an eigenvalue equal to zero cannot be rejected.
The test of the maximum (remaining) eigenvalue is a likelihood ratio test. 
The test statistic is
LR(r0, r0 + 1) = -T ln (1 - Lamda r0+1)	(7)
where LR (r0, r0 + 1) is the likelihood ratio test statistic for testing whether rank 
(Pi) = r0 versus the alternative hypothesis that rank (Pi) = r0 + 1. 
For example, the hypothesis that rank (Pi) = 0 versus the alternative that rank 
(Pi) = 1 is tested by the likelihood ratio test statistic LR(0, 1) = -T ln (1 - Lamda 1).
This likelihood ratio statistic does not have the usual asymptotic chi 2 distribution.
This is similar to the situation for the Dickey-Fuller test: the unit roots in the data generate nonstandard asymptotic distributions.
 
Trace Test

The trace test is a test whether the rank of the matrix ? is r0. The null hypothesis
is  that rank (?) =  r0. The alternative hypothesis is that r0  < rank (?)  = n,  
where n is  the maximum number of possible cointegrating vectors. For the succeeding 
test if this null hypothesis is rejected, the next null hypothesis is that 
rank (?) = r0 + 1 and the alternative hypothesis is that r0 + 1 < rank (?) = n.
Testing proceeds as for the maximum eigenvalue test.5 
The likelihood ratio test statistic is
 
LR(r0, n) = -T Sigma(i = r0+1 to n) ln(1-Lamdai)

where LR(r0, n) is the likelihood ratio statistic for testing whether rank (Pi) = r 
versus the alternative hypothesis that rank (Pi) <= n.  For  example,  the hypothesis
that rank (Pi) = 0 versus  the  alternative  that  rank (?)   n is  tested  by  
the  likelihood  ratio  test  statistic.

LR(0, n) = -T Sigma ( i =1 to n) ln (1 - Lamda i).

Why is the trace test called the “trace test”? It is called the trace test because the test
statistic’s asymptotic distribution is the trace of a matrix based on functions of 
Brownian motion or standard Wiener processes (Johansen Econometrica 1995, p. 1555).
That doesn’t help much; most texts don’t bother to explain the name at all because much
more detail is necessary to say anything more informative.6 Maybe a negative will be 
informative: The test is not based on the trace of ?.
5A helpful thought to avoid some confusion is to keep in mind that the null hypothesis 
starts off from “not cointegrated”.
6It is not hard to back out the actual matrix of eigenvalues which has the test 
statistic in equation (8) as the logarithm of its trace. It’s also not illuminating.


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

ARDL models contains the lagged values of the dependent variables(Ys) and the current &
 lagged values of regressors(Xs) as explanatory variables.
Unlike VAR model, that strictly assumes that all the variables are endogenous,
 ARDL uses a combination of both endogenous & exogeneous variables.
Stationarity is not a necessary condition. However, all the variables shouldn’t be stationary at 2nd difference.
If the variables are cointegrated, then we can go for both short-0run ARDL models or long-run VECM models.
If the variables are not cointegrated, then we can only use short-run ARDL models along with VAR.
ARDL models are generally more efficient in case of small sample, whereas it may not be the case for VAR.
ARDL model also provides unbiased long-term estimates of the variables.
 

Model Specification:

            Yt = f(Yt-1, Xt, Xt-1, Xt-2…..)

A generalized ARDL (p,q) model is specified as:
Yt = ao + ?i=1p ai Yt-I + ?qi=1 ßi Xt-I + €t
Yt = A vector
Xi = Explanatory variables (might be exogeneous) and should be either I(0) or I(1)
Yi = Explanatory variables, mostly lags of dependent variable and hence could be endogenous by nature.
ai & ßi  = coefficients
p & q = are optimum lag orders or Auto regressive as well as for X explanatory variables
€t = vector of error term. It is assumed to be white noise, serially uncorrelated.
Note that in ARDL models, the dependent variable (Yt) is a function of its own lags 
as well as current and lagged values of other exogenous variables of the model. 
Here the lag orders of p & q need not necessarily be the same. Unlike VAR, 
we can use different lags for p & q.
To perform the bounds test for cointegration, the conditional ARDL 
(p, q1, q2) model with 3 variables is specified as:

 

Hypothesis of bounds test:

Ho: b1i = b2i = b3i = 0…………..where……….. i=1,2,3
       B1i = b2i = …… = 0………….where………….i = 1,2,…
H1: b1i != b2i != b3i != 0
That is the coefficients of the long-run equation is all zero.
If the hypothesis of long-run coefficients i.e. “ß” couldn’t be rejected, then we can establish only 
the short-run relationships.
If we could reject the Ho; then we can move to VECM models.

 Model Specification:

deltaGDPt = a01 + b11 deltaGDPt-i + b21 deltaExt-i + b31 deltaM3t-i + ?p i=1 a1i deltaGDPt-i + ?q i=1 a2i deltaExt-i + ?q i=1 a3ideltaM3t-i + €1t
deltaEXt = a02 + b12 deltaGDPt-i + b22 deltaExt-i + b32 deltaM3t-i + ?p i=1 a1i deltaEXt-i + ?q i=1 a2i deltaExt-i + ?q i=1 a3ideltaM3t-i + €2t
deltaM3t = a03 + b13 deltaGDPt-i + b23 deltaExt-i + b33 deltaM3t-i + ?p i=1 a1i deltaM3t-i + ?q i=1 a2i deltaGDPt-i + ?q i=1 a3ideltaEXt-i + €3t
If there is no cointegration, the ARDL (p,q1,q2) model of the above could be specified as:
deltaGDPt = a01 +?p i=1 a1i deltaGDPt-i + ?q i=1 a2i deltaExt-i + ?q i=1 a3ideltaM3t-i + €1t
Note that for cointegration, the series must be I(1). 
But, when, there is no cointegration then we will go for VAR or ARDL models that
 measures the short term relationships and hence, the series must be I(0). 
 So in the above equation, we have taken the variables in 1st difference (i.e.   delta).
But if the series are cointegrated then the error correction model (ECM) 
specification of the above models could be written as

deltaGDPt = a01 +?p i=1 a1i deltaGDPt-i + ?q i=1 a2i deltaExt-i + ?q i=1 a3ideltaM3t-i + gammaECTt-i + €t
Here, gammaECT represent the long-run relationship whereas rest of the portion of RHS represents short-run relationship among the variables. And gamma, the coefficient of ECT should be -ve & significant. A +ve ECT shows that the impact is explosive and there is no convergence.

Note:
A1i, a2i & a3i = are short-term parameters that measures short-run dynamic coefficients
Bi that is (b11, b21, b31), (b12, b22, b23) and (b13, b23, b33) are long-term parameters. Hence, in 1st equation, ECT = (deltaGDPt-i – thetaXt)
Theta = (?q i=0 bi)/a implies the long-run parameters.
The bounds test indicates whether to specify a VECM, ECM or ARDL model.
Specify the VECM if there is cointegration in any of the 3 equations
While estimating ECM and VECM. We naturally obtain the short-run dynamic parameters i.e. (ai)
The short-run causal effects can be analyzed through the significant “ai” parameters.
A significant ECT i.e (-x) also indicates long-run relationship between variables with one direction.



_________________________________________________________________________________________
ARIMA
_________________________________________________________________________________________

What is “Unit Root”?
A unit root (also called a unit root process or a difference stationary process)
is a stochastic trend in a time series, sometimes called a “random walk with 
drift”; If a time series has a unit root, it shows a systematic pattern that 
is unpredictable
What is a Unit Root Test?
Unit root tests are tests for stationarity in a time series.
A time series has stationarity if a shift in time doesn’t cause a change in 
the shape of the distribution; unit roots are one cause for non-stationarity.
These tests are known for having low statistical power. Many tests exist, 
in part, because none stand out as having the most power. Tests include:
•	Augmented Dickey-Fuller (ADF) test 
•	 Elliott–Rothenberg–Stock Test
•	The Schmidt–Phillips Test 
•	 Phillips–Perron (PP) Test 
•	 Zivot-Andrews test 

Testing stationarity using correlogram
Ho : Variable is stationary or there is no trend
H1 : Variable is not a stationary or there is trend
If probability of a stat of AC and PAC is less than 0.05 then reject Ho.
In case of correlogram, we wish not to reject Ho and input probability values 
to be greater than 0.05
ACF: Auto-Correlation Function (ACF) represents the correlation between 
the observation at the current time 't' and it's lag 't -i'. For e.g., 
if we assume that up to day 'i' stock prices correlated with its past values 
then we can calculate its ACF to know how effectively todays stock price is 
correlated with its past.
PACF: Partial Auto-Correlation function (PACF) represents the correlation 
between observation at two time period given that we consider both the 
observations are correlated to the observations at other time period.
For example: current stock price of HDFC can be correlated with HDFCt-1 
and HDFCt-2 and can also be correlated with HDFCt-1 only. Then PACF of HDFCt
with HDFCt-1 measures the correlation between t & t-i after taking out the 
influence of t-2 on t. Hence PACF measures the real correlation between two 
time periods after taking out the influence of other time periods. 
Therefore, in practice, we use PACF to evaluate the AR models, because PACF 
captures the true correlation among the selected AR(P) orders taking out the
influence of other higher orders on current (t).
Similarly, we use ACF to evaluate the MA(q) models. The PACF measures the 
correlation between time-series observations after controlling for the 
correlation at intermediate lags. Hence. PACF measures the true marginal 
effects of significant lags.
Rules of using ACF & PACF
If we have a time-series data set, then the 1st step is to see whether there are
any obvious trends/time trends. If there is any trend, there the data set 
violates the basic assumption of stationarity. The next step is to de trend or 
log-different to make it stationary.
After do-trending or making the stationary we must decide between AR and mA, 
which model we should of use. As we have said, we use PACF to decide the order 
of AR model a Significant PACF value have to be chosen for example, if the 
PACF of t-1 and t-2 stock price is Significant, and rest of the t-i lays are 
insignificant, then we should choose a AR (2) i.e.2nd order Auto-regression model.
Then use ACF to determine the terms of MA. Like previous, we will find significant
order Of ACF to identify optimum order of M.A(q).
Similarly, looking at PACF and ACF together, we will find the order Of ARMA, (P, Q).
Note: The real dotted lines present the significant thresholds. The vertical 
(black) lines represents ACF and PACF values at each time lag. Only the vertical
 lines that cross the significant threshold lines /confidence interval times are
 called significant.
In the above graph. PACF recommends a 3rd or AR model (AR(3)) and t-1, t-2 & t-3 
lags are found significant. Similarly, in ACF graph, 1st order MA is recommended 
of as t-1 is the only significant ACF
Looking at ACF and PACF, either we can recommend AR (3) or MA (l) or ARMA (3,0,1)model
Continuation of PACF
The PACF measures the correlation between, time-series observations offer 
controlling for the correlations at intermediate lags. Hence PACF measures the 
true marginal effects of significant
Summarizing the pattern of ACF & PACF in ARMA modelling
ACF Pattern	PACF PAttern
            AR(p)-Exponential decay (or) Damped sine wave pattern	Significant spikes through 1st lag
MA (q) — Significant spikes through 1st lag	Exponential decay (or) Damped sine wave pattern
ARMA (1,1) Exponential Decay from lag 1	Exponential decay from lag 1
ARMA(p,q)-exponential Decay	Exponential Decay

Steps to model AR, MA, ARMA:
Step l: Identification process. That is analyze the time series plot to visualize stationarity, trend, Seasonality etc.
Step-2: Undertake testing unit root through DF, ADF, PP, KPSS etc
Step-3: Analyze both at ACF & PACF for the data both at level 1st and the data difference
Step 4: Decide order of AR and MA and finalize the possible of ARMA (p, q)
Step-5: Estimate the models.
The figure (l ) shows the data is not stationary, as  we reject the Ho: variable 
to stationary because the probability of ACF PACF is less than 0.05, and the 
autocorrelation plot is exceeding the dotted lines. It implies the error terms 
indicated by ACF is auto-correct
The pattern of ACF and PACF is matching the point 1 of summary table
The figure (2) shows the ACF and PACF Of the data in 1st difference. 
We can see the ACF and PACF lines are within the dotted confidence interval and the prob. values of the lag are also greater than 0.05. Hence, we cannot reject the null hypothesis
Note, that if the pattern of ACF & PACF is same, then we will be having ARMA 
models.
In ARIMA- Box - Jenken suggest building parsimonious models. Parsimonious 
model are small and less parameters. Hence, it gives better forecast than 
over-parameterize model. Based on Boy- Joskine parsimonious modelling, 
choose the ARMA model that is small with less parameters but gives better 
estimates.
Best suitable ARMA:
Estimate all the possible combinations of ARIMA. i.e AR (l), AR (2), 
ARMA (l, l), (2,1)… and so on. It's always better to select the (p, q) 
from ACF & PACF plots. That is select the order of lag, where ACF & PACF 
crosses the Cl line. Then compare the estimated statistics Of all the model 
to choose the best one.  
	
Stata Arima
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
