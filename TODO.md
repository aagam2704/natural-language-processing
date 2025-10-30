# TODO: Run Real-Time Twitter Sentiment Analysis Project

## Prerequisites
- [ ] Ensure Docker is installed and running (for Kafka)
- [ ] Ensure MongoDB is installed and running (for database)
- [ ] Python virtual environment set up

## Setup Steps
- [x] Activate virtual environment
- [x] Install Python dependencies from requirements.txt (fix pandas issue if needed)
- [x] Start Kafka using Docker Compose
- [x] Create Kafka topic 'twitter'
- [x] Seed MongoDB with initial data (optional, for testing)
- [x] Run Kafka producer to send tweets
- [x] Run PySpark consumer to process tweets and store in MongoDB
- [x] Run Django dashboard

## Issues to Resolve
- PowerShell syntax: Use ; instead of && for command chaining
- Pandas installation failure on Windows: Pandas 2.3.3 is already installed, but requirements.txt specifies 2.2.2. Building from source fails. Consider updating requirements.txt to match installed version or use conda for installation.
- Docker connection issue: Ensure Docker Desktop is running
- Venv activation: Use correct path to activate script

## Commands to Run
1. Activate venv: & 'Real-Time-Twitter-Sentiment-Analysis\venv\Scripts\Activate.ps1'
2. Install deps: pip install -r requirements.txt (fix pandas)
3. Start Kafka: cd Real-Time-Twitter-Sentiment-Analysis; docker-compose -f zk-single-kafka-single.yml up -d
4. Create topic: kafka-topics --create --topic twitter --bootstrap-server localhost:9092
5. Seed Mongo: python scripts\seed_mongo.py
6. Run producer: cd Kafka-PySpark; python producer-validation-tweets.py
7. Run consumer: cd Kafka-PySpark; python consumer-pyspark.py
8. Django: cd Django-Dashboard; python manage.py collectstatic --noinput; python manage.py runserver
