##Goal: 
Given a labeled dataset (i.e. TMI vs non-TMI), we analyze and distinguish the differences in the profiles’ behaviors, predict and forecast the trajectory model and its trends, and then assess risk factors among these groups. The problems we encounter are the followings: 
*	Feature Selection: What features and how many features to model? 
*	Use Case: given a recorded data or a set of meaningful signals at a time point (i.e. 9 months from the incidence), assess the risk of having the disorder.
*	In the matter of fact, the model is sensitive to **time**, however there will be **segmental changes over time** of the same subject (i.e. a certain degree of elevation in some features over the past 3 months may “qualify” the subject to a higher risk.)
*	Looking for influential features such as age and gender that help to assess risks (i.e. a boy is more likely to have autism than a girl)




##Analysis/Modeling Approaches:  

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

###Application on EEG data:  
------------------------  
 
**Result of the project**: 

*	We found the trends and trajectory model of the EEG measurements for each groups: normal, high risk, and diagnosed with autism.
*	given a set of measures over time from a new subject, we are able to compare against the group trajectories and determine whether the new trajectories are more likely to belong to the normal group or the autism group
*	risk assessment given not just a one-time measurement but a trajectory of measurements


**Data Structure**  
- multiple records for one subject (at time points 3, 6, 9, 12, 18, 24, 36 months of age)  
- Identifiers: 
	- ID: subject ID 
	- Age: time variable
	- gender
	- class: indicator (asd-autism, typ-normal, hra-high risk autism but do not have autism)  
- Measurements:  
	- sensor or channel (19):  
` ["C3", "C4", "O1", "O2", "Cz", "F3", "F4", "F7", "F8", "Fz", "Fp1", "Fp2", "P3", "P4", "Pz", "T7", "T8", "P7", "P8"]`  
	- features (9):   
` ['Power', 'SampE', 'RR', 'DET', 'LAM', 'L_entr', 'L_max', 'L_mean', 'TT']`  
	- Frequency band or scale (6):  
` [0,1,2,3,4,5]`  
	Example: `C3.Power.s0`  

**Key Steps**  
- plot profile plots for subjects from `asd` and `typ` group    
- observe/fit trends  
- develop a determination method  

**Issues**  
- feature selection  
	- one more dimension to consider--time!  
	- some activities may only be caught by specific scale of the channel-feature pair
- too many features (1025)  
- utilize time variable  
	- slopes between two time points   
	- fit trajectories with polynomials, make the coefficients as the new features for each subject of a given measurement  

**Approaches**  
- feature selection:  
	- ordinary feature selection tools only depended on one-time measurement, do not consider time or change over time.  
	- we want to make our model sensitive to time or change over time.  
	-**feature ranking** based on differences on average trajectories of the groups  
		- for each feature, find the average trajectories for the groups
		- there are differences in distances/area between the curves
		- there are differences in the coefficients when fit the curves with polynomials  
	-**slope comparison** 




###Software and Packages  
-----------------  
**R**:  
* `crimCV`: this software fits finite mixtures of `Zero-inflated Poisson` models to longitudinal count data.  

* `lme4`: 
```r
lmer(read ~ 1+ grade + ( 1 + grade | subid ), data = MPLS.LS, REML = FALSE)  
```  





