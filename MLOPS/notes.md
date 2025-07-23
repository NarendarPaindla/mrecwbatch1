## Module 1: Introduction & ML Lifecycle Management

**Tools:** Python, Jupyter Notebook, MLflow, Git, GitHub

### What you’ll learn

* The six ML lifecycle phases:

  1. **Data Collection**
  2. **Preprocessing**
  3. **Training**
  4. **Evaluation**
  5. **Deployment**
  6. **Monitoring**
* How MLflow tracks experiments automatically.

### End-to-end code (notebook)

1. **Install and import MLflow**

   ```bash
   pip install mlflow scikit-learn pandas
   ```
2. **Notebook code**

   ```python
   # In a Jupyter cell
   import mlflow
   import mlflow.sklearn
   from sklearn.datasets import load_iris
   from sklearn.model_selection import train_test_split
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.metrics import accuracy_score
   import pandas as pd

   # 1. Load data
   iris = load_iris(as_frame=True)
   X, y = iris.data, iris.target

   # 2. Split
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.3, random_state=42
   )

   # 3. Start MLflow run
   with mlflow.start_run(run_name="RF_Iris"):
       params = {"n_estimators": 100, "max_depth": 3}
       mlflow.log_params(params)

       # 4. Train
       model = RandomForestClassifier(**params, random_state=42)
       model.fit(X_train, y_train)

       # 5. Evaluate
       preds = model.predict(X_test)
       acc = accuracy_score(y_test, preds)
       mlflow.log_metric("accuracy", acc)

       # 6. Log model
       mlflow.sklearn.log_model(model, artifact_path="rf_model")

   print(f"Logged model with accuracy: {acc:.2f}")
   ```
3. **View in MLflow UI**

   ```bash
   mlflow ui
   ```

   Open [http://localhost:5000](http://localhost:5000) in your browser.

### Kid tip

> “Think of MLflow like a notebook that remembers every experiment for you!”

### Checkpoint Summary

* ✔️ Installed and used MLflow
* ✔️ Loaded, split, and trained on the Iris dataset
* ✔️ Logged parameters, metrics, and model to MLflow
* ✔️ Viewed runs in the MLflow UI

### Mini-Project

* **Track a second model:**

  * Change `n_estimators` and `max_depth`.
  * Compare both runs’ accuracies in your notebook.

---

## Module 2: CI/CD for Machine Learning

**Tools:** GitHub, GitHub Actions, Python scripts, MLflow CLI

### What you’ll learn

* Automating training & tests on every code change (“CI”)
* Publishing artifact snapshots after success (“CD”)

### End-to-end code

1. **Project structure**

   ```
   mlops-ci/
   ├── train.py
   ├── tests/
   │   └── test_preprocess.py
   └── .github/workflows/ci.yml
   ```
2. **`train.py`**

   ```python
   import mlflow, mlflow.sklearn
   from sklearn.datasets import load_iris
   from sklearn.model_selection import train_test_split
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.metrics import accuracy_score

   def train_and_log():
       iris = load_iris(as_frame=True)
       X, y = iris.data, iris.target
       X_train, X_test, y_train, y_test = train_test_split(
           X, y, test_size=0.3, random_state=42
       )
       params = {"n_estimators": 50, "max_depth": 2}
       with mlflow.start_run():
           mlflow.log_params(params)
           model = RandomForestClassifier(**params, random_state=42)
           model.fit(X_train, y_train)
           acc = accuracy_score(y_test, model.predict(X_test))
           mlflow.log_metric("accuracy", acc)
           mlflow.sklearn.log_model(model, "model")
       print(f"Run completed with accuracy {acc:.2f}")

   if __name__ == "__main__":
       train_and_log()
   ```
3. **`tests/test_preprocess.py`**

   ```python
   from sklearn.datasets import load_iris
   from sklearn.model_selection import train_test_split

   def test_split_sizes():
       iris = load_iris(as_frame=True)
       X, y = iris.data, iris.target
       X_train, X_test, y_train, y_test = train_test_split(
           X, y, test_size=0.3, random_state=42
       )
       assert len(X_train) > len(X_test)
   ```
4. **`.github/workflows/ci.yml`**

   ```yaml
   name: CI

   on:
     push:
       branches: [ main ]

   jobs:
     build-and-test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.9'
         - name: Install dependencies
           run: |
             pip install mlflow scikit-learn pytest
         - name: Run training script
           run: python train.py
         - name: Run tests
           run: pytest tests/
         - name: Publish MLflow artifacts
           run: |
             mlflow artifacts list .
   ```

### Kid tip

> “CI/CD is like a robot that builds your Lego castle every time you add a new brick.”

### Checkpoint Summary

* ✔️ Created `train.py` and unit test
* ✔️ Configured GitHub Actions workflow
* ✔️ Automated training, testing, and artifact listing

### Mini-Project

* **Add a new unit test** for data preprocessing (e.g., test a feature’s value range).

---

## Module 3: Model & Data Versioning

**Tools:** DVC, MLflow Tracking & Registry, Git

### What you’ll learn

* Versioning raw data with DVC
* Registering and pulling model versions via MLflow

### End-to-end code

1. **Initialize DVC & Git**

   ```bash
   git init
   dvc init
   ```
2. **Add raw data**

   ```bash
   # Suppose you have data/raw.csv
   dvc add data/raw.csv
   git add data/.gitignore data/raw.csv.dvc
   git commit -m "Version raw data with DVC"
   ```
3. **Train & register model** (in `train_and_register.py`)

   ```python
   import mlflow, mlflow.sklearn
   from sklearn.model_selection import train_test_split
   from sklearn.ensemble import RandomForestClassifier
   import pandas as pd

   df = pd.read_csv("data/raw.csv")
   X = df.drop("target", axis=1)
   y = df["target"]
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

   with mlflow.start_run() as run:
       mlflow.sklearn.log_model(
           sklearn_model=RandomForestClassifier(n_estimators=10),
           artifact_path="model"
       )
       model_uri = f"runs:/{run.info.run_id}/model"
       # Register to MLflow Model Registry
       mlflow.register_model(model_uri, "MyModel")
       print("Registered run", run.info.run_id)
   ```
4. **Load a previous model version**

   ```python
   import mlflow.pyfunc

   # Load version 1 of "MyModel"
   model = mlflow.pyfunc.load_model("models:/MyModel/1")
   preds = model.predict(X_test)
   ```

### Kid tip

> “DVC is like saving different drafts of your homework so you can go back if you make a mistake.”

### Checkpoint Summary

* ✔️ Versioned dataset with DVC
* ✔️ Tracked & registered a model in MLflow Registry
* ✔️ Loaded a specific model version in code

### Mini-Project

* **Roll back** to an older dataset version (`dvc checkout`) and retrain the model.

---

## Module 4: Automated ML Pipelines

**Tools:** Prefect, Python, Git

### What you’ll learn

* Defining and running a multi-step pipeline locally
* Logging each step’s output

### End-to-end code

1. **Install Prefect**

   ```bash
   pip install prefect pandas scikit-learn
   ```
2. **`pipeline.py`**

   ```python
   from prefect import task, Flow
   from sklearn.datasets import load_iris
   from sklearn.model_selection import train_test_split
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.metrics import accuracy_score

   @task
   def load_data():
       data = load_iris(as_frame=True)
       return data.data, data.target

   @task
   def preprocess(X, y):
       return train_test_split(X, y, test_size=0.3, random_state=42)

   @task
   def train(X_train, y_train):
       model = RandomForestClassifier(n_estimators=20, random_state=42)
       model.fit(X_train, y_train)
       return model

   @task
   def evaluate(model, X_test, y_test):
       acc = accuracy_score(y_test, model.predict(X_test))
       print(f"Pipeline accuracy: {acc:.2f}")
       return acc

   with Flow("mlops-pipeline") as flow:
       X, y = load_data()
       X_train, X_test, y_train, y_test = preprocess(X, y)
       model = train(X_train, y_train)
       evaluate(model, X_test, y_test)

   if __name__ == "__main__":
       flow.run()
   ```

### Kid tip

> “A pipeline is like a breakfast line: you go from plate → eggs → toast → butter in order.”

### Checkpoint Summary

* ✔️ Defined tasks for each ML step
* ✔️ Composed and ran the Prefect `Flow` locally
* ✔️ Observed logs for every task

### Mini-Project

* **Add a validation task:** compute and print a confusion matrix.

---

## Module 5: Continuous Monitoring & Drift Detection

**Tools:** Flask, MLflow, simple Python script

### What you’ll learn

* Serving your model via a minimal API
* Comparing live data stats against baseline

### End-to-end code

1. **Flask app (`app.py`)**

   ```python
   from flask import Flask, request, jsonify
   import mlflow.pyfunc

   app = Flask(__name__)
   model = mlflow.pyfunc.load_model("models:/MyModel/1")

   @app.route("/predict", methods=["POST"])
   def predict():
       data = request.get_json()  # expect {"features": [ ... ]}
       preds = model.predict(data["features"])
       return jsonify({"predictions": preds.tolist()})

   if __name__ == "__main__":
       app.run(debug=True, port=5001)
   ```
2. **Drift detection script (`drift_monitor.py`)**

   ```python
   import pandas as pd
   from scipy.stats import ks_2samp

   # Baseline data
   baseline = pd.read_csv("data/raw.csv")
   # Simulated new data
   new_data = pd.read_csv("data/new.csv")

   alerts = []
   for col in baseline.columns.drop("target"):
       stat, p = ks_2samp(baseline[col], new_data[col])
       if p < 0.05:
           alerts.append(f"Drift detected in '{col}' (p={p:.3f})")

   if alerts:
       print("ALERTS:")
       for a in alerts:
           print(" -", a)
   else:
       print("No drift detected.")
   ```

### Kid tip

> “Monitoring is like checking your plants every day to see if they need water.”

### Checkpoint Summary

* ✔️ Deployed model via Flask endpoint
* ✔️ Simulated drift and detected it with a simple test
* ✔️ Printed alerts when drift occurs

### Mini-Project

* **Extend** `drift_monitor.py` to send an email when drift is found (use `smtplib`).

---

## Module 6: Case Studies & Best Practices

**Tools:** None (discussion + diagrams)

### What you’ll learn

* **Netflix** recommendation pipeline
* **Uber** Michelangelo MLOps platform
* **Airbnb** dynamic pricing infrastructure

### End-to-end guide

1. **Block diagram** each system on paper or whiteboard:

   * Data sources → Feature store → Training → Deployment → Monitoring
2. **Map** each Netflix/Uber/Airbnb step to our Modules 1–5.
3. **Summarize** lessons:

   * Version everything
   * Automate pipelines
   * Monitor continuously

### Kid tip

> “Think of these companies like big science fairs showing how they build and care for their models.”

### Checkpoint Summary

* ✔️ Understood real-world MLOps platforms
* ✔️ Mapped theory modules to large systems
* ✔️ Noted common best practices

### Mini-Project

* **Pick one case study** and sketch your own mini-ML pipeline, labeling each step with the corresponding module number.

---


