# Task 3: Data Analysis with Pandas
# Dataset: Student Grades & Performance

import pandas as pd

# ─────────────────────────────────────────
# STEP 1: Load and Inspect the Dataset
# ─────────────────────────────────────────

print("=" * 50)
print("STEP 1: Loading and Inspecting the Dataset")
print("=" * 50)

df = pd.read_csv("students.csv")

print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\nDataset Shape (rows, columns):", df.shape)

print("\nColumn Names:", list(df.columns))

print("\nData Types:")
print(df.dtypes)

print("\nBasic Statistics:")
print(df.describe())

print("\nMissing Values per Column:")
print(df.isnull().sum())


# ─────────────────────────────────────────
# STEP 2: Clean Missing or Incorrect Data
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("STEP 2: Cleaning the Dataset")
print("=" * 50)

print("\nRows before cleaning:", len(df))

# Fill missing scores with the column median
for col in ["math_score", "science_score", "english_score"]:
    median_val = df[col].median()
    missing = df[col].isnull().sum()
    df[col] = df[col].fillna(median_val)
    print(f"  Filled {missing} missing value(s) in '{col}' with median ({median_val})")

# Fix attendance column — strip spaces and convert to float
df["attendance_%"] = df["attendance_%"].astype(str).str.strip()
df["attendance_%"] = pd.to_numeric(df["attendance_%"], errors="coerce")
df["attendance_%"] = df["attendance_%"].fillna(df["attendance_%"].median())

# Fix grade column — fill missing grade with F for students with very low scores
df["grade"] = df["grade"].fillna("F")

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nRows after cleaning:", len(df))


# ─────────────────────────────────────────
# STEP 3: Filtering, Grouping & Aggregation
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("STEP 3: Filtering, Grouping & Aggregation")
print("=" * 50)

# --- Filtering ---
print("\n-- Top Performers (Grade A) --")
top_students = df[df["grade"] == "A"][["name", "math_score", "science_score", "english_score", "grade"]]
print(top_students.to_string(index=False))

print("\n-- Students with Attendance below 70% --")
low_attendance = df[df["attendance_%"] < 70][["name", "attendance_%", "grade"]]
print(low_attendance.to_string(index=False))

# --- Average score per student ---
df["average_score"] = df[["math_score", "science_score", "english_score"]].mean(axis=1).round(2)

# --- Grouping by Grade ---
print("\n-- Average Scores by Grade --")
grade_group = df.groupby("grade")[["math_score", "science_score", "english_score", "average_score"]].mean().round(2)
print(grade_group)

# --- Grouping by Gender ---
print("\n-- Average Scores by Gender --")
gender_group = df.groupby("gender")[["math_score", "science_score", "english_score", "average_score"]].mean().round(2)
print(gender_group)

# --- Aggregation: Subject-wise stats ---
print("\n-- Subject-wise Statistics --")
subject_stats = df[["math_score", "science_score", "english_score"]].agg(["mean", "min", "max", "std"]).round(2)
print(subject_stats)

# --- Grade distribution ---
print("\n-- Grade Distribution --")
grade_counts = df["grade"].value_counts().sort_index()
print(grade_counts)


# ─────────────────────────────────────────
# STEP 4: Insights Summary
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("STEP 4: Insights Summary")
print("=" * 50)

total = len(df)
grade_a = len(df[df["grade"] == "A"])
grade_f = len(df[df["grade"] == "F"])
top_student = df.loc[df["average_score"].idxmax(), "name"]
low_student = df.loc[df["average_score"].idxmin(), "name"]
best_subject = df[["math_score", "science_score", "english_score"]].mean().idxmax().replace("_score", "").title()
weak_subject = df[["math_score", "science_score", "english_score"]].mean().idxmin().replace("_score", "").title()

print(f"\n Total Students Analysed : {total}")
print(f" Grade A Students        : {grade_a} ({round(grade_a/total*100)}% of class)")
print(f" Grade F Students        : {grade_f} ({round(grade_f/total*100)}% of class)")
print(f" Top Performing Student  : {top_student}")
print(f" Lowest Scoring Student  : {low_student}")
print(f" Strongest Subject       : {best_subject}")
print(f" Weakest Subject         : {weak_subject}")
print(f" Avg Class Attendance    : {df['attendance_%'].mean().round(1)}%")

print("\nDone.")
