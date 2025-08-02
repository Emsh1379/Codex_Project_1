import csv
import math

FILENAME = 'FirstAuthor-Year-NumberofPatients-AnemiaAnyGrade.csv'

studies = []
with open(FILENAME, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = float(row['Number of Patients'])
        p_raw = float(row['Anemia Any Grade (%)']) / 100.0
        events = p_raw * n
        # continuity correction for 0 or 100% proportions
        if events == 0:
            events += 0.5
            n += 1
        elif events == n:
            events -= 0.5
            n += 1
        p = events / n
        studies.append({'name': row['First Author'], 'year': row['Year'], 'n': n, 'p': p})

# Compute event counts
for study in studies:
    study['events'] = study['p'] * study['n']

# Fixed effect weights using inverse variance of proportion
for study in studies:
    p = study['p']
    n = study['n']
    se = math.sqrt(p * (1 - p) / n)
    study['se'] = se
    study['weight'] = 1.0 / (se ** 2)

# Fixed effect pooled proportion
sum_w = sum(s['weight'] for s in studies)
p_fixed = sum(s['weight'] * s['p'] for s in studies) / sum_w

# DerSimonian-Laird random effects
Q = sum(s['weight'] * (s['p'] - p_fixed) ** 2 for s in studies)
df = len(studies) - 1
C = sum_w - sum(s['weight'] ** 2 for s in studies) / sum_w
tau2 = max((Q - df) / C, 0)
for study in studies:
    study['rand_weight'] = 1.0 / (study['se'] ** 2 + tau2)

sum_w_star = sum(s['rand_weight'] for s in studies)
p_random = sum(s['rand_weight'] * s['p'] for s in studies) / sum_w_star
se_random = math.sqrt(1 / sum_w_star)
ci_low = p_random - 1.96 * se_random
ci_high = p_random + 1.96 * se_random

I2 = 0.0
if Q > df:
    I2 = max((Q - df) / Q, 0) * 100

print(f'Number of studies: {len(studies)}')
print(f'Fixed effect pooled proportion: {p_fixed*100:.2f}%')
print(f'Random effects pooled proportion: {p_random*100:.2f}%')
print(f'95% CI: [{ci_low*100:.2f}%, {ci_high*100:.2f}%]')
print(f'I^2: {I2:.2f}%')
