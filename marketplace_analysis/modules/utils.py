from math import radians, sin, cos, asin, sqrt

def haversine_distance(lon1, lat1, lon2, lat2):
    """
    Compute distance between two pairs of coordinates (lon1, lat1, lon2, lat2)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))

def return_significative_coef(model):
    """
    Returns p_value, lower and upper bound coefficients
    from a statsmodels object.
    """
    # Extract p_values
    p_values = model.pvalues.reset_index()
    p_values.columns = ['feature', 'p_value']

    # Extract coef_int
    coef = model.params.reset_index()
    coef.columns = ['feature', 'coef']
    df = p_values.merge(coef, on='feature').query("p_value<0.05")\
        .sort_values('coef', ascending=False).reset_index(drop=True).rename(columns={'p_value':'p-value'})

    df['p-value'] = df['p-value'].apply(lambda x: '{:,.4f}'.format(x))
    df['coef'] = df['coef'].apply(lambda x: '{:,.2f}'.format(x))

    return df[df['feature'] != 'Intercept'].reset_index(drop=True)
