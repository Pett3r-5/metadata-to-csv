import pandas as pd
from scipy.stats import shapiro
from scipy.stats import ttest_ind
from scipy.stats import pearsonr

df = pd.read_csv('./pulls_vscode_with_cycle.csv')
rows_count_before_clean_up = len(df.index)

print('info: ', df.info())
print('description: ', df.describe())

valid_prs = df[
                df['totalReviews'].notnull() & 
               df['cycle_hours'].notnull() & 
               df['number'].notnull() & 
               df['title'].notnull() & 
               df['author'].notnull() & 
               df['created_at'].notnull() & 
               df['merged_at'].notnull() &
               df['state'].notnull() &
               df['state'].notnull()
            ]

print('removed lines: ', rows_count_before_clean_up - len(valid_prs.index))
print('filtered head:\n', valid_prs.head())
print('cycle_hours count: ', valid_prs['cycle_hours'].count())
print('cycle_hours média: ', valid_prs['cycle_hours'].mean())
print('cycle_hours mediana: ', valid_prs['cycle_hours'].median())
print('cycle_hours desvio padrão: ', valid_prs['cycle_hours'].std())
print('cycle_hours desvio min: ', valid_prs['cycle_hours'].min())
print('cycle_hours quartis 25%: ', valid_prs['cycle_hours'].quantile(0.25))
print('cycle_hours quartis 50%: ', valid_prs['cycle_hours'].quantile(0.50))
print('cycle_hours quartis 75%: ', valid_prs['cycle_hours'].quantile(0.75))
print('----- \n')

poucos_reviews = valid_prs[valid_prs['totalReviews'] < 2]
muitos_reviews = valid_prs[valid_prs['totalReviews'] >= 2]

# for pull in poucos_reviews['cycle_hours']:
#     print(pull)
#     print(isinstance(pull, float))

poucos_reviews_media = poucos_reviews['cycle_hours'].mean()
print('Poucos_reviews (grupo A) média: ', poucos_reviews_media)
print('Poucos_reviews (grupo A) mediana: ', poucos_reviews['cycle_hours'].median())
print('Poucos_reviews (grupo A) desvio padrão: ', poucos_reviews['cycle_hours'].std())
print('----- \n')

muitos_reviews_media = muitos_reviews['cycle_hours'].mean()
print('muitos_reviews (grupo B) média: ', muitos_reviews_media)
print('muitos_reviews (grupo B) mediana: ', muitos_reviews['cycle_hours'].median())
print('muitos_reviews (grupo B) desvio padrão: ', muitos_reviews['cycle_hours'].std())

diferenca_percentual = (muitos_reviews_media - poucos_reviews_media) / poucos_reviews_media * 100
print('Diferença percentual: ', "{:.2f}".format(diferenca_percentual), '%')
print('----- \n')

poucos_reviews_norm = shapiro(poucos_reviews['cycle_hours'].to_numpy())
print('Normalidade grupo A: ', str(poucos_reviews_norm))

muitos_reviews_norm = shapiro(muitos_reviews['cycle_hours'].to_numpy())
print('Normalidade grupo B: ', muitos_reviews_norm)

res = ttest_ind(poucos_reviews['cycle_hours'], muitos_reviews['cycle_hours'])
print(res.pvalue)
#pvalue < 0.05, logo rejeitamos H₀. Foi encontrada uma diferença significativa.
print('----- \n')

pearsonRes = pearsonr(valid_prs['totalReviews'], valid_prs['cycle_hours'])
print(pearsonRes)
# |r| < 0.3: correlação fraca

# Os grupos têm distribuições normais? Sim.
# Qual teste foi utilizado e por quê? T-test, devido às distribuições normais.
# Há diferença estatisticamente significativa entre os grupos? (p < 0.05) Sim.
# A diferença observada nas médias é apenas devido ao acaso? Não.
# Qual é a correlação entre número de reviews e tempo de ciclo? Correlação fraca.
# Os resultados confirmam ou contradizem a intuição inicial? Confirmam.

