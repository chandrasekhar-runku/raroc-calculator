"""Basel IRB risk-weighted assets and RAROC for a single corporate loan."""
from math import exp, log, sqrt
from scipy.stats import norm

PD_FLOOR = 0.0005  # 0.05% floor (Basel III final reforms)


def asset_correlation(pd: float) -> float:
    w = (1 - exp(-50 * pd)) / (1 - exp(-50))
    return 0.12 * w + 0.24 * (1 - w)


def maturity_adjustment(pd: float) -> float:
    return (0.11852 - 0.05478 * log(pd)) ** 2


def capital_requirement_k(pd: float, lgd: float, maturity: float = 2.5) -> float:
    """Capital requirement K as a fraction of EAD (99.9% confidence)."""
    pd = max(pd, PD_FLOOR)
    maturity = min(max(maturity, 1.0), 5.0)
    r = asset_correlation(pd)
    b = maturity_adjustment(pd)

    conditional_pd = norm.cdf(
        (norm.ppf(pd) + sqrt(r) * norm.ppf(0.999)) / sqrt(1 - r)
    )
    k = (lgd * conditional_pd - pd * lgd) * (1 + (maturity - 2.5) * b) / (1 - 1.5 * b)
    return max(k, 0.0)


def calculate_rwa(ead, pd, lgd, maturity=2.5, scaling_factor=1.0):
    """RWA = K x 12.5 x EAD. Basel II used a 1.06 scaling factor; Basel III final removes it."""
    k = capital_requirement_k(pd, lgd, maturity)
    return k * 12.5 * ead * scaling_factor


def calculate_raroc(
    ead, pd, lgd, maturity,
    interest_rate, funding_cost, fees, opex,
    capital_ratio=0.105, tax_rate=0.0,
):
    """
    RAROC = (Revenue - Funding cost - Opex - Expected loss) x (1 - tax) / Capital
    Capital = RWA x capital ratio (regulatory capital as a proxy for economic capital).
    All rate inputs are annual, as decimals (0.03 = 3%).
    """
    rwa = calculate_rwa(ead, pd, lgd, maturity)
    capital = rwa * capital_ratio
    revenue = ead * interest_rate + fees
    funding = ead * funding_cost
    operating = ead * opex
    expected_loss = pd * lgd * ead

    net_income = (revenue - funding - operating - expected_loss) * (1 - tax_rate)
    raroc = net_income / capital if capital > 0 else float("nan")

    return {
        "RWA": rwa,
        "Risk weight (%)": rwa / ead * 100,
        "Capital held": capital,
        "Revenue": revenue,
        "Funding cost": funding,
        "Opex": operating,
        "Expected loss": expected_loss,
        "Net income": net_income,
        "RAROC (%)": raroc * 100,
    }
