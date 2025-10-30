import re
import nltk
from typing import Optional

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Lazy-load Spark pipeline. If Spark is not available or fails to load (common on Windows
# without Hadoop/winutils), fall back to a lightweight rule-based classifier so the
# web UI's classify page still works.

class_index_mapping = {0: "Negative", 1: "Positive", 2: "Neutral", 3: "Irrelevant"}


def clean_text(text: Optional[str]) -> str:
    if text is None:
        return ''
    # Remove links starting with https://, http://, www., or containing .com
    text = re.sub(r'https?://\S+|www\.\S+|\.com\S+|youtu\.be/\S+', '', text)
    # Remove words starting with # or @
    text = re.sub(r'(@|#)\w+', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Simple fallback sentiment classifier (bag of positive/negative words). This runs
# quickly and allows the classify endpoint to work even when Spark isn't available.
POS_WORDS = set(["good", "great", "happy", "love", "excellent", "best", "awesome", "nice", "win"])
NEG_WORDS = set(["bad", "sad", "hate", "terrible", "worst", "angry", "awful", "lose", "problem"])


def fallback_classify(text: str) -> str:
    toks = [t.lower() for t in re.findall(r"\w+", text)]
    pos = sum(1 for t in toks if t in POS_WORDS)
    neg = sum(1 for t in toks if t in NEG_WORDS)
    if pos == 0 and neg == 0:
        return "Neutral"
    return "Positive" if pos >= neg else "Negative"


def classify_text(text: str) -> str:
    """Try to classify using the Spark pipeline if available; otherwise use fallback."""
    preprocessed = clean_text(text)

    # Try lazy Spark usage to avoid import-time failures
    try:
        # Import here so the module can be imported even when Spark isn't configured
        from pyspark.sql import SparkSession
        from pyspark.ml import PipelineModel

        # Use a module-global pipeline if already loaded
        if not globals().get("_spark_pipeline"):
            spark = SparkSession.builder.appName("classify tweets").getOrCreate()
            # Try possible model locations relative to project layout
            model_paths = [
                "logistic_regression_model.pkl",
                "Kafka-PySpark/logistic_regression_model.pkl",
                "../Kafka-PySpark/logistic_regression_model.pkl",
                "../logistic_regression_model.pkl",
                "Django-Dashboard/logistic_regression_model.pkl",
                "ML PySpark Model/logistic_regression_model.pkl",
            ]
            loaded = False
            for p in model_paths:
                try:
                    pipeline = PipelineModel.load(p)
                    globals()["_spark_pipeline"] = pipeline
                    globals()["_spark_session"] = spark
                    loaded = True
                    break
                except Exception:
                    continue
            if not loaded:
                raise RuntimeError("Could not find/load Spark pipeline model")

        pipeline = globals().get("_spark_pipeline")
        spark = globals().get("_spark_session")
        data = [(preprocessed,)]
        df = spark.createDataFrame(data, ["Text"])
        processed = pipeline.transform(df)
        # prediction column index may vary; look up by name if possible
        try:
            prediction = processed.collect()[0][6]
        except Exception:
            # fallback to selecting by column name
            if "prediction" in processed.columns:
                prediction = processed.collect()[0][processed.columns.index("prediction")]
            else:
                raise
        return class_index_mapping[int(prediction)]

    except Exception as e:
        # Log the exception server-side and use fallback
        print("Spark classify failed, using fallback. Error:", e)
        return fallback_classify(preprocessed)
