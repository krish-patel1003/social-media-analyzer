from fastapi import FastAPI, Depends
from .utils.database import get_database
from .services.analyzer import EngagementAnalyzer
from .services.data_generator import generate_mock_data
from .services.insights import generate_insights

app = FastAPI(title="Social Media Analyzer API")

@app.post("/generate-data")
async def generate_data(num_records: int = 100, db=Depends(get_database)):
    collection = await db.get_collection("engagement_data")
    await generate_mock_data(collection, num_records)
    return {"message": f"Generated {num_records} mock records"}

@app.get("/analyze")
async def analyze_data(db=Depends(get_database)):
    collection = await db.get_collection("engagement_data")
    
    analyzer = EngagementAnalyzer()
    temporal_patterns = await analyzer.analyze_temporal_patterns(collection)
    tag_co_occurrence = await analyzer.analyze_tag_co_occurrence(collection)
    sentiment_impact = await analyzer.analyze_sentiment_impact(collection)
    post_lifespan = await analyzer.analyze_post_lifespan(collection)
    
    insights = generate_insights(
        temporal_patterns,
        tag_co_occurrence,
        sentiment_impact,
        post_lifespan
    )
    
    return {
        "temporal_patterns": temporal_patterns,
        "tag_co_occurrence": tag_co_occurrence,
        "sentiment_impact": sentiment_impact,
        "post_lifespan": post_lifespan,
        "insights": insights
    }