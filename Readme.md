# Fraud Detection Intelligent System

An intelligent fraud detection system that combines machine learning models, rule-based detection engines, and retrieval-augmented generation (RAG) to identify and investigate fraudulent transactions in real-time.

## Project Overview

This system processes financial transactions through multiple detection layers:
- **ML Engine**: XGBoost-based predictive model for fraud probability scoring
- **Rules Engine**: Behavior, velocity, amount, country, and device-based rules for fraud detection
- **Data Pipeline**: Kafka-based streaming architecture for real-time transaction processing
- **Investigation**: RAG-powered system for fraud case investigation and reporting
- **Dashboard**: Streamlit-based real-time fraud monitoring and alert visualization
- **Storage**: Supabase backend for persistent alert and transaction storage

## Project Outline

### Core Architecture

```
Transaction Input → Kafka Producer → Consumer Pipeline → Multi-Layer Detection → Storage → Dashboard
                                            ↓
                                   ML Model Scoring
                                   Rules Engine Scoring
                                   User Profile Analysis
                                            ↓
                                   Combined Risk Score
                                            ↓
                                   Alert Generation & Reporting
```

---

## File Structure & Descriptions

### Root Level Files
| File | Description |
|------|-------------|
| [main.py](main.py) | Entry point for the fraud detection system (currently empty, ready for orchestration logic) |
| [create_project.py](create_project.py) | Project initialization script that sets up directory structure and configuration files |
| [requirements.txt](requirements.txt) | Python dependencies including Kafka, XGBoost, Streamlit, FAISS, and ML libraries |
| [docker-compose.yml](docker-compose.yml) | Docker configuration for running Kafka and other services in containers |
| [Readme.md](Readme.md) | Project documentation and setup guide |
| [models](models) | Directory containing pre-trained ML models (XGBoost pickle files and FAISS indices) |
| [Data/transactions.csv](Data/transactions.csv) | Sample transaction data for testing and model training |

---

### Configuration Module (`config/`)
| File | Description |
|------|-------------|
| [config/__init__.py](config/__init__.py) | Package initialization file for config module |
| [config/config.py](config/config.py) | Environment configuration loader for Supabase credentials and API keys using dotenv |

---

### Dashboard Module (`dashboard/`)
| File | Description |
|------|-------------|
| [dashboard/__init__.py](dashboard/__init__.py) | Package initialization file for dashboard module |
| [dashboard/app.py](dashboard/app.py) | Streamlit dashboard application for real-time fraud monitoring and alert visualization |
| [dashboard/alert.py](dashboard/alert.py) | Alert management functions including fetching and extracting fraud alerts from Supabase |

---

### Data Engine Module (`engine/`)
| File | Description |
|------|-------------|
| [engine/__init__.py](engine/__init__.py) | Package initialization file for engine module |
| [engine/producer.py](engine/producer.py) | Kafka producer that generates and streams synthetic or real transactions to the Kafka topic |
| [engine/consumer.py](engine/consumer.py) | Kafka consumer that processes incoming transactions through the fraud detection pipeline |
| [engine/user_profile.py](engine/user_profile.py) | Creates and manages user profile data including spending patterns and location history |
| [engine/user_history.py](engine/user_history.py) | Maintains transaction history for each user for historical analysis and trend detection |
| [engine/user_stats.py](engine/user_stats.py) | Calculates user behavioral statistics like average transaction amount and frequency |

---

### Machine Learning Module (`ml/`)
| File | Description |
|------|-------------|
| [ml/__init__.py](ml/__init__.py) | Package initialization file for ml module |
| [ml/fraud_model.py](ml/fraud_model.py) | Loads pre-trained XGBoost model and provides fraud probability prediction for transactions |
| [ml/train_xgb.py](ml/train_xgb.py) | Training script for XGBoost fraud detection model on historical labeled data |
| [ml/predict.py](ml/predict.py) | Prediction utility that applies the trained model to new transactions in batch or real-time |
| [ml/features.py](ml/features.py) | Feature engineering pipeline that extracts and transforms transaction features for model input |
| [ml/decision_engine.py](ml/decision_engine.py) | Combines ML predictions with rule-based scores to generate final fraud risk decisions |
| [ml/export_transactions.py](ml/export_transactions.py) | Utility script to export labeled transactions for model training and evaluation |

---

### Rules Engine Module (`Rules/`)
| File | Description |
|------|-------------|
| [Rules/__init__.py](Rules/__init__.py) | Package initialization file for Rules module |
| [Rules/amount_rules.py](Rules/amount_rules.py) | Detects unusually large transactions compared to user's historical spending patterns |
| [Rules/velocity_rules.py](Rules/velocity_rules.py) | Flags rapid-fire transactions within short time windows to detect velocity-based fraud |
| [Rules/behaviour_rules.py](Rules/behaviour_rules.py) | Analyzes deviation from user's typical transaction behavior and spending habits |
| [Rules/country_rules.py](Rules/country_rules.py) | Identifies impossible travel scenarios and transactions from high-risk countries |
| [Rules/device_rules.py](Rules/device_rules.py) | Detects new or unknown devices and device-switching fraud patterns |
| [Rules/scoring.py](Rules/scoring.py) | Aggregates results from all rule engines and calculates combined fraud risk score |

---

### RAG Module (`rag/`)
| File | Description |
|------|-------------|
| [rag/__init__.py](rag/__init__.py) | Package initialization file for RAG module |
| [rag/build_index.py](rag/build_index.py) | Creates FAISS vector index from fraud knowledge documents for semantic search |
| [rag/create_documents.py](rag/create_documents.py) | Generates fraud case documentation and knowledge base documents from transaction data |
| [rag/fraud_docs.json](rag/fraud_docs.json) | JSON file containing fraud patterns, case studies, and investigative guidelines |
| [rag/fraud_index.faiss](rag/fraud_index.faiss) | Pre-built FAISS vector index for fast similarity search of fraud cases and patterns |
| [rag/retrieve.py](rag/retrieve.py) | Retrieves similar fraud cases and patterns from the FAISS index using semantic similarity |
| [rag/investigator.py](rag/investigator.py) | Generates detailed fraud investigation reports using retrieved context and LLM analysis |
| [rag/test.py](rag/test.py) | Test script for validating RAG pipeline functionality and retrieval accuracy |

---

### Simulator Module (`simulator/`)
| File | Description |
|------|-------------|
| [simulator/__init__.py](simulator/__init__.py) | Package initialization file for simulator module |
| [simulator/transaction_generator.py](simulator/transaction_generator.py) | Generates synthetic transactions with realistic patterns and occasional fraud scenarios for testing |

---

### Storage Module (`storage/`)
| File | Description |
|------|-------------|
| [storage/__init__.py](storage/__init__.py) | Package initialization file for storage module |
| [storage/db.py](storage/db.py) | Supabase database interface for storing and retrieving fraud alerts and transaction records |
| [storage/storage.py](storage/storage.py) | Generic storage abstraction layer for managing fraud detection results and audit logs |

---

## Technology Stack

- **ML Framework**: XGBoost for predictive fraud detection
- **Streaming**: Apache Kafka for real-time transaction processing
- **Vector Search**: FAISS for semantic similarity search in RAG module
- **Embeddings**: Sentence-Transformers for generating document and query embeddings
- **LLM**: Ollama for local inference in fraud investigation
- **Frontend**: Streamlit for interactive dashboard
- **Backend**: Supabase for cloud database and REST API
- **ML Utilities**: Scikit-learn, joblib, numpy, pandas
- **Visualization**: Plotly for interactive charts

## Getting Started

### Prerequisites
- Python 3.8+
- Docker and Docker Compose (for Kafka)
- Supabase account or local setup

### Installation

1. **Clone the repository and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Kafka services:**
   ```bash
   docker-compose up -d
   ```

3. **Configure environment variables:**
   - Create `.env` file with Supabase credentials
   - Configure Kafka broker URLs if different from localhost:9092

4. **Initialize the system:**
   ```bash
   python create_project.py
   ```

### Running the System

1. **Start the Kafka producer (generates transactions):**
   ```bash
   python engine/producer.py
   ```

2. **Start the Kafka consumer (processes transactions):**
   ```bash
   python engine/consumer.py
   ```

3. **Launch the dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```

## Key Features

✅ **Real-time Fraud Detection**: Multi-layer detection combining ML and rules  
✅ **Intelligent Investigation**: RAG-powered fraud case analysis  
✅ **User Behavior Analysis**: Profile-based and history-based detection  
✅ **Rule-Based Detection**: Country, device, velocity, amount, and behavior rules  
✅ **Streaming Architecture**: Kafka-based scalable transaction processing  
✅ **Interactive Dashboard**: Real-time alerts and fraud monitoring visualization  
✅ **Persistent Storage**: Supabase backend for audit trails and historical analysis

