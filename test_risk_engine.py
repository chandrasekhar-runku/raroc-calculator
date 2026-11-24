from risk_engine import calculate_rwa

def test_reference_case():
    rw = calculate_rwa(ead=100, pd=0.01, lgd=0.45, maturity=2.5) / 100
    assert 0.90 < rw < 0.96

def test_higher_pd_means_higher_rwa():
    assert calculate_rwa(100, 0.05, 0.45) > calculate_rwa(100, 0.01, 0.45)

def test_higher_lgd_means_higher_rwa():
    assert calculate_rwa(100, 0.01, 0.75) > calculate_rwa(100, 0.01, 0.45)
