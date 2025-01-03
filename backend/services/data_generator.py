from datetime import datetime, timedelta
import uuid
import random
from textblob import TextBlob

async def generate_mock_data(collection, num_records=100):
    """Generate mock data with advanced attributes."""
    post_types = ['carousel', 'reel', 'static']
    tags = ['#motivation', '#fitness', '#moviememe', '#cricketmeme']
    
    docs_to_insert = []
    for _ in range(num_records):
        post_type = random.choice(post_types)
        engagement_multiplier = {
            'carousel': 1.2,
            'reel': 1.5,
            'static': 1.0
        }[post_type]
        tag = random.choice(tags)
        caption = f"This is a post about {tag}."
        sentiment_score = TextBlob(caption).sentiment.polarity
        posted_date = datetime.utcnow() - timedelta(days=random.randint(0, 30))
        # Ensure the date key in the timeline is formatted correctly
        timeline = {(posted_date + timedelta(hours=i)).isoformat().replace(":", "_").replace(".", "_"): random.randint(0, 50) for i in range(6)}
        docs_to_insert.append({
            "_id": str(uuid.uuid4()),
            "post_type": post_type,
            "likes": int(random.randint(50, 500) * engagement_multiplier),
            "shares": int(random.randint(10, 100) * engagement_multiplier),
            "comments": int(random.randint(5, 50) * engagement_multiplier),
            "tags": [tag],
            "caption": caption,
            "impressions": random.randint(1000, 5000),
            "sentiment": sentiment_score,
            "posted_date": posted_date.isoformat(),
            "engagement_timeline": timeline
        })

    result = await collection.insert_many(docs_to_insert)
    print(f"Inserted {len(result.inserted_ids)} mock records.")