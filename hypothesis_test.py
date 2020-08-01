import math
import scipy.stats

def hyp_test(size1, year1, size2, year2):
    """
    size1/2 == total population
    year1/2 == population need to test
    Use two tailed Hypothesis test and Z test.
    """
    print("Null Hypothesis H0:  year1 == year2")
    print("Alternative Hypothesis HA: year1 != year2")
    alpha = 0.05/2
    p_h = (year2 + year1)/(size2 + size1)
    stdd = ((p_h * (1 - p_h))/size2) + ((p_h * (1 - p_h))/size1)
    z_value = (year2/size2 - year1/size1) / math.sqrt(stdd)
    print("z value: ", z_value)
    p_value = scipy.stats.norm.sf(abs(z_value))*2
    print("p value: ", p_value)
    if p_value > alpha:
        print("Fail to reject H0: year1 == year2")
    else:
        print("Reject H0: year1 != year2")
