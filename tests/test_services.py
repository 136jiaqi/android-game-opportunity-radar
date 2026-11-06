from services.normalization import canonical_name
from services.demand_analysis import classify
from services.scoring import opportunity, coverage_score
def test_normalize(): assert canonical_name('Game: One!') == 'gameone'
def test_demand_keywords(): assert 'cheat' in classify('Need a cheat trainer')
def test_no_fake_score(): assert opportunity(1,None,2,3) is None
def test_coverage(): assert coverage_score(3,4)[1] == 'high'
