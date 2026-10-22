# Spaceship Titanic

Download the data from the [Kaggle competition data page](https://www.kaggle.com/competitions/spaceship-titanic/data): sign in, accept the competition rules, and click **Download All**.

From the repository root, unzip the downloaded archive into the competition's `input/` folder:

```bash
mkdir -p spaceship_titanic_students/input
unzip ~/Downloads/spaceship-titanic.zip -d spaceship_titanic_students/input
```

Adjust the archive path if needed. The CSV files should sit directly inside `spaceship_titanic_students/input/` (`train.csv`, `test.csv`, and `sample_submission.csv`). Run pipelines from `spaceship_titanic_students/` so they can find `input/`.
