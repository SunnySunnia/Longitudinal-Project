##Goal:  
Given labeled data (i.e. TMI vs non-TMI), analyze the diffence in the data behaviors, model the trajectories, and assess risk among the groups.  
* What features and how many features to model? ---->`feature selection`  
* use case: given a value(or set of values) at a time point (9-month-old), assess the risk of having the disease.  
* so the model has to be sensitive to **time** of course, secondly will be **segmental change over time** from the past of the same subject (i.e. a certain elevation in the features over 3 months will 'qualifies' the subject to a higher risk?) 
* look for influetial **features** that help assessing risk (i.e. a boy is more likely to have autism than a girl)  



##Analysis/Modeling approaches:  

###Linear Mixed Effects Regression (LMER)  
-------------------------  
**Mechanism:**  
* mean change over time  
* Components: 

| Component      |                          Description     | Level of Effect  | Symbol   |    
|--------------- |:----------------------------------------:|:----------------:| --------:|    
| Fixed Effects  | Regression coefficients                  | Group            | \beta    |       
| Random Effects | Individual deviations from fixed effects | Individual       | b        |       
| Random Error   | Regression error term                    | Individual       | \epsilon |     

* 

**Algorithm:**  
* Example data: MPLS  

subid | read.5 | read.6 | read.7 | read.8 | risk | gen | eth | ell | sped | att  
1 | 172 | 185 | 179 | 194 | HHM | F | Afr | 0 | N | 0.94  
7 | 199 | 208 | 213 | 218 | POV | M | Afr | 0 | N | 0.97  

* Date must be in long-format: `reshape()`  
    Long, page 76-77  

  ```r
  MPLS = reshape(data = MPLS, varying = 2:5, v.names = "read", 
                 timevar = "grade", times = 5:8, idvar = "subid" , direction = "long" )
  ```
* MPLS.L  



* 


**References:**  
```
  Long, J. (2012). Longitudinal data analysis for the behavioral sciences using R. Thousand Oaks, Calif.: SAGE.
```  


###Growth Curve Modeling (GCM)  
-------------------  
**Mechanism:**  
* fitting an unconditional model that estimates the shape of development over time using `mean` and `covariance structure`.  
* pro: if all individuals in the population follow a similar functional form of development.  
* con: if one trajectory shape is not able to "fit all".  

**Algorithm:**  
* 


###Growth Mixture Modeling (GMM)  
-------------------------  
**Mechanism:**  
* finite mixture models  
* approximating unknown distributions  
* pro: if the general population is thought to be composed of distinct sub-populations, each following a conventional GCM.  
* con: if you dont know how many sub-populations are there.  

**Algorithm:**  
*  

###Group-Based Trajectory Modeling (GBTM)  
--------------------  
**Mechanism:**  
* application of finite mixture  
* assumes the population is composed of a mixture of distinct groups defined by their `developmental trajectory`.  
* pro: takes no stand on the population distribution of trajectories and instead uses the trajectory groups as a statistical device for approximating the unknown distribution of trajectories across population members.  
* the model's estimated parameters are from the product of maximum likelihood estimation.  
* the shapes of the trajectories are described by a polynomial function of age or time.  
*   

**Algorithm:**  
* the unconditional probability of observing individual's longitudinal sequence of behavioral measurements is the sum of the probability of the bahaviors, given the individual belongs to specific group, weighted by the probability of belonging to the group.  
* `Y_i = {y_i1, y_i2,..., y_iT}` : a longitudinal sequence of measurements on individual `i` over `T` periods.  
* `P(Y_i)` : probability of `Y_i`: unconditional probability of observing individual `i`'s longitudinal sequence of behavioral measurements `Y_i`     
        - count data -- Poisson distribution  
        - censored data -- censoredd normal distribution  
        - binary data -- binary logit distribution  
        - `P(Y_i) = sum across all j {pi_j * P^j(Y_i)}`  

* `P^j(Y_i)` : probability of `Y_i` given membership in group `j`.  
        - `P^j(Y_i) = product over T { p^j(y_it) }`  
* `pi_j` : probability of a randomly chosen population member belonging to group `j`.  
        - `pi_j = e^(theta_j) / sum all j {e^(theta_j)}`  
* `p^j(y_it)` : probability distribution function of `y_it` given membership in group `j`.  
        - **group-specific specification**.  
        - for each individual within a given trajectory group `j`, the distribution of `y_it` for period `t` is independent of realized level of the outcome in prior periods `y_it-1`, `y_it-2`, ...  
        - example: the `tobit` model in econometrics  
        - Constructed from the following assumptions:  
            count data -- Poisson distribution  
            censored data -- censoredd normal distribution  
            binary data -- binary logit distribution  
        - 2.4.2 (Page 42)  
* `y_it` : measuring individual `i`'s potentiaal for engaging in a behavior at age/time `t`.  
        - example : `y_it = beta_j0 + beta_j1 *Age_it + beta_j2 * (Age_it)^2 + beta_j3 * (Age_it)^3 + epsilon_it`  
        - `beta_jk` : the `k`th coefficient/parameter that determines the shape of the individual `i`'s behavior given membership in group `j`.  
* goal: estimate a set of parameters to maximize `P(Y_i)`  
* the likelihood for the entire sample of N individuals:  
        `L = product over N { P(Y_i) }`  
* key:  
        - choice of an appropriate form of `p^j(y_it)` for characterizingthe distributional properties of censored/continuous data.  
        - specification of a link function the connects the course of the behavior or outcome with age or time.  
* Steps:  
        - model the behaviors with functions, `y_it`, with unknown coefficients for varying time `t` given membership in group `j`  
        - incorporate the emperical behavior function into a probability distribution function, `p^j(y_it)`, with unknown coefficients from `y_it` given membership in `j`   
        - product over `T` to reach `P^j(Y_i)`  
        - sum `pi_j * P^j(Y_i)` over all `j` to reach `P(Y_i)`   
            - **pi_j** = ?? (Page 41)   
        - product over `N` to reach the maximum likelihood function `L(theta)`  
        - log transformation to get `l(theta) = log( L(teta) )`  
        - set derivative of  `l(theta)` to `0` and solve for the unknown parameters  
        - 
* posterior probabilities for group assignment: given the modeled trajectory, what is the probability of a group assignment.  
        - 


###Software and Packages  
-----------------  
**R**:  
* `crimCV`: this software fits finite mixtures of `Zero-inflated Poisson` models to longitudinal count data.  

* `lme4`: 
```r
lmer(read ~ 1+ grade + ( 1 + grade | subid ), data = MPLS.LS, REML = FALSE)  
```  





