from matplotlib.ticker import MaxNLocator
import numpy as np

####################################################################################################
#                               Get the min and max values in an array                             #
####################################################################################################
import numpy as np

def _data_min_max(data):
    """
    Returns the minimum and maximum of a list or array of numbers.
    Works with lists or numpy arrays.
    """
    # Convert to array first
    data = np.asarray(data)
    
    # Check for empty data
    if data.size == 0:
        raise ValueError("data is empty")
    
    min_val = np.min(data)
    max_val = np.max(data)
    return min_val, max_val

####################################################################################################
#                    Compute equispaced intermediate ticks between min and max values              #
####################################################################################################   
def _intermediate_ticks(min_val, max_val, max_ticks=5):
    """
    Returns tick values including exact min and max,
    plus nicely rounded, equispaced interior ticks.
    
    Uses a “nice” step size similar to Matplotlib's AutoLocator:
    step is a power of 10 times 1, 2, or 5.
    
    Parameters:
        min_val : float
        max_val : float
        max_ticks : approximate number of interior ticks
    
    Returns:
        list of tick values
    """
    if min_val == max_val:
        return [min_val]

    # Compute raw step size
    raw_step = (max_val - min_val) / (max_ticks + 1)  # +1 to leave room for min/max

    # Compute nice step: 1, 2, or 5 × 10^n
    magnitude = 10 ** np.floor(np.log10(raw_step))
    residual = raw_step / magnitude
    if residual <= 1:
        nice_step = 1 * magnitude
    elif residual <= 2:
        nice_step = 2 * magnitude
    elif residual <= 5:
        nice_step = 5 * magnitude
    else:
        nice_step = 10 * magnitude

    # Generate interior ticks
    start = np.ceil(min_val / nice_step) * nice_step
    end = np.floor(max_val / nice_step) * nice_step
    interior_ticks = list(np.arange(start, end + 0.5*nice_step, nice_step))

    # Remove duplicates and ensure strictly inside min/max
    interior_ticks = [t for t in interior_ticks if min_val < t < max_val]

    # Combine min, interior ticks, max
    return [min_val] + interior_ticks + [max_val]

