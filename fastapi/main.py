from fastapi import FastAPI
from fastapi.responses import JSONResponse
from elasticsearch import Elasticsearch
import os

app = FastAPI()

es_username = os.environ.get("ELASTICSEARCH_USERNAME", "elastic")
es_password = os.environ.get("ELASTICSEARCH_PASSWORD", "elastic")
es_hosts = os.environ.get("ELASTICSEARCH_HOSTS", "http://localhost:9200")
es = Elasticsearch(hosts=es_hosts, basic_auth=(es_username, es_password))

@app.get("/average-rating-by-company/{company_name}")
async def average_rating_by_company(company_name: str):
    res = es.search(index="companies_reviews", body={
        "query": {
            "match": {"company_name": company_name}
        },
        "aggs": {
            "average_rating": {
                "avg": {"field": "rating"}
            }
        }
    })
    return JSONResponse(content={"average_rating": res["aggregations"]["average_rating"]["value"]})


@app.get("/total-reviews-by-company/{company_name}")
async def total_reviews_by_company(company_name: str):
    res = es.count(index="companies_reviews", body={
        "query": {
            "match": {"company_name": company_name}
        }
    })
    return JSONResponse(content={"total_reviews": res["count"]})

@app.get("/rating-distribution-by-company/{company_name}")
async def rating_distribution_by_company(company_name: str):
    res = es.search(index="companies_reviews", body={
        "query": {
            "match": {"company_name": company_name}
        },
        "aggs": {
            "ratings": {
                "terms": {"field": "rating"}
            }
        }
    })
    ratings = res["aggregations"]["ratings"]["buckets"]
    distribution = {r["key"]: r["doc_count"] for r in ratings}
    return JSONResponse(content={"rating_distribution": distribution})

@app.get("/top-terms/{company_name}")
async def top_terms(company_name: str):
    res = es.search(index="companies_reviews", body={
        "query": {
            "match": {"company_name": company_name}
        },
        "aggs": {
            "top_title_terms": {
                "terms": {
                    "field": "title_keywords",
                    "exclude": "[.!,]"  # Exclude characters "." and "!" and ","
                }
            }
        }
    })
    top_title_terms = [(t["key"], t["doc_count"]) for t in res["aggregations"]["top_title_terms"]["buckets"]]
    return JSONResponse(content={"top_title_terms": top_title_terms})

@app.get("/average-sentiment-by-company/{company_name}")
async def average_sentiment_by_company(company_name: str):
    res = es.search(index="companies_reviews", body={
        "query": {
            "match": {"company_name": company_name}
        },
        "aggs": {
            "average_sentiment": {
                "avg": {"field": "sentiment_score"}
            }
        }
    })
    return JSONResponse(content={"average_sentiment": res["aggregations"]["average_sentiment"]["value"]})

@app.get("/average-accuracy-by-company/{company_name}")
async def average_accuracy_by_company(company_name: str):
    res = es.search(index="companies_reviews", body={
        "query": {
            "match": {"company_name": company_name}
        },
        "aggs": {
            "average_accuracy": {
                "avg": {"field": "accuracy_score"}
            }
        }
    })
    return JSONResponse(content={"average_accuracy": res["aggregations"]["average_accuracy"]["value"]})