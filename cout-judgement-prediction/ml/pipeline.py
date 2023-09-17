import pandas as pd
import pathlib
from pycaret.regression import RegressionExperiment

cwd = pathlib.Path.cwd()

file_path = cwd.parent / 'data' / 'eug_judgments_raw.csv'

df = pd.read_csv(
    file_path.as_posix(),
    # on_bad_lines="warn"
)

df['application_date'] = pd.to_datetime(df['application_date'])
df['judgment_date'] = pd.to_datetime(df['judgment_date'])

ignore_features = [
    "case",
    "document",
    "judgment_date",
    "name_of_the_parties",
    "curia",
    "eur_lex",
]

text_features = ["name_of_the_parties"]

date_features = [
    'application_date',
]

categorical_features = [
    "subject_matter",
]

exp = RegressionExperiment()

exp.setup(
    df,
    target='days_to_judgment',
    session_id=123,
    use_gpu=True,
    categorical_features=categorical_features,
    ignore_features=ignore_features,
    date_features=date_features,
    create_date_columns=["day", "month", "year"],
    # rare_value="subject_matter",
    # rare_to_value=0.1,
)


best = exp.compare_models()

print(best)

exp.plot_model(best, plot='feature')

# exp.evaluate_model(best)

exp.plot_model(best, plot='residuals')

exp.plot_model(best, plot='error')

# predict on test set
holdout_pred = exp.predict_model(best)

# finalize model
final_best = exp.finalize_model(best)

test = exp.predict_model(final_best, data=holdout_pred)

print(final_best)

exp.save_model(final_best, 'best_pipeline')
